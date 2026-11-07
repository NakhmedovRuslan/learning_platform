from stripe import StripeClient

from config.settings import STRIPE_API_KEY

client = StripeClient(STRIPE_API_KEY)

def create_stripe_product(name):
    """Создание продукта в страйпе"""

    product = client.v1.products.create({"name": name})
    return product

def create_stripe_price(amount):
    """Создание цены в страйп"""
    price = client.v1.prices.create({
        "currency": "rub",
        "unit_amount": amount * 100,
        "recurring": {"interval": "month"},
        "product_data": {"name": "Python-разработчик"},
    })
    return price

def create_stripe_session(price):
    session = client.v1.checkout.sessions.create({
        "success_url": "https://127.0.0.1:8000/",
        "line_items": [{"price": price.get("id"), "quantity": 1}],
        "mode": "subscription",
    })
    return session.get("id"), session.get("url")