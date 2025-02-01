document.addEventListener('DOMContentLoaded', function () {
    todaysChores = document.getElementById('todays-chores').children;
    for (chore of todaysChores) {
        chore.addEventListener('click', function () {
            fetch('/toggle-chore-completed', {
                method: 'POST',
                body: JSON.stringify({
                    chore_id: chore.dataset.choreId
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(response => response.json()).then(result => {
                if (!result.completed) {
                    chore.classList.remove('completed');
                } else {
                    chore.classList.add('completed');
                }
            });
        });
    }
});