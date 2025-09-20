# 💰 SmartSplitter – Community Expense Splitter

SmartSplitter is a Python application to manage and split expenses across multiple families (like Splitwise, but tailored for community events).  
It supports **CSV**, **Google Sheets**, and a **Streamlit web app** interface.

---

## 🚀 Features
- Track expenses across multiple families
- Collates multiple entries per family automatically
- Calculate total spend, equal share, and settlement amounts
- Data sources: **CSV** and **Google Sheets**
- Command-line and **Streamlit web interface**
- Modular design for future extensions (PDF export, databases, etc.)
- Tested with **pytest**

---

## 📂 Project Structure

```
expense-splitter/
│
├── app.py                   # Streamlit web app
├── main.py                  # CLI entry point
├── expenses.py              # Core business logic
├── test_expenses.py         # Tests (pytest)
│
├── storage/                 # Storage backends
│   ├── __init__.py
│   ├── csv_storage.py       # CSV read/write
│   └── sheets_storage.py    # Google Sheets reader
│
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/expense-splitter.git
cd expense-splitter
```

### 2. Create a Virtual Environment
```bash
python3 -m venv smartsplitter-env
source smartsplitter-env/bin/activate   # Linux/Mac
smartsplitter-env\Scripts\activate     # Windows PowerShell
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

(You can regenerate `requirements.txt` at any time by running  
`pip freeze > requirements.txt`.)

### 4.  Set up Google Sheets API credentials
Follow the [gspread documentation](https://docs.gspread.org/en/latest/oauth2.html) to create a service account and enable the Google Sheets API.
Download the JSON credentials file and save it as `credentials.json` in the project's root directory.

---

## 📦 Dependencies
- Python 3.9+
- [Streamlit](https://streamlit.io) – web UI
- [gspread](https://github.com/burnash/gspread) – Google Sheets API client
- [google-auth](https://google-auth.readthedocs.io) – authentication
- [pytest](https://docs.pytest.org/) – testing framework
- Pandas (for CSV handling in Streamlit)

---

## 🖥 Usage

### Run CLI Version
```bash
python main.py
```

### Run Streamlit Web App
```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📝 Tests
Run unit tests:
```bash
pytest -v
```

---

## 🔐 Google Sheets Setup
1. Create a [Google Cloud Project](https://console.cloud.google.com/).
2. Enable **Google Sheets API**.
3. Create a **Service Account** and download `credentials.json`.
4. Place `credentials.json` in the project root.
5. Share your Google Sheet with the service account email (found inside `credentials.json`).

Now the app can fetch data directly from Google Sheets.

---

## 🌍 Deployment
- **Local use:** Run with `streamlit run app.py`
- **Cloud:** Deploy free on [Streamlit Cloud](https://streamlit.io/cloud) so community members can use it without installing anything.

---

## 🤝 Contributing
1. Fork the repo
2. Create a feature branch (`git checkout -b feature/xyz`)
3. Commit changes (`git commit -m "Added xyz"`)
4. Push (`git push origin feature/xyz`)
5. Open a Pull Request

---

## 📜 License
MIT License (free to use, modify, and distribute)
