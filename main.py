from fastapi import FastAPI, UploadFile, File
import pandas as pd
import io
from analysis import analyze_data

app = FastAPI(title="SME Financial Health Platform")

@app.get("/")
def home():
    return {"status": "SME Financial Health API running 🚀"}

@app.post("/analyze")
async def analyze_financial_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))

        print("\n=== EXCEL HEADERS ===")
        print(df.columns)

        print("\n=== FIRST 5 ROWS ===")
        print(df.head())

        result = analyze_data(df)

        return {
            "message": "Analysis completed successfully",
            "results": result
        }

    except Exception as e:
        return {"ERROR": str(e)}
