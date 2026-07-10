import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "facultyerp.settings")
django.setup()

from core.models import Faculty
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
import datetime

data = [
    (1, "Faculty 1", "Computer", "2026-07-01T09:00:00"),
    (2, "Faculty 2", "Computer", "2026-07-02T09:00:00"),
    (3, "Faculty 3", "Computer", "2026-07-03T09:00:00"),
    (4, "Faculty 4", "Computer", "2026-07-04T09:00:00"),
    (5, "Faculty 5", "Computer", "2026-07-05T09:00:00"),
    (6, "Faculty 6", "IT", "2026-07-06T09:00:00"),
    (7, "Faculty 7", "IT", "2026-07-07T09:00:00"),
    (8, "Faculty 8", "IT", "2026-07-08T09:00:00"),
    (9, "Faculty 9", "IT", "2026-07-09T09:00:00"),
    (10, "Faculty 10", "IT", "2026-07-10T09:00:00"),
]

for uid, name, dept, created_at in data:
    user, created = User.objects.get_or_create(
        id=uid, 
        defaults={
            'username': f'faculty_{uid}', 
            'email': f'faculty{uid}@example.com'
        }
    )
    if created:
        user.set_password('password123')
        user.save()
        
    dt = make_aware(parse_datetime(created_at))
    
    faculty, f_created = Faculty.objects.get_or_create(
        id=uid, 
        defaults={
            'user': user,
            'name': name,
            'department': dept,
            'is_verified': True,
        }
    )
    
    if not f_created:
        faculty.user = user
        faculty.name = name
        faculty.department = dept
        faculty.is_verified = True
        faculty.save()
        
print("Successfully added 10 Faculty members.")
