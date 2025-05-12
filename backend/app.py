from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_file
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import sqlite3
import hashlib
import json
from datetime import datetime
from flask_cors import CORS
import requests
from PIL import Image, ImageDraw, ImageFont
import os
import io
import logging

app = Flask(__name__)
app.secret_key = 'cosmic_void_123'
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8000"}})
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
analyzer = SentimentIntensityAnalyzer()

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Ensure generated images directory exists
os.makedirs('static/generated', exist_ok=True)

def init_db():
    try:
        conn = sqlite3.connect('data/hivemind.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS moods (id INTEGER PRIMARY KEY, user_id INTEGER, mood TEXT, sentiment TEXT, insight TEXT, image_path TEXT, timestamp TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS dreams (id INTEGER PRIMARY KEY, user_id INTEGER, dream TEXT, tone TEXT, themes TEXT, fears TEXT, ptsd TEXT, persona TEXT, description TEXT, future_echoes TEXT, timestamp TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS fears (id INTEGER PRIMARY KEY, user_id INTEGER, fear TEXT, timestamp TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS personas (id INTEGER PRIMARY KEY, user_id INTEGER, persona TEXT, description TEXT, timestamp TEXT)''')
        conn.commit()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
    finally:
        conn.close()

init_db()

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('data/hivemind.db')
    c = conn.cursor()
    c.execute("SELECT id, username FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    if user:
        return User(user[0], user[1])
    return None

def generate_insight_image(insight_text, output_path):
    try:
        img = Image.open('static/images/space.jpg')
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Futura.ttc', 30)
        text_lines = insight_text.split('\n')
        y = 50
        for line in text_lines:
            draw.text((50, y), line, fill=(0, 247, 255), font=font)
            y += 40
        img.save(output_path, 'PNG')
        return True
    except Exception as e:
        logger.error(f"Error generating image: {e}")
        return False

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = hashlib.sha256(request.form.get('password', '').encode()).hexdigest()
        conn = sqlite3.connect('data/hivemind.db')
        c = conn.cursor()
        c.execute("SELECT id, username FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            user_obj = User(user[0], user[1])
            login_user(user_obj)
            return redirect(url_for('dashboard'))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = hashlib.sha256(request.form.get('password', '').encode()).hexdigest()
        conn = sqlite3.connect('data/hivemind.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            conn.close()
            return render_template('signup.html', error="Username already exists")
        finally:
            conn.close()
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        tab = request.form.get('tab')
        if tab == 'mood':
            mood = request.form.get('mood')
            if not mood:
                return render_template('dashboard.html', error="Mood cannot be empty", active_tab='mood')
            sentiment_scores = analyzer.polarity_scores(mood)
            sentiment = 'POSITIVE' if sentiment_scores['compound'] > 0.05 else 'NEGATIVE' if sentiment_scores['compound'] < -0.05 else 'NEUTRAL'
            insight = f"Your mood reflects a {'positive' if sentiment == 'POSITIVE' else 'challenging' if sentiment == 'NEGATIVE' else 'balanced'} state."
            image_path = f"static/generated/mood_{current_user.id}_{int(datetime.now().timestamp())}.png"
            insight_text = f"Mood: {mood}\nSentiment: {sentiment}\nInsight: {insight}"
            generate_insight_image(insight_text, image_path)
            conn = sqlite3.connect('data/hivemind.db')
            c = conn.cursor()
            c.execute("INSERT INTO moods (user_id, mood, sentiment, insight, image_path, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                      (current_user.id, mood, sentiment, insight, image_path, datetime.now().isoformat()))
            conn.commit()
            conn.close()
            return render_template('dashboard.html', success="Mood submitted successfully", active_tab='mood')
        elif tab == 'dream':
            dream_text = request.form.get('dream')
            if not dream_text:
                return render_template('dashboard.html', error="Dream cannot be empty", active_tab='dream')
            sentiment_scores = analyzer.polarity_scores(dream_text)
            tone = 'POSITIVE' if sentiment_scores['compound'] > 0.05 else 'NEGATIVE' if sentiment_scores['compound'] < -0.05 else 'NEUTRAL'
            themes = 'Mystery' if 'snake' in dream_text.lower() or 'chase' in dream_text.lower() else 'Exploration'
            fears = 'fear_of_pursuit' if 'running' in dream_text.lower() or 'chase' in dream_text.lower() else 'none'
            ptsd = 'Potential PTSD: Intense fear detected' if 'fear' in fears or sentiment_scores['neg'] > 0.3 else 'No PTSD indicators'
            persona = 'Mystery' if 'snake' in dream_text.lower() else 'Vulnerability' if 'fear' in fears else 'Empathy'
            persona_desc = 'Your inner self is a cosmic enigma, yet to be unveiled.' if persona == 'Mystery' else 'You seek control in chaos.' if persona == 'Vulnerability' else 'You connect deeply with others.'
            future_echoes = 'In 2080, you unravel a galactic riddle...' if persona == 'Mystery' else 'In 2075, you lead a rebellion...'
            conn = sqlite3.connect('data/hivemind.db')
            c = conn.cursor()
            c.execute("INSERT INTO dreams (user_id, dream, tone, themes, fears, ptsd, persona, description, future_echoes, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (current_user.id, dream_text, tone, themes, fears, ptsd, persona, persona_desc, future_echoes, datetime.now().isoformat()))
            c.execute("INSERT INTO fears (user_id, fear, timestamp) VALUES (?, ?, ?)", (current_user.id, fears, datetime.now().isoformat()))
            c.execute("INSERT INTO personas (user_id, persona, description, timestamp) VALUES (?, ?, ?, ?)",
                      (current_user.id, persona, persona_desc, datetime.now().isoformat()))
            conn.commit()
            conn.close()
            return render_template('dashboard.html', result={
                'dream': dream_text, 'tone': tone, 'themes': themes, 'fears': fears, 'ptsd': ptsd, 'persona': persona,
                'persona_desc': persona_desc, 'future_echoes': future_echoes
            }, success="Dream submitted successfully", active_tab='dream')
    # Resonance Map data
    conn = sqlite3.connect('data/hivemind.db')
    c = conn.cursor()
    c.execute("SELECT mood, sentiment, timestamp FROM moods WHERE user_id = ?", (current_user.id,))
    moods = c.fetchall()
    c.execute("SELECT dream, tone, themes, timestamp FROM dreams WHERE user_id = ?", (current_user.id,))
    dreams = c.fetchall()
    map_data = {
        'moods': [{'text': m[0], 'sentiment': m[1], 'timestamp': m[2]} for m in moods],
        'dreams': [{'text': d[0], 'tone': d[1], 'themes': d[2], 'timestamp': d[3]} for d in dreams],
        'community': [{'x': i, 'y': i*2, 'text': f'Community {i}'} for i in range(5)]
    }
    conn.close()
    return render_template('dashboard.html', map_data=json.dumps(map_data), active_tab='mood')

@app.route('/api/share/x', methods=['POST'])
@login_required
def share_x():
    data = request.json
    insight = data.get('insight')
    if not insight:
        return jsonify({'error': 'Insight cannot be empty'}), 400
    tweet = f"My Cosmic Insight from HiveMind: {insight} #HiveMind #CosmicInsights #DreamTheFuture"
    return jsonify({'status': 'success', 'message': 'Shared to X', 'tweet': tweet})

@app.route('/api/share/instagram', methods=['POST'])
@login_required
def share_instagram():
    data = request.json
    insight = data.get('insight')
    if not insight:
        return jsonify({'error': 'Insight cannot be empty'}), 400
    share_url = f"https://www.instagram.com/?caption={insight}%20%23HiveMind%20%23CosmicInsights"
    return jsonify({'status': 'success', 'message': 'Ready to share on Instagram', 'url': share_url})

@app.route('/api/generate_image/mood/<id>', methods=['GET'])
@login_required
def generate_image(id):
    conn = sqlite3.connect('data/hivemind.db')
    c = conn.cursor()
    c.execute("SELECT mood, sentiment, insight, image_path FROM moods WHERE id = ? AND user_id = ?", (id, current_user.id))
    result = c.fetchone()
    conn.close()
    if not result or not os.path.exists(result[3]):
        return jsonify({'error': 'Image not found'}), 404
    return send_file(result[3], mimetype='image/png')

@app.route('/api/moods', methods=['GET'])
@login_required
def get_moods():
    conn = sqlite3.connect('data/hivemind.db')
    c = conn.cursor()
    c.execute("SELECT id, mood, sentiment, insight, image_path, timestamp FROM moods WHERE user_id = ?", (current_user.id,))
    moods = [{'id': m[0], 'mood': m[1], 'sentiment': m[2], 'insight': m[3], 'image_path': m[4], 'timestamp': m[5]} for m in c.fetchall()]
    conn.close()
    return jsonify(moods)

@app.route('/api/dreams', methods=['GET'])
@login_required
def get_dreams():
    conn = sqlite3.connect('data/hivemind.db')
    c = conn.cursor()
    c.execute("SELECT id, dream, tone, themes, fears, ptsd, persona, description, future_echoes, timestamp FROM dreams WHERE user_id = ?", (current_user.id,))
    dreams = [{'id': d[0], 'dream': d[1], 'tone': d[2], 'themes': d[3], 'fears': d[4], 'ptsd': d[5], 'persona': d[6], 'description': d[7], 'future_echoes': d[8], 'timestamp': d[9]} for d in c.fetchall()]
    conn.close()
    return jsonify(dreams)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)