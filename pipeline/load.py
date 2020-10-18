from pipeline.extract import read_unf_csv
from pipeline.transform import transform_rows, transform_row, data
from pipeline.persistance import connection, query, update
import uuid

db = connection("CapsuleCorp")


def load_location_row(row):
    l_id = None
    location_name = row[1]

    checkDbQuery = f"""SELECT id FROM Location WHERE l_name ='{location_name}' """
    updateDbQuery = f""" INSERT INTO Location (id, l_name) VALUES (%s, %s)"""

    check = query(db, checkDbQuery)

    if len(check) == 0:
        l_id = str(uuid.uuid4())
        update(db, updateDbQuery, (l_id, location_name))
    else:
        l_id = check[0][0]
    
    return l_id

def load_transaction_row(row, l_id):

    updateDbQuery = f""" INSERT INTO Transaction (id, date_time, l_id, payment_type, total) VALUES (%s, %s, %s, %s, %s)"""
    tsac_id = str(uuid.uuid4())
    date_time = row[0]
    payment_type = row[3]
    total = row[4]

    update(db, updateDbQuery, (tsac_id, date_time, l_id, payment_type, float(total)))

    return tsac_id

def load_product_row(row):
    p_id = None
    checkDbQuery = f"""SELECT id FROM Product WHERE size = '{product['size']}' AND name = '{product['name']}' AND price = '{float(product['price'])}'"""
    updateDbQuery = """INSERT INTO Product ( id, size, name, price) VALUES (%s, %s, %s, %s)"""
    id_dict = {}
    basket = row[2]

    for product in basket:
        check = query(db, checkDbQuery)
        if len(check) == 0:
            p_id = str(uuid.uuid4())
            update(db, updateDbQuery, (p_id, product['size'], product['name'],product['price']))
        else:
            p_id = check[0][0]
        prod = {p_id: product['price']}
        id_dict.update(prod)
        
    return id_dict
    

   



def load_orders_row(d_time, tsac_id, p_id, price):
    updateDbQuery = """INSERT INTO Orders (date_time, tsac_id, prod_id, price) VALUES (%s, %s, %s, %s)"""

    update(db, updateDbQuery, (d_time, tsac_id, p_id, price))






def load_by_row(t_data):

    for row in t_data:

        date = row[0]
        l_id = load_location_row(row)
        tsac_id = load_transaction_row(row, l_id)
        id_list = load_product_row(row)

        for p_id, price in id_list.values():

            load_orders_row(date, tsac_id, p_id, price)

        

