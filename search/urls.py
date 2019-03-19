from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    # トップ画面
    path('', views.IndexView.as_view(), name='index'),

    # 登録画面
    path('create/', views.CreateView.as_view(), name='create'),

    # 詳細画面
    path('search/<int:pk>/', views.DetailView.as_view(), name='detail'),
]