import os
from django.utils.text import slugify
from queue import Full
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser



def generar_ruta_foto_restaurante(instance, filename):
    """Genera la ruta personalizada para la foto del restaurante."""
    nombre_restaurante = slugify(instance.nombre)  # Convierte el nombre del restaurante a formato slug
    extension = filename.split('.')[-1]  # Obtiene la extensión del archivo original
    nuevo_nombre_archivo = f'{nombre_restaurante}.{extension}'  # Nuevo nombre del archivo
    return os.path.join('restaurantes/', nuevo_nombre_archivo)  # Devuelve la nueva ruta

class Restaurante(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    direccion = models.CharField(max_length=100)
    celular = models.CharField(max_length=20)
    correo = models.EmailField()
    ubicacion = models.CharField(max_length=255, blank=True, null=True)
    foto = models.ImageField(upload_to=generar_ruta_foto_restaurante, default='default/default_restaurante.png')
    horario = models.CharField(max_length=100, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Comprobamos si ya existe una instancia en la base de datos
        try:
            this = Restaurante.objects.get(id=self.id)
            # Si se sube una nueva imagen y la imagen actual NO es la por defecto
            if self.foto and this.foto != self.foto:
                if this.foto.name != 'default/default_restaurante.png' and os.path.isfile(this.foto.path):
                    os.remove(this.foto.path)
        except Restaurante.DoesNotExist:
            # El restaurante no existe todavía en la base de datos (es nuevo)
            pass

        # Guardar la nueva instancia de Restaurante
        super().save(*args, **kwargs)

def generar_ruta_foto_turista(instance, filename):
    """Genera la ruta personalizada para la foto del turista."""
    nombre_turista = slugify(instance.Tnombre + '-' + instance.Tapellido)  # Combina el nombre y apellido
    extension = filename.split('.')[-1]  # Obtiene la extensión del archivo original
    nuevo_nombre_archivo = f'{nombre_turista}.{extension}'  # Nuevo nombre del archivo
    return os.path.join('turistas/', nuevo_nombre_archivo)  # Devuelve la nueva ruta

class Turista(models.Model):
    Tnombre = models.CharField(max_length=100)
    Tapellido = models.CharField(max_length=100)
    Tcorreo = models.EmailField()
    Tcelular = models.CharField(max_length=10)
    Tfoto = models.ImageField(upload_to=generar_ruta_foto_turista, default='default/default_turista.png')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.Tnombre} {self.Tapellido}'
    
    def save(self, *args, **kwargs):
        # Comprobamos si ya existe una instancia en la base de datos
        try:
            this = Turista.objects.get(id=self.id)
            # Si se sube una nueva imagen y la imagen actual NO es la por defecto
            if self.Tfoto and this.Tfoto != self.Tfoto:
                if this.Tfoto.name != 'default/default_turista.png' and os.path.isfile(this.Tfoto.path):
                    os.remove(this.Tfoto.path)
        except Turista.DoesNotExist:
            # El turista no existe todavía en la base de datos (es nuevo)
            pass
        # Guardar la nueva instancia de Turista
        super().save(*args, **kwargs)

def generar_ruta_foto(instance, filename):
    """Genera la ruta personalizada para la foto, usando el nombre del restaurante y del plato"""
    nombre_restaurante = slugify(instance.restaurante.nombre)  # Convierte el nombre del restaurante a formato slug
    nombre_plato = slugify(instance.nombre)  # Convierte el nombre del plato a formato slug
    extension = filename.split('.')[-1]  # Obtiene la extensión del archivo original
    nuevo_nombre_archivo = f'{nombre_restaurante}_{nombre_plato}.{extension}'  # Nuevo nombre del archivo
    return os.path.join('platos/', nuevo_nombre_archivo)  # Devuelve la nueva ruta

def generar_ruta_video(instance, filename):
    """Genera la ruta personalizada para el video, usando el nombre del restaurante y del plato"""
    nombre_restaurante = slugify(instance.restaurante.nombre)
    nombre_plato = slugify(instance.nombre)
    extension = filename.split('.')[-1]
    nuevo_nombre_archivo = f'{nombre_restaurante}_{nombre_plato}.{extension}'
    return os.path.join('videos/platos/', nuevo_nombre_archivo)
        
class Plato(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    foto = models.ImageField(upload_to=generar_ruta_foto, default='default/default_plato.png')
    video = models.FileField(upload_to=generar_ruta_video, null=True, blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    ingrediente = models.TextField(null=True, blank=True)  
    instruccion = models.TextField(null=True, blank=True)
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        # Comprobamos si ya existe una instancia en la base de datos
        try:
            this = Plato.objects.get(id=self.id)
            # Si se sube una nueva imagen y la imagen actual NO es la por defecto
            if self.foto and this.foto != self.foto:
                if this.foto.name != 'default/default_plato.png' and os.path.isfile(this.foto.path):
                    os.remove(this.foto.path)
        except Plato.DoesNotExist:
            # El plato no existe todavía en la base de datos (es nuevo)
            pass

        # Guardar la nueva instancia de Plato
        super().save(*args, **kwargs)

class Reseña(models.Model):
    
    calificacion = models.IntegerField(null=True)
    comentario = models.TextField(null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    turista = models.ForeignKey(Turista, on_delete=models.CASCADE)
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)

    def __str__(self):
        return self.comentario 
    
def generar_ruta_foto_evento(instance, filename):
    """Genera la ruta personalizada para la foto del evento, usando el nombre del restaurante y del evento."""
    nombre_restaurante = slugify(instance.restaurante.nombre)  # Convierte el nombre del restaurante a formato slug
    nombre_evento = slugify(instance.nombre)  # Convierte el nombre del evento a formato slug
    extension = filename.split('.')[-1]  # Obtiene la extensión del archivo original
    nuevo_nombre_archivo = f'{nombre_restaurante}_{nombre_evento}.{extension}'  # Nuevo nombre del archivo
    return os.path.join('eventos/', nuevo_nombre_archivo)  # Devuelve la nueva ruta
    
class EventoGastronomico(models.Model):
    
    nombre = models.CharField(max_length=255)
    fecha_inicio = models.DateTimeField(null=True)  # Usar DateTimeField para fechas
    fecha_fin = models.DateTimeField(null=True)  # Usar DateTimeField para fechas
    ubicacion = models.CharField(max_length=255)
    descripcion = models.TextField()
    foto = models.ImageField(upload_to=generar_ruta_foto_evento, default='default/default_evento.png')
    restaurante = models.ForeignKey('Restaurante', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        # Comprobamos si ya existe una instancia en la base de datos
        try:
            this = EventoGastronomico.objects.get(id=self.id)
            # Si se sube una nueva imagen y la imagen actual NO es la por defecto
            if self.foto and this.foto != self.foto:
                if this.foto.name != 'default/default_evento.png' and os.path.isfile(this.foto.path):
                    os.remove(this.foto.path)
        except EventoGastronomico.DoesNotExist:
            # El evento no existe todavía en la base de datos (es nuevo)
            pass

        # Guardar la nueva instancia de EventoGastronomico
        super().save(*args, **kwargs)
    
