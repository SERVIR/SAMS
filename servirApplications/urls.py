"""servirApplications URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from app import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('detail/<int:post_id>', views.detail, name='detail'),
    path('toggle-like/<int:app_id>/', views.toggle_like, name='toggle_like'),
    path('developer/<int:post_id>', views.developer, name='developer'),
    path('scientist/<int:post_id>', views.scientist, name='scientist'),
    path('app-table/', views.app_table, name='app-table'),
    path('log-submit/', views.log_submit, name='log-submit'),
    path('feedback-submit/', views.feedback_submit, name='feedback-submit'),
    path('general-feedback-submit/', views.general_feedback_submit, name='general-feedback-submit'),
    path('fill_information/', views.fill_information, name='fill_information'),
    path('login', views.login),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)