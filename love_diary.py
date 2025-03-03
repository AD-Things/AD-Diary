import streamlit as st
import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials
import json

# Google Sheets Setup
SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]

# Load credentials from Streamlit Secrets
creds_info = json.loads(st.secrets["GOOGLE_SHEETS_CREDENTIALS"])
creds = Credentials.from_service_account_info(creds_info, scopes=SCOPE)

# Connect to Google Sheets
client = gspread.authorize(creds)

# Create or Open a Google Sheet
SHEET_NAME = 'Love Diary'
try:
    sheet = client.open(SHEET_NAME).sheet1
except gspread.SpreadsheetNotFound:
    sheet = client.create(SHEET_NAME).sheet1
    sheet.append_row(["Date", "Message"])

def save_message(message):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([date, message])

def get_messages():
    return sheet.get_all_records()

# Streamlit UI
st.title("💕 Love Diary for Adrija 💕")
st.write("Leave a cute message for your Cutiee!")

# Message Input
message = st.text_area("Write a love note:")

if st.button("Save Message"):
    if message.strip():
        save_message(message)
        st.success("💌 Message saved for Adrija!")
    else:
        st.error("Please write something sweet!")

# Display Messages
st.header("💖 Your Messages for Adrija 💖")
messages = get_messages()
for msg in reversed(messages):
    st.write(f"**{msg['Date']}**: {msg['Message']}")

st.write("Sending virtual hugs to Adrija! 💖")
