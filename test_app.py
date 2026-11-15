import json
from pathlib import Path
import subprocess
import sys
import unittest

from app import run

ROOT = Path(__file__).resolve().parent


class ProjetoTest(unittest.TestCase):
    def test_exemplo_documentado(self):
        data = json.loads((ROOT / "exemplo.json").read_text(encoding="utf-8"))
        result = run(data)
        self.assertEqual(result['alternativas_equilibradas'], ['carro', 'bicicleta'])

    def test_cli_com_exemplo(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "app.py"), str(ROOT / "exemplo.json")],
            capture_output=True, text=True, encoding="utf-8", check=True,
        )
        self.assertEqual(json.loads(result.stdout)['alternativas_equilibradas'], ['carro', 'bicicleta'])

    def test_rejeita_dados_incompletos(self):
        with self.assertRaises((KeyError, ValueError, TypeError)):
            run({})

    def test_opcao_dominada_nao_equilibrada(self):
        result = run(dict(origem="A", destino="B", modos=[dict(modo="carro", minutos=10, custo=10), dict(modo="onibus", minutos=20, custo=10), dict(modo="bicicleta", minutos=30, custo=0)]))
        self.assertEqual(result["alternativas_equilibradas"], ["carro", "bicicleta"])

    def test_rejeita_modo_repetido(self):
        item = dict(modo="carro", minutos=10, custo=5)
        with self.assertRaises(ValueError):
            run(dict(origem="A", destino="B", modos=[item, item]))
