
# The schedule is from
last_update = "16 November 2017"

# Vehicles
# Data structure for a vehicle is
# [vehicle_name, capacity, driver_name]

car_1 = ["Car - 1", 4, "Anji Babu"]
car_2 = ["Car - 2", 4, "Mumtaz"]
car_3 = ["Car - 3", 4, "Bikshapathi"]
car_4 = ["Car - 4", 4, "Laxman"]
winger_1 = ["Winger - 1", 12, "Pandey"]
winger_2 = ["Winger - 2", 12, "Khaja"]
bus = ["Bus", 22, "Bus Driver"]
bus_rd = ["Bus (via Ratnadeep)", 22, "Bus Driver"]


# Services
# The data structure for the service is
# {
#   "HHSS" : [vehicle1],
#   "hhss" : [vehicle1, vehicle2]
# }

indus_fretb_weekday = {
    "0745": [car_4],
    "0800": [bus, winger_1],
    "0845": [bus, winger_1],
    "0930": [bus],
    "1100": [winger_2],
}

fretb_indus_weekday = {
    "1830": [bus_rd],
    "2000": [bus],
    "2100": [bus, winger_1],
    "2200": [winger_2],
    "2300": [car_4],
    "0000": [car_4],
    "0100": [car_4],
    "0200": [car_4]
}

indus_fretb_sunday = {
    "0840": [bus, car_1],
    "0930": [bus, winger_1],
    "1045": [bus, winger_1],
    "1215": [bus, winger_1]
}

fretb_indus_sunday = {
    "1400": [bus, winger_1],
    "1500": [bus, winger_1],
    "1600": [bus, winger_1],
    "1800": [bus, winger_1]
}

indus_fretb_saturday = {
    "0745": [car_4],
    "0800": [bus, winger_1],
    "0845": [bus, winger_1],
    "0930": [bus],
    "1100": [winger_2]
}

fretb_indus_saturday = {
    "1830": [bus_rd],
    "2000": [bus],
    "2100": [bus, winger_1],
    "2200": [winger_2],
    "2300": [car_4],
    "0000": [car_4],
    "0100": [car_4],
    "0200": [car_4]
}

aparna_fretb_weekday = {
    "0700": [car_4],
    "0740": [car_1],
    "0800": [car_3],
    "0820": [car_2],
    "0840": [winger_2]
}

fretb_aparna_weekday = {
    "1730": [car_1, car_2],
    "1815": [winger_1],
    "1900": [winger_2],
    "1915": [car_2],
    "1940": [car_1],
    "2000": [car_3]
}

aparna_fretb_saturday = {
    "0700": [car_4],
    "0740": [car_2],
    "0800": [car_3],
    "0840": [winger_2]
}

fretb_aparna_saturday = {
    "1730": [car_2],
    "1815": [winger_2],
    "1900": [winger_2],
    "1930": [car_2],
    "2000": [car_3]
}

aparna_fretb_sunday = {
    "0740": [car_4],
    "0800": [car_1],
    "0840": [winger_2]
}

fretb_aparna_sunday = {
    "1730": [car_1],
    "1815": [car_1],
    "1900": [car_1],
    "1940": [car_1],
}

