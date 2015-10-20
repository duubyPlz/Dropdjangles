// works with table.css

/*
timetable.js TODO
=========================

add grid to available class (for 2-3 hours class)

move class to a different time

class colouring

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
    var streams = [];

    // load all class when the page is loaded
    $.get("/get_all_class/",{},function (data) {
        for(var i = 0; i < data.all_class.length; i++) {
            // alert("col:"+col+",row:"+row+",courseId:"+courseId+",classType:"+classType+",hours:"+hours);
            add_class_to_timetable(data.all_class[i]);
        }
    }); 

    //  this will gray out all the available timeslot
    $('body aside.sidebar-left-collapse div.sidebar-links ').on('click','div.link-yellow ul.sub-links li.sidebar_classes',
        function(){
            courseId = this.id.split('|')[0]
            classType = this.id.split('|')[1]
            // console.log('clicked');
            // check if already greyed out
            if (timetable.find('td').hasClass('tableClassSelectingAvail')) {
                $('td').removeClass('tableClassSelectingAvail');
                $('td').removeClass('tableClassSelectingNotAvail');
            }

            $.get("/class_search/",{
                courseId: courseId,
                classType: classType,
            }, function (data) {
                // streams = data
                streams = data.streams;
                // console.log(data.streams);

                // the course and the class type from the sublinks
                // alert(courseId+" , "+classType);
                timetable.children().each(function (row){
                    $(this).children().each(function (col){
                        if(class_on_timetable(col,row,data.streams) && col != 0){
                            $(this).addClass('tableClassSelectingAvail');
                        } else if (col != 0) {
                            $(this).addClass('tableClassSelectingNotAvail');
                        }
                    });
                });
            }); 
        }
    );


    timetable.find('td').on('click','div.remove_class',function() {
        var row = $(this).parent().data('row');
        var col = $(this).parent().data('col');
        remove_class_all_stream_from_timetable(col,row);
        $(this).find('div.remove_class').data('clicked',true);
    });

    // Locate which box we clicked on
    timetable.find('td').click(function () {

        if($(this).find('div.remove_class').data('clicked') == true){
            $(this).find('div.remove_class').data('clicked',false);

            return;
        }



        var row = $(this).data('row');
        var col = $(this).data('col');
        // alert("col:"+col+"row:"+row+" is clicked");
        var me = $(this);
        // var cell = $('#TimeTable tbody tr').eq(row).find('td').eq(col);
        if($(this).hasClass('hasClass')){
            var class_info = $(this).data('class_info');
            // console.log(class_info);
            remove_class_all_stream_from_timetable(col,row);
            var sidebar_classes = $('body aside.sidebar-left-collapse div.sidebar-links div.link-yellow ul.sub-links li.sidebar_classes');
            // console.log(sidebar_classes)
            var target_class_courseId = class_info['name'];
            var target_class_classType = class_info['classtype'];
            sidebar_classes.each(function(){
                // console.log($(this));
                var curr_courseId = $(this).attr('id').split('|')[0];
                var curr_classType = $(this).attr('id').split('|')[1];
                if(target_class_courseId == curr_courseId && target_class_classType == curr_classType) {
                    $(this).trigger('click');
                }
            });
        } else if ($(this).hasClass('tableClassSelectingAvail')) {
            // var index = which_index(col, row);
            // var cell = $('#TimeTable tbody tr').eq(row).find('td').eq(col);
            var index_str = which_stream_index_from_col_row(streams,col,row);
            // console.log(index_str);
            // alert("index_str = "+index_str);
            var i = index_str.split('|')[0];
            var j = index_str.split('|')[1];
            $.get("/timetable_have_classtype_this_course/",
                {
                    'courseId':  streams[i][0]['name'],
                    'classType': streams[i][0]['classtype'],
                },
                function (data) {
                    if (data.have_this_classtype == 0) {
                        for (var k = 0; k < streams[i].length; k++){
                            // console.log(this_class);
                            add_class_to_timetable(streams[i][k]);
                            add_class_to_backend(streams[i][k]);
                        }
                    }
                }
            );

            // remove all the select class tag
            $('td').removeClass('tableClassSelectingAvail');
            $('td').removeClass('tableClassSelectingNotAvail');
        } else {
            $('td').removeClass('tableClassSelectingAvail');
            $('td').removeClass('tableClassSelectingNotAvail');   
        }
    });


    // friends
    $('.sidebar-right-collapse .sidebar_friendlist li div div label input').change(
    function(){
        if ($(this).is(':checked')) {
            var color_index = Math.floor((Math.random() * 100) + 1)%color_list.length;
            friend_username = $(this).val();

            $.get("/get_friends_classes/", {'friend_username' : friend_username}, function (data) {
                // console.log(data.friends_classes);
                overlay_friends_class(data.friends_classes, friend_username, color_index);
                $(this).addClass('friend_username_highlight');
                $(this).css("background-color","rgba("+color_list[color_index][1]+","+color_list[color_index][2]+","+color_list[color_index][3]+",0.7)")
            });  
        } else {
            friend_username = $(this).val();
            remove_friends(friend_username);
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
        cell.append("<div style='cursor: pointer;' class='remove_class pull-right'>&times;</div>");
        cell.append("<div style='cursor: default;'><b>" + courseId + "</b><br>" +classType+"</div>");
        for (var i = 1; i < hours; i++) {
            $('#TimeTable tbody tr').eq(row+i).find('td').eq(col).hide();
        }
    }

    function add_class_to_timetable (a_class) {
        // console.log(a_class);
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
        // cell.attr('rowspan',hours);
        cell.data('class_info',a_class);
        // cell.attr('id',courseId+"|"+classType+"|"+day+"|"+timeFrom+"|"+timeTo);
        cell.append("<div style='cursor: pointer;' class='remove_class pull-right'>&times;</div>");
        cell.append("<div style='cursor: default;'><b>" + courseId + "</b><br>" +classType+"</div>");
        for (var i = 1; i < hours; i++) {
            cell = $('#TimeTable tbody tr').eq(row+i).find('td').eq(col);
            cell.addClass('hasClass');
            $(cell).attr('style', 'border-top-width: 2px; border-top-color: #e8c447');
        }
    }

    function add_friend_class_to_timetable (a_class,friend_username,color_index) {
        // console.log(a_class);
        var col =       which_col(a_class);
        var row =       which_row(a_class);
        var hours =     class_hours(a_class);
        var timeFrom =  a_class['timeFrom'];
        var timeTo =    a_class['timeTo'];
        var day =       a_class['day'];
        var classType = a_class['classtype'];
        var courseId =  a_class['name'];
        var cell = $('#TimeTable tbody tr').eq(row).find('td').eq(col);
        // cell.addClass('hasFriendClass');
        // cell.attr('rowspan',hours);
        cell.data('friend_class_info',a_class);
        // cell.attr('id',courseId+"|"+classType+"|"+day+"|"+timeFrom+"|"+timeTo);
        // cell.append("<div style='cursor: pointer;' class='remove_class pull-right'>&times;</div>");
        // cell.append("<div style='cursor: default;'><b>" + courseId + "</b><br>" +classType+"</div>");
        for (var i = 0; i < hours; i++) {
            // console.log(i);
            // console.log(hours);
            cell = $('#TimeTable tbody tr').eq(row+i).find('td').eq(col);
            cell.append("<div class='hasFriendsClass friend_class_"+friend_username+"'></div>");
            // console.log('friend: ' + friend_username);
            cell.find('div.hasFriendsClass').css("background-color","rgba("+color_list[color_index][1]+","+color_list[color_index][2]+","+color_list[color_index][3]+",0.7)");
        }
    }

    function overlay_friends_class (class_list, friend_username, color_index) {
        for (var i = 0; i < class_list.length; i++) {
            var a_class = class_list[i];
            // console.log(a_class);
            var hours = class_hours(a_class);
            var col = which_col(a_class);
            var row = which_row(a_class);
            //  overlay the cell
            // console.log("rgba("+color_list[color_index][1]+","+color_list[color_index][2]+","+color_list[color_index][3]+",0.7)");
            add_friend_class_to_timetable(a_class,friend_username,color_index);
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

    function remove_friends (friend_username) {
        $('td').find('div.hasFriendsClass').each(function () {
            if ($(this).hasClass('friend_class_' + friend_username)) {
                // console.log('OK');
                $(this).remove();
            }
        })
    }

    // function remove_class_from_timetable (a_class) {
    //     var col = which_col(a_class);
    //     var row = which_row(a_class);
    //     var class_block = $('#TimeTable tbody tr').eq(row).find('td').eq(col);
    //     remove_class_from_backend(a_class);
    //     // check if we need to unspan the row
    //     var rowspan = (rowspan === undefined) ? class_block.attr('rowspan') : 1;
    //     // console.log(rowspan);
    //     for(var i = 1; i < rowspan; i++) {
    //        class_block.parent().parent().children().eq(row+i).find('td').eq(col).show(); 
    //     }
    //     // remove the whole original cell
    //     class_block.removeData('class_info');
    //     class_block.removeClass('hasClass');
    //     class_block.removeAttr('rowspan');
    //     class_block.find('div').remove();

    // }

    function remove_class_from_timetable (a_class) {
        var col = which_col(a_class);
        var row = which_row(a_class);
        var class_block = $('#TimeTable tbody tr').eq(row).find('td').eq(col);
        remove_class_from_backend(a_class);
        // check if we need to unspan the row
        // var rowspan = (rowspan === undefined) ? class_block.attr('rowspan') : 1;
        // console.log(rowspan);
        var hours = class_hours(a_class);
        for(var i = 1; i < hours; i++) {
            // class_block.parent().parent().children().eq(row+i).find('td').eq(col).show(); 
            class_block.parent().parent().children().eq(row+i).find('td').eq(col).removeClass('hasClass');
            class_block.parent().parent().children().eq(row+i).find('td').eq(col).removeAttr('style');
        }
        // remove the whole original cell
        class_block.removeData('class_info');
        class_block.removeClass('hasClass');
        class_block.removeAttr('style');
        class_block.removeAttr('rowspan');
        class_block.find('div').remove();

    }

    function remove_class_all_stream_from_timetable(col,row){
        var class_block = $('#TimeTable tbody tr').eq(row).find('td').eq(col);
        var class_info = class_block.data('class_info');
        remove_this_class_stream_from_timetable(class_info);
    }

    function remove_this_class_stream_from_timetable(class_info) {
        remove_class_from_timetable(class_info);
        $.get("/class_stream_search/",{
            courseId:  class_info['name'],
            classType: class_info['classtype'],
            timeFrom:  class_info['timeFrom'],
            day:       class_info['day'],
        }, function (data) {
            // console.log(data);
            for(var i = 0; i < data.stream.length; i++){
                var target_class = data.stream[i];
                remove_class_from_timetable(target_class);
            }
        });
    }


    function remove_class_from_backend (a_class) {
        $.post("/class_remove/",{
            courseId:  a_class['name'],
            classType: a_class['classtype'],
            day:       a_class['day'],
            timeFrom:  a_class['timeFrom'],
        });
    }

    // function which_index(col,row) {
    //     var timeFrom = (row + 9) * 100;
    //     var day = col - 1;
    //     // alert("which_index: checking: timeFrom:"+timeFrom+",day:"+day);

    //     for (var i = 0; i < streams.length; i++) {
    //         // alert("which_index: checking: "+class_list[i]['day']+"-"+class_list[i]['timeFrom']);
    //         if (parseInt(class_list[i]['day']) == day
    //            && parseInt(class_list[i]['timeFrom']) == timeFrom) {
    //             return i;
    //         }
    //     }
    //     return -1;
    // }

    function which_stream_index_from_col_row (streams,col,row) {
        var r = (row + 9) * 100;
        for (var i = 0; i < streams.length; i++) {
            for(var j = 0; j < streams[i].length; j++){

                if(streams[i][j]['day'] == col-1 && streams[i][j]['timeFrom'] <= r && streams[i][j]['timeTo'] > r){
                    return i+"|"+j;
                }
            }
        }
        return "-1|-1";
    }
    


    function which_col(a_class) {
        // console.log('col is '+parseInt(a_class['day'])+1);
        return parseInt(a_class['day'])+1;
    }

    function which_row (a_class) {
        // console.log('row is '+((parseInt(a_class['timeFrom'])/100) - 9));
        return (parseInt(a_class['timeFrom'])/100) - 9;
    }

    function class_on_timetable (col,row,streams) {
        var r = (row + 9) * 100;
        for (var i = 0; i < streams.length; i++) {
            for(var j = 0; j < streams[i].length; j++){ 
                if(streams[i][j]['day'] == col-1 &&
                    streams[i][j]['timeFrom'] <= r &&
                    streams[i][j]['timeTo'] > r)
                    return true;
            }
        }
        return false;
    }

    function class_hours(a_class) {
        return Math.ceil((parseInt(a_class['timeTo']) - parseInt(a_class['timeFrom'])) / 100);
    }

    var color_list = [
        ['5d8aa8',93,138,168],
        ['e32636',227,38,54],
        ['ffbf00',55,191,0],
        ['9966cc',153,102,204],
        ['8db600',141,182,0],
        ['f5f5dc',245,245,220],
        ['b2ffff',178,255,255]
    ];


});


