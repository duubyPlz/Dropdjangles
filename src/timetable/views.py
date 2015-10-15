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
    timetable = usr_profile.timetable
    if timetable is None:
        timetable = Timetable.objects.create(name=usr_profile.user.username+"'s 15s2")
        usr_profile.timetable = timetable
        usr_profile.save()


    # find the course instance and add the course to the timetable
    if request.POST.get("course_code"):
        course_code = request.POST.get("course_code").upper()
        for course in Course.objects.raw("SELECT * FROM timetable_course WHERE name=%s",[course_code]):
            if course in timetable.courses.all():
                timetable.courses.add(course)
            timetable.save()

    if request.POST.get("rm_course"):
        course_code = request.POST.get("rm_course_code").upper()
        for course in Course.objects.raw("SELECT * FROM timetable_course WHERE name=%s",[course_code]):
            # print course
            timetable.courses.remove(course)
            timetable.save()
    

    
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
    
    if request.POST.get("friend_search"):
        #scrap the friend_text string for either username or password
        friend_text = request.POST.get("friend_search")        
        friend_text = friend_text.rstrip()

        #get friend from given friend_search text
        friendUser = None
        for usr in User.objects.raw("SELECT * FROM auth_user WHERE username LIKE %s",[friend_text]):
            friendUser = usr         
            break

        #add friendUser to currUser if they exist
        if (friendUser is not None):
            #get this friend's user profile
            friendUserProfile = friendUser.profile
            friendUserProfile.pending_friends.add(usr_profile)
            friendUserProfile.save()



    # Get all the courses from the user's timetable
    timetableCourses = timetable.courses.all()
    # Get all the class from the courses
    class_list = []
    exist_classtype = []
    for course in timetableCourses:
        for c in Class.objects.raw("SELECT * FROM timetable_class WHERE name=%s",[course.name]):
            if not c.classtype in exist_classtype:
                class_list.append(c)
                exist_classtype.append(c.classtype)

    friend_list = usr_profile.friends.all()
    pending_friend_list = usr_profile.pending_friends.all()

    context = {
        'course_list': course_list,
        'timetableCourses': timetableCourses,
        'class_list': class_list,
        'friend_list': friend_list,
        'pending_friend_list': pending_friend_list,
    }
    return render(request, 'main.html' ,context)

@csrf_exempt
def class_search(request):
    # Require user to login inorder to continue
    if not request.user.is_authenticated():
        return login(request)
    context = {}
    if request.method == 'GET' :
        course_name = request.GET['courseId'].upper()
        class_type = request.GET['classType']
        
        avail_class_list = []
        for c in Class.objects.raw("SELECT * FROM timetable_class WHERE name=%s AND classtype=%s",[course_name,class_type]):
            avail_class_list.append(c.as_dict())
        
        context = {
            'avail_class_list' : avail_class_list,
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
        # print "input: courseId:%s,classType:%s,day:%s,timeFrom:%s" % (course_name, class_type, day, time_from)
        require_class = None
        for c in Class.objects.raw("SELECT * FROM timetable_class WHERE name=%s AND classtype=%s",[course_name,class_type]):
            if(int(c.timeFrom) == int(time_from) and int(c.day) == int(day)):
                require_class = c
        timetable = request.user.profile.timetable
        if require_class in timetable.classes.all():
# INSERT HERE: DONT ADD IF EXIST
# example
# self.apps.filter(id=app_id).exists()

            timetable.classes.add(require_class)


        timetable.save()
    return JsonResponse({})

@csrf_exempt
def class_remove(request):
#     # Require user to login inorder to continue
#     if not request.user.is_authenticated():
#         return login(request)
#     if request.method == 'POST':
#         course_name = request.POST['courseId'].upper()
#         class_type = request.POST['classType']
#         day = request.POST['day']
#         timeFrom = request.POST['timeFrom']
#         wanted_class
#         for c in Class.objects.raw("SELECT id FROM timetable_class() WHERE name=%s AND classtype=%s AND day=%d AND timeFrom=%d",[course_name,class_type,day,timeFrom]):
#             wanted_class = c
    return JsonResponse({})

@csrf_exempt
def login(request):
    if request.user.is_authenticated():
        return timetable(request)
    return render(request, 'custom_login.html', {})






