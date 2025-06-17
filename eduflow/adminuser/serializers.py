from rest_framework import serializers
from .models import Course,Subject,Chapter,Lesson


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields=['id','course_name']

class SubjectSerializer(serializers.ModelSerializer):
    course=serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    class Meta:
        model=Subject
        fields=['id','course','subject_name']
        
    def to_representation(self, instance):
        return {
            "id":instance.id,
            "course":instance.course.course_name,
            "subject_name":instance.subject_name
        }

class ChapterSerializer(serializers.ModelSerializer):
    subject=serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())
    class Meta:
        model=Chapter
        fields=['id','subject','chapter_name']
        

    def to_representation(self, instance):
        return {
            "id":instance.id,
            "subject":instance.subject.subject_name,
            "chapter_name":instance.chapter_name
        }        

class LessonSerializer(serializers.ModelSerializer):
    chapter=serializers.PrimaryKeyRelatedField(queryset=Chapter.objects.all())
    class Meta:
        model=Lesson
        fields=['id','chapter','lesson_name','video','is_approved']

    def to_representation(self, instance):
        return {
            "id":instance.id,
            "chapter":instance.chapter.chapter_name,
            "lesson_name":instance.lesson_name,
            "video": instance.video.url if instance.video else None,
            "is_approved":instance.is_approved 
        }   
    def create(self, validated_data):
        print("im in lesson add ser===")
        chapter_data=validated_data.pop('chapter')
        validated_data['is_approved'] = False 
        new_lessoon=Lesson.objects.create(chapter=chapter_data,**validated_data)
        return new_lessoon
    def update(self, instance, validated_data):
        request_user=self.context['request'].user
        if request_user.role==1:
            try:
                chapter_=validated_data.pop('chapter')
            except:
                chapter_=instance.chapter       
            instance.lesson_name=validated_data.get('lesson_name',instance.lesson_name)
            instance.video=validated_data.get('video',instance.video)
        else:
            instance.is_approved=validated_data.get('is_approved',instance.is_approved) 
        instance.save()
        return instance