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
    var class_list = [];

    // load all class when the page is loaded
    $.get("/get_all_class/",{},function (data) {
        class_list = data.all_class;
        // console.log(class_list);
        for(var i = 0; i < class_list.length; i++) {
            var row = (parseInt(class_list[i]['timeFrom'])/100)-9;
            var col = parseInt(class_list[i]['day'])+1;
            var courseId = class_list[i]['name'];
            var classType = class_list[i]['classtype'];
            var hours = class_hours(class_list,i);
            // alert("col:"+col+",row:"+row+",courseId:"+courseId+",classType:"+classType+",hours:"+hours);
            add_class_to_timetable(col,row,courseId,classType,hours);
        }
    }); 




    //  this will gray out all the available timeslot
    $('.sidebar_classes').on('click',function(){
        courseId = this.id.split('|')[0]
        classType = this.id.split('|')[1]

        $.get("/class_search/",{
            courseId: courseId,
            classType: classType,
        }, function (data) {
            class_list = data.avail_class_list;
            // console.log(class_list);
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
    

    $('body').on('click',function (e) { 
        // alert('works: col:'+$(this).data('col')+",row:"+$(this).data('row'));
    });



    // Locate which box we clicked on
    timetable.find('td').click(function () {
        var row = $(this).data('row');
        var col = $(this).data('col');
        // alert("col:"+col+"row:"+row+" is clicked");
        var me = $(this);
        var cell = $('#TimeTable tbody tr').eq(row).find('td').eq(col);
        if(cell.hasClass('hasClass')){
            console.log("this is a class");
        } else if (cell.hasClass('tableClassSelectingAvail') && !cell.hasClass('hasClass')) {
            var index = which_index(col, row);
            var hours = class_hours(class_list,index);
            // for (var i = 0; i < hours; i++) {
            // var curr_row = row + i;
            var cell = $('#TimeTable tbody tr').eq(row).find('td').eq(col);
            add_class_to_timetable(col,row,courseId,classType,hours);
            add_class_to_backend(courseId,classType,col-1,class_list[index]['timeFrom']);
            // alert("col-1:"+(col-1)+",day:"+class_list[index]['day']);

            // remove all the select class tag
            $('td').removeClass('tableClassSelectingAvail');
            $('td').removeClass('tableClassSelectingNotAvail');
        }
    });










    // Helper functions

    function add_class_to_timetable (col,row,courseId,classType,hours) {
            var cell = $('#TimeTable tbody tr').eq(row).find('td').eq(col);
            cell.addClass('hasClass');
            cell.attr('rowspan',hours);
            cell.append("<div id='remove_class' style='float: right;margin-top:-13px;position: absolute;'>&times;");
            cell.append("<b>" + courseId + "</b><br>" +classType+"</div>");
            for (var i = 1; i < hours; i++) {
                $('#TimeTable tbody tr').eq(row+i).find('td').eq(col).hide();
            }
    }

    function add_class_to_backend (courseId,classType,day,timeFrom) {
        $.post("/class_add/",{
            courseId: courseId,
            classType: classType,
            day: day,
            timeFrom: timeFrom,
        });
    }

    function which_index(col, row) {
        var timeFrom = (row + 9) * 100;
        var day = col - 1;
        var i;
        // alert("which_index: checking: timeFrom:"+timeFrom+",day:"+day);
        for (i = 0; i < class_list.length; i++) {
            // alert("which_index: checking: "+class_list[i]['day']+"-"+class_list[i]['timeFrom']);
            if (parseInt(class_list[i]['day']) == day
               && parseInt(class_list[i]['timeFrom']) == timeFrom) {
                return i;
            }
        }
        return -1;
    }

    function class_on_timetable (col,row) {
        var i;
        var r = (row + 9) * 100;
        for (i = 0; i < class_list.length; i++) {
            if(class_list[i]['day'] == col-1 &&
                class_list[i]['timeFrom'] <= r &&
                class_list[i]['timeTo'] > r)
                return true;
        }
        return false;
    }

    function class_hours(class_list,index) {
        return Math.ceil((parseInt(class_list[index]['timeTo']) - parseInt(class_list[index]['timeFrom'])) / 100);
    }
});