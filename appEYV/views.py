from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import Producto 
from .forms import CustomUserCreationForm, ProductoForm, TipoProductoForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse


# Create your views here.
def home(request):
    return render(request, 'app/home.html')

def crearcuenta(request):
    return render(request, 'app/crearcuenta.html')

def pedido(request):
    return render(request, 'app/pedido.html')
def pago(request):
    total = request.session.get('cart_total', 0)  # Obtén el total desde la sesión
    context = {
        'total': total
    }
    return render(request, 'app/pago.html', context)

def modificar_producto (request, id):

    producto = get_object_or_404(Producto, id=id)

    data = {
        'form': ProductoForm(instance=producto)
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect("listar-productos")
        data ["form"] = formulario
    return render(request, 'app/producto/modificar.html', data)

def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    
    if request.method == 'POST':
        producto.delete()
        return HttpResponseRedirect(reverse('listar-productos')) 
    
    return render(request, 'app/producto/eliminar_confirmacion.html', {'producto': producto})

def agregar_producto(request):

    data = {
        'form': ProductoForm()
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            data ["mensaje"] = "Guardado correctamente"
        else:
            data ["form"] = formulario

    return render(request,'app/producto/agregar.html', data)

def listar_productos(request):
    productos = Producto.objects.all()
    data = {
        'productos': productos
    }
        
    
    return render (request, 'app/producto/listar.html', data)

def product_list(request):
    tipo = request.GET.get('tipo')  # Obtener el tipo de producto desde el parámetro de la URL
    id_constante = request.GET.get('id_constante')  # Obtener la ID constante si existe
    productos = Producto.objects.all()

    # Filtrar por tipo si se especifica
    if tipo:
        try:
            tipo = int(tipo)  # Convertir a entero
            productos = productos.filter(Tipo_prod=tipo)
        except ValueError:
            productos = Producto.objects.none()  # Si no es un entero válido, devuelve vacío

    # Filtrar adicionalmente por ID constante si se especifica
    if id_constante:
        productos = productos.filter(ID_prod=id_constante)

    paginator = Paginator(productos, 12)  # Mostrar 12 productos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'app/home.html', {
        'page_obj': page_obj,
        'tipo': tipo,
        'id_constante': id_constante,
    })



from django.contrib.auth.models import User
from .models import Cliente

def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            # Crear usuario
            user = formulario.save()
            Nombre_cli = formulario.cleaned_data['first_name']
            Apellido_cli = formulario.cleaned_data['last_name']
            Email = formulario.cleaned_data['email']
            username = Email.split("@")[0]
            # Crear cliente asociado
            Cliente.objects.create(
                usuario=user,
                Nombre_cli=Nombre_cli,
                Apellido_cli=Apellido_cli,
                Email=Email
                
            )


            login(request, user)
            messages.success(request, "Registro Correcto")
            return redirect(to="product_list")
        data["form"] = formulario
    return render(request, 'registration/registro.html', data)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def productos(request):
    productos = Producto.objects.all()  # Obtiene todos los productos
    return render(request, 'productos.html', {'products': productos})

@csrf_exempt
def carrito(request):
    if request.method == 'POST':
        cart = json.loads(request.body)  # Puede fallar si el JSON está malformado
        # Aquí puedes procesar los datos y luego redirigir o renderizar
        return JsonResponse({'success': True, 'message': 'Carrito procesado'})
    else:
        # Renderiza la página del carrito
        cart = request.session.get('cart', {})
        total = sum(item['Precio'] * item['cantidad'] for item in cart.values())
        return render(request, 'app/carrito.html', {'cart': cart, 'total': total})

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Pago

@csrf_exempt
def procesar_pago(request):
    if request.method == 'POST':
        try:
            datos = json.loads(request.body)
            Pago.objects.create(
                ID_pago=datos['id'],
                Tipo_pago="PayPal",
                estado=datos['status'],
                email_comprador=datos['payer']['email_address'],
                monto=datos['purchase_units'][0]['amount']['value'],
                moneda=datos['purchase_units'][0]['amount']['currency_code'],
                fecha=datos['create_time'],
                datos_raw=datos  # Guarda los datos completos para auditoría o análisis
            )
            return JsonResponse({'success': True})
        except Exception as e:
            print(f"Error al procesar el pago: {e}")
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Método no permitido'})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def productos(request):
    productos = Producto.objects.all()  # Obtiene todos los productos
    return render(request, 'productos.html', {'products': productos})

@csrf_exempt
def carrito(request):
    if request.method == 'POST':
        cart = json.loads(request.body)  # Puede fallar si el JSON está malformado
        # Aquí puedes procesar los datos y luego redirigir o renderizar
        return JsonResponse({'success': True, 'message': 'Carrito procesado'})
    else:
        # Renderiza la página del carrito
        cart = request.session.get('cart', {})
        total = sum(item['Precio'] * item['cantidad'] for item in cart.values())
        return render(request, 'app/carrito.html', {'cart': cart, 'total': total})

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Pago

@csrf_exempt
def procesar_pago(request):
    if request.method == 'POST':
        try:
            datos = json.loads(request.body)
            Pago.objects.create(
                ID_pago=datos['id'],
                Tipo_pago="PayPal",
                estado=datos['status'],
                email_comprador=datos['payer']['email_address'],
                monto=datos['purchase_units'][0]['amount']['value'],
                moneda=datos['purchase_units'][0]['amount']['currency_code'],
                fecha=datos['create_time'],
                datos_raw=datos  # Guarda los datos completos para auditoría o análisis
            )
            return JsonResponse({'success': True})
        except Exception as e:
            print(f"Error al procesar el pago: {e}")
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Método no permitido'})

@csrf_exempt
def guardar_carrito(request):
    if request.method == 'POST':
        try:
            datos = json.loads(request.body)
            request.session['cart_total'] = datos['total']  # Guarda el total en la sesión
            return JsonResponse({'success': True})
        except Exception as e:
            print(f"Error al guardar el carrito: {e}")
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Método no permitido'})
    
from transbank.webpay.webpay_plus.transaction import Transaction

# Vista para iniciar pago con Transbank
def iniciar_pago_transbank(request):
    total = request.session.get('cart_total', 0)
    transaction = Transaction()
    response = transaction.create(
        buy_order="orden1234",  # Genera un identificador único
        session_id="sesion1234",  # Genera una sesión única
        amount=total,
        return_url="http://127.0.0.1:8000/resultado-transbank/"
    )
    return redirect(response['url'] + '?token_ws=' + response['token'])
