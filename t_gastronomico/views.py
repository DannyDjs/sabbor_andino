import json
from PIL import Image
from io import BytesIO
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.core.files.base import ContentFile
from django.core.files import File
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.urls import reverse
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import UserSerializer,PlatoSerializer,RestauranteSerializer,EventoGastronomicoSerializer,TuristaSerializer,ReseñaSerializer
from .models import Plato,Restaurante,Turista,Reseña,EventoGastronomico,User,Turista
from .forms import RestauranteForm, TuristaForm,EventoGastronomicoForm
from rest_framework.parsers import MultiPartParser, FormParser

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        # Validamos los datos de inicio de sesión usando el serializador
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # Obtenemos el nombre de usuario y la contraseña validados
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        # Autenticamos al usuario
        user = authenticate(username=username, password=password)
        
        if user is None:
            # Si las credenciales son inválidas
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        # Verificamos si el usuario tiene un perfil de turista
        try:
            turista = Turista.objects.get(user=user)
        except Turista.DoesNotExist:
            # Si el usuario no es un turista, devolver un error
            return Response({'error': 'Access denied: Only tourists can log in.'}, status=status.HTTP_403_FORBIDDEN)

        # Si es un turista, obtenemos o creamos el token
        token, created = Token.objects.get_or_create(user=user)

        # Devolvemos la respuesta con el token y los detalles del usuario
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
        })

class PlatoViewSet(viewsets.ModelViewSet):
    queryset = Plato.objects.all()  # Asegúrate de que el queryset esté definido
    serializer_class = PlatoSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['restaurante']
    
    def get_queryset(self):
        queryset = Plato.objects.all()
        restaurante_id = self.request.query_params.get('restaurante_id', None)
        if restaurante_id is not None:
            queryset = queryset.filter(restaurante_id=restaurante_id)
        return queryset
    
class  RestauranteViewSet(viewsets.ModelViewSet):
    queryset=Restaurante.objects.all()
    serializer_class = RestauranteSerializer
    
class  EventoGastronomicoViewSet(viewsets.ModelViewSet):
    queryset = EventoGastronomico.objects.all()
    serializer_class = EventoGastronomicoSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['restaurante']
    
    def get_queryset(self):
        queryset = EventoGastronomico.objects.all()
        restaurante_id = self.request.query_params.get('restaurante_id', None)
        if restaurante_id is not None:
            queryset = queryset.filter(restaurante_id=restaurante_id)
        return queryset

class TuristaViewSet(viewsets.ModelViewSet):
    queryset = Turista.objects.all()
    serializer_class = TuristaSerializer
    filter_backends = (DjangoFilterBackend,)
    parser_classes = (MultiPartParser, FormParser)
    filterset_fields = ['user']

    def get_queryset(self):
        # Obtener el queryset de todos los turistas
        queryset = Turista.objects.all()

        # Obtener el user_id desde los parámetros de la solicitud
        user_id = self.request.query_params.get('user_id', None)

        # Filtrar el queryset si el user_id es proporcionado
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)

        # Retornar el queryset filtrado
        return queryset
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
class ReseñaViewSet(viewsets.ModelViewSet):
    queryset = Reseña.objects.all()
    serializer_class = ReseñaSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering = ['-fecha']  # Ordenar por fecha de creación, ajusta según tu modelo

    def get_queryset(self):
        queryset = Reseña.objects.all()
        plato_id = self.request.query_params.get('plato_id', None)
        
        # Filtrar comentarios que no son nulos o vacíos
        queryset = queryset.exclude(comentario__isnull=True).exclude(comentario__exact='')
        
        if plato_id is not None:
            queryset = queryset.filter(plato_id=plato_id)
        return queryset
    
#autenticacion

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                auth_login(request, user)
                
                # Verificar si el usuario es turista o restaurante
                if hasattr(user, 'turista'):
                    # Usuario vinculado a un turista
                    request.session['user_type'] = 'turista'  # Agregar variable de sesión
                    return redirect("index")  # Redirigir a la página 'home' para turistas
                
                elif hasattr(user, 'restaurante'):
                    restaurante =user.restaurante
                    # Usuario vinculado a un restaurante
                    request.session['user_type'] = 'restaurante'  # Agregar variable de sesión
                    request.session['restaurante_nombre'] = restaurante.nombre
                    request.session['restaurante_foto_url'] = restaurante.foto.url
                    return redirect("index_dashboard")  # Redirigir a la página 'dashboard' para restaurantes

    else:
        form = AuthenticationForm()
    
    return render(request, "registration/login.html", {"form": form})

def logout(request):
    # Eliminar la variable de sesión 'user_type'
    if 'user_type' in request.session:
        del request.session['user_type']
        
    auth_logout(request)
    # Redirige al usuario a la página de inicio o login tras cerrar sesión
    return redirect("login")

def signup(request):
    if request.method == 'POST':
        print(request.POST)
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            # Guardar el usuario
            user = user_form.save()
            # Obtener el tipo de usuario seleccionado
            user_type = request.POST.get('user_type')
            print(f"Tipo de usuario seleccionado: {user_type}")
            if user_type == 'turista':
                turista_form = TuristaForm(request.POST, request.FILES)
                if turista_form.is_valid():
                    # Guardar el perfil de turista y asociarlo con el usuario
                    turista = turista_form.save(commit=False)
                    turista.user = user  # Asociar con el usuario creado
                    turista.save()
                    print("Turista registrado correctamente")
                else:
                    print(turista_form.errors)
            elif user_type == 'restaurante':
                restaurante_form = RestauranteForm(request.POST, request.FILES)
                if restaurante_form.is_valid():
                    # Guardar el perfil de restaurante y asociarlo con el usuario
                    restaurante = restaurante_form.save(commit=False)
                    restaurante.user = user  # Asociar con el usuario creado

                    # Procesar el campo de ubicación
                    ubicacion = request.POST.get('ubicacion')
                    print(f"Ubicación recibida: {ubicacion}")  # Verifica que se recibe la ubicación
                    if ubicacion:
                        try:
                            ubicacion_data = json.loads(ubicacion)
                            restaurante.ubicacion = ubicacion_data
                        except json.JSONDecodeError:
                            print("Error al decodificar el campo de ubicación")
                    
                    # Obtener la imagen del formulario
                    imagen = restaurante_form.cleaned_data.get('foto')
                    print(f"Imagen: {imagen}")
                    if imagen is not None:  # Verifica si se seleccionó un archivo
                        # Abre la imagen y la redimensiona
                        img = Image.open(imagen)
                        img = img.resize((300, 300), Image.LANCZOS)
                        if img.mode in ('RGBA', 'P'):  # Añade 'RGBA' a la lista
                            img = img.convert('RGB')
                        # Guarda la imagen redimensionada en un objeto BytesIO
                        thumb_io = BytesIO()
                        img.save(thumb_io, format='JPEG')
                        # Crea un nuevo Django File con la imagen redimensionada
                        imagen.file = File(thumb_io, name=imagen.name)
                    
                    restaurante.save()
                    print("Restaurante registrado correctamente")
                else:
                    print(restaurante_form.errors)

            return redirect('login')  # Redirigir a la vista de login después del registro

    else:
        user_form = UserCreationForm()
        turista_form = TuristaForm()
        restaurante_form = RestauranteForm()

    return render(request, 'registration/signup.html', {
        'user_form': user_form,
        'turista_form': turista_form,
        'restaurante_form': restaurante_form
    })


def base(request):
    # Lógica para la vista base
    return render(request, "base.html")
# inicio de pagina general

def index(request):
    return render(request, "index.html")
@login_required
def error(request):
    # Lógica para la vista error
    return render(request, "error.html")

def acerca_de(request):
    # Lógica para la vista acerca_de
    return render(request, "t_gastronomico/acerca_de.html")

def contacto(request):
    # Lógica para la vista contacto
    return render(request, "t_gastronomico/contacto.html")


#inicio de sesion Turista
@login_required
def buscar(request):
    query = request.GET.get('q', '')
    if query:
        restaurantes = Restaurante.objects.filter(nombre__icontains=query)
        platos = Plato.objects.filter(nombre__icontains=query)
        resultados = list(restaurantes) + list(platos)
    else:
        resultados = []

    resultados_dict = [{'nombre': obj.nombre, 'tipo': 'Restaurante' if isinstance(obj, Restaurante) else 'Plato'} for obj in resultados]

    return JsonResponse(resultados_dict, safe=False)

@login_required
def index_turista(request):
    # Lógica para la vista index turista
    return render(request, "index_turista.html")

@login_required
def restaurantes(request):
    restaurantes = Restaurante.objects.all()  # Obtén todos los platos  
    return render(request, "t_gastronomico/restaurantes.html", {'restaurantes': restaurantes})

@login_required
def restaurante_detalle(request, restaurante_id):
    restaurante = get_object_or_404(Restaurante, id=restaurante_id)
    
    plato = Plato.objects.filter(restaurante=restaurante)
    
    return render(request, "t_gastronomico/restaurante_detalle.html", {'restaurante': restaurante, 'plato': plato})

@login_required
def platos(request):
    platos = Plato.objects.all()  # Obtén todos los platos  
    return render(request, 't_gastronomico/platos.html', {'platos': platos})

@login_required
def plato_detalle(request, plato_id):
    plato = get_object_or_404(Plato, id=plato_id)
    resenas = plato.reseña_set.filter(calificacion__isnull=True).order_by('-fecha')
    return render(request, 't_gastronomico/plato_detalle.html', {'plato': plato, 'resena': resenas})

@login_required
@csrf_exempt
def calificacion(request):
    if request.method == 'POST':
        try:
            rating = request.POST.get('rating')
            turista_id = request.POST.get('turista_id')
            plato_id = request.POST.get('plato_id')
            restaurante_id = request.POST.get('restaurante_id')
            # Obtener instancias de Turista, Plato y Restaurante (manejo de errores con get_object_or_404)
            turista = get_object_or_404(Turista, id=turista_id)
            plato = get_object_or_404(Plato, id=plato_id)
            restaurante = get_object_or_404(Restaurante, id=restaurante_id)
        
            # Crear y guardar la reseña en la base de datos
            reseña = Reseña(calificacion=rating, turista=turista, plato=plato, restaurante=restaurante)
            reseña.save()
            
            return JsonResponse({'status': 'success'})
        
        except Turista.DoesNotExist:
            return JsonResponse({'error': 'Turista no encontrado'}, status=404)
        
        except Plato.DoesNotExist:
            return JsonResponse({'error': 'Plato no encontrado'}, status=404)
        
        except Restaurante.DoesNotExist:
            return JsonResponse({'error': 'Restaurante no encontrado'}, status=404)
        
        except Exception as e:
            # Manejar cualquier otra excepción inesperada
            return JsonResponse({'error': str(e)}, status=500)
    
    else:
        return JsonResponse({'error': 'Método no permitido.'}, status=405)
    
@login_required
def agregar_resena(request):
    if request.method == "POST":
        comentario = request.POST.get('comentario')
        restaurante_id = request.POST.get('restaurante')
        turista_id = request.POST.get('turista')
        plato_id = request.POST.get('plato')

        nueva_resena = Reseña(
            comentario=comentario,
            restaurante_id=restaurante_id,
            turista_id=turista_id,
            plato_id=plato_id
        )
        nueva_resena.save()

        # Devuelve los datos del nuevo comentario en formato JSON
        return JsonResponse({
            'comentario': nueva_resena.comentario,
            'turista': {
                'nombre': request.user.username,
                'Tfoto': request.user.turista.Tfoto.url,
            },
            'fecha': nueva_resena.fecha.strftime('%Y-%m-%d %H:%M:%S')
        })
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required  
def obtener_eventos(request):
    eventos = EventoGastronomico.objects.all()
    eventos_list = [{
        'title': evento.nombre,
        'description': evento.descripcion,
        'start': evento.fecha_inicio.isoformat(),
        'end': evento.fecha_fin.isoformat()
    } for evento in eventos]
    return JsonResponse(eventos_list, safe=False)

@login_required
def eventos (request):
    return render(request, "t_gastronomico/eventos.html")

#inicio de sesion Restaurante

@login_required
def dashboard(request):
    # Lógica para la vista dashboard
    return render(request, 'index_dashboard.html')

@login_required
def index_dashboard(request):
    # Lógica para la vista dashboard
    if request.user.is_authenticated:
        try:
            restaurante = Restaurante.objects.get(user=request.user)
            cantidad_platos = Plato.objects.filter(restaurante=restaurante).count()
            cantidad_eventos = EventoGastronomico.objects.filter(restaurante=restaurante).count()
            cantidad_calificaciones = Reseña.objects.filter(restaurante=restaurante, calificacion__isnull=False).count()
            cantidad_comentarios = Reseña.objects.filter(restaurante=restaurante, comentario__isnull=False).count()
            
            context = {
                'restaurante': restaurante,
                'cantidad_platos': cantidad_platos,
                'cantidad_eventos': cantidad_eventos,
                'cantidad_calificaciones': cantidad_calificaciones,
                'cantidad_comentarios': cantidad_comentarios,
            }
            
            return render(request, 'index_dashboard.html', context)
        except Restaurante.DoesNotExist:
            return redirect('login')
    else:
        return redirect('login')

@login_required
def editar_restaurante(request):
    try:
        restaurante = Restaurante.objects.get(user=request.user)
    except Restaurante.DoesNotExist:
        return redirect('error')

    if request.method == 'POST':
        print("Datos enviados:", request.POST)
        form = RestauranteForm(request.POST, request.FILES, instance=restaurante)
        if form.is_valid():
            print("Formulario válido")
            restaurante = form.save(commit=False)

            imagen = form.cleaned_data.get('foto')

            if imagen:
                # Redimensionar la imagen
                img = Image.open(imagen)
                img = img.resize((600, 600), Image.LANCZOS)
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')

                # Guardar la imagen redimensionada en un objeto BytesIO
                thumb_io = BytesIO()
                img.save(thumb_io, format='JPEG')
                thumb_io.seek(0)  # Asegúrate de estar en el inicio del archivo

                # Usar ContentFile para crear un nuevo archivo en memoria
                nueva_imagen = ContentFile(thumb_io.read(), imagen.name)
                restaurante.foto = nueva_imagen
            print("Ubicación capturada:", form.cleaned_data.get('ubicacion'))
            # Guardar la ubicación y otros datos
            restaurante.save()
            request.session['restaurante_foto_url'] = restaurante.foto.url
            request.session['restaurante_nombre'] = restaurante.nombre
            request.session['restaurante_ubicacion'] = restaurante.ubicacion
            return redirect('dashboard')
    else:
        
        form = RestauranteForm(instance=restaurante)
        print("Errores de formulario:", form.errors)

    return render(request, 'editar_restaurante.html', {'form': form})


@login_required
def agregar_plato(request):
    # Lógica para la vista agregar_plato
    if request.method == "POST":
        nombre = request.POST["txtNombre"]
        descripcion = request.POST["txtDescripcion"]
        foto = request.FILES.get("imgFoto")  # Utiliza .get en lugar de ['imgFoto']
        video = request.FILES.get("imgVideo")  # Utiliza .get en lugar de ['imgFoto']
        precio = request.POST["txtPrecio"]
        ingrediente = request.POST["txtIngrediente"]
        instruccion = request.POST["txtInstruccion"]

        # Asegúrate de que el usuario esté autenticado y sea un restaurante
        if request.user.is_authenticated:
            try:
                restaurante = request.user.restaurante
            except Restaurante.DoesNotExist:
                 return redirect('error')  # o donde quieras redirigir a los usuarios que no son restaurantes

            # Verifica si se seleccionó una imagen
            if foto is not None:  
                # Abre la imagen y la redimensiona
                img = Image.open(foto)
                img = img.resize((600, 600), Image.LANCZOS)
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')

                # Guarda la imagen redimensionada en un objeto BytesIO
                thumb_io = BytesIO()
                img.save(thumb_io, format='JPEG')

                # Crea un nuevo Django File con la imagen redimensionada
                foto = ContentFile(thumb_io.getvalue(), foto.name)
            else:
                # Si no se selecciona ninguna imagen, asigna una imagen por defecto
                with open('imagenes/platos/default.png','rb') as default_image:
                    foto = ContentFile(default_image.read(), 'imagen_por_defecto.jpg')

            # Crea y guarda el objeto Plato
            plato = Plato(
                nombre=nombre,
                descripcion=descripcion,
                foto=foto,
                video=video,
                precio=precio,
                restaurante=restaurante,
                ingrediente=ingrediente,
                instruccion=instruccion
            )
            plato.save()

            return redirect("listar_plato")

    return render(request, "platos/agregar_plato.html")

@login_required
def editar_plato(request, plato_id):
    plato = get_object_or_404(Plato, id=plato_id)

    # Asegúrate de que el usuario esté autenticado y sea el dueño del plato
    if request.user.is_authenticated and plato.restaurante == request.user.restaurante:
        if request.method == "POST":
            plato.nombre = request.POST["txtNombre"]
            plato.descripcion = request.POST["txtDescripcion"]
            foto = request.FILES.get("imgFoto")  # Utiliza .get en lugar de ['imgFoto']
            video = request.FILES.get("imgVideo")  # Obtiene el video subido
            precio = request.POST["txtPrecio"].replace(",", ".")
            plato.ingrediente = request.POST["txtIngrediente"]
            plato.instruccion = request.POST["txtInstruccion"]
            
            
            plato.precio = precio

            if foto is not None:  # Verifica si se seleccionó un archivo
                # Abre la imagen y la redimensiona
                
                img = Image.open(foto)
                img = img.resize((600, 600), Image.LANCZOS)
                if img.mode in ('RGBA', 'P'):  # Añade 'RGBA' a la lista
                    img = img.convert('RGB')

                # Guarda la imagen redimensionada en un objeto BytesIO
                thumb_io = BytesIO()
                img.save(thumb_io, format='JPEG')

                # Crea un nuevo Django File con la imagen redimensionada
                foto = ContentFile(thumb_io.getvalue(), foto.name)
                plato.foto = foto
        
            if video is not None:  # Verifica si se seleccionó un video
                plato.video = video  # Guarda el video en el plato
            

            plato.save()
            return redirect("listar_plato")

    else:
        return redirect('error')  # o donde quieras redirigir a los usuarios que no son dueños del plato

    return render(request, "platos/editar_plato.html", {"Plato": plato})

@login_required
def listar_plato(request):
    if request.user.is_authenticated:
        try:
            restaurante = request.user.restaurante
        except Restaurante.DoesNotExist:
            return redirect('error')  # o donde quieras redirigir a los usuarios que no son restaurantes

        platos = Plato.objects.filter(restaurante=restaurante)  # Filtrar los platos por el restaurante
        return render(request, "platos/listar_plato.html", {"platos": platos})

    return redirect('login')  # Redirige a los usuarios no autenticados a la página de inicio de sesión

def listar_plato_to_mobile(request):
    platos = Plato.objects.all()
    data = serializers.serialize("json", platos, fields=("nombre", "descripcion"))
    return HttpResponse(data)

@login_required
def eliminar_plato(request, plato_id):
    plato = get_object_or_404(Plato, id=plato_id)

    # Asegúrate de que el usuario esté autenticado y sea el dueño del plato
    if request.user.is_authenticated and plato.restaurante == request.user.restaurante:
        plato.delete()
        return redirect("listar_plato")

    else:
        return render(request,"error.html",{"mensaje": "No se encontró el plato con el id especificado o no tienes permiso para eliminarlo"},)
    
@login_required
def crear_evento(request):
    if request.method == 'POST':
        form = EventoGastronomicoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.restaurante = request.user.restaurante
            evento.save()
            return redirect('crear_evento')
    else:
        form = EventoGastronomicoForm()

    return render(request, 'crear_evento.html', {'form': form})

@login_required
def listar_evento(request):
    if request.user.is_authenticated:
        try:
            restaurante = request.user.restaurante
        except Restaurante.DoesNotExist:
            return redirect('error')  # o donde quieras redirigir a los usuarios que no son restaurantes

        evento = EventoGastronomico.objects.filter(restaurante=restaurante)  # Filtrar los platos por el restaurante
        return render(request, "listar_evento.html", {"evento": evento})

    return redirect('login') 

@login_required
def editar_evento(request, evento_id):
    evento = get_object_or_404(EventoGastronomico, id=evento_id)

    # Asegúrate de que el usuario esté autenticado y sea el dueño del evento
    if request.user.is_authenticated and evento.restaurante == request.user.restaurante:
        if request.method == "POST":
            form = EventoGastronomicoForm(request.POST, request.FILES, instance=evento)
            if form.is_valid():
                form.save()
                return redirect("listar_evento")
        else:
            form = EventoGastronomicoForm(instance=evento)
    else:
        return redirect('error')  # o donde quieras redirigir a los usuarios que no son dueños del evento

    return render(request, "editar_evento.html", {"form": form})  

@login_required
def eliminar_evento(request, evento_id):
    evento = get_object_or_404(EventoGastronomico, id=evento_id)

    # Asegúrate de que el usuario esté autenticado y sea el dueño del evento
    if request.user.is_authenticated and evento.restaurante == request.user.restaurante:
        if request.method == "POST":
            evento.delete()
            return redirect("listar_evento")

    else:
        return redirect('error')  # o donde quieras redirigir a los usuarios que no son dueños del evento

    return render(request, "eliminar_evento.html", {"evento": evento})
@login_required
def buscar_dashboard(request):
    query = request.GET.get('q')
    results = []

    if query:
        # Definir las posibles rutas y sus nombres amigables
        search_map = {
            'agregar plato': reverse('agregar_plato'),
            'listar plato': reverse('listar_platos'),
            'editar restaurante': reverse('editar_restaurante'),
            # Agregar más rutas según sea necesario
        }

        # Buscar coincidencias en las claves del mapa de búsqueda
        for key, url in search_map.items():
            if query.lower() in key:
                results.append((key, url))

    return render(request, 'buscar_dashboard.html', {'query': query, 'results': results})

def historia(request):
    # Lógica para la vista historia
    return render(request, "t_gastronomico/historia.html")

def cultura(request):
    # Lógica para la vista cultura
    return render(request, "t_gastronomico/cultura.html")


@login_required
def obtener_calificaciones(request):
    if request.method == 'GET':
        turista_id = request.GET.get('turista_id')
        
        # Obtener todas las calificaciones del turista desde la base de datos
        calificaciones = Reseña.objects.filter(turista_id=turista_id).values('plato_id', 'calificacion')
        
        # Convertir las calificaciones en una lista de diccionarios
        calificaciones_list = list(calificaciones)

        return JsonResponse({'calificaciones': calificaciones_list})
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    

