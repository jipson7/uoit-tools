
$(function () {
    var today = new Date();
    $('#roomfinder-datetime').datetimepicker({
        defaultDate: today,
        stepping: 30
    });
});
