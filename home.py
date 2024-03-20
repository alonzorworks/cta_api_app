import pandas as pd 
import streamlit as st 
from streamlit_lottie import st_lottie
import gmaps
import folium 
from streamlit_folium import st_folium
from ipywidgets import embed
import streamlit.components.v1 as components
import googlemaps
import datetime as dt 
import json
import urllib
from urllib.request import urlopen
import json
# IMPORTANT NOTE: this page is for the online streamlit app where API keys are provided using the web interface.
# If you need to provide your own keys using the .gitignore config use the local file.
#from config import google_map_key   #, cta_bus_tracker_key, cta_train_tracker_key  ---> We only needed the GoogleMap Key Other APIs could be implemented for more information potentially
import requests
#Contigency url import
import urllib.request as urlrq
import certifi
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import io # Will Help us utilize CTA API to connect to Autorefreshed CSV
from ipywidgets import embed
import gmplot
import tempfile
from distutils.version import StrictVersion
from streamlit_folium import st_folium
st.set_option('deprecation.showPyplotGlobalUse', False)
import sys
from PIL import Image
# sys.path.insert(0, 'my_functions/my_functions')
# from functions.my_functions import m
#import functions.my_functions as mf

st.set_page_config(
    page_title="CTA API Project",
    page_icon="🚆",
)


#Image In Sidebar 
with st.sidebar.container():
    image = Image.open(r"images/pictures/ahead_transparent_edit2.png")  
    st.image(image, use_column_width=True)


# Function Section ========================================================================

# Better king 👑
def get_json_from_link(url):
    """Can turn link into a readable JSON format. Actually returns a dictionary that can be converted into a JSON."""
    # Create a custom context that allows all ciphers
    ctx = ssl.create_default_context()
    ctx.set_ciphers('DEFAULT:@SECLEVEL=0')

    # Open the URL with the custom context
    with urlopen(url, context=ctx) as response:
        data = response.read().decode("utf-8")

    return json.loads(data)



def retrieve_cta_route_alerts_all():
    """No credentials are needed."""
    base_url = "https://www.transitchicago.com/api/1.0/alerts.aspx?outputType=JSON"
    return base_url

google_map_key = st.secrets["google_map_key"]

gmaps = googlemaps.Client(key= google_map_key)



#=============================================================================================================






st.header("Chicago CTA API Project 🚌🚐🚶🏿‍♂️🌆")
st.write("This project utilizes APIs made by Google and the Chicago Transit Authority (CTA). With this project users will be able to learn about real time potential impediments on their public transportation commutes.", )

with st.expander("Click to see the Project's Purpose (Mentoring an Intern)"):
    st.subheader("Purpose of This Project")
    st.write("This project was not my idea. An intern came up with this concept. More info will be given on the credits page.")


# Original Code ======================================================    
st.header("Enter in Two Chicago Addresses")
st.write("The addresses must be complete as shown in the exemplars. The two addresses must be unique. 🚨")


start_address = st.text_input(
        "Enter Your Start Address 👇",
        label_visibility= "visible",
        placeholder= "333 W 35th St, Chicago, IL 60616",
    )
if start_address == "":
    start_address = "333 W 35th St, Chicago, IL 60616"

st.write(f"Your Starting Address is: {start_address}")

# End Address
end_address = st.text_input(
        "Enter Your Ending Address 👇",
        label_visibility= "visible",
        placeholder= "2100 W Belmont Ave, Chicago, IL 60618",
    )
if end_address == "":
    end_address = "2100 W Belmont Ave, Chicago, IL 60618"

st.write(f"Your Ending Address is: {end_address}")

# End of Original code ========================================================
# Deleted other intro attempt this one is the best

    

now = dt.datetime.now()









# Will generate a route with directions soon. 
# Will add  Chicago coordinates to give the map a focus point. 

chicago_coordinates = (41.8781, -87.6298)

directions_result = gmaps.directions(start_address,
                                     end_address,
                                     mode="transit",
                                     departure_time=now)

# Converts the default list to JSON which is much more useful. 
directions_json = json.dumps(directions_result)

# We will first collect basic trip info
depart_time = json.loads(directions_json)[0]["legs"][0]["departure_time"]["text"]
arrival_time = json.loads(directions_json)[0]["legs"][0]["arrival_time"]["text"]
travel_time = json.loads(directions_json)[0]["legs"][0]["duration"]["text"]
distance_traveled = json.loads(directions_json)[0]["legs"][0]["distance"]["text"]

# Formatted Addresses
# Overwrites the Address the User Supplies because it is probably enchanced by Google
# May display this to the user later on
start_address = json.loads(directions_json)[0]["legs"][0]["start_address"]
end_address = json.loads(directions_json)[0]["legs"][0]["end_address"]

# Now we should be able to see how many steps we have by getting the length of the list.
num_steps = len(json.loads(directions_json)[0]["legs"][0]["steps"])
st.header(f"Public Transit Directions 🔎📖")
st.subheader(f"There are {num_steps} Steps")


def get_travel_information():
     # Adding All Necessary Variables for Each Step
    step_travel_method = json.loads(directions_json)[0]["legs"][0]["steps"][num]["travel_mode"]
    step_instruction = json.loads(directions_json)[0]["legs"][0]["steps"][num]["html_instructions"]
    step_distance = json.loads(directions_json)[0]["legs"][0]["steps"][num]["distance"]["text"]
    step_duration = json.loads(directions_json)[0]["legs"][0]["steps"][num]["duration"]["text"]
    step_start_lat = json.loads(directions_json)[0]["legs"][0]["steps"][num]["start_location"]["lat"]
    step_start_lng = json.loads(directions_json)[0]["legs"][0]["steps"][num]["start_location"]["lng"]
    step_end_lat = json.loads(directions_json)[0]["legs"][0]["steps"][0]["end_location"]["lat"]
    step_end_lng = json.loads(directions_json)[0]["legs"][0]["steps"][0]["end_location"]["lng"]
    
    # Detail instructions for the for loop.
    # It appears that detail comes before the simple direction.
    step_instruction_detail = json.loads(directions_json)[0]["legs"][0]["steps"][0]["steps"][num]["html_instructions"]
    step_instruction_detail_distance = json.loads(directions_json)[0]["legs"][0]["steps"][0]["steps"][num]["distance"]["text"]
    step_instruction_detail_duration = json.loads(directions_json)[0]["legs"][0]["steps"][0]["steps"][num]["duration"]["text"]
    
    
    return step_travel_method, step_instruction, step_distance, step_duration, step_start_lat, step_start_lng, step_end_lat, step_end_lng, step_instruction_detail, step_instruction_detail_distance, step_instruction_detail_duration
    
# Data Dictionary 📙
route_dict = {
    "step": [],
    "curr_step": [],
    "formatted_step": [],
    "travel_method": [],
    "travel_method_detail": [],
    "distance" : [],
    "step_start_lat": [],
    "step_start_lng" : [],
    "step_end_lat" : [],
    "step_end_lng" : []
}

# Need to have a list of bus and train identifiers to get the 
# MARKER the marker would be '77' for buses 'Red' for train as an example
train_routes = []
bus_routes = []

# MUST MODIFY BY ELIMINATING THE WRITE FILES ONLY 📝📝
# THIS WILLL ALLOW FOR THE MAP TO COME FIRST
for num in range(num_steps):
    # There are multiple sets of steps separated by lists for the complete instructions 
    # These must all be accounted for and recorded 
    
    
    # Adding All Necessary Variables for Each Step
    step_travel_method = json.loads(directions_json)[0]["legs"][0]["steps"][num]["travel_mode"]
    step_instruction = json.loads(directions_json)[0]["legs"][0]["steps"][num]["html_instructions"] # **Look at this don't modify
    step_distance = json.loads(directions_json)[0]["legs"][0]["steps"][num]["distance"]["text"]
    step_duration = json.loads(directions_json)[0]["legs"][0]["steps"][num]["duration"]["text"]
    step_start_lat = json.loads(directions_json)[0]["legs"][0]["steps"][num]["start_location"]["lat"]
    step_start_lng = json.loads(directions_json)[0]["legs"][0]["steps"][num]["start_location"]["lng"]
    step_end_lat = json.loads(directions_json)[0]["legs"][0]["steps"][num]["end_location"]["lat"]
    step_end_lng = json.loads(directions_json)[0]["legs"][0]["steps"][num]["end_location"]["lng"]
    
    # Detail instructions for the for loop.
    # It appears that detail comes before the simple direction. Wil have simple come before complex.
    step_instruction_detail = json.loads(directions_json)[0]["legs"][0]["steps"][num]["html_instructions"]
    
    try:
        step_instruction_detail_distance = json.loads(directions_json)[0]["legs"][0]["steps"][0]["steps"][num]["distance"]["text"]
    except:
        step_instruction_detail_distance = ":orange[(distance not specified)]."
    
    try:
        step_instruction_detail_duration = json.loads(directions_json)[0]["legs"][0]["steps"][0]["steps"][num]["duration"]["text"]
    except:
        step_instruction_detail_duration = ":orange[(estimate not available)]."
        
    
 
    # Current step and total steps
    # Need to add a 1 to compensate for the fact that python counts from 0.
    curr_step = num + 1
    num_steps = len(json.loads(directions_json)[0]["legs"][0]["steps"])
    
    formatted_step = f"({curr_step}/{num_steps})"
    
    # Tells if the person is walking, taking the bus, or subway given in all caps
    travel_mode = json.loads(directions_json)[0]["legs"][0]["steps"][num]["travel_mode"]
    
    try:
        travel_mode_detail = json.loads(directions_json)[0]["legs"][0]["steps"][num]["transit_details"]["line"]["vehicle"]["type"]
    except KeyError:
        travel_mode_detail = "WALK"
        
        
    # This is a NEW section.==============================  👇👇👇👇👇👇👇👇👇👇👇👇👇👇👇
    # This is where we can add the bus or train route.
    # Having this will enable us to plot check for alerts for instructions that involve CTA vehicles.
    # REMEMBER we must try to avoid errors for walking instructions.
    # Public transportation is furnished with additional fields 
    
    
    try:
        if json.loads(directions_json)[0]["legs"][0]["steps"][num]["transit_details"]["line"]["vehicle"]["type"] == "BUS":
                short_route_name = json.loads(directions_json)[0]["legs"][0]["steps"][num]["transit_details"]["line"]["short_name"]
                bus_routes.append(short_route_name)
        elif json.loads(directions_json)[0]["legs"][0]["steps"][num]["transit_details"]["line"]["vehicle"]["type"] == "SUBWAY":
            short_route_name = json.loads(directions_json)[0]["legs"][0]["steps"][num]["transit_details"]["line"]["name"]
            # We need to get the first word which indicates the color of the train station. 
            # We need 'Red' not 'Red Line' therefore we split it.
            train_routes.append(short_route_name.split(" ", 1)[0])
    except:
        pass
          
    
    
    # If Statement to determine the output 
    if step_travel_method == "WALKING":
        st.write(f"""{formatted_step} [{step_travel_method}🚶‍♂️] {step_instruction_detail} for {step_instruction_detail_distance}, which should
             take approximately {step_instruction_detail_duration}. {step_instruction}.""",  unsafe_allow_html=True)
  
    
    
    try:
        turn_step_length = len(json.loads(directions_json)[0]["legs"][0]["steps"][num]["steps"])
        with st.expander(f"See Google Maps-esque Ministeps For Step #{num + 1} 🍬🍭"):
            #st.write("⭐ " + json.loads(directions_json)[0]["legs"][0]["steps"][0]["steps"][0]["html_instructions"], unsafe_allow_html= True)
            for sub_step in range(turn_step_length):
                sub_instruction = json.loads(directions_json)[0]["legs"][0]["steps"][num]["steps"][sub_step]["html_instructions"]
                st.write(f"•  {sub_instruction}", unsafe_allow_html = True)
        
    except KeyError:
        pass
    

    
    if json.loads(directions_json)[0]["legs"][0]["steps"][num]["travel_mode"] == "TRANSIT":
        # Now that we have established that the route is public transportation we can define
        # special variables that pertain to transit only. 
        number_of_stops = json.loads(directions_json)[0]["legs"][0]["steps"][num]["transit_details"]["num_stops"]
        
        # Departure Info
        departure_stop_name = json.loads(directions_json)[0]["legs"][0]["steps"][num]["transit_details"]["departure_stop"]["name"]
        departure_stop_lat = json.loads(directions_json)[0]["legs"][0]["steps"][num]["transit_details"]["departure_stop"]["location"]["lat"]
        departure_stop_lng = json.loads(directions_json)[0]["legs"][0]["steps"][num]["transit_details"]["departure_stop"]["location"]["lng"]
        departure_time = json.loads(directions_json)[0]["legs"][0]["steps"][num]["transit_details"]["departure_time"]["text"]
        
        
        #Arrival Info 
        arrival_stop_name = json.loads(directions_json)[0]["legs"][0]["steps"][num]["transit_details"]["arrival_stop"]["name"]
        arrival_stop_lat = json.loads(directions_json)[0]["legs"][0]["steps"][num]["transit_details"]["arrival_stop"]["location"]["lat"]
        arrival_stop_lng = json.loads(directions_json)[0]["legs"][0]["steps"][num]["transit_details"]["arrival_stop"]["location"]["lng"]
        arrival_time = json.loads(directions_json)[0]["legs"][0]["steps"][num]["transit_details"]["arrival_time"]["text"]
        
        #Route information
        route_headsign = json.loads(directions_json)[0]["legs"][0]["steps"][num]["transit_details"]["headsign"]
        route_name = json.loads(directions_json)[0]["legs"][0]["steps"][num]["transit_details"]["line"]["name"]
        route_duration = json.loads(directions_json)[0]["legs"][0]["steps"][num]["duration"]["text"]
        route_vehicle_type = json.loads(directions_json)[0]["legs"][0]["steps"][num]["transit_details"]["line"]["vehicle"]["type"]
        #Specific Route Is Important Gives Route and Direction
        # Example would be Red Line/Howard.
        specific_route_and_destination = f"{route_name}/{route_headsign}"
        
           # If Statement to determine the output 
        if step_travel_method == "WALKING":
            st.write(f"""{formatted_step} [{step_travel_method}] {step_instruction_detail} for {step_instruction_detail_distance}, which should
                take approximately {step_instruction_detail_duration}. {step_instruction}.""",  unsafe_allow_html=True)
        elif step_travel_method == "TRANSIT":
            st.write(f"""{formatted_step} [{step_travel_method}] Proceed to the {step_instruction_detail} for {step_instruction_detail_distance}, which should
                take approximately {step_instruction_detail_duration}. {step_instruction} ({specific_route_and_destination}).""",  unsafe_allow_html=True)
        
        
        
        # The short route name only pertains to the bus
        # This short name is very important for finding the bus route. 
        # Example would be route 77. Note that in Chicago only buses have short route names. 
        # To avoid throwing an error we will use an if statement to verify we're only dealing with buses.
        
        if json.loads(directions_json)[0]["legs"][0]["steps"][num]["transit_details"]["line"]["vehicle"]["type"] == "BUS":
            short_route_name = json.loads(directions_json)[0]["legs"][0]["steps"][num]["transit_details"]["line"]["short_name"]
            st.write(f"""[🚌] Take the {route_vehicle_type} route {specific_route_and_destination} (#{short_route_name}) from {departure_stop_name} to {arrival_stop_name}.
                    You should leave at {departure_time} and arrive at {arrival_time}. The trip should take about {route_duration}. There are :green[{number_of_stops}] stops.""")
        elif json.loads(directions_json)[0]["legs"][0]["steps"][num]["transit_details"]["line"]["vehicle"]["type"] == "SUBWAY":
            st.write(f"""[🚉] Take the {route_vehicle_type} line {specific_route_and_destination} from {departure_stop_name} to {arrival_stop_name}.
                 You should leave at {departure_time} and arrive at {arrival_time}. The trip should take about {route_duration}. There are :green[{number_of_stops}] stops.""")
     
            
# Add to Dictionaries.
    route_dict["step"].append(num)
    route_dict["curr_step"].append(curr_step)
    route_dict["formatted_step"].append(formatted_step)
    route_dict["travel_method"].append(travel_mode)
    route_dict["travel_method_detail"].append(travel_mode_detail)
    route_dict["distance"].append(step_distance)
    route_dict["step_start_lat"].append(step_start_lat)
    route_dict["step_start_lng"].append(step_start_lng)
    route_dict["step_end_lat"].append(step_end_lat)
    route_dict["step_end_lng"].append(step_end_lng)

# END OF MODIFIED INSTRUCTIONS WHERE WE GET RID OF THE WRITE INSTRUCTIONS ===================================👆👆👆👆👆👆👆👆👆👆👆👆
    
    
# Back to Making the Maps 🗾
# We Need Longitudes and Latitudes for the start and end locations.
start_location_lat = json.loads(directions_json)[0]["legs"][0]["start_location"]["lat"]
start_location_lng = json.loads(directions_json)[0]["legs"][0]["start_location"]["lng"]

end_location_lat = json.loads(directions_json)[0]["legs"][0]["end_location"]["lat"]
end_location_lng = json.loads(directions_json)[0]["legs"][0]["end_location"]["lng"]



gmap = gmplot.GoogleMapPlotter(chicago_coordinates[0], chicago_coordinates[1], apikey= google_map_key, zoom = 14)
gmap.directions(
    (start_location_lat, start_location_lng),
    (end_location_lat, end_location_lng),
    travel_mode = "TRANSIT"
    
)

gmap.draw("map.html")

# Read the HTML file contents
with open("map.html", "r") as f:
    html_contents = f.read()

 #Folium Mapmaking



m = folium.Map(location= (chicago_coordinates[0], chicago_coordinates[1]), zoom_start= 11.2, width= 1500, height = 700)

def map_placeholder(route_dict = route_dict):
    
    coordinate_list = []
    
    # Get the list of coordinates from the dictionary
    # Can get the number of entires in the dictionary lists which are all equal in number 
    num_entries = len(route_dict["step"])
    
    for entry in range(num_entries):
        if route_dict["travel_method"][entry] == "BUS":
            st.write("Yes")
        
            folium.Marker([route_dict["step_start_lat"][entry], 
                            route_dict["step_start_lng"][entry]],
                            popup=('Bus Station{} \n '.format(route_dict["formatted_step"][entry]))
                            ,icon = folium.Icon(color='blue',icon_color='white',prefix='fa', icon='bus')
                            ).add_to(m)
            
        return

num_entries = len(route_dict["step"])

# Preperation for Polyline
list_of_coord = []

# Need to make a list of list 
# Each list should contain coordinates the start coordinate longitude and latitude
# One list for the starting point a second for the end point
# Of course we iterate through the dictionary



# Creates a List of Tuples for Plotting Lines
for coord in range(num_entries):
    list_of_coord.append(tuple((route_dict["step_start_lat"][coord], route_dict["step_start_lng"][coord])))
    list_of_coord.append(tuple((route_dict["step_end_lat"][coord], route_dict["step_end_lng"][coord])))    

# Plots the lines between the points
folium.PolyLine(list_of_coord,
                color='black',
                dash_array='10').add_to(m)


for entry in range(num_entries):
    if route_dict["travel_method_detail"][entry] == "BUS":
        
        folium.Marker([route_dict["step_start_lat"][entry], 
                        route_dict["step_start_lng"][entry]],
                        popup=('Bus Station{} \n '.format(route_dict["formatted_step"][entry]) + " " + route_dict["distance"][entry] + " start of step.")
                        ,icon = folium.Icon(color='blue',icon_color='white',prefix='fa', icon='bus', opacity = 0.7)
                        ).add_to(m)
        
        
        folium.Marker([route_dict["step_end_lat"][entry], 
                        route_dict["step_end_lng"][entry]],
                        popup=('Bus Station{} \n '.format(route_dict["formatted_step"][entry]) + " " + route_dict["distance"][entry] + " end of step.")
                        ,icon = folium.Icon(color='blue',icon_color='#34252F',prefix='fa', icon='bus', opacity = 0.7)
                        ).add_to(m)
        
    elif route_dict["travel_method_detail"][entry] == "SUBWAY":
        
        folium.Marker([route_dict["step_start_lat"][entry], 
                        route_dict["step_start_lng"][entry]],
                        popup=('Train Station{} \n '.format(route_dict["formatted_step"][entry]) + " " + route_dict["distance"][entry] + " start of step.")
                        ,icon = folium.Icon(color='red',icon_color='white',prefix='fa', icon='train', opacity = 0.7)
                        ).add_to(m)
        
        
        folium.Marker([route_dict["step_end_lat"][entry], 
                        route_dict["step_end_lng"][entry]],
                        popup=('Train Station{} \n '.format(route_dict["formatted_step"][entry]) + " " + route_dict["distance"][entry] + " end of step.")
                        ,icon = folium.Icon(color='red',icon_color='#34252F',prefix='fa', icon='train', opacity = 0.7)
                        ).add_to(m)
        
    elif route_dict["travel_method_detail"][entry] == "WALK":
        
        folium.Marker([route_dict["step_start_lat"][entry], 
                        route_dict["step_start_lng"][entry]],
                        popup=('Walk{} \n '.format(route_dict["formatted_step"][entry]) + " " + route_dict["distance"][entry] + " start of step.")
                        ,icon = folium.Icon(color='lightgray',icon_color='white',prefix='fa', icon='user', opacity = 0.7)
                        ).add_to(m)
        
        
        folium.Marker([route_dict["step_end_lat"][entry], 
                        route_dict["step_end_lng"][entry]],
                        popup=('Walk{} \n '.format(route_dict["formatted_step"][entry]) + " " + route_dict["distance"][entry] + " end of step.")
                        ,icon = folium.Icon(color='lightgray',icon_color='#34252F',prefix='fa', icon='user', opacity = 0.7)
                        ).add_to(m)
        
st.header("Visualize The Route 🔎🚌🚆🌎")
with st.expander("Understanding the Map 📝"):
    st.markdown('''
<style>
[data-testid="stMarkdownContainer"] ul{
    padding-left:40px;
}
</style>
''', unsafe_allow_html=True)
    st.markdown("""
                Please note: 
                - The map encompasses all forms of travel by a black dotted line
                - The bus stops are represented by a blue waypoint and a bus icon
                - The train stops are represented by a red waypoint and a train icon
                - The white icon means that it is the bus/train station you start with 
                - The black icon means that is the bus/ train station you end with
                - Some bus and train waypoints may overlap due to closeness of proximity
                - There is a gray person icon that represents walking, the aforementioned logic still applies
                """)

st_folium(m)

st.header("See Alerts For CTA Buses and Trains on Your Route 🚧👷‍♂️👷‍♀️🚍🕴🚉")
st.write("Please Note 📝")
st.write("It is possible that some of these alerts will not be pertinent to you. This is because we are checking the bus/train station itself and not the particular destinations and stops that are within your journeys.")
st.write(f":orange[If nothing shows below that means there are no alerts]!")


# Make a list out of the train and bus lists
bus_routes = list(set(bus_routes))
train_routes = list(set(train_routes))
train_bus_list = train_routes + bus_routes
# Will Use Prep For the Final JSON load
base_alert_json_prep_link = retrieve_cta_route_alerts_all()
baseline_alert = get_json_from_link(base_alert_json_prep_link)
baseline_alert_prep = json.dumps(baseline_alert)



# Python will break up a large list into parts. Note that these lists are still recognized as one making it easier to iterate.
all_alerts_length = len(json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"])
for alert_num in range(all_alerts_length):
    try:
        alert_ser_id = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["ImpactedService"]["Service"][1]["ServiceId"]
        
        for route in train_bus_list:
            
            if alert_ser_id == route:
            
            
                try:
                    
                    # We can use alert ser for apples to apples comparison but we will used the detail one to display the info
                    # Isolating because alert_ser_id is easier to work with making it special 
                    alert_ser_id = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["ImpactedService"]["Service"][1]["ServiceId"]
                    # Note we will use Service Name instead: alert_service_name
                    
                    alert_headline = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["Headline"]
                    alert_id = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["AlertId"]
                    alert_service_id = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["ImpactedService"]["Service"][1]["ServiceId"]
                    alert_service_stop_type = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["ImpactedService"]["Service"][0]["ServiceTypeDescription"]
                    alert_vehicle_desc = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["ImpactedService"]["Service"][0]["ServiceTypeDescription"]
                    alert_service_name = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["ImpactedService"]["Service"][1]["ServiceName"]
                    alert_severity_score = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["SeverityScore"]
                    alert_severity_color = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["SeverityColor"]
                    alert_severity_css = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["SeverityCSS"]
                    alert_impact = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["Impact"]
                    alert_severity_event_start = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["EventStart"]
                    alert_severity_event_end = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["EventEnd"]
                    alert_tbd = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["TBD"] #Boolean
                    alert_major_event_end = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["EventEnd"]
                    alert_url = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["AlertURL"]["#cdata-section"]
                    alert_vehicle_desc = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["ImpactedService"]["Service"][0]["ServiceTypeDescription"]
                    #alert_service_name = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["ImpactedService"]["Service"][0]["ServiceName"]
                    alert_backcolor = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["ImpactedService"]["Service"][0]["ServiceBackColor"]
                    alert_service_url = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["ImpactedService"]["Service"][0]["ServiceURL"]["#cdata-section"]
                    
                    
                    alert_short_description = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["ShortDescription"]
                    alert_full_description = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["FullDescription"]["#cdata-section"]
                
                    st.divider()
                    st.subheader(alert_headline)
                    st.write(f"Alert ID: {alert_id}")
                    st.write(f"{alert_service_name} - {alert_ser_id} {alert_service_stop_type}")
                    st.write(f"Severity score: {alert_severity_score}. SEVERITY: {alert_severity_css}.")
                    st.write(f"Alert severity start date and time: {alert_severity_event_start}")
                    st.write(f"Alert end date and time: {alert_severity_event_end}")
                    
                    with st.expander("Click to see detailed alerts."):
                        st.subheader("Basic Alert Description")
                        st.write(alert_short_description, unsafe_allow_html= True)
                        
                        st.subheader("Detailed Alert Description")
                        st.write(alert_full_description, unsafe_allow_html= True)
                        st.write(f"CTA official webpage concerning this alert. [Link]({alert_service_url}) to page.")
                    
                    st.divider()
                    
                except:
                    pass
        
        else:
            pass    
    except:
        pass


# All Alerts
st.header("All CTA Alerts")
st.subheader("Special Considerations 🌷🌸🌺💮")
st.write(f"Certain bus/train stations may include a code instead of an easily discernable name. Some of these codes if not all of them can be found in CTA's documentation, which can be found [here](https://www.transitchicago.com/developers/ttdocs/).")
st.write("While the header does claim that all alerts are listed this may not be the case. Some alerts may have been skipped if they caused an error when processed in Python.")


if st.button("Click Here to Show All Alerts"):
    for alert_num in range(all_alerts_length):
        #ser_id = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["ImpactedService"]["Service"][1]["ServiceId"]
        # For some reason the above line of code gives issues. ^^^^^^
        
        try:
            
            # We can use alert ser for apples to apples comparison but we will used the detail one to display the info
            # Isolating because alert_ser_id is easier to work with making it special 
            alert_ser_id = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["ImpactedService"]["Service"][1]["ServiceId"]
            # Note we will use Service Name instead: alert_service_name
            
            alert_headline = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["Headline"]
            alert_id = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["AlertId"]
            alert_service_id = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["ImpactedService"]["Service"][1]["ServiceId"]
            alert_service_stop_type = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["ImpactedService"]["Service"][0]["ServiceTypeDescription"]
            alert_vehicle_desc = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["ImpactedService"]["Service"][0]["ServiceTypeDescription"]
            alert_service_name = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["ImpactedService"]["Service"][1]["ServiceName"]
            alert_severity_score = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["SeverityScore"]
            alert_severity_color = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["SeverityColor"]
            alert_severity_css = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["SeverityCSS"]
            alert_impact = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["Impact"]
            alert_severity_event_start = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["EventStart"]
            alert_severity_event_end = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["EventEnd"]
            alert_tbd = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["TBD"] #Boolean
            alert_major_event_end = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["EventEnd"]
            alert_url = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["AlertURL"]["#cdata-section"]
            alert_vehicle_desc = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["ImpactedService"]["Service"][0]["ServiceTypeDescription"]
            #alert_service_name = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["ImpactedService"]["Service"][0]["ServiceName"]
            alert_backcolor = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["ImpactedService"]["Service"][0]["ServiceBackColor"]
            alert_service_url = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["ImpactedService"]["Service"][0]["ServiceURL"]["#cdata-section"]
            
            
            alert_short_description = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["ShortDescription"]
            alert_full_description = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][alert_num]["FullDescription"]["#cdata-section"]
        
            st.divider()
            st.subheader(alert_headline)
            st.write(f"Alert ID: {alert_id}")
            st.write(f"{alert_service_name} - {alert_ser_id} {alert_service_stop_type}")
            st.write(f"Severity score: {alert_severity_score}. SEVERITY: {alert_severity_css}.")
            st.write(f"Alert severity start date and time: {alert_severity_event_start}")
            st.write(f"Alert end date and time: {alert_severity_event_end}")
            
            with st.expander("Click to see detailed alerts."):
                st.subheader("Basic Alert Description")
                st.write(alert_short_description, unsafe_allow_html= True)
                
                st.subheader("Detailed Alert Description")
                st.write(alert_full_description, unsafe_allow_html= True)
                st.write(f"CTA official webpage concerning this alert. [Link]({alert_service_url}) to page.")
            
            st.divider()
            
        except:
            pass

# STREAMLIT USER CAN NOW SEE DIRECTIONS 
# Display the HTML file in Streamlit using st.markdown
#st.markdown(html_contents, unsafe_allow_html=True)

