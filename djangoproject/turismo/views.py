from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Producto, CarritoItem, Carrito
from .forms import ProductoForm, CarritoItemForm

def index(request):
    productos = Producto.objects.all()
    return render(request, 'turismo/index.html', {'productos': productos})

def producto_lista(request):
    productos = Producto.objects.all()
    return render(request, 'turismo/producto_lista.html', {'productos': productos})

def producto_detalle(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'turismo/producto_detalle.html', {'producto': producto})

def producto_crear(request):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('producto_lista')
        else:
            return render(request, 'turismo/producto_form.html', {'form': form})
    else:
        form = ProductoForm()
    return render(request, 'turismo/producto_form.html', {'form': form})

def producto_editar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('producto_lista')
        else:
            return render(request, 'turismo/producto_form.html', {'form': form})
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'turismo/producto_form.html', {'form': form})

def producto_eliminar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        producto.delete()
        return redirect('producto_lista')
    return render(request, 'turismo/producto_eliminar.html', {'producto': producto})

@login_required
def carrito_agregar(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    carrito_item, created = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto)
    carrito_item.cantidad += 1
    carrito_item.save()
    return redirect('carrito_lista')

@login_required
def carrito_lista(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    carrito_items = carrito.carritoitem_set.all()
    return render(request, 'turismo/carrito_lista.html', {'carrito_items': carrito_items})

@login_required
def carrito_editar(request, pk):
    carrito_item = get_object_or_404(CarritoItem, pk=pk)
    if request.method == "POST":
        form = CarritoItemForm(request.POST, instance=carrito_item)
        if form.is_valid():
            form.save()
            return redirect('carrito_lista')
        else:
            return render(request, 'turismo/carrito_form.html', {'form': form})
    else:
        form = CarritoItemForm(instance=carrito_item)
    return render(request, 'turismo/carrito_form.html', {'form': form})

@login_required
def carrito_eliminar(request, pk):
    carrito_item = get_object_or_404(CarritoItem, pk=pk)
    if request.method == "POST":
        carrito_item.delete()
        return redirect('carrito_lista')
    return render(request, 'turismo/carrito_eliminar.html', {'carrito_item': carrito_item})

@login_required
def checkout(request):
    return render(request, 'turismo/checkout.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
