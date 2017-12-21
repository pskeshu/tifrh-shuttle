from flask import Flask, render_template
import datetime
import subprocess
import pytz
from shuttle import schedule

tz = pytz.timezone("Asia/Kolkata")
app = Flask(__name__)
app.jinja_env.filters['zip'] = zip


def get_fortune():
    try:
        message = subprocess.run("fortune", stdout=subprocess.PIPE).stdout
        return message.decode('utf-8')
    except:
        return "The universe is a pretty big place.\
        If it's just us, seems like an awful waste of space. -- Carl Sagan"


def smart_timeleft(time_string, tomorrow=False):
    """This function takes in a time string, and calculates the time left
    for that time string. If the time encoded in the time string is passed,
    the function will calculate the time left for that with the tomorrow
    argument being true."""
    if tomorrow is False:
        day = datetime.datetime.now(tz=tz).date()
    else:
        day = datetime.datetime.now(tz=tz).date()
        day += datetime.timedelta(days=1)
    date_string = "{}-{}-GMT+0530".format(str(day), time_string)
    td_obj = datetime.datetime.strptime(date_string,
                                        "%Y-%m-%d-%H%M-GMT%z")
    remaining_time = (td_obj - datetime.datetime.now(tz)).total_seconds()
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
    now = datetime.datetime.now(tz)
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


@app.route('/next')
def next():
    fretb_indus, indus_fretb, fretb_aparna, aparna_fretb = \
        fetch_shuttle_schedule()

    time_fretb_IC, id_fretb_IC = next_shuttle(fretb_indus)
    time_fretb_AS, id_fretb_AS = next_shuttle(fretb_aparna)
    time_IC_fretb, id_IC_fretb = next_shuttle(indus_fretb)
    time_AS_fretb, id_AS_fretb = next_shuttle(aparna_fretb)

    minutes_fretb_IC = int(time_fretb_IC/60)
    minutes_fretb_AS = int(time_fretb_AS/60)
    minutes_IC_fretb = int(time_IC_fretb/60)
    minutes_AS_fretb = int(time_AS_fretb/60)

    shuttles_fretb_IC = fretb_indus[id_fretb_IC]
    shuttles_fretb_AS = fretb_aparna[id_fretb_AS]
    shuttles_IC_fretb = indus_fretb[id_IC_fretb]
    shuttles_AS_fretb = aparna_fretb[id_AS_fretb]

    fretb_indus_info = {
        "shuttle_time": id_fretb_IC,
        "minutes": minutes_fretb_IC,
        "shuttles": shuttles_fretb_IC
    }

    fretb_aparna_info = {
        "shuttle_time": id_fretb_AS,
        "minutes": minutes_fretb_AS,
        "shuttles": shuttles_fretb_AS
    }

    indus_fretb_info = {
        "shuttle_time": id_IC_fretb,
        "minutes": minutes_IC_fretb,
        "shuttles": shuttles_IC_fretb
    }

    aparna_fretb_info = {
        "shuttle_time": id_AS_fretb,
        "minutes": minutes_AS_fretb,
        "shuttles": shuttles_AS_fretb
    }

    return render_template("home.html",
                           title="TIFR Hyderabad Shuttle Timings",
                           fretb_indus_info=fretb_indus_info,
                           fretb_aparna_info=fretb_aparna_info,
                           indus_fretb_info=indus_fretb_info,
                           aparna_fretb_info=aparna_fretb_info,
                           fortune=get_fortune(),
                           last_update=schedule.last_update
                           )


@app.route('/')
@app.route('/all')
def all_shuttles():
    fretb_indus, indus_fretb, fretb_aparna, aparna_fretb = \
        fetch_shuttle_schedule()

    tl_fretb_indus = [smart_timeleft(_) for _ in fretb_indus]
    tl_indus_fretb = [smart_timeleft(_) for _ in indus_fretb]
    tl_fretb_aparna = [smart_timeleft(_) for _ in fretb_aparna]
    tl_aparna_fretb = [smart_timeleft(_) for _ in aparna_fretb]

    minutes_fretb_IC = [int(_/60) for _ in tl_fretb_indus]
    minutes_fretb_AS = [int(_/60) for _ in tl_fretb_aparna]
    minutes_IC_fretb = [int(_/60) for _ in tl_indus_fretb]
    minutes_AS_fretb = [int(_/60) for _ in tl_aparna_fretb]

    fretb_indus_info = {
        "shuttle_time": fretb_indus,
        "minutes": minutes_fretb_IC,
    }

    fretb_aparna_info = {
        "shuttle_time": fretb_aparna,
        "minutes": minutes_fretb_AS,
    }

    indus_fretb_info = {
        "shuttle_time": indus_fretb,
        "minutes": minutes_IC_fretb,
    }

    aparna_fretb_info = {
        "shuttle_time": aparna_fretb,
        "minutes": minutes_AS_fretb,
    }

    return render_template("all.html",
                           title="All shuttles",
                           fretb_indus_info=fretb_indus_info,
                           fretb_aparna_info=fretb_aparna_info,
                           indus_fretb_info=indus_fretb_info,
                           aparna_fretb_info=aparna_fretb_info,
                           fortune=get_fortune(),
                           last_update=schedule.last_update)


@app.route('/pdf')
def return_pdf():
    return '<embed src="static/20171116.pdf" width="100%" height="100%" />'
