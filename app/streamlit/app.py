import pandas as pd
import plotly.express as px
import psycopg2
import streamlit as st
from constants import C
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static


# Function to connect to PostgreSQL
def get_connection():
    conn = psycopg2.connect(host=C.HOST, database=C.DBNAME, user=C.USER, password=C.PASSWORD)
    return conn


# Function to fetch data from PostgreSQL
def fetch_data(query):
    conn = get_connection()
    try:
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Error: {str(e)}")
    finally:
        conn.close()


# Streamlit app UI
st.title(":rainbow[Pulse]")
st.subheader(":blue[*A Business Analytics App*]")
# vertical space
st.markdown("<br><br>", unsafe_allow_html=True)


# Define the query
hot_events_query = """SELECT * FROM public_agg.hot_events"""
popular_venues_query = """SELECT * FROM public_agg.popular_venues"""
rsvp_heatmap_query = """SELECT * FROM public_agg.rsvp_heatmap"""
top_active_groups_query = """SELECT * FROM public_agg.top_active_groups"""
trending_topics_query = """SELECT * FROM public_agg.trending_topics"""

# # Fetching data
trending_topics_query_data = fetch_data(trending_topics_query)
hot_events_query_data = fetch_data(hot_events_query)
rsvp_heatmap_query_data = fetch_data(rsvp_heatmap_query)
popular_venues_query_data = fetch_data(popular_venues_query)
top_active_groups_query_data = fetch_data(top_active_groups_query)


#### Hot events
# Set the title for the scorecard section
st.title("🔥 Upcoming Events")

# Create a single row with columns for each event
cols = st.columns(len(top_active_groups_query_data))

for index, row in top_active_groups_query_data.iterrows():
    with cols[index]:
        # Display the participant count on top and the event name below with larger font
        st.markdown(f"""
            <div style="text-align: left;">
                <p style="margin: 0;color: grey;">{row['event_count']} Events</p>
                <h style="font-size: 1.5em; color: white; margin: 0;">{row['group_name']}</h>
            </div>
        """, unsafe_allow_html=True)

#### Top Active Groups
# Set the title for the scorecard section
st.title("Top Active Groups")

# Create a single row with columns for each event
cols = st.columns(len(hot_events_query_data))

for index, row in hot_events_query_data.iterrows():
    with cols[index]:
        # Display the participant count on top and the event name below with larger font
        st.markdown(f"""
            <div style="text-align: left;">
                <p style="margin: 0;color: grey;">{row['rsvp_count']} Participants</p>
                <h style="font-size: 1.5em; color: white; margin: 0;">{row['name']}</h>
            </div>
        """, unsafe_allow_html=True)

#### Trending Topics

# Prepare data for the bar chart
topics = trending_topics_query_data['top_topics']
counts = trending_topics_query_data['topic_cnt']

# Create the bar chart
fig, ax = plt.subplots()
ax.bar(topics, counts, color='skyblue')
ax.set_xlabel("Topics")
ax.set_ylabel("# Events with this topic")
ax.set_title("Top Trending Topics")
plt.xticks(rotation=45, ha="right")

# Display the plot in Streamlit
st.title("Top Trending Topics")
st.pyplot(fig)


#### Popular Venues

st.title("Popular Venues")

# Initialize a map centered on the Netherlands
m = folium.Map(location=[52.3676, 4.9041], zoom_start=7)  # Center around Amsterdam

# Add a pin-style marker for each venue
for index, row in popular_venues_query_data.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"<strong>{row['venue_name']}</strong><br>City: {row['city']}",
        icon=folium.Icon(icon="map-marker", prefix="fa", color="red")  # Red pin marker
    ).add_to(m)

# Display the map in Streamlit
folium_static(m, width=700, height=500)


#### RSVP behaviour

# Pivot the data for heatmap
heatmap_data = rsvp_heatmap_query_data.pivot(index="hour_of_day", columns="day_of_week", values="rsvp_count").fillna(0)

# Streamlit app display
st.title("RSVP Heatmap by Day and Hour")

# Create the heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="YlGnBu", cbar=True)
plt.xlabel("Day of the Week")
plt.ylabel("Hour of the Day")
plt.title("Number of RSVPs per Day and Hour")
st.pyplot(plt)



