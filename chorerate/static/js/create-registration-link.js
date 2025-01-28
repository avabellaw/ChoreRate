import btnClickMsg from "./btn-click-msg.js";

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('registration-link-btn').addEventListener('click', function(event) {
        fetch('/get-registration-link', {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.getElementById('csrf-token').value,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'household_id': document.getElementById('household-id').value
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                let link = data.registration_link;
                navigator.clipboard.writeText(link).then(() => {
                    btnClickMsg(this, event);
                }).catch(err => {
                    console.error('Failed to copy: ', err);
                });
            } else {
                alert(data.message);
            }
        });
    });

});