from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash

def index(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            current_password = request.POST.get('current_password', '')
            new_password = request.POST.get('new_password', '')
            print(current_password, new_password)

            user = request.user

            # ตรวจสอบว่ารหัสผ่านปัจจุบันถูกต้องหรือไม่
            if not check_password(current_password, user.password):
                return JsonResponse({'success': False, 'error': 'Current password is incorrect.'})

            # อัปเดตรหัสผ่านใหม่
            user.set_password(new_password)
            user.save()

            # ทำให้ session ยังคงอยู่หลังจากเปลี่ยนรหัสผ่าน
            update_session_auth_hash(request, user)

            return JsonResponse({'success': True, 'message': 'Password changed successfully!'})
        return render(request, "app/auth/profile/index.html")
    else:
        return redirect("signin")
