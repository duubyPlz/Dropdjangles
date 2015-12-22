$(function(){

    var current_friend_list  = [];
    var current_pending_list = [];
    var current_waiting_list = [];

    setInterval(refresh_all_friend_list,2000);

    function refresh_all_friend_list() {
        refresh_friend_list();
        refresh_pending_friend_list();
        refresh_waiting_friend_list();
    }

    $('body aside.sidebar-right-collapse').on('click', 'ul#friend_list.list-group.sidebar_friendlist li.list-group-item div.fluid-container div.row button',
        function(){
            remove_friend_from_sidebar($(this).val());
        }
    );

    function remove_friend_from_sidebar(username) {
        console.log('remove_friend: '+username);
        $.post('/remove_friend/',
            {
                'rm_friend_username' : username,
            },
            function (data){
                console.log("Exit Status: "+data.exit_status);
            }
        );
    }

    $('body div#addFriendModal div.form-group button').on('click',
        function(){
            add_friend($(this).parent().find('input').val());
            $(this).parent().find('input').val('');
        }
    );

    function add_friend (query_text) {
        $.post('/add_friend/',
            {
                'friend_username' : query_text,
            },
            function (data){
                console.log("Add Friend: "+query_text);
                console.log("Exit Status: "+data.exit_status);
            }
        );
    }

    $('body aside.sidebar-right-collapse ul#pending_list.list-group.sidebar_friendlist').on('click',
        'li.list-group-item button.accept_button',
        function(){
            console.log("accept friend request: "+$(this).val());
            accept_friend_request($(this).val());
        }
    );
    function accept_friend_request (username) {
        $.post('/accept_friend_request/',
            {
                'friend_username' : username,
            },
            function(data) {
                console.log("Accept Friend Request, Exit Status: "+data.exit_status);
            }
        );
    }

    $('body aside.sidebar-right-collapse ul#pending_list.list-group.sidebar_friendlist').on('click',
        'li.list-group-item button.deny_button',
        function(){
            console.log("deny friend request: "+$(this).val());
            deny_friend_request($(this).val());
        }
    );
    function deny_friend_request (username) {
        $.post('/deny_friend_request/',
            {
                'friend_username' : username,
            },
            function(data) {
                console.log("Deny Friend Request, Exit Status: "+data.exit_status);
            }
        );
    }




    function refresh_friend_list() {
        $.post('/get_friend_list/',{},
            function (data) {
                console.log("Friend list: "+data.friend_list);
                console.log(current_friend_list);
                var friend_list = data.friend_list;
                var list = $('body aside.sidebar-right-collapse ul.list-group.sidebar_friendlist#friend_list');
                for(var i = 0; i < current_friend_list.length; i++){
                    if($.inArray(current_friend_list[i],friend_list) < 0){
                        // remove friend from sidebar
                        list.find('li.list-group-item#'+current_friend_list[i]).remove();
                        current_friend_list.splice(i,1);
                    }
                }
                for(var i = 0; i < friend_list.length;i++) {
                    if($.inArray(friend_list[i],current_friend_list) < 0){
                        list.find('li.h4.list-group-item.active').after("\
                            <li class='list-group-item' id='"+friend_list[i]+"'> \
                              <div class='fluid-container'> \
                                <div class='row'> \
                                  <div class='col-xs-9'> \
                                    <button type='submit' class='not-focusable btn btn-xs btn-link' value='"+friend_list[i]+"' name='rm_friend'> \
                                      <span class='glyphicon glyphicon-remove' aria-hidden='true'></span> \
                                    </button> \
                                    "+friend_list[i]+" \
                                  </div> \
                                  <div class='col-xs-3'> \
                                    <input type='checkbox' name='friend' value='"+friend_list[i]+"'> \
                                  </div> \
                                </div> \
                              </div> \
                            </li> \
                        ");
                        current_friend_list.push(friend_list[i]);
                    }
                }
            }
        );
    }

    function refresh_pending_friend_list() {
        $.post('/get_pending_friend_list/',{},
            function (data) {
                // console.log("pending: "+data.pending_friend_list);
                // console.log("curr pending: "+current_pending_list);
                var pending_list = data.pending_friend_list;
                var list = $('body aside.sidebar-right-collapse ul#pending_list.list-group.sidebar_friendlist');
                if (pending_list.length > 0) {
                    list.find('li').slideDown('fast');
                } else {
                    list.find('li').slideUp('fast');
                }
                for(var i = 0; i < current_pending_list.length; i++){
                    if($.inArray(current_pending_list[i],pending_list) < 0){
                        // remove friend from sidebar
                        list.find('li.list-group-item#'+current_pending_list[i]).remove();
                        current_pending_list.splice(i,1);
                    }
                }
                for(var i = 0; i < pending_list.length;i++) {
                    if($.inArray(pending_list[i],current_pending_list) < 0){
                        // alert("added penging friend: "+pending_list[i]);
                        list.find('li.h4.list-group-item.active').after(" \
                          <li class='list-group-item' id='"+pending_list[i]+"'> \
                            <div class='fluid-container'> \
                              <div class='row'> \
                                "+pending_list[i]+" \
                                <div class='pull-right'> \
                                  <button type='submit' class='btn btn-xs btn-link not-focusable accept_button' value='"+pending_list[i]+"'' name='accept_request'> \
                                    <span class='glyphicon glyphicon-ok' aria-hidden='true'></span> \
                                  </button> \
                                  <button type='submit' class='btn btn-xs btn-link not-focusable deny_button' value='"+pending_list[i]+"' name='deny_request'> \
                                    <span class='glyphicon glyphicon-remove' aria-hidden='true'></span> \
                                  </button> \
                                </div> \
                              </div> \
                            </div> \
                          </li> \
                        ");
                        current_pending_list.push(pending_list[i]);
                    }
                }
            }
        );
    }

    function refresh_waiting_friend_list() {
        $.post('/get_waiting_friend_list/',{},
            function (data){
                // console.log("waiting: "+data.waiting_on_list);
                // console.log(current_waiting_list);
                var waiting_on_list = data.waiting_on_list;

                var list = $('body aside.sidebar-right-collapse ul#waiting_list.list-group.sidebar_friendlist');
                if (waiting_on_list.length > 0) {
                    list.find('li').slideDown('fast');
                } else {
                    list.find('li').slideUp('fast');
                }
                for(var i = 0; i < current_waiting_list.length; i++){
                    if($.inArray(current_waiting_list[i],waiting_on_list) < 0){
                        // remove friend from sidebar
                        list.find('li.list-group-item#'+current_waiting_list[i]).remove();
                        current_waiting_list.splice(i,1);
                    }
                }
                for(var i = 0; i < waiting_on_list.length; i++) {
                    if($.inArray(waiting_on_list[i],current_waiting_list) < 0){
                        // alert("added waiting friend: "+waiting_on_list[0]);
                        list.find('li.h4.list-group-item.active').after(" \
                            <li class='list-group-item' id='"+waiting_on_list[i]+"'> \
                              <div class='fluid-container'> \
                                <div class='row'> \
                                  <div class='col-xs-11'> \
                                    "+waiting_on_list[i]+" \
                                  </div> \
                                </div> \
                              </div> \
                            </li> \
                        ");
                        current_waiting_list.push(waiting_on_list[i]);
                    }
                }
            }
        );
    }
})