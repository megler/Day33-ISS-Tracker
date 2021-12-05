# ISS Notifier and Mapper

Get an email if the ISS is overhead. Also, track ISS on world map.
Day 33 Python Bootcamp


## Usage

1. Create file named .env and add:
    1. MY_EMAIL = "your_email_address@email.com"
    2. MY_PASSWORD = "your-email-password"
    3. SMTP = 'smtp-for-your-email-provider'

2. The code as written will only check your position relative to the ISS one time.
If you want a continual check, you'll need to add a while loop with a time delay.

## Example

    while True:
        time.sleep(60)
        if check_iss_position and check_sun_position:
            send_mail("The ISS is overhead!")

3. Running the while loop impacts the Flask server. This wasn't really meant to 
map, but I wanted to test Folium. More would need to be added via Flask and JS to
have both the email check and the map work simultaneously. 

4. To start the flask app:

    1. run `python main.py` in your terminal
    2. go to `http://127.0.0.1:5000/` in your browser.

5. You can put additional markers on the map. Line 83 has a marker set for
Orlando, FL, but it can be changed to anything. 
See [Folium](https://python-visualization.github.io/folium/index.html#) docs for customization.




## License
[MIT](https://choosealicense.com/licenses/mit/)