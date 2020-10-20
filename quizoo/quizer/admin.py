from django.contrib import admin
from .models import Quiz, Questions, Options, CorrectOptions, UsersGivingTest, RecordedResponses

admin.site.register(
    [Quiz, Questions, Options, CorrectOptions, UsersGivingTest, RecordedResponses]
)
# Register your models here.
