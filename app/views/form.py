from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from equipment.models import EquipmentType
from report_repair.models import Report, ReportImage, ReportStatus
from django.http import JsonResponse
import os
from user.models import User, Role
import mimetypes


def form(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            equipment_type_id = request.POST.get("equipment_type")
            title = request.POST.get("title")
            detail = request.POST.get("detail")
            images = request.FILES.getlist("images")
            status = ReportStatus.objects.filter(sequence=0).first()

            report = Report.objects.create(
                equipment_type_id=equipment_type_id,
                title=title,
                detail=detail,
                status=status,
                user=request.user,
            )

            for image in images:
                report_image = ReportImage(report=report, image=image)
                report_image.save()

            # ดึงอีเมลของผู้ใช้ที่มี role เป็น "Admin"
            admin_emails = list(
                User.objects.filter(role__name="admin")
                .exclude(email__isnull=True)
                .exclude(email__exact="")
                .values_list("email", flat=True)
            )

            if admin_emails:  # เช็คว่ามีอีเมลแอดมินอยู่หรือไม่
                try:
                    # ส่งอีเมลแจ้งเตือน
                    subject = "แจ้งเตือน: มีการส่งคำขอซ่อมใหม่"
                    message = (
                        f"ผู้ใช้ {report.user.first_name} {report.user.last_name} ได้ส่งคำขอซ่อมอุปกรณ์:\n\n"
                        f"อุปกรณ์ {report.equipment_type.name}\n"
                        f"ชื่อเรื่อง: {report.title}\n"
                        f"รายละเอียด: {report.detail}"
                    )

                    email = EmailMessage(
                        subject,
                        message,
                        os.getenv("EMAIL_HOST_USER"),  # ใช้ค่าจาก .env
                        admin_emails,  # ส่งอีเมลไปยังแอดมินทุกคน
                    )

                    # แนบไฟล์ภาพ
                    # แนบไฟล์ภาพ
                    images = ReportImage.objects.filter(report=report)
                    for image in images:
                            image_path = image.image.path
                            content_type, _ = mimetypes.guess_type(image_path)
                            
                            with open(image_path, "rb") as img_file:
                                email.attach(image.image.name, img_file.read(), content_type or "application/octet-stream")

                    email.send()
                    print("Sent email")
                except Exception as e:
                    print(os.getenv("EMAIL_HOST_USER"))
                    print(f"Error sending email: {e}")  # Debugging หากส่งเมลไม่สำเร็จ

            return JsonResponse({"success": True})

        equipment_types = EquipmentType.objects.all()
        context = {"url": "form", "equipment_types": equipment_types}
        return render(request, "app/form/index.html", context)
    else:
        return redirect("signin")
