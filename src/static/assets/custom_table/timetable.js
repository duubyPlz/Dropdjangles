// works with table.css

$(document).ready(function() {
    var timetable = $("#TimeTable tbody");
    timetable.children().each(function (row) { // iterate over <tr>s
        $(this).children().each(function (col) { // iterate over <td>s
            $(this).data('row', row);
            $(this).data('col', col);
        });
    });

    var courseId;
    var classType;
    var avail_class_list;


    //  this will gray out all the available timeslot
    $('.sidebar_classes').on('click',function(){
        courseId = this.id.split('|')[0]
        classType = this.id.split('|')[1]

        $.get("/class_search/",{
            courseId: courseId,
            classType: classType,
        }, function (data) {
            avail_class_list = data.avail_class_list;
            console.log(avail_class_list);
            
            function class_on_timetable (col,row) {
                var i;
                var r = (row + 8) * 100;
                for (i = 0; i < avail_class_list.length; i++)
                    if(avail_class_list[i]['day'] == col-1 &&
                        avail_class_list[i]['timeFrom'] <= r &&
                        avail_class_list[i]['timeTo'] > r)
                        return true;
                return false;
            }

            // the course and the class type from the sublinks
            // alert(courseId+" , "+classType);
            timetable.children().each(function (row){
                $(this).children().each(function (col){
                    if(class_on_timetable(col,row)){
                        $(this).addClass('tableClassSelectingAvail');
                    } else {
                        $(this).addClass('tableClassSelectingNotAvail');
                    }
                });
            });
        }); 

    });

    // Locate which box we clicked on
    timetable.find('td').click(function () {
        var row = $(this).data('row');
        var col = $(this).data('col');
        if($(this).hasClass('tableClassSelectingAvail') && !$(this).hasClass('hassClass')){
            $(this).addClass('hasClass');
            $(this).html(courseId+"<p>"+classType);
        }

        // remove all the select class tag
        $('td').removeClass('tableClassSelectingAvail');
        $('td').removeClass('tableClassSelectingNotAvail');
        // alert("You clicked on row " + row + ", col " + col);
    });
});