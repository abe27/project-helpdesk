from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from department.models import Department
from user.models import User
from django.contrib import messages  # type: ignore
import os
from django.core.mail import EmailMessage


# Create your views here.
def load_departments(request):
    company_id = request.GET.get("company")
    departments = Department.objects.filter(company_id=company_id).all()
    return JsonResponse(list(departments.values("id", "name")), safe=False)


def update_user_status(request):
    if (
        request.method == "POST"
        and request.user.is_authenticated
        and request.user.is_staff
    ):
        user_id = request.POST.get("user_id")
        is_active = request.POST.get("is_active") == "true"
        try:
            user = User.objects.get(id=user_id, company=request.user.company)
            user.is_active = is_active
            user.save()

            if is_active:
                try:
                    subject = "แจ้งเตือน: การสมัครสมาชิกได้รับการอนุมัติแล้ว"
                    message = (
                        f"สำหรับผู้ใช้ {user.first_name} {user.last_name} ที่ได้สมัครสมาชิกบนระบบ HelpDesk\n\n"
                        f"ขณะนี้คุณสามารถเข้าสู่ระบบได้แล้ว"
                        f"\n\nขอบคุณที่ใช้บริการ"
                    )
                    email = EmailMessage(
                        subject,
                        message,
                        os.getenv("EMAIL_HOST_USER"),
                        [user.email],
                    )
                    email.send()
                except Exception as e:
                    print(f"Error sending email: {e}")
                    
            return JsonResponse(
                {"success": True, "message": "สถานะได้รับการอัปเดตเรียบร้อยแล้ว"}
            )
        except User.DoesNotExist:
            return JsonResponse(
                {"success": False, "message": "ไม่พบผู้ใช้งานที่ระบุ"}, status=404
            )
    return JsonResponse({"success": False, "message": "การร้องขอไม่ถูกต้อง"}, status=400)


def reset_password(request):
    if (
        request.method == "POST"
        and request.user.is_authenticated
        and request.user.is_staff
    ):
        user_id = request.POST.get("user_id")
        new_password = request.POST.get("new_password")

        if not new_password or len(new_password) < 8:
            return JsonResponse(
                {"success": False, "message": "รหัสผ่านต้องมีอย่างน้อย 8 ตัวอักษร"}, status=400
            )

        try:
            user = User.objects.get(id=user_id, company=request.user.company)
            user.set_password(new_password)
            user.save()

            return JsonResponse({"success": True, "message": "รีเซ็ตรหัสผ่านสำเร็จ"})
        except User.DoesNotExist:
            return JsonResponse(
                {"success": False, "message": "ไม่พบผู้ใช้งานที่ระบุ"}, status=404
            )

    return JsonResponse({"success": False, "message": "การร้องขอไม่ถูกต้อง"}, status=400)


def edit_user_admin(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        user = get_object_or_404(User, id=user_id)

        # อัปเดตข้อมูลทั่วไป
        user.emp_id = request.POST.get("emp_id")
        user.email = request.POST.get("email")
        user.username = request.POST.get("username")
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.tel = request.POST.get("tel")
        user.fcdept_id = request.POST.get("department")
        user.save()
        messages.success(request, "อัพเดทผู้ใช้สำเร็จ!")  # เพิ่มข้อความแจ้งเตือน

        return redirect("user")
