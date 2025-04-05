from django import forms
from .models import User
from department.models import Department


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["department"].queryset = Department.objects.none()

        if "company" in self.data:
            try:
                company_id = int(self.data.get("company"))
                self.fields["department"].queryset = Department.objects.filter(
                    company_id=company_id
                ).order_by("name")
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty queryset
        elif self.instance.pk and self.instance.company:
            self.fields["department"].queryset = Department.objects.filter(
                company_id=self.instance.company.id
            ).order_by("name")


class AddUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "emp_id",
            "email",
            "username",
            "password",
            "first_name",
            "last_name",
            "tel",
            "company",
            "department",
        ]
        labels = {
            "emp_id": "รหัสพนักงาน",
            "email": "อีเมล",
            "username": "ชื่อผู้ใช้",
            "password": "รหัสผ่าน",
            "first_name": "ชื่อจริง",
            "last_name": "นามสกุล",
            "tel": "เบอร์โทร",
            "company": "บริษัท",
            "department": "แผนก",
        }
        widgets = {
            "emp_id": forms.TextInput(
                attrs={"class": "form-control", "required": True}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "required": True}
            ),
            "username": forms.TextInput(
                attrs={"class": "form-control", "required": True}
            ),
            "password": forms.PasswordInput(
                attrs={"class": "form-control", "required": True}
            ),
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "required": True}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "required": True}
            ),
            "tel": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "company": forms.HiddenInput(attrs={"required": True}),
            "department": forms.Select(
                attrs={"class": "form-control", "required": True}
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)  # รับค่า user ผ่าน kwargs
        super(AddUserForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields["company"].initial = (
                user.company.id if user.company else "ไม่ระบุบริษัท"
            )
            self.fields["department"].queryset = Department.objects.filter(
                company=user.company
            )

    def save(self, commit=True):
        user = super(AddUserForm, self).save(commit=False)
        # เข้ารหัสรหัสผ่านก่อนบันทึก
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
