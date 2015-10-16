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
        console.log(data.all_class);
        for(var i = 0; i < data.all_class.length; i++) {
            // alert("col:"+col+",row:"+row+",courseId:"+courseId+",classType:"+classType+",hours:"+hours);
            add_class_to_timetable(data.all_class[i]);
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
                    if(class_on_timetable(col,row,class_list) && col != 0){
                        $(this).addClass('tableClassSelectingAvail');
                    } else if (col != 0) {
                        $(this).addClass('tableClassSelectingNotAvail');
                    }
                });
            });
        }); 

    });
    

    // $('body').on('click',function (e) { 
    //     // alert('works: col:'+$(this).data('col')+",row:"+$(this).data('row'));
    // });


    // Locate which box we clicked on
    timetable.find('td').click(function () {
        var row = $(this).data('row');
        var col = $(this).data('col');
        // alert("col:"+col+"row:"+row+" is clicked");
        // var me = $(this);
        // var cell = $('#TimeTable tbody tr').eq(row).find('td').eq(col);
        if($(this).hasClass('hasClass')){
            // console.log("this is a class");
            $(this).children('div #remove_class').on('click',function() {
                // console.log("remove_class,col:"+col+",row:"+row);
                // console.log($(this).parent().data('class_info'));
                remove_class_from_timetable(col,row);
            });
        } else if ($(this).hasClass('tableClassSelectingAvail') && !$(this).hasClass('hasClass')) {
            var index = which_index(col, row);
            // var cell = $('#TimeTable tbody tr').eq(row).find('td').eq(col);
            add_class_to_timetable(class_list[index]);
            add_class_to_backend(class_list[index]);
            // alert("col-1:"+(col-1)+",day:"+class_list[index]['day']);

            // remove all the select class tag
            $('td').removeClass('tableClassSelectingAvail');
            $('td').removeClass('tableClassSelectingNotAvail');
        }
    });











    // Helper functions

    function add_class_to_timetable (a_class) {
            var col =       which_col(a_class);
            var row =       which_row(a_class);
            var hours =     class_hours(a_class);
            var timeFrom =  a_class['timeFrom'];
            var timeTo =    a_class['timeTo'];
            var day =       a_class['day'];
            var classType = a_class['classtype'];
            var courseId =  a_class['name'];
            var cell = $('#TimeTable tbody tr').eq(row).find('td').eq(col);
            cell.addClass('hasClass');
            cell.attr('rowspan',hours);
            cell.data('class_info',a_class);
            // cell.attr('id',courseId+"|"+classType+"|"+day+"|"+timeFrom+"|"+timeTo);
            cell.append("<div id='remove_class' style='cursor: pointer;float: right;margin-top:-13px;position: absolute;'>&times;</div>");
            cell.append("<div style='cursor: pointer;'><b>" + courseId + "</b><br>" +classType+"</div>");
            for (var i = 1; i < hours; i++) {
                $('#TimeTable tbody tr').eq(row+i).find('td').eq(col).hide();
            }
    }

    function add_class_to_backend (a_class) {
        $.post("/class_add/",{
            courseId:  a_class['name'],
            classType: a_class['classtype'],
            day:       a_class['day'],
            timeFrom:  a_class['timeFrom'],
        });
    }

    function remove_class_from_timetable (col,row) {
        console.log("removing from timetable");
        var class_block = $('#TimeTable tbody tr').eq(row).find('td').eq(col);
        // remove the class from backend
        remove_class_from_backend(class_block.data('class_info'));
        // check if we need to unspan the row
        var rowspan = (rowspan === undefined) ? class_block.attr('rowspan') : 1;
        console.log(rowspan);
        for(var i = 1; i < rowspan; i++) {
           class_block.parent().parent().children().eq(row+i).find('td').eq(col).show(); 
        }
        // remove the whole original cell
        class_block.removeData('class_info');
        class_block.removeClass('hasClass');
        class_block.removeAttr('rowspan');
        class_block.find('div').remove();
    }

    function remove_class_from_backend (a_class) {
        $.post("/class_remove/",{
            courseId:  a_class['name'],
            classType: a_class['classtype'],
            day:       a_class['day'],
            timeFrom:  a_class['timeFrom'],
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

    function which_col(a_class) {
        return parseInt(a_class['day'])+1;
    }

    function which_row (a_class) {
        return (parseInt(a_class['timeFrom'])/100) - 9;
    }

    function class_on_timetable (col,row,class_list) {
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

    function class_hours(a_class) {
        return Math.ceil((parseInt(a_class['timeTo']) - parseInt(a_class['timeFrom'])) / 100);
    }
});