from django.shortcuts import render
from .models import Application


apps = [
    {
        "id": 1,
        "name": "Carbon Monitoring",
        "image": "https://tethys.servirglobal.net/static/carbon_monitoring/images/icon.gif",
        "description": "This is info about the Carbon Monitoring",
        "color": "silver",
        "url": "https://apps.servirglobal.net/apps/carbonmonitoring/",
    },
    {
        "id": 2,
        "name": "Hydroviewer Nepal",
        "image": "https://apps.servirglobal.net/static/hydroviewer_nepal/images/logo.png",
        "description": "This is info about the Streamflow Prediction System",
        "color": "brown",
        "url":"http://tethys.icimod.org/apps/streamflownepal/",
    },
    {
        "id": 3,
        "name": "Hydroviewer Bangladesh",
        "image": "https://apps.servirglobal.net/static/hydroviewer_bangladesh/images/Bangladesh_Hiwat_Hidroviewer_Logo.png",
        "description": "This is info about the Streamflow Prediction System",
        "color": "blue",
        "url": "http://tethys.icimod.org/apps/hiwatbangladesh/"
    },
    {
        "id": 4,
        "name": "Water Watch",
        "image": "https://apps.servirglobal.net/static/waterwatch/images/logo_2.png",
        "description": "This is info about the Water Watch",
        "color": "red",
        "url": "https://apps.servirglobal.net/apps/waterwatch/"
    },
    {
        "id": 5,
        "name": "India AQX",
        "image": "https://apps.servirglobal.net/static/aqx_india/images/logo.png",
        "description": "This is info about the India AQX",
        "color": "silver",
        "url": "https://apps.servirglobal.net/apps/aqx-india/",
    },
    {
        "id": 6,
        "name": "Rheas Viewer",
        "image": "https://apps.servirglobal.net/static/rheasvieweroption2/images/logo.png",
        "description": "This is info about the Rheas Viewer",
        "color": "brown",
        "url":"https://apps.servirglobal.net/apps/rheasvieweroption2/",
    },
    {
        "id": 7,
        "name": "Water Quality E&S Africa",
        "image": "https://apps.servirglobal.net/static/waterq/images/icon.png",
        "description": "This is info about the Water Quality E&S Africa",
        "color": "blue",
        "url": "https://apps.servirglobal.net/apps/waterq/"
    },
    {
        "id": 8,
        "name": "Lower Mekong SWAT",
        "image": "https://apps.servirglobal.net/static/swat2/images/logo.png",
        "description": "This is info about the Lower Mekong SWAT",
        "color": "red",
        "url": "https://apps.servirglobal.net/apps/swat2/"
    },
]
# Create your views here.
def index(request):

    return render(request, "index.html", context={"apps": Application.objects.exclude(shown=False).all()})