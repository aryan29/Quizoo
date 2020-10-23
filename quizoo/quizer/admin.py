from django.contrib import admin
from .models import Quiz, Questions, Options, CorrectOptions, UsersGivingTest, RecordedResponses, TestLogs

admin.site.register(
    [Quiz, Questions, Options, CorrectOptions,
        UsersGivingTest, RecordedResponses, TestLogs]
)
# Register your models here.
