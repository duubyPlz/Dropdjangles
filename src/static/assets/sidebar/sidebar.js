$(function(){
    // $('.link-yellow').on('mouseover',self,
    //     function(){
    //         $(this).addClass('selected');
    //     }
    // ); 
    // $('.link-yellow').on('mouseout',self,
    //     function(){
    //         $(this).removeClass('selected');
    //     }
    // );


    // $('.link-yellow').on({
    //     mouseenter: function () {
    //         $(this).addClass('selected');
    //     },
    //     mouseleave: function () {
    //         $(this).removeClass('selected');
    //     }    
    // });


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


    $('body .sidebar-left-collapse .input-group.margin .btn.btn-default.not-focusable').on('click',
        function() {
            var required_course_code = $(this).parent().parent().find('input').val().toUpperCase();
            $.get("/course_add/",{
                'required_course_code': required_course_code,
            }, function (data) {
                // console.log(data);
                var sidebar_links = $('body aside.sidebar-left-collapse div.sidebar-links');
                console.log(sidebar_links);
                var classes_sublinks = "";
                for (var i = 0; i < data.class_types.length; i++){        
                    classes_sublinks = classes_sublinks +"<li class='sidebar_classes' id="+required_course_code+"|"+data.class_types[i]+">"+data.class_types[i]+"</li>";
                }
                if(data.class_types.length > 0) {
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
        }
    );



})