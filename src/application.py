from stravalib import Client
from authentication import *
from sendLINEMessage import *
from flask import Flask, request


app = Flask(__name__)


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
    # Here we send a LINE message with the Strava activity link
    # when a non-indoor activity is created
    if (data["aspect_type"] == "create"):
        client = Client(access_token=get_access_token())
        activity = client.get_activity(data["object_id"])
        if (activity.trainer is True): # indoor activity
            print("Activity " + str(activity.id) + " is an indoor activity, please manually delete it via " +
                  "https://www.strava.com/activities/" + str(activity.id))
            return ("INDOOR_ACTIVITY_CREATED", 200)
        else:
            if sendLINEMessage("https://www.strava.com/activities/" + str(activity.id)):
                print("LINE message sent!")
                return ("ACTIVITY_CREATED", 200)
            else:
                return ("SOMETHING_WAS_WRONG", 404)
    elif (data["aspect_type"] == "update"):
        return ("ACTIVITY_UPDATED", 200)
    elif (data["aspect_type"] == "delete"):
        return ("ACTIVITY_DELETED", 200)


if __name__ == "__main__":
    app.run(debug=True)