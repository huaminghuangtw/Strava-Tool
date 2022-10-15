import requests
import os
import pandas as pd
from datetime import date, datetime, timedelta
from threading import Timer
from pyngrok import ngrok
from flask import Flask, request

from authentication import *
from sendLINEMessage import *
from strava_data import *
from strava_analysis import *


app = Flask(__name__)
on_heroku = 'DYNO' in os.environ
processed_activities = {}
VERIFY_TOKEN = "STRAVA"


"""
Delete existing webhook subscriptions if any and
create a new one
"""
@app.route('/')
def index():
    def view_subscription():
        try:
            base_url = "https://www.strava.com/api/v3/push_subscriptions"
            params = {
                'client_id': STRAVA_CLIENT_ID,
                'client_secret': STRAVA_CLIENT_SECRET
            }
            r = requests.get(base_url, params=params)
        except requests.exceptions.RequestException:
            return None
        return r.json()
    def delete_subscription(subscription_id):
        try:
            base_url = "https://www.strava.com/api/v3/push_subscriptions/{}".format(subscription_id)
            params = {
                'client_id': STRAVA_CLIENT_ID,
                'client_secret': STRAVA_CLIENT_SECRET
            }
            requests.delete(base_url, params=params)
        except requests.exceptions.RequestException:
            return None
    def create_subscription(callback_url):
        try:
            base_url = "https://www.strava.com/api/v3/push_subscriptions"
            data = {
                'client_id': STRAVA_CLIENT_ID,
                'client_secret': STRAVA_CLIENT_SECRET,
                'callback_url': callback_url,
                'verify_token': VERIFY_TOKEN
            }
            requests.post(base_url, data=data)
        except requests.exceptions.RequestException:
            return None
    
    existing_subscription = view_subscription()
    if existing_subscription:
        existing_subscription_id = existing_subscription[0]["id"]
        delete_subscription(existing_subscription_id)

    if on_heroku:
        heroku_app_url = "https://my-strava-webhook.herokuapp.com"
        create_subscription(heroku_app_url + "/webhook")
    else:
        tunnels = ngrok.connect(5000, bind_tls=True)
        ngrok_url = tunnels.public_url
        create_subscription(ngrok_url + "/webhook")

    return ("SUCCESS", 200)


"""
Validate webhook subscriptions
"""
@app.get('/webhook')
def webhook_get():
    data = request.args
    print(data)
    
    # Parse the query string parameters
    mode = data['hub.mode']
    verify_token = data['hub.verify_token']
    challenge = data['hub.challenge']

    if (mode != 'subscribe') or (verify_token != VERIFY_TOKEN):
        print('WEBHOOK_NOT_VERIFIED')
        return ('INVALID_REQUEST', 401)
    else:
        print('WEBHOOK_VERIFIED')
        return ({'hub.challenge': challenge}, 200)


"""
Receive webhook events
"""
@app.post('/webhook')
def webhook_post():
    def calculate_Ride_Stats(access_token: str) -> str:
        seconds_since_epoch = datetime.now().timestamp()
        start_of_this_week = date.today() - timedelta(days=date.today().weekday())
        start_of_this_week_UNIX = datetime.combine(start_of_this_week, datetime.min.time()).timestamp()
        start_of_the_week_one_month_ago = start_of_this_week_UNIX - (60 * 60 * 24 * 7 * 4)
        
        recent_ride_totals = get_Timeinterval_Activity_Data(access_token, int(seconds_since_epoch), int(start_of_the_week_one_month_ago))
        recent_ride_totals = create_Activity_DataFrame(recent_ride_totals)
        recent_ride_totals['start_date_local'] = pd.to_datetime(recent_ride_totals['start_date_local'])
        recent_ride_totals['start_time'] = recent_ride_totals['start_date_local'].dt.time
        recent_ride_totals['start_date'] = recent_ride_totals['start_date_local'].dt.date
        
        this_week_rides = recent_ride_totals.loc[
                                                (recent_ride_totals['type'] == 'Ride') &
                                                (recent_ride_totals['distance'] > 0) &
                                                (recent_ride_totals['start_date'] >= start_of_this_week)
                                            ]
        this_week_virtualrides = recent_ride_totals.loc[
                                                        (recent_ride_totals['type'] == 'VirtualRide') &
                                                        (recent_ride_totals['start_date'] >= start_of_this_week)
                                                    ]
        
        last_four_weeks_rides = recent_ride_totals.loc[
                                                    (recent_ride_totals['type'] == 'Ride') &
                                                    (recent_ride_totals['distance'] > 0) &
                                                    (recent_ride_totals['start_date'] < start_of_this_week)
                                                ]
        last_four_weeks_virtualrides = recent_ride_totals.loc[
                                                    (recent_ride_totals['type'] == 'VirtualRide') &
                                                    (recent_ride_totals['start_date'] < start_of_this_week)
                                                ]
        
        ride_stats = \
            "📈 This week:\n" + \
            " • Distance = {:.2f} km\n".format((this_week_rides['distance'].sum() + this_week_virtualrides['distance'].sum()) / 1000) + \
            " • Moving time = {}h {}m\n".format((this_week_rides['moving_time'].sum() + this_week_virtualrides['moving_time'].sum()) // 3600,
                                                ((this_week_rides['moving_time'].sum() + this_week_virtualrides['moving_time'].sum()) % 3600) // 60) + \
            " • Elevation gain = {} m".format(round(this_week_rides['total_elevation_gain'].sum() + this_week_virtualrides['total_elevation_gain'].sum())) + \
            "\n\n" + \
            "📈 Last 4 weeks avg:\n" + \
            " • Distance = {:.2f} km\n".format(round((last_four_weeks_rides['distance'].sum() + last_four_weeks_virtualrides['distance'].sum()) / 4) / 1000) + \
            " • Moving time = {}h {}m\n".format(int(((last_four_weeks_rides['moving_time'].sum() + last_four_weeks_virtualrides['moving_time'].sum()) / 4) // 3600),
                                                int((((last_four_weeks_rides['moving_time'].sum() + last_four_weeks_virtualrides['moving_time'].sum()) / 4) % 3600) // 60)) + \
            " • Elevation gain = {} m".format(round((last_four_weeks_rides['total_elevation_gain'].sum() + last_four_weeks_virtualrides['total_elevation_gain'].sum()) / 4))
        
        return ride_stats
    
    print('EVENT_RECEIVED')
    data = request.json
    print(data)
    
    # You can do whatever you want upon receiving a webhook event
    # Here we send LINE messages when a new activity is created
    access_token = get_Access_Token()
    if (data["aspect_type"] == "create"):
        latest_activity = get_Latest_Activity_Data(access_token)[0]
        global processed_activities
        # Only send LINE messages once for a given activity
        if (latest_activity["id"] not in processed_activities):
            strava_activity_url = "https://www.strava.com/activities/" + str(latest_activity["id"])
            if ((latest_activity["type"] == 'Ride') or (latest_activity["type"] == 'VirtualRide')) and \
                (latest_activity["distance"] > 0):
                ride_stats = calculate_Ride_Stats(access_token)
                processed_activities[latest_activity["id"]] = True
                sendLINEMessage(strava_activity_url + "\n\n" + ride_stats)
            else:
                sendLINEMessage(strava_activity_url)
            print("LINE messages sent!")
        else:
            print("No LINE messages sent!")
        return ("ACTIVITY_CREATED", 200)
    elif (data["aspect_type"] == "update"):
        return ("ACTIVITY_UPDATED", 200)
    elif (data["aspect_type"] == "delete"):
        return ("ACTIVITY_DELETED", 200)


"""
Open the web browser silently
"""
def open_browser():
    if on_heroku:
        requests.get("https://my-strava-webhook.herokuapp.com")
    else:
        requests.get("http://127.0.0.1:5000")


if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run(debug=True)