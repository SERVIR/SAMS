function handleExit() {
    if (history.length > 1) {
        history.back(); // Go back if there's history
    } else {
        window.close(); // Close the tab if there's no history
    }
}