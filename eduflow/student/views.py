from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import AssignmentSubmission,StudentProfile,Leaderboard
from rest_framework.permissions import IsAuthenticated,AllowAny
from. serializers import StudentProfileSerializer
from adminuser.models import Lesson
from rest_framework.response import Response
from teacher.models import AssignmentTask
from rest_framework import status
from account .models import CustomUser
from account .permissions import IsStudent
from django.db.models import Q
from adminuser.models import Course,Subject,Chapter,Lesson
from adminuser.serializers import CourseSerializer,SubjectSerializer,ChapterSerializer,LessonSerializer


class StudentProfileStudentView(ModelViewSet):
    serializer_class=StudentProfileSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        queryset=StudentProfile.objects.filter(user=self.request.user)
        return queryset
    def perform_create(self, serializer):
        print("im hereree")
        serializer.save(user=self.request.user)
 

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to update this profile.")
        serializer.save()

class StudentCourseView(APIView):
    def get(self,request):
        course=Course.objects.all()
        ser=CourseSerializer(course, many=True)
        return Response(ser.data)
    
class StudentSubjectView(APIView):
    permission_classes=[IsStudent]
    def get(self,request):
        subject_id=request.GET.get('subjectId')
        student_course = request.user.studentprofile.course
        if subject_id:
            subject=Subject.objects.get(id=subject_id)
            ser=SubjectSerializer(subject)

        else:  
            subject=Subject.objects.filter(course=student_course)
            ser=SubjectSerializer(subject, many=True)
        return Response(ser.data)


class StudentChapterView(APIView):
    permission_classes=[IsStudent]    
    def get(self,request):
        subject_id=request.GET.get('subjectId')
        chapter_id=request.GET.get('chapterId')
        print('subjece_id=',subject_id)
        print('chapter_id=',chapter_id)
        student_course = request.user.studentprofile.course
        # chapter=Chapter.objects.filter(subject__course=student_course)
        if subject_id:
            chapter=Chapter.objects.filter(subject=subject_id)
            ser=ChapterSerializer(chapter, many=True)
        elif chapter_id:    
            chapter=Chapter.objects.get(id=chapter_id)
            ser=ChapterSerializer(chapter)
        else:
            chapter=Chapter.objects.filter(subject__course=student_course)
            ser=ChapterSerializer(chapter, many=True)
        return Response(ser.data)     

# students get recorderd videos
from adminuser.serializers import LessonSerializer

class LessonStudentView(APIView):
    permission_classes=[IsStudent]
    def get(self,request):
        chapter_id=request.GET.get('chapterId')
        lesson_id=request.GET.get('lessonId')
        print(chapter_id)
        student_=StudentProfile.objects.get(user=request.user)   
        student_course=student_.course
        if chapter_id:
            k=Lesson.objects.filter(Q(chapter__subject__course__course_name=student_course)& Q(is_approved=True) & Q(chapter=chapter_id))
            ser=LessonSerializer(k,many=True)
        elif lesson_id:
            k=Lesson.objects.get(id=lesson_id)
            ser=ser=LessonSerializer(k)   
        else:    
            k=Lesson.objects.filter(Q(chapter__subject__course__course_name=student_course)& Q(is_approved=True))    
            ser=LessonSerializer(k,many=True)
        return Response(ser.data,status=status.HTTP_200_OK)
    

# assignment task students view  
from teacher.serializers import TaskSerializer

# class TaskStudentsView(APIView):
#     permission_classes=[IsStudent]
#     def get(self,request):
#         try:
#             task_id=request.GET.get('taskId')
#             k=AssignmentSubmission.objects.get(id=task_id)
#             print('==',task_id)
#         except:
#             k=AssignmentTask.objects.filter(students=student_).exclude(blocked_students=student_)     
#         student_=StudentProfile.objects.get(user=request.user)
        
        
#         print("students in views", k)
#         ser=TaskSerializer(k, many=True,context={'user': request.user})
#         return Response(ser.data,status=status.HTTP_200_OK)
class TaskStudentsView(APIView):
    permission_classes = [IsStudent]

    def get(self, request):
        try:
            student_ = StudentProfile.objects.get(user=request.user)

            task_id = request.GET.get('taskId')

            if task_id:
                task = AssignmentTask.objects.get(id=task_id,is_completed=False)
                ser = TaskSerializer(task, context={'user': request.user})
                return Response(ser.data, status=status.HTTP_200_OK)

            else:
                tasks = AssignmentTask.objects.filter(
                    students=student_,
                    is_completed=False
                ).exclude(blocked_students=student_)
                ser = TaskSerializer(tasks, many=True, context={'user': request.user})
                return Response(ser.data, status=status.HTTP_200_OK)

        except AssignmentTask.DoesNotExist:
            return Response({'detail': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)

        except StudentProfile.DoesNotExist:
            return Response({'detail': 'Student profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# assignment submission for student

from .serializers import AssignmentSubmissionSerializer

class SubmissionStudentsView(APIView):
    # permission_classes=[IsStudent]
    def get(self,request):
        task_id=request.GET.get('taskId')
        if task_id:
            k=AssignmentSubmission.objects.get(id=task_id)
            print("gett")
        else:
            k=AssignmentSubmission.objects.filter(student__user=request.user)
  
        ser=AssignmentSubmissionSerializer(k,many=True)
        print("dAta===",ser.data)
        return Response(ser.data,status=status.HTTP_200_OK)
    def post(self,request):
        print("====vie=1")
        task_id=request.GET.get('taskId')
        data_=request.data
        # task=AssignmentTask.objects.filter(id=task_id)
        print("====vie=2")
        
        ser = AssignmentSubmissionSerializer(data=data_, context={'request': request})
        if ser.is_valid():
            ser.save()
            m=AssignmentTask.objects.get(id=task_id)
            m.is_completed=True
            m.save()
            return Response({"data": ser.data, "message": "assignment added successfully"}, status=status.HTTP_201_CREATED)

        return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)
    def put(self,request):
        updated_data=request.data
        id_=updated_data.get('id')
        if id_ is None:
            return Response({"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            old_data=AssignmentSubmission.objects.get(id=id_)
        except AssignmentSubmission.DoesNotExist:
            return Response('no data found')
        ser=AssignmentSubmissionSerializer(old_data,data=updated_data,partial=True,context={'request': request})
        if ser.is_valid():
            ser.save()
            return Response({"data":ser.data,"message": "submitted assignment updated successfully"}, status=status.HTTP_200_OK)
        return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)

# leaderboard

from .serializers import leaderboardserialier

class LeaderBoardView(APIView):
    permission_classes=[IsStudent]
    def get(self,request):
        k=Leaderboard.objects.order_by('-mark')[:3]
        print(k)
        ser=leaderboardserialier(k,many=True)
        user_student=StudentProfile.objects.get(user=request.user)
        k=ser.data
        my_rank=0
        
        for i in k:
            # print(i.get('mark'))
            if i.get('student_name')==user_student:
                my_rank=i.get('rank')
                # print('kkk',i.rank)
        print(k)
        # k[3]=my_rank
        try:
           k0=(k[0])
        except:
           k0=None   
        try:
           k1=(k[1])
        except:
           k1=None    
        try:
           k2=(k[2])
        except:
           k2=None 
        return Response({
            "ranks":k,
            # "my_rank":my_rank
        })








# =====================================








# student/views.py
from rest_framework import generics
from .models import StudentProfileDetail
from .serializers import StudentProfileDetailSerializer
from rest_framework.permissions import IsAuthenticated

class StudentProfileDetailView(generics.RetrieveAPIView):
    queryset = StudentProfileDetail.objects.select_related(
        'user', 'personal_detail', 'preference',
        'guardian_detail', 'address_detail', 'academic_detail'
    )
    serializer_class = StudentProfileDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Return the profile for the logged-in user
        return StudentProfileDetail.objects.get(user__user=self.request.user)
