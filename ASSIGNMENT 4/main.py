from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# -------------------------
# PRODUCTS DATABASE
# -------------------------
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 299, "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "in_stock": True}
]

# -------------------------
# STORAGE
# -------------------------
cart = []
orders = []
order_counter = 1


# -------------------------
# PYDANTIC MODEL
# -------------------------
class CheckoutRequest(BaseModel):
    customer_name: str
    delivery_address: str


# -------------------------
# HELPER FUNCTION
# -------------------------
def calculate_total(product, quantity):
    return product["price"] * quantity


# -------------------------
# VIEW PRODUCTS (Q1)
# -------------------------
@app.get("/products")
def get_products():
    return {"products": products}


# -------------------------
# ADD TO CART (Q2)
# -------------------------
@app.post("/cart/add")
def add_to_cart(product_id: int, quantity: int = 1):

    product = next((p for p in products if p["id"] == product_id), None)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if not product["in_stock"]:
        raise HTTPException(status_code=400, detail=f"{product['name']} is out of stock")

    for item in cart:
        if item["product_id"] == product_id:
            item["quantity"] += quantity
            item["subtotal"] = calculate_total(product, item["quantity"])
            return {"message": "Cart updated", "cart_item": item}

    cart_item = {
        "product_id": product["id"],
        "product_name": product["name"],
        "quantity": quantity,
        "unit_price": product["price"],
        "subtotal": calculate_total(product, quantity)
    }

    cart.append(cart_item)

    return {"message": "Added to cart", "cart_item": cart_item}


# -------------------------
# VIEW CART (Q3)
# -------------------------
@app.get("/cart")
def view_cart():

    if not cart:
        return {"message": "Cart is empty"}

    grand_total = sum(item["subtotal"] for item in cart)

    return {
        "items": cart,
        "item_count": len(cart),
        "grand_total": grand_total
    }


# -------------------------
# REMOVE ITEM (Q4)
# -------------------------
@app.delete("/cart/{product_id}")
def remove_item(product_id: int):

    for item in cart:
        if item["product_id"] == product_id:
            cart.remove(item)
            return {"message": "Item removed from cart"}

    raise HTTPException(status_code=404, detail="Item not found in cart")


# -------------------------
# CHECKOUT (Q5 + BONUS)
# -------------------------
@app.post("/cart/checkout")
def checkout(data: CheckoutRequest):

    global order_counter

    # ⭐ BONUS: handle empty cart
    if not cart:
        raise HTTPException(
            status_code=400,
            detail="Cart is empty — add items first"
        )

    placed_orders = []
    grand_total = 0

    for item in cart:

        order = {
            "order_id": order_counter,
            "customer_name": data.customer_name,
            "product": item["product_name"],
            "quantity": item["quantity"],
            "total_price": item["subtotal"],
            "delivery_address": data.delivery_address
        }

        orders.append(order)
        placed_orders.append(order)

        grand_total += item["subtotal"]
        order_counter += 1

    cart.clear()

    return {
        "message": "Checkout successful",
        "orders_placed": placed_orders,
        "grand_total": grand_total
    }


# -------------------------
# VIEW ORDERS (Q6)
# -------------------------
@app.get("/orders")
def view_orders():
    return {
        "orders": orders,
        "total_orders": len(orders)
    }