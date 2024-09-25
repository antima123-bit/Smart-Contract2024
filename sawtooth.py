import requests
import hashlib
import base64
import numpy as np
from scipy.signal import sawtooth
import matplotlib.pyplot as plt

SAWTOOTH_REST_API_URL = "https://3f0e-2409-40d0-2017-4c12-d38-528a-3538-8ab4.ngrok.io" 

class Product:
    def __init__(self, id, name, price, quantity, category):
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category

def create_product_on_chain(product):
    product_data = f"{product.id},{product.name},{product.price},{product.quantity},{product.category}"
    payload = base64.b64encode(product_data.encode()).decode()

    transaction = {
        "payload": payload,
        "inputs": [product_address(product.id)],
        "outputs": [product_address(product.id)],
        "signer_public_key": "your_public_key",  
        "batcher_public_key": "your_public_key",  
        "dependencies": [],
    }

    url = f"{SAWTOOTH_REST_API_URL}/batches"
    headers = {'Content-Type': 'application/octet-stream'}
    response = requests.post(url, headers=headers, data=transaction)

    if response.status_code == 200:
        print(f"Product {product.name} added to the blockchain.")
    else:
        print(f"Failed to add product: {response.text}")

def product_address(product_id):
    return hashlib.sha512(product_id.encode()).hexdigest()[0:6]

def sawtooth_modification(products):
    time = np.linspace(0, 10, len(products))
    sawtooth_wave = sawtooth(2 * np.pi * time)
    
    print("\nSawtooth wave values applied:")
    print(sawtooth_wave)
    
    for i, product in enumerate(products):
        factor = 1 + sawtooth_wave[i] * 0.1
        product.price = max(1, product.price * factor)
        create_product_on_chain(product)  

def plot_prices(products, original_prices):
    product_names = [product.name for product in products]
    modified_prices = [product.price for product in products]
    
    plt.figure(figsize=(10, 6))
    index = np.arange(len(products))
    bar_width = 0.35
    
    plt.bar(index, original_prices, bar_width, label='Original Prices', color='blue')
    plt.bar(index + bar_width, modified_prices, bar_width, label='Modified Prices', color='green')
    
    plt.xlabel('Products')
    plt.ylabel('Price')
    plt.title("Product Prices Before and After Sawtooth Modification")
    plt.xticks(index + bar_width / 2, product_names, rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

def main():
    products = [
        Product(1, "Sony TV", 999.99, 50, "Electronics"),
        Product(2, "Apple Watch", 299.99, 100, "Electronics"),
        Product(3, "Bottle", 9.99, 200, "Household"),
        Product(4, "Laptop", 1299.99, 30, "Electronics"),
        Product(5, "Headphones", 99.99, 150, "Electronics"),
        Product(6, "Blender", 49.99, 75, "Household"),
        Product(7, "Camera", 499.99, 40, "Electronics"),
        Product(8, "Smartphone", 699.99, 80, "Electronics"),
        Product(9, "Microwave", 89.99, 60, "Household"),
        Product(10, "Desk Lamp", 19.99, 90, "Household")
    ]
    
    original_prices = [product.price for product in products]
    
    sawtooth_modification(products) 
    
    plot_prices(products, original_prices) 

if __name__ == "__main__":
    main()
