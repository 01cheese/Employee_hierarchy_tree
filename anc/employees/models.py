from django.db import models

class Employee(models.Model):
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    date_of_hire = models.DateField()
    email = models.EmailField()
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates')

    def __str__(self):
        return self.full_name