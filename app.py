from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
import random
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'cosmic_void_123'

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    try:
        conn = sqlite3.connect('data/hivemind.db')
        c = conn.cursor()
        c.execute("SELECT id, username FROM users WHERE id = ?", (user_id,))
        user = c.fetchone()
        conn.close()
        if user:
            print(f"User loaded: {user[1]}")
            return User(user[0], user[1])
        print("User not found")
        return None
    except Exception as e:
        print(f"Error loading user: {e}")
        return None

# Database initialization
def init_db():
    try:
        if not os.path.exists('data'):
            os.makedirs('data')
        conn = sqlite3.connect('data/hivemind.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS moods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            mood TEXT,
            quantum_state TEXT,
            universal_pulse REAL,
            cosmic_insight TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS dreams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            dream TEXT,
            emotional_tone TEXT,
            themes TEXT,
            continuation TEXT,
            resonance_score REAL,
            sensory_vision TEXT,
            sensory_feel TEXT,
            sensory_sound TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS fears (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            dream_id INTEGER,
            fear_type TEXT,
            intensity REAL,
            ptsd_indicator TEXT,
            coping_suggestion TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS personas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            dream_id INTEGER,
            traits TEXT,
            cosmic_description TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        conn.commit()
        conn.close()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")

# Mood analysis
def analyze_mood(mood):
    try:
        analyzer = SentimentIntensityAnalyzer()
        score = analyzer.polarity_scores(mood)['compound']
        print(f"Mood analyzed: {mood}, Score: {score}")
        return score
    except Exception as e:
        print(f"Error analyzing mood: {e}")
        return 0

# Generate cosmic insight
def generate_insight(quantum_state):
    insights = {
        'POSITIVE': 'Embrace the cosmic energy, your vibes are aligning the stars!',
        'NEGATIVE': 'The void is heavy, but even black holes birth new galaxies.',
        'NEUTRAL': 'In the cosmic balance, you are the pivot of infinite possibilities.'
    }
    return insights.get(quantum_state, 'Sync with the void to find your path.')

# Mood-to-avatar mapping
def get_avatar_style(quantum_state):
    if quantum_state == "POSITIVE":
        return "star-glow"
    elif quantum_state == "NEGATIVE":
        return "nebula-cloud"
    else:
        return "quantum-particle"

# Save mood to database
def save_mood(user_id, mood, quantum_state, universal_pulse, cosmic_insight):
    try:
        conn = sqlite3.connect('data/hivemind.db')
        c = conn.cursor()
        c.execute("INSERT INTO moods (user_id, mood, quantum_state, universal_pulse, cosmic_insight) VALUES (?, ?, ?, ?, ?)",
                  (user_id, mood, quantum_state, universal_pulse, cosmic_insight))
        conn.commit()
        conn.close()
        print(f"Mood saved for user {user_id}: {mood}")
    except Exception as e:
        print(f"Error saving mood: {e}")

# Dream analysis
def analyze_dream(dream):
    try:
        analyzer = SentimentIntensityAnalyzer()
        score = analyzer.polarity_scores(dream)['compound']
        emotional_tone = "POSITIVE" if score > 0 else "NEGATIVE" if score < 0 else "NEUTRAL"
        
        # Keyword-based theme detection
        themes = []
        dream_lower = dream.lower()
        if any(word in dream_lower for word in ['fly', 'soar', 'sky']):
            themes.append("Freedom")
        if any(word in dream_lower for word in ['dark', 'forest', 'shadow']):
            themes.append("Fear")
        if any(word in dream_lower for word in ['light', 'glow', 'star']):
            themes.append("Hope")
        if any(word in dream_lower for word in ['city', 'building', 'street']):
            themes.append("Exploration")
        if not themes:
            themes.append("Mystery")
        
        print(f"Dream analyzed: {dream}, Tone: {emotional_tone}, Themes: {themes}")
        return emotional_tone, themes, score
    except Exception as e:
        print(f"Error analyzing dream: {e}")
        return "NEUTRAL", ["Mystery"], 0

# Dark fears and PTSD analysis
def analyze_fears_and_ptsd(dream, user_id, dream_id):
    try:
        dream_lower = dream.lower()
        fears = []
        intensity = 0
        
        # Fear detection
        fear_map = {
            "fear_of_loss": ["death", "lose", "gone"],
            "fear_of_failure": ["fall", "fail", "collapse"],
            "fear_of_abandonment": ["alone", "abandon", "left"],
            "fear_of_pursuit": ["chase", "run", "hunt"]
        }
        for fear_type, keywords in fear_map.items():
            if any(keyword in dream_lower for keyword in keywords):
                fears.append(fear_type)
                intensity += 0.3
        
        # PTSD detection: Trigger on single negative dream
        ptsd_indicator = "No PTSD indicators detected"
        if "chase" in dream_lower or "dark" in dream_lower or len(fears) > 0:
            ptsd_indicator = "Potential PTSD: Intense fear detected"
        
        # Coping suggestion
        coping_suggestion = "Reflect on your dream in a journal. Consider discussing intense fears with a trusted friend or professional."
        
        # Save fears
        conn = sqlite3.connect('data/hivemind.db')
        c = conn.cursor()
        if fears:
            for fear in fears:
                c.execute("INSERT INTO fears (user_id, dream_id, fear_type, intensity, ptsd_indicator, coping_suggestion) VALUES (?, ?, ?, ?, ?, ?)",
                          (user_id, dream_id, fear, intensity, ptsd_indicator, coping_suggestion))
        else:
            c.execute("INSERT INTO fears (user_id, dream_id, fear_type, intensity, ptsd_indicator, coping_suggestion) VALUES (?, ?, ?, ?, ?, ?)",
                      (user_id, dream_id, "No fears detected", 0, ptsd_indicator, coping_suggestion))
        conn.commit()
        conn.close()
        
        print(f"Fears analyzed: {fears}, PTSD: {ptsd_indicator}, Dream ID: {dream_id}")
        return fears, ptsd_indicator, coping_suggestion
    except Exception as e:
        print(f"Error analyzing fears/PTSD: {e}")
        return [], "No PTSD indicators detected", "Try reflecting on your dream to understand its meaning."

# Second character analysis
def analyze_second_character(user_id, dream, themes, emotional_tone, fears):
    try:
        dream_lower = dream.lower()
        traits = []
        cosmic_description = []
        
        # Single dream-based traits
        if "fly" in dream_lower or "city" in dream_lower:
            traits.append("Creativity")
            cosmic_description.append("Your creativity sparks like a supernova, birthing new universes.")
        if "hope" in dream_lower or "light" in dream_lower:
            traits.append("Empathy")
            cosmic_description.append("Your empathy flows like a cosmic river, linking distant galaxies.")
        if any(fear in ["fear_of_loss", "fear_of_abandonment"] for fear in fears):
            traits.append("Vulnerability")
            cosmic_description.append("Your vulnerability is a tender nebula, cradling stars yet to be born.")
        if any(fear in ["fear_of_pursuit", "fear_of_failure"] for fear in fears):
            traits.append("Control-Seeking")
            cosmic_description.append("Your control-seeking nature is a black hole, pulling chaos into order.")
        
        # Resilience check
        conn = sqlite3.connect('data/hivemind.db')
        c = conn.cursor()
        one_week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
        c.execute("SELECT quantum_state FROM moods WHERE user_id = ? AND timestamp > ?", 
                  (user_id, one_week_ago))
        recent_moods = c.fetchall()
        positive_mood_count = sum(1 for m in recent_moods if m[0] == "POSITIVE")
        if positive_mood_count > 0 and emotional_tone == "NEGATIVE":
            traits.append("Resilience")
            cosmic_description.append("Your resilience shines like a pulsar, pulsing strong through the void.")
        
        if not traits:
            traits.append("Mystery")
            cosmic_description.append("Your inner self is a hidden constellation, waiting to be charted. Share more dreams to reveal it.")
        
        # Save persona
        c.execute("INSERT INTO personas (user_id, dream_id, traits, cosmic_description) VALUES (?, ?, ?, ?)",
                  (user_id, dream_id, ", ".join(traits), "; ".join(cosmic_description)))
        conn.commit()
        conn.close()
        
        print(f"Second character analyzed: {traits}, Dream ID: {dream_id}")
        return traits, cosmic_description
    except Exception as e:
        print(f"Error analyzing second character: {e}")
        return ["Mystery"], ["Your inner self is a cosmic enigma, yet to be unveiled."]

# Generate symbolic continuation
def generate_continuation(emotional_tone, themes):
    continuations = {
        "POSITIVE": [
            "You ascend higher, discovering a glowing orb that whispers your destiny.",
            "A radiant path opens, leading you to a cosmic sanctuary of infinite wisdom."
        ],
        "NEGATIVE": [
            "You confront the shadows, finding a hidden light that guides you forward.",
            "The darkness parts, revealing a bridge to a realm of newfound strength."
        ],
        "NEUTRAL": [
            "The path twists, unveiling a mirror that reflects your inner universe.",
            "You drift into a nebula, where whispers of truth shape your next step."
        ]
    }
    return random.choice(continuations.get(emotional_tone, ["The void unfolds, revealing a new chapter of your journey."]))

# Generate Future Echoes
def generate_future_echoes(dream, themes, fears, traits):
    future_scenarios = {
        "Freedom": [
            "In 2075, you pilot a starship through neon skies, exploring uncharted galaxies.",
            "By 2100, your creative vision shapes a utopian city floating in the cosmos."
        ],
        "Fear": [
            "In 2080, you lead a rebellion against a shadowy AI overlord chasing your people.",
            "By 2090, you uncover a hidden truth in a dark forest of digital illusions."
        ],
        "Hope": [
            "In 2070, you guide humanity with a glowing star’s wisdom, uniting distant worlds.",
            "By 2120, your empathy builds a cosmic alliance against interstellar strife."
        ],
        "Exploration": [
            "In 2065, you map a bustling megacity on a distant planet, uncovering alien secrets.",
            "By 2100, your adventures redefine humanity’s place in the galactic frontier."
        ],
        "Mystery": [
            "In 2085, you decode a cryptic signal from the void, revealing your cosmic destiny.",
            "By 2150, your journey unveils a hidden universe within the folds of reality."
        ]
    }
    primary_theme = themes[0] if themes else "Mystery"
    scenario = random.choice(future_scenarios.get(primary_theme, ["In the future, you shape the cosmos in ways yet unseen."]))
    
    # Personalize with fears/traits
    if "fear_of_pursuit" in fears:
        scenario += " Your courage overcomes relentless pursuers."
    if "Creativity" in traits:
        scenario += " Your innovative ideas spark a new era."
    if "Empathy" in traits:
        scenario += " Your compassion unites diverse beings."
    
    return scenario

# Calculate resonance score
def calculate_resonance_score(themes, emotional_tone):
    value_scores = {
        "Freedom": 20,
        "Hope": 15,
        "Exploration": 15,
        "Courage": 10,
        "Love": 10,
        "Mystery": 5,
        "Fear": -5
    }
    score = sum(value_scores.get(theme, 5) for theme in themes)
    if emotional_tone == "POSITIVE":
        score += 10
    elif emotional_tone == "NEGATIVE":
        score -= 5
    return min(max(score, 0), 100)

# Generate sensory blueprints
def generate_sensory_blueprints(themes):
    vision_map = {
        "Freedom": "Neon skies with endless horizons",
        "Fear": "Dark mists swirling around jagged peaks",
        "Hope": "Golden stars pulsing in a velvet void",
        "Exploration": "Bustling cosmic cities with glowing spires",
        "Mystery": "Shimmering auroras over an unknown realm"
    }
    feel_map = {
        "Freedom": "Weightless, soaring through the cosmos",
        "Fear": "A chill, as if shadows cling to your skin",
        "Hope": "Warmth, like a star’s gentle embrace",
        "Exploration": "A thrill, as if every step reveals wonders",
        "Mystery": "A tingle, as secrets unfold around you"
    }
    sound_map = {
        "Freedom": "A uplifting hum of distant galaxies",
        "Fear": "Low, eerie whispers in the void",
        "Hope": "Soft chimes of celestial light",
        "Exploration": "Rhythmic pulses of an alien metropolis",
        "Mystery": "Faint echoes of an unseen presence"
    }
    primary_theme = themes[0] if themes else "Mystery"
    return (
        vision_map.get(primary_theme, "A vast, uncharted cosmos"),
        feel_map.get(primary_theme, "A sense of infinite possibility"),
        sound_map.get(primary_theme, "A soft cosmic hum")
    )

# Save dream to database
def save_dream(user_id, dream, emotional_tone, themes, continuation, resonance_score, sensory_vision, sensory_feel, sensory_sound):
    try:
        conn = sqlite3.connect('data/hivemind.db')
        c = conn.cursor()
        c.execute("INSERT INTO dreams (user_id, dream, emotional_tone, themes, continuation, resonance_score, sensory_vision, sensory_feel, sensory_sound) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (user_id, dream, emotional_tone, ", ".join(themes), continuation, resonance_score, sensory_vision, sensory_feel, sensory_sound))
        dream_id = c.lastrowid
        conn.commit()
        conn.close()
        print(f"Dream saved for user {user_id}: {dream}, Dream ID: {dream_id}")
        return dream_id
    except Exception as e:
        print(f"Error saving dream: {e}")
        return None

# Get resonance map data
def get_resonance_map_data(user_id):
    try:
        conn = sqlite3.connect('data/hivemind.db')
        c = conn.cursor()
        
        # User moods
        c.execute("SELECT quantum_state, universal_pulse, timestamp FROM moods WHERE user_id = ?", (user_id,))
        moods = c.fetchall()
        mood_data = []
        for m in moods:
            try:
                timestamp = datetime.strptime(m[2], '%Y-%m-%d %H:%M:%S')
                hours_ago = (datetime.now() - timestamp).total_seconds() / 3600
                mood_data.append({
                    'x': float(hours_ago),  # Ensure float
                    'y': float(m[1]),       # Ensure float
                    'color': 'blue' if m[0] == 'POSITIVE' else 'red' if m[0] == 'NEGATIVE' else 'white'
                })
            except (ValueError, TypeError) as e:
                print(f"Skipping invalid mood data: {m}, Error: {e}")
                continue
        
        # User dreams
        c.execute("SELECT themes, resonance_score, timestamp FROM dreams WHERE user_id = ?", (user_id,))
        dreams = c.fetchall()
        dream_data = []
        for d in dreams:
            try:
                timestamp = datetime.strptime(d[2], '%Y-%m-%d %H:%M:%S')
                hours_ago = (datetime.now() - timestamp).total_seconds() / 3600
                dream_data.append({
                    'x': float(hours_ago),
                    'y': float(d[1]),
                    'size': float(d[1]) / 10,
                    'themes': d[0].split(', ') if d[0] else ['Mystery']
                })
            except (ValueError, TypeError) as e:
                print(f"Skipping invalid dream data: {d}, Error: {e}")
                continue
        
        # Community data (anonymized)
        c.execute("SELECT themes, resonance_score FROM dreams WHERE user_id != ?", (user_id,))
        community_dreams = c.fetchall()
        community_data = []
        for d in community_dreams:
            try:
                community_data.append({
                    'x': float(random.uniform(-100, 100)),
                    'y': float(random.uniform(0, 100)),
                    'size': float(d[1]) / 20,
                    'color': 'rgba(255, 255, 255, 0.2)'
                })
            except (ValueError, TypeError) as e:
                print(f"Skipping invalid community data: {d}, Error: {e}")
                continue
        
        conn.close()
        print(f"Resonance map data: Moods={len(mood_data)}, Dreams={len(dream_data)}, Community={len(community_data)}")
        return {'moods': mood_data, 'dreams': dream_data, 'community': community_data}
    except Exception as e:
        print(f"Error getting resonance map data: {e}")
        return {'moods': [], 'dreams': [], 'community': []}

# Routes
@app.route('/')
def index():
    print("Redirecting to login")
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            conn = sqlite3.connect('data/hivemind.db')
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            flash('Account created! Log in to enter the void.', 'success')
            print(f"Signup successful: {username}")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists. Try another.', 'error')
            print(f"Signup failed: Username {username} exists")
        except Exception as e:
            print(f"Error during signup: {e}")
            flash('An error occurred. Please try again.', 'error')
        finally:
            conn.close()
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            conn = sqlite3.connect('data/hivemind.db')
            c = conn.cursor()
            c.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))
            user = c.fetchone()
            conn.close()
            if user and user[2] == password:
                user_obj = User(user[0], user[1])
                login_user(user_obj)
                print(f"Login successful: {username}")
                return redirect(url_for('dashboard'))
            flash('Invalid credentials. Try again.', 'error')
            print(f"Login failed: Invalid credentials for {username}")
        except Exception as e:
            print(f"Error during login: {e}")
            flash('An error occurred. Please try again.', 'error')
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        mood = request.form['mood']
        sentiment_score = analyze_mood(mood)
        quantum_state = "POSITIVE" if sentiment_score > 0 else "NEGATIVE" if sentiment_score < 0 else "NEUTRAL"
        universal_pulse = abs(sentiment_score) * 100
        cosmic_insight = generate_insight(quantum_state)
        avatar_style = get_avatar_style(quantum_state)
        save_mood(current_user.id, mood, quantum_state, universal_pulse, cosmic_insight)
        return render_template('dashboard.html', quantum_state=quantum_state, universal_pulse=universal_pulse, cosmic_insight=cosmic_insight, avatar_style=avatar_style)
    return render_template('dashboard.html', avatar_style="quantum-particle")

@app.route('/dream', methods=['GET', 'POST'])
@login_required
def dream():
    if request.method == 'POST':
        dream = request.form['dream']
        emotional_tone, themes, sentiment_score = analyze_dream(dream)
        continuation = generate_continuation(emotional_tone, themes)
        resonance_score = calculate_resonance_score(themes, emotional_tone)
        sensory_vision, sensory_feel, sensory_sound = generate_sensory_blueprints(themes)
        dream_id = save_dream(current_user.id, dream, emotional_tone, themes, continuation, resonance_score, sensory_vision, sensory_feel, sensory_sound)
        fears, ptsd_indicator, coping_suggestion = analyze_fears_and_ptsd(dream, current_user.id, dream_id)
        traits, cosmic_description = analyze_second_character(current_user.id, dream, themes, emotional_tone, fears)
        future_echo = generate_future_echoes(dream, themes, fears, traits)
        return render_template('dream.html', dream=dream, emotional_tone=emotional_tone, themes=themes, continuation=continuation, resonance_score=resonance_score, sensory_vision=sensory_vision, sensory_feel=sensory_feel, sensory_sound=sensory_sound, fears=fears, ptsd_indicator=ptsd_indicator, coping_suggestion=coping_suggestion, traits=traits, cosmic_description=cosmic_description, future_echo=future_echo)
    return render_template('dream.html')

@app.route('/resonance')
@login_required
def resonance():
    map_data = get_resonance_map_data(current_user.id)
    return render_template('resonance.html', map_data=map_data)

@app.route('/logout')
@login_required
def logout():
    print(f"User {current_user.username} logged out")
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=8000)
