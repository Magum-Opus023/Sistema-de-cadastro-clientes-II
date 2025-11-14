from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina_inicial, name='pagina_inicial'),
    path('clientes/', views.cliente_list, name='cliente_list'),
    path('cliente/novo/', views.criar_cliente, name='criar_cliente'),
    path('cliente/editar/<int:pk>/', views.atualizar_cliente, name='atualizar_cliente'),
    path('cliente/excluir/<int:pk>/', views.excluir_cliente, name='excluir_cliente'),
    path('contas/login/', views.login_view, name='login'),
    path('contas/registro/', views.registrar_view, name='registro'),
    path('contas/logout/', views.logout_view, name='logout'),
]