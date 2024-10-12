import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Plato,EventoGastronomico,Restaurante,Turista


@receiver(post_delete, sender=Plato)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """ Elimina archivos de imagen (foto) y video cuando el objeto Plato se elimina """
    
    # Eliminar la imagen (foto) si existe y no es la imagen por defecto
    if instance.foto and instance.foto.name != 'default/default_plato.png':  # No eliminar la imagen por defecto
        if os.path.isfile(instance.foto.path):
            os.remove(instance.foto.path)
    
    # Eliminar el video si existe
    if instance.video:
        if os.path.isfile(instance.video.path):
            os.remove(instance.video.path)

@receiver(post_delete, sender=EventoGastronomico)
def auto_delete_file_on_delete_evento(sender, instance, **kwargs):
    """ Elimina la imagen cuando el evento se elimina """
    
    # Eliminar la imagen (foto) si existe y no es la imagen por defecto
    if instance.foto and instance.foto.name != 'default/default_evento.png':  # No eliminar la imagen por defecto
        if os.path.isfile(instance.foto.path):
            os.remove(instance.foto.path)
            
@receiver(post_delete, sender=Restaurante)
def auto_delete_file_on_delete_restaurante(sender, instance, **kwargs):
    """ Elimina la imagen cuando el restaurante se elimina """
    
    # Eliminar la imagen (foto) si existe y no es la imagen por defecto
    if instance.foto and instance.foto.name != 'default/default_restaurante.png':  # No eliminar la imagen por defecto
        if os.path.isfile(instance.foto.path):
            os.remove(instance.foto.path)
            
@receiver(post_delete, sender=Turista)
def auto_delete_file_on_delete_turista(sender, instance, **kwargs):
    """ Elimina la imagen cuando el turista se elimina """
    
    # Eliminar la imagen (foto) si existe y no es la imagen por defecto
    if instance.foto and instance.foto.name != 'default/default_turista.png':  # No eliminar la imagen por defecto
        if os.path.isfile(instance.foto.path):
            os.remove(instance.foto.path)
