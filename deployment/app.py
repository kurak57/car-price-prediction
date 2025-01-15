import streamlit as st
from ml_app import run_ml_app

def main():
    menu = ['Home', 'Car Price Prediction']
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == 'Home':
        st.markdown(
            """
            <h1 style='text-align: center;'>Car Price Prediction: Insights at Your Fingertips</h1>
            <p>
                Understanding the value of a car is essential for both buyers and sellers. 
                With the power of data science and machine learning, we can provide reliable 
                predictions to help you make informed decisions.
            </p>
            <p>Here’s how our car price prediction tool works:</p>
            <ul>
                <li><strong>Data Analysis:</strong> We analyze historical car price data to identify patterns and trends.</li>
                <li><strong>Modeling:</strong> Our machine learning models use factors like brand, model, year, mileage, and condition to predict prices.</li>
                <li><strong>User Input:</strong> Simply provide the required details about the car, and our model will generate an accurate estimate.</li>
                <li><strong>Transparency:</strong> We ensure that our predictions are based on well-tested algorithms and verified data.</li>
            </ul>
            <p>
                Whether you’re buying your dream car or selling one you own, our tool helps you navigate the market with confidence.
            </p>
            <p style='text-align: center;'><strong>Make informed decisions. Predict with confidence.</strong></p>
            """,
            unsafe_allow_html=True
        )

    elif choice == "Car Price Prediction":
        run_ml_app()

if __name__ == '__main__':
    main()
