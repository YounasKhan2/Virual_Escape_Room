from flask import Flask, render_template, request, redirect, url_for, session, flash
import database
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# Use environment variable for secret key in production
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Initialize database on startup if it doesn't exist
if not os.path.exists(database.get_db_path()):
    database.init_db()

@app.route('/')
def home():
    games = database.get_games()
    preview_games = games[:2] 
    return render_template('index.html', games=preview_games)

@app.route('/escaperooms')
def escaperooms():
    games = database.get_games()
    return render_template('escaperooms.html', games=games)

@app.route('/faqs')
def faqs():
    faqs_data = database.get_faqs()
    return render_template('faqs.html', faqs=faqs_data)

# NEW ROUTES FOR GAMES
@app.route('/game1')
def game1():
    if 'user_id' not in session:
        flash('Please login to play the game', 'error')
        return redirect(url_for('login'))
    return render_template('game1.html')

@app.route('/game2') 
def game2():
    if 'user_id' not in session:
        flash('Please login to play the game', 'error')
        return redirect(url_for('login'))
    return render_template('game2.html')

@app.route('/game3')
def game3():
    if 'user_id' not in session:
        flash('Please login to play the game', 'error')
        return redirect(url_for('login'))
    return render_template('game3.html')

# Authentication Routes
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('signup.html')
        
        # Check if user already exists
        conn = sqlite3.connect(database.get_db_path())
        c = conn.cursor()
        c.execute('SELECT id FROM users WHERE email = ? OR username = ?', (email, username))
        existing_user = c.fetchone()
        
        if existing_user:
            flash('User already exists with this email or username', 'error')
            conn.close()
            return render_template('signup.html')
        
        # Create new user
        hashed_password = generate_password_hash(password)
        c.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                 (username, email, hashed_password))
        conn.commit()
        user_id = c.lastrowid
        conn.close()
        
        session['user_id'] = user_id
        session['username'] = username
        flash('Account created successfully!', 'success')
        return redirect(url_for('home'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = sqlite3.connect(database.get_db_path())
        c = conn.cursor()
        c.execute('SELECT id, username, password FROM users WHERE email = ?', (email,))
        user = c.fetchone()
        conn.close()
        
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    # Get port from environment variable for Azure compatibility
    port = int(os.environ.get('PORT', 8000))
    # Set debug=False for production and host='0.0.0.0' for Azure
    app.run(host='0.0.0.0', port=port, debug=False)