from flask import Flask, render_template, request
from pymongo import MongoClient
import pickle
import random

app = Flask(__name__)

client = MongoClient(
    "mongodb+srv://akshaya131206_db_user:Akshaya1312*@cluster0.r25leqn.mongodb.net/?appName=Cluster0"
)

mongodb = client["smart_logistics_db"]

collection = mongodb["delivery_predictions"]

time_model = pickle.load(
    open("delivery_time_model.pkl", "rb")
)

delay_model = pickle.load(
    open("delay_prediction_model.pkl", "rb")
)

delivery_partner_encoder = pickle.load(
    open("delivery_partner_encoder.pkl", "rb")
)

package_type_encoder = pickle.load(
    open("package_type_encoder.pkl", "rb")
)

vehicle_type_encoder = pickle.load(
    open("vehicle_type_encoder.pkl", "rb")
)

delivery_mode_encoder = pickle.load(
    open("delivery_mode_encoder.pkl", "rb")
)

region_encoder = pickle.load(
    open("region_encoder.pkl", "rb")
)

weather_condition_encoder = pickle.load(
    open("weather_condition_encoder.pkl", "rb")
)

delay_encoder = pickle.load(
    open("delay_encoder.pkl", "rb")
)

#index page

@app.route("/")
def home():

    return render_template("index.html")

#predict page

@app.route("/predict", methods=["POST"])
def predict():

    delivery_partner = request.form[
        "delivery_partner"
    ]

    package_type = request.form[
        "package_type"
    ]

    vehicle_type = request.form[
        "vehicle_type"
    ]

    delivery_mode = request.form[
        "delivery_mode"
    ]

    region = request.form[
        "region"
    ]

    weather_condition = request.form[
        "weather_condition"
    ]

    distance_km = float(
        request.form["distance_km"]
    )

    package_weight_kg = float(
        request.form["package_weight_kg"]
    )

    delivery_partner_encoded = (
        delivery_partner_encoder.transform(
            [delivery_partner]
        )[0]
    )

    package_type_encoded = (
        package_type_encoder.transform(
            [package_type]
        )[0]
    )

    vehicle_type_encoded = (
        vehicle_type_encoder.transform(
            [vehicle_type]
        )[0]
    )

    delivery_mode_encoded = (
        delivery_mode_encoder.transform(
            [delivery_mode]
        )[0]
    )

    region_encoded = (
        region_encoder.transform(
            [region]
        )[0]
    )

    weather_condition_encoded = (
        weather_condition_encoder.transform(
            [weather_condition]
        )[0]
    )

    features = [[

        delivery_partner_encoded,

        package_type_encoded,

        vehicle_type_encoded,

        delivery_mode_encoded,

        region_encoded,

        weather_condition_encoded,

        distance_km,

        package_weight_kg
    ]]

    predicted_time = time_model.predict(
        features
    )[0]

    predicted_time = round(
        predicted_time,
        2
    )


    if predicted_time <= 0:

        predicted_time = random.randint(
            20,
            60
        )

    delay_prediction = delay_model.predict(
        features
    )[0]

    delay_result = delay_encoder.inverse_transform(
        [delay_prediction]
    )[0]

    order_id = "ORD" + str(
        random.randint(1000, 9999)
    )

    delivery_progress = random.randint(
        1,
        100
    )

    if delivery_progress < 30:

        status = "Order Placed"

    elif delivery_progress < 60:

        status = "Out For Delivery"

    elif delivery_progress < 90:

        status = "Near Destination"

    else:

        status = "Delivered Successfully"

    if delay_result == "yes":

        status = "Delayed"

    prediction_data = {

        "order_id": order_id,

        "delivery_partner": delivery_partner,

        "package_type": package_type,

        "vehicle_type": vehicle_type,

        "delivery_mode": delivery_mode,

        "region": region,

        "weather_condition": weather_condition,

        "distance_km": distance_km,

        "package_weight_kg":
        package_weight_kg,

        "predicted_time_minutes":
        predicted_time,

        "delay_prediction":
        delay_result,

        "delivery_progress":
        delivery_progress,

        "status":
        status
    }

    collection.insert_one(
        prediction_data
    )

    return render_template(

        "index.html",

        order_id=order_id,

        prediction_text=
        f"Estimated Delivery Time: {predicted_time} minutes",

        prediction_value=
        predicted_time,

        delay_text=
        f"Delay Prediction: {delay_result.upper()}",

        status=status,

        delivery_progress=
        delivery_progress
    )

#history page

@app.route("/history")
def history():

    records = collection.find()

    return render_template(

        "history.html",

        records=records
    )

#dashboard page

@app.route("/dashboard")
def dashboard():

    data = list(collection.find())

    total_orders = len(data)

    valid_times = []

    delayed_orders = 0

    for item in data:

        if "predicted_time_minutes" in item:

            valid_times.append(
                item["predicted_time_minutes"]
            )

        if item.get(
            "delay_prediction"
        ) == "yes":

            delayed_orders += 1

    if len(valid_times) > 0:

        avg_time = round(

            sum(valid_times) /
            len(valid_times),

            2
        )

    else:

        avg_time = 0

    ontime_orders = (
        total_orders - delayed_orders
    )

    return render_template(

        "dashboard.html",

        total_orders=total_orders,

        avg_time=avg_time,

        delayed_orders=delayed_orders,

        ontime_orders=ontime_orders
    )

#route optimization

@app.route("/route_optimizer")
def route_optimizer():

    return render_template(
        "route_optimizer.html"
    )

#optimized result

@app.route("/optimize", methods=["POST"])
def optimize():

    routes = []

    distance_A = float(
        request.form["distance_A"]
    )

    traffic_A = request.form["traffic_A"]

    weather_A = request.form["weather_A"]

    eta_A = distance_A * 5

    if traffic_A == "Medium":

        eta_A += 10

    elif traffic_A == "High":

        eta_A += 20

    if weather_A == "Rainy":

        eta_A += 10

    elif weather_A == "Cloudy":

        eta_A += 5

    routes.append({

        "route": "A",

        "distance": distance_A,

        "traffic": traffic_A,

        "weather": weather_A,

        "eta": round(eta_A, 2)
    })

 
    distance_B = float(
        request.form["distance_B"]
    )

    traffic_B = request.form["traffic_B"]

    weather_B = request.form["weather_B"]

    eta_B = distance_B * 5

    if traffic_B == "Medium":

        eta_B += 10

    elif traffic_B == "High":

        eta_B += 20

    if weather_B == "Rainy":

        eta_B += 10

    elif weather_B == "Cloudy":

        eta_B += 5

    routes.append({

        "route": "B",

        "distance": distance_B,

        "traffic": traffic_B,

        "weather": weather_B,

        "eta": round(eta_B, 2)
    })


    distance_C = float(
        request.form["distance_C"]
    )

    traffic_C = request.form["traffic_C"]

    weather_C = request.form["weather_C"]

    eta_C = distance_C * 5

    if traffic_C == "Medium":

        eta_C += 10

    elif traffic_C == "High":

        eta_C += 20

    if weather_C == "Rainy":

        eta_C += 10

    elif weather_C == "Cloudy":

        eta_C += 5

    routes.append({

        "route": "C",

        "distance": distance_C,

        "traffic": traffic_C,

        "weather": weather_C,

        "eta": round(eta_C, 2)
    })


    best_route = min(

        routes,

        key=lambda x: x["eta"]
    )

    return render_template(

        "optimized_result.html",

        routes=routes,

        best_route=best_route
    )

if __name__ == "__main__":

    app.run(debug=True)