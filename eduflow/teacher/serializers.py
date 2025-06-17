from rest_framework import serializers
from. models import TeacherProfile,AssignmentTask
from account.models import CustomUser
from student.models import StudentProfile

from account.serializers import CustomUserSerializer


class TeacherProfileSerislizer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    class Meta:
        model=TeacherProfile
        fields=['id','user_id', 'teacher_name']

    def to_representation(self, instance):
        return{
            "id":instance.id,
            "user":CustomUserSerializer(instance.user).data,
            "teacher_name":instance.teacher_name
        }    

    def create(self, validated_data):
        teacher_name_=validated_data.get('teacher_name')
        user_id = validated_data.pop('user_id')  
        try:
            user_= CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:    
            raise serializers.ValidationError("no user found")
        teacher = TeacherProfile.objects.create(user=user_, teacher_name=teacher_name_)
        return teacher    
    
    def update(self, instance, validated_data):
        instance.teacher_name=validated_data.get('teacher_name',instance.teacher_name)
        instance.save()
        return instance
    

from student.serializers import StudentProfileSerializer

class TaskSerializer(serializers.ModelSerializer):
    students = serializers.PrimaryKeyRelatedField(queryset=StudentProfile.objects.all(),many=True)
    class Meta:
        model=AssignmentTask
        fields='__all__'    
    def to_representation(self, instance): 
        request_user = self.context.get('user')
        try:
            k=StudentProfile.objects.get(user=request_user)
            student_list=[{"full_name":k.full_name}]
            user_="student"
        except StudentProfile.DoesNotExist:
            student_list=[{
                "full_name":st.full_name}for st in instance.students.all()
            ] 
            user_="teacher"
        ret={
        "id": instance.id,      
        "students":student_list,
        "task_name": instance.task_name,
        "task_file": instance.task_file.url if instance.task_file else None, 
        "description": instance.description,
        "uploaded_at": instance.uploaded_at,
        "submission_deadline": instance.submission_deadline,
        }
        if user_=="teacher":
            ret['blocked_students']=[{"full_name":s.full_name} for s in instance.blocked_students.all()]
        return ret


    def create(self, validated_data):
        students = validated_data.pop('students', [])
        blocked_students = validated_data.pop('blocked_students', [])
        print("students = ", students)
        print("blocked_students = ", blocked_students)
        new_data = AssignmentTask.objects.create(**validated_data)
        new_data.students.set(students)
        new_data.blocked_students.set(blocked_students)
        assigned_students_set = set(new_data.students.all())
        blocked_students_set = set(new_data.blocked_students.all())
        unblocked_students = assigned_students_set - blocked_students_set
        print("Unblocked students: ", unblocked_students)
        k=StudentProfile.objects.get(id=8)
        if k in blocked_students:
            print("blockeed")  
        print("k in ser",k)
        return new_data

    def update(self, instance, validated_data):
        instance.task_name=validated_data.get('task_name',instance.task_name)
        instance.task_file=validated_data.get('task_file',instance.task_file)
        instance.description=validated_data.get('description',instance.description)
        instance.submission_deadline=validated_data.get('submission_deadline',instance.submission_deadline)
        if 'students' in validated_data:
            instance.students.set(validated_data['students'])
        instance.save()
        return instance






