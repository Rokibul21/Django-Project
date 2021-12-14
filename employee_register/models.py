from django.db import models
from django.http import request


class StudentData(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    email=models.CharField(max_length=255) 
    genders = (
        ('male', 'male'),
        ('female', 'female'),
        ('others', 'others'),
    )

    gender          = models.CharField(max_length=50, choices=genders)
    created_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

  
    
    class Meta:

        db_table = 'studentdata'

        verbose_name = "studentdata"

        verbose_name_plural = "Student Data"




    # def __str__(self):

    #     return '%s' % (self.StudentData)
    

    


