'Compare custo e tempo de carro, ônibus, bicicleta e caminhada usando suas estimativas.'


from math import isfinite
from unicodedata import combining, normalize


def texto(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Use texto não vazio.")
    return value.strip()


def numero(value, minimo=0):
    if type(value) not in (int, float) or not isfinite(value) or value < minimo:
        raise ValueError(f"Use um número finito a partir de {minimo}.")
    return value


from urllib.parse import urlencode


MODOS = {"carro": "driving", "a-pe": "walking", "bicicleta": "bicycling", "onibus": "transit"}


def modo_chave(modo):
    texto_normalizado = normalize("NFD", texto(modo).casefold())
    sem_acentos = "".join(letra for letra in texto_normalizado if not combining(letra))
    return "-".join(sem_acentos.split())


def _url(acao, parametros):
    url = "https://www.google.com/maps/" + acao + "?" + urlencode({"api": 1, **parametros})
    if len(url) > 2048:
        raise ValueError("O endereço gerado ultrapassa o limite do Google Maps.")
    return url


def rota(origem, destino, modo="carro", paradas=(), evitar_pedagios=False):
    pontos = [texto(parada) for parada in paradas]
    if len(pontos) > 3 or any("|" in parada for parada in pontos):
        raise ValueError("Use até 3 paradas por link e evite o caractere |.")
    chave = modo_chave(modo)
    if chave not in MODOS:
        raise ValueError(f"Modo desconhecido: {modo}")
    params = {"origin": texto(origem), "destination": texto(destino), "travelmode": MODOS[chave]}
    if pontos:
        params["waypoints"] = "|".join(pontos)
    if evitar_pedagios:
        params["avoid"] = "tolls"
    return _url("dir/", params)


def run(data):
    origem, destino = texto(data["origem"]), texto(data["destino"])
    opcoes = []
    vistos = set()
    for item in data["modos"]:
        modo = modo_chave(item["modo"])
        if modo in vistos:
            raise ValueError("Cada modo deve aparecer uma vez.")
        vistos.add(modo)
        opcoes.append({"modo": modo, "minutos": numero(item["minutos"], 0.01),
                       "custo": numero(item["custo"]), "google_maps": rota(origem, destino, modo)})
    if not opcoes:
        raise ValueError("Informe ao menos um modo de transporte.")
    opcoes.sort(key=lambda item: (item["minutos"], item["custo"], item["modo"]))
    melhores = []
    for item in opcoes:
        tempo, custo = item["minutos"], item["custo"]
        dominada = any(x["minutos"] <= tempo and x["custo"] <= custo
                       and (x["minutos"], x["custo"]) != (tempo, custo) for x in opcoes)
        if not dominada:
            melhores.append(item["modo"])
    mais_barata = min(opcoes, key=lambda item: (item["custo"], item["minutos"], item["modo"]))
    return {"opcoes": opcoes, "alternativas_equilibradas": melhores,
            "mais_rapida": opcoes[0]["modo"], "mais_barata": mais_barata["modo"]}


import argparse
from contextlib import nullcontext
import sys
from relatorio_csv import escrever_csv
import json
from pathlib import Path


def objeto_sem_campos_repetidos(pares):
    objeto = {}
    for chave, valor in pares:
        if chave in objeto:
            raise ValueError(f"Campo JSON repetido: {chave!r}.")
        objeto[chave] = valor
    return objeto


def rejeitar_constante_json(constante):
    raise ValueError(f"Constante numérica inválida em JSON: {constante}.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entrada", help="Arquivo JSON com os dados ou - para a entrada padrão")
    parser.add_argument("--csv", action="store_true", help="Exportar o tempo e o custo de cada modo de transporte em CSV")
    args = parser.parse_args()

    try:
        entrada = nullcontext(sys.stdin.buffer) if args.entrada == "-" else Path(args.entrada).open(encoding="utf-8-sig")
        with entrada as source:
            data = json.load(
                source,
                object_pairs_hook=objeto_sem_campos_repetidos,
                parse_constant=rejeitar_constante_json,
            )
        if not isinstance(data, dict):
            raise ValueError("A entrada deve ser um objeto JSON.")
        result = run(data)
    except RecursionError:
        parser.exit(2, "O JSON tem níveis de aninhamento demais.\n")
    except (KeyError, TypeError, ValueError, OSError) as exc:
        parser.exit(2, f"Erro nos dados ou na execução: {exc}\n")

    sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    if args.csv:
        escrever_csv(result, sys.stdout)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
