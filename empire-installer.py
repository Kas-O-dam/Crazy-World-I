import json
from PIL import Image

countries = list()
scenario = "1914/"
JSON_end = dict()

def rgb_to_hex(rgb:tuple):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

# parsing json
with open("scenario/" + scenario + "country-set.json") as country_set:
    country_set = json.load(country_set)
    for country in country_set:
        countries.append(country["name"])

# parsing png to python dict
for country_name in countries:
    with Image.open( "scenario/" + scenario + "empires-png/{}.png".format(country_name)) as empire_png:
        magenta_region = list()
        empire_png.mode = "RGBA"
        loaded_empire = empire_png.load()
        for x in range(empire_png.width):
            for y in range(empire_png.height):
                if rgb_to_hex(loaded_empire[x, y]) == "#ff00ff":
                    magenta_region.append((x, y))
        JSON_end[country_name] = magenta_region

# saving as json
with open("scenario/" + scenario + "empires.json", "w") as empires_json:
    json.dump(JSON_end, empires_json, ensure_ascii="utf-8")

