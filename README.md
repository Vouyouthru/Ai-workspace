# Personal AI Workspace

A multipage personal AI assistant built with Python, Streamlit, Ollama Cloud, and SQLite.

## Features
- Home dashboard
- Ollama Cloud chat with saved conversation history
- Personal knowledge library (TXT, MD, PDF, DOCX, Python, JSON, CSV, HTML, YAML, TOML, LOG)
- Editable learning profile and assistant instructions
- Saved concepts and simple spaced review
- Settings page with connection test
- Keyword-based retrieval from uploaded files

## 1. Install Python
Install Python 3.11 or newer from https://www.python.org/downloads/ . On Windows, tick **Add Python to PATH** during setup.

## 2. Open the project in VS Code
Extract the ZIP, then open the `personal_ai_workspace` folder in VS Code.

## 3. Create a virtual environment
Open Terminal > New Terminal in VS Code and run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, use Command Prompt in VS Code and run:

```bat
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Get an Ollama Cloud API key
Sign in at https://ollama.com/ and create an API key from your account settings. This project calls the OpenAI-compatible endpoint `https://ollama.com/v1`; it does not require `ollama run` or downloading a model to your PC.

## 5. Run the app
From the project root (the folder containing `app.py`), run:

```powershell
streamlit run app.py
```

Streamlit should open the app in your browser. If it does not, open the local URL printed in the terminal, usually http://localhost:8501 .

## 6. Configure the model
Open **Settings**, paste your Ollama Cloud API key, enter a model name available to your account, save, and press **Test Ollama Cloud connection**. The starter default is `gpt-oss:20b`, but availability may vary by account; if it fails, select a model listed in your Ollama Cloud account and try again. The key remains in the app's session memory while the app is running.

You may instead create a `.env` file in the project root containing:

```text
OLLAMA_API_KEY=your_key_here
OLLAMA_MODEL=gpt-oss:20b
```

Do not share or commit `.env`. Restart Streamlit after changing it.

## 7. Add your existing learning documents
Open **Knowledge Library** and upload your files:
- `Act as my personal learning coach.(1).txt`
- `How I Learn Best(1).txt`
- `Your learning style(1).txt`

You can also copy their contents into the editable Learning Profile page. Uploaded content is extracted and saved in `data/library/`; relevant excerpts may be sent to Ollama Cloud during chat.

## Troubleshooting
- **`streamlit` is not recognized:** activate `.venv` and run `python -m pip install -r requirements.txt` again.
- **API key / 401 / 403 error:** check that the key is correct and active.
- **Model not found / unavailable:** enter a model name currently available to your Ollama Cloud account.
- **Blank page or import error:** make sure you launched `streamlit run app.py` from the project root and check the terminal traceback.
- **PDF text missing:** scanned image-only PDFs need OCR; this starter extracts selectable text only.
- **PowerShell activation blocked:** use the Command Prompt activation command above.

## Data and privacy
- Chat history, document metadata, and review items: `data/workspace.sqlite3`
- Extracted text: `data/library/`
- Learning profile: `profile.json`
- Ollama Cloud receives prompts, chat messages, and retrieved document excerpts. Avoid uploading secrets or sensitive files.

## Current limitations
The document search is keyword overlap, not embedding-based semantic search. The app does not yet support image OCR, multi-user accounts, cloud deployment, or automatic export/backup. It is a local single-user workspace starter.
