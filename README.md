HiveMind

A cosmic mood and dream analysis app with X-inspired UI, avatars, and human input-driven insights.

Local Setup





Create virtual environment: python3 -m venv venv



Activate: source venv/bin/activate



Install dependencies: pip install -r requirements.txt



Download Chart.js: curl -o static/lib/chart.min.js https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js



Run: python3 app.py



Open: http://localhost:8000

Features





Mood analysis with cosmic insights and avatars.



AI + NLP dream interpretation with emotional tone, themes, and symbolic continuations.



Resonance score based on universal human values.



Sensory blueprints for immersive dream experiences.



Dark fears and PTSD tracking with coping suggestions.



Second character analysis to uncover hidden personality traits.



Navigation bar for easy access to all features.



Share option to copy or tweet dream analysis insights.



Cosmic Resonance Map: Visualize moods and dreams as a galactic map.



Future Echoes: Sci-fi scenarios based on dream/mood patterns.

Debugging





If PTSD/Persona shows "None", enter dreams like "I was chased in a dark forest" or moods like "Feeling hopeful".



Check terminal logs for errors (e.g., "Fears analyzed", "Second character analyzed").



Verify database: sqlite3 data/hivemind.db "SELECT * FROM fears; SELECT * FROM personas;"



Ensure static/lib/chart.min.js and static/script.js are loaded for resonance map.
