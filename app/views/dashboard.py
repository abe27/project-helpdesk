from django.shortcuts import render, redirect
from report_repair.models import Report, ReportStatus
from datetime import datetime
import openpyxl
from django.http import HttpResponse


def index(request):
    if request.user.is_authenticated:
        if request.user.role:
            if request.user.role.name == "admin":
                company = request.user.company
                current_year = datetime.now().year  # ดึงปีปัจจุบัน


                # ตรวจสอบว่ามีสถานะที่ sequence=3 หรือไม่
                status_success = None
                try:
                    status_success = ReportStatus.objects.get(sequence=3)
                except ReportStatus.DoesNotExist:
                    pass

                # ตรวจสอบว่ามีสถานะที่ sequence=4 หรือไม่
                status_fail = None
                try:
                    status_fail = ReportStatus.objects.get(sequence=4)
                except ReportStatus.DoesNotExist:
                    pass


                progress_reports = (
                    Report.objects.filter(
                        user__company=company, created_at__year=current_year
                    )
                    .exclude(status__in=[status_success, status_fail])
                    .count()
                )
                success_reports = Report.objects.filter(
                    user__company=company,
                    status=status_success,
                    created_at__year=current_year,
                ).count()
                fail_reports = Report.objects.filter(
                    user__company=company, status=status_fail, created_at__year=current_year
                ).count()
                all_reports = Report.objects.filter(
                    user__company=company, created_at__year=current_year
                ).count()

                monthly_reports = []
                for month in range(1, 13):  # Loop ตั้งแต่ ม.ค. - ธ.ค.
                    count = Report.objects.filter(
                        user__company=company,
                        created_at__year=current_year,
                        created_at__month=month,
                    ).count()
                    monthly_reports.append(count)

                context = {
                    "url": "dashboard",
                    "progress_reports": progress_reports,
                    "success_reports": success_reports,
                    "fail_reports": fail_reports,
                    "all_reports": all_reports,
                    "monthly_reports": monthly_reports,  # ส่งข้อมูลรายเดือนไปยังเทมเพลต
                }
                return render(request, "app/home/index.html", context)
        return redirect("form")
    else:
        return redirect("signin")


def generate_report(request):
    if not request.user.is_authenticated:
        return redirect("signin")

    company = request.user.company
    current_year = datetime.now().year

    # ดึงข้อมูลรายงานทั้งหมดของบริษัทตามปีปัจจุบัน
    reports = Report.objects.filter(
        user__company=company, created_at__year=current_year
    )

    # สร้างไฟล์ Excel
    wb = openpyxl.Workbook()

    # หัวตาราง
    headers = [
        "Report ID",
        "Title",
        "Equipment Type",
        "Detail",
        "Status",
        "Remark",
        "User",
        "Staff",
        "Created At",
        "Start Date",
        "End Date",
    ]

    # แยกข้อมูลเป็น Dictionary ตามสถานะ
    status_dict = {}
    for report in reports:
        status_name = report.status.name if report.status else "Unknown"
        if status_name not in status_dict:
            status_dict[status_name] = []

        status_dict[status_name].append(
            [
                report.id,
                report.title or "-",
                report.equipment_type.name if report.equipment_type else "-",
                report.detail or "-",
                report.status.name if report.status else "-",
                report.remark or "-",
                report.user.get_full_name() if report.user else "-",
                report.staff.get_full_name() if report.staff else "-",
                report.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                (
                    report.start_date.strftime("%Y-%m-%d %H:%M:%S")
                    if report.start_date
                    else "-"
                ),
                (
                    report.end_date.strftime("%Y-%m-%d %H:%M:%S")
                    if report.end_date
                    else "-"
                ),
            ]
        )

    # ลบ default sheet ที่สร้างโดยอัตโนมัติ
    default_sheet = wb.active
    wb.remove(default_sheet)

    # สร้าง sheet ตามสถานะ และเพิ่มข้อมูล
    for status, data in status_dict.items():
        ws = wb.create_sheet(title=status[:31])  # จำกัดชื่อ sheet ไม่เกิน 31 ตัวอักษร
        ws.append(headers)  # เพิ่มหัวตาราง
        for row in data:
            ws.append(row)

    # กำหนดชื่อไฟล์และตอบกลับเป็น Excel
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="Report.xlsx"'
    wb.save(response)
    return response
