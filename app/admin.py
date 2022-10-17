from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportActionModelAdmin

from .models import *
from import_export import resources

admin.site.site_header = "SERVIR Apps Portal"


class RegionAdminResource(resources.ModelResource):
    class Meta:
        model = Region


class RegionAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    resource_class = RegionAdminResource


admin.site.register(Region, RegionAdmin)


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
# Added inline to show log entries
# ----------------------------------------------------------------------------------------------------------------------
class LogInline(admin.TabularInline):
    model = Log


class ApplicationAdminResource(resources.ModelResource):
    class Meta:
        model = Application


class ApplicationAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    list_display = ('name', 'organization', 'active', 'shown', 'display_priority', 'incomplete_info')
    list_filter = ('active', 'shown', 'organization', 'deployment_environment', 'primary_developer')
    search_fields = ('name', 'organization__name')
    filter_horizontal = ('datasets', 'scientists', 'serviceareas', 'developers', 'application_components')
    ordering = ('name',)
    inlines = [LogInline, ]
    resource_class = ApplicationAdminResource


admin.site.register(Application, ApplicationAdmin)


class OrganizationResource(resources.ModelResource):
    class Meta:
        model = Organization


class OrganizationAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    list_display = ('name', 'description', 'url', 'date_added', 'date_modified')
    search_fields = ('name', 'description')
    ordering = ('name',)
    resource_class = OrganizationResource


admin.site.register(Organization, OrganizationAdmin)


class ServiceAreaResource(resources.ModelResource):
    class Meta:
        model = ServiceArea


class ServiceAreaAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    list_display = ('name', 'description', 'service_catalog_url')
    search_fields = ('name', 'description')
    ordering = ('name',)
    resource_class = ServiceAreaResource


admin.site.register(ServiceArea, ServiceAreaAdmin)


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


class ScientistResource(resources.ModelResource):
    class Meta:
        model = Scientist


class ScientistAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    list_display = ('name', 'organization', 'active')
    list_filter = ('active', 'organization')
    search_fields = ('name',)
    ordering = ('name',)
    filter_horizontal = ('applications',)
    resource_class = ScientistResource


admin.site.register(Scientist, ScientistAdmin)


class LogResource(resources.ModelResource):
    class Meta:
        model = Log


class LogAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    list_display = ('application', 'log_entry', 'date_added', 'date_modified')
    list_filter = ('application',)
    search_fields = ('application__name', 'log_entry')
    ordering = ('application',)
    date_hierarchy = 'date_added'
    resource_class = LogResource


admin.site.register(Log, LogAdmin)


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
# Added inline to show log entries
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
