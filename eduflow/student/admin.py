from django.contrib import admin
from .models import StudentProfile,AssignmentSubmission,Leaderboard,StudentProfileDetail,AcademicDetail,AddressDetail,GuardianDetail,Preference,PersonalDetail

admin.site.register(StudentProfile)
admin.site.register(AssignmentSubmission)
admin.site.register(Leaderboard)
admin.site.register(StudentProfileDetail)
admin.site.register(AcademicDetail)
admin.site.register(AddressDetail)
admin.site.register(GuardianDetail)
admin.site.register(Preference)

admin.site.register(PersonalDetail)

# Register your models here.
