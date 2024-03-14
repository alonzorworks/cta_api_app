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
from config import google_map_key, cta_bus_tracker_key, cta_train_tracker_key
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

# CTA Train Stops is an API That Does Not Need a key to access
cta_train_stops = requests.get("https://data.cityofchicago.org/resource/8pix-ypme.csv")
cta_train_stops = cta_train_stops.content
df_train = pd.read_csv(io.StringIO(cta_train_stops.decode("utf-8")))

st.subheader("Train Data")
df_train

# df_train_unique = df_train.copy()
# df_train_unique = df_train_unique.drop_duplicates("stop_name")
# df_train_unique

# CTA Bus Stops No Key Needed
cta_bus_stops = requests.get("https://data.cityofchicago.org/resource/qs84-j7wh.csv")
cta_bus_stops = cta_bus_stops.content
df_bus = pd.read_csv(io.StringIO(cta_bus_stops.decode("utf-8")))

st.subheader("Bus Data")
df_bus



# Now Timestamp 
now = dt.datetime.now()

# Lat is North and South. Long is east and west. Latitude comes first.
chicago_coordinates = (41.8781, -87.6298)

# Obselete code that only worked for propper SSL certificates
# def get_json_from_link(url):
#     """Can turn link into a readable JSON format."""
    
#     #Good code preserved =======
#     ssl._create_default_https_context = ssl._create_unverified_context
    
#     response = urlopen(url)
#     data = response.read().decode("utf-8")
#     return json.loads(data)
    #Preserve==========
    
   
    

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

# Create Requests for CTA API Function
def retrieve_cta_bus_json(api_key, bus_route_number):
    """Can use api key to get the JSON with all information available.
    The bus number can be a single one. Or it can be a list of strings. 
    I.E 'X1,X2' these must be concactenated into one string seperated by commas.
    """
    base_url = f"https://www.ctabustracker.com/bustime/api/v2/getvehicles?key={api_key}&rt={bus_route_number}&format=json"
    #base_url = f"http://www.ctabustracker.com/bustime/api/v2/gettime?key={api_key}&format=json"
    
    # Example route instead of the variable (verified to work)
    #base_url = f"https://www.ctabustracker.com/bustime/api/v2/getvehicles?key={api_key}&rt=77&format=json"
        
    return base_url 


def retrieve_cta_train_json(api_key, mapid):
    """Need to have the Stop ID. This encompasses the rt and final destination. Need to use a table to get the number.
    
    Stop ID is an integer with 5 numbers. 
    
    XXXXX = Starting Train Stop (End of The Line)
    
    Need to have from the google api key
    
    "rt":"Red Line"
    "destNm":"Howard"
    Basically only need the delay boolean 
    "isDly"
    
    
    Sample URL:
    http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key=a8456djbhf8475683jf7818bha81&mapid=40380&max=5
    
    
    """
    
    
    
    # base_url = f"https://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key={api_key}&stpid=40190"
    base_url = f"https://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key={api_key}&mapid={mapid}&outputType=JSON"
    
    
    return base_url

def retrieve_cta_route_alerts_all():
    """No credentials are needed."""
    base_url = "https://www.transitchicago.com/api/1.0/alerts.aspx?outputType=JSON"
    return base_url

def retrieve_cta_route_alerts_specified(route_id):
    """No credentials are needed."""
    base_url = f"https://www.transitchicago.com/api/1.0/alerts.aspx?routeid={route_id}&outputType=JSON"
    return base_url

# TRAVEL APIs ================================================================================================ 🚌🚇
# Bus API
st.subheader("Bus JSON")
# TO get this working we need to use two functions
# retrieve_cta_bus_json
# get_json_from_link
base_bus_json_prep_link = retrieve_cta_bus_json(cta_bus_tracker_key, "77")
baseline_bus = get_json_from_link(base_bus_json_prep_link)
st.write(baseline_bus, unsafe_allow_html= True)


# Train API
st.subheader("Train JSON")
base_train_json_prep_link = retrieve_cta_train_json(cta_train_tracker_key, "40190")
baseline_train = get_json_from_link(base_train_json_prep_link)
st.write(baseline_train, unsafe_allow_html= True)

# General API
st.subheader("CTA Alert JSON")
base_alert_json_prep_link = retrieve_cta_route_alerts_all()
baseline_alert = get_json_from_link(base_alert_json_prep_link)

# Will Use Prep For the Final JSON load
baseline_alert_prep = json.dumps(baseline_alert)


st.write(baseline_alert, unsafe_allow_html= True)

gmaps = googlemaps.Client(key= google_map_key)

# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

st.title("CTA Project 🚄🚆🚌🚇🚍")
st.subheader("CTA Directions JSON")

# Default directions except driving is now transit location Australia 
directions_result = gmaps.directions("Sydney Town Hall",
                                     "Parramatta, NSW",
                                     mode="transit",
                                     departure_time=now)

# Checking to see if Chicago is More Detailed 
directions_result = gmaps.directions("333 W 35th St, Chicago, IL 60616",
                                     "2100 W Belmont Ave, Chicago, IL 60618",
                                     mode="transit",
                                     departure_time=now)




# Converts the default list to JSON which is much more useful. 
directions_json = json.dumps(directions_result)

# Trip information
depart_time = json.loads(directions_json)[0]["legs"][0]["departure_time"]["text"]
arrival_time = json.loads(directions_json)[0]["legs"][0]["arrival_time"]["text"]
travel_time = json.loads(directions_json)[0]["legs"][0]["duration"]["text"]
distance_traveled = json.loads(directions_json)[0]["legs"][0]["distance"]["text"]

# Formatted Addresses
start_address = json.loads(directions_json)[0]["legs"][0]["start_address"]
end_address = json.loads(directions_json)[0]["legs"][0]["end_address"]


# Testing areas ============================================
st.write(json.loads(directions_json)[0]["legs"][0])

st.subheader("Important Steps JSON")
st.write(json.loads(directions_json))

# Need Steps 
st.subheader("Route Step JSON")
route_steps = json.loads(directions_json)[0]["legs"][0]["steps"] 
st.write(route_steps)

# Basic Instructions 
# For everything step related the 0 will have to be replaced with an actual counter in the range.
# This will enable it to iterate over the steps.

# NOTE 
# BETA TESTING VAL
# Now by looking at the JSON it appears that (direction_json)[0] is constant
# It seems that ["legs"][0] is constant as well.
# The only thing that we will have to iterate over must be ["steps"] this will be replaced by a num as we iterate over the range


step_travel_method = json.loads(directions_json)[0]["legs"][0]["steps"][0]["travel_mode"]
step_instruction = json.loads(directions_json)[0]["legs"][0]["steps"][0]["html_instructions"]
step_distance = json.loads(directions_json)[0]["legs"][0]["steps"][0]["distance"]["text"]
step_duration = json.loads(directions_json)[0]["legs"][0]["steps"][0]["duration"]["text"]
step_start_lat = json.loads(directions_json)[0]["legs"][0]["steps"][0]["start_location"]["lat"]
step_start_lng = json.loads(directions_json)[0]["legs"][0]["steps"][0]["start_location"]["lng"]
step_end_lat = json.loads(directions_json)[0]["legs"][0]["steps"][0]["end_location"]["lat"]
step_end_lng = json.loads(directions_json)[0]["legs"][0]["steps"][0]["end_location"]["lng"]

# Detail Section That Gives More Info on HTML Directions etc. 
# The detail gives you where to turn. This is essential for useful instructions.Must come after the simple step instructions.
# Will also label the distance under the detail nomenclature for organizational purposes.
step_instruction_detail = json.loads(directions_json)[0]["legs"][0]["steps"][0]["steps"][0]["html_instructions"]
step_instruction_detail_distance = json.loads(directions_json)[0]["legs"][0]["steps"][0]["steps"][0]["distance"]["text"]
step_instruction_detail_duration = json.loads(directions_json)[0]["legs"][0]["steps"][0]["steps"][0]["duration"]["text"]



# Now we should be able to see how many steps we have by getting the length of the list.
num_steps = len(json.loads(directions_json)[0]["legs"][0]["steps"])
st.header(f"{num_steps}")


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
# MARKER
train_routes = []
bus_routes = []


st.divider()
# Now we can make the for loop utilizing the logic that we ironed out earlier 
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
    # It appears that detail comes before the simple direction.
    # Code below does not iterate over the detailed
    #step_instruction_detail = json.loads(directions_json)[0]["legs"][0]["steps"][0]["steps"][num]["html_instructions"]
    #step_instruction_detail = json.loads(directions_json)[0]["legs"][0]["steps"][0]["steps"][num]["html_instructions"]
    step_instruction_detail = json.loads(directions_json)[0]["legs"][0]["steps"][num]["html_instructions"]
    
    
    step_instruction_detail_distance = json.loads(directions_json)[0]["legs"][0]["steps"][0]["steps"][num]["distance"]["text"]
    step_instruction_detail_duration = json.loads(directions_json)[0]["legs"][0]["steps"][0]["steps"][num]["duration"]["text"]
    
    # Turn step attempt 
    # Need to determine the lengths of embedded steps
    # Not every step will have this so we must use try keyword
    # try:
    #     turn_step_length = len(json.loads(directions_json)[0]["legs"][0]["steps"][num]["steps"])
    #     #st.write("⭐ " + json.loads(directions_json)[0]["legs"][0]["steps"][0]["steps"][0]["html_instructions"], unsafe_allow_html= True)
    #     st.write(f"Pre-requisute Ministeps For Step #{num + 1} 🍬🍭")
    #     for sub_step in range(turn_step_length):
    #         sub_instruction = json.loads(directions_json)[0]["legs"][0]["steps"][num]["steps"][sub_step]["html_instructions"]
    #         st.write(f"•  {sub_instruction}", unsafe_allow_html = True)
        
    # except KeyError:
    #     pass
    
    
    
    
    # Get the Bus or Train Route
    # BUS Route
    
    
    
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
        
        
    # This is a NEW section.==============================
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
        
    
    
    
    #Good code
    
    # st.write(f"""{formatted_step} [{step_travel_method}] {step_instruction} {step_instruction_detail} for {step_instruction_detail_distance} which should
    #          take approximately {step_instruction_detail_duration}.""",  unsafe_allow_html=True) # Steps out of order on this one.
    
    # Greater code======================================================
    # Good Baseline but needs to be customized to avoid the API 's awkward phraseology.
    # st.write(f"""{formatted_step} [{step_travel_method}] {step_instruction_detail} for {step_instruction_detail_distance}, which should
    #          take approximately {step_instruction_detail_duration}. {step_instruction}.""",  unsafe_allow_html=True)
    # ==============================================
    
    
    # If Statement to determine the output 
    if step_travel_method == "WALKING":
        st.write(f"""{formatted_step} [{step_travel_method}🚶‍♂️] {step_instruction_detail} for {step_instruction_detail_distance}, which should
             take approximately {step_instruction_detail_duration}. {step_instruction}.""",  unsafe_allow_html=True)
    # elif step_travel_method == "TRANSIT":
    #     st.write(f"""{formatted_step} [{step_travel_method}] Proceed to the {step_instruction_detail} for {step_instruction_detail_distance}, which should
    #          take approximately {step_instruction_detail_duration}. {step_instruction}.""",  unsafe_allow_html=True)
        
        
    
    
    try:
        turn_step_length = len(json.loads(directions_json)[0]["legs"][0]["steps"][num]["steps"])
        with st.expander(f"See Google Maps-esque Ministeps For Step #{num + 1} 🍬🍭"):
            #st.write("⭐ " + json.loads(directions_json)[0]["legs"][0]["steps"][0]["steps"][0]["html_instructions"], unsafe_allow_html= True)
            for sub_step in range(turn_step_length):
                sub_instruction = json.loads(directions_json)[0]["legs"][0]["steps"][num]["steps"][sub_step]["html_instructions"]
                st.write(f"•  {sub_instruction}", unsafe_allow_html = True)
        
    except KeyError:
        pass
    
    
    
    
    # st.info(json.loads(directions_json)[0]["legs"][0]["steps"][num]["travel_mode"])
    
    
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
    
    
    
        # st.info(number_of_stops)
        # st.success("Public Transportation")
    
    # Bus Route
    
    
    # Need to use if statement based off of method of travel to supplement instructions.
    # By using this method we can avoid dealing with error handling. Try, finally etc.
    # We will use elif because we only want one of these stipulations to fire off. 
    
    
    
    # if step_travel_method == "WALKING":
    #     st.success(step_travel_method)
    #     st.write(f"""{formatted_step} [{step_travel_method}] {step_instruction_detail} for {step_instruction_detail_distance} which should
    #             take approximately {step_instruction_detail_duration}. {step_instruction}.""",  unsafe_allow_html=True)
    # if step_travel_method == "TRANSIT":
    #     get_travel_information
    #     st.header("Seperator 🎪")
    #     st.info(step_travel_method)
    #     public_transport_method_type = json.loads(directions_json)[0]["legs"][0]["steps"][0]["steps"][num]#["transit_details"]
        
    #     st.write(public_transport_method_type)
        
    
    
    
    # Now we can try 

st.divider()

st.write(route_dict)

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

# Display the HTML file in Streamlit
#st.components.v1.html(html_contents, height=600)

# Display the HTML file in Streamlit using st.markdown
st.markdown(html_contents, unsafe_allow_html=True)

# Folium Mapmaking

st.write(route_dict["travel_method"])

m = folium.Map(location= (chicago_coordinates[0], chicago_coordinates[1]), zoom_start= 11)

def map_path(route_dict = route_dict):
    
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

st.write(route_dict["travel_method_detail"])

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
        


st.header("Map Making 🌎🗾")
st_folium(m, width= 500)





# Train ServiceId is the color of the line service id for redline is 'Red'
# Need the JSON path to the color
# ServiceType is either a B or T for bus or train
# Iterate over JSON listings with all bus and train routes 
# Can even seperate the bus and train iterations for effiencies 
# Service ID for the bus is the bus number i.e "81"
# Booleans include MajorAlert TBD etc.
st.header("Check for Delays in Route")

bus_routes = list(set(bus_routes))
train_routes = list(set(train_routes))
detail_alert = json.loads(baseline_alert_prep)

# Python will break up a large list into parts. Note that these lists are still recognized as one making it easier to iterate.
all_alerts_length = len(json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"])

st.write(f"There are :green[{all_alerts_length}] alerts.")

# Will Outline Important Values that we can place in the for loop
json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][0] # This is how we get to the list of alerts

alert_headline = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][0]["Headline"]
alert_id = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][0]["AlertId"]
alert_service_id = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][0]["ImpactedService"]["Service"][1]["ServiceId"]
alert_service_name = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][0]["ImpactedService"]["Service"][0]["ServiceName"]
alert_service_stop_type = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][0]["ImpactedService"]["Service"][0]["ServiceTypeDescription"]
st.write(alert_service_stop_type)
alert_severity_score = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][0]["SeverityScore"]
alert_severity_color = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][0]["SeverityColor"]
alert_severity_css = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][0]["SeverityCSS"]
alert_impact = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][0]["Impact"]
alert_severity_event_start = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][0]["EventStart"]
alert_severity_event_end = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][0]["EventEnd"]
alert_tbd = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][0]["TBD"] #Boolean
alert_major_event_end = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][0]["EventEnd"]
alert_url = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][0]["AlertURL"]["#cdata-section"]
alert_vehicle_desc = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][0]["ImpactedService"]["Service"][0]["ServiceTypeDescription"]
#alert_service_name = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][0]["ImpactedService"]["Service"][0]["ServiceName"]
alert_backcolor = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][0]["ImpactedService"]["Service"][0]["ServiceBackColor"]
alert_service_url = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][0]["ImpactedService"]["Service"][0]["ServiceURL"]["#cdata-section"]


# Descriptions Will Come Last
alert_short_description = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][0]["ShortDescription"]
alert_full_description = json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][0]["FullDescription"]["#cdata-section"]


st.header("ServiceID Test 🧠")
#st.write(json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"][0]["ImpactedService"]["Service"][1]["ServiceId"])

st.write(detail_alert, unsafe_allow_html= True)

# Need to Find the Alerts for the route 
# Bus for loop

train_bus_list = train_routes + bus_routes
st.write(all_alerts_length)
st.header("Bus and Trains on Route 🚌🚄")
st.write(train_bus_list)

# SPECIFIC ROUTE 👑==========================================================
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




# ================================================================================
st.header("ALL RESULTS IN JSON")
# Back up of lenghth that makes this code possible
# all_alerts_length = len(json.loads(baseline_alert_prep)["CTAAlerts"]["Alert"])
    
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
            
        
        
        
            
    

    



# TODO 
# Make a unique list of bus numbers seperate list for train numbers in route used 
# Make two sets of unique list for trains and buses affected a long with information will be dictionary set of lists 
# For matches give alerts 

# Seperate section for all alerts



"""
TODO NOTE: 

Things to do next.

1. Make a for in range in loop for the number of steps. Have it write out in a readable format.
2. Number the steps, and an emojji pertaining to the type of route that is being taken. A train emoji for train, bus for bus etc.
3. Record the step number and the longitude at latitude in the dictionary. 
4. Make a color coded map using folium where the icons/color for walking, busing, and taking the train are different. 
5. Make the folium map. May have to use two lists for instructions.
6. Show the static map side by side. 
7. Find a way to utilize the dictionary (or lists if their creation is necessary) to get all of the buses and train routes in the trip. 
8. Use the CTA buses and train APIs to inform users of any delays, utilizing colors for timeliness status.
9. Add lottie file images.
10. Add searchbars to make users be able to enter in the address that they want to see.
11. Add a credit page.

### IMPORTANT NEW NOTE 3/4/24
1. Finish arrival first add headsign, route/line info, vehicle info (bus or train) ✅
2. Replicate over to departure time. ✅
3. Embellish instructions of the steps that involve bus or train. ✅
4. Explore CTA bus and train APIs and documentation. (Postponed)

# IMPORTANT NEW NOTE 3/4/24 -3/7/24 
1. Explore bus/train documentation ✅ \n
1B. Add CTA detail alert API
2. Obtain list of bus/train routes used
3. Check the list of routes impacted by delays 
4. Show affected routes and details about the impact. Also have a section where users can see non-pertinent impacted routes.
5. Work on mapping.
6. Make seperate page for functions to import.
7. Create page for delays and closures CTA wide. Credit page also.

Alert API Documentation
https://www.transitchicago.com/developers/alerts/


"""

"""
Second Page Filter for Alerts
 1-19 Accessibility and informational alerts
This range includes alerts related to accessible paths, as well as special notes about service and
information about added service.
 20-39 Planned/anticipated events affecting bus and train service
This range includes notices about planned work, service changes and reroutes that are
anticipated (parade reroutes, for example) which potentially affect all users of a named service.
 40-59 Minor delays and reroutes affecting bus and train service
This range includes notices about unanticipated minor delays and reroutes that affect all users of
a named service.
 60-79 Significant delays and reroutes affecting bus and train service
This range includes notices about unanticipated significant delays (sporadic or consistent) and
reroutes that affect all users of a named service.
 80-99 Major delays and service disruptions
This range includes alerts about unanticipated major delays and service disruptions where a
service is significantly impacted by an event, and considering service alternatives may be
advisable


type 
Valid values for “type” include:
 bus
 rail
 station
 systemwide
Specify any combination by separating multiple
terms with commas (no spaces). Default is
“bus,rail,systemwide”.

Chicago Data Portal Train
https://data.cityofchicago.org/Transportation/CTA-System-Information-List-of-L-Stops/8pix-ypme/about_data


Chicago Data Portal Bus
https://data.cityofchicago.org/Transportation/CTA-Bus-Stops/hvnx-qtky

"""



# What I tried earlier
# for step in directions_result:
#     st.write(step[0]["html_instructions"])
    

# for i in range (0, len (result['routes'][0]['legs'][0]['steps'])):
#     j = json_result['routes'][0]['legs'][0]['steps'][i]['html_instructions'] 
#     st.write(j)


# chi_map = gmaps.figure(center = chicago_coordinates, zoom_level = 12)

# st.map(chi_map)







