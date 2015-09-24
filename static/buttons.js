
$(document).ready(function(){
    $("#addCourse").click(function(){
        {{ c = CourseInstance.objects.create(Course.objects.get(name='COMP1917'),Timetable.objects.get(id=1)) }}
    });
});
