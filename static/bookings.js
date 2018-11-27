$(document).ready(function(){
    $.ajax({
        url: "/bookings/time/"+$("#id_reserved_date").val()+"/",
        success: function(result){$( "#time" ).html(result);}
    });
});

$(".date").click(function() {
    $("#id_reserved_date").val($(this).data("date")).addClass("selected");
    $(".date").removeClass("selected");
    $(this).addClass("selected");
    $.ajax({
        url: "/bookings/time"+$(this).data("time"),
        success: function(result){$( "#time" ).html(result);},
        dataType : "html"
    });
});
$(".pax").click(function() {
    $("#id_party_size").val($(this).data("pax")).addClass("selected");
    $(".pax").removeClass("selected");
    $(this).addClass("selected");
});
$("#id_phone, #id_name, #id_email, #id_party_size, #id_reserved_date, #id_reserved_time, #id_booking_method, #id_notes").change(function(){
    $(this).addClass("selected");
})
$("#id_party_size").change(function(){
    $(".pax").removeClass("selected");
})
$("#id_reserved_date").change(function(){
    $(".date").removeClass("selected");
})
$("#id_reserved_time").change(function(){
    $(".time").removeClass("selected");
})
$("#remove").click(function() {
    $(".date").removeClass("selected");
    $(".time").removeClass("selected");
    $(".pax").removeClass("selected");
    $("#id_phone").removeClass("selected");
    $("#id_name").removeClass("selected");
    $("#id_email").removeClass("selected");
    $("#id_party_size").removeClass("selected");
    $("#id_reserved_date").removeClass("selected");
    $("#id_reserved_time").removeClass("selected");
    $("#id_booking_method").removeClass("selected");
    $("#id_notes").removeClass("selected");
    $("id_status".val(""))
})
$("#id_reservation_time").prop("readonly", true);

$("#id_reserved_date, #pick_date").datepicker({dateFormat: 'dd/mm/yy', minDate: 0});

$("#to_reserved_date").click(function() {
    $("#id_reserved_date").addClass("selected").focus();
});

$("#to_party_size").click(function() {
    $("#id_party_size").addClass("selected").focus();
});
