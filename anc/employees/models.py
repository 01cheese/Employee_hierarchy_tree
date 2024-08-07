from django.db import models

class Employee(models.Model):
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    date_of_hire = models.DateField()
    email = models.EmailField()
    manager = models.ForeignKey('self', null=True, blank=True, related_name='subordinates', on_delete=models.SET_NULL)

    def __str__(self):
        return self.full_name
