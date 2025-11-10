"""
Test server minimal pour vérifier l'installation
"""
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="ShareYourSales API - Test")

@app.get("/")
def read_root():
    return {"message": "ShareYourSales API fonctionne !"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Server is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)