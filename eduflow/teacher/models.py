from django.db import models
from account.models import CustomUser
# from student.models import StudentProfile


class TeacherProfile(models.Model):
    user=models.OneToOneField(CustomUser, on_delete= models.CASCADE)
    teacher_name=models.CharField(max_length=100)

    def __str__(self):
        return self.teacher_name


class AssignmentTask(models.Model):
    students = models.ManyToManyField("student.StudentProfile",related_name="assigned_tasks")
    task_name=models.CharField(max_length=50)
    task_file=models.FileField(upload_to='assignment/', null=True, blank=True) 
    description=models.TextField(null=True)
    uploaded_at=models.DateField(auto_now_add=True)
    submission_deadline=models.DateTimeField(null=True)
    blocked_students=models.ManyToManyField("student.StudentProfile",related_name="blocked_tasks",blank=True)
    is_completed=models.BooleanField(default=False)
    

    def __str__(self):
        return self.task_name

