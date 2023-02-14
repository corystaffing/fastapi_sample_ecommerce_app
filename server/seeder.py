from faker import Faker
import faker_commerce
import random
# import db_setup
from db_setup import *
from pprint import pprint

fake = Faker()
fake.add_provider(faker_commerce.Provider)
# print('------------')
# print('yoooooooooooo')
# print(fake.ecommerce_name())
# print('------------')


random_ids = list(range(1,2000))

def generate_customers(num_customers: int):
    customers = []
    for i in range(num_customers):
        customer              = generate_customer()
        customer["addresses"] = generate_addresses(2)
        customer["orders"]    = generate_orders(2, random_ids, random_ids,
                                                random.choice(customer['addresses'])['id'],
                                                random.choice(customer['addresses'])['id']
                                                )
        customers.append(customer)
    return customers

def generate_customer(for_seeding: bool = False):
    customer = {}
    if not for_seeding: # use a random id if not actually seeding
        customer['id'] = random.randint(1, 1000)

    customer['first_name']   = fake.first_name()
    customer['last_name']    = fake.last_name()
    customer['email']        = f'{customer["first_name"].lower()}.{customer["last_name"].lower()}@example.org'
    customer['phone_number'] = fake.phone_number()
    return customer

def seed_customers(num_customers: int):
    # generate customers list
    # insert into db
    customers = []
    for i in range(num_customers):
        # customer = generate_customer(for_seeding = True)
        # customers.append(customer)
        # or:
        customers.append(generate_customer(for_seeding=True))

    # insert into db
    db = get_db()
    pprint('-------------------------------uiouiouio---------------------------------')
    pprint(db.execute("SELECT CURRENT_TIMESTAMP;"))
    pprint('-------------------------------uiouiouio---------------------------------')

    return {"message": "success"}

def generate_orders(num_orders, customer_ids, product_ids, billing_address_id, shipping_address_id):
    orders = []
    for i in range(num_orders):
        order = {
            "customer_id":         fake.random_element(customer_ids),
            "billing_address_id":  billing_address_id,
            "shipping_address_id": shipping_address_id,
            "product_id":          fake.random_element(product_ids),
            "date":                fake.date_this_century(),
            "quantity":            fake.random_int(min=1, max=50),
            "review_score":        fake.random_int(min=1, max=100),
            "review_text":         fake.text(max_nb_chars=100),
            "total_amount":        fake.pydecimal(left_digits=4, right_digits=2, positive=True)
        }
        orders.append(order)
    return orders

def generate_addresses(num_addresses: int = 1):
    addresses = []
    for i in range(num_addresses):
        address = {
            # this would probably have a first/last name in prod
            "id":           random.randint(1, 2000),
            "customer_id":  random.randint(1, 2000),
            "street":       f'{fake.street_address()} - {fake.secondary_address()}',
            # "address_line_2": fake.secondary_address(),
            "city":         fake.city(),
            "state":        fake.state(),
            "zip":          fake.zipcode(),
            "country_code": "US",
        }
        addresses.append(address)
    return addresses

def generate_products(n: int =10):
    sizes = ['extra small', 'small', 'medium', 'large', 'extra large', 'custom size']

    products = []
    for _ in range(n):
        product = {
            'name':        fake.ecommerce_name(),
            'price':       fake.random_int(min=2, max=100, step=1),
            'category':    fake.random_int(min=1, max=15),
            'color':       fake.color_name(),
            # 'size':        fake.random_int(min=30, max=52),
            'size':        random.choice(sizes),
            'description': fake.text(),
        }
        products.append(product)
    return products
