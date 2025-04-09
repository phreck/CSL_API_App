from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

from .models import ScreeningEntity, Address, EntityID, SearchQuery
from .serializers import (
    ScreeningEntitySerializer,
    ScreeningEntityCreateUpdateSerializer,
    AddressSerializer,
    EntityIDSerializer,
    SearchQuerySerializer
)
from core.services.csl_service import csl_service


class StandardResultsSetPagination(PageNumberPagination):
    """Standard pagination class for API views"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class ScreeningEntityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing ScreeningEntity instances.
    """
    queryset = ScreeningEntity.objects.all().order_by('-updated_at')
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['source_list', 'entity_number', 'sdn_type']
    search_fields = ['name', 'alt_names', 'remarks']
    ordering_fields = ['name', 'created_at', 'updated_at', 'score']
    
    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action in ['create', 'update', 'partial_update']:
            return ScreeningEntityCreateUpdateSerializer
        return ScreeningEntitySerializer
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Custom action to search entities using complex criteria
        """
        query = request.query_params.get('q', '')
        source_list = request.query_params.get('source_list')
        country = request.query_params.get('country')
        
        # Start with all entities
        queryset = self.get_queryset()
        
        # Apply filters based on parameters
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(alt_names__icontains=query)
            )
        
        if source_list:
            queryset = queryset.filter(source_list=source_list)
        
        if country:
            queryset = queryset.filter(addresses__country__iexact=country)
        
        # Apply pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def external_search(self, request):
        """
        Search using the external CSL API and store results
        """
        query = request.query_params.get('q', '')
        if not query:
            return Response(
                {"error": "Search query parameter 'q' is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Extract additional parameters
        sources = request.query_params.get('sources', '').split(',') if request.query_params.get('sources') else None
        countries = request.query_params.get('countries', '').split(',') if request.query_params.get('countries') else None
        fuzzy_name = request.query_params.get('fuzzy_name', 'true').lower() == 'true'
        size = int(request.query_params.get('size', '20'))
        offset = int(request.query_params.get('offset', '0'))
        
        # Get user information if available
        user = request.user.username if request.user.is_authenticated else None
        
        # Search using CSL service
        results = csl_service.search_entities(
            query=query,
            sources=sources,
            countries=countries,
            fuzzy_name=fuzzy_name,
            size=size,
            offset=offset,
            user=user
        )
        
        # Store entities in database
        if 'results' in results and results['results']:
            for entity_data in results['results']:
                csl_service.fetch_and_store_entity(entity_data)
        
        return Response(results)
    
    @action(detail=False, methods=['get'])
    def source_lists(self, request):
        """
        Get a list of all source lists
        """
        source_lists = ScreeningEntity.objects.values_list('source_list', flat=True).distinct()
        return Response(sorted(source_lists))


class AddressViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing Address instances.
    """
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['country', 'city']
    
    @action(detail=False, methods=['get'])
    def countries(self, request):
        """
        Get a list of all countries
        """
        countries = Address.objects.values_list('country', flat=True).distinct()
        return Response(sorted(country for country in countries if country))


class EntityIDViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing EntityID instances.
    """
    queryset = EntityID.objects.all()
    serializer_class = EntityIDSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id_type', 'id_country']


class SearchQueryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing search history.
    """
    queryset = SearchQuery.objects.all().order_by('-timestamp')
    serializer_class = SearchQuerySerializer
    pagination_class = StandardResultsSetPagination
