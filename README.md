# 🏗️ Prontuario Web

<img width="1456" height="720" alt="logoProntuario" src="https://github.com/user-attachments/assets/cea9c3c0-01ff-4d53-b5b6-a4def7554fb0" />

Un'applicazione web open-source sviluppata in **Python** e **Streamlit** dedicata al calcolo strutturale rapido. 

Ispirata ai classici prontuari di ingegneria, questa app permette agli utenti di selezionare uno schema statico, inserire i propri parametri (geometria, carichi, materiale) e ottenere in tempo reale:
* Le **Reazioni Vincolari**.
* I valori massimi di **Momento Flettente**, **Taglio** e **Freccia**.
* I **Diagrammi delle Sollecitazioni** (V e M) tracciati in modo dinamico.

## 🚀 Funzionalità Attuali

Il prontuario attualmente supporta i seguenti schemi statici:
1. **Trave in semplice appoggio** con carico uniformemente distribuito.
2. **Mensola incastrata** con carico concentrato in punta.

*I grafici sono generati utilizzando Matplotlib e seguono la convenzione del disegno strutturale (es. momento positivo tracciato verso il basso).*

## 📁 Struttura del Progetto

Il codice è stato ingegnerizzato separando il *frontend* dal *backend* per garantire la massima modularità:

```text
prontuario-travi/
├── app.py              # Interfaccia utente in Streamlit (Frontend)
├── src_code.py         # Logica di calcolo, equazioni e grafici (Backend)
├── requirements.txt    # Lista delle dipendenze Python
└── README.md           # Documentazione del progetto

```

## 🛠️ Installazione

Per far girare questo progetto sul tuo computer locale, segui questi passaggi:

1. **Clona il repository:**
```bash
git clone [https://github.com/tuo-username/prontuario-travi.git](https://github.com/tuo-username/prontuario-travi.git)
cd prontuario-travi

```


2. **Crea un ambiente virtuale (Opzionale ma consigliato):**
```bash
python -m venv venv
source venv/bin/activate  # Su Windows usa: venv\Scripts\activate

```


3. **Installa le dipendenze:**
```bash
pip install -r requirements.txt

```



## 💻 Utilizzo

Una volta installate le librerie, puoi avviare l'applicazione Streamlit con un solo comando:

```bash
streamlit run app.py

```

Il tuo browser predefinito si aprirà automaticamente all'indirizzo `http://localhost:8501` mostrando l'interfaccia dell'app.

## 🚧 Sviluppi Futuri (Roadmap)

* [ ] Aggiunta della trave appoggiata con carico triangolare.
* [ ] Aggiunta di carichi parzialmente distribuiti.
* [ ] Integrazione di un database o un dizionario con i profili metallici standard (HEA, IPE, ecc.) per precompilare automaticamente il Momento d'Inerzia ($I$).
* [ ] Esportazione dei risultati in PDF.

## 🤝 Contribuire

I contributi sono benvenuti! Se vuoi aggiungere un nuovo schema statico o migliorare l'interfaccia:

1. Fai un Fork del progetto.
2. Crea un tuo branch (`git checkout -b feature/NuovoSchema`).
3. Fai il commit delle tue modifiche (`git commit -m 'Aggiunto schema mensola con carico distribuito'`).
4. Fai il push sul branch (`git push origin feature/NuovoSchema`).
5. Apri una Pull Request.

---

*Sviluppato con ❤️ per l'Ingegneria e l'Architettura.*

```

### Un piccolo consiglio extra:
Nel README ho menzionato un file chiamato `requirements.txt`. È uno standard di GitHub che serve a dire agli altri quali librerie servono per far funzionare il tuo codice. 

Crealo nella stessa cartella e scrivici dentro semplicemente questo:
```text
streamlit
numpy
matplotlib
