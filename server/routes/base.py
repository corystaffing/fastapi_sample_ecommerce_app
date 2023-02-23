import os, json
from fastapi import Depends, HTTPException, APIRouter, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
import pandas as pd
import seeder

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.get("/seed")
def seed(seed: bool = False, gen: str = None, qty: int = 2):
    result = None
    if seed:
        if gen == 'customers':
            result = seeder.seed_customers(qty)
        elif gen == 'products':
            result = seeder.seed_products(qty)
        elif gen == 'orders':
            pass
            # result = seeder.seed_orders(qty)
            #arguments: 'customer_ids', 'product_ids', 'billing_address_id', and 'shipping_address_id'
        elif gen == 'addresses':
            result = seeder.seed_addresses(qty)
        else:
            result = {"message": "Did not specify a valid generator"}

    else:
        result = {"message": "will not seed without ?seed=true"}

    return result

@router.get("/seed/generate")
def seed_generate(gen: str = None, qty: int = 2):
    result = None
    if gen == 'customers':
        result = seeder.generate_customers(qty)
    elif gen == 'products':
        result = seeder.generate_products(qty)
    elif gen == 'customer':
        result = seeder.generate_customer(for_seeding=False)
    elif gen == 'orders':
        pass
        # result = seeder.generate_orders(qty)
        #arguments: 'customer_ids', 'product_ids', 'billing_address_id', and 'shipping_address_id'
    elif gen == 'addresses':
        result = seeder.generate_addresses(qty)
    else:
        result = {"message": "Did not specify a valid generator"}

    return result

@router.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@router.get("/products")
def product_index(q: str = None):
    data = {}
    return {"product": data, "q": q, "yo": "yo"}

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

# analysis routes
@router.get("/analysis")
def analysis(q: str = None):
    return {"q": q, "message": "todo"}

