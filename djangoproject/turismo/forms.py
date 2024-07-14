from django import forms
from .models import Producto, CarritoItem

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'descripcion', 'imagen']

class CarritoItemForm(forms.ModelForm):
    class Meta:
        model = CarritoItem
        fields = ['producto', 'cantidad']
