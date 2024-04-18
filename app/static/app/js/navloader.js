function setActive(which) {
    if(which) {
        const which_obj = $("#" + which);
        if (which_obj.length) {
            which_obj.addClass("active");
        } else {
            setTimeout(function () {
                setActive(which);
            }, 200);
        }
    }
}