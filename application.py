from flask import Flask, request, Response
import json

application = Flask(__name__)

@application.route("/", methods=["GET"])
def health_check():
    return Response(
        response=json.dumps({'error': 'none', 'data': 'Health check good.'}),
        status=200,
        mimetype='application/json'
    )

if __name__ == "__main__":
    application.run(host='0.0.0.0')