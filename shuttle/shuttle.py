from flask import Flask, render_template
from datetime import datetime
import subprocess

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

app = Flask(__name__)


def get_fortune():
    message = subprocess.run("fortune", stdout=subprocess.PIPE).stdout
    return message.decode('utf-8')


def time_now():
    """Get the current time, and return the hours and minutes in the datetime
    format."""
    right_now = datetime.now()
    hhss = "{}{}".format(right_now.hour, right_now.minute)
    return datetime.strptime(hhss, '%H%M')


def next_shuttle(schedule_dict):
    """Based on the dictionary passed to this function, and the current time,
    this function will return the time remaining for the next shuttle in
    seconds, and the shuttle index from the dictionary."""

    timings = list(schedule_dict.keys())  # Shuttle timings

    # For each shuttle: shuttle time - current time
    # This is a datetime object.
    all_shuttles_datetime = [datetime.strptime(_, '%H%M') - time_now()
                             for _ in timings]

    # For each shuttle: the time left in seconds.
    all_shuttles_seconds = [_.total_seconds() for _ in all_shuttles_datetime]

    # The early morning shuttles that are there for the next day
    # confuses the program, as datatime.strptime by default assumes
    # date as 1990/01/01. The shuttles that are technically tomorrow
    # (midnight onwards) as assumed as shuttles today.
    # Needs a better hack than ignoring negative time.
    remaining_time_seconds = min(_ for _ in all_shuttles_seconds if _ > 0)

    # Index for the shuttle that is next in line.
    idx = all_shuttles_seconds.index(remaining_time_seconds)

    # Shuttle index from the service dictionary
    shuttle = timings[idx]
    return remaining_time_seconds, shuttle


@app.route('/')
def main():
    time_indus, id_indus = next_shuttle(fretb_indus_weekday)

    time_aparna, id_aparna = next_shuttle(fretb_aparna_weekday)

    minutes_indus = int(time_indus/60)
    minutes_aparna = int(time_aparna/60)

    shuttles_indus = fretb_indus_weekday[id_indus]
    shuttles_aparna = fretb_aparna_weekday[id_aparna]

    return render_template("home.html",
                           shuttle_time_indus=id_indus,
                           time_left_indus=minutes_indus,
                           shuttles_indus=shuttles_indus,
                           shuttle_time_aparna=id_aparna,
                           time_left_aparna=minutes_aparna,
                           shuttles_aparna=shuttles_aparna,
                           fortune=get_fortune()
                           )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
