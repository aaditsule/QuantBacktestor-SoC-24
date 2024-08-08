import { tickers } from './constants.js';

// Define available keywords
const availableKeywords = tickers;

// Select relevant DOM elements
const resultsBox = document.querySelector(".result-box");
const symbol = document.getElementById("symbol");
const cancelButton = document.getElementById("cancel-button");

// Hide results box initially
resultsBox.style.display = 'none';

// Event listener for input box input event
symbol.addEventListener('input', function() {
    let input = symbol.value.trim().toLowerCase(); // Get input value in lowercase
    let results = availableKeywords.filter(keyword => keyword.toLowerCase().startsWith(input));
    display(results);
});

// Event listener for input box focus event (to show options)
symbol.addEventListener('focus', function() {
    let input = symbol.value.trim().toLowerCase(); // Get input value in lowercase
    let results = availableKeywords.filter(keyword => keyword.toLowerCase().startsWith(input));
    display(results);
});

// Event listener for cancel button click event
cancelButton.addEventListener('click', function() {
    symbol.value = ''; // Clear input value
    resultsBox.style.display = 'none'; // Hide results
    selectedResultIndex = -1; // Reset selected index
});

// Function to display results in the result box
function display(results) {
    const content = results.map(result => `<li>${result}</li>`).join('');
    resultsBox.innerHTML = '<ul>' + content + '</ul>';
    resultsBox.style.display = results.length > 0 ? 'block' : 'none'; // Show/hide results box

    // Add click event listener to each suggestion item
    const items = resultsBox.querySelectorAll('li');
    items.forEach((item, index) => {
        item.addEventListener('click', function() {
            symbol.value = results[index]; // Set input value to clicked item
            resultsBox.style.display = 'none'; // Hide results box
            selectedResultIndex = -1; // Reset selected index
        });
    });
}

let selectedResultIndex = -1; // Track selected result index

// Handle keyboard navigation (Arrow keys)
symbol.addEventListener('keydown', function(event) {
    const results = Array.from(resultsBox.querySelectorAll('li'));

    if (event.key === 'ArrowUp' && selectedResultIndex > 0) {
        selectedResultIndex--;
    } else if (event.key === 'ArrowDown' && selectedResultIndex < results.length - 1) {
        selectedResultIndex++;
    }

    // Highlight the selected item
    results.forEach((result, index) => {
        if (index === selectedResultIndex) {
            result.classList.add('selected');
            symbol.value = result.textContent.trim(); // Set input value to selected item

            // Auto-scrolling logic
            const scrollTop = resultsBox.scrollTop;
            const offsetTop = result.offsetTop;
            const scrollHeight = resultsBox.scrollHeight;
            const clientHeight = resultsBox.clientHeight;

            if (offsetTop < scrollTop) {
                resultsBox.scrollTop = offsetTop;
            } else if (offsetTop + result.clientHeight > scrollTop + clientHeight) {
                resultsBox.scrollTop = offsetTop - clientHeight + result.clientHeight;
            }
        } else {
            result.classList.remove('selected');
        }
    });
});

// Handle Enter key to select the highlighted item and close the menu
symbol.addEventListener('keydown', function(event) {
    const results = Array.from(resultsBox.querySelectorAll('li'));

    if (event.key === 'Enter') {
        if (selectedResultIndex !== -1) {
            symbol.value = results[selectedResultIndex].textContent.trim();
        }
        resultsBox.style.display = 'none'; // Hide results
        selectedResultIndex = -1; // Reset selected index
    }
});

// Handle backspacing to reset selected index
symbol.addEventListener('keyup', function(event) {
    if (event.key === 'Backspace') {
        selectedResultIndex = -1; // Reset selected index
    }
});
