# ✨ Lumina Scout
### Intelligent Lead Discovery Engine

**Lumina Scout** è un'applicazione avanzata di **Lead Generation** progettata per trovare, analizzare e qualificare potenziali clienti (B2B) sfruttando l'intelligenza artificiale e le API di Google Maps.

A differenza dei semplici scraper, Lumina Scout è costruito per **eliminare il rumore** (PagineGialle, Facebook, aggregatori) e fornire solo **siti web aziendali ufficiali**, arricchiti con dati tecnici (Tech Stack, Chatbot, Email).

---

## 🚀 Funzionalità Chiave

### 1. 🔍 Strategie di Ricerca Avanzate
*   **Google Maps (Local Business)**: Interroga direttamente il database di Maps per trovare attività fisiche nel raggio specificato.
*   **Deep Maps Scan**: L'AI genera automaticamente 8+ varianti della keyword (es. "Discount", "Ipermercato", "Minimarket") per aggirare il limite di risultati di Google e trovare tutto.
*   **Native Web Search**: Fallback su DuckDuckGo o Bing per ricerche globali.

### 2. 🛡️ Filtri Anti-Rumore
*   **Blacklist Severa**: Rimuove automaticamente domini inutili come Facebook, Instagram, Yelp, TripAdvisor, PagineGialle, ecc.
*   **De-Duplicazione**: Controlla lo storico per non farti mai spendere crediti o tempo su URL già analizzati in passato.

### 3. 🧠 Analisi Intelligente (AI)
Per ogni sito trovato, il bot "entra" e analizza:
*   **Tech Stack**: Rileva se usano WordPress, Shopify, Wix, ecc.
*   **Chatbot Detector**: Identifica se è presente un sistema di chat (Intercom, Zendesk, WhatsApp Widget, ecc.).
*   **Try-On Detection**: (Opzionale) Cerca keyword specifiche per tecnologie di prova virtuale (VTO).
*   **Email Scraper**: Estrae email pubbliche e filtra quelle "junk" (es. `sentry@`, `wix@`).

### 4. 📊 Export Professionale
*   **Native Excel (.xlsx)**: Report formattato con colonne auto-adattate, pronto per essere consegnato al cliente o importato nel CRM.
*   **CSV**: Formato standard per integrazioni rapide.

---

## 🛠️ Tecnologie Usate

*   **Frontend**: [Streamlit](https://streamlit.io/) (Interfaccia Reattiva)
*   **Backend**: Python 3.10+
*   **Search API**: [Serper.dev](https://serper.dev/) (Wrapper professionale per Google Maps/Search)
*   **AI Logic**: [OpenAI CLI](https://github.com/openai/openai-python) (Compatibile con OpenRouter, OpenAI o Local LLM)
*   **Data Processing**: Pandas, BeautifulSoup4, OpenPyXL.

---

## 📦 Installazione

1.  **Clona il Repository** (o scarica la cartella):
    ```bash
    git clone https://github.com/tuo-user/lumina-scout.git
    cd lumina-scout
    ```

2.  **Crea un Virtual Environment (Opzionale ma consigliato)**:
    ```bash
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```

3.  **Installa le Dipendenze**:
    ```bash
    pip install -r requirements.txt
    ```
    *(Assicurati che `requirements.txt` includa: `streamlit`, `pandas`, `requests`, `beautifulsoup4`, `openai`, `google-search-python`, `duckduckgo-search`, `openpyxl`, `xlsxwriter`)*

---

## 🎮 Come si Usa

1.  **Avvia l'App**:
    ```bash
    streamlit run app.py
    ```

2.  **Configura nel Sidebar**:
    *   **LLM Provider**: Seleziona OpenRouter (consigliato), OpenAI o Locale.
    *   **Search Engine**: Lascia su **"Google Maps (Local Business)"** per la massima precisione locale.

3.  **Lancia una Ricerca**:
    *   Vai nel tab **"🕵️‍♂️ Auto Scout"**.
    *   **Target**: Scrivi la categoria (es. *"Supermercato"*).
    *   **Location**: Scrivi la città/CAP (es. *"Polla, SA"*).
    *   **Radius**: Seleziona il raggio (es. *20km*).
    *   Clicca **"Start Scouting 🚀"**.

4.  **Analisi & Export**:
    *   L'app mostrerà il progresso in tempo reale.
    *   A fine scansione, scarica il report cliccando su **"Download Excel Report"**.

---

## ⚠️ Risoluzione Problemi Comuni

*   **"Analisi Fallita"**: Succede se un sito è offline o blocca i bot. L'app ora segna "Scrape Fail" ma salva comunque il lead.
*   **Risultati fuori zona**: Se Google Maps restituisce risultati di altre città, prova ad essere più specifico nel campo Location (es. *"84035 Polla SA"* invece di solo *"Polla"*).
*   **Zero Risultati**: Verifica la API Key di Serper o prova ad attivare "Ignore History" se hai già scansionato tutto.

---

**Versione**: 2.0 (Lumina Rebrand)
**Autore**: Antigravity (AI Agent) per User
