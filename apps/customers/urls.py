from django.urls import path

from . import views

app_name = 'customers'

urlpatterns = [
    path('', views.customer_list, name='customer_list'),
    path('add/', views.customer_add, name='customer_add'),
    path('<int:pk>/edit/', views.customer_edit, name='customer_edit'),
    path('<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    path('import/', views.customer_import, name='customer_import'),
    path('api/search/', views.customer_search_api, name='customer_search_api'),
    path('api/quick-create/', views.customer_quick_create, name='customer_quick_create'),
]
