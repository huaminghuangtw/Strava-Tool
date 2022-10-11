from stravalib import Client
from authentication import *
from sendLINEMessage import *
from flask import Flask, request
from StravaAnalysisTool_Kernel import *


app = Flask(__name__)
processed_activities = {}


# Validate webhook subscriptions
@app.get('/webhook')
def webhook_get():
    data = request.args
    print(data)
    # Your verify token (should be a random string)
    VERIFY_TOKEN = "STRAVA"
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


# Receive webhook events
@app.post('/webhook')
def webhook_post():
    print('EVENT_RECEIVED')
    data = request.json
    print(data)
    # You can do whatever you want upon receving a webhook event
    # Here we send LINE messages when a new activity is created
    if (data["aspect_type"] == "create"):
        access_token = get_Access_Token()
        client = Client(access_token)
        latest_activity = client.get_activity(data["object_id"])
        global processed_activities
        # Only send LINE messages once for a given activity
        if (latest_activity.id not in processed_activities):
            msg = "https://www.strava.com/activities/" + str(latest_activity.id)
            if ((latest_activity.type == 'Ride') or (latest_activity.type == 'VirtualRide')) and \
			   (latest_activity.trainer == False):
                athlete = get_Athlete(access_token)
                recent_ride_totals = get_Recent_Ride_Totals(athlete['id'], access_token)
                msg = msg + "\n\n" + \
                    "📈 Last 4 weeks:\n" + \
                    " • Distance = {:.2f} km\n".format(recent_ride_totals['distance'] / 1000) + \
                    " • Moving time = {}h {}m\n".format(recent_ride_totals['moving_time'] // 3600,
                                                       (recent_ride_totals['moving_time'] % 3600) // 60) + \
                    " • Elevation gain = {} m".format(round(recent_ride_totals['elevation_gain']))
            processed_activities[latest_activity.id] = True
            sendLINEMessage(msg)
            print("LINE messages sent!")
        else:
            print("No LINE messages sent!")
        return ("ACTIVITY_CREATED", 200)
    elif (data["aspect_type"] == "update"):
        return ("ACTIVITY_UPDATED", 200)
    elif (data["aspect_type"] == "delete"):
        return ("ACTIVITY_DELETED", 200)


if __name__ == "__main__":
    app.run(debug=True)