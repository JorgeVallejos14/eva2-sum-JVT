from django.test import TestCase
from django.contrib.auth.models import Group, Permission, User

from datetime import date
from decimal import Decimal

from .models import Atencion, Cliente


class ClienteAtencionTests(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nombre='Ana Pérez',
            telefono='+56 9 1234 5678',
            email='ana@example.com',
            direccion='Av. Siempre Viva 123',
            saldo=Decimal('15000'),
        )

    def test_atencion_queda_asociada_al_cliente(self):
        atencion = Atencion.objects.create(
            cliente=self.cliente,
            titulo='Control general',
            fecha=date(2026, 10, 14),
            descripcion='Revisión de rutina',
            monto=Decimal('25000'),
        )

        self.assertEqual(atencion.cliente, self.cliente)
        self.assertEqual(str(self.cliente), 'Ana Pérez')
        self.assertEqual(str(atencion), 'Control general - Ana Pérez')

    def test_eliminar_cliente_elimina_sus_atenciones(self):
        Atencion.objects.create(
            cliente=self.cliente,
            titulo='Vacunación',
            fecha=date(2026, 10, 14),
            descripcion='Aplicación de vacuna',
            monto=Decimal('12000'),
        )

        self.cliente.delete()

        self.assertEqual(Atencion.objects.count(), 0)

    def test_montos_se_pueden_mostrar_como_pesos_chilenos(self):
        from .admin import formato_pesos

        self.assertEqual(formato_pesos(Decimal('12990')), '$12.990')


class PermisosTests(TestCase):
    def test_digitador_no_tiene_permiso_para_eliminar(self):
        grupo = Group.objects.create(name='Digitador')
        permisos = Permission.objects.filter(
            content_type__app_label='mascotas',
            content_type__model__in=('cliente', 'atencion'),
            codename__in=('view_cliente', 'add_cliente', 'change_cliente',
                          'view_atencion', 'add_atencion', 'change_atencion'),
        )
        grupo.permissions.set(permisos)
        usuario = User.objects.create_user('digitador')
        usuario.groups.add(grupo)

        self.assertTrue(usuario.has_perm('mascotas.add_cliente'))
        self.assertTrue(usuario.has_perm('mascotas.change_atencion'))
        self.assertFalse(usuario.has_perm('mascotas.delete_cliente'))

    def test_revisor_solo_tiene_permisos_de_lectura(self):
        grupo = Group.objects.create(name='Revisor')
        permisos = Permission.objects.filter(
            content_type__app_label='mascotas',
            content_type__model__in=('cliente', 'atencion'),
            codename__in=('view_cliente', 'view_atencion'),
        )
        grupo.permissions.set(permisos)
        usuario = User.objects.create_user('revisor')
        usuario.groups.add(grupo)

        self.assertTrue(usuario.has_perm('mascotas.view_cliente'))
        self.assertFalse(usuario.has_perm('mascotas.add_cliente'))
        self.assertFalse(usuario.has_perm('mascotas.delete_atencion'))
