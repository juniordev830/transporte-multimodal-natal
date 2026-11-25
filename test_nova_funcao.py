import unittest
from app import run
class Limites(unittest.TestCase):
    def test_orcamento_e_tempo(self):
        data={"origem":"Natal","destino":"Alecrim","teto_reais":5,"teto_minutos":30,"modos":[{"modo":"carro","minutos":10,"custo":20},{"modo":"onibus","minutos":25,"custo":5},{"modo":"a-pe","minutos":40,"custo":0}]}
        result=run(data)
        self.assertEqual(result["dentro_do_limite"],["onibus"])
        self.assertEqual(result["mais_rapida_dentro_do_limite"],"onibus")
        data["teto_minutos"]=15
        self.assertIsNone(run(data)["mais_rapida_dentro_do_limite"])
