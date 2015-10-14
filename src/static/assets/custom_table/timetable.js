// works with table.css

$(document).ready(function() {
    var timetable = $("#TimeTable tbody");
    timetable.children().each(function (row) { // iterate over <tr>s
        $(this).children().each(function (col) { // iterate over <td>s
            $(this).data('row', row);
            $(this).data('col', col);
        });
    });

    // Locate which box we clicked on
    timetable.find('td').click(function () {
        var row = $(this).data('row');
        var col = $(this).data('col');
        if($(this).hasClass('tableClassSelectingAvail')){
            $(this).addClass('hasClass');
        }
        $('td').removeClass('tableClassSelectingAvail');
        $('td').removeClass('tableClassSelectingNotAvail');
        // alert("You clicked on row " + row + ", col " + col);
    });



    $('.sidebar_classes').on('click',function(){
        var courseId = this.id.split('|')[0]
        var classType = this.id.split('|')[1]
        // alert(timetable.attr('id'));

        // Jquery Ajax
        $.get("/class_search/",{
            courseId: courseId,
            classType: classType,
        }, function (data) {
            alert("Data: " + data.message);
        });
        // $.ajax({
        //     type: 'GET',
        //     url: "/class_search/"+courseId+"/"+classType+"/",
        //     success: function(data) {
        //         // alert('Load was performed.'+data.ajax_resp);
        //         console.log(data); // log the returned json to the console
        //     }
        // })
        

        // Get the course and the class type from the sublinks
        // alert(courseId+" , "+classType);
        timetable.children().each(function (row){
            $(this).children().each(function (col){
                if(col == 3 && (row == 5 || row == 9)){
                    $(this).addClass('tableClassSelectingAvail');
                } else {
                    $(this).addClass('tableClassSelectingNotAvail');
                }
            });
        });
    });
});