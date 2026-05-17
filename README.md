# Prontuario Strutturale

Applicazione Streamlit per il calcolo rapido di schemi statici ricorrenti.
Il prontuario permette di scegliere vincolo e azione, inserire i parametri
geometrici/meccanici e ottenere diagrammi, valori massimi e relazioni
scaricabili.

## Funzionalita

- Schemi di trave appoggiata, mensola, incastro-appoggio e incastro-incastro.
- Casi con carichi distribuiti, concentrati, triangolari, momenti imposti,
  cedimenti e gradienti termici.
- Schemi speciali: archi, cavi, trave continua, ponte sospeso, ponte Langer,
  trave Gerber e urto dinamico su mensola.
- Diagrammi di taglio, momento flettente, rotazione e deformata.
- Tabella di sintesi con `Vmax`, `Mmax`, `theta max`, `vmax`, ascissa e segno.
- Relazione PDF e scheda Word editabile per il caso selezionato.

## Struttura

```text
Prontuario/
|-- app.py                  # Interfaccia Streamlit
|-- prontuario_schemi.py    # Mappa completa vincolo/carico del menu
|-- prontuario_results.py   # Sintesi tabellare dei risultati
|-- src_code.py             # Calcoli, grafici e relazione PDF
|-- prontuario_word.py      # Generazione scheda Word
|-- test_prontuario.py      # Test parametrizzati sui casi JSON
|-- test/                   # Casi benchmark
|-- requirements.txt        # Dipendenze Python
```

## Installazione

```bash
pip install -r requirements.txt
```

## Avvio

```bash
streamlit run app.py
```

## Test

```bash
pytest -q
```

## Output tecnici

La scheda Word viene generata con `python-docx` e contiene:

- dati di input del caso corrente;
- sintesi dei massimi di taglio, momento, rotazione e deformata;
- risultati specifici per schemi con spinte, trazioni o urto dinamico;
- diagrammi allegati in formato immagine.

La relazione PDF esistente resta disponibile come esportazione rapida.

La mappa del menu e' coperta da test: ogni combinazione esposta deve avere un
blocco di calcolo in `app.py`, e i blocchi gia' implementati non devono restare
nascosti.
