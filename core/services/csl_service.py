import requests
import logging
import os
from datetime import datetime
from django.conf import settings
from typing import Dict, List, Any, Optional, Union
from api.models import ScreeningEntity, Address, EntityID, SearchQuery

# Configure logger
logger = logging.getLogger(__name__)


class CSLService:
    """
    Service class for interacting with the Consolidated Screening List API.
    """
    
    def __init__(self):
        self.base_url = settings.CSL_API_URL
        self.subscription_key = settings.CSL_SUBSCRIPTION_KEY
        
        # Debug info about environment variables
        logger.info(f"CSL_API_URL from settings: '{self.base_url}'")
        logger.info(f"CSL_SUBSCRIPTION_KEY from settings: '{self.subscription_key}'")
        
        # Check if we can get them directly from os.environ
        logger.info(f"CSL_API_URL from os.environ: '{os.environ.get('CSL_API_URL')}'")
        logger.info(f"CSL_SUBSCRIPTION_KEY from os.environ: '{os.environ.get('CSL_SUBSCRIPTION_KEY')}'")
    
    def build_params(self, **kwargs) -> Dict[str, Any]:
        """
        Build query parameters for the CSL API request.
        
        Args:
            **kwargs: Various search parameters for the CSL API
            
        Returns:
            Dict of query parameters
        """
        params = {}
        
        # Add search parameters if provided
        for key, value in kwargs.items():
            if value:
                params[key] = value
                
        return params
    
    def fetch_data(self, **kwargs) -> Dict[str, Any]:
        """
        Fetch data from the CSL API with the provided parameters.
        
        Args:
            **kwargs: Various search parameters for the CSL API
            
        Returns:
            Response data from CSL API
        """
        params = self.build_params(**kwargs)
        
        # Set up headers with the API key
        # Ensure headers match exactly what the API expects
        headers = {
            'Cache-Control': 'no-cache',
            'subscription-key': self.subscription_key
        }
        
        # Log request details for debugging
        logger.debug(f"CSL API Request - URL: {self.base_url}")
        logger.debug(f"CSL API Request - Key: {self.subscription_key}")
        logger.debug(f"CSL API Request - Headers: {headers}")
        logger.debug(f"CSL API Request - Params: {params}")
        
        try:
            # Make the request with the properly formatted headers
            response = requests.get(self.base_url, params=params, headers=headers)
            
            # Log response details
            logger.debug(f"CSL API Response - Status Code: {response.status_code}")
            logger.debug(f"CSL API Response - Headers: {dict(response.headers)}")
            
            if response.status_code != 200:
                logger.error(f"CSL API Error - Status Code: {response.status_code}")
                logger.error(f"CSL API Error - Response: {response.text}")
                return {"error": f"API Error: {response.status_code}", "message": response.text}
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data from CSL API: {e}")
            return {"error": str(e)}
    
    def search_entities(self, query: str, sources: Optional[List[str]] = None,
                       countries: Optional[List[str]] = None, entity_types: Optional[List[str]] = None,
                       fuzzy_name: bool = True, address: Optional[str] = None, 
                       city: Optional[str] = None, state: Optional[str] = None,
                       postal_code: Optional[str] = None, size: int = 100, 
                       offset: int = 0, user: Optional[str] = None) -> Dict[str, Any]:
        """
        Search entities in the CSL API.
        
        Args:
            query: Search query string
            sources: List of source lists to search
            countries: List of countries to filter by
            entity_types: List of entity types to filter by
            fuzzy_name: Use fuzzy name matching
            address: Street address to search for
            city: City to search for
            state: State/province to search for
            postal_code: Postal code to search for
            size: Number of results to return (max 100)
            offset: Offset for pagination
            user: Optional user identifier for logging
            
        Returns:
            Search results with metadata
        """
        search_params = {
            'name': query,  # API uses 'name' not 'q'
            'sources': ','.join(sources) if sources else None,
            'countries': ','.join(countries) if countries else None,
            'types': ','.join(entity_types) if entity_types else None,
            'fuzzy_name': 'true' if fuzzy_name else 'false',
            'address': address,
            'city': city,
            'state': state,
            'postal_code': postal_code,
            'size': min(size, 100),  # Cap at 100 as per API limits
            'offset': offset
        }
        
        # Store search query in database
        search_query = SearchQuery.objects.create(
            query_text=query,
            results_count=0,  # Will update after getting results
            user=user,
            search_params=search_params
        )
        
        # Fetch results from API
        results = self.fetch_data(**search_params)
        
        # Update search query with result count
        if 'total' in results:
            search_query.results_count = results.get('total', 0)
            search_query.save()
        
        return results
    
    def fetch_and_store_entity(self, entity_data: Dict[str, Any]) -> ScreeningEntity:
        """
        Process an entity from API response and store in database.
        
        Args:
            entity_data: Dictionary containing entity data from CSL API
            
        Returns:
            Created or updated ScreeningEntity instance
        """
        # Extract address and ID data
        addresses_data = entity_data.pop('addresses', [])
        ids_data = entity_data.pop('ids', [])
        
        # Format dates properly
        for date_field in ['start_date', 'end_date']:
            if entity_data.get(date_field):
                try:
                    entity_data[date_field] = datetime.strptime(
                        entity_data[date_field], '%Y-%m-%d'
                    ).date()
                except (ValueError, TypeError):
                    entity_data[date_field] = None
        
        # Create or update entity
        source_id = entity_data.get('source_id') or entity_data.get('id')
        if not source_id:
            # Generate a composite ID if not provided
            source_id = f"{entity_data.get('source_list')}-{entity_data.get('name')}"
        
        entity, created = ScreeningEntity.objects.update_or_create(
            source_id=source_id,
            defaults={
                'name': entity_data.get('name', ''),
                'alt_names': entity_data.get('alt_names', []),
                'source_list': entity_data.get('source_list', ''),
                'source_information_url': entity_data.get('source_information_url'),
                'source_list_url': entity_data.get('source_list_url'),
                'programs': entity_data.get('programs', []),
                'federal_register_notice': entity_data.get('federal_register_notice'),
                'start_date': entity_data.get('start_date'),
                'end_date': entity_data.get('end_date'),
                'remarks': entity_data.get('remarks'),
                'entity_number': entity_data.get('entity_number'),
                'sdn_type': entity_data.get('sdn_type'),
                'score': entity_data.get('score', 0),
            }
        )
        
        # If entity was updated, clear existing related data
        if not created:
            entity.addresses.all().delete()
            entity.ids.all().delete()
        
        # Create addresses
        for addr_data in addresses_data:
            Address.objects.create(
                entity=entity,
                address=addr_data.get('address'),
                city=addr_data.get('city'),
                state=addr_data.get('state'),
                country=addr_data.get('country'),
                postal_code=addr_data.get('postal_code')
            )
        
        # Create IDs
        for id_data in ids_data:
            # Format dates for IDs
            issue_date = None
            expiration_date = None
            
            if id_data.get('issue_date'):
                try:
                    issue_date = datetime.strptime(id_data['issue_date'], '%Y-%m-%d').date()
                except (ValueError, TypeError):
                    pass
                    
            if id_data.get('expiration_date'):
                try:
                    expiration_date = datetime.strptime(id_data['expiration_date'], '%Y-%m-%d').date()
                except (ValueError, TypeError):
                    pass
            
            EntityID.objects.create(
                entity=entity,
                id_type=id_data.get('type', ''),
                id_number=id_data.get('number', ''),
                id_country=id_data.get('country'),
                issue_date=issue_date,
                expiration_date=expiration_date
            )
        
        return entity
    
    def fetch_and_store(self, **kwargs) -> Dict[str, Any]:
        """
        Fetch data from CSL API and store all entities in the database.
        
        Args:
            **kwargs: Search parameters for the CSL API
            
        Returns:
            Dictionary with results and metadata
        """
        results = self.fetch_data(**kwargs)
        entities_created = 0
        
        if 'results' in results:
            for entity_data in results['results']:
                self.fetch_and_store_entity(entity_data)
                entities_created += 1
        
        return {
            'total': results.get('total', 0),
            'entities_created': entities_created,
            'search_performed': kwargs
        }


# Singleton instance for reuse
csl_service = CSLService()