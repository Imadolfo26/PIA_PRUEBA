from django.urls import path
from . import views  

app_name = 'pedidos'

urlpatterns = [
    path('login/', views.v_login, name='login'),
    path('registro/', views.v_registro, name='registro'),
    path('mesero/', views.v_mesero, name='adminMesero'),
    path('mesero/crear/', views.v_crear_pedido, name='crear_pedido'),
    path('mesero/editar/<int:id_pedido>/', views.v_editar_pedido, name='editar_pedido'),
    path('mesero/eliminar/<int:id_pedido>/', views.v_eliminar_pedido, name='eliminar_pedido'),
    path('chef/', views.v_chef, name='adminChef'),
    path('chef/aceptar/<int:id_pedido>/', views.v_aceptar_pedido, name='aceptar_pedido'),
]