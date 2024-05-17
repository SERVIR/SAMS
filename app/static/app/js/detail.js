$(window).on('load', function () {
    // Get all elements with class "profile-container"
    const profileContainers = document.getElementsByClassName('profile-container');

    // Initialize maximum height to 0
    let maxHeight = 0;

    // Loop through all elements and find the maximum height
    for (let i = 0; i < profileContainers.length; i++) {
        const height = profileContainers[i].offsetHeight;
        if (height > maxHeight) {
            maxHeight = height;
        }
    }

    // Set the height of all elements to the maximum height
    for (let i = 0; i < profileContainers.length; i++) {
        profileContainers[i].style.height = maxHeight + 'px';
    }

});
