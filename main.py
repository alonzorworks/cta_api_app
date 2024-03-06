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
import json
from config import google_map_key

# Now Timestamp 
now = dt.datetime.now()

# Lat is North and South. Long is east and west. Latitude comes first.
chicago_coordinates = (41.87, 87.62)


gmaps = googlemaps.Client(key= google_map_key)

# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

st.title("CTA Project 🚄🚆🚌🚇🚍")

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

st.write(json.loads(directions_json))

# Need Steps 
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
    step_instruction_detail = json.loads(directions_json)[0]["legs"][0]["steps"][0]["steps"][num]["html_instructions"]
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
    
    # Tells if the person is walking, taking the bus, or subway
    travel_mode = json.loads(directions_json)[0]["legs"][0]["steps"][num]["travel_mode"]
    
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

# IMPORTANT NEW NOTE 3/4/24
1. Explore bus/train documentation 
2. Obtain list of bus/train routes used
3. Check the list of routes impacted by delays 
4. Show affected routes and details about the impact. Also have a section where users can see non-pertinent impacted routes.
5. Work on mapping.
"""





# What I tried earlier
# for step in directions_result:
#     st.write(step[0]["html_instructions"])
    

# for i in range (0, len (result['routes'][0]['legs'][0]['steps'])):
#     j = json_result['routes'][0]['legs'][0]['steps'][i]['html_instructions'] 
#     st.write(j)


# chi_map = gmaps.figure(center = chicago_coordinates, zoom_level = 12)

# st.map(chi_map)







