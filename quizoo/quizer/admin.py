from django.contrib import admin
from .models import Quiz, Questions, Options, CorrectOptions, UsersGivingTest

admin.site.register(
    [Quiz, Questions, Options, CorrectOptions, UsersGivingTest]
)
# Register your models here.
