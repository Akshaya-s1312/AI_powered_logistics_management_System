import pandas as pd
import pickle

from sklearn.model_selection import train_test_split

from sklearn.preprocessing import LabelEncoder

from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    accuracy_score
)

df = pd.read_csv(
    "More_Realistic_Delivery_Logistics.csv"
)

df = df.drop(columns=[

    "delivery_id",

    "delivery_status",

    "delivery_rating",

    "delivery_cost",

    "expected_time_hours"
])

delivery_partner_encoder = LabelEncoder()

df["delivery_partner"] = (
    delivery_partner_encoder.fit_transform(
        df["delivery_partner"]
    )
)

package_type_encoder = LabelEncoder()

df["package_type"] = (
    package_type_encoder.fit_transform(
        df["package_type"]
    )
)

vehicle_type_encoder = LabelEncoder()

df["vehicle_type"] = (
    vehicle_type_encoder.fit_transform(
        df["vehicle_type"]
    )
)

delivery_mode_encoder = LabelEncoder()

df["delivery_mode"] = (
    delivery_mode_encoder.fit_transform(
        df["delivery_mode"]
    )
)

region_encoder = LabelEncoder()

df["region"] = (
    region_encoder.fit_transform(
        df["region"]
    )
)

weather_condition_encoder = LabelEncoder()

df["weather_condition"] = (
    weather_condition_encoder.fit_transform(
        df["weather_condition"]
    )
)

delay_encoder = LabelEncoder()

df["delayed"] = (
    delay_encoder.fit_transform(
        df["delayed"]
    )
)

X = df[[

    "delivery_partner",

    "package_type",

    "vehicle_type",

    "delivery_mode",

    "region",

    "weather_condition",

    "distance_km",

    "package_weight_kg"
]]

y_time = df[
    "delivery_time_hours"
]

y_delay = df[
    "delayed"
]

X_train_time, X_test_time, y_train_time, y_test_time = train_test_split(

    X,

    y_time,

    test_size=0.2,

    random_state=42
)

X_train_delay, X_test_delay, y_train_delay, y_test_delay = train_test_split(

    X,

    y_delay,

    test_size=0.2,

    random_state=42
)

time_model = RandomForestRegressor(

    n_estimators=100,

    random_state=42
)

time_model.fit(

    X_train_time,

    y_train_time
)

time_predictions = time_model.predict(
    X_test_time
)

mae = mean_absolute_error(

    y_test_time,

    time_predictions
)

mse = mean_squared_error(

    y_test_time,

    time_predictions
)

r2 = r2_score(

    y_test_time,

    time_predictions
)

print("\n===== DELIVERY TIME MODEL =====")

print(f"MAE : {mae}")

print(f"MSE : {mse}")

print(f"R2 Score : {r2}")

delay_model = RandomForestClassifier(

    n_estimators=100,

    random_state=42
)

delay_model.fit(

    X_train_delay,

    y_train_delay
)

delay_predictions = delay_model.predict(
    X_test_delay
)

accuracy = accuracy_score(

    y_test_delay,

    delay_predictions
)

print("\n===== DELAY MODEL =====")

print(f"Accuracy : {accuracy}")

pickle.dump(

    time_model,

    open(
        "delivery_time_model.pkl",
        "wb"
    )
)

pickle.dump(

    delay_model,

    open(
        "delay_prediction_model.pkl",
        "wb"
    )
)

pickle.dump(

    delivery_partner_encoder,

    open(
        "delivery_partner_encoder.pkl",
        "wb"
    )
)

pickle.dump(

    package_type_encoder,

    open(
        "package_type_encoder.pkl",
        "wb"
    )
)

pickle.dump(

    vehicle_type_encoder,

    open(
        "vehicle_type_encoder.pkl",
        "wb"
    )
)

pickle.dump(

    delivery_mode_encoder,

    open(
        "delivery_mode_encoder.pkl",
        "wb"
    )
)

pickle.dump(

    region_encoder,

    open(
        "region_encoder.pkl",
        "wb"
    )
)

pickle.dump(

    weather_condition_encoder,

    open(
        "weather_condition_encoder.pkl",
        "wb"
    )
)

pickle.dump(

    delay_encoder,

    open(
        "delay_encoder.pkl",
        "wb"
    )
)

print("\nModels and encoders saved successfully.")