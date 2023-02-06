import os, json
from fastapi import Depends, HTTPException, APIRouter, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
import pandas as pd

router = APIRouter()

#for test data
f = open(os.path.join("data.json"), "r")
data = json.load(f)
f.close()

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@router.get("/wells")
def well_index():
    return {"wells": data}

@router.get("/products")
def product_index(q: str = None):
    data = {}
    return {"product": data, "q": q}

@router.get('/products/state')
def product_state():
    #bar chart showing the most popular states that a product is shipped to, based on the order data.

    # Load the orders data into a Pandas DataFrame
    orders = pd.read_csv('orders.csv')

    # Extract the state information from the delivery address
    orders['state'] = orders['delivery_address'].str.extract(r'(\b\w{2}\b)')

    # Group the data by state and count the number of orders for each state
    state_counts = orders.groupby('state').count()['order_id']

    # Sort the data in descending order
    state_counts.sort_values(ascending=False, inplace=True)

    # Plot the results
    state_counts.plot(kind='bar')
