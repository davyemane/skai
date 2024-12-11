from django.urls import path
from . import views

urlpatterns = [
    path('connect-db/', views.connect_db, name='connect_db'),
    path('list-connections/', views.list_connections, name='list_connections'),
    path('execute-query/', views.execute_query, name='execute_query'),

]
