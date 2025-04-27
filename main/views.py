import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from django.shortcuts import render, get_object_or_404
from .models import Day, WorkTime, Staff
from django.contrib.auth.decorators import login_required
from django.contrib import messages
@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def work_times(request):
    work_times = WorkTime.objects.all()[::-1]
    context = {'work_times': work_times}
    return render(request, 'work_times.html', context)


@login_required
def add_worktime(request):
    staffs = Staff.objects.all()
    time_choices = [f"{hour:02}:{minute:02}" for hour in range(7, 25) for minute in (0, 30)]
    from datetime import datetime

    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        break_time = request.POST.get('break_time')
        day = request.POST.get('day')  # bu 'YYYY-MM-DD' formatda bo'ladi

        # Sana formatini to'g'rilaymiz
        try:
            day_date = datetime.strptime(day, '%Y-%m-%d').date()
        except ValueError:
            return HttpResponse("Noto'g'ri sana formati", status=400)

        # Agar Day modelida bu sana mavjud bo'lmasa, yaratamiz
        day, created = Day.objects.get_or_create(date=day_date)

        # WorkTime yozuvini yaratish (bu yerda sizning modelga bog'liq)
        WorkTime.objects.create(
            staff_id=staff_id,
            start_time=start_time,
            end_time=end_time,
            break_time=break_time,
            day=day,
            date=day_date  # ✅ bu yerda POST orqali kelgan sana saqlanadi
        )

        return redirect('work_times')  # kerakli sahifaga qaytarish

    return render(request, 'add_worktime.html', {
        'staffs': staffs,
        'time_choices': time_choices,
    })


@login_required
def delete_worktime(request, pk):
    worktime = get_object_or_404(WorkTime, pk=pk)
    worktime.delete()
    return redirect('work_times')

@login_required
def delete_staff(request, pk):
    if request.method == 'POST':
        staff = get_object_or_404(Staff, pk=pk)
        staff.delete()
        return redirect('stuffs')  # O'chirilgandan keyin xodimlar ro'yxati sahifasiga qaytish
    return redirect('stuffs')

@login_required
def staffs(request):
    # faqat superuser barcha xodimlar ro'yxatini ko'radi
    if request.user.is_superuser:
        staff_list = Staff.objects.all()
    else:
        # Faqat login qilgan xodim ko'rsatilsin
        staff_list = Staff.objects.filter(user=request.user)

    return render(request, 'stuffs.html', {'staff_list': staff_list})



def add_staff(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        name = request.POST.get('name')
        phone = request.POST.get('phone')
        bank_account = request.POST.get('bank_account')
        image = request.FILES.get('image')

        # Foydalanuvchi mavjudligini tekshirish
        if User.objects.filter(username=username).exists():
            messages.error(request, "Bu username allaqachon mavjud! Boshqa username tanlang.")
            return render(request, 'add_staff.html')

        # Foydalanuvchini yaratish
        is_staff = role == 'staff'
        is_superuser = role == 'superuser'

        user = User.objects.create_user(
            username=username,
            password=password,
            is_staff=is_staff,
            is_superuser=is_superuser
        )

        # Staff yaratish
        Staff.objects.create(
            user=user,
            name=name,
            phone=phone,
            bank_account=bank_account,
            image=image
        )

        messages.success(request, "Xodim muvaffaqiyatli qo'shildi!")
        return redirect('stuffs')

    return render(request, 'add_staff.html')


@login_required
def days(request):
    days = Day.objects.all()
    day_details = []

    for day in days:
        work_times = WorkTime.objects.filter(day=day).select_related('staff')
        staff_names = [wt.staff.name for wt in work_times]
        day_details.append({
            'date': day.date,
            'staff_names': staff_names
        })

    return render(request, 'day.html', {'day_details': day_details})


@login_required
def day_detail(request, year, month, day):
    date = datetime.date(year, month, day)
    details = WorkTime.objects.filter(date=date)

    return render(request, 'day_detail.html', {
        'date': date,
        'details': details,
    })



@login_required
def staff_detail(request, staff_id):
    # Staffni olish
    staff = get_object_or_404(Staff, id=staff_id)

    # Cheklash: Agar foydalanuvchi superuser bo'lmasa va ma'lumot unga tegishli bo'lmasa
    if not request.user.is_superuser and staff.user != request.user:
        return redirect('stuffs')  # Kirish huquqi yo'q bo'lsa, foydalanuvchilar sahifasiga qaytadi

    # Ish vaqtlarini olish
    worktimes = WorkTime.objects.filter(staff=staff).order_by('-date')

    # Filtr: Foydalanuvchi parametr orqali boshlanish va tugash sanasini bersa
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            worktimes = worktimes.filter(date__range=(start_date_obj, end_date_obj))
        except ValueError:
            pass  # Agar noto'g'ri sana format kiritilsa, filtr qo'llanmaydi

    # Total hours hisoblash
    total_hours = sum([wt.total_hours for wt in worktimes])

    # Vaqtni formatlash
    hours = int(total_hours)
    minutes = int((total_hours - hours) * 60)
    formatted_time = f"{hours} soat {minutes} daqiqa"

    return render(request, 'staff_detail.html', {
        'staff': staff,
        'worktimes': worktimes,
        'total_hours': total_hours,
        'formatted_time': formatted_time,
    })

