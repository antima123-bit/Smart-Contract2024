E-Commerce System with Product Recommendation and Price Modification

Overview
Welcome to the E-Commerce System repository! This project is a comprehensive e-commerce system that encompasses various functionalities such as product management, shopping cart operations, order placement, and product recommendations. Additionally, it features a unique price modification technique utilizing a Sawtooth wave. It also includes a predictive model to enhance product recommendations and visualizations to analyze product orders.

Table of Contents
Features
Setup
Usage
Main Code
Model Code
Sawtooth Wave Modification
Visualizations
Files Description
License
Features
Product Management: Add, remove, update, and display products.
Shopping Cart: Add products to the cart and place orders with simulated transaction failures.
Product Recommendations: Suggest products based on the category of a viewed product.
Price Modification: Adjust product prices using a Sawtooth wave function.
Predictive Model: Build and evaluate a logistic regression model for product recommendations.
Visualizations: Generate visualizations including bar charts, pie charts, and heatmaps.
Setup
Clone the Repository
bash
Copy code
git clone https://github.com/yourusername/ecommerce-system.git
cd ecommerce-system
Install Required Packages
Ensure you have the necessary Python packages installed. You can install them using pip:

bash
Copy code
pip install pandas numpy matplotlib seaborn scikit-learn scipy
Data Files
Ensure that the following CSV files are available in the specified paths:

products.csv
orders.csv
users.csv
Adjust the file paths in the code if necessary.

Usage
Main Code
The main.py file includes the core functionality of the e-commerce system:

Adding Products: Add products with details such as ID, name, price, quantity, and category.
Removing Products: Remove products by their ID.
Updating Products: Update product details using the product ID.
Displaying Products: Show all available products.
Adding to Cart and Placing Orders: Add products to the cart and place orders with a simulated transaction outcome.
Product Recommendations: Get recommendations for similar products based on the category of a viewed product.
Data Simulation: Generate test data for different operations and log conflicts.
Model Code
The model.py file includes the logic for building and evaluating a logistic regression model:

Data Preparation: Load and merge data from CSV files.
Feature Engineering: Encode categorical variables and split data into training and testing sets.
Model Training: Train a logistic regression model.
Model Evaluation: Evaluate the model using accuracy score, classification report, and confusion matrix.
Visualizations: Generate bar charts, pie charts, and heatmaps to visualize product orders and prices.
Prediction: Make predictions using the trained model.
Sawtooth Wave Modification
The swatooth.py file demonstrates how to modify product prices using a Sawtooth wave function:

Displaying Products: Display products with original prices.
Applying Sawtooth Modification: Modify product prices based on a Sawtooth wave.
Visualizing Prices: Compare original and modified prices using bar charts.
Visualizations
Here are some visualizations generated from the project:

Top 5 Products by Number of Orders

Average Order Price by Product Category

Histogram of Order Prices

Temperature Heatmap

Files Description
main.py: Contains the core e-commerce system implementation.
model.py: Contains code for building and evaluating the predictive model.
swatooth.py: Contains code for Sawtooth wave price modification and visualization.
products.csv: Example product data (ensure it matches the format expected in model.py).
orders.csv: Example order data (ensure it matches the format expected in model.py).
users.csv: Example user data (ensure it matches the format expected in model.py).
License
This project is licensed under the MIT License - see the LICENSE file for details.

