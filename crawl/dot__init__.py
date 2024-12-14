import os
from dotenv import load_dotenv, dotenv_values 

from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons

load_dotenv() 
 
# accessing and printing value
api_key = os.getenv("G_MAPS_API")
map_id = os.getenv("MAP_ID")
print(map_id)

app = Flask(__name__, template_folder="templates")

# you can set key as config
app.config['GOOGLEMAPS_KEY'] = api_key
# Initialize the extension
GoogleMaps(app)

@app.route("/")
def map_created_in_view():

    # gmap = Map(
    #     identifier="gmap",
    #     varname="gmap",
    #     lat=37.4419,
    #     lng=-122.1419,
    #     markers={
    #         icons.dots.green: [(37.4419, -122.1419), (37.4500, -122.1350)],
    #         icons.dots.blue: [(37.4300, -122.1400, "Hello World")],
    #     },
    #     style="height:400px;width:600px;margin:0;",
    # )

    gmap = Map(
        identifier="gmap",
        varname="gmap",
        lat=37.4419,
        lng=-122.1419,
        markers={
            icons.dots.green: [(37.4419, -122.1419), (37.4500, -122.1350)],
            icons.dots.blue: [(37.4300, -122.1400, "Hello World")],
        },
        style="height:400px;width:600px;margin:0;"
    )

    

    return render_template("index.html", gmap=gmap)


@app.route("/1")
def map_created_in_view_1():

    # gmap = Map(
    #     identifier="gmap",
    #     varname="gmap",
    #     lat=37.4419,
    #     lng=-122.1419,
    #     markers={
    #         icons.dots.green: [(37.4419, -122.1419), (37.4500, -122.1350)],
    #         icons.dots.blue: [(37.4300, -122.1400, "Hello World")],
    #     },
    #     style="height:400px;width:600px;margin:0;",
    # )

    gmap = Map(
        identifier="gmap",
        varname="gmap",
        lat=37.4419,
        lng=-122.1419,
        markers={
            icons.dots.green: [(37.4419, -122.1419), (37.4500, -122.1350)],
            icons.dots.blue: [(37.4300, -122.1400, "Hello World")],
        },
        style="height:400px;width:600px;margin:0;",
        map_ids=[map_id]
    )
    print(gmap.map_ids)

    sndmap = Map(
        identifier="sndmap",
        varname="sndmap",
        lat=37.4419,
        lng=-122.1419,
        markers={
            icons.dots.green: [(37.4419, -122.1419), (37.4500, -122.1350)],
            icons.dots.blue: [(37.4300, -122.1400, "Hello World")],
        },
    )

    trdmap = Map(
        identifier="trdmap",
        varname="trdmap",
        lat=37.4419,
        lng=-122.1419,
        markers=[
            {
                "icon": icons.alpha.B,
                "lat": 37.4419,
                "lng": -122.1419,
                "infobox": "Hello I am <b style='color:green;'>GREEN</b>!",
            },
            {
                "icon": icons.dots.blue,
                "lat": 37.4300,
                "lng": -122.1400,
                "infobox": "Hello I am <b style='color:blue;'>BLUE</b>!",
            },
            {
                "icon": "//maps.google.com/mapfiles/ms/icons/yellow-dot.png",
                "lat": 37.4500,
                "lng": -122.1350,
                "infobox": (
                    "Hello I am <b style='color:#ffcc00;'>YELLOW</b>!"
                    "<h2>It is HTML title</h2>"
                    "<img src='//placehold.it/50'>"
                    "<br>Images allowed!"
                ),
            },
        ],
    )

    mymap = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)]
    )
    

    return render_template("example.html", 
        mymap=mymap,
        gmap=gmap,
        sndmap=sndmap,
        trdmap=trdmap
    )


##if __name__ == "__main__":
##    app.run(port=5000, debug=True)
