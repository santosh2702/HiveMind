document.addEventListener('DOMContentLoaded', function() {
    // Form Animations
    function setupFormAnimations() {
        const inputs = document.querySelectorAll('input, textarea');
        inputs.forEach(input => {
            input.addEventListener('focus', () => {
                input.style.boxShadow = '0 0 10px #00f7ff';
                input.style.transform = 'scale(1.05)';
            });
            input.addEventListener('blur', () => {
                input.style.boxShadow = 'none';
                input.style.transform = 'scale(1)';
            });
        });

        // Reset form after submission
        const forms = document.querySelectorAll('#mood-form, #dream-form');
        forms.forEach(form => {
            form.addEventListener('submit', () => {
                setTimeout(() => {
                    form.reset();
                }, 1000);
            });
        });
    }

    // Share Buttons
    function setupShareButtons() {
        const shareXButtons = document.querySelectorAll('.share-x');
        shareXButtons.forEach(button => {
            button.addEventListener('click', async () => {
                const insight = button.dataset.insight;
                try {
                    const response = await fetch('/api/share/x', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ insight })
                    });
                    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                    const result = await response.json();
                    alert(result.message + ': ' + result.tweet);
                } catch (e) {
                    console.error('Share to X failed:', e);
                    alert('Error sharing to X: ' + e.message);
                }
            });
        });

        const shareInstagramButtons = document.querySelectorAll('.share-instagram');
        shareInstagramButtons.forEach(button => {
            button.addEventListener('click', async () => {
                const insight = button.dataset.insight;
                try {
                    const response = await fetch('/api/share/instagram', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ insight })
                    });
                    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                    const result = await response.json();
                    window.open(result.url, '_blank');
                } catch (e) {
                    console.error('Share to Instagram failed:', e);
                    alert('Error preparing Instagram share: ' + e.message);
                }
            });
        });
    }

    // Mood History
    function setupMoodHistory() {
        const moodsDiv = document.getElementById('moods');
        if (moodsDiv) {
            fetch('/api/moods')
                .then(response => response.json())
                .then(moods => {
                    moodsDiv.innerHTML = '';
                    moods.forEach(mood => {
                        const div = document.createElement('div');
                        div.className = 'result';
                        div.innerHTML = `
                            <p>Mood: ${mood.mood}</p>
                            <p>Sentiment: ${mood.sentiment}</p>
                            <p>Insight: ${mood.insight}</p>
                            <p>Timestamp: ${mood.timestamp}</p>
                            <img src="${mood.image_path}" class="insight-image" alt="Mood Insight">
                            <div class="share-buttons">
                                <button class="share-x" data-insight="${mood.mood} - ${mood.insight}">Share on X</button>
                                <button class="share-instagram" data-insight="${mood.mood} - ${mood.insight}">Share on Instagram</button>
                                <a href="/api/generate_image/mood/${mood.id}" download="mood_insight.png"><button>Download Image</button></a>
                            </div>
                        `;
                        moodsDiv.appendChild(div);
                    });
                    setupShareButtons();
                })
                .catch(error => console.error('Error fetching moods:', error));
        }
    }

    // Dream History
    function setupDreamHistory() {
        const dreamsDiv = document.getElementById('dreams');
        if (dreamsDiv) {
            fetch('/api/dreams')
                .then(response => response.json())
                .then(dreams => {
                    dreamsDiv.innerHTML = '';
                    dreams.forEach(dream => {
                        const div = document.createElement('div');
                        div.className = 'result';
                        div.innerHTML = `
                            <p>Dream: ${dream.dream}</p>
                            <p>Tone: ${dream.tone}</p>
                            <p>Themes: ${dream.themes}</p>
                            <p>Fears: ${dream.fears}</p>
                            <p>PTSD: ${dream.ptsd}</p>
                            <p>Persona: ${dream.persona}</p>
                            <p>Description: ${dream.description}</p>
                            <p>Future Echoes: ${dream.future_echoes}</p>
                            <div class="share-buttons">
                                <button class="share-x" data-insight="Dream: ${dream.dream} - Tone: ${dream.tone} - Persona: ${dream.persona}">Share on X</button>
                                <button class="share-instagram" data-insight="Dream: ${dream.dream} - Tone: ${dream.tone} - Persona: ${dream.persona}">Share on Instagram</button>
                            </div>
                        `;
                        dreamsDiv.appendChild(div);
                    });
                    setupShareButtons();
                })
                .catch(error => console.error('Error fetching dreams:', error));
        }
    }

    // Resonance Map
    function setupResonanceMap() {
        const resonanceCanvas = document.getElementById('resonanceMap');
        if (resonanceCanvas) {
            try {
                const mapData = JSON.parse(document.getElementById('mapData').textContent || '{}');
                const ctx = resonanceCanvas.getContext('2d');
                new Chart(ctx, {
                    type: 'scatter',
                    data: {
                        datasets: [
                            {
                                label: 'Moods',
                                data: mapData.moods.map(m => ({x: new Date(m.timestamp).getTime(), y: m.sentiment === 'POSITIVE' ? 1 : m.sentiment === 'NEGATIVE' ? -1 : 0, text: m.text})),
                                backgroundColor: '#00f7ff',
                                pointRadius: 5
                            },
                            {
                                label: 'Dreams',
                                data: mapData.dreams.map(d => ({x: new Date(d.timestamp).getTime(), y: d.tone === 'POSITIVE' ? 1.5 : d.tone === 'NEGATIVE' ? -1.5 : 0, text: d.text})),
                                backgroundColor: '#a100ff',
                                pointRadius: 8
                            },
                            {
                                label: 'Community',
                                data: mapData.community,
                                backgroundColor: '#ffffff',
                                pointRadius: 3
                            }
                        ]
                    },
                    options: {
                        scales: {
                            x: { type: 'time', title: { display: true, text: 'Time' } },
                            y: { title: { display: true, text: 'Sentiment' } }
                        },
                        plugins: {
                            tooltip: {
                                callbacks: {
                                    label: context => context.raw.text || ''
                                }
                            }
                        }
                    }
                });
            } catch (e) {
                console.error('Error rendering Resonance Map:', e);
            }
        }
    }

    // Initial setup
    setupFormAnimations();
    setupShareButtons();
    setupMoodHistory();
    setupDreamHistory();
    setupResonanceMap();
});