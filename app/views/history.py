from django.shortcuts import render, redirect
from equipment.models import EquipmentType
from report_repair.models import Report, ReportStatus, ReportImage
from django.http import JsonResponse  # type: ignore
from user.models import User
from datetime import datetime
import os
from django.core.mail import EmailMessage
import mimetypes


def status(request):
    if request.user.is_authenticated:
        reports = Report.objects.filter(user=request.user).prefetch_related("images")
        # for report in reports:
        #     print(f"Report ID: {report.id}")
        #     for image in report.images.all():
        #         print(f"Image: {image.image}")
        equipment_types = EquipmentType.objects.all()
        reportStatus = ReportStatus.objects.all()
        context = {
            "url": "status",
            "reports": reports,
            "equipment_types": equipment_types,
            "reportStatus": reportStatus,
        }
        return render(request, "app/user/status/index.html", context)
    else:
        return redirect("signin")


def status_admin(request):
    if request.user.is_authenticated and request.user.role.name == "admin":
        reports = Report.objects.filter(
            user__company=request.user.company
        ).prefetch_related("images")
        equipment_types = EquipmentType.objects.all()
        reportStatus = ReportStatus.objects.all()
        staffs = User.objects.filter(
            role__name__in=["staff", "admin"],
            company=request.user.company,
        )
        context = {
            "url": "status_admin",
            "reports": reports,
            "equipment_types": equipment_types,
            "reportStatus": reportStatus,
            "staffs": staffs,
        }
        return render(request, "app/admin/status/index.html", context)
    else:
        return redirect("/")


def assign_report(request):
    if request.method == "POST":
        report_id = request.POST.get("report_id")
        staff_id = request.POST.get("staff_id")
        remark = request.POST.get("remark")

        try:
            report = Report.objects.get(id=report_id)
            staff = User.objects.get(id=staff_id)
            status = ReportStatus.objects.get(sequence=1)

            report.staff = staff
            report.remark = remark
            report.status = status
            report.save()

            try:
                subject = "แจ้งเตือน: มีการส่งคำขอซ่อมใหม่"
                message = (
                    f"ผู้ใช้ {report.user.first_name} {report.user.last_name} ได้ส่งคำขอซ่อมอุปกรณ์:\n\n"
                    f"อุปกรณ์ {report.equipment_type.name}\n"
                    f"ชื่อเรื่อง: {report.title}\n"
                    f"รายละเอียด: {report.detail}\n"
                    f"หมายเหตุ: {remark}"
                )

                email = EmailMessage(
                    subject,
                    message,
                    os.getenv("EMAIL_HOST_USER"),
                    [staff.email],
                )
                # แนบไฟล์ภาพ
                images = ReportImage.objects.filter(report=report)
                for image in images:
                    image_path = image.image.path
                    content_type, _ = mimetypes.guess_type(image_path)

                    with open(image_path, "rb") as img_file:
                        email.attach(
                            image.image.name,
                            img_file.read(),
                            content_type or "application/octet-stream",
                        )

                email.send()
            except Exception as e:
                print(f"Error sending email to staff: {e}")

            return JsonResponse({"status": "success"})
        except Report.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Report not found"})
        except User.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Employee not found"})
    return JsonResponse({"status": "error", "message": "Invalid request"})


def status_staff(request):
    if (
        request.user.is_authenticated
        and request.user.role.name == "admin"
        or request.user.role.name == "staff"
    ):
        reports = Report.objects.filter(staff=request.user).prefetch_related("images")
        equipment_types = EquipmentType.objects.all()
        reportStatus = ReportStatus.objects.all()
        context = {
            "url": "status_staff",
            "reports": reports,
            "equipment_types": equipment_types,
            "reportStatus": reportStatus,
        }
        return render(request, "app/staff/status/index.html", context)
    else:
        return redirect("/")


def accept_report(request):
    if request.method == "POST":
        report_id = request.POST.get("report_id")
        remark = request.POST.get("remark")

        try:
            report = Report.objects.get(id=report_id)
            status = ReportStatus.objects.get(sequence=2)

            report.remark = remark
            report.status = status
            report.start_date = datetime.now()
            report.save()

            return JsonResponse({"status": "success"})
        except Report.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Report not found"})
    return JsonResponse({"status": "error", "message": "Invalid request"})


def complete_report(request):
    if request.method == "POST":
        report_id = request.POST.get("report_id")
        remark = request.POST.get("remark")
        complete_status = request.POST.get("complete_status")

        try:
            report = Report.objects.get(id=report_id)
            if complete_status == "complete":
                status = ReportStatus.objects.get(sequence=3)
            else:
                status = ReportStatus.objects.get(sequence=4)

            report.remark = remark
            report.status = status
            report.end_date = datetime.now()
            report.save()

            def send_mail_to_user():
                try:
                    subject = "แจ้งเตือน: ความคืบหน้ารายการที่แจ้งซ่อม"
                    message = (
                        f"ผู้ใช้ {report.user.first_name} {report.user.last_name} ได้แจ้งซ่อม:\n\n"
                        f"อุปกรณ์ {report.equipment_type.name}\n"
                        f"ชื่อเรื่อง: {report.title}\n"
                        f"รายละเอียด: {report.detail}\n"
                        f"หมายเหตุ: {remark}\n"
                        f"สถานะการแจ้งซ่อม: {report.status.name}"
                    )
                    email = EmailMessage(
                        subject,
                        message,
                        os.getenv("EMAIL_HOST_USER"),
                        [report.user.email],
                    )
                    # แนบไฟล์ภาพ
                    # images = ReportImage.objects.filter(report=report)
                    # for image in images:
                    #     image_path = image.image.path
                    #     content_type, _ = mimetypes.guess_type(image_path)

                    #     with open(image_path, "rb") as img_file:
                    #         email.attach(
                    #             image.image.name,
                    #             img_file.read(),
                    #             content_type or "application/octet-stream",
                    #         )

                    email.send()
                except Exception as e:
                    print(f"Error sending email to user: {e}")

            send_mail_to_user()
            return JsonResponse({"status": "success"})
        except Report.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Report not found"})
    return JsonResponse({"status": "error", "message": "Invalid request"})
