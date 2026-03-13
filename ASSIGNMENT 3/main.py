from fastapi import FastAPI, Response, status, Query

app = FastAPI()

# Initial Products
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True}
]

# -----------------------------
# Helper Function
# -----------------------------
def find_product(product_id: int):
    for p in products:
        if p["id"] == product_id:
            return p
    return None


# -----------------------------
# Q1 & Q2 – GET All Products
# -----------------------------
@app.get("/products")
def get_products():
    return {
        "products": products,
        "total": len(products)
    }


# -----------------------------
# Q1 – POST Add Product
# -----------------------------
@app.post("/products")
def add_product(name: str, price: int, category: str, in_stock: bool):

    next_id = max(p["id"] for p in products) + 1

    new_product = {
        "id": next_id,
        "name": name,
        "price": price,
        "category": category,
        "in_stock": in_stock
    }

    products.append(new_product)

    return {
        "message": "Product added successfully",
        "product": new_product
    }


# -----------------------------
# Q4 – PUT Update Price
# -----------------------------
@app.put("/products/{product_id}")
def update_price(product_id: int, price: int, response: Response):

    product = find_product(product_id)

    if not product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Product not found"}

    product["price"] = price

    return {
        "message": "Price updated successfully",
        "product": product
    }


# -----------------------------
# Q3 – DELETE Product
# -----------------------------
@app.delete("/products/{product_id}")
def delete_product(product_id: int, response: Response):

    product = find_product(product_id)

    if not product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Product not found"}

    products.remove(product)

    return {
        "message": f"Product '{product['name']}' deleted"
    }


# -----------------------------
# Q5 – Inventory Audit
# (Must be ABOVE /products/{product_id})
# -----------------------------
@app.get("/products/audit")
def product_audit():

    in_stock_list = [p for p in products if p["in_stock"]]
    out_stock_list = [p for p in products if not p["in_stock"]]

    stock_value = sum(p["price"] * 10 for p in in_stock_list)

    priciest = max(products, key=lambda p: p["price"])

    return {
        "total_products": len(products),
        "in_stock_count": len(in_stock_list),
        "out_of_stock_names": [p["name"] for p in out_stock_list],
        "total_stock_value": stock_value,
        "most_expensive": {
            "name": priciest["name"],
            "price": priciest["price"]
        }
    }


# -----------------------------
# ⭐ BONUS – Bulk Discount
# -----------------------------
@app.put("/products/discount")
def bulk_discount(
    category: str = Query(..., description="Category to discount"),
    discount_percent: int = Query(..., ge=1, le=99, description="Discount percentage")
):

    updated = []

    for p in products:
        if p["category"] == category:
            p["price"] = int(p["price"] * (1 - discount_percent / 100))
            updated.append(p)

    if not updated:
        return {"message": f"No products found in category: {category}"}

    return {
        "message": f"{discount_percent}% discount applied to {category}",
        "updated_count": len(updated),
        "updated_products": updated
    }


# -----------------------------
# GET Single Product
# -----------------------------

@app.get("/products/{product_id}")
def get_product(product_id: int, response: Response):

    product = find_product(product_id)

    if not product:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Product not found"}

    return product