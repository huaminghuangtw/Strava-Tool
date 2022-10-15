import requests


def get_Athlete(access_token: str) -> dict:
	try:
		base_url = "https://www.strava.com/api/v3/athlete"
		header = {'Authorization': 'Bearer ' + access_token}
		r = requests.get(base_url, headers=header)
	except requests.exceptions.RequestException:
		return None

	athlete = r.json()

	return athlete


def get_Recent_Ride_Totals(athlete_id: int, access_token: str) -> dict:
	try:
		base_url = "https://www.strava.com/api/v3/athletes/{}/stats".format(athlete_id)
		header = {'Authorization': 'Bearer ' + access_token}
		r = requests.get(base_url, headers=header)
	except requests.exceptions.RequestException:
		return None

	recent_ride_totals = r.json().get('recent_ride_totals')

	return recent_ride_totals


def get_Latest_Activity_Data(access_token: str, numberOfActivities: int = 1) -> list:
    try:
        base_url = "https://www.strava.com/api/v3/athlete/activities"
        header = {'Authorization': 'Bearer ' + access_token}
        param = {
			'per_page': numberOfActivities,
			'page': 1
		}
        r = requests.get(base_url, headers=header, params=param)
    except requests.exceptions.RequestException:
        return None

    my_dataset = r.json()

    return my_dataset


def get_Timeinterval_Activity_Data(access_token: str, before: int, after: int) -> list:
    """
    @params:
        before, after - should be in UNIX time format
    """
    page_id = 1
    per_page = 50

    my_dataset = []

    while True:
        try:
            base_url = "https://www.strava.com/api/v3/athlete/activities"
            header = {'Authorization': 'Bearer ' + access_token}
            param = {
				'before': before,
				'after': after,
				'per_page': per_page,
				'page': page_id
			}
            r = requests.get(base_url, headers=header, params=param)
        except requests.exceptions.RequestException:
            return None
        
        dataset = r.json()

        if not dataset:
            break

        page_id += 1
        my_dataset += dataset

    return my_dataset


def get_All_Activity_Data(access_token: str) -> list:
    page_id = 1
    per_page = 50

    my_dataset = []

    while True:
        try:
            base_url = "https://www.strava.com/api/v3/athlete/activities"
            header = {'Authorization': 'Bearer ' + access_token}
            param = {
				'per_page': per_page,
				'page': page_id
			}
            r = requests.get(base_url, headers=header, params=param)
        except requests.exceptions.RequestException:
            return None
        
        dataset = r.json()

        if not dataset:
            break

        page_id += 1
        my_dataset += dataset

    return my_dataset