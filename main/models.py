from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


def upload_document(instance, filename):
    return f'documents/{instance.user.username}/{filename}'


class UserDocuments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doc_type = models.CharField(max_length=10, choices=[
        ('pan', 'pan'),
        ('aadhar', 'aadhar'),
        ('others', 'others')
    ])
    document = models.FileField(upload_to=upload_document)

    def __str__(self):
        return f'{self.user.username}  - {self.doc_type}'
