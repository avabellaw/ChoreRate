document.addEventListener('DOMContentLoaded', function() {

    document.getElementById('chore-frequency').onchange = function() {
        const selectedValue = this.value;
        
        if (selectedValue === 'daily') {
            document.getElementById('frequency').innerText = 'day';
        } else if (selectedValue === 'weekly') {
            document.getElementById('frequency').innerText = 'week';
        } else if (selectedValue === 'monthly') {
            document.getElementById('frequency').innerText = 'month';
        }
    };

});