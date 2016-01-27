from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Course, Timetable, Class, UserProfile
from django.contrib.auth.models import User

from django.http import JsonResponse
from django.core import serializers

@csrf_exempt
def timetable(request):
    # Require user to login inorder to continue
    if not request.user.is_authenticated():
        return login(request)

    # Load the course list and class list
    course_list = Course.objects.order_by('name')
    # class_list = Class.objects.all()


    # Get the timetable from the user if there is one
    # Create one if it doesn't exist
    usr_profile = request.user.profile
    friend_list = usr_profile.friends.all()
    pending_friend_list = usr_profile.pending_friends.all()

    timetable = usr_profile.timetable
    if timetable is None:
        timetable = Timetable.objects.create(name=usr_profile.user.username+"'s 15s2")
        usr_profile.timetable = timetable
        usr_profile.save()


    # find the course instance and add the course to the timetable
    # if request.POST.get("course_code"):
    #     course_code = request.POST.get("course_code").upper()
    #     for course in Course.objects.raw("SELECT * FROM timetable_course WHERE name=%s",[course_code]):
    #         if course not in timetable.courses.all():
    #             timetable.courses.add(course)
    #         timetable.save()

    # if request.POST.get("rm_course"):
    #     course_code = request.POST.get("rm_course_code").upper()
    #     for course in Course.objects.raw("SELECT * FROM timetable_course WHERE name=%s",[course_code]):
    #         # print course
    #         timetable.courses.remove(course)
    #         timetable.save()
    

    
    #reject a friend request  
    if (request.POST.get("deny_request") or request.POST.get("accept_request")):
        requestingFriend = request.POST.get("respond_friend_code")
        friendUser = None      
        for usr in User.objects.raw("SELECT * FROM auth_user WHERE username LIKE %s",[requestingFriend]):
            friendUser = usr
            break
         
        if (friendUser is not None):
            friendUserProfile = friendUser.profile
            usr_profile.pending_friends.remove(friendUserProfile)

            #determine if we are accepting or denying, if accepting -> add eachother
            if request.POST.get("accept_request"):
                usr_profile.friends.add(friendUserProfile)    
                friendUserProfile.friends.add(usr_profile)
                friendUserProfile.save()
            usr_profile.save()
    
    if request.POST.get("rm_friend"):
        friendToRemove = request.POST.get("rm_friend_code")
        friendUser = None
        for usr in User.objects.raw("SELECT * FROM auth_user WHERE username LIKE %s",[friendToRemove]):
            friendUser = usr
            break

        if (friendUser is not None):
            friendUserProfile = friendUser.profile
            #remove from each user
            usr_profile.friends.remove(friendUserProfile)
            friendUserProfile.friends.remove(usr_profile)
            usr_profile.save()
            friendUserProfile.save()

    if request.POST.get("friend_search"):
        #scrap the friend_text string for either username or password
        friend_text = request.POST.get("friend_search")        
        friend_text = friend_text.rstrip()
        
        #check if you are trying to add yourself
        if (friend_text == usr_profile.user.username):
            friend_text=''
        #check if you are trying to add a friend
        for friend in usr_profile.friends.all():
            if (friend_text == friend.user.username):
                friend_text=''

        #get friend from given friend_search text
        friendUser = None
        for usr in User.objects.raw("SELECT * FROM auth_user WHERE username LIKE %s",[friend_text]):
            friendUser = usr         
            break
       
        #try email
        if (friendUser is None):
            for usr in User.objects.raw("SELECT * FROM auth_user WHERE email LIKE %s",[friend_text]):
                friendUser = usr
                break


        #add friendUser to currUser if they exist
        if (friendUser is not None):
            #get this friend's user profile
            friendUserProfile = friendUser.profile

            if friendUserProfile in usr_profile.pending_friends.all():
                usr_profile.pending_friends.remove(friendUserProfile)
                usr_profile.friends.add(friendUserProfile)
                friendUserProfile.friends.add(usr_profile)
                usr_profile.save()
                friendUserProfile.save()
            else:
                friendUserProfile.pending_friends.add(usr_profile)
            friendUserProfile.save()



    # Get all the courses from the user's timetable
    timetableCourses = timetable.courses.all()
    # Get all the class from the courses
    class_list = []
    for course in timetableCourses:
        exist_classtype = []
        for c in Class.objects.raw("SELECT * FROM timetable_class WHERE name=%s",[course.name]):
            if not c.classtype in exist_classtype:
                class_list.append(c)
                exist_classtype.append(c.classtype)
    
    #find what friends we are waiting for
    waiting_on_list = []
    for friend in UserProfile.objects.all():
        for friend_waiting in friend.pending_friends.all():
            if (friend_waiting.user.username == usr_profile.user.username):
                waiting_on_list.append(friend)

    context = {
        'course_list': course_list,
        'timetableCourses': timetableCourses,
        'class_list': class_list,
        'friend_list': friend_list,
        'pending_friend_list': pending_friend_list,
        'waiting_on_list': waiting_on_list,
    }
    return render(request, 'main.html' ,context)

@csrf_exempt
def add_friend(request):
    if not request.user.is_authenticated():
        return login(request)

    exit_status = 'Unknown'
    if request.method == 'POST' and request.POST:
        user_profile = request.user.profile
        # friend_list = usr_profile.friends.all()
        # pending_friend_list = usr_profile.pending_friends.all()

        friend_username = request.POST.get("friend_username")        
        friend_username = friend_username.rstrip()

        #check if you are trying to add yourself
        if friend_username == user_profile.user.username:
            context = { 'exit_status' : 'Fail to add youself as friend' }
            return JsonResponse(context)

        #check if you are trying to add a friend
        for friend_profile in user_profile.friends.all():
            if friend_username == friend_profile.user.username:
                context = { 'exit_status' : 'Fail to add your friend twice' }
            return JsonResponse(context)

        #get friend from given friend_username text
        friendUser = None
        for usr in User.objects.raw("SELECT * FROM auth_user WHERE username LIKE %s",[friend_username]):
            friendUser = usr         
            break
        #try email
        if (friendUser is None):
            for usr in User.objects.raw("SELECT * FROM auth_user WHERE email LIKE %s",[friend_username]):
                friendUser = usr
                break

        #add friendUser to currUser if they exist
        if (friendUser is not None):
            #get this friend's user profile
            friendUserProfile = friendUser.profile

            # if they both add each other
            if friendUserProfile in user_profile.pending_friends.all():
                user_profile.pending_friends.remove(friendUserProfile)
                print 1;
                if friendUserProfile not in user_profile.friends.all():
                    user_profile.friends.add(friendUserProfile)
                    user_profile.save()
                    print 2;
                    if user_profile not in friendUserProfile.friends.all():
                        friendUserProfile.friends.add(user_profile)
                        friendUserProfile.save()
                        print 3;
                        exit_status = 0
                    else:
                        exit_status = "user_profile is in friendUser_profile.friends"
                else:
                    exit_status = "friendUserProfile is in user_profile.friends, already friends"
            else:
                if user_profile not in friendUserProfile.pending_friends.all():
                    friendUserProfile.pending_friends.add(user_profile)
                    friendUserProfile.save()
                    exit_status = 0
                else:
                    exit_status = "user_profile is in friend user pending_friends"
        else:
            exit_status = "can't find friend user"

    context = { 'exit_status' : exit_status }
    return JsonResponse(context)

@csrf_exempt
def remove_friend (request):
    if not request.user.is_authenticated():
        return login(request)

    exit_status = 'Unknown'
    if request.method == 'POST' and request.POST:
        user_profile = request.user.profile
        friendToRemove = request.POST.get("rm_friend_username")
        friendUser = None
        for user in User.objects.raw("SELECT * FROM auth_user WHERE username LIKE %s",[friendToRemove]):
            friendUser = user
            break

        if (friendUser is not None):
            friendUserProfile = friendUser.profile
            #remove from each user
            if friendUserProfile in user_profile.friends.all():
                user_profile.friends.remove(friendUserProfile)
                user_profile.save()
                if user_profile in friendUserProfile.friends.all():
                    friendUserProfile.friends.remove(user_profile)
                    friendUserProfile.save()
                    exit_status = 0
                else:
                    exit_status = "user_profile is not in friendUserProfile"
            else:
                exit_status = "friendUserProfile is not in user_profile.friends"
        else:
            exit_status = "can't find friend user"

    context = { 'exit_status' : exit_status }
    return JsonResponse(context)


@csrf_exempt
def accept_friend_request (request):
    if not request.user.is_authenticated():
        return login(request)

    exit_status = "Unknown"
    if request.method == 'POST':
        user_profile = request.user.profile

        requestingFriend = request.POST.get("friend_username")
        friendUser = None      
        for user in User.objects.raw("SELECT * FROM auth_user WHERE username LIKE %s",[requestingFriend]):
            friendUser = user
            break
         
        if friendUser is not None:
            friendUserProfile = friendUser.profile
            if friendUserProfile in user_profile.pending_friends.all():
                user_profile.pending_friends.remove(friendUserProfile)
                user_profile.save()
                if friendUserProfile not in user_profile.friends.all():
                    user_profile.friends.add(friendUserProfile)
                    user_profile.save()
                    if user_profile not in friendUserProfile.friends.all():
                        friendUserProfile.friends.add(user_profile)
                        friendUserProfile.save()
                        exit_status = 0
                    else:
                        exit_status = "user is in friend's friends, already friends"
                else:
                    exit_status = "friendUserProfile is in user_profile.friends"
            else:
                exit_status = "friendUserProfile is not in user pending friends"
        else:
            exit_status = "friend user is None"
    context = { 'exit_status' : exit_status }
    return JsonResponse(context)



@csrf_exempt
def deny_friend_request (request):
    if not request.user.is_authenticated():
        return login(request)

    exit_status = "Unknown"
    if request.method == 'POST':
        user_profile = request.user.profile

        requestingFriend = request.POST.get("friend_username")
        friendUser = None      
        for user in User.objects.raw("SELECT * FROM auth_user WHERE username LIKE %s",[requestingFriend]):
            friendUser = user
            break
         
        if friendUser is not None:
            friendUserProfile = friendUser.profile
            if friendUserProfile in user_profile.pending_friends.all():
                user_profile.pending_friends.remove(friendUserProfile)
                user_profile.save()
                if friendUserProfile in user_profile.friends.all():
                    user_profile.friends.remove(friendUserProfile)
                    user_profile.save()
                    exit_status = "friendUserProfile is in user_profile.friends"
                    if user_profile in friendUserProfile.friends.all():
                        friendUserProfile.friends.remove(user_profile)
                        friendUserProfile.save()
                        exit_status = "user is in friend's friends, already friends"
                    else:
                        exit_status = 0
                else:
                    exit_status = 0
            else:
                exit_status = "friendUserProfile is not in user pending friends"
        else:
            exit_status = "friend user is None"
    context = { 'exit_status' : exit_status }
    return JsonResponse(context)

@csrf_exempt
def get_friend_list (request):
    context = {}
    if request.method == 'POST':
        all_friends = []
        for f in request.user.profile.friends.all():
            all_friends.append(f.as_string());
        context = {
            'friend_list' : all_friends,
        }
    return JsonResponse(context)

@csrf_exempt
def get_pending_friend_list (request):
    context = {}
    if request.method == 'POST':
        all_friends = []
        for f in request.user.profile.pending_friends.all():
            all_friends.append(f.as_string())
        context = {
            'pending_friend_list' : all_friends,
        }
    return JsonResponse(context)

@csrf_exempt
def get_waiting_friend_list (request):
    waiting_on_list = []
    if request.method == 'POST':
        user_profile = request.user.profile
        for friend_profile in UserProfile.objects.all():
            for friend_waiting in friend_profile.pending_friends.all():
                if (friend_waiting.user.username == user_profile.user.username):
                    waiting_on_list.append(friend_profile.as_string())
    context = {
        'waiting_on_list' : waiting_on_list,
    }
    return JsonResponse(context)


@csrf_exempt
def course_add(request):
    # Require user to login inorder to continue
    if not request.user.is_authenticated():
        return login(request)
 
    context = {}
    if request.method == 'GET' :
        course_code = request.GET['required_course_code'].upper()
        course_code = course_code.rstrip()
        course_code_valid = 0

        class_types = []
        for course in Course.objects.raw("SELECT * FROM timetable_course WHERE name=%s",[course_code]):
            if course not in request.user.profile.timetable.courses.all():
                # print "added course"
                request.user.profile.timetable.courses.add(course)
                request.user.profile.timetable.save()
                course_code_valid = 1

                for c in Class.objects.raw("SELECT * FROM timetable_class WHERE name=%s",[course_code]):
                    if c.classtype not in class_types:
                        class_types.append(c.classtype)

        context = {
            'valid' : course_code_valid,
            'class_types' :       class_types,
        }
    return JsonResponse(context)

@csrf_exempt
def course_remove(request):
    # Require user to login inorder to continue
    if not request.user.is_authenticated():
        return login(request)

    exit_code = 0
    if request.method == 'GET':
        course_code = request.GET['required_course_code'].upper()
        course_code = course_code.rstrip()

        for course in Course.objects.raw("SELECT * FROM timetable_course WHERE name=%s",[course_code]):
            if course in request.user.profile.timetable.courses.all():
                request.user.profile.timetable.courses.remove(course)
                request.user.profile.timetable.save()
                print ('asdf')
                exit_code = 1
    context = {
        'exit_code' : exit_code,
    }
    return JsonResponse(context)

@csrf_exempt
def class_search(request):
    # Require user to login inorder to continue
    if not request.user.is_authenticated():
        return login(request)
    context = {}
    if request.method == 'GET' :
        course_name = request.GET['courseId'].upper()
        class_type = request.GET['classType']
        
        all_class_list = []
        for c in Class.objects.raw("SELECT * FROM timetable_class WHERE name=%s AND classtype=%s",[course_name,class_type]):
            all_class_list.append(c)

        added_class = []
        streams = []
        for c in all_class_list:
            if c not in added_class:
                curr_stream_list = []
                curr_stream_list.append(c.as_dict())
                added_class.append(c)
                for shared_stream_class in c.shared_stream.all():
                    curr_stream_list.append(shared_stream_class.as_dict())
                streams.append(curr_stream_list)

        # print streams
        context = {
            'streams' : streams,
        }
    return JsonResponse(context)

@csrf_exempt
def class_stream_search(request):
    if not request.user.is_authenticated():
        return login(request)
    context = {}
    if request.method == 'GET' :
        course_name = request.GET['courseId'].upper()
        class_type = request.GET['classType']
        time_from = request.GET['timeFrom']
        day = request.GET['day']
        
        stream = []
        for c in Class.objects.raw("SELECT * FROM timetable_class WHERE name=%s AND classtype=%s AND time_from=%s AND day=%s",[course_name,class_type,time_from,day]):
            stream.append(c.as_dict())
            for shared_stream_class in c.shared_stream.all():
                stream.append(shared_stream_class.as_dict())
        context = {
            'stream' : stream,
        }
    return JsonResponse(context)

@csrf_exempt
def class_add(request):
    # Require user to login inorder to continue
    if not request.user.is_authenticated():
        return login(request)

    if request.method == 'POST':
        course_name = request.POST.get('courseId').upper()
        class_type = request.POST.get('classType')
        day = request.POST.get('day')
        time_from = request.POST.get('timeFrom')
        #print "input: courseId:%s,classType:%s,day:%s,timeFrom:%s" % (course_name, class_type, day, time_from)
        require_class = None
        for c in Class.objects.raw("SELECT * FROM timetable_class WHERE name=%s AND classtype=%s",[course_name,class_type]):
            if(int(c.time_from) == int(time_from) and int(c.day) == int(day)):
                require_class = c
        timetable = request.user.profile.timetable
        if require_class not in timetable.classes.all(): # class is already in timetable
            timetable.classes.add(require_class)

        timetable.save()
    return JsonResponse({})

@csrf_exempt
def class_remove(request):
    # Require user to login inorder to continue
    if not request.user.is_authenticated():
        return login(request)

    if request.method == 'POST':
        course_name = request.POST.get('courseId').upper()
        class_type = request.POST.get('classType')
        day = request.POST.get('day')
        time_from = request.POST.get('timeFrom')
        #print "input: courseId:%s,classType:%s,day:%s,timeFrom:%s" % (course_name, class_type, day, time_from)
        require_class = None
        for c in Class.objects.raw("SELECT * FROM timetable_class WHERE name=%s AND classtype=%s",[course_name,class_type]):
            if(int(c.time_from) == int(time_from) and int(c.day) == int(day)):
                require_class = c
        timetable = request.user.profile.timetable
        if require_class in timetable.classes.all(): # class is already in timetable
            timetable.classes.remove(require_class)
        timetable.save()
    return JsonResponse({})


@csrf_exempt
def get_all_class(request):
    if not request.user.is_authenticated():
        return login(request)
    context = {}
    if request.method == 'GET':
        all_class = []
        for c in request.user.profile.timetable.classes.all():
            all_class.append(c.as_dict())
        # print "get class ok"
        context = {
            'all_class' : all_class,
        }
    return JsonResponse(context)

@csrf_exempt
def get_friends_classes(request):
    if not request.user.is_authenticated():
        return login(request)
    context = {}
    if request.method == 'GET':
        all_classes = []
        friend_username = request.GET.get('friend_username')
        print (friend_username)
        for usr in User.objects.raw("SELECT * FROM auth_user WHERE username LIKE %s",[friend_username]):
            for c in usr.profile.timetable.classes.all():
                all_classes.append(c.as_dict())
                context = {
                    'friends_classes' : all_classes,
                }
            break
    return JsonResponse(context);

@csrf_exempt
def timetable_have_classtype_this_course(request):
    if not request.user.is_authenticated():
        return login(request)
    context = {}
    if request.method == 'GET':
        have_this_classtype = 0
        course_name = request.GET.get('courseId').upper()
        class_type = request.GET.get('classType')
        # print "hello"
        for c in request.user.profile.timetable.classes.all():
            if (c.name == course_name and class_type == c.classtype):
                have_this_classtype = 1
        context = {
            'have_this_classtype' : have_this_classtype,
        }
    return JsonResponse(context);


@csrf_exempt
def login(request):
    if request.user.is_authenticated():
        return timetable(request)
    return render(request, 'custom_login.html', {})

@csrf_exempt
def register(request):
    if request.user.is_authenticated():
        return timetable(request)
    return render(request, 'custom_register.html', {})

@csrf_exempt
def forgot_password(request):
    if request.user.is_authenticated():
        return timetable(request)
    return render(request, 'custom_forgot_password.html', {})






