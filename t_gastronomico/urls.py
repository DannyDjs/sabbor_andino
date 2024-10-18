from . import views
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework  import routers
from rest_framework.authtoken.views import obtain_auth_token
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

#enrutador

router = routers.DefaultRouter()
#vistas correspondientes  a cada modelo

router.register(r'plato',views.PlatoViewSet)
router.register(r'restaurante',views.RestauranteViewSet)
router.register(r'evento',views.EventoGastronomicoViewSet)
router.register(r'User',views.UserViewSet)
router.register(r'turista',views.TuristaViewSet)
router.register(r'resena',views.ReseñaViewSet)


# urls.py
urlpatterns = [
    path ('api/',include(router.urls)),
    path('api-token-auth/', views.CustomAuthToken.as_view(), name='api_token_auth'),
    path('api/google-login/', views.google_login, name='google_login'),
    path('api/register_turista/', views.register_turista, name='register_turista'),
    path('api/version/', views.get_version, name='get_version'),

    # Ruta para la página de inicio
    path("", views.index, name="index"),
    path("acerca_de/", views.acerca_de, name="acerca_de"),
    path("app/", views.app, name="app"),
    path("error/", views.error, name="error"),
    
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    # Ruta para solicitar la recuperación de contraseña
     # URL para solicitar un restablecimiento de contraseña
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/contraseña/password_reset.html'), name='password_reset'),
    
    # URL que se muestra después de enviar el formulario de restablecimiento de contraseña
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/contraseña/password_reset_done.html'), name='password_reset_done'),
    
    # URL para confirmar el restablecimiento de la contraseña
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/contraseña/password_reset_confirm.html'), name='password_reset_confirm'),
    
    # URL que se muestra después de cambiar la contraseña
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/contraseña/password_reset_complete.html'), name='password_reset_complete'),
    
    path("index_turista", views.index_turista, name="index_turista"),
    path("calificacion/", views.calificacion, name="calificacion"),
    path('obtener_calificaciones/', views.obtener_calificaciones, name='obtener_calificaciones'),
    path('buscar/', views.buscar, name='buscar'),
    path("restaurantes/", views.restaurantes, name="restaurantes"),
    path("restaurante_detalle/<int:restaurante_id>/", views.restaurante_detalle, name="restaurante_detalle"),
    path("platos/", views.platos, name="platos"),
    path("plato_detalle/<int:plato_id>/", views.plato_detalle, name="plato_detalle"),
    path('agregar_resena/', views.agregar_resena, name='agregar_resena'),
    path('eventos/', views.eventos, name='eventos'),
    path('obtener_eventos/', views.obtener_eventos, name='obtener_eventos'),
    
    path("dashboard/", views.dashboard, name="dashboard"),
    path("editar_restaurante/", views.editar_restaurante, name="editar_restaurante"),
    path("agregar/", views.agregar_plato, name="agregar_plato"),
    path("editar/<int:plato_id>/", views.editar_plato, name="editar_plato"),
    path("listar/", views.listar_plato, name="listar_plato"),
    path("eliminar/<int:plato_id>/", views.eliminar_plato, name="eliminar_plato"),
    path("crear_evento/", views.crear_evento, name="crear_evento"),
    path("listar_evento/", views.listar_evento, name="listar_evento"),
    path("editar_evento/<int:evento_id>/", views.editar_evento, name="editar_evento"),
    path("eliminar_evento/<int:evento_id>/", views.eliminar_evento, name="eliminar_evento"),
    path("buscar_dashboard/", views.buscar_dashboard, name="buscar_dashboard"),
    
    
    path("signup/turista/<int:user_id>/", views.complete_turista, name="complete_turista"),
    path("signup/restaurante/<int:user_id>/", views.complete_restaurante, name="complete_restaurante"),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")), 
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
