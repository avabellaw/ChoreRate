document.addEventListener('DOMContentLoaded', function() {
    btn = document.getElementById('run-chore-allocation');

    btn.addEventListener('click', function() {
        fetch('/run-chore-allocation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(response => {
            console.log(response);  
            location.reload();          
        }).catch(error => {
            console.error('Error:', error);
        });
    });
});