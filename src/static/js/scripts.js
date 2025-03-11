// This file contains JavaScript code for client-side interactivity, such as handling user input and updating the interactive map.

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the interactive map
    initMap();

    // Event listener for artifact search
    const searchInput = document.getElementById('artifact-search');
    searchInput.addEventListener('input', function() {
        const query = searchInput.value.toLowerCase();
        filterArtifacts(query);
    });
});

// Function to initialize the interactive map
function initMap() {
    // Code to set up the map goes here
    // This could involve using a mapping library like Leaflet or Google Maps API
}

// Function to filter artifacts based on user input
function filterArtifacts(query) {
    const artifactList = document.querySelectorAll('.artifact-item');
    artifactList.forEach(function(item) {
        const name = item.querySelector('.artifact-name').textContent.toLowerCase();
        if (name.includes(query)) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });
}