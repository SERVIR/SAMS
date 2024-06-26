from django import forms
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


# ----------------------------------------------------------------------------------------------------------------------
# Application admin page
# Added inlines to show feedback entries and links
# ----------------------------------------------------------------------------------------------------------------------
class FeedbackInline(admin.TabularInline):
    model = Feedback


class LinkInline(admin.TabularInline):
    model = Link


class ApplicationAdminResource(resources.ModelResource):
    class Meta:
        model = Application


class ApplicationAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    list_display = ('name', 'organization', 'active', 'shown', 'display_priority', 'incomplete_info', 'total_likes')
    list_filter = ('active', 'shown', 'ast_round', 'organization')
    search_fields = ('name', 'description', 'organization__name')
    filter_horizontal = (
        'datasets', 'scientists', 'serviceareas', 'developers', 'deployment_environment', 'application_components')
    ordering = ('name',)
    inlines = [LinkInline, LogInline, FeedbackInline]
    readonly_fields = ('total_likes',)
    fieldsets = (
        ('Identification', {
            'fields': ('name', 'description', 'total_likes', 'url', 'icon', 'organization', 'region', 'serviceareas',),
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

    def total_likes(self, obj):
        return obj.like_count()

    total_likes.short_description = 'Total Likes'


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
    list_display = ('application', 'date_modified', 'log_entry', 'user')
    list_filter = ('application',)
    search_fields = ('application__name', 'log_entry', 'user__username')
    ordering = ('application',)
    date_hierarchy = 'date_added'
    resource_class = LogResource


admin.site.register(Log, LogAdmin)


# ----------------------------------------------------------------------------------------------------------------------
# Log model admin page
# Added ModelResource to allow import/export
# ----------------------------------------------------------------------------------------------------------------------
class FeedbackAdminForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['application'].required = False


class FeedbackResource(resources.ModelResource):
    class Meta:
        model = Feedback


class FeedbackAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    form = FeedbackAdminForm
    list_display = ('application', 'date_modified', 'feedback_entry', 'user', 'resolved')
    list_filter = ('application', 'resolved')
    search_fields = ('application__name', 'feedback_entry', 'user__username')
    ordering = ('application',)
    date_hierarchy = 'date_added'
    resource_class = FeedbackResource


admin.site.register(Feedback, FeedbackAdmin)


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
    filter_horizontal = ('applications',)
    resource_class = DeploymentEnvironmentResource


admin.site.register(DeploymentEnvironment, DeploymentEnvironmentAdmin)

admin.site.register(Like)


# ----------------------------------------------------------------------------------------------------------------------
# ExternalApp admin page
# Added ModelResource to allow import/export
# ----------------------------------------------------------------------------------------------------------------------
class ExternalAppResource(resources.ModelResource):
    class Meta:
        model = ExternalApp

class ExternalAppAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin):
    list_display = ('name', 'description', 'url', 'user', 'date_added')
    search_fields = ('name', 'description', 'url', 'user')
    ordering = ('name',)
    filter_horizontal = ('serviceareas',)
    date_hierarchy = 'date_added'

admin.site.register(ExternalApp, ExternalAppAdmin)