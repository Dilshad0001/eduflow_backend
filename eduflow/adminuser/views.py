from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework.viewsets import ModelViewSet
from student.models import StudentProfile
from rest_framework.response import Response
from teacher.models import TeacherProfile
from .models import Course,Subject,Chapter,Lesson
from rest_framework.permissions import AllowAny,IsAdminUser
from account.models import CustomUser
from rest_framework import status


# admin users list view
from account.serializers import CustomUserSerializer





class UsersListAdminView(APIView):
    permission_classes=[IsAdminUser]
    def get(self,request):
        user_=CustomUser.objects.all()
        ser=CustomUserSerializer(user_,many=True)
        # blocked_user=[user for user in ser.data if user['is_blocked']==True]
        # users=[user for user in ser.data if user['is_blocked']==False]
        return Response(
            {"users":ser.data
            }
        )
    def put(self,request):
        k=request.data
        try:
            id_=k['id']
        except:
            return Response("enter user id")
        data_=CustomUser.objects.get(id=id_)
        ser=CustomUserSerializer(data_,data=k,partial=True)    
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)

# list of all student for admin

from student.serializers import StudentProfileSerializer

class StudentLsistAdminview(APIView):
    permission_classes=[IsAdminUser]
    def get(self,request):
        keyword=request.GET.get('student')
        if keyword :
            students=StudentProfile.objects.filter(full_name__startswith=keyword)
        else:    
            students=StudentProfile.objects.all()
        ser=StudentProfileSerializer(students, many=True)
        return Response(ser.data,status=status.HTTP_200_OK)

from account.serializers import CustomUserSerializer


# list of teachers for admin

from teacher.serializers import TeacherProfileSerislizer

class TeacherListAdminView(APIView):
    permission_classes=[IsAdminUser]

    def get(self,request):
        keyword=request.GET.get('teacher')
        if keyword :
            teachers=TeacherProfile.objects.filter(teacher_name__startswith=keyword)
        else:    
            teachers=TeacherProfile.objects.all()        
        ser=TeacherProfileSerislizer(teachers, many=True)
        return Response(ser.data,status=status.HTTP_200_OK)
    def post(self,request):
        new_teacher=request.data
        ser=TeacherProfileSerislizer(data=new_teacher)
        if ser.is_valid():
            teacher_profile=ser.save()
            user_=teacher_profile.user
            user_.role=CustomUser.TEACHER
            user_.is_staff=True
            user_.save()
            return Response({"data":ser.data,"message": "Teacher added successfully"}, status=status.HTTP_201_CREATED)
        return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request):
        teacher_=request.data
        id_=teacher_.get('id',None)
        if id_ is None:
            return Response ({"error": "Teacher ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        data_=TeacherProfile.objects.get(id=id_)
        if data_ is None:
            return Response({"error": "Teacher not found"}, status=status.HTTP_404_NOT_FOUND)
        data_.delete()
        return Response({"message": "Teacher deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



# add new course for admin
from .serializers import CourseSerializer

class CourseAdminView(ModelViewSet):
    
    serializer_class=CourseSerializer      
    permission_classes=[IsAdminUser]

    def get_queryset(self):
        try:
            id=self.request.GET.get('id')
            queryset=Course.objects.all(id=id)
        except:
            queryset=Course.objects.all()


        return queryset
    

# add new subject for admin
from. serializers import SubjectSerializer

class SubjectAdminView(ModelViewSet):
    # queryset=Subject.objects.all()
    serializer_class=SubjectSerializer
    permission_classes=[IsAdminUser]  

    def get_queryset(self):
        
        print("in try==1")
        course_id=self.request.GET.get('courseId')
        if course_id :
            print("in try==2",course_id)
            queryset=Subject.objects.filter(course=course_id)
            print("in try==3")
        else:    
            print("in try==4")
            queryset=Subject.objects.all()
            print("in try==5")
        return queryset
    


# add new Chapter for admin

from. serializers import ChapterSerializer

class ChapterAdminView(ModelViewSet):
    # queryset=Chapter.objects.all()
    serializer_class=ChapterSerializer
    permission_classes=[IsAdminUser]

    def get_queryset(self):
        subject_id=self.request.GET.get('subjectId')
        if subject_id :
            print("in try==2",subject_id)
            
            queryset=Chapter.objects.filter(subject=subject_id)
 
        else:    
            print("in try==4")
            queryset=Chapter.objects.all()
            print("in try==5")
        return queryset


# add new lesson for admin

from. serializers import LessonSerializer

class LessonAdminView(ModelViewSet):
    # queryset=Lesson.objects.all()
    serializer_class=LessonSerializer
    permission_classes=[IsAdminUser]

    def get_queryset(self):
        chapter_id=self.request.GET.get('chapterId')
        if chapter_id :            
            queryset=Lesson.objects.filter(chapter=chapter_id)
        else:    
            queryset=Lesson.objects.all()
        return queryset



    