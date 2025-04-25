from fastapi import FastAPI
from models import Item  # Import the Item model

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# Example of using Item in your FastAPI routes
@app.get("/items/{item_id}")
def read_item(item_id: int):
    # You can interact with your Item model here
    return {"item_id": item_id}
