from django.contrib import admin
from .models import Application, Organization, ServiceArea, Service, Developer, Scientist, Log, Dataset, \
    DeploymentEnvironment, ApplicationComponent, Region

admin.site.site_header = "SERVIR Apps Portal"

admin.site.register(Region)


# Registering models here.
@admin.register(ApplicationComponent)
class ApplicationComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    ordering = ('name',)
    filter_horizontal = ('applications',)

# ----------------------------------------------------------------------------------------------------------------------
# Application admin page
# Added inline to show log entries
# ----------------------------------------------------------------------------------------------------------------------
class LogInline(admin.TabularInline):
    model = Log

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'active', 'shown', 'display_priority', 'incomplete_info')
    list_filter = ('active', 'shown', 'organization', 'deployment_environment', 'primary_developer')
    search_fields = ('name', 'organization__name')
    filter_horizontal = ('datasets', 'scientists', 'serviceareas', 'developers', 'application_components')
    ordering = ('name',)
    inlines = [LogInline,]


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'url', 'date_added', 'date_modified')
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(ServiceArea)
class ServiceAreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'service_catalog_url')
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'service_area', 'service_catalog_url')
    list_filter = ('service_area',)
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'active')
    list_filter = ('active', 'organization')
    search_fields = ('name',)
    ordering = ('name',)
    filter_horizontal = ('applications',)


@admin.register(Scientist)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'active')
    list_filter = ('active', 'organization')
    search_fields = ('name',)
    ordering = ('name',)
    filter_horizontal = ('applications',)



@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('application', 'log_entry', 'date_added', 'date_modified')
    list_filter = ('application',)
    search_fields = ('application__name', 'log_entry')
    ordering = ('application',)
    date_hierarchy = 'date_added'


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'date_added', 'date_modified')
    search_fields = ('name', 'description')
    ordering = ('name',)
    filter_horizontal=('applications',)

# ----------------------------------------------------------------------------------------------------------------------
# Development environment admin page
# Added inline to show log entries
# ----------------------------------------------------------------------------------------------------------------------
class AppInline(admin.TabularInline):
    model = Application
    fields = ('name', 'url', 'organization', 'active')

@admin.register(DeploymentEnvironment)
class DeploymentEnvironmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    ordering = ('name',)
    inlines = [AppInline,]
