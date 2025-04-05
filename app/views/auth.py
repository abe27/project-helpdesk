from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from user.models import User
from company.models import Company
from department.models import Department
from django.contrib.auth import get_user_model
from django.db import transaction
from django.contrib.auth.hashers import make_password  # type: ignore
import os
from django.core.mail import EmailMessage


def sign_in(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        username_or_email = request.POST["username_or_email"]
        password = request.POST["password"]
        user = authenticate(request, username=username_or_email, password=password)

        if user is None:
            try:
                # Find user by email
                user = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            return redirect("/")  # Redirect to the home page or dashboard
        else:
            messages.error(request, "Invalid email or password")
    return render(request, "app/auth/signin/index.html")


def sign_up(request):
    if request.user.is_authenticated:
        return redirect("/")

    User = get_user_model()
    companies = Company.objects.all()
    departments = Department.objects.all()

    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        company_id = request.POST.get("company")
        department_id = request.POST.get("department")
        emp_id = request.POST.get("emp_id")
        tel = request.POST.get("tel")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("signup")

        try:
            with transaction.atomic():
                company = Company.objects.get(id=company_id)
                department = Department.objects.get(id=department_id)

                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=make_password(password1),
                    first_name=first_name,
                    last_name=last_name,
                    emp_id=emp_id,
                    tel=tel,
                    company=company,
                    department=department,
                    role=None,  # ตั้งค่า role เป็น None หรือค่าเริ่มต้น
                    is_active=False,
                )

                # ส่งอีเมลแจ้งเตือนให้ผู้ใช้
                def send_mail_to_user():
                    try:
                        subject = "แจ้งเตือน: การสมัครสมาชิกใหม่"
                        message = (
                            f"ยินดีต้อนรับสู่ระบบแจ้งซ่อม!\n\n"
                            f"กรุณาติดต่อ Admin ของทาง IT เพื่อยืนยันการสมัคร.\n"
                            f"หาก IT ยืนยันการสมัครแล้ว ท่านจะสามารถเข้าสู่ระบบได้.\n"
                            f"ขอขอบคุณที่สมัครสมาชิก"
                        )
                        send_email = EmailMessage(
                            subject,
                            message,
                            os.getenv("EMAIL_HOST_USER"),
                            [email],
                        )

                        send_email.send()
                        print("Sent email")
                    except Exception as e:
                        print(os.getenv("EMAIL_HOST_USER"))
                        print(f"Error sending email: {e}")

                # ส่งอีเมลแจ้งเตือนให้ admin
                def send_mail_to_admin():
                    # ดึงอีเมลของผู้ใช้ที่มี role เป็น "admin"
                    admin_emails = list(
                        User.objects.filter(role__name="admin", company=company)
                        .exclude(email__isnull=True)
                        .exclude(email__exact="")
                        .values_list("email", flat=True)
                    )

                    if admin_emails:  # เช็คว่ามีอีเมลแอดมินอยู่หรือไม่
                        try:
                            subject = "แจ้งเตือน: มีผู้ใช้ใหม่สมัครสมาชิก"
                            message = (
                                f"มีผู้ใช้ใหม่สมัครสมาชิกในระบบแจ้งซ่อม:\n"
                                f"ชื่อผู้ใช้: {username}\n"
                                f"ชื่อ: {first_name} {last_name}\n"
                                f"อีเมล: {email}\n"
                                f"หมายเลขบัตรพนักงาน: {emp_id}\n"
                                f"เบอร์โทรศัพท์: {tel}\n"
                                f"บริษัท: {company.name}\n"
                                f"แผนก: {department.name}\n"
                            )
                            send_email = EmailMessage(
                                subject,
                                message,
                                os.getenv("EMAIL_HOST_USER"),
                                admin_emails,
                            )
                            send_email.send()
                            print("Sent email to admin")
                        except Exception as e:
                            print(os.getenv("EMAIL_HOST_USER"))
                            print(f"Error sending email to admin: {e}")

                send_mail_to_user()
                send_mail_to_admin()
                messages.success(request, "Account created successfully. Please login.")
                return redirect("signin")
        except Exception as e:
            messages.error(request, f"Error creating account: {e}")
            return redirect("signup")

    return render(
        request,
        "app/auth/signup/index.html",
        {"companies": companies, "departments": departments},
    )


def sign_out(request):
    logout(request)
    return redirect("/")
