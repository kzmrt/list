from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    # トップ画面
    path('', views.IndexView.as_view(), name='index'),
]