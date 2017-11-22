from flask import Flask
from datetime import datetime

# Vehicles
car_1 = ["Car - 1", 4, "Anji Babu"]
car_2 = ["Car - 2", 4, "Mumtaz"]
car_3 = ["Car - 3", 4, "Bikshapathi"]
car_4 = ["Car - 4", 4, "Laxman"]
winger_1 = ["Winger - 1", 12, "Pandey"]
winger_2 = ["Winger - 2", 12, "Khaja"]
bus = ["Bus", 22, "Bus Driver"]
bus_rd = ["Bus (via Ratnadeep)", 22, "Bus Driver"]


# Timings
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


app = Flask(__name__)


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

    # Shuttle index from the dictionary
    shuttle = timings[idx]
    return remaining_time_seconds, shuttle


def add_template(vehicle_ID, capacity, driver):
    """HTML string that creates a table with vehicle ID, capacity of the
    vehicle and the name of the driver."""
    template = """
    <tr>
    <td>{}</td>
    <td>{}</td>  
    <td>{}</td>    
    </tr>
    """
    return template.format(vehicle_ID, capacity, driver)


@app.route('/')
def main():
    remaining_time_seconds, shuttle_ID = next_shuttle(fretb_indus_weekday)

    minutes = int(remaining_time_seconds/60)

    shuttles = fretb_indus_weekday[shuttle_ID]

    s = """
        <!DOCTYPE html>
        <html>
        <head>
        <style>
        table, th, td {
            border: 1px solid black;
        }
        </style>
        </head>
        <body>
        """

    s += """<table>
            <caption>The next shuttle to Indus Crest is at 
            <b>{}</b> h in <b>{}</b> minutes.
            </caption>""".format(shuttle_ID, minutes)
    s += """
            <tr>
            <th>Vehicle ID</th>
            <th>Capacity</th>  
            <th>Driver</th>    
            </tr>
        """

    for shuttle in shuttles:
        s += add_template(*shuttle)

    return s + "</table></body></html>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
