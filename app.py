import streamlit as st
import pickle
import numpy as np

# Load the pre-trained model
with open('models/lgbm_model.pkl', 'rb') as file:
    loaded_model = pickle.load(file)


# defining of ordinal mapping
ordinal_mapping = {
    'Very Poor' : 0,
    'Poor': 1,
    'Average':2,
    'Good':3,
    'Excellent':4,
    'Outstanding':5
}


# Defined satisfaction mapping
satisfaction_mapping = {0: 'neutral or dissatisfied', 1: 'satisfied'}


# Function to predict satisfaction
def predict_satisfaction(online_boarding, delay_ratio, inflight_wifi, passenger_class, inflight_entertainment, 
                         flight_distance, seat_comfort, leg_room_service, on_board_service, ease_online_booking, cleanliness):
    
    X_new = np.array([online_boarding, delay_ratio, inflight_wifi, passenger_class, inflight_entertainment, 
                      flight_distance, seat_comfort, leg_room_service, on_board_service, ease_online_booking, cleanliness]).reshape(1, -1)
    
    y_pred_new = loaded_model.predict(X_new)
    return y_pred_new


# streamlit app title and layout 
st.title(':orange[Flight Satisfaction Prediction]')
st.markdown("**Get an instant prediction of flight satisfaction based on various factors.**")

# Created two columns for a better layout 
col1, col2 = st.columns(2)

# Column 1 - Collected Delay and Distance Info
with col1:
    st.header(':red[Flight Information]')

    arrival_delay = st.number_input('Arrival Delay (minutes)', min_value=0.0,step=1.0,help='Total minutes flight was delyed upon arrival.')
    departure_delay = st.number_input('Departure Delay(minutes)',min_value=0.0,step=1.0,help='Total minutes flight was delayed upon departure.')
    flight_distance = st.number_input('Flight Distance(km)',min_value=0.0, value = 1000.0,step=1.0,help='Distance between departure and destination in kilometers.')

    # total delay and delay ratio
    total_delay = arrival_delay + departure_delay
    delay_ratio = (total_delay) / (flight_distance + 1)

# Column 2 - Collected User Preferences for Flight Service
with col2:
    st.header(':red[Service Ratings]')

    inflight_wifi = st.selectbox('Inflight WiFi Service', list(ordinal_mapping.keys()), help = 'Rate the inflight WiFi service.')

    online_boarding = st.selectbox('Online Boarding',list(ordinal_mapping.keys()), help='Rate the online boarding process.')

    ease_online_booking = st.selectbox('Ease of Online Booking', list(ordinal_mapping.keys()),help='Rate the ease of booking the flight process.')

    seat_comfort = st.selectbox('Seat Comfort', list(ordinal_mapping.keys()),help='Rate the comfort level of the seat.')

    inflight_entertainment = st.selectbox('Inflight Entertainment',list(ordinal_mapping.keys()),help='Rate the inflight entertainment options.')

    on_board_service = st.selectbox('On-board service',list(ordinal_mapping.keys()),help='Rate the quality of on-board service.')

    leg_room_service = st.selectbox('Leg Room Service',list(ordinal_mapping.keys()),help = 'Rate the legroom space during the flight.')

    cleanliness = st.selectbox('Cleanliness', list(ordinal_mapping.keys()), help = 'Rate the cleanliness of the flight environment.')

    # Converted ordinal inputs to numeric values
    inflight_wifi_num = ordinal_mapping[inflight_wifi]
    online_boarding_num = ordinal_mapping[online_boarding]
    ease_online_booking_num = ordinal_mapping[ease_online_booking]
    seat_comfort_num = ordinal_mapping[seat_comfort]
    inflight_entertainment_num = ordinal_mapping[inflight_entertainment]
    on_board_service_num = ordinal_mapping[on_board_service]
    leg_room_service_num = ordinal_mapping[leg_room_service]
    cleanliness_num = ordinal_mapping[cleanliness]

# Organized additiional options in a horizontal layout
st.header(':red[Additional Travel Information]')

# Convertion of class and Age to numeric values


passenger_class = st.selectbox('Class',['Business','Eco','Eco Plus'], help='Specify the class of your travel.')

class_mapping = {
        'Business':0,
        'Eco':1,
        'Eco Plus': 2
    }


passenger_class_num = class_mapping[passenger_class]

# Button to make the prediction
if st.button('Predict Satisfaction'):
    # Make the prediction
    prediction = predict_satisfaction(online_boarding_num, delay_ratio, inflight_wifi_num, passenger_class_num, 
                                      inflight_entertainment_num, flight_distance, seat_comfort_num, leg_room_service_num, 
                                      on_board_service_num, ease_online_booking_num, cleanliness_num)

    # Maping of the numeric prediction to satisfaction label
    satisfaction_label =satisfaction_mapping[int(prediction[0])]

    # Display the prediction with interactivity
    if satisfaction_label == 'satisfied':
        st.success(f'✅ ** Prediction: {satisfaction_label.capitalize()} **')
    else:
        st.warning(f'⚠️ ** Prediction: {satisfaction_label.capitalize()} **')

