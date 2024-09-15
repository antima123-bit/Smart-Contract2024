import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import sawtooth

class Product:
    def __init__(self, id, name, price, quantity, category):
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category

#to display products
def show_products(products, title):
    print(title)
    for product in products:
        print(f"ID: {product.id} | Name: {product.name} | Price: ${product.price:.2f} | Quantity: {product.quantity} | Category: {product.category}")

def sawtooth_modification(products):
  
    time = np.linspace(0, 10, len(products))  # Generate time values for sawtooth wave
    sawtooth_wave = sawtooth(2 * np.pi * time)
    
    print("\nSawtooth wave values applied:")
    print(sawtooth_wave)  
    
    for i, product in enumerate(products):
        factor = 1 + sawtooth_wave[i] * 0.1 
        product.price = max(1, product.price * factor) 

def plot_prices(products, original_prices, title):
    product_names = [product.name for product in products]
    modified_prices = [product.price for product in products]
    
    plt.figure(figsize=(10, 6))
    index = np.arange(len(products))
    bar_width = 0.35
    
    plt.bar(index, original_prices, bar_width, label='Original Prices', color='blue')
    plt.bar(index + bar_width, modified_prices, bar_width, label='Modified Prices', color='green')
    
    plt.xlabel('Products')
    plt.ylabel('Price')
    plt.title(title)
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
    
    show_products(products, "Original Products:")
    

    original_prices = [product.price for product in products]
    
    sawtooth_modification(products)
    
    show_products(products, "\nProducts after Sawtooth Price Modification:")
    
    plot_prices(products, original_prices, "Product Prices Before and After Sawtooth Modification")

if __name__ == "__main__":
    main()
