let data = [];

fetch('data.json')
    .then(res => res.json())
    .then(json => {
        data = json;
        displayEvents(data);
    });

function displayEvents(events) {
    const guide = document.getElementById('guide');
    guide.innerHTML = '';
    events.forEach(e => {
        const div = document.createElement('div');
        div.classList.add('event', e.category);
        div.innerHTML = `<strong>Channel ${e.channel}</strong>: ${e.event} (${e.time}) [${e.category}]`;
        guide.appendChild(div);
    });
}

document.getElementById('search').addEventListener('input', (event) => {
    const query = event.target.value.toLowerCase();
    const filtered = data.filter(e =>
        e.event.toLowerCase().includes(query) || e.category.toLowerCase().includes(query)
    );
    displayEvents(filtered);
});

function filterCategory(cat) {
    if(cat === 'all') {
        displayEvents(data);
    } else {
        displayEvents(data.filter(e => e.category === cat));
    }
}
