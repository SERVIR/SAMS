let selected_service_area = -999;

function filter_service_area(which) {

    if (which) {
        const service = $(which);
        $("#navbarTabs a").removeClass("active");
        service.addClass('active');
        $("#active_service_text").text(which.text);
        selected_service_area = service.attr('service_area_id');
    }

    $("#filter_region").text($('input[name=region_radio]:checked').attr('data-label'));

    const apps = $(".gallery-card.ember-view");
    apps.map(function (i, app) {
        const app_obj = $(app);
        if(app_obj.attr('app_filter')) {
            if (app_obj.attr('app_filter').includes(selected_service_area) && app_obj.attr('region').includes($('input[name=region_radio]:checked').val())) {
                app_obj.show();
            } else {
                app_obj.hide();
            }
        } else{
            app_obj.show();
        }
    });
}

function text_filter(search) {
    const search_value = search.value.toLowerCase();
    const apps = $(".gallery-card.ember-view");
    apps.map(function (i, app) {
        const app_obj = $(app);
        if(app_obj.attr('app_filter')) {
            if (app_obj.find(".hidden-description").val().toLowerCase().includes(search_value) || app_obj.find(".app-title").val().toLowerCase().includes(search_value)) {
                app_obj.show();
            } else {
                app_obj.hide();
            }
        }else{
            app_obj.show();
        }
    });
}

$(function () {
    $('input[name=region_radio]').on('change', function () {
        filter_service_area();
    });
});

function open_app(url) {
    document.location = url;
}