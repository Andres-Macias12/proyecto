from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from gestion import views as gestion_views
from django.contrib.auth import views as auth_views
from gestion import views
from gestion.views import home, agendar_cita, obtener_citas_json, ver_historia_paciente, registrar_tratamiento, lista_tratamientos, editar_tratamiento, eliminar_tratamiento

 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registro/', gestion_views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='gestion/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('pacientes/', views.lista_pacientes, name='lista_pacientes'),
    path('pacientes/registrar/', views.registrar_paciente, name='registrar_paciente'),
    path('citas/', views.lista_citas, name='lista_citas'),
    path('citas/registrar/', views.registrar_cita, name='registrar_cita'),
    path('reportes/', views.panel_reportes, name='panel_reportes'),
    path('reportes/exportar_csv/', views.exportar_citas_csv, name='exportar_citas_csv'),
    path('citas/json/', views.obtener_citas_json, name='obtener_citas_json'),
    path('citas/calendario/', views.calendario_citas, name='calendario_citas'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cambiar-logo/', views.cambiar_logo, name='cambiar_logo'),
    path('tratamientos/', gestion_views.lista_tratamientos, name='lista_tratamientos'),
    path('configuraciones/', views.configuraciones, name='configuraciones'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('facturacion/', views.facturacion, name='facturacion'),
    path('inventario/', views.inventario, name='inventario'),
    path('pacientes/historia/<int:id>/', views.ver_historia_paciente, name='ver_historia_paciente'),
    path('pacientes/editar/<int:id>/', views.editar_paciente, name='editar_paciente'),
    path('pacientes/eliminar/<int:id>/', views.eliminar_paciente, name='eliminar_paciente'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('api/get-citas/', views.get_citas, name='get_citas'),
    path('calendario-citas/', views.calendario_citas, name='calendario_citas'),
    path('citas/registrar/', views.registrar_cita, name='registrar_cita'), 
    path('', home, name='inicio'),
    path('api/get-citas/', obtener_citas_json, name='get_citas_json'), 
    path('agendar_cita/', views.agendar_cita, name='agendar_cita'),
    path('guardar_cita/', views.guardar_cita, name='guardar_cita'),
    path('buscar_pacientes/', views.buscar_pacientes, name='buscar_pacientes'),
    path('lista_citas/', views.lista_citas, name='lista_citas'),
    path('calendario/', views.calendario_citas, name='calendario_citas'),
    path('citas/<str:fecha>/', views.citas_del_dia, name='citas_del_dia'),
    path('paciente/<int:paciente_id>/historia/', views.ver_historia_paciente, name='ver_historia_paciente'),
    path('enviar_notificaciones/', views.enviar_notificaciones, name='enviar_notificaciones'),
    path('tratamientos/registrar/<int:paciente_id>/', gestion_views.registrar_tratamiento, name='registrar_tratamiento'),
    path('tratamientos/<int:paciente_id>/', gestion_views.lista_tratamientos, name='lista_tratamientos'),
    path('tratamientos/editar/<int:id>/', editar_tratamiento, name='editar_tratamiento'),
    path('tratamientos/eliminar/<int:id>/', eliminar_tratamiento, name='eliminar_tratamiento'),
    path('paciente/<int:paciente_id>/tratamientos/registrar/', registrar_tratamiento, name='registrar_tratamiento'),
    path('tratamientos/', views.lista_tratamientos, name='lista_tratamientos'),
    path('tratamientos/agregar/', views.agregar_tratamiento, name='agregar_tratamiento'),
    path('citas/confirmar/<int:cita_id>/<str:confirmacion>/', views.confirmar_cita, name='confirmar_cita'),
    path('reportes/exportar_csv/', views.exportar_csv, name='exportar_csv'),
    path('reportes/data/', views.panel_reportes_data, name='panel_reportes_data'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)