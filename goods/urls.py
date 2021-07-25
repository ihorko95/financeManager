from django.urls import path, include

from goods.views import indexPage

urlpatterns = [
    path('', indexPage)
]