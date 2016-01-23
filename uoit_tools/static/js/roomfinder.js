
$(function () {
    var today = new Date();
    $('#roomfinder-date').datepicker({
        'startDate': today,
        autoclose: true
    });
    $('#roomfinder-date').datepicker('update', today);

    $('#roomfinder-start').timepicker();
    $('#roomfinder-end').timepicker();
});
