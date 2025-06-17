from django.shortcuts import render
from rest_framework.views import APIView
from .models import TeacherProfile,AssignmentTask
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.db.models import Q
from student.models import StudentProfile,AssignmentSubmission
from rest_framework.viewsets import ModelViewSet 
from adminuser .models import Course,Chapter,Subject,Lesson
from rest_framework import status
from account.permissions import IsTeacher

from adminuser.serializers import CourseSerializer,SubjectSerializer,ChapterSerializer,LessonSerializer

# teacher can view and update their profile

from . serializers import TeacherProfileSerislizer

class TeacherPrifileView(APIView):
    permission_classes=[IsTeacher]
    def get(self,request):
        print("**** teacher profile get====")
        teacher_data=TeacherProfile.objects.filter(user=request.user).first()
        if teacher_data is None:
            return Response("no data found")
        ser=TeacherProfileSerislizer(teacher_data)
        return Response(ser.data,status=status.HTTP_200_OK)
    def patch(self,request):
        teacher_data=TeacherProfile.objects.get(user=request.user)  
        ser=TeacherProfileSerislizer(teacher_data,data=request.data,partial=True,context={'request':request})
        if ser.is_valid():
            ser.save()
            return Response({"data":ser.data,"message": "profile updated successfully"}, status=status.HTTP_200_OK)
        return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)



# assignment task for teacher
from .serializers import TaskSerializer
        
class TaskTeacherView(ModelViewSet):
    serializer_class=TaskSerializer
    permission_classes=[IsTeacher]

    def get_queryset(self):
        queryset=AssignmentTask.objects.all()
        keyword=self.request.GET.get('task',None)
        if keyword:
            queryset=AssignmentTask.objects.filter(Q(task_name__istartswith=keyword)| Q(students__full_name__istartswith=keyword))
        return queryset
from adminuser.serializers import ChapterSerializer    
class ChapterTeacherView(APIView):
    def get(self,request):
        k=Chapter.objects.all()
        ser=ChapterSerializer(k, many=True)
        return Response(ser.data)

# recorded lesson
from adminuser.serializers import LessonSerializer

class LessonTeacherView(ModelViewSet):
    
    serializer_class=LessonSerializer
    permission_classes=[IsTeacher]

    def get_queryset(self):
        chapter_id=self.request.GET.get('chapterId')
        # lesson_id=self.request.GET.get('lessonId')
        if chapter_id:
            queryset=Lesson.objects.filter(chapter=chapter_id)
        # elif lesson_id:
        #     queryset=Lesson.objects.get(id=lesson_id) 
        else:
            queryset=Lesson.objects.all()       
        return queryset


 

# assignmen submission teacher view, and update mark
from student.serializers import AssignmentSubmissionSerializer


class SubmissionTeacherView(APIView):
    permission_classes=[IsTeacher]
    def get(self,request):
        print("get=1")
        keyword=request.GET.get('submission')
        submission_id=request.GET.get('submissionId')
        print("get=2")
        if keyword:
            print("get=3")
            submitted_data=AssignmentSubmission.objects.filter(Q(student__full_name__istartswith=keyword) | Q(assignment__task_name__istartswith=keyword))
            ser=AssignmentSubmissionSerializer(submitted_data,many=True)
        elif submission_id:
            print("get=4")
            submitted_data=AssignmentSubmission.objects.get(id=submission_id)
            ser=AssignmentSubmissionSerializer(submitted_data)    
        else:
            print("get=5")
            submitted_data=AssignmentSubmission.objects.all()
            ser=AssignmentSubmissionSerializer(submitted_data,many=True)
        return Response(ser.data,status=status.HTTP_200_OK)
    def put(self,request):
        k=request.data
        print("1")
        id_=request.GET.get('taskId')
        print("2")
        if id_ is None:
            print("3")
            return Response("id must be requierd")
        try:
            print("4")
            m=AssignmentSubmission.objects.get(id=id_)
            print("5")
        except AssignmentSubmission.DoesNotExist:
            print("6")
            return Response("no data found") 
        print("taskid--=",id_)   
        print("7")
        ser=AssignmentSubmissionSerializer(m,k,partial=True, context={'request': request})
        print("8")
        if ser.is_valid():
            ser.save()
            return Response({"data":ser.data,"message": "mark updated successfully"}, status=status.HTTP_200_OK)
        return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)
    

from student.serializers import StudentProfileSerializer
class UsersListTeacherView(APIView):
    def get(self,request):
        user_=StudentProfile.objects.all()
        ser=StudentProfileSerializer(user_,many=True)
        return Response(ser.data)
 


from adminuser.serializers import CourseSerializer
class CourseTeacherView(APIView):
    permission_classes=[IsTeacher]
    def get(self,request):
        course_id=request.GET.get('courseId')
        if course_id:
            course=Course.objects.get(id=course_id)
            ser=CourseSerializer(course)
        else:
            course=Course.objects.all()
            ser=CourseSerializer(course,many=True)
        return Response(ser.data)



class TeacherSubjectView(APIView):
    permission_classes=[IsTeacher]
    def get(self,request):
        subject_id=request.GET.get('subjectId')
        course_id=request.GET.get('courseId')
        if subject_id:
            print("in if")
            subject=Subject.objects.get(id=subject_id)
            ser=SubjectSerializer(subject)
        elif course_id:
            subject=Subject.objects.filter(course=course_id)
            ser=SubjectSerializer(subject, many=True)            
        else:  
            subject=Subject.objects.all()
            ser=SubjectSerializer(subject, many=True)
        return Response(ser.data)
    


class TeacherChapterView(APIView):
    permission_classes=[IsTeacher]    
    def get(self,request):
        subject_id=request.GET.get('subjectId')
        chapter_id=request.GET.get('chapterId')
        print('subjece_id=',subject_id)
        print('chapter_id=',chapter_id)
        # chapter=Chapter.objects.filter(subject__course=student_course)
        if subject_id:
            chapter=Chapter.objects.filter(subject=subject_id)
            ser=ChapterSerializer(chapter, many=True)
        elif chapter_id:    
            chapter=Chapter.objects.get(id=chapter_id)
            ser=ChapterSerializer(chapter)
        else:
            chapter=Chapter.objects.all()
            ser=ChapterSerializer(chapter, many=True)
        return Response(ser.data)     