from fastapi import FastAPI

app = FastAPI(
    title="Project Shepherd API",
    version="0.1.0",
    description="API oficial de Project Shepherd"
)


@app.get("/")
def read_root():
    return {
        "message": "Welcome to Project Shepherd API 🚀"
    }