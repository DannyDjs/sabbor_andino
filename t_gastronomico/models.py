import os
from django.utils.text import slugify
from queue import Full
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser



# Create your models here
class Restaurante(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    direccion = models.CharField(max_length=100)
    celular = models.CharField(max_length=20)
    correo = models.EmailField()
    ubicacion = models.CharField(max_length=255, blank=True, null=True)
    foto = models.ImageField(upload_to='restaurante/', default='default/default_restaurante.png')
    horario = models.CharField(max_length=100, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Obtener el nombre de la imagen con el formato deseado
        if self.pk:  # Si el restaurante ya existe
            old_restaurante = Restaurante.objects.get(pk=self.pk)
            old_foto = old_restaurante.foto
        else:
            old_foto = None  # Inicializar old_foto en caso de que sea una nueva instancia

        # Guardar la imagen con el nombre del restaurante
        if self.foto:
            # Renombrar la imagen al guardar
            file_extension = os.path.splitext(self.foto.name)[1]  # Obtener la extensión del archivo
            self.foto.name = f"{self.nombre.replace(' ', '')}{file_extension}"

        super().save(*args, **kwargs)

        if self.pk and old_foto and old_foto != self.foto:
            # Eliminar la imagen antigua si ha cambiado
            try:
                if old_foto and os.path.isfile(old_foto.path):
                    os.remove(old_foto.path)
            except Exception as e:
                print(f"Error al eliminar la imagen antigua: {e}")

     
class Turista(models.Model):
     Tnombre = models.CharField(max_length=100)
     Tapellido = models.CharField(max_length=100)
     Tcorreo = models.EmailField()
     Tcelular = models.CharField(max_length=10)
     Tfoto = models.ImageField(upload_to='turista/',default='default/default_turista.png')
     user = models.OneToOneField(User, on_delete=models.CASCADE)
     
            
class Plato(models.Model):
     nombre = models.CharField(max_length=100)
     descripcion = models.TextField()
     foto = models.ImageField(upload_to='platos/',default='default/default_plato.png')
     video = models.FileField(upload_to='videos/platos/', null=True, blank=True)
     precio = models.DecimalField(max_digits=8, decimal_places=2)
     ingrediente = models.TextField(null=True, blank=True)  
     instruccion = models.TextField(null=True, blank=True)
     restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)

     def save(self, *args, **kwargs):
        old_foto = None
        old_video = None

        if self.pk:  # Si el plato ya existe
            old_plato = Plato.objects.get(pk=self.pk)
            old_foto = old_plato.foto
            old_video = old_plato.video

        # Obtener el nombre del restaurante
        restaurante_nombre = self.restaurante.nombre.replace(' ', '_')

        # Renombrar la imagen al guardar
        if self.foto:
            file_extension = os.path.splitext(self.foto.name)[1]  # Obtener la extensión del archivo
            self.foto.name = f"{restaurante_nombre}_{self.nombre.replace(' ', '_')}{file_extension}"

        # Renombrar el video al guardar
        if self.video:
            file_extension = os.path.splitext(self.video.name)[1]  # Obtener la extensión del archivo
            self.video.name = f"{restaurante_nombre}_{self.nombre.replace(' ', '_')}{file_extension}"

        super().save(*args, **kwargs)

        if old_foto and old_foto != self.foto and old_foto.name != 'default/default_plato.png':
            # Eliminar la imagen antigua si ha cambiado y no es la imagen por defecto
            if os.path.isfile(old_foto.path):
                os.remove(old_foto.path)

        if old_video and old_video != self.video:
            # Eliminar el video antiguo si ha cambiado
            if os.path.isfile(old_video.path):
                os.remove(old_video.path)

class Reseña(models.Model):
     calificacion = models.IntegerField(null=True)
     comentario = models.TextField(null=True)
     fecha = models.DateTimeField(auto_now_add=True)
     restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
     turista = models.ForeignKey(Turista, on_delete=models.CASCADE)
     plato = models.ForeignKey(Plato, on_delete=models.CASCADE)

     def __str__(self):
          return self.comentario 
     
class EventoGastronomico(models.Model):
    
    nombre = models.CharField(max_length=255)
    fecha_inicio = models.DateTimeField(null=True)  # Usar DateTimeField para fechas
    fecha_fin = models.DateTimeField(null=True)  # Usar DateTimeField para fechas
    ubicacion = models.CharField(max_length=255)
    descripcion = models.TextField()
    foto = models.ImageField(upload_to='eventos/',default='default/default_evento.png')
    restaurante = models.ForeignKey('Restaurante', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.nombre} - {self.mes}"
     
     
