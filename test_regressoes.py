import unittest
from app import run

class MultimodalTests(unittest.TestCase):
    def test_pareto_frontier(self):
        data={"origem":"Natal","destino":"Parnamirim","modos":[{"modo":"carro","minutos":20,"custo":20},{"modo":"onibus","minutos":40,"custo":5},{"modo":"bicicleta","minutos":60,"custo":0},{"modo":"a-pe","minutos":90,"custo":0}]}
        result=run(data)
        self.assertEqual(result["alternativas_equilibradas"],["carro","onibus","bicicleta"])

    def test_duplicate_mode_rejected(self):
        with self.assertRaises(ValueError):
            run({"origem":"Natal","destino":"Parnamirim","modos":[{"modo":"carro","minutos":10,"custo":2},{"modo":"carro","minutos":20,"custo":3}]})

if __name__=="__main__": unittest.main()
