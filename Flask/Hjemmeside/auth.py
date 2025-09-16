import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import base64   
from io import BytesIO
from dotenv import load_dotenv
from cryptography.fernet import Fernet
import os
from datetime import datetime

auth = Blueprint('auth', __name__)
DB_PATH = 'Hjemmeside/Database/credentials.db'

AUTHORIZED_COMPANIES = {
    "KEA",
    "Frederiksberg Kommune",
    "Gooner Games Inc",
}
load_dotenv() 
key = os.getenv("FERNET_KEY")
fernet = Fernet(key)

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def clear_database():
    db = get_db()
    db.execute("DELETE FROM GAME_DATA")
    db.execute("DELETE FROM CREDENTIALS")
    db.commit()
    db.close()


def get_statistik():
    db = get_db()
    company = session.get('user_company')
    if company:
        data = db.execute(
            '''
            SELECT g.*
              FROM GAME_DATA g
              JOIN CREDENTIALS c ON g.USERNAME = c.USERNAME
             WHERE c.COMPANY = ?
            ''',
            (company,)
        ).fetchall()
    else:
        data = db.execute("SELECT * FROM GAME_DATA").fetchall()
    db.close()
    return data

def samlet_statistik():
    rows = get_statistik()  
    users_completed = 0
    print(rows)
    
    users   = [r["USERNAME"] for r in rows]
    lvl1    = [r["LEVEL1"]   for r in rows]
    lvl2    = [r["LEVEL2"]   for r in rows]
    lvl3    = [r["LEVEL3"]   for r in rows]
    lvl4    = [r["LEVEL4"]   for r in rows]
   
    for r in rows:
        if sum([r["LEVEL1"], r["LEVEL2"], r["LEVEL3"], r["LEVEL4"]]) == 4:
            users_completed +=1

    total_possible = len(rows) 
    total_not_done = total_possible - users_completed

    fig = Figure()
    ax  = fig.subplots()
    fig.subplots_adjust(bottom=0.3)
  
    labels = 'Gennemført', 'Ikke gennemført'
    sizes = [users_completed, total_not_done]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%')
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def bruger_statistik():
    company = session.get('user_company')
    sql = '''
    SELECT game_data.username, credentials.FIRSTNAME, credentials.LASTNAME,
           LEVEL1, LEVEL2, LEVEL3, LEVEL4, ACTIVITY
    FROM game_data
    JOIN credentials ON game_data.username = credentials.username
    WHERE credentials.COMPANY = ?;
    '''
    db = get_db()
    rows = db.execute(sql, (company,)).fetchall()
    db.close()
    user_stats = []
    for row in rows:
        decrypted_firstname = fernet.decrypt(row["FIRSTNAME"]).decode()
        decrypted_lastname = fernet.decrypt(row["LASTNAME"]).decode()
        levels_completed = sum([row["LEVEL1"], row["LEVEL2"], row["LEVEL3"], row["LEVEL4"]])
        user_stats.append({
            "firstname": decrypted_firstname,
            "lastname": decrypted_lastname,
            "levels_completed": levels_completed,
            "percentage": int(levels_completed / 4 * 100),
            "activity": row["ACTIVITY"]
        })
    return user_stats 

def navn_join():
    query = """
    SELECT game_data.username, credentials.FIRSTNAME, credentials.LASTNAME, credentials.COMPANY
    FROM game_data
    JOIN credentials ON game_data.username = credentials.username;
    """
    db = get_db()
    data = db.execute(query).fetchall()
    db.close()
    return data
    
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        company = request.form.get('company', "").strip()
        username = request.form['username'].strip()
        password = request.form['password']

        if company not in AUTHORIZED_COMPANIES:
            flash('Sorry, "%s" is not authorized to register for our services.' % company)
            return redirect(url_for('auth.register'))

        db = get_db()

        if db.execute(
            "SELECT 1 FROM CREDENTIALS WHERE USERNAME = ?",
            (username,)
        ).fetchone():
            flash(f"Username '{username}' is already taken.")
            db.close()
            return redirect(url_for('auth.register'))

        encoded_email = email.encode()
        encoded_fornavn = firstname.encode()
        encoded_efternavn = lastname.encode()

        encrypted_fornavn = fernet.encrypt(encoded_fornavn)
        encrypted_efternavn = fernet.encrypt(encoded_efternavn)
        encrypted_email = fernet.encrypt(encoded_email)
    
        hashed_password = generate_password_hash(password)
    
        try:
            db.execute(
                'INSERT INTO CREDENTIALS '
                '(EMAIL, FIRSTNAME, LASTNAME, COMPANY, USERNAME, PASSWORD)'
                'VALUES (?, ?, ?, ?, ?, ?)',
                (encrypted_email, encrypted_fornavn, encrypted_efternavn, company, username, hashed_password)
            )
            db.commit()
        except sqlite3.IntegrityError:
            db.rollback()
            flash('That email is already registered.')
            return redirect(url_for('auth.register'))
        
        finally:
            db.close()
    
    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        pw = request.form['password']
        db = get_db()
        user = db.execute(
            "SELECT EMAIL, PASSWORD, COMPANY, ADMIN FROM CREDENTIALS WHERE USERNAME = ?",
            (username,)
        ).fetchone()
        db.close()
        session_company = user['COMPANY']
        session_admin = user['ADMIN']
        if user and check_password_hash(user['PASSWORD'], pw):
            session['user_email'] = user['EMAIL']
            session['user_company'] = user['COMPANY'] 
            session['user_admin'] = user['ADMIN'] # store company in session
            return redirect(url_for('routes.home'))
        
        flash('Invalid email, firstname or password.')
    
    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.pop('user_email', None)
    session.pop('user_company', None)
    return redirect(url_for('routes.home'))

@auth.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"status": "error", "message": "Invalid request."}), 400
    username = data['username'].strip()
    pw = data['password']
    

    db = get_db()
    user = db.execute(
        "SELECT USERNAME, PASSWORD FROM CREDENTIALS WHERE USERNAME = ?",
        (username,)
    ).fetchone()
    db.close()
    

    
    if user and check_password_hash(user['PASSWORD'], pw): 
        return jsonify({"status": "success", "username": user['USERNAME']})
      
    return jsonify({"status": "error", "message": "Invalid username or password."}), 401

@auth.route('/api/submit', methods=['POST'])
def receive_data():
    data = request.get_json()
    activity = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    username = data.get('username')
    level1 = data.get('level_1')
    level2 = data.get('level_2')
    level3 = data.get('level_3')
    level4 = data.get('level_4')
    db = get_db()
    user = db.execute("""INSERT OR REPLACE INTO GAME_DATA (USERNAME, LEVEL1, LEVEL2, LEVEL3, LEVEL4, ACTIVITY) VALUES (?, ?, ?, ?, ?, ?)""",
        (username, level1, level2, level3, level4, activity)
    )
    db.commit()
    db.close()
    return jsonify({"status": "success", "message": "Data received successfully."}), 200

@auth.route('/api/get_data', methods=['GET'])
def send_data():
    username = request.args.get('username')
    db = get_db()
    data = db.execute("SELECT LEVEL1, LEVEL2, LEVEL3, LEVEL4 FROM GAME_DATA WHERE USERNAME = ?", (username,)).fetchone()
    db.close()
    if data:
        return jsonify(
            {
                "level_1": data['LEVEL1'],
                "level_2": data['LEVEL2'],
                "level_3": data['LEVEL3'],
                "level_4": data['LEVEL4'],
                "status": "success"
            }
        )
    else:
        return jsonify({"status": "error", "message": "No data found."}), 404

@auth.route('/download')
def download():
    return render_template('download.html')

@auth.route('/about_us')
def about_us():
    return render_template('about_us.html')

@auth.route('/dashboard')
def dashboard():
    if session['user_admin'] == 0:
        flash('')
        return redirect(url_for('routes.home'))
        
    plot_png = samlet_statistik()
    user_stats = bruger_statistik()
    all_users = alle_brugere()
    
    return render_template('dashboard.html', plot_png=plot_png, user_stats=user_stats, all_users=all_users)

def alle_brugere():
    rows = get_statistik()
    return len(rows)