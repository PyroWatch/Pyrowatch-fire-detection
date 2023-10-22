from flask import Flask, request, jsonify
from flask_api import status
from sms import SMS

app = Flask(__name__)


app.config["JSONIFY_MIMETYPE"] = "application/json; charset=utf-8"

@app.route('/api/bulk-sms', methods=['POST'])
def send_sms():
    if request.is_json:
        try:
            data = request.json
            apiKey = 'YOUR_AFFRICASTALKING_API_KEY'
            username = 'YOUR_AFFRICASTALKING_USERNAME'
            recipients = ['AUTHORITIES_CONTACT_NUMBERS']
            message = data['message']
            sms = SMS(username, apiKey)
            sms.send(message, recipients)
            return jsonify({"message": "SMS sent successfully"}), status.HTTP_200_OK

        except Exception as e:
            print(e)
            return jsonify({"error": "Invalid JSON"}), status.HTTP_400_BAD_REQUEST
    else:
        return jsonify({"error": "Request body must be JSON"}), status.HTTP_400_BAD_REQUEST
    
if __name__ == '__main__':
    app.run(debug=True)