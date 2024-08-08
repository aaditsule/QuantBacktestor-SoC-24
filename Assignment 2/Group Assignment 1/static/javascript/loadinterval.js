import { intervals } from './constants.js';

document.addEventListener('DOMContentLoaded', function() {
    const selectElement = document.getElementById('interval');
    
    // Populate the select element with options from the intervals array
    intervals.forEach(interval => {
        const option = document.createElement('option');
        option.value = interval.value;
        option.textContent = interval.label;
        selectElement.appendChild(option);
    });

    // Set default selected option to '1d' (Daily)
    selectElement.value = '1d';
});