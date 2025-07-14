from flask import Flask, request, jsonify, render_template
import psycopg2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify_code():
    code = request.form.get('code')
    # database code here
    return jsonify(...)
