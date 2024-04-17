from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportActionModelAdmin

from .models import *
from import_export import resources

admin.site.site_header = "SERVIR Apps Portal"


# ----------------------------------------------------------------------------------------------------------------------
# Region admin page
# ----------------------------------------------------------------------------------------------------------------------
class RegionAdminResource(resources.ModelResource):
    class Meta:
        model = Region


class RegionAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    resource_class = RegionAdminResource


admin.site.register(Region, RegionAdmin)


# ----------------------------------------------------------------------------------------------------------------------
# Application Component admin page
# ----------------------------------------------------------------------------------------------------------------------

class ApplicationComponentResource(resources.ModelResource):
    class Meta:
        model = ApplicationComponent


class ApplicationComponentAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    ordering = ('name',)
    filter_horizontal = ('applications',)
    resource_class = ApplicationComponentResource


admin.site.register(ApplicationComponent, ApplicationComponentAdmin)


# ----------------------------------------------------------------------------------------------------------------------
# Application admin page
# Added inlines to show log entries and links
# ----------------------------------------------------------------------------------------------------------------------
class LogInline(admin.TabularInline):
    model = Log


class LinkInline(admin.TabularInline):
    model = Link


class ApplicationAdminResource(resources.ModelResource):
    class Meta:
        model = Application


class ApplicationAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    list_display = ('name', 'organization', 'active', 'shown', 'display_priority', 'incomplete_info')
    list_filter = ('active', 'shown', 'organization', 'deployment_environment')
    search_fields = ('name', 'organization__name')
    filter_horizontal = ('datasets', 'scientists', 'serviceareas', 'developers', 'application_components')
    ordering = ('name',)
    inlines = [LinkInline, LogInline, ]
    fieldsets = (
        ('Identification', {
            'fields': ('name', 'description', 'url', 'icon', 'organization', 'region', 'serviceareas',),
        }),
        ('Infrastructure', {
            'fields': (
            'deployment_environment', 'deployment_env_further_details', 'application_components', 'datasets',)
        }),
        ('AST Involvement', {
            'fields': ('ast_pi', 'ast_round',)
        }),
        ('Teams', {
            'fields': ('developers', 'scientists',)
        }),
        ('Repository & Documentation', {
            'fields': ('code_repo_url', 'design_documentation_url',)
        }),
        ('Status', {
            'fields': (
            'date_released', 'active', 'date_decommissioned', 'shown', 'display_priority', 'incomplete_info',)
        }),

    )
    resource_class = ApplicationAdminResource


admin.site.register(Application, ApplicationAdmin)


# ----------------------------------------------------------------------------------------------------------------------
# Link model admin page
# Added ModelResource to allow import/export
# ----------------------------------------------------------------------------------------------------------------------
class LinkAdminResource(resources.ModelResource):
    class Meta:
        model = Link


class LinkAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    list_display = ('application', 'url', 'description')
    list_filter = ('application',)
    search_fields = ('application__name', 'description', 'url', 'additional_description')
    ordering = ('application',)
    resource_class = LinkAdminResource


admin.site.register(Link, LinkAdmin)


# ----------------------------------------------------------------------------------------------------------------------
# Organization Area model admin page
# Added ModelResource to allow import/export
# ----------------------------------------------------------------------------------------------------------------------
class OrganizationResource(resources.ModelResource):
    class Meta:
        model = Organization


class OrganizationAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    list_display = ('name', 'description', 'url', 'date_added', 'date_modified')
    search_fields = ('name', 'description')
    ordering = ('name',)
    resource_class = OrganizationResource


admin.site.register(Organization, OrganizationAdmin)


# ----------------------------------------------------------------------------------------------------------------------
# Service Area model admin page
# Added ModelResource to allow import/export
# ----------------------------------------------------------------------------------------------------------------------
class ServiceAreaResource(resources.ModelResource):
    class Meta:
        model = ServiceArea


class ServiceAreaAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    list_display = ('name', 'description', 'service_catalog_url')
    search_fields = ('name', 'description')
    ordering = ('name',)
    filter_horizontal = ('applications',)
    resource_class = ServiceAreaResource


admin.site.register(ServiceArea, ServiceAreaAdmin)


# ----------------------------------------------------------------------------------------------------------------------
# Service model admin page
# Added ModelResource to allow import/export
# ----------------------------------------------------------------------------------------------------------------------
class ServiceResource(resources.ModelResource):
    class Meta:
        model = Service


class ServiceAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    list_display = ('name', 'description', 'service_area', 'service_catalog_url')
    list_filter = ('service_area',)
    search_fields = ('name', 'description')
    ordering = ('name',)
    resource_class = ServiceResource


admin.site.register(Service, ServiceAdmin)


# ----------------------------------------------------------------------------------------------------------------------
# Scientist model admin page
# Added ModelResource to allow import/export
# ----------------------------------------------------------------------------------------------------------------------
class DeveloperResource(resources.ModelResource):
    class Meta:
        model = Developer


class DeveloperAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    list_display = ('name', 'organization', 'active')
    list_filter = ('active', 'organization')
    search_fields = ('name',)
    ordering = ('name',)
    filter_horizontal = ('applications',)
    resource_class = DeveloperResource


admin.site.register(Developer, DeveloperAdmin)


# ----------------------------------------------------------------------------------------------------------------------
# Scientist model admin page
# Added AppInLine to show related applications
# Added ModelResource to allow import/export
# ----------------------------------------------------------------------------------------------------------------------
class ScientistResource(resources.ModelResource):
    class Meta:
        model = Scientist


class ScientistAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    list_display = ('name', 'organization', 'active')
    list_filter = ('active', 'organization')
    search_fields = ('name',)
    ordering = ('name',)
    filter_horizontal = ('applications',)
    # inlines = [AppInline, ]
    resource_class = ScientistResource


admin.site.register(Scientist, ScientistAdmin)


# ----------------------------------------------------------------------------------------------------------------------
# Log model admin page
# Added ModelResource to allow import/export
# ----------------------------------------------------------------------------------------------------------------------
class LogResource(resources.ModelResource):
    class Meta:
        model = Log


class LogAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    list_display = ('application', 'date_modified', 'log_entry')
    list_filter = ('application',)
    search_fields = ('application__name', 'log_entry')
    ordering = ('application',)
    date_hierarchy = 'date_added'
    resource_class = LogResource


admin.site.register(Log, LogAdmin)


# ----------------------------------------------------------------------------------------------------------------------
# Dataset model admin page
# Added ModelResource to allow import/export
# ----------------------------------------------------------------------------------------------------------------------
class DatasetResource(resources.ModelResource):
    class Meta:
        model = Dataset


class DatasetAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    list_display = ('name', 'description', 'date_added', 'date_modified')
    search_fields = ('name', 'description')
    ordering = ('name',)
    filter_horizontal = ('applications',)
    resource_class = DatasetResource


admin.site.register(Dataset, DatasetAdmin)


# ----------------------------------------------------------------------------------------------------------------------
# Development environment admin page
# Added AppInLine to show related applications
# Added ModelResource to allow import/export
# ----------------------------------------------------------------------------------------------------------------------
class AppInline(admin.TabularInline):
    model = Application
    fields = ('name', 'url', 'organization', 'active')


class DeploymentEnvironmentResource(resources.ModelResource):
    class Meta:
        model = DeploymentEnvironment


class DeploymentEnvironmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    ordering = ('name',)
    inlines = [AppInline, ]
    resource_class = DeploymentEnvironmentResource


admin.site.register(DeploymentEnvironment, DeploymentEnvironmentAdmin)
