#ts for api connection
from fastapi import FastAPI
import pandas as pd
import sqlite3
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
@app.get("/api/finaltable")
def sqlconnection():
    azl= sqlite3.connect("final.db")   
    finaldf= pd.read_sql_query("SELECT * FROM finaltable", azl) 
    return finaldf.to_dict(orient="records")

@app.get("/")
def dashboard():
    return FileResponse("bootstrapped_dashboard.html")