from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()

# -------------------- PRODUCTS DATA --------------------
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics"},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery"},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics"},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery"}
]

# -------------------- TASK 1 --------------------
@app.get("/products/search")
def search_products(keyword: str = Query(...)):
    result = []

    for product in products:
        if keyword.lower() in product["name"].lower():
            result.append(product)

    if not result:
        return {"message": f"No products found for: {keyword}"}

    return {
        "keyword": keyword,
        "total_found": len(result),
        "products": result
    }


# -------------------- TASK 2 --------------------
@app.get("/products/sort")
def sort_products(
    sort_by: str = "price",
    order: str = "asc"
):
    if sort_by not in ["price", "name"]:
        return {"error": "sort_by must be 'price' or 'name'"}

    if order not in ["asc", "desc"]:
        return {"error": "order must be 'asc' or 'desc'"}

    reverse = True if order == "desc" else False

    sorted_products = sorted(
        products,
        key=lambda x: x[sort_by],
        reverse=reverse
    )

    return {
        "sort_by": sort_by,
        "order": order,
        "products": sorted_products
    }


# -------------------- TASK 3 --------------------
@app.get("/products/page")
def paginate_products(
    page: int = 1,
    limit: int = 2
):
    if page < 1 or limit < 1:
        return {"error": "page and limit must be greater than 0"}

    total_products = len(products)
    total_pages = (total_products + limit - 1) // limit

    start = (page - 1) * limit
    end = start + limit

    paginated_products = products[start:end]

    return {
        "page": page,
        "limit": limit,
        "total_products": total_products,
        "total_pages": total_pages,
        "products": paginated_products
    }


# -------------------- TASK 4 --------------------
orders = []
order_id_counter = 1


class Order(BaseModel):
    customer_name: str
    product_id: int


@app.post("/orders")
def create_order(order: Order):
    global order_id_counter

    new_order = {
        "order_id": order_id_counter,
        "customer_name": order.customer_name,
        "product_id": order.product_id
    }

    orders.append(new_order)
    order_id_counter += 1

    return {
        "message": "Order created successfully",
        "order": new_order
    }


@app.get("/orders/search")
def search_orders(customer_name: str = Query(...)):
    result = []

    for order in orders:
        if customer_name.lower() in order["customer_name"].lower():
            result.append(order)

    if not result:
        return {"message": f"No orders found for: {customer_name}"}

    return {
        "customer_name": customer_name,
        "total_found": len(result),
        "orders": result
    }
# -------------------- BONUS --------------------
@app.get("/orders/page")
def paginate_orders(
    page: int = 1,
    limit: int = 3
):
    if page < 1 or limit < 1:
        return {"error": "page and limit must be greater than 0"}

    total_orders = len(orders)

    total_pages = (total_orders + limit - 1) // limit

    start = (page - 1) * limit
    end = start + limit

    paginated_orders = orders[start:end]

    return {
        "page": page,
        "limit": limit,
        "total_orders": total_orders,
        "total_pages": total_pages,
        "orders": paginated_orders
    }
# -------------------- TASK 5 --------------------
@app.get("/products/sort-by-category")
def sort_by_category():
    sorted_products = sorted(
        products,
        key=lambda x: (x["category"], x["price"])
    )

    return {
        "message": "Products sorted by category, then price",
        "products": sorted_products
    }
# -------------------- TASK 6 --------------------
@app.get("/products/browse")
def browse_products(
    keyword: str = None,
    sort_by: str = "price",
    order: str = "asc",
    page: int = 1,
    limit: int = 4
):
    result = products

    # 🔍 1. FILTER (search)
    if keyword:
        result = [
            p for p in result
            if keyword.lower() in p["name"].lower()
        ]

    # ↕️ 2. SORT
    if sort_by not in ["price", "name"]:
        return {"error": "sort_by must be 'price' or 'name'"}

    if order not in ["asc", "desc"]:
        return {"error": "order must be 'asc' or 'desc'"}

    reverse = True if order == "desc" else False

    result = sorted(
        result,
        key=lambda x: x[sort_by],
        reverse=reverse
    )

    # 📄 3. PAGINATION
    total_found = len(result)
    total_pages = (total_found + limit - 1) // limit

    start = (page - 1) * limit
    end = start + limit

    paginated_result = result[start:end]

    return {
        "keyword": keyword,
        "sort_by": sort_by,
        "order": order,
        "page": page,
        "limit": limit,
        "total_found": total_found,
        "total_pages": total_pages,
        "products": paginated_result
    }