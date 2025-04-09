from django.db import models
from django.utils import timezone


class ScreeningEntity(models.Model):
    """
    Main model for storing Consolidated Screening List entities.
    """
    name = models.CharField(max_length=255)
    alt_names = models.JSONField(blank=True, null=True)  # Store alternative names as JSON
    source_list = models.CharField(max_length=100)
    source_information_url = models.URLField(max_length=255, blank=True, null=True)
    source_list_url = models.URLField(max_length=255, blank=True, null=True)
    programs = models.JSONField(blank=True, null=True)  # Store programs as JSON array
    federal_register_notice = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    entity_number = models.CharField(max_length=100, blank=True, null=True)
    sdn_type = models.CharField(max_length=100, blank=True, null=True)  # Specially Designated Nationals type
    score = models.IntegerField(default=0)  # For search relevance
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # API identifier from source
    source_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Screening Entity"
        verbose_name_plural = "Screening Entities"
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['source_list']),
            models.Index(fields=['source_id']),
        ]


class Address(models.Model):
    """
    Model for storing addresses associated with a screening entity.
    """
    entity = models.ForeignKey(ScreeningEntity, related_name='addresses', on_delete=models.CASCADE)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        parts = []
        if self.address:
            parts.append(self.address)
        if self.city:
            parts.append(self.city)
        if self.country:
            parts.append(self.country)
        
        return ", ".join(parts) or "No address details"
    
    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
        indexes = [
            models.Index(fields=['country']),
            models.Index(fields=['city']),
        ]


class EntityID(models.Model):
    """
    Model for storing identification documents associated with a screening entity.
    """
    entity = models.ForeignKey(ScreeningEntity, related_name='ids', on_delete=models.CASCADE)
    id_type = models.CharField(max_length=100)
    id_number = models.CharField(max_length=255)
    id_country = models.CharField(max_length=255, blank=True, null=True)
    issue_date = models.DateField(blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.id_type}: {self.id_number}"
    
    class Meta:
        verbose_name = "Entity ID"
        verbose_name_plural = "Entity IDs"
        indexes = [
            models.Index(fields=['id_type']),
            models.Index(fields=['id_number']),
        ]


class SearchQuery(models.Model):
    """
    Model for storing search queries to the CSL API.
    """
    query_text = models.CharField(max_length=255)
    results_count = models.IntegerField(default=0)
    user = models.CharField(max_length=255, blank=True, null=True)  # Optional user identifier
    timestamp = models.DateTimeField(default=timezone.now)
    search_params = models.JSONField(blank=True, null=True)  # Store search parameters as JSON
    
    def __str__(self):
        return f"{self.query_text} ({self.results_count} results)"
    
    class Meta:
        verbose_name = "Search Query"
        verbose_name_plural = "Search Queries"
        indexes = [
            models.Index(fields=['query_text']),
            models.Index(fields=['timestamp']),
        ]
