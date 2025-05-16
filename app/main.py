from fastapi import FastAPI

app = FastAPI()

@app.get("/data")
@app.get("/data/")
def get_data():
    return {"message": "Hola Paul, tus datos están protegidos!"}
