import googlemaps
from datetime import datetime
import os
from dotenv import load_dotenv, dotenv_values 
load_dotenv() 
 
# accessing and printing value
api_key = os.getenv("G_MAPS_API")
# print(api_key)

language = 'en-UA'
gmaps = googlemaps.Client(key=api_key)

# Geocoding an address
# geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

# # Look up an address with reverse geocoding
# reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# # Request directions via public transit
# now = datetime.now()
# directions_result = gmaps.directions("Sydney Town Hall",
#                                      "Parramatta, NSW",
#                                      mode="transit",
#                                      departure_time=now)

# # Validate an address with address validation
# addressvalidation_result =  gmaps.addressvalidation(['1600 Amphitheatre Pk'], 
#                                                     regionCode='US',
#                                                     locality='Mountain View', 
#                                                     enableUspsCass=True)

# # Get an Address Descriptor of a location in the reverse geocoding response
# # address_descriptor_result = gmaps.reverse_geocode((40.714224, -73.961452), enable_address_descriptor=True)
# address_descriptor_result = gmaps.reverse_geocode((40.714224, -73.961452))


# print(geocode_result, '\n\n', reverse_geocode_result, '\n\n', address_descriptor_result)
places = gmaps.places(
            "Кошик",
            location=(50.90, 34.79),
            radius=20,
            region='EU',
            language=language,
            open_now=False
        )
print(
    len(places['results'])

)
for i,it in enumerate(places["results"]):
    print(i, it['formatted_address'], it["place_id"], it)
    print(gmaps.place(
            it["place_id"],
            fields=["name", "formatted_address", "business_status", "geometry/location",
                    "place_id", "reviews", "type"],
            language=language,
            # reviews_no_translations=True,
            reviews_sort="newest",
        ))

# i = 0
# while i < 50:
#     print(i, 
#         gmaps.find_place(
#                 "Кошик",
#                 "textquery",
#                 fields=["name", "business_status", "geometry/location", "place_id", "formatted_address"],
#                 # location_bias="point:50.54,34.47",
#                 location_bias=f"circle:{i}@50.54,34.47",
#                 language="en-UA"
#             )

#     )
#     i +=1