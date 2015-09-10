
$(document).ready(function init() {
    var body = $("#tableTest tbody");
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
         // alert("You clicked on row " + row + ", col " + col);
    });

});

