import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()


import random
from datacenter.models import Schoolkid
from datacenter.models import Mark
from datacenter.models import Chastisement
from datacenter.models import Lesson
from datacenter.models import Commendation
from datetime import date
from django.core.exceptions import ObjectDoesNotExist


def get_schoolkid_by_full_name(full_name):

    schoolkids = Schoolkid.objects.filter(full_name__contains=full_name)

    if schoolkids.exists():
        if schoolkids.count() > 1:
            print(f"Multiple schoolkids found with the name '{full_name}'. Please provide more specific information.")
            return None
        else:
            return schoolkids.first()
    else:
        print(f"Schoolkid '{full_name}' not found. Make sure you enter your name correctly. For example: Иванов Иван")
        return None
    

def fix_marks(schoolkid_full_name):

    schoolkid = get_schoolkid_by_full_name(schoolkid_full_name)

    if schoolkid:
        bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__lt=4)
        bad_marks.update(points=5)
    

def remove_chastisements(schoolkid_full_name):

    schoolkid = get_schoolkid_by_full_name(schoolkid_full_name)

    if schoolkid:
        chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
        chastisements.delete()


def create_commendation(schoolkid_full_name, subject_title):

    schoolkid = get_schoolkid_by_full_name(schoolkid_full_name)

    if schoolkid:
        lessons = Lesson.objects.filter(
            year_of_study=schoolkid.year_of_study,
            group_letter=schoolkid.group_letter,
            subject__title=subject_title
        ).order_by('-date')
        
        latest_lesson = lessons.first()

        if latest_lesson is None:
            print(f"No lessons found for subject '{subject_title}' Make sure you enter your name correctly. For example: Математика")
        else:
            commendation_text = random.choice([
                'Молодец!',
                'Отлично!',
                'Ты меня приятно удивил!',
                'Именно этого я давно ждал от тебя!',
                'Потрясающе!',
                'Так держать!',
                'Я тобой горжусь!',
                'Я вижу, как ты стараешься!',
                'Ты многое сделал, я это вижу!',
            ])

        commendation = Commendation.objects.create(
            text=commendation_text,
            created=latest_lesson.date,
            schoolkid=schoolkid,
            subject=latest_lesson.subject,
            teacher=latest_lesson.teacher
        )


if __name__ == '__main__':
    schoolkid_full_name = input("Enter the full name of the schoolkid: ")
    operation = input("Enter the operation to perform (fix_marks/remove_chastisements/create_commendation): ")

    if operation == 'fix_marks':
        fix_marks(schoolkid_full_name)
    elif operation == 'remove_chastisements':
        remove_chastisements(schoolkid_full_name)
    elif operation == 'create_commendation':
        subject_title = input("Enter the subject title: ")
        create_commendation(schoolkid_full_name, subject_title)
    else:
        print("Invalid operation.")        
