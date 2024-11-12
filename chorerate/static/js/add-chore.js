document.addEventListener('DOMContentLoaded', function() {

    document.getElementById('chore-frequency').onchange = function() {
        const selectedValue = this.value;
        if (this.value === 'daily') {
            document.getElementById('frequency').innerText = 'day';
        } else if (this.value === 'weekly') {
            document.getElementById('frequency').innerText = 'week';
        } else if (this.value === 'monthly') {
            document.getElementById('frequency').innerText = 'month';
        }
    };

});