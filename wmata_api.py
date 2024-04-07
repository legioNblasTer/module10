import json
import requests
from flask import Flask

# API endpoint URL's and access keys
WMATA_API_KEY = "4ed30bb7d68e4ffbb4e7ea7d177e92e7"
INCIDENTS_URL = "https://api.wmata.com/Incidents.svc/json/ElevatorIncidents"
headers = {"api_key": WMATA_API_KEY, 'Accept': '*/*'}

################################################################################

app = Flask(__name__)


# get incidents by machine type (elevators/escalators)
# field is called "unit_type" in WMATA API response
@app.route("/incidents/<unit_type>", methods=["GET"])
def get_incidents(unit_type):
    # create an empty list called 'incidents'
    incidents = []

    # use 'requests' to do a GET request to the WMATA Incidents API
    resp_inc = requests.get(INCIDENTS_URL, headers=headers)

    # retrieve the JSON from the response
    json_resp_inc = resp_inc.json()

    # iterate through the JSON response and retrieve all incidents matching 'unit_type'
    elev_inc = json_resp_inc["ElevatorIncidents"]

    # for each incident, create a dictionary containing the 4 fields from the Module 7 API definition
    num_elev = len(json_resp_inc["ElevatorIncidents"])

    if unit_type == "escalators":
        UNIT_TYPE_ = "ESCALATOR"
    else:
        UNIT_TYPE_ = "ELEVATOR"


    #   -StationCode, StationName, UnitType, UnitName
    # add each incident dictionary object to the 'incidents' list
    for i in range(num_elev):
        if elev_inc[i]['UnitType'] == UNIT_TYPE_:
            inc_dict = {'StationCode': elev_inc[i]['StationCode'], 'StationName': elev_inc[i]['StationName'],
                        'UnitName': elev_inc[i]['UnitName'], 'UnitType': elev_inc[i]['UnitType']}
            incidents.append(inc_dict)

    # return the list of incident dictionaries using json.dumps()
    return json.dumps(incidents)


if __name__ == '__main__':
    app.run(debug=True)
