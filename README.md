# About CTA API Project 
### Note to developers at the bottom

The project allows users to enter a start and end address 

With the address a route and map will be generated

The program will also check for delays on your route 

You have the option to see all alerts for CTA buses and trains


# How to Use 
Make sure that the addresses that you use are in the city limits of Chicago

You can use google maps to copy and paste properly formatted addresses, examples include:

2650a W Bradley Pl, Chicago, IL 60618

1060 W Addison St, Chicago, IL 60613

# Note to Developers 

### Need to have a Google Maps API key to work on this. The API Key will allow you to work with the Python Package GMaps 

GMaps Routes Documentation 
https://github.com/googlemaps/google-maps-services-python

GMaps Direction Documentation
https://developers.google.com/maps/documentation/directions/get-directions#alternatives


GMap Developers explain how to get a paid google maps api key. The first link will walk you through the process.


# You Need CTA APIs and Keys 
For the ones you need to request, I recommend that you use a business email and that you give a good reason you need access. 

CTA Alerts - No key required
https://www.transitchicago.com/developers/alerts/

CTA Bus Tracker API - Need to Request a key
https://www.transitchicago.com/developers/bustracker/ 

CTA Train Tracker API - Need to Request a Key 
https://www.transitchicago.com/developers/traintrackerapply/

You will need to set up your config.py and .gitignore to prevent your keys from getting leaked.


# How The Project is Structured VERY IMPORTANT 
All of the functionality is on the home.py file. 

I used the main.py file for testing. However that page is a great resource for exploring JSONs and other data.

The code should work out of the box after you setup your config and .gitignore with your access keys.

The my_functions page was where some of the main.py code was cut down to be more manageable. Originally it was going to be used to import the functions into home.py but that proved to be too much of a hassle. 

You may find that some of the distances and duration is replaced with an orange placeholder text. See code below. 

        try:
                step_instruction_detail_distance = json.loads(directions_json)[0]["legs"][0]["steps"][0]["steps"][num]["distance"]["text"]
            except:
                step_instruction_detail_distance = ":orange[(distance not specified)]."
    
    try:
        step_instruction_detail_duration = json.loads(directions_json)[0]["legs"][0]["steps"][0]["steps"][num]["duration"]["text"]
    except:
        step_instruction_detail_duration = ":orange[(estimate not available)]."


You may be able to find a way to make the actual duration and distance show up for every route.


Credits 
Project credits in the about page
Project concept created by an intern

More features may be added by the intern in separate repository. 
