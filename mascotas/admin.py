from django.contrib import admin

from .models import Atencion, Cliente


def formato_pesos(valor):
    return f'${valor:,.0f}'.replace(',', '.')


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'email', 'direccion', 'saldo_formateado')
    list_filter = ('saldo',)
    search_fields = ('nombre', 'telefono', 'email')

    @admin.display(description='Saldo')
    def saldo_formateado(self, obj):
        return formato_pesos(obj.saldo)


@admin.register(Atencion)
class AtencionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'cliente', 'fecha', 'monto_formateado')
    list_filter = ('fecha', 'cliente')
    search_fields = ('titulo', 'cliente__nombre')

    @admin.display(description='Monto')
    def monto_formateado(self, obj):
        return formato_pesos(obj.monto)
