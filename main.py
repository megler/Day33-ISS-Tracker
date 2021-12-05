# issTracker.py
#
# Python Bootcamp Day 33 - ISS Tracker
# Usage:
#      Get an email if the ISS is overhead. Also, track ISS on world map.
#
# Marceia Egler December 5, 2021


import requests, os, time, folium, smtplib
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask


MY_LAT = 28.538336  # Your latitude
MY_LONG = -81.379234  # Your longitude


def send_mail(message):
    MY_EMAIL = os.getenv("MY_EMAIL")
    MY_PASSWORD = os.getenv("MY_PASSWORD")
    SMTP = os.getenv("SMTP")
    with smtplib.SMTP(SMTP, 587) as connection:
        connection.set_debuglevel(1)
        connection.ehlo()
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs="example.email.com",  # CHANGE TO EMAIL YOU WANT TO SEND TO
            msg=f"From: {MY_EMAIL}\nSubject: The ISS Is Overhead\n\n{message}",
        )


def check_iss_position():

    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if (
        MY_LAT - 5 <= iss_latitude <= MY_LAT + 5
        and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5
    ):

        return True


def check_sun_position():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get(
        "https://api.sunrise-sunset.org/json", params=parameters
    )
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now()

    if time_now >= sunset and time_now <= sunrise:
        return True


app = Flask(__name__)


@app.route("/")
def index():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    start_coords = (iss_latitude, iss_longitude)
    folium_map = folium.Map(location=start_coords, zoom_start=2)
    color = folium.Icon(color="red")
    folium.Marker(
        [iss_latitude, iss_longitude],
        popup=(iss_latitude, iss_longitude),
        icon=color,
    ).add_to(folium_map)
    folium.Marker([MY_LAT, MY_LONG]).add_to(folium_map)
    return folium_map._repr_html_()


if __name__ == "__main__":
    app.run(debug=True)

    if check_iss_position and check_sun_position:
        send_mail("The ISS is overhead!")
