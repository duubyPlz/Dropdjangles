$(function(){
    $('body aside.sidebar-left-collapse div.sidebar-links').on("mouseover",".link-yellow",
        function(){
            $(this).addClass('selected');
        }
    );
    $('body aside.sidebar-left-collapse div.sidebar-links').on("mouseout",".link-yellow",
        function(){
            $(this).removeClass('selected');
        }
    );

    // add course to list
    $('body .sidebar-left-collapse .input-group.margin .btn.btn-default.not-focusable').on('click',
        function() {
            var required_course_code = $(this).parent().parent().find('input').val().toUpperCase();
            $.get("/course_add/",{
                'required_course_code': required_course_code,
            }, function (data) {
                // console.log(data);
                console.log("add course to list");
                var sidebar_links = $('body aside.sidebar-left-collapse div.sidebar-links');
                var classes_sublinks = "";
                for (var i = 0; i < data.class_types.length; i++){   
                    console.log("adding"+ data.class_types[i]);     
                    classes_sublinks = classes_sublinks +"<li style='cursor: move;' class='sidebar_classes draggable' id='"+required_course_code+"|"+data.class_types[i]+"'>"+data.class_types[i]+"</li>";
                }
                if(data.valid) {
                    sidebar_links.append(" \
                        <div class='link-yellow'> \
                            <a style='cursor: default;'> \
                                <div class='sidebar_remove_btn'> \
                                    <span class='sidebar_course_code'>"+required_course_code+"</span> \
                                    <button type='button' class='btn btn-xs btn-link not-focusable' name='rm_course'> \
                                        <span class='glyphicon glyphicon-remove' aria-hidden='true'></span> \
                                    </button> \
                                </div> \
                            </a> \
                            <ul class='sub-links'> \
                              "+classes_sublinks+" \
                            </ul> \
                        </div>");
                }
            });
            $(this).parent().parent().find('input').val('');
        }
    );


    // remove a course
    $('body .sidebar-left-collapse .sidebar-links ').on('click','div.link-yellow a .sidebar_remove_btn .btn.btn-xs.btn-link.not-focusable',
        function() {
            var required_course_code = $(this).siblings()[0].innerHTML;
            var obj = $(this);
            $("#TimeTable tbody tr").find('td.hasClass').each(function() {
                if ($(this).children().children()[0]) {
                    var current_course_code = $(this).children().children()[0].innerHTML;
                    console.log($(this).children().children()[0]);
                    console.log($(this).children().children()[0].innerHTML);
                    if (current_course_code == required_course_code) {
                        $(this).find('div.remove_class').trigger('click');
                    }
                }
            });
            // console.log(classes);

            // var i;
            // for (i=0; i<classes.length; i++) {
            // //     if (obj.hasClass('hasClass') && ($(this).find('b').innerHTML == )) {
            // //         console.log('asdf');
            // //         console.log(obj.data('class_info'));
            // //     }
            // }
            // if hasClass then get row & col & remove, for all td's
            // $(this).parent().parent().parent().parent().remove();
            $.get("/course_remove/", {
                'required_course_code': required_course_code,
            }, function (data) {
                // remove link-yellow
                if (data.exit_code == 1) {
                    obj.parent().parent().parent().remove();
                }
            })
        }
    );
})