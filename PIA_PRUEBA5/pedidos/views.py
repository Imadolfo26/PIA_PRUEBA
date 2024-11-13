from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import PEDIDO
from .forms import LoginForm, RegistroForm, PedidoForm

# Create your views here.

# Vista para el login
def v_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cuenta = form.cleaned_data['cuenta'].upper()
            contrasena = form.cleaned_data['contrasena']
            user = authenticate(request, username=cuenta, password=contrasena)
            if user is not None:
                login(request, user)
                if user.usuario.rol == 1:  # Si es mesero
                    return redirect(reverse('pedidos:adminMesero')) 
                elif user.usuario.rol == 2:  # Si es chef
                    return redirect('pedidos:adminChef')  
            else:
                form.add_error(None, "Los datos son incorrectos.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# Vista para el registro
def v_registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return render(request, 'registro.html', {'registro_exitoso': True, 'form': form})
            except Exception as e:
                form.add_error(None, 'El nombre de usuario ya está en uso.')
                return render(request, 'registro.html', {'form': form, 'registro_exitoso': False})
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form, 'registro_exitoso': False})

# Vistas para MESERO

# Vista de lista de pedidos
@login_required
def v_mesero(request):
    if request.user.usuario.rol != 1:  # Verificar si es un mesero
        return redirect('pedidos:login')
    
    pedidos = PEDIDO.objects.all().order_by('estatus')  # Obtener pedidos ordenados por el estado
    
    # Configurar la paginación
    paginator = Paginator(pedidos, 5)  # Mostrar 5 pedidos por página
    page_number = request.GET.get('page')  # Obtener el número de página de la URL
    page_obj = paginator.get_page(page_number)  # Obtener la página actual
    
    return render(request, 'adminMesero.html', {'pedidos': page_obj})

# Vista para crear un nuevo pedido
@login_required
def v_crear_pedido(request):
    if request.user.usuario.rol != 1:  # Verificar si es un mesero
        return redirect('pedidos:login')
    
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.idUsuarioRegistro = request.user.usuario  # Asignar el mesero actual como creador del pedido
            pedido.estatus = 1 # El pedido comienza con el estatus 'CREADO'
            pedido.save()
            messages.success(request, 'Pedido creado exitosamente.')
            return render(request, 'crearPedido.html', {'form': form, 'pedido_creado': True})
    else:
        form = PedidoForm()
    return render(request, 'crearPedido.html', {'form': form})

# Vista para editar un pedido existente
@login_required
def v_editar_pedido(request, id_pedido):
    if request.user.usuario.rol != 1:  # Verificar si es un mesero
        return redirect('pedidos:login')
    
    pedido = get_object_or_404(PEDIDO, idPedido=id_pedido)

    # Verificar si el pedido ya está aceptado y no permitir la edición si lo está
    if pedido.estatus != 1:  # Si no está en estado 'CREADO'
        messages.error(request, 'No puedes editar este pedido, ya ha sido aceptado.')
        return redirect('pedidos:adminMesero')
    
    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pedido actualizado exitosamente.')
            return render(request, 'editarPedido.html', {'form': form, 'pedido': pedido, 'pedido_actualizado': True})
    else:
        form = PedidoForm(instance=pedido)
    return render(request, 'editarPedido.html', {'form': form, 'pedido': pedido})

# Vista para eliminar un pedido
@login_required
def v_eliminar_pedido(request, id_pedido):
    if request.user.usuario.rol != 1:  # Verificar si es un mesero
        return redirect('pedidos:login')
    
    pedido = get_object_or_404(PEDIDO, idPedido=id_pedido, estatus=1)  # Solo se pueden eliminar pedidos con estatus 'CREADO'
    
    if request.method == 'POST':
        pedido.delete()
        messages.success(request, 'Pedido eliminado exitosamente.')
        return redirect('pedidos:adminMesero')
    
    messages.error(request, 'Operación no permitida.')
    return redirect('pedidos:adminMesero')

# Vistas para CHEF

# Vista de lista de pedidos
@login_required
def v_chef(request):
    if request.user.usuario.rol != 2:  # Verifica que el usuario sea un chef
        return redirect('pedidos:login')
    
    pedidos = PEDIDO.objects.select_related('idUsuarioRegistro').all().order_by('estatus')  # Obtiene todos los pedidos relacionados al idUsuarioRegistro ordenados por el estado

    # Configurar la paginación
    paginator = Paginator(pedidos, 5)  # Mostrar 5 pedidos por página
    page_number = request.GET.get('page')  # Obtener el número de página de la URL
    page_obj = paginator.get_page(page_number)  # Obtener la página actual
    
    return render(request, 'adminChef.html', {'pedidos': page_obj})

# Vista para que el chef pueda aceptar los pedidos
@login_required
def v_aceptar_pedido(request, id_pedido):
    if request.user.usuario.rol != 2:  # Verifica que el usuario sea chef
        return redirect('pedidos:login')

    try:
        pedido = PEDIDO.objects.get(idPedido=id_pedido)
        if pedido.estatus == 1:  # Solo permite aceptar si el pedido está en estado 'CREADO'
            pedido.estatus = 2  # Cambia el estado a 'ACEPTADO'
            pedido.save()
            messages.success(request, 'El pedido ha sido aceptado.')
    except PEDIDO.DoesNotExist:
        messages.error(request, 'El pedido no existe.')

    return redirect('pedidos:adminChef')
