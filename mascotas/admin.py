from django.contrib import admin

from .models import Atencion, Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'email', 'saldo')
    search_fields = ('nombre', 'telefono', 'email')


@admin.register(Atencion)
class AtencionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'cliente', 'fecha', 'monto')
    list_filter = ('fecha',)
    search_fields = ('titulo', 'cliente__nombre')
