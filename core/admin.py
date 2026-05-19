from django.contrib import admin
from .models import AssessmentPack, AssessmentVersion, AssessmentAttempt, AssessmentAnswer, GeneratedReport
admin.site.register(AssessmentPack)
admin.site.register(AssessmentVersion)
admin.site.register(AssessmentAttempt)
admin.site.register(AssessmentAnswer)
admin.site.register(GeneratedReport)
