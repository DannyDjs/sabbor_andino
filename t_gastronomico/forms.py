from django import forms
from .models import Restaurante,Turista,Reseña,EventoGastronomico,Plato
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RestauranteForm(forms.ModelForm):
    ubicacion = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Restaurante
        fields = ['nombre', 
                  'descripcion', 
                  'direccion', 
                  'celular', 
                  'correo', 
                  'ubicacion', 
                  'foto',
                  'horario'
                  ]
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripcion',
            'direccion': 'Direccion',
            'celular': 'Celular',
            'correo': 'Correo',
            'ubicacion': 'Ubicacion',
            'foto': 'Imagen',
            'horario': 'Horario',
        }
        
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Ingresa el nombre del restaurante','required': True}),
            'descripcion': forms.Textarea(attrs={ 'class': 'form-control', 'rows': 2, 'placeholder': 'Describe el restaurante'  }),
            'direccion': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Ingresa la dirección','required': True}),
            'celular': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Ingresa el número de celular','maxlength': 10 ,'required': True }),
            'correo': forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Ingresa el correo electrónico'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control-file' }),
            'horario': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Ingresa el horario de atención','required': True}),
            
        }
    
class TuristaForm(forms.ModelForm):
    class Meta:
        model = Turista
        fields = ['Tnombre', 
                  'Tapellido', 
                  'Tcorreo', 
                  'Tcelular', 
                  'Tfoto'
                  ]
        labels = {
            'Tnombre': 'Nombre',
            'Tapellido': 'Apellido',
            'Tcorreo': 'Correo electrónico',
            'Tcelular': 'Número de celular',
            'Tfoto': 'Foto de perfil',
        }
        widgets = {
            'Tnombre': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'Tapellido': forms.TextInput(attrs={'class': 'form-control','required': True}),
            'Tcorreo': forms.EmailInput(attrs={'class': 'form-control', }),
            'Tcelular': forms.TextInput(attrs={'class': 'form-control','required': True}),
            'Tfoto': forms.FileInput(attrs={'class': 'form-control'}),
        }
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Reseña
        fields = ['comentario', 'calificacion']
        
class EventoGastronomicoForm(forms.ModelForm):
    class Meta:
        model = EventoGastronomico
        fields = ['nombre', 'fecha_inicio', 'fecha_fin', 'ubicacion', 'descripcion', 'foto']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre del evento'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Seleccione la fecha de inicio'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Seleccione la fecha de fin'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la ubicación del evento'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describa el evento gastronómico'}),
        }

        
class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = ['nombre', 'descripcion','ingrediente','instruccion','foto','video','precio']
        labels = {
            'nombre': 'NOMBRE',
            'descripcion': 'DESCRIPCION',
            'ingrediente': 'INGREDIENTES',
            'instruccion': 'INSTRUCCION',
            'foto': 'IMAGEN DEL PLATO',
            'video': 'VIDEO ',
            'precio': 'PRECIO',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre del evento'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Describa el evento gastronómico'}),
            'ingrediente': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Describa el evento gastronómico'}),
            'instruccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Describa el evento gastronómico'}),
            
        }
        
class CustomUserCreationForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ('','Selecciona una opcion'),
        ('turista', 'Turista'),
        ('restaurante', 'Restaurante')
    ]

    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, label="Tipo de usuario")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'user_type']
        
