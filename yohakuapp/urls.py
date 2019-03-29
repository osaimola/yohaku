from django.urls import path
from yohakuapp import views

app_name = "yohakuapp"
urlpatterns = [
    path('', views.index, name='index')
]