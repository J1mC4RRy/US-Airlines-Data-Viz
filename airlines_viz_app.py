import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
@st.cache_data
def load_data():
    return pd.read_csv("synthetic_airlines_dataset.csv")

data = load_data()

# Sidebar filters
st.sidebar.header("Filters")
selected_airlines = st.sidebar.multiselect("Choose Airlines", data["Airline"].unique())
if not selected_airlines:
    selected_airlines = data["Airline"].unique()
filtered_data = data[data["Airline"].isin(selected_airlines)]

# Visualization 1: Number of flights per airline
st.header("Number of Flights per Airline")
fig1 = px.bar(filtered_data, x="Airline", title="Number of Flights per Airline", 
              labels={"Airline": "Airline"}, height=400)
st.plotly_chart(fig1)

# Preparing data for Visualization 2
city_coordinates = {
    # These are example coordinates; you might need to add or adjust for cities in your dataset.
    "New York": (-74.006, 40.7128),
    "Los Angeles": (-118.2437, 34.0522),
    "Chicago": (-87.6298, 41.8781)
}

flight_paths = data.groupby(["Origin", "Destination"]).size().reset_index(name="Counts")
flight_paths['Origin_lon'] = flight_paths['Origin'].apply(lambda x: city_coordinates.get(x, (0, 0))[0])
flight_paths['Origin_lat'] = flight_paths['Origin'].apply(lambda x: city_coordinates.get(x, (0, 0))[1])
flight_paths['Destination_lon'] = flight_paths['Destination'].apply(lambda x: city_coordinates.get(x, (0, 0))[0])
flight_paths['Destination_lat'] = flight_paths['Destination'].apply(lambda x: city_coordinates.get(x, (0, 0))[1])

# Visualization 2: Flight Paths between Cities
st.header("Flight Paths between Cities")

fig2 = px.scatter_geo(flight_paths,
                      lat=flight_paths['Origin_lat'],
                      lon=flight_paths['Origin_lon'],
                      hover_name="Origin",
                      title="Flight Paths between Cities")

for _, row in flight_paths.iterrows():
    fig2.add_trace(
        px.line_geo(lat=[row['Origin_lat'], row['Destination_lat']],
                    lon=[row['Origin_lon'], row['Destination_lon']])
        .data[0]
    )

st.plotly_chart(fig2)

# Visualization 3: Flight Prices Distribution
st.header("Flight Prices Distribution")
fig3 = px.histogram(filtered_data, x="Price ($)", nbins=50, title="Flight Prices Distribution", height=400)
st.plotly_chart(fig3)

# Visualization 4: Flight Duration by Airline
st.header("Flight Duration by Airline")
fig4 = px.box(filtered_data, x="Airline", y="Flight Duration (hrs)", title="Flight Duration by Airline")

st.plotly_chart(fig4)
