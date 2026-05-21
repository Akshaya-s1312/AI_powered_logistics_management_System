# AI Powered Logistics Management System

An intelligent logistics management platform built using Flask, Machine Learning, and MongoDB that predicts delivery times, identifies delays, analyzes logistics performance, and optimizes delivery routes.

## Features

- Delivery Time Prediction using Machine Learning
- Delay Prediction System
- Route Optimization
- Dashboard Analytics
- Prediction History Tracking
- MongoDB Database Integration
- Responsive User Interface


## Technologies Used

### Backend
- Python
- Flask

### Machine Learning
- Scikit-learn
- Random Forest Algorithms

### Database
- MongoDB

### Frontend
- HTML
- CSS


## Modules

### Delivery Time Prediction
Predicts estimated delivery time based on:
- Delivery Partner
- Package Type
- Vehicle Type
- Delivery Mode
- Region
- Weather Conditions
- Distance
- Package Weight

### Delay Prediction
Predicts whether a delivery will be delayed or delivered on time.

### Route Optimization
Compares multiple routes and selects the best route based on:
- Distance
- Traffic
- Weather Conditions

### Dashboard
Displays:
- Total Orders
- Average Delivery Time
- Delayed Orders
- On-Time Deliveries

### History Tracking
Stores prediction records in MongoDB for future analysis.


## Project Structure

```bash
deliverytime/
│
├── app.py
├── trainmodel.py
├── More_Realistic_Delivery_Logistics.csv
│
├── templates/
│   ├── index.html
│   ├── dashboard.html
│   ├── history.html
│   ├── route_optimizer.html
│   └── optimized_result.html
│
├── static/
│   └── style.css
│
└── README.md
