// works with table.css

/*
timetable.js TODO

save added class to backend
cancel gray

add grid to available class (for 2-3 hours class)

merge cell by colspan=“2” or rowspan

move class to a different time

remove class from timetable

class colouring


display all class on timetable_class at start


auto refresh every two second

*/

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
                    if(class_on_timetable(col,row) && col != 0){
                        $(this).addClass('tableClassSelectingAvail');
                    } else if (col != 0) {
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
        // alert("col:"+col+"row:"+row+" is clicked");
        var index = which_index(col, row);
        var hours = class_hours(index);
        var i;
        for (i=0; i < hours; i++) {
            var curr_row = row + i;
            var cell = $('#TimeTable tbody tr').eq(curr_row).find('td').eq(col);
            if(cell.hasClass('tableClassSelectingAvail') && !cell.hasClass('hasClass')){
                cell.addClass('hasClass');
                cell.html("<center><b>" + courseId + "</b><br>" +classType+"</center>");
            }
        }
        // alert("col-1:"+(col-1)+",day:"+avail_class_list[index]['day']);
        add_class_to_backend(courseId,classType,col-1,avail_class_list[index]['timeFrom']);

        // remove all the select class tag
        $('td').removeClass('tableClassSelectingAvail');
        $('td').removeClass('tableClassSelectingNotAvail');
    });

    function add_class_to_backend (courseId,classType,day,timeFrom) {
        $.post("/class_add/",{
            courseId: courseId,
            classType: classType,
            day: day,
            timeFrom: timeFrom,
        });
        // var data = {
        //     'courseId': courseId,
        //     'classType': classType,
        //     'day': day,
        //     'timeFrom': timeFrom,
        // };
        // $.ajax({
        //     "type": "POST",
        //     "dataType": "json",
        //     "url": "/class_add/",
        //     "data": data,
        //     "success": function (result) {
        //         console.log(result);
        //     },
        // })
    }

    function which_index(col, row) {
        var timeFrom = (row + 9) * 100;
        var day = col - 1;
        var i;
        // alert("which_index: checking: timeFrom:"+timeFrom+",day:"+day);
        for (i = 0; i < avail_class_list.length; i++) {
            // alert("which_index: checking: "+avail_class_list[i]['day']+"-"+avail_class_list[i]['timeFrom']);
            if (parseInt(avail_class_list[i]['day']) == day
               && parseInt(avail_class_list[i]['timeFrom']) == timeFrom) {
                return i;
            }
        }
        return -1;
    }

    function class_on_timetable (col,row) {
        var i;
        var r = (row + 9) * 100;
        for (i = 0; i < avail_class_list.length; i++) {
            if(avail_class_list[i]['day'] == col-1 &&
                avail_class_list[i]['timeFrom'] <= r &&
                avail_class_list[i]['timeTo'] > r)
                return true;
        }
        return false;
    }

    function class_hours(index) {
        return Math.ceil((parseInt(avail_class_list[index]['timeTo']) - parseInt(avail_class_list[index]['timeFrom'])) / 100);
    }
});