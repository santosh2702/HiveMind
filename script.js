function shareInsight() {
    const dream = document.querySelector('.dream-text')?.textContent.replace('Dream: ', '') || 'No dream';
    const tone = document.querySelector('.tone-text')?.textContent.replace('Emotional Tone: ', '') || 'Unknown';
    const themes = document.querySelector('.themes-text')?.textContent.replace('Themes: ', '') || 'None';
    const fears = document.querySelector('.fears-text')?.textContent.replace('Dark Fears: ', '') || 'None';
    const ptsd = document.querySelector('.ptsd-text')?.textContent.replace('PTSD Indicator: ', '') || 'None';
    const persona = document.querySelector('.persona-text')?.textContent.replace('Cosmic Persona: ', '') || 'None';
    const description = document.querySelector('.description-text')?.textContent.replace('Description: ', '') || 'None';

    const summary = `My Cosmic Insight from HiveMind:\nDream: ${dream}\nTone: ${tone}\nThemes: ${themes}\nFears: ${fears}\nPTSD: ${ptsd}\nPersona: ${persona}\nDescription: ${description}\nExplore your cosmic self at http://localhost:8000!`;

    // Copy to clipboard
    navigator.clipboard.writeText(summary).then(() => {
        alert('Cosmic insight copied to clipboard!');
    }).catch(err => {
        console.error('Failed to copy: ', err);
        alert('Failed to copy. Please try again.');
    });

    // Twitter share
    const twitterUrl = `https://x.com/intent/tweet?text=${encodeURIComponent(summary)}`;
    window.open(twitterUrl, '_blank');
}

function renderResonanceMap(mapData) {
    console.log('Rendering resonance map with data:', mapData);
    
    if (!mapData || !mapData.moods || !mapData.dreams || !mapData.community) {
        console.error('Invalid map data:', mapData);
        document.getElementById('resonanceMap').style.display = 'none';
        alert('No data available for resonance map. Try adding moods and dreams.');
        return;
    }

    try {
        const ctx = document.getElementById('resonanceMap').getContext('2d');
        new Chart(ctx, {
            type: 'scatter',
            data: {
                datasets: [
                    {
                        label: 'Moods',
                        data: mapData.moods.map(m => ({
                            x: m.x,
                            y: m.y
                        })),
                        backgroundColor: mapData.moods.map(m => m.color),
                        pointRadius: 5
                    },
                    {
                        label: 'Dreams',
                        data: mapData.dreams.map(d => ({
                            x: d.x,
                            y: d.y
                        })),
                        backgroundColor: 'rgba(29, 161, 242, 0.5)',
                        pointRadius: mapData.dreams.map(d => d.size)
                    },
                    {
                        label: 'Community',
                        data: mapData.community.map(c => ({
                            x: c.x,
                            y: c.y
                        })),
                        backgroundColor: mapData.community.map(c => c.color),
                        pointRadius: mapData.community.map(c => c.size)
                    }
                ]
            },
            options: {
                scales: {
                    x: { display: false },
                    y: { display: false }
                },
                plugins: {
                    legend: { display: true },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                if (context.dataset.label === 'Dreams') {
                                    const index = context.dataIndex;
                                    const themes = mapData.dreams[index]?.themes || ['Unknown'];
                                    return `Dream Themes: ${themes.join(', ')}`;
                                }
                                return context.dataset.label;
                            }
                        }
                    }
                }
            }
        });
        console.log('Resonance map rendered successfully');
    } catch (error) {
        console.error('Error rendering resonance map:', error);
        document.getElementById('resonanceMap').style.display = 'none';
        alert('Failed to render resonance map. Please try again.');
    }
}
