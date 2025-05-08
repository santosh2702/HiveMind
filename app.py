from flask import Flask, request, jsonify, render_template
from transformers import pipeline

app = Flask(__name__)

# Initialize sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis")

# Dummy X trends
def get_x_trends():
    tweets = [
        "Sab log khush hai aaj!",
        "Bohot tension ho raha hai yaar.",
        "Naya tech scene mast hai!"
    ]
    sentiments = [sentiment_analyzer(tweet)[0] for tweet in tweets]
    positive_count = sum(1 for s in sentiments if s['label'] == 'POSITIVE')
    total = len(sentiments)
    positive_percentage = (positive_count / total) * 100 if total > 0 else 0
    return positive_percentage

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    user_mood = request.form.get('mood')
    if not user_mood:
        return jsonify({'error': 'Mood toh daal, bhai!'})

    # Analyze mood
    mood_analysis = sentiment_analyzer(user_mood)[0]
    mood_label = mood_analysis['label']
    mood_score = mood_analysis['score']

    # Collective vibe
    positive_percentage = get_x_trends()

    # Desi suggestions
    suggestions = {
        'POSITIVE': [
            "Bhai, tu toh mood mein hai! Ek selfie daal de X pe.",
            "Mast vibe hai, yaar! Aaj koi naya kaam shuru kar.",
            "Tu toh khushiyon ka baadshah hai! Chai ke saath maza le."
        ],
        'NEGATIVE': [
            "Mood off hai? Ek garam chai pi, sab theek ho jayega.",
            "Thoda chill kar, bhai. Apna favorite gaana sun le.",
            "Low feel ho raha hai? Dost ko call kar aur bakchodi kar."
        ]
    }
    suggestion = suggestions[mood_label][hash(user_mood) % len(suggestions[mood_label])]

    return jsonify({
        'mood': mood_label,
        'confidence': mood_score,
        'collective_positive': positive_percentage,
        'suggestion': suggestion
    })

if __name__ == '__main__':
    app.run(debug=True)
