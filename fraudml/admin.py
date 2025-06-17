from django.contrib import admin
from .models import UploadedModel
from .models import Transaction

admin.site.register(Transaction)
admin.site.register(UploadedModel)
