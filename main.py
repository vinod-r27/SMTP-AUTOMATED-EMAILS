from datetime import date
import pandas as pd
from send_email import send_email
import logging
from urllib.error import HTTPError

# Setup logging
logging.basicConfig(
    filename="email_reminders.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

SHEET_ID = "1jn6P63PI1xHF5CYI4Ln193_-63mOee_WDJ4g1BOU6Mk"
SHEET_NAME = "data"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

def load_df(url):
    """Loads the invoice data from the given Google Sheets URL."""
    try:
        print("Attempting to load data from URL:", url)  # Debugging statement
        parse_dates = ["due_date", "reminder_date"]
        df = pd.read_csv(url, parse_dates=parse_dates)
        print("Data loaded successfully.")
        return df
    except HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        logging.error(f"HTTP Error: {e.code} - {e.reason}")
        raise ValueError("Failed to load data due to an HTTP error. Please check the URL and access permissions.")
    except Exception as e:
        print(f"Failed to load data: {e}")
        logging.error(f"Failed to load data from URL: {e}")
        raise ValueError("An error occurred while loading data. Please check the URL and the data format.")

def query_data_and_send_emails(df):
    """Sends email reminders for unpaid invoices."""
    present = date.today()
    email_counter = 0

    for _, row in df.iterrows():
        try:
            if pd.notna(row["reminder_date"]) and pd.notna(row["has_paid"]):
                if (present >= row["reminder_date"].date()) and (row["has_paid"].strip().lower() == "no"):
                    send_email(
                        subject=f'[Coding Is Fun] Invoice: {row["invoice_no"]}',
                        receiver_email=row["email"],
                        name=row["name"],
                        due_date=row["due_date"].strftime("%d, %b %Y"),
                        invoice_no=row["invoice_no"],
                        amount=row["amount"],
                    )
                    logging.info(f"Email sent to {row['email']} for Invoice {row['invoice_no']}")
                    email_counter += 1
        except Exception as e:
            logging.error(f"Failed to send email for Invoice {row['invoice_no']}: {e}")

    return f"Total Emails Sent: {email_counter}"

if __name__ == "__main__":
    try:
        df = load_df(URL)
        result = query_data_and_send_emails(df)
        print(result)
    except ValueError as e:
        print(e)
        logging.critical(f"Script failed: {e}")
