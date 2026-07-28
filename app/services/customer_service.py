import pandas as pd

df = pd.read_csv("data/customers.csv")


def get_customer(customer_id: int):

    customer = df[df["customer_id"] == customer_id]

    if customer.empty:
        return None

    return customer.iloc[0].to_dict()