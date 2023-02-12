import time

from fastapi import FastAPI
from pydantic import BaseModel
import google.auth
from googleapiclient.discovery import build

# GLOBALS
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets'
]

# App Instantiation
app = FastAPI()

# Modelss


class SheetsRequest(BaseModel):
    sheetId: str
    sheetName: str


@app.get("/health")
def health():
    return "Ok"


@app.post("/example-sheets-read")
def example_sheets_read_func(sheets_request: SheetsRequest):
    return example_sheets_read(sheets_request.sheetId, sheets_request.sheetName)


@app.post("/example-sheets-write")
def example_sheets_write_func(sheets_request: SheetsRequest):
    example_sheets_write(sheets_request.sheetId, sheets_request.sheetName)
    return "Ok"


def example_sheets_read(sheet_id, sheet_name):
    # Get GCP auth and create Sheets API Client
    creds, _ = google.auth.default(scopes=SCOPES)
    service = build("sheets", "v4", credentials=creds)
    sheets_client = service.spreadsheets()

    # Read data from the sheet_id and sheet_range
    sheet_range = f"{sheet_name}!A:Z"
    result = sheets_client.values().get(
        spreadsheetId=sheet_id,
        range=sheet_range
    ).execute()
    values = result.get("values", [])
    return values


def example_sheets_write(sheet_id, sheet_name):
    # Get GCP auth and create Sheets API Client
    creds, _ = google.auth.default(scopes=SCOPES)
    service = build("sheets", "v4", credentials=creds)
    sheets_client = service.spreadsheets()

    # Update the sheet_id/sheet_name with the example values below
    data = [
        "1", "2", "From Cloud Run!", f"{time.time()}"
    ]
    sheet_range = f"{sheet_name}!A1:D1"
    sheet_data = {
        "range": sheet_range,
        "values": [data]
    }
    result = sheets_client.values().update(
        spreadsheetId=sheet_id,
        range=sheet_range,
        valueInputOption="USER_ENTERED",
        body=sheet_data
    ).execute()
    return result
