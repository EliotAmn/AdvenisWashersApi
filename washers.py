from flask import Flask, request, jsonify
import requests
import pytz
from datetime import datetime, timezone
app = Flask(__name__)

@app.route('/laverie-api', methods=["GET"])
def laverie_api():
    data = {}
    result = requests.post("https://status.wi-line.fr/update_machine_ext.php", data={
        "action": "READ_LIST_STATUS",
        "serial_centrale": "0d2dd57f11646817de62376e18816e88"
    }).json()

    paris_timezone = pytz.timezone("Europe/Paris")

    for machine in result["machine_info_status"]['machine_list']:
        id = machine['selecteur_machine']
        name = machine['nom_type']
        status = {
            0: "ERROR",
            1: "FREE",
            2: "BUSY",
            3: "HS",
            11: "BUSY"
        }[machine['status']]

        date_string = machine['date_virtu_off']['date']
        input_datetime = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S.%f")
        paris_timezone = pytz.timezone("Europe/Paris")
        paris_datetime = input_datetime.replace(tzinfo=pytz.UTC).astimezone(paris_timezone)
        date_str = paris_datetime.strftime("%Y-%m-%d %H:%M:%S")
        date_timestamp = paris_datetime.timestamp()

        data[int(id)] = {
            "name": name,
            "id": str(id),
            "status": status,
            "last_start_str": date_str,
            "last_start_timestamp": round(date_timestamp)
        }
    return data, 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=10005)
