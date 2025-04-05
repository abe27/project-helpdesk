from django.shortcuts import render, redirect
from user.models import User
from department.models import Department
from user.form import AddUserForm
from django.contrib import messages


def index(request):
    if request.user.is_authenticated and request.user.role.name == "admin":
        users = User.objects.filter(company=request.user.company)
        departments = Department.objects.filter(company=request.user.company)
        context = {
            "url": "user",
        }
        if request.method == "POST":
            form = AddUserForm(request.POST, user=request.user)  # ส่ง request.user ใน POST
            if form.is_valid():
                form.save()
                messages.success(request, "เพิ่มผู้ใช้สำเร็จ!")  # เพิ่มข้อความแจ้งเตือน
                return redirect("user")
        else:
            form = AddUserForm(user=request.user)  # ส่ง request.user ใน GET
        context.update(
            {
                "users": users,
                "form": form,
                "departments": departments,
            }
        )
        return render(request, "app/admin/user/index.html", context)
    else:
        return redirect("signin")
