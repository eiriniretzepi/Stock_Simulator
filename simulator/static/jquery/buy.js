$("#incdec input").change(function(){
  alert("The text has been changed.");
});
$(document).ready(function(){
$("#up").on('click',function(){
    $("#incdec input").val(parseInt($("#incdec input").val())+1);
    alert("The text has been changed.");
});

$("#down").on('click',function(){
    if(parseInt($("#incdec input").val())!=0) {
        $("#incdec input").val(parseInt($("#incdec input").val()) - 1);
    }
});

});
