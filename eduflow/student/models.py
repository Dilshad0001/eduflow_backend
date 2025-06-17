from django.db import models
from adminuser.models import Course
from account.models import CustomUser
# from teacher. models import AssignmentTask

class StudentProfile(models.Model):
    user=models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    full_name=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=12)
    course=models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name


class AssignmentSubmission(models.Model):
    STATUS_CHOICES=[
        ("pending","pending"),
        ("submitted","submitted"),
        ("approved","approved"),
        ("rejected","rejected")
    ]
    student=models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    assignment = models.ForeignKey("teacher.AssignmentTask", on_delete=models.CASCADE)
    file=models.FileField(upload_to="submissions/",null=True)
    submitted_at=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=20, choices=STATUS_CHOICES,default="pending")
    mark=models.PositiveBigIntegerField(null=True,blank=True)

    def __str__(self):
        return f"{self.student.full_name}-{self.assignment.task_name}"
    
class Leaderboard(models.Model):
    student_name=models.OneToOneField(StudentProfile, on_delete=models.CASCADE)
    mark=models.FloatField(null=True)

    def __str__(self):
        return f"{self.student_name} with mark{self.mark} "


         


from django.db import models

# 1. Personal Details
class PersonalDetail(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Prefer not to say'),
    ]
    user = models.OneToOneField(StudentProfile, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    mobile_number = models.CharField(max_length=15)
    alternate_number = models.CharField(max_length=15, blank=True, null=True)
    nationality = models.CharField(max_length=50)
    blood_group = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return self.full_name

# 2. Preferences
class Preference(models.Model):
    user = models.OneToOneField(StudentProfile, on_delete=models.CASCADE)
    language = models.CharField(max_length=30, default="English")
    notifications_email = models.BooleanField(default=True)
    notifications_sms = models.BooleanField(default=False)
    course_reminders = models.BooleanField(default=True)
    theme = models.CharField(max_length=20, choices=[('light', 'Light'), ('dark', 'Dark')], default='light')
    learning_mode = models.CharField(max_length=20, choices=[('self', 'Self-paced'), ('live', 'Live'), ('both', 'Both')], default='self')
    timezone = models.CharField(max_length=100, default='UTC')

# 3. Guardian Details
class GuardianDetail(models.Model):
    RELATIONSHIP_CHOICES = [
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('guardian', 'Guardian'),
        ('other', 'Other'),
    ]
    full_name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=15)

# 4. Address Details
class AddressDetail(models.Model):
    current_address = models.TextField()
    permanent_address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)

# 5. Academic Details
class AcademicDetail(models.Model):
    institution = models.CharField(max_length=100)
    education_level = models.CharField(max_length=50)
    course_stream = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=50, blank=True, null=True)
    year_of_study = models.CharField(max_length=20)
    enrollment_status = models.CharField(max_length=20, choices=[('active', 'Active'), ('passed_out', 'Passed Out'), ('dropped', 'Dropped')])
    document_upload = models.FileField(upload_to='documents/', blank=True, null=True)

# 6. Main Student Profile
class StudentProfileDetail(models.Model):
    user = models.OneToOneField(StudentProfile, on_delete=models.CASCADE)
    personal_detail = models.OneToOneField(PersonalDetail, on_delete=models.CASCADE)
    preference = models.OneToOneField(Preference, on_delete=models.CASCADE)
    guardian_detail = models.OneToOneField(GuardianDetail, on_delete=models.CASCADE)
    address_detail = models.OneToOneField(AddressDetail, on_delete=models.CASCADE)
    academic_detail = models.OneToOneField(AcademicDetail, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile of {self.user.full_name}"

