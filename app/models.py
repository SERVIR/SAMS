from django.db import models
from django.contrib.auth.models import User
from django import utils
from django.utils import timezone
from datetime import date

# models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


# ---------------------------------------------------------------------------------------------
# Application model - This is the main model for the application
# ---------------------------------------------------------------------------------------------
class Application(models.Model):
    name = models.CharField(help_text="Application name", max_length=250)
    description = models.TextField(help_text="Brief application description", blank=True)
    url = models.URLField(max_length=200, blank=True)
    icon = models.ImageField(upload_to='icons/', blank=True)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE,
                                     help_text="Organization that developed the application", blank=True)
    serviceareas = models.ManyToManyField('ServiceArea', blank=True)
    datasets = models.ManyToManyField('Dataset', blank=True)
    active = models.BooleanField(default=True, help_text="Is this application active?")
    shown = models.BooleanField(default=False, help_text="Is this application visible?")
    developers = models.ManyToManyField('Developer', blank=True, related_name='developers')
    # primary_developer = models.ForeignKey('Developer', on_delete=models.CASCADE, blank=True)
    scientists = models.ManyToManyField('Scientist', blank=True)
    code_repo_url = models.URLField(max_length=250, blank=True, help_text="Code repository location")
    design_documentation_url = models.URLField(max_length=250, blank=True, help_text="Design documentation location")
    application_components = models.ManyToManyField('ApplicationComponent', blank=True)
    platform_description = models.TextField(help_text="Brief description of platform used in the app", blank=True)
    deployment_environment = models.ManyToManyField('DeploymentEnvironment', blank=True)
    deployment_env_further_details = models.TextField(help_text="Further details about the deployment environment",
                                                      blank=True)
    date_released = models.DateField(default=utils.timezone.now,
                                     help_text="Approximate date the application was released")
    date_decommissioned = models.DateField(blank=True, null=True,
                                           help_text="Approximate date the application was decommissioned")
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    region = models.ManyToManyField('Region', blank=True)
    display_priority = models.IntegerField(help_text="Display priority (lower numbers shown at the top of the list)",
                                           default=10, blank=True)
    incomplete_info = models.BooleanField(default=True, help_text="Application needs more information added?")
    ast_pi = models.ForeignKey('Scientist', on_delete=models.CASCADE, related_name="PI_Scientist",
                               help_text="Scientist who is/was the PI when the application was developed",
                               blank=True, default=None, null=True)
    ast_round = models.IntegerField(help_text="AST round they were involved with when the app was created",
                                    default=None, blank=True, null=True)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('detail', kwargs={'post_id': self.pk})

    def like_count(self):
        return self.like_set.count()

    def __str__(self):
        return self.name

# ---------------------------------------------------------------------------------------------
# "Like" model - To register likes for the applications
# ---------------------------------------------------------------------------------------------
class Like(models.Model):
    application = models.ForeignKey('Application', on_delete=models.CASCADE, default=None, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f"{self.user.username} likes {self.application.name}"

    class Meta:
        unique_together = ('user', 'application')  # Ensures a user can only like an application once



# ---------------------------------------------------------------------------------------------
# Organization model - To identify the organizations associated with the applications
# ---------------------------------------------------------------------------------------------
class Organization(models.Model):
    name = models.CharField(help_text="Name of the organization", max_length=250)
    description = models.TextField()
    url = models.URLField(max_length=200)
    icon = models.ImageField(upload_to='icons/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------------------------
# Service Area model - To identify the service areas associated with the applications
# ---------------------------------------------------------------------------------------------
class ServiceArea(models.Model):
    name = models.CharField(help_text="Name of the service area", max_length=250)
    description = models.TextField()
    service_catalog_url = models.URLField(max_length=200, blank=True,
                                          help_text="Reference to the SERVIR Service catalog")
    icon = models.ImageField(upload_to='icons/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    applications = models.ManyToManyField('Application', through=Application.serviceareas.through, blank=True)

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------------------------
# Services model - For future connection to the service catalog
# ---------------------------------------------------------------------------------------------
class Service(models.Model):
    name = models.CharField(help_text="Service Name", max_length=250)
    description = models.TextField()
    service_area = models.ForeignKey(ServiceArea, on_delete=models.CASCADE)
    service_catalog_url = models.URLField(max_length=200, help_text="Reference to the SERVIR Service catalog")
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------------------------
# Log model - For tracking changes & issues regarding specific applications
# ---------------------------------------------------------------------------------------------
class Log(models.Model):
    application = models.ForeignKey('Application', on_delete=models.CASCADE)
    log_entry = models.TextField()
    date = models.DateField(help_text="Date issue or milestone happened", blank=True, default=date.today)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logs', default=7)  # Add this line

    def __str__(self):
        return self.application.name


# ---------------------------------------------------------------------------------------------
# Feedback model - For feedback regarding specific applications
# ---------------------------------------------------------------------------------------------
class Feedback(models.Model):
    application = models.ForeignKey('Application', on_delete=models.CASCADE, default=None, null=True)
    feedback_entry = models.TextField()
    date = models.DateField(help_text="Date feedback reported", blank=True, default=date.today)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback', default=7)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)




# ---------------------------------------------------------------------------------------------
# Deployment environments - To track where the application is deployed
# ---------------------------------------------------------------------------------------------
class DeploymentEnvironment(models.Model):
    name = models.CharField(help_text="Name of the deployment environment", max_length=250)
    description = models.TextField(help_text="Brief description of the deployment environment", blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    applications = models.ManyToManyField('Application', through=Application.deployment_environment.through, blank=True)

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------------------------
# Region model - To track SERVIR regions where the application is used
# ---------------------------------------------------------------------------------------------
class Region(models.Model):
    name = models.CharField(help_text="Name of the region",
                            max_length=250)
    accronym = models.CharField(help_text="Region accronym", max_length=4, blank=True)
    organization = models.ManyToManyField('Organization', blank=True)

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------------------------
# Dataset model - To track datasets used in the applications
# ---------------------------------------------------------------------------------------------
class Dataset(models.Model):
    name = models.CharField(help_text="Name of the dataset", max_length=250)
    description = models.TextField(help_text="Brief description of the dataset", blank=True)
    url = models.URLField(max_length=200, blank=True, help_text="Dataset location")
    credentials = models.TextField(help_text="Credentials for accessing the dataset", blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    applications = models.ManyToManyField('Application', through=Application.datasets.through, blank=True)

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------------------------
# Application component model - To track application components used in the applications
# ---------------------------------------------------------------------------------------------
class ApplicationComponent(models.Model):
    name = models.CharField(help_text="Name of the application component (indicate version if relevant)",
                            max_length=250)
    description = models.TextField(help_text="Further details for the application component", blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    applications = models.ManyToManyField('Application', through=Application.application_components.through, blank=True)

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------------------------
# Developer model - To track developers of the applications
# ---------------------------------------------------------------------------------------------
class Developer(models.Model):
    name = models.CharField(help_text="Name of the developer", max_length=250)
    photo = models.ImageField(upload_to='icons/',
                              blank=True, null=True,
                              help_text="Square image, minimum 150px X 150px")
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    active = models.BooleanField(default=True, help_text="Is the developer active?")
    applications = models.ManyToManyField('Application', through=Application.developers.through, blank=True)

    @property
    def image_url(self):
        if self.photo:
            return self.photo.url
        else:
            return "/static/app/img/no_profile.png"

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------------------------
# Scientist model - To track scientists involved in defining the applications
# ---------------------------------------------------------------------------------------------
class Scientist(models.Model):
    name = models.CharField(help_text="Name of the developer", max_length=250)
    photo = models.ImageField(upload_to='icons/',
                              blank=True,
                              null=True,
                              help_text="Square image, minimum 150px X 150px")
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    active = models.BooleanField(default=True, help_text="Is the scientist active?")
    applications = models.ManyToManyField('Application', through=Application.scientists.through, blank=True)

    @property
    def image_url(self):
        if self.photo:
            return self.photo.url
        else:
            return "/static/app/img/no_profile.png"

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------------------------
# Link model - To track links to additional resources for the applications
# ---------------------------------------------------------------------------------------------
class Link(models.Model):
    url = models.URLField(max_length=200, blank=True, help_text="Link location")
    description = models.CharField(help_text="Link Description", max_length=250, blank=True)
    additional_description = models.TextField(help_text="Further details for the link", blank=True)
    application = models.ForeignKey('Application', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.url


# ---------------------------------------------------------------------------------------------
# ExternalApp model - To track third party applications of interest to SERVIR
# ---------------------------------------------------------------------------------------------
class ExternalApp(models.Model):
    url = models.URLField(max_length=255, help_text="Primary URL of the application", blank=True)
    serviceareas = models.ManyToManyField('ServiceArea', blank=True)
    name = models.CharField(help_text="Application name", max_length=250)
    description = models.TextField(help_text="Brief description. Why is the app relevant for SERVIR?", blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ExternalApps', default=7)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
