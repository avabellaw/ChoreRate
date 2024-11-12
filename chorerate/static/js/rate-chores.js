document.addEventListener('DOMContentLoaded', function() {
    let choresList;
    let index = 1;
    fetch('/rate/get-unrated')
        .then(response => response.json())
        .then(data => {
            choresList = data;
            document.getElementById('unrated-total').textContent = choresList.length;
            showChore();
        })
        .catch(error => console.error('Error fetching unrated chores:', error));

    function showChore() {
        if (index < choresList.length) {
            document.getElementById('chore-index').textContent = index;

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
            document.getElementById('rate-chores-container').classList.add('hidden');
            let message = document.getElementById('message');
            message.classList.remove('hidden');
        }
    }
});