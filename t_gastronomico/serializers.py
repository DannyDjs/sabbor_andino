# serializers.py
from django.contrib.auth.models import User
from .models import EventoGastronomico, Plato, Restaurante, Turista, Reseña
from rest_framework import serializers
from django.db.models import Avg


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password')


class PlatoSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Plato
        fields = ['id', 'nombre', 'foto', 'video', 'descripcion','precio', 'ingrediente', 'instruccion', 'average_rating','restaurante_id']

    def get_average_rating(self, obj):
        # Calcula la calificación promedio de las reseñas asociadas al plato
        return Reseña.objects.filter(plato=obj).aggregate(Avg('calificacion'))['calificacion__avg'] or 0


class RestauranteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurante
        fields = "__all__"
        
class EventoGastronomicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventoGastronomico
        fields = "__all__"

class TuristaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turista
        fields = "__all__"
        
class ReseñaSerializer(serializers.ModelSerializer):
    turista = TuristaSerializer(read_only=True)  # Leer detalles del turista
    turista_id = serializers.PrimaryKeyRelatedField(
        queryset=Turista.objects.all(), source='turista', write_only=True
    )  # Para escribir el ID del turista
    
    class Meta:
        model = Reseña
        fields = ['id', 'comentario','calificacion', 'fecha', 'plato', 'restaurante', 'turista', 'turista_id']
    
    
    