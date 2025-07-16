from flask import Flask, request, jsonify, render_template, redirect, url_for
import psycopg2
import os

app = Flask(__name__)

# Get database connection string from environment variable
DATABASE_URL = os.environ.get('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)

# HOME PAGE
@app.route('/')
def index():
    cur = conn.cursor()
    cur.execute('SELECT "Code", "Name" FROM treatment_code ORDER BY "Code" ASC')
    codes = cur.fetchall()
    cur.close()
    return render_template('index.html', codes=codes)

# VERIFY CODE
@app.route('/verify', methods=['POST'])
def verify_code():
    try:
        code = int(request.form.get('code', '').strip())
    except ValueError:
        return jsonify({"status": "invalid", "description": "Invalid code format"})

    cur = conn.cursor()
    cur.execute('SELECT "Name" FROM treatment_code WHERE "Code" = %s', (code,))
    result = cur.fetchone()
    cur.close()

    if result:
        return jsonify({"status": "valid", "description": result[0]})
    else:
        return jsonify({"status": "invalid", "description": "Code not found"})

# SEARCH
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('term', '')
    cur = conn.cursor()
    cur.execute('SELECT "Code", "Name" FROM treatment_code WHERE CAST("Code" AS TEXT) LIKE %s LIMIT 10', (f'{query}%',))
    results = cur.fetchall()
    cur.close()
    return jsonify([{"code": row[0], "name": row[1]} for row in results])

# ADD TREATMENT
@app.route('/add', methods=['GET', 'POST'])
def add_treatment():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        code = request.form.get('code', '').strip()
        if not name or not code.isdigit():
            return "Invalid input", 400
        cur = conn.cursor()
        cur.execute('INSERT INTO treatment_code ("Name", "Code") VALUES (%s, %s)', (name, int(code)))
        conn.commit()
        cur.close()
        return redirect(url_for('index'))
    return render_template('add.html')

# RUN SERVER
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
