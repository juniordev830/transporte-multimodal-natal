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

    def test_reject_bad_input_shape(self):
        for value in (None, [], "not-json-object", 42):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "objeto JSON"):
                run(value)

    def test_reject_non_list_and_non_object_modes(self):
        base = {"origem": "Natal", "destino": "Parnamirim"}
        for items in (None, "carro", [], [None], ["carro"], [{}] * 5):
            with self.subTest(items=items), self.assertRaisesRegex(ValueError, "1 a 4 modos"):
                run({**base, "modos": items})

    def test_reject_unknown_mode_without_silent_substitution(self):
        data = {"origem": "Natal", "destino": "Parnamirim",
                "modos": [{"modo": "aviao", "minutos": 15, "custo": 20}]}
        with self.assertRaisesRegex(ValueError, "Modo desconhecido"):
            run(data)


if __name__=="__main__": unittest.main()
