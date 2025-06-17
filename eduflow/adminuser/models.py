from django.db import models

class Course(models.Model):
    course_name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.course_name

class Subject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.subject_name} ({self.course.course_name})"

class Chapter(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)  
    chapter_name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.chapter_name} ({self.subject.subject_name} - {self.subject.course.course_name})"

class Lesson(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)  
    lesson_name = models.CharField(max_length=30)
    is_approved=models.BooleanField(default=False)
    video = models.FileField(upload_to='videos/', null=True, blank=True) 
    

    def __str__(self):
        return f"{self.lesson_name} ({self.chapter.chapter_name} - {self.chapter.subject.subject_name} - {self.chapter.subject.course.course_name})"



