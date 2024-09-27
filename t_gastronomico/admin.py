from django.contrib import admin
from t_gastronomico.views import Plato
from t_gastronomico.views import Restaurante
from .models import Turista

# Register your models here.
admin.site.register(Plato)
admin.site.register(Restaurante)
admin.site.register(Turista)
