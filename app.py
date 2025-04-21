from flask import Flask, request, jsonify
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz

app = Flask(__name__)
geolocator = Nominatim(user_agent="timezone_api")
tf = TimezoneFinder()

AUTHORIZED_TOKEN = "secret-token-123"

def safe_geocode(city):
    try:
        return geolocator.geocode(city, timeout=5)
    except GeocoderTimedOut:
        return None

@app.route('/time', methods=['GET'])
def get_time():
    auth_header = request.headers.get('Authorization')
    if not auth_header or auth_header != f"Bearer {AUTHORIZED_TOKEN}":
        return jsonify({"error": "Unauthorized"}), 403

    city = request.args.get('city')
    if not city:
        return jsonify({"error": "Missing 'city' parameter"}), 400

    location = safe_geocode(city)
    if not location:
        return jsonify({"error": f"City '{city}' not found"}), 404

    timezone_str = tf.timezone_at(lat=location.latitude, lng=location.longitude)
    if not timezone_str:
        return jsonify({"error": "Timezone not found"}), 500

    tz = pytz.timezone(timezone_str)
    local_time = datetime.now(tz)
    offset = local_time.utcoffset()

    return jsonify({
        "city": city,
        "local_time": local_time.strftime('%Y-%m-%d %H:%M:%S'),
        "utc_offset": str(offset)
    })

if __name__ == '__main__':
    app.run(port=5050)
