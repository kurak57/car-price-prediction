import streamlit as st
import joblib
import os
import pandas as pd

def encode(df, encoder):
# define columns to encode
    categorical_columns = ['Manufacturer', 'Model', 'Category', 'Leather interior', 'Fuel type', 'Gear box type', 'Drive wheels', 'Doors', 'Wheel', 'Color']

    # encode data
    encoder = joblib.load(encoder)
    df_encoded = df.copy()
    df_encoded[categorical_columns] = encoder.transform(df_encoded[categorical_columns])

    #drop needless feature
    df_encoded = df_encoded.drop(columns=['Doors','Cylinders','Drive wheels'])
    return df_encoded

# Attribute information for car price prediction
attribute_info = """
- Levy: Additional fee or tax for the vehicle in USD
- Brand: The manufacturer or brand of the car (e.g., Toyota, Mazda, etc.).
- Model: The specific model of the car (e.g., Elantra, RX 450, etc.).
- Prod. year: The year the vehicle was manufactured.
- Category: The type or category of the car (e.g., sedan, jeep, minibus, etc.).
- Leather interior: Indicates whether the car has a leather interior (yes/no).
- Fuel type: The type of fuel the car uses (e.g., petrol, diesel, hybrid, etc.).
- Engine volume: The engine capacity in liters.
- Mileage: The distance the vehicle has traveled (in kilometers).
- Cylinders: The number of cylinders in the car's engine.
- Gearbox type: The type of gearbox or transmission (e.g., manual, automatic, semi-automatic).
- Drive wheels: The type of drivetrain (e.g., FWD - front-wheel drive, RWD - rear-wheel drive, AWD - all-wheel drive).
- Doors: The number of doors on the vehicle.
- Wheel: The steering side of the vehicle (e.g., left-hand drive or right-hand drive).
- Color: The color of the car (e.g., black, white, red, etc.).
- Airbags: The number of airbags (safety cushions) in the car.
"""

# Streamlit App
def run_ml_app():
    st.title("Car Price Prediction App")

    with st.expander("Attribute Information"):
        st.markdown(attribute_info)

    st.subheader("Input Car Details")

    # Input fields
    levy = st.number_input("Levy (e.g., 0 if no levy)", min_value=0, step=1)
    manufacturer = st.selectbox("Brand", ['Select Brand','LEXUS', 'CHEVROLET', 'HONDA', 'FORD', 'HYUNDAI', 'TOYOTA',
       'MERCEDES-BENZ', 'OPEL', 'PORSCHE', 'BMW', 'JEEP', 'VOLKSWAGEN',
       'AUDI', 'RENAULT', 'NISSAN', 'SUBARU', 'DAEWOO', 'KIA',
       'MITSUBISHI', 'SSANGYONG', 'MAZDA', 'GMC', 'FIAT', 'INFINITI',
       'ALFA ROMEO', 'SUZUKI', 'ACURA', 'LINCOLN', 'VAZ', 'GAZ',
       'CITROEN', 'LAND ROVER', 'MINI', 'DODGE', 'CHRYSLER', 'JAGUAR',
       'ISUZU', 'SKODA', 'DAIHATSU', 'BUICK', 'TESLA', 'CADILLAC',
       'PEUGEOT', 'BENTLEY', 'VOLVO', 'სხვა', 'HAVAL', 'HUMMER', 'SCION',
       'UAZ', 'MERCURY', 'ZAZ', 'ROVER', 'SEAT', 'LANCIA', 'MOSKVICH',
       'MASERATI', 'FERRARI', 'SAAB', 'LAMBORGHINI', 'ROLLS-ROYCE',
       'PONTIAC', 'SATURN', 'ASTON MARTIN', 'GREATWALL'])
    model = st.text_input("Model (e.g., Corolla, X5, etc.)")
    prod_year = st.number_input("Production Year", min_value=1900, max_value=2025, step=1)
    category = st.selectbox("Category",['Jeep', 'Hatchback', 'Sedan', 'Microbus', 'Goods wagon',
                                        'Universal', 'Coupe', 'Minivan', 'Cabriolet', 'Limousine','Pickup'])
    leather_interior = st.selectbox("Leather Interior", ["Yes", "No"])
    fuel_type = st.selectbox("Fuel Type", ['Hybrid', 'Petrol', 'Diesel', 'CNG', 'Plug-in Hybrid', 'LPG', 'Hydrogen'])
    engine_volume = st.number_input("Engine Volume (e.g., 1.6)", min_value=0.0, step=0.1)
    mileage = st.number_input("Mileage (km)", min_value=0, step=1)
    cylinders = st.number_input("Cylinders", min_value=0.0, step=0.1)
    gear_box_type = st.selectbox("Gear Box Type", ['Automatic', 'Tiptronic', 'Variator', 'Manual'])
    drive_wheels = st.selectbox("Drive Wheels", ['4x4', 'Front', 'Rear'])

    doors_display = ['2', '4', '>5']
    doors_mapping = {'2': '02-Mar', '4': '04-May', '>5': '>5'}
    doors = st.selectbox("Doors", doors_display)

    wheel = st.selectbox("Wheel", ['Left wheel', 'Right-hand drive'])
    color = st.text_input("Color (e.g., Red, Black, etc.)")
    airbags = st.number_input("Airbags", min_value=0, max_value=20, step=1)

    data_baru = {
        "Levy": [levy],
        "Manufacturer": [manufacturer],
        "Model": [model],
        "Prod. year": [prod_year],
        "Category": [category],
        "Leather interior": [leather_interior],
        "Fuel type": [fuel_type],
        "Engine volume": [engine_volume],
        "Mileage": [mileage],
        "Cylinders": [cylinders],
        "Gear box type": [gear_box_type],
        "Drive wheels": [drive_wheels],
        "Doors": [doors_mapping[doors]],
        "Wheel": [wheel],
        "Color": [color],
        "Airbags": [airbags]
    }

    
    # Displaying the inputs entered by the user
    with st.expander("Your Input Details"):
        df_new = pd.DataFrame(data_baru)
        st.dataframe(df_new)


    # Prediction Section
    st.subheader("Prediction Result")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_file = os.path.join(base_dir, "car_prediction_model.joblib")
    encoder_file = os.path.join(base_dir, "loo_encoder.joblib")

    # Button to start prediction
    if st.button("Start Prediction"):
        df_encoded = encode(df_new, encoder_file)
        if os.path.exists(model_file):
            model = joblib.load(model_file)
            # Perform prediction
            prediction = model.predict(df_encoded)  # Ensure the model handles preprocessing internally
            st.success(f"The predicted price is: ${round(prediction[0], 2)}")
        else:
            st.error("Model file not found. Please ensure 'car_prediction_model.joblib' is in the same directory.")

# Run the app
if __name__ == "__main__":
    run_ml_app()
    
