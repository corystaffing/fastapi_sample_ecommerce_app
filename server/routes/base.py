import os, json
from fastapi import Depends, HTTPException, APIRouter

router = APIRouter()


f = open(os.path.join("data.json"), "r")
data = json.load(f)
f.close()


@router.get("/")
def root():
    return {"message": "hola world"}

@router.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@router.get("/wells")
def well_index():
    return {"wells": data}
