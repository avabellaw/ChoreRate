document.addEventListener('DOMContentLoaded', function() {
    let choresList;
    let index = 0;
    let rateContainer = document.getElementById('rate-chores-container');
    let showBackBtn = false;
    fetch('/rate/get-unrated')
        .then(response => response.json())
        .then(data => {
            choresList = data;
            document.getElementById('unrated-total').textContent = choresList.length;
            if(showChore()) {
                rateContainer.classList.remove('hidden');
            }
            document.getElementById('loading-indicator').classList.add('hidden');
        })
        .catch(error => console.error('Error fetching unrated chores:', error));
    
    // Add event listeners to rate buttons
    let buttons = document.getElementById('rate-btn-container').children;
    for (let button of buttons) {
        button.addEventListener('click', function() {
            chooseRating(this);
        });
    }

    const chooseRating = (btn) => {
        let rating = btn.dataset.rate;
        let chore = choresList[index - 1];

        // If previously rated
        if (chore.rating) {
            document.querySelector(`button[data-rate="${chore.rating}"]`).classList.remove('selected');
        }
        
        // Set rating for if back button is pressed
        chore.rating = rating;

        fetch('/rate', {
            method: 'POST',
            body: JSON.stringify({
                rating: rating,
                chore_id: chore.id
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
    
    function showChore() {
        if (index < choresList.length) {
            // Show back button if there's a previous chore 
            if (index === 1 && !showBackBtn) {
                let backBtn = document.getElementById('back-btn')
                
                backBtn.classList.remove('hidden');
                backBtn.addEventListener('click', function() {
                    index -= 2;
                    showChore();
                });
                showBackBtn = true;
            }

            document.getElementById('chore-index').textContent = index + 1;

            // Get chore and then increment index
            let chore = choresList[index++];

            // If previously rated - the back button was pressed
            if (chore.rating) {
                let prevRating = chore.rating;
                document.querySelector(`button[data-rate="${prevRating}"]`).classList.add('selected');
            }

            document.getElementById('chore-name').textContent = chore.name;
            document.getElementById('times-per-frequency').textContent = chore.times_per_frequency;
            if (chore.frequency === 'daily') {
                document.getElementById('frequency').textContent = 'day';
            } else if (chore.frequency === 'weekly') {
                document.getElementById('frequency').textContent = 'week';
            } else if (chore.frequency === 'monthly') {
                document.getElementById('frequency').textContent = 'month';
            }

            return true;
        } else {
            rateContainer.classList.add('hidden');
            document.getElementById('message').classList.remove('hidden');
            refreshPageAfterTimeout();
            return false; // Signal that there are no more chores to rate.
        }
    }

    async function refreshPageAfterTimeout(){
        setTimeout(function() {
            window.location.reload();
        }, 3000);
    }
});