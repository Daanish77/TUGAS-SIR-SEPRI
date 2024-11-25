from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'saya_suka_nigga' 

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',  
        password='',  
        database='bakso_app'  
    )
    return connection

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        
        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            error = "Login gagal. Silakan cek username atau password."
            return render_template('login.html', error=error)
    
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        pembuat_bakso = request.form['pembuat_bakso']
        tahun_diciptakan = request.form['tahun_diciptakan']
        ket = request.form['ket']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO bakso (nama, harga, deskripsi) VALUES (%s, %s, %s)", (pembuat_bakso, tahun_diciptakan, ket))
        conn.commit()
        success_message = "Data berhasil disimpan."
        return render_template('dashboard.html', success_message=success_message)
    
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
