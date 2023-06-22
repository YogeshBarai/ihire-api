from flask import Flask, jsonify, render_template
from services.init_db.initiate_db import db_blueprint
import socket
from dotenv import load_dotenv
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
env = os.path.join(basedir,'.env')
load_dotenv(env)
print(os.environ.get('DATABASE_URI'))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')

# Initialize the database blueprint
app.register_blueprint(db_blueprint)

# Register additional blueprints

# This function get the hostname and IP deatils of server, required for microservices
def fetchDetails():
	hostname = socket.gethostname()
	host_ip = socket.gethostbyname(hostname)
	return str(hostname) , str(host_ip)

# Health endpoint
@app.route('/api/health', methods=['GET'])
def health():
    return 'OK'

# API status endpoint
@app.route('/api/status', methods=['GET'])
def api_status():
    return jsonify({
        'status': 'OK',
        'message': 'API is running'
    })

# Endpoint for dynamic page 
@app.route("/api/details")
def details():
	hostname, ip = fetchDetails()
	return render_template('home.html', HOSTNAME=hostname, IP=ip)

if __name__ == '__main__':
    app.run(debug=True)
