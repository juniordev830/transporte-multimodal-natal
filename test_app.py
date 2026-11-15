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

    def test_aceita_modos_como_escritos_em_portugues(self):
        result = run({
            "origem": "Natal", "destino": "Parnamirim",
            "modos": [
                {"modo": " Ônibus ", "minutos": 20, "custo": 5},
                {"modo": "A pé", "minutos": 40, "custo": 0},
            ],
        })
        self.assertEqual([item["modo"] for item in result["opcoes"]], ["onibus", "a-pe"])
        self.assertIn("travelmode=transit", result["opcoes"][0]["google_maps"])
        self.assertIn("travelmode=walking", result["opcoes"][1]["google_maps"])

    def test_aliases_do_mesmo_modo_nao_duplicam_opcoes(self):
        item = {"modo": "onibus", "minutos": 20, "custo": 5}
        with self.assertRaisesRegex(ValueError, "uma vez"):
            run({"origem": "A", "destino": "B", "modos": [item, dict(item, modo="Ônibus")]})

    def test_rejeita_modo_repetido(self):
        item = dict(modo="carro", minutos=10, custo=5)
        with self.assertRaises(ValueError):
            run(dict(origem="A", destino="B", modos=[item, item]))

    def test_resumo_distingue_menor_tempo_e_menor_custo(self):
        data = json.loads((ROOT / "exemplo.json").read_text(encoding="utf-8"))
        result = run(data)
        self.assertEqual(result["mais_rapida"], "carro")
        self.assertEqual(result["mais_barata"], "bicicleta")
        self.assertEqual(result["alternativas_equilibradas"], ["carro", "bicicleta"])

    def test_desempate_por_custo_ou_tempo(self):
        result = run(dict(origem="A", destino="B", modos=[
            dict(modo="carro", minutos=20, custo=8),
            dict(modo="onibus", minutos=20, custo=5),
            dict(modo="bicicleta", minutos=30, custo=5),
        ]))
        self.assertEqual(result["mais_rapida"], "onibus")
        self.assertEqual(result["mais_barata"], "onibus")

    def test_rejeita_lista_sem_opcoes(self):
        with self.assertRaisesRegex(ValueError, "ao menos um modo"):
            run(dict(origem="A", destino="B", modos=[]))
