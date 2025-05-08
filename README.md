HiveMind 🌌
A Cosmic Mood Analysis App Powered by Quantum Vibes
HiveMind is a futuristic web application that syncs your emotions with the universe’s pulse. Featuring a sci-fi interface with a cosmic void backdrop, ambient music, and quantum-inspired insights, it analyzes your mood, reflects collective vibes, and offers suggestions to elevate your consciousness. Built for Replit’s free plan and hosted on GitHub, HiveMind is your portal to the multiverse.
Features

Sci-Fi Interface: Immersive cosmic void with twinkling stars and neon cyan/magenta accents.
Ambient Soundtrack: Autoplaying sci-fi music with a play/pause toggle for user control.
Sentiment Analysis: Detects your mood (POSITIVE/NEGATIVE) with a confidence score using VADER.
Universal Pulse: Displays a percentage of positive vibes based on dummy social trends.
Cosmic Insights: Personalized suggestions to align your energy (e.g., “Your vibe is stellar!”).
Responsive Design: Seamless experience on mobile and desktop.
Zero-Cost Deployment: Runs efficiently on Replit’s free tier.

Tech Stack

Backend: Python 3.11, Flask 3.0.3
Sentiment Analysis: VADER Sentiment 3.3.2
Frontend: HTML, CSS, JavaScript
Audio: Royalty-free MP3 (Pixabay)
Fonts: Exo 2, Source Code Pro (Google Fonts)
Hosting: Replit (free plan)

Prerequisites

Replit account (free tier) or local Python environment.
Internet connection for external audio and fonts.
Modern browser (Chrome, Firefox recommended) with audio autoplay enabled.

Setup Instructions
On Replit

Create a Repl:

Visit Replit and start a new Python project (e.g., HiveMind).


Import from GitHub:

Click Import from GitHub and enter: https://github.com/<your-username>/HiveMind.
Alternatively, manually add app.py, templates/index.html, and .replit from the repository.


Configure .replit:

Ensure .replit contains:run = "python3 app.py"




Install Dependencies:

In the Replit Shell, run:pip install flask==3.0.3 vaderSentiment==3.3.2 --no-cache-dir




Run the App:

Click Run or execute:python3 app.py


Access the app at the provided URL (e.g., https://<your-project>.replit.app).



Locally

Clone the Repository:

Clone this repo:git clone https://github.com/<your-username>/HiveMind.git
cd HiveMind




Install Dependencies:

Ensure Python 3.11 is installed.
Run:pip3 install flask==3.0.3 vaderSentiment==3.3.2




Run the App:

Execute:python3 app.py


Open http://localhost:5000 in a browser.



Usage

Launch the App:

Navigate to the Replit URL or http://localhost:5000.
Enjoy a cosmic interface with a starfield and ambient music.


Input Your Mood:

Enter your emotional state (e.g., “Feeling stellar today” or “Lost in the void”).
Click Sync with the Void.


Explore Results:

Quantum State: Your mood (POSITIVE/NEGATIVE) with a sync percentage.
Universal Pulse: Percentage of positive collective vibes.
Cosmic Insight: A suggestion to harmonize your energy.


Manage Music:

Toggle the Play/Pause Music button in the top-right to control the soundtrack.



Future Enhancements

Integrate real-time social media trends (e.g., X API) for dynamic Universal Pulse.
Add user accounts for personalized mood tracking.
Enhance cosmic insights with more varied suggestions.
Support multiple ambient music tracks for user customization.
Optimize starfield animation for low-end devices.

Acknowledgments

Crafted with passion for the multiverse, inspired by quantum entanglement and cosmic consciousness.
Gratitude to Pixabay for royalty-free audio and Google Fonts for sci-fi typography.
Thanks to Replit for enabling free hosting.

Sync with the void and discover
