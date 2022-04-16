# Just the methods for cohorts
from django.shortcuts import render, redirect, HttpResponse
from .models import Cohort, Student
from .forms import CohortForm, StudentForm
import requests

def get_cohort(cohort_id):
    return Cohort.objects.get(id=cohort_id)

def cohort_list(request):
    cohorts = Cohort.objects.all()
    return render(request, 'cohorts_and_students/cohorts_list.html', {'cohorts': cohorts})

def cohort_detail(request, cohort_id):
    cohort = get_cohort(cohort_id)
    return render(request, 'cohorts_and_students/cohort_detail.html', {'cohort': cohort})

def new_cohort(request):
    if request.method == "POST":
        form = CohortForm(request.POST)
        if form.is_valid():
            cohort = form.save(commit=False)
            cohort.save()
            return redirect('cohort_detail', cohort_id=cohort.id)
    else:
        form = CohortForm()
    return render(request, 'cohorts_and_students/cohort_form.html', {'form': form, 'type_of_request': 'New'})

def edit_cohort(request, cohort_id):
    cohort = get_cohort(cohort_id)
    if request.method == "POST":
        form = CohortForm(request.POST, instance=cohort)
        if form.is_valid():
            cohort = form.save(commit=False)
            cohort.save()
            return redirect('cohort_detail', cohort_id=cohort.id)
    else:
        form = CohortForm(instance=cohort)
    return render(request, 'cohorts_and_students/cohort_form.html', {'form': form, 'type_of_request': 'Edit'})

def delete_cohort(request, cohort_id):
    if request.method == "POST":
        cohort = get_cohort(cohort_id)
        cohort.delete()
    return redirect('cohort_list')

def get_student(student_id):
    return Student.objects.get(slug=student_id)

def student_list(request, cohort_id):
    cohort = get_cohort(cohort_id)
    students = cohort.students.all()
    return render(request, 'cohorts_and_students/students_list.html', {'cohort': cohort, 'students': students})

def student_detail(request, cohort_id, student_id):
    cohort = get_cohort(cohort_id)
    student = get_student(student_id)
    res = requests.get(f"https://gender-api.com/get?name={student.first_name}&key=WEKfoglTbaeLsx5ZM2BzWrlPzjkS5qzpngBq")
    res_json = res.json()
    gender = {
        "gender": res_json["gender"],
        "confidence": res_json["accuracy"]
    }
    return render(request, 'cohorts_and_students/student_detail.html', {'cohort': cohort, 'student': student, "gender": gender})

def new_student(request, cohort_id):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.save()
            return redirect('student_detail', cohort_id=student.cohort.id, student_id=student.id)
    else:
        form = StudentForm()
    return render(request, 'cohorts_and_students/student_form.html', {'form': form, 'type_of_request': 'New'})

def edit_student(request, cohort_id, student_id):
    cohort = get_cohort(cohort_id)
    student = get_student(student_id)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            student.save()
            return redirect('student_detail', student_id=student.slug, cohort_id=cohort_id)
    else:
        form = StudentForm(instance=student)
    return render(request, 'cohorts_and_students/student_form.html', {'form': form, 'type_of_request': 'Edit'})

def delete_student(request, cohort_id, student_id):
    if request.method == "POST":
        student = get_student(student_id)
        student.delete()
    return redirect('student_list', cohort_id=cohort_id)