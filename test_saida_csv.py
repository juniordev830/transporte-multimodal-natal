import csv
import io
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent


class ExportacaoCliTest(unittest.TestCase):
    def test_exemplo_completo(self):
        comando = [sys.executable, str(ROOT / "app.py"), str(ROOT / "exemplo.json")]
        dados = subprocess.check_output([*comando, '--csv']).decode("utf-8")
        linhas = list(csv.reader(io.StringIO(dados), delimiter=";"))
        self.assertEqual(linhas[0], ['modo', 'minutos', 'custo', 'google_maps'])
        self.assertTrue(all(len(linha) == len(linhas[0]) for linha in linhas))
        self.assertIn('bicicleta', [celula for linha in linhas[1:] for celula in linha])

    def test_celulas_com_formulas_e_numeros_negativos(self):
        from relatorio_csv import celula

        self.assertEqual(celula(" =A1"), "' =A1")
        self.assertEqual(celula(-2), -2)
        self.assertEqual(celula("João"), "João")
