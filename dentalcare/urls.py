from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from gestion import views as gestion_views
from django.contrib.auth import views as auth_views
from gestion import views
from gestion.views import home, agendar_cita, obtener_citas_json, ver_historia_paciente, registrar_tratamiento, lista_tratamientos, editar_tratamiento, eliminar_tratamiento, reservation_view

 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registro/', gestion_views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='gestion/login.html'), name='login'),
    path('login/', views.login_cliente, name='login'),
    path('cliente_dashboard/', views.cliente_dashboard, name='cliente_dashboard'),
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
    path('citas/<str:fecha>/', views.citas_del_dia, name='citas_del_dia'),
    path('reportes/exportar_csv/', views.exportar_csv, name='exportar_csv'),
    path('reportes/data/', views.panel_reportes_data, name='panel_reportes_data'),
    path('api/obtener-reservas/', views.obtener_reservas, name='obtener_reservas'),
    path('api/reservar/', views.reservar, name='reservar'),
    path('reservas/', views.reservas, name='reservas'),
    path('api/obtener-horas-disponibles/', views.obtener_horas_disponibles, name='obtener_horas_disponibles'),
    path('', views.home, name='home'),  # Definir la vista de inicio con el nombre 'home'
    path('reservas/', views.reservas, name='reservas'),  # Definir la vista de reservas
    path('blog/', views.blog, name='blog'),
    path('blog/', views.blog, name='blog'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('reserva/', reservation_view, name='reservation'),
    path('confirmar_cita/<int:cita_id>/<str:confirmacion>/', views.confirmar_cita, name='confirmar_cita'),
    path('cancelar_cita/<int:cita_id>/', views.cancelar_cita, name='cancelar_cita'),
    path('reprogramar_cita/<int:id>/', views.reprogramar_cita, name='reprogramar_cita'),
    path('actualizar_cita/<int:id>/', views.actualizar_cita, name='actualizar_cita'),
    path('generar_factura_pdf/<int:factura_id>/', views.generar_factura_pdf, name='generar_factura_pdf'),
    path('facturas/', views.lista_facturas, name='lista_facturas'),
    path('factura/crear/', views.crear_factura, name='crear_factura'),
    path('factura/editar/<int:factura_id>/', views.editar_factura, name='editar_factura'),
    path('factura/enviar/<int:factura_id>/', views.enviar_factura_correo, name='enviar_factura_correo'),
    path('factura/<int:factura_id>/', views.factura_detalle, name='factura_detalle'),
    path('factura/guardar/', views.guardar_factura, name='guardar_factura'),
    path('reportes/generar_pdf/', gestion_views.descargar_reporte_pdf, name='descargar_reporte_pdf'),
    path('inventario/', views.lista_inventario, name='lista_inventario'),
    path('inventario/agregar/', views.agregar_producto, name='agregar_producto'),
    path('inventario/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('inventario/eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    path('inventario/', views.inventario, name='inventario'),
    path('crear_cliente/', views.crear_cliente, name='crear_cliente'),
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('cliente_dashboard/', views.cliente_dashboard, name='cliente_dashboard'),
    path('clientes/', views.lista_pacientes, name='lista_clientes'),
    path('ver_cliente/<int:cliente_id>/', views.ver_cliente, name='ver_cliente'),
    path('editar_cliente/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('eliminar_cliente/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('pacientes/', views.lista_pacientes, name='lista_pacientes'),
    path('ver_paciente/<int:id>/', views.ver_paciente, name='ver_paciente'),
    path('editar_paciente/<int:id>/', views.editar_paciente, name='editar_paciente'),
    path('eliminar_paciente/<int:id>/', views.eliminar_paciente, name='eliminar_paciente'),
    path('crear_factura/', views.crear_factura, name='crear_factura'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),  # Página para solicitar el correo
    path('reset_password/', views.reset_password, name='reset_password'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)