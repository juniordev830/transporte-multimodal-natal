"""Proteções da construção de links Google Maps para entradas não confiáveis."""
import unittest
from itertools import repeat
from app import rota


class WaypointSafetyTests(unittest.TestCase):
    def test_rejeita_paradas_com_tipo_incorreto(self):
        for value in ("Natal", b"Natal", None, 42):
            with self.subTest(value=value), self.assertRaises(ValueError):
                rota("Natal", "Recife", paradas=value)

    def test_iterador_sem_fim_e_interrompido_no_limite(self):
        with self.assertRaisesRegex(ValueError, "até 3 paradas"):
            rota("Natal", "Recife", paradas=repeat("Parada"))

    def test_mantem_tres_paradas_validas(self):
        link = rota("Natal", "Recife", paradas=("A", "B", "C"))
        self.assertIn("waypoints=A%7CB%7CC", link)


if __name__ == "__main__":
    unittest.main()
