from rest_framework import serializers
from .models import ScreeningEntity, Address, EntityID, SearchQuery


class AddressSerializer(serializers.ModelSerializer):
    """Serializer for Address model"""
    
    class Meta:
        model = Address
        fields = ['id', 'address', 'city', 'state', 'country', 'postal_code']


class EntityIDSerializer(serializers.ModelSerializer):
    """Serializer for EntityID model"""
    
    class Meta:
        model = EntityID
        fields = ['id', 'id_type', 'id_number', 'id_country', 'issue_date', 'expiration_date']


class ScreeningEntitySerializer(serializers.ModelSerializer):
    """Serializer for ScreeningEntity model with nested address and ID serializers"""
    
    addresses = AddressSerializer(many=True, read_only=True)
    ids = EntityIDSerializer(many=True, read_only=True)
    
    class Meta:
        model = ScreeningEntity
        fields = [
            'id', 'name', 'alt_names', 'source_list', 'source_information_url', 
            'source_list_url', 'programs', 'federal_register_notice', 
            'start_date', 'end_date', 'remarks', 'entity_number', 'sdn_type',
            'score', 'created_at', 'updated_at', 'source_id', 'addresses', 'ids'
        ]


class ScreeningEntityCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating ScreeningEntity with nested address and ID data
    """
    addresses = AddressSerializer(many=True, required=False)
    ids = EntityIDSerializer(many=True, required=False)
    
    class Meta:
        model = ScreeningEntity
        fields = [
            'id', 'name', 'alt_names', 'source_list', 'source_information_url', 
            'source_list_url', 'programs', 'federal_register_notice', 
            'start_date', 'end_date', 'remarks', 'entity_number', 'sdn_type',
            'score', 'source_id', 'addresses', 'ids'
        ]
    
    def create(self, validated_data):
        """Override create method to handle nested objects"""
        addresses_data = validated_data.pop('addresses', [])
        ids_data = validated_data.pop('ids', [])
        
        entity = ScreeningEntity.objects.create(**validated_data)
        
        # Create addresses
        for address_data in addresses_data:
            Address.objects.create(entity=entity, **address_data)
        
        # Create IDs
        for id_data in ids_data:
            EntityID.objects.create(entity=entity, **id_data)
        
        return entity
    
    def update(self, instance, validated_data):
        """Override update method to handle nested objects"""
        addresses_data = validated_data.pop('addresses', None)
        ids_data = validated_data.pop('ids', None)
        
        # Update ScreeningEntity fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update addresses if provided
        if addresses_data is not None:
            # Remove existing addresses
            instance.addresses.all().delete()
            # Create new addresses
            for address_data in addresses_data:
                Address.objects.create(entity=instance, **address_data)
        
        # Update IDs if provided
        if ids_data is not None:
            # Remove existing IDs
            instance.ids.all().delete()
            # Create new IDs
            for id_data in ids_data:
                EntityID.objects.create(entity=instance, **id_data)
        
        return instance


class SearchQuerySerializer(serializers.ModelSerializer):
    """Serializer for SearchQuery model"""
    
    class Meta:
        model = SearchQuery
        fields = ['id', 'query_text', 'results_count', 'user', 'timestamp', 'search_params']
        read_only_fields = ['id', 'timestamp']