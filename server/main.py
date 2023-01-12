from fastapi import FastAPI
import json, os


f = open(os.path.join("data.json"), "r")
data = json.load(f)
f.close()

app = FastAPI()

@app.get("/")
def root():
    return {"message": "hola world"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/wells")
def well_index():
    return {"wells": data}
