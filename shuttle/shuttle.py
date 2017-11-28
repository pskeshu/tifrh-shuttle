from flask import Flask, render_template
import datetime
import subprocess
import schedule

app = Flask(__name__)


def get_fortune():
    message = subprocess.run("fortune", stdout=subprocess.PIPE).stdout
    return message.decode('utf-8')


def smart_datetime(time_string, tomorrow=False):
    if tomorrow is False:
        day = datetime.date.today()
    else:
        day = datetime.date.today()
        day = day.timedelta(days=1)
    date_string = "{}-{}".format(str(day), time_string)

    td_obj = datetime.datetime.strptime(date_string, "%Y-%m-%d-%H%M")
    remaining_time = (td_obj - datetime.datetime.now()).total_seconds()
    if remaining_time > 0:
        return remaining_time
    else:
        return smart_datetime(time_string, tomorrow=True)


def time_left(schedule_list):
    """Take a list of time. Convert the ones that are tomorrow appropriately.
    """
    dt_objects = [(smart_datetime(_))
                  for _ in schedule_list]
    return dt_objects


def next_shuttle(schedule_dict):
    """Based on the dictionary passed to this function, and the current time,
    this function will return the time remaining for the next shuttle in
    seconds, and the shuttle index from the dictionary."""

    timings = list(schedule_dict.keys())  # Shuttle timings

    # For each shuttle: shuttle time - current time
    # This is a datetime object.
    all_shuttles_datetime = time_left(timings)
    exit()

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

    now = datetime.datetime.now()
    day_of_week = now.weekday()

    if (day_of_week <= 4):
        fretb_indus = schedule.fretb_indus_weekday
        fretb_aparna = schedule.fretb_aparna_weekday
    elif (day_of_week == 5):
        fretb_indus = schedule.fretb_indus_saturday
        fretb_aparna = schedule.fretb_aparna_saturday
    else:
        fretb_indus = schedule.fretb_indus_sunday
        fretb_aparna = schedule.fretb_aparna_sunday

    time_indus, id_indus = next_shuttle(fretb_indus)
    time_aparna, id_aparna = next_shuttle(fretb_aparna)

    minutes_indus = int(time_indus/60)
    minutes_aparna = int(time_aparna/60)

    shuttles_indus = fretb_indus[id_indus]
    shuttles_aparna = fretb_aparna[id_aparna]

    # return render_template("home.html",
    #                       shuttle_time_indus=id_indus,
    #                       time_left_indus=minutes_indus,
    #                       shuttles_indus=shuttles_indus,
    #                       shuttle_time_aparna=id_aparna,
    #                       time_left_aparna=minutes_aparna,
    #                       shuttles_aparna=shuttles_aparna,
    #                       fortune=get_fortune(),
    #                       last_update=schedule.last_update
    #                       )


if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=80)
    main()
