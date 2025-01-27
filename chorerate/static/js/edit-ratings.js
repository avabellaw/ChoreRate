document.addEventListener('DOMContentLoaded', function () {
    let choreBtnContainers = document.getElementsByClassName('rate-btn-container')

    for (let btnContainer of choreBtnContainers) {
        let buttons = btnContainer.children;
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
    }
});