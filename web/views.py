from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from api.models import ScreeningEntity, Address, SearchQuery
from core.services.csl_service import csl_service
from core.constants.csl_constants import CSL_SOURCES, CSL_ENTITY_TYPES


def index(request):
    """Home page view"""
    # Get latest entities for display
    latest_entities = ScreeningEntity.objects.all().order_by('-updated_at')[:10]
    
    # Get search statistics
    total_entities = ScreeningEntity.objects.count()
    total_searches = SearchQuery.objects.count()
    source_lists = ScreeningEntity.objects.values_list('source_list', flat=True).distinct()
    
    context = {
        'latest_entities': latest_entities,
        'total_entities': total_entities,
        'total_searches': total_searches,
        'source_lists': source_lists,
    }
    
    return render(request, 'web/index.html', context)


def search(request):
    """Search page view"""
    query = request.GET.get('q', '')
    source_list = request.GET.get('source_list', '')
    entity_type = request.GET.get('entity_type', '')
    country = request.GET.get('country', '')
    address = request.GET.get('address', '')
    city = request.GET.get('city', '')
    state = request.GET.get('state', '')
    postal_code = request.GET.get('postal_code', '')
    page_number = request.GET.get('page', 1)
    use_api = request.GET.get('use_api', 'off') == 'on'
    
    entities = []
    total_results = 0
    
    if query:
        # Record search query
        SearchQuery.objects.create(
            query_text=query,
            results_count=0,  # Will be updated after search
            search_params={
                'source_list': source_list,
                'entity_type': entity_type,
                'country': country,
                'address': address,
                'city': city,
                'state': state,
                'postal_code': postal_code,
                'use_api': use_api
            }
        )
        
        if use_api:
            # Search using external API
            api_results = csl_service.search_entities(
                query=query,
                sources=[source_list] if source_list else None,
                countries=[country] if country else None,
                entity_types=[entity_type] if entity_type else None,
                address=address if address else None,
                city=city if city else None,
                state=state if state else None,
                postal_code=postal_code if postal_code else None
            )
            
            if 'results' in api_results:
                # Process and store results
                for entity_data in api_results.get('results', []):
                    csl_service.fetch_and_store_entity(entity_data)
                
                total_results = api_results.get('total', 0)
                messages.success(request, f"Found {total_results} results from the CSL API")
        
        # Query database for results
        queryset = ScreeningEntity.objects.all().order_by('-updated_at')  # Add explicit ordering to fix pagination warning
        
        if query:
            queryset = queryset.filter(name__icontains=query)
            
        if source_list:
            queryset = queryset.filter(source_list=source_list)
            
        if entity_type:
            queryset = queryset.filter(sdn_type=entity_type)
            
        if country:
            queryset = queryset.filter(addresses__country__iexact=country).distinct()
            
        if address:
            queryset = queryset.filter(addresses__address__icontains=address).distinct()
            
        if city:
            queryset = queryset.filter(addresses__city__iexact=city).distinct()
            
        if state:
            queryset = queryset.filter(addresses__state__iexact=state).distinct()
            
        if postal_code:
            queryset = queryset.filter(addresses__postal_code__iexact=postal_code).distinct()
        
        # Paginate results
        paginator = Paginator(queryset, 10)
        
        try:
            entities = paginator.page(page_number)
            total_results = queryset.count()
        except PageNotAnInteger:
            entities = paginator.page(1)
        except EmptyPage:
            entities = paginator.page(paginator.num_pages)
        
        # Update search query with result count
        search_query = SearchQuery.objects.filter(query_text=query).order_by('-timestamp').first()
        if search_query:
            search_query.results_count = total_results
            search_query.save()
    
    # Get list of available countries and source lists for filters
    countries = Address.objects.values_list('country', flat=True).distinct()
    db_source_lists = ScreeningEntity.objects.values_list('source_list', flat=True).distinct()
    
    context = {
        'query': query,
        'entities': entities,
        'total_results': total_results,
        'source_list': source_list,
        'entity_type': entity_type,
        'country': country,
        'address': address,
        'city': city,
        'state': state,
        'postal_code': postal_code,
        'countries': sorted(c for c in countries if c),
        'source_lists': sorted(db_source_lists),
        'csl_sources': CSL_SOURCES,  # Add CSL sources from constants
        'entity_types': CSL_ENTITY_TYPES,  # Add entity types from constants
        'use_api': use_api
    }
    
    return render(request, 'web/search.html', context)


def entity_detail(request, pk):
    """Entity detail page view"""
    entity = get_object_or_404(ScreeningEntity, pk=pk)
    
    context = {
        'entity': entity,
    }
    
    return render(request, 'web/entity_detail.html', context)


def about(request):
    """About page view"""
    return render(request, 'web/about.html')
