
$(function () {
    $('#roomfinder-datetime').datetimepicker({
        defaultDate: new Date(),
        stepping: 30,
        format: "dddd, MMMM Do YYYY, h:mm a"
    });
});

function roomFind() {
    var date = $('#roomfinder-datetime').data('date');
    $.ajax({
        url: '/roomfinder',
        data: { 'date': date },
        success: displayRooms,
        error: showRoomFinderError
    });
}

function displayRooms(result) {
    console.log('success');
    console.log(result);
}

function showRoomFinderError(error) {
    console.log('fail');
    console.log(error);
}
