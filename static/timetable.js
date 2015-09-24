$(document).ready(function() {
    var body = $("#TimeTable tbody");
        body.children().each(function (row) { // iterate over <tr>s
             $(this).children().each(function (col) { // iterate over <td>s
                 $(this).data('row', row);
                 $(this).data('col', col);
             });
        });
       body.find('td').click(function () {
           var row = $(this).data('row');
           var col = $(this).data('col');
           if($(this).hasClass('tableClassSelectingAvail')){
               $(this).addClass('hasClass');
           }
               $('td').removeClass('tableClassSelectingAvail');
               $('td').removeClass('tableClassSelectingNotAvail');
          //alert("You clicked on row " + row + ", col " + col);
    });
    $('.addClass').click(function(){
         var body = $("#TimeTable tbody");
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

