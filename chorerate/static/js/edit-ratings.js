document.addEventListener('DOMContentLoaded', function () {
    let buttons = document.getElementById('rate-btn-container').children;
    for (let button of buttons) {
        button.addEventListener('click', function () {
            let btnParent = this.parentElement;

            let rating = parseInt(this.dataset.rate);
            let choreID = parseInt(btnParent.dataset.chore);

            fetch('/rate', {
                method: 'POST',
                body: JSON.stringify({
                    rating: rating,
                    chore_id: choreID
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                btnParent.querySelector('.selected').classList.remove('selected');
                button.classList.add('selected');
            });
        });
    }
});