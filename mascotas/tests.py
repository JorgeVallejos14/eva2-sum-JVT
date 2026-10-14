from django.test import TestCase

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
