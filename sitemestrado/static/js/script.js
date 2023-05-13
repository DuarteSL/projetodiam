$(document).ready(function () {
    $("#btn1").click(function () {
        $('#future').show();
        $('#past').hide();
    });
});
$(document).ready(function () {
    $("#btn2").click(function () {
        $('#future').hide();
        $('#past').show();
    });
});
