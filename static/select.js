
$(document).ready(function (){
    $('#addDiv').on('click',function(){
          alert("HI");
        var body = $("#tableTest tbody");
        body.children().each(function(row){
            $(this).children().each(function (col){
                if(col == 3 && (row == 5 || row == 9)){
                    $(this).addClass('tableClassSelectingAvail');
                }
                else{
                    $(this).addClass('tableClassSelectingNotAvail');
                }
            });
        });
    });
});


