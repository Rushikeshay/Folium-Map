
import pandas as pd
import folium
from geopy.exc import GeocoderTimedOut
import time
from geopy.geocoders import Nominatim

# Define your places (name + description only)
dc_places = [
    {"name": "The Potter's House Cafe & Bookstore", "desc": "Coffee and books"},
    {"name": "Bukom Cafe", "desc": "Good West African live music."},
    {"name": "Tryst", "desc": "Very crowded coffee shop with a chaotic atmosphere."},
    {"name": "The Diner", "desc": "Cheap American diner food."},
    {"name": "Roofers Union", "desc": "Nice chill rooftop."},
    {"name": "Kalorama Park", "desc": "Great for summer picnics."},
    {"name": "The Board Room", "desc": "Spent many evenings playing board games with friends."},
    {"name": "Tatiana Pizza", "desc": "A perfect place to get a large slice of pizza after a night of board games."},
    {"name": "Iron Age - Columbia Heights", "desc": "Unlimited seafood."},
    {"name": "Meridian Hill Park", "desc": "Beautiful park for an evening stroll."},
    {"name": "Makan", "desc": "Great Malaysian food."},
    {"name": "The Coupe", "desc": "Great brunch place."},
    {"name": "Red Derby", "desc": "Lovely rooftop."},
    {"name": "Anafre DC", "desc": "Good place for Mexican seafood."},
    {"name": "King Street Oyster Bar", "desc": "Perfect for happy hour oysters."},
    {"name": "Kelly's Irish Times", "desc": "Go for a Guiness."},
    {"name": "Rock Creek Park", "desc": "Countless weekends spent hiking here."},
    {"name": "The Wharf", "desc": "Go for a walk feel like a tourist."},
    {"name": "Titanic Memorial", "desc": "Part of the Wharf no one usually goes to. But I like it."},
    {"name": "Lincoln Memorial", "desc": "Go behind the memo"},
    {"name": "Spice 6 Modern Indian", "desc": "The best South Indian food in DC."},
    {"name": "King Street", "desc": "Beautiful old town. Great for a walk.", "location": "King Street, Alexandria, VA"}
    ]

# Set up geolocator
geolocator = Nominatim(user_agent="dc_mapper")

# Safe geocoding with retry logic
def safe_geocode(place_name, retries=3):
    for attempt in range(retries):
        try:
            return geolocator.geocode(f"{place_name}, Washington, DC", timeout=10)
        except GeocoderTimedOut:
            print(f"Timeout ({attempt+1}/{retries}) for {place_name}")
            time.sleep(1)
    return None

# Geocode each place
for place in dc_places:
    if place["name"] == "Tatiana Pizza":
        location = safe_geocode("1730 Connecticut Ave NW, Washington, DC 20009")
    elif place["name"] == "The Potter's House Cafe & Bookstore":
        location = safe_geocode("1658 Columbia Rd NW, Washington, DC 20009")
    elif place["name"] == "Spice 6 Modern Indian":
        location = safe_geocode("740 6th St NW, Washington, DC 20001")
    else:
        location = safe_geocode(place["name"])
    
    if location:
        place["latitude"] = location.latitude
        place["longitude"] = location.longitude
    else:
        place["latitude"] = None
        place["longitude"] = None
        print(f"Location not found: {place['name']}")

# Create folium map centered on Adams Morgan
m = folium.Map(location=[38.9212, -77.0421], zoom_start=16, tiles=None)

# Add base layers
folium.TileLayer('OpenStreetMap', name='OpenStreetMap').add_to(m)

# Add markers to map
for place in dc_places:
    if place["latitude"] is not None and place["longitude"] is not None:
        folium.Marker(
            location=[place["latitude"], place["longitude"]],
            popup=f"<strong>{place['name']}</strong><br>{place['desc']}",
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(m)

# Add layer control
folium.LayerControl().add_to(m)

# Save the map
m.save("DC_map.html")
print("Map saved to DC_map.html")

exit()