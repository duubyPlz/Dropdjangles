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
        var index = which_index(col, row);
        var hours = class_hours(index);
        var i;
        for (i=0; i<hours; i++) {
            //alert(i + " " + hours);
            var curr_row = row + i;
            var cell = $('#TimeTable tbody tr').eq(curr_row).find('td').eq(col);

            if(cell.hasClass('tableClassSelectingAvail') && !cell.hasClass('hasClass')){
                cell.addClass('hasClass');
                cell.html(courseId + classType);
                //alert('cell: ' + cell.index() + ' this: ' + $(this).index());
            }
        }

        // remove all the select class tag
        $('td').removeClass('tableClassSelectingAvail');
        $('td').removeClass('tableClassSelectingNotAvail');
        // alert("You clicked on row " + row + ", col " + col);
    });

    function which_index(col, row) {
        var timeFrom = (row + 8) * 100;
        var day = col - 1;
        var i;
        for (i = 0; i < avail_class_list.length; i++) {
            if (avail_class_list[i]['day'] == day
             && avail_class_list[i]['timeFrom'] == timeFrom) {
                return i;
            }
        }
        return -1;
    }

    function class_on_timetable (col,row) {
        var i;
        var r = (row + 8) * 100;
        for (i = 0; i < avail_class_list.length; i++) {
            if(avail_class_list[i]['day'] == col-1 &&
                avail_class_list[i]['timeFrom'] <= r &&
                avail_class_list[i]['timeTo'] > r)
                return true;
        }
        return false;
    }

    function class_hours(index) {
        return Math.floor((avail_class_list[index]['timeTo'] - avail_class_list[index]['timeFrom']) / 100);
    }
});