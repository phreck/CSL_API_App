# Generated by Django 5.2 on 2025-04-09 18:09

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScreeningEntity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('alt_names', models.JSONField(blank=True, null=True)),
                ('source_list', models.CharField(max_length=100)),
                ('source_information_url', models.URLField(blank=True, max_length=255, null=True)),
                ('source_list_url', models.URLField(blank=True, max_length=255, null=True)),
                ('programs', models.JSONField(blank=True, null=True)),
                ('federal_register_notice', models.CharField(blank=True, max_length=255, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('entity_number', models.CharField(blank=True, max_length=100, null=True)),
                ('sdn_type', models.CharField(blank=True, max_length=100, null=True)),
                ('score', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('source_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
            ],
            options={
                'verbose_name': 'Screening Entity',
                'verbose_name_plural': 'Screening Entities',
                'indexes': [models.Index(fields=['name'], name='api_screeni_name_436db8_idx'), models.Index(fields=['source_list'], name='api_screeni_source__1e8ad0_idx'), models.Index(fields=['source_id'], name='api_screeni_source__516df6_idx')],
            },
        ),
        migrations.CreateModel(
            name='SearchQuery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query_text', models.CharField(max_length=255)),
                ('results_count', models.IntegerField(default=0)),
                ('user', models.CharField(blank=True, max_length=255, null=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('search_params', models.JSONField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Search Query',
                'verbose_name_plural': 'Search Queries',
                'indexes': [models.Index(fields=['query_text'], name='api_searchq_query_t_abb9a8_idx'), models.Index(fields=['timestamp'], name='api_searchq_timesta_dc9364_idx')],
            },
        ),
        migrations.CreateModel(
            name='EntityID',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_type', models.CharField(max_length=100)),
                ('id_number', models.CharField(max_length=255)),
                ('id_country', models.CharField(blank=True, max_length=255, null=True)),
                ('issue_date', models.DateField(blank=True, null=True)),
                ('expiration_date', models.DateField(blank=True, null=True)),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ids', to='api.screeningentity')),
            ],
            options={
                'verbose_name': 'Entity ID',
                'verbose_name_plural': 'Entity IDs',
                'indexes': [models.Index(fields=['id_type'], name='api_entityi_id_type_ee389c_idx'), models.Index(fields=['id_number'], name='api_entityi_id_numb_3ab5a9_idx')],
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(blank=True, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('state', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=50, null=True)),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='api.screeningentity')),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
                'indexes': [models.Index(fields=['country'], name='api_address_country_c6c93e_idx'), models.Index(fields=['city'], name='api_address_city_b3934e_idx')],
            },
        ),
    ]
