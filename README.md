# Comparador multimodal de Natal

Compare custo e tempo de carro, ônibus, bicicleta e caminhada usando suas estimativas.

## Rodar

Python 3.10 ou mais recente. Cada execução lê um JSON local e imprime outro JSON no terminal.

```bash
python app.py exemplo.json
python -m unittest -v
```

## Uso

Passe custo em reais e duração em minutos para cada opção. O programa destaca as alternativas em que nenhuma outra é pelo menos tão boa nos dois critérios e melhor em um deles. O relatório também indica `mais_rapida` (desempate pelo menor custo) e `mais_barata` (desempate pelo menor tempo). É necessário informar ao menos um modo. Os valores são estimativas fornecidas por você, não preços ou tempos consultados em tempo real.

## Google Maps

Os links seguem a documentação de [Maps URLs](https://developers.google.com/maps/documentation/urls/get-started) e abrem o app ou site sem chave. Confira no Maps a rota oferecida, a cobertura de transporte e as condições do momento. Os valores numéricos no arquivo de exemplo são demonstrações.

## Estado do projeto

Versão inicial funcional por linha de comando, sem interface web. Usa apenas a biblioteca padrão do Python. Os testes executam os exemplos e verificam as regras do projeto.

## Exportação para planilha

Use `python app.py exemplo.json --csv > relatorio.csv` para exportar o tempo e o custo de cada modo de transporte. O CSV usa ponto e vírgula, conserva a ordem do relatório e inclui o cabeçalho mesmo quando a seleção está vazia. O JSON continua sendo a saída padrão.

Também é possível encadear a ferramenta com outro comando usando `-` como entrada. Exemplo em um terminal Bash:

```bash
cat exemplo.json | python app.py -
```
