# 💰 Community Expense Splitter

An intuitive Streamlit application designed to simplify expense splitting for groups and communities. This tool helps you easily track and calculate shared expenses, ensuring everyone pays their fair share.

## ✨ Features

- **Flexible Data Import:** Load expense data from either a CSV file or a Google Sheet.
- **Automatic Calculation:** Automatically calculates the total expenses, each member's share, and who owes whom.
- **Clear and Concise Reporting:** Presents a clear breakdown of expenses, individual shares, and settlement details.
- **User-Friendly Interface:** A simple and intuitive web interface built with Streamlit.

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- Pip

### Installation

1.  **Clone the repository:**

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create and activate a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4.  **Set up Google Sheets API credentials:**

    - Follow the [gspread documentation](https://docs.gspread.org/en/latest/oauth2.html) to create a service account and enable the Google Sheets API.
    - Download the JSON credentials file and save it as `credentials.json` in the project's root directory.

### Running the Application

To start the Streamlit application, run the following command in your terminal:

```sh
streamlit run app.py
```

##  usage

1.  **Select Data Source:**

    - Choose between uploading a CSV file or connecting to a Google Sheet.

2.  **Load Data:**

    - **CSV:** Click the "Upload CSV file" button and select your file. The CSV should have columns for "Family" and "Amount".
    - **Google Sheets:** Enter the name of your Google Sheet and click "Load Sheet." The sheet should have columns for "Family" and "Amount."

3.  **View Results:**

    - The application will display a table of the expenses, a summary of the total expenses and each person's share, and a settlement report showing who needs to pay and who should receive money.
