document.addEventListener('DOMContentLoaded', function() {
    let choresList;
    let index = 0;
    let rateContainer = document.getElementById('rate-chores-container');
    fetch('/rate/get-unrated')
        .then(response => response.json())
        .then(data => {
            choresList = data;
            document.getElementById('unrated-total').textContent = choresList.length;
            console.log(data);
            showChore();

            rateContainer.classList.remove('hidden');
            document.getElementById('loading-indicator').classList.add('hidden');
        })
        .catch(error => console.error('Error fetching unrated chores:', error));
    
    const chooseRating = (btn) => {
        let rating = btn.dataset.rate;
        let choreId = choresList[index - 1].id;
        fetch('/rate', {
            method: 'POST',
            body: JSON.stringify({
                rating: rating,
                chore_id: choreId
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            showChore();
        });
    }

    let buttons = document.getElementById('rate-btn-container').children;
    for (let button of buttons) {
        button.addEventListener('click', function() {
            chooseRating(this);
        });
    }
    
    function showChore() {
        if (index <= choresList.length) {
            document.getElementById('chore-index').textContent = index + 1;

            // Get chore and then increment index
            let chore = choresList[index++];

            document.getElementById('chore-name').textContent = chore.name;
            document.getElementById('times-per-frequency').textContent = chore.times_per_frequency;
            if (chore.frequency === 'daily') {
                document.getElementById('frequency').textContent = 'day';
            } else if (chore.frequency === 'weekly') {
                document.getElementById('frequency').textContent = 'week';
            } else if (chore.frequency === 'monthly') {
                document.getElementById('frequency').textContent = 'month';
            }
        } else {
            rateContainer.classList.add('hidden');
            let message = document.getElementById('message');
            message.classList.remove('hidden');
        }
    }
});