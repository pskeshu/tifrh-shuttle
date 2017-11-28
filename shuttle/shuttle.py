from flask import Flask, render_template
import datetime
import subprocess
import schedule

app = Flask(__name__)


def get_fortune():
    message = subprocess.run("fortune", stdout=subprocess.PIPE).stdout
    return message.decode('utf-8')


def smart_timeleft(time_string, tomorrow=False):
    """This function takes in a time string, and calculates the time left
    for that time string. If the time encoded in the time string is passed,
    the function will calculate the time left for that with the tomorrow
    argument being true."""
    if tomorrow is False:
        day = datetime.date.today()
    else:
        day = datetime.date.today() + datetime.timedelta(days=1)
    date_string = "{}-{}".format(str(day), time_string)
    td_obj = datetime.datetime.strptime(date_string, "%Y-%m-%d-%H%M")
    remaining_time = (td_obj - datetime.datetime.now()).total_seconds()
    if remaining_time > 0:
        return remaining_time
    else:
        return smart_timeleft(time_string, tomorrow=True)


def next_shuttle(schedule_dict):
    """Based on the dictionary passed to this function,
    this function will return the time remaining for the next shuttle in
    seconds, and the shuttle index from the dictionary."""

    timings = list(schedule_dict.keys())  # Shuttle timings

    # Time left for various shuttles in seconds.
    all_shuttles_seconds = [(smart_timeleft(_)) for _ in timings]

    # Find the next shuttle among all the shuttles.
    remaining_time_seconds = min(_ for _ in all_shuttles_seconds if _ > 0)

    # Index for the shuttle that is next in line.
    idx = all_shuttles_seconds.index(remaining_time_seconds)

    # Shuttle index from the service dictionary
    shuttle = timings[idx]
    return remaining_time_seconds, shuttle


def fetch_shuttle_schedule():
    now = datetime.datetime.now()
    day_of_week = now.weekday()

    if (day_of_week <= 4):
        fretb_indus = schedule.fretb_indus_weekday
        fretb_aparna = schedule.fretb_aparna_weekday
        indus_fretb = schedule.indus_fretb_weekday
        aparna_fretb = schedule.aparna_fretb_weekday
    elif (day_of_week == 5):
        fretb_indus = schedule.fretb_indus_saturday
        fretb_aparna = schedule.fretb_aparna_saturday
        indus_fretb = schedule.indus_fretb_saturday
        aparna_fretb = schedule.aparna_fretb_saturday
    else:
        fretb_indus = schedule.fretb_indus_sunday
        fretb_aparna = schedule.fretb_aparna_sunday
        indus_fretb = schedule.indus_fretb_sunday
        aparna_fretb = schedule.aparna_fretb_sunday

    return fretb_indus, indus_fretb, fretb_aparna, aparna_fretb


@app.route('/')
def main():
    fretb_indus, indus_fretb, fretb_aparna, aparna_fretb = fetch_shuttle_schedule()

    time_indus, id_indus = next_shuttle(fretb_indus)
    time_aparna, id_aparna = next_shuttle(fretb_aparna)

    minutes_indus = int(time_indus/60)
    minutes_aparna = int(time_aparna/60)

    shuttles_indus = fretb_indus[id_indus]
    shuttles_aparna = fretb_aparna[id_aparna]

    return render_template("home.html",
                           shuttle_time_indus=id_indus,
                           time_left_indus=minutes_indus,
                           shuttles_indus=shuttles_indus,
                           shuttle_time_aparna=id_aparna,
                           time_left_aparna=minutes_aparna,
                           shuttles_aparna=shuttles_aparna,
                           fortune=get_fortune(),
                           last_update=schedule.last_update
                           )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
