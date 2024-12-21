import json
import streamlit as st
import requests

# Initialize options dictionary
user_options = {}

# App Title
st.title('Loan Default Prediction')

# Load field configurations from JSON
streamlit_options = json.load(open("streamlit_options.json"))

# Create sliders for numerical fields
for field_name, range_values in streamlit_options["slider_fields"].items():
    min_val, max_val = range_values
    if isinstance(min_val, int) and isinstance(max_val, int):
        current_value = (min_val + max_val) // 2  # Midpoint for integers
        user_options[field_name] = st.sidebar.slider(
            field_name, min_val, max_val, value=current_value
        )
    else:
        min_val = float(min_val)
        max_val = float(max_val)
        current_value = round((min_val + max_val) / 2, 2)
        user_options[field_name] = st.sidebar.slider(
            field_name, min_value=min_val, max_value=max_val, value=current_value, step=0.01
        )

# Create dropdowns for categorical fields
for field_name, values in streamlit_options["single_select_fields"].items():
    user_options[field_name] = st.sidebar.selectbox(field_name, values)

# Display user inputs
st.write("User Input Options:")
st.json(user_options)

# Predict Button
if st.button('Predict'):
    data = json.dumps(user_options, indent=2)
    r = requests.post('http://138.197.107.85:80/predict', data=data)

    if r.status_code == 200:
        result = r.json()
        prediction = result['prediction']
        probability = result['probability_of_default']

        # Interpret Prediction
        if prediction == 1:
            st.error("Prediction: High Risk of Default")
        else:
            st.success("Prediction: Low Risk of Default")

        # Explain Probability
        st.info(f"Probability of Default: {probability:.2f}")
        if probability >= 0.5:
            st.warning(
                "This individual has a high probability of defaulting on the loan. "
                "Consider reviewing their application more thoroughly."
            )
        else:
            st.success(
                "This individual has a low probability of defaulting on the loan. "
                "They may be a good candidate for approval."
            )
    else:
        st.error(f"Error: {r.status_code}")