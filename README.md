# 🌟 E-Commerce System with Product Recommendations & Price Magic 🌟

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)](https://github.com/yourusername/ecommerce-system)
[![Contributors](https://img.shields.io/badge/Contributors-1-orange.svg)](https://github.com/yourusername/ecommerce-system/graphs/contributors)

## Overview
This repository contains a comprehensive e-commerce system implementation with features including product management, cart functionality, order placement, product recommendations, and price modification using the Sawtooth wave. It also includes a predictive model for product recommendations and visualizations to analyze product orders.

## 📚 Table of Contents

- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
  - [Main Code](#main-code)
  - [Model Code](#model-code)
  - [Sawtooth Wave Modification](#sawtooth-wave-modification)
- [Visualizations](#visualizations)
- [Files Description](#files-description)
- [License](#license)

## 🚀 Features

✨ **Product Management:** Add, remove, update, and display products with ease.  
🛒 **Shopping Cart:** Simulate adding products to the cart and placing orders, complete with transaction outcomes.  
🔍 **Product Recommendations:** Get personalized product suggestions based on the category of items you love.  
🔧 **Price Modification:** Watch prices dance with our Sawtooth wave function.  
📈 **Predictive Model:** Leverage logistic regression to enhance product recommendations.  
📊 **Visualizations:** Explore bar charts, pie charts, and heatmaps to get insights into product orders.

## 💻 Setup

### Clone the Repository
git clone https://github.com/yourusername/ecommerce-system.git
cd ecommerce-system

## 🛠️ Usage

### Main Code

The `main.py` file powers the e-commerce magic:

- **Adding Products**: Input products with ID, name, price, quantity, and category.
- **Removing Products**: Remove items by their ID.
- **Updating Products**: Modify product details with a simple ID lookup.
- **Displaying Products**: Showcase all available products.
- **Adding to Cart & Placing Orders**: Simulate adding items to the cart and placing orders.
- **Product Recommendations**: Discover similar products based on your preferences.
- **Data Simulation**: Create test data for different scenarios and log conflicts.

### Model Code

In `model.py`, the logistic regression model shines:

- **Data Preparation**: Merge data from CSV files and get it ready for modeling.
- **Feature Engineering**: Encode categorical data and split into training/testing sets.
- **Model Training**: Train a logistic regression model.
- **Model Evaluation**: Assess model performance with accuracy scores and confusion matrices.
- **Visualizations**: Craft charts and heatmaps to visualize product data.
- **Prediction**: Use the model to make data-driven predictions.

### Sawtooth Wave Modification

With `swatooth.py`, experience price modifications like never before:

- **Displaying Products**: View products with their original prices.
- **Applying Sawtooth Modification**: Adjust prices using the Sawtooth wave function.
- **Visualizing Prices**: Compare original vs. modified prices through bar charts.


## 📊 Visualizations

Explore the insights with these stunning visualizations:

### 📈 Top 5 Products by Number of Orders
![IMG-20240810-WA0008](https://github.com/user-attachments/assets/ba9e2689-c192-45c0-94a5-3610728f57c8)


### 🥧 Average Order Price by Product Category

![IMG-20240810-WA0007](https://github.com/user-attachments/assets/4d4db86a-9900-49b9-a8af-af719cc2b393)

### 📉 Swatooth implement Histogram of Order Prices
![Figure_1](https://github.com/user-attachments/assets/d86338b1-b4c9-4c89-821f-be05c6a77f15)


### 🌡️ Temperature Heatmap
![IMG-20240810-WA0009](https://github.com/user-attachments/assets/f80a992a-f766-4162-bff8-3aa9914b0770)



## 📁 Files Description

- **`main.py`:** The heart of the e-commerce system.  
- **`model.py`:** Where the predictive magic happens.  
- **`swatooth.py`:** Your guide to Sawtooth wave price modifications.  
- **`products.csv`:** Sample product data.  
- **`orders.csv`:** Sample order data.  
- **`users.csv`:** Sample user data.


## 📜 License

This project is licensed under the [MIT License](LICENSE) - check out the LICENSE file for more details.





























