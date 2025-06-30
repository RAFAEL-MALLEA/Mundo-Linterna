from django.contrib import admin
from .models import Venta, Administrador, Usuario, Producto, DetalleVenta, Factura, Pago, Cliente, Compra, MedioPago, TipoProducto
# Register your models here.

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('Nombre_cli', 'Apellido_cli', 'Email')

admin.site.register(Venta)
admin.site.register(Administrador)
admin.site.register(Usuario)
admin.site.register(Producto)
admin.site.register(DetalleVenta)
admin.site.register(Factura)
admin.site.register(Pago)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Compra)
admin.site.register(MedioPago)
admin.site.register(TipoProducto)