from django.contrib import admin
from .models import ScreeningEntity, Address, EntityID, SearchQuery

class AddressInline(admin.TabularInline):
    model = Address
    extra = 0

class EntityIDInline(admin.TabularInline):
    model = EntityID
    extra = 0

@admin.register(ScreeningEntity)
class ScreeningEntityAdmin(admin.ModelAdmin):
    list_display = ('name', 'source_list', 'entity_number', 'created_at', 'updated_at')
    list_filter = ('source_list', 'sdn_type')
    search_fields = ('name', 'alt_names', 'source_list', 'entity_number')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [AddressInline, EntityIDInline]
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'alt_names', 'source_list', 'source_id', 'entity_number', 'sdn_type')
        }),
        ('Details', {
            'fields': ('source_information_url', 'source_list_url', 'programs', 
                      'federal_register_notice', 'start_date', 'end_date', 'remarks')
        }),
        ('Metadata', {
            'fields': ('score', 'created_at', 'updated_at')
        }),
    )

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('entity', 'country', 'city', 'address')
    list_filter = ('country',)
    search_fields = ('entity__name', 'country', 'city', 'address')

@admin.register(EntityID)
class EntityIDAdmin(admin.ModelAdmin):
    list_display = ('entity', 'id_type', 'id_number', 'id_country')
    list_filter = ('id_type', 'id_country')
    search_fields = ('entity__name', 'id_type', 'id_number')

@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ('query_text', 'results_count', 'user', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('query_text', 'user')
    readonly_fields = ('timestamp',)
