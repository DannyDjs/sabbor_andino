from django import forms
from .models import Restaurante,Turista,Reseña,EventoGastronomico

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
        
    widgets = {
        'foto': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
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
    widgets = {
            'Tnombre': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'Tapellido': forms.TextInput(attrs={'class': 'form-control'}),
            'Tcorreo': forms.EmailInput(attrs={'class': 'form-control', 'required': True}),
            'Tcelular': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'Tfoto': forms.FileInput(attrs={'class': 'form-control'}),
        }
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Reseña
        fields = ['comentario', 'calificacion']
        
class EventoGastronomicoForm(forms.ModelForm):
    class Meta:
        model = EventoGastronomico
        fields = ['nombre', 'fecha_inicio', 'fecha_fin', 'ubicacion', 'descripcion','foto']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }
        