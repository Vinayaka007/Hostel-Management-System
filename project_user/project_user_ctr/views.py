from django.http import HttpResponse
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.http import HttpResponse, JsonResponse
from .models import Register, HostelApp
from .forms import HostelApplicationForm
from .forms import AdminLoginForm, ComplaintBoxForm, NoticeForm
from .models import AdminLog, Register, RoomAllot, HostelApp, ComplaintBox, Notice





def index_page(request):
    return HttpResponse(render(request, "index.html"))

def base_page(request):
    return HttpResponse(render(request, "base.html"))

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success') 
        else:
            return render(request, 'register.html', {'form': form, 'error_message': 'Form submission failed. Please check your data.'})
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register.html', {'form': form})

def success_page(request):
    return render(request, 'success.html')


def logout_view():
    return render("")




def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            reg_no = form.cleaned_data['reg_no']
            password = form.cleaned_data['password']
            try:
                user = Register.objects.get(reg_no=reg_no)
                if user.password == password:
                    request.session['user_id'] = user.id
                    return redirect('user_index') 
                else:
                    messages.error(request, 'Invalid registration number or password')
            except Register.DoesNotExist:
                messages.error(request, 'Invalid registration number or password')
        else:
            messages.error(request, 'Invalid form submission')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})




def user_index(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = Register.objects.get(id=user_id)
            return render(request, 'user_index.html', {'user': user})
        except Register.DoesNotExist:
            messages.error(request, 'User not found')
            request.session.flush()
            return redirect('login')
    else:
        messages.error(request, 'User not logged in')
        return redirect('login')



def student_page(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = Register.objects.get(id=user_id)
            return render(request, 'student_page.html', {'user': user})
        except Register.DoesNotExist:
            messages.error(request, 'User not found')
            request.session.flush()
            return redirect('login')
    else:
        messages.error(request, 'User not logged in')
        return redirect('login')





def generate_pdf(data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []

    
    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleN.fontName = 'Helvetica'
    styleN.fontSize = 8 

    
    title_style = ParagraphStyle(name='TitleStyle', fontSize=16, alignment=1)
    title = Paragraph('Hostel Application', title_style)
    story.append(title)

   
    story.append(Paragraph('<br/><br/>', styles['Normal']))

    
    table_data = [
        ['Full Name', data.get('full_name', 'N/A')],
        ['Father\'s Name', data.get('father_name', 'N/A')],
        ['Mobile No', data.get('mobile_no', 'N/A')],
        ['Email', data.get('email', 'N/A')],
        ['Address', data.get('address', 'N/A')],
        ['Institution', data.get('institution', 'N/A')],
        ['Course', data.get('course', 'N/A')],
        ['Registration No', data.get('reg_no', 'N/A')],
        ['Academic Year', data.get('ac_year', 'N/A')],
        ['Course Year', data.get('course_year', 'N/A')],
        ['Mother\'s Name', data.get('mother_name', 'N/A')],
        ['Occupation', data.get('occupation', 'N/A')],
        ['Landline Number', data.get('landline_num', 'N/A')],
        ['Emergency Contact', data.get('emergency_contact', 'N/A')],
        ['Father\'s Email', data.get('father_email', 'N/A')],
    ]

    table = Table(table_data, colWidths=[200, 300])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),  
        ('TEXTCOLOR', (0, 0), (-1, 0), (0, 0, 0)),  
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 1, (0, 0, 0)),  
        ('GRID', (0, 0), (-1, -1), 0.5, (0, 0, 0)),  
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),  
        ('FONTSIZE', (0, 0), (-1, -1), 8),  
    ]))

    
    story.append(table)

    
    doc.build(story)

    buffer.seek(0)
    return buffer







def apply_for_hostel(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'User not logged in')
        return redirect('login')

    try:
        user = Register.objects.get(id=user_id)
    except Register.DoesNotExist:
        messages.error(request, 'User not found')
        request.session.flush()
        return redirect('login')

    if request.method == "POST":
        form = HostelApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            hostel_application = form.save(commit=False)
            hostel_application.user = user
            hostel_application.full_name = user.full_name
            hostel_application.father_name = user.father_name
            hostel_application.mobile_no = user.mobile_no
            hostel_application.email = user.email
            hostel_application.address = user.address
            hostel_application.institution = user.institution
            hostel_application.course = user.course
            hostel_application.reg_no = user.reg_no
            hostel_application.save()

            user_details = {
                'full_name': hostel_application.full_name,
                'father_name': hostel_application.father_name,
                'mobile_no': hostel_application.mobile_no,
                'email': hostel_application.email,
                'address': hostel_application.address,
                'institution': hostel_application.institution,
                'course': hostel_application.course,
                'reg_no': hostel_application.reg_no,
                'ac_year': hostel_application.ac_year,
                'course_year': hostel_application.course_year,
                'mother_name': hostel_application.mother_name,
                'occupation': hostel_application.occupation,
                'landline_num': hostel_application.landline_num,
                'emergency_contact': hostel_application.emergency_contact,
                'father_email': hostel_application.father_email,
            }
            
            pdf_buffer = generate_pdf(user_details)
            response = HttpResponse(pdf_buffer, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="hostel_application.pdf"'
            messages.success(request, 'Your application has been successfully submitted!')
            return JsonResponse({'pdf': response.content.decode('latin1')})

        else:
            messages.error(request, 'Form is not valid. Please correct the errors.')
    else:
        form = HostelApplicationForm(initial={
            'full_name': user.full_name,
            'father_name': user.father_name,
            'mobile_no': user.mobile_no,
            'email': user.email,
            'address': user.address,
            'institution': user.institution,
            'course': user.course,
            'reg_no': user.reg_no,
        })

    return render(request, 'apply_for_hostel.html', {'form': form, 'user': user})






# views.py

def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            try:
                user = AdminLog.objects.get(user_name=username, password=password)
                request.session['admin_user_id'] = user.id
                request.session['admin_user_name'] = user.user_name
                return redirect('admin_work')
            except AdminLog.DoesNotExist:
                messages.error(request, "Invalid username or password")
    else:
        form = AdminLoginForm()
    
    return render(request, 'admin_login.html', {'form': form})

def complaint_box(request):
    if request.method == 'POST':
        form = ComplaintBoxForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('complaint_success')
    else:
        user_id = request.session.get('user_id')
        if user_id:
            try:
                user = Register.objects.get(id=user_id)
                user_data = {
                    'name': user.full_name,
                    'email': user.email,
                    'phone': user.mobile_no,
                    'register_number': user.reg_no,
                }
                form = ComplaintBoxForm(initial=user_data)
            except Register.DoesNotExist:
                form = ComplaintBoxForm()
                messages.error(request, 'User not found')
        else:
            form = ComplaintBoxForm()
    return render(request, 'complaint_box.html', {'form': form})

def complaint_success(request):
    return render(request, 'complaint_success.html')

def room_allotment(request):
    return render(request, 'room_allotment.html')

def get_room_details(request):
    floor = request.GET.get('floor')
    room_number = request.GET.get('room_number')

    rooms = RoomAllot.objects.filter(floor=floor, room_number=room_number)

    response_data = []
    for room in rooms:
        response_data.append({
            'name': room.name,
            'usn': room.usn,
        })

    if not response_data:
        response_data.append({
            'name': 'Not found',
            'usn': 'Not found',
        })

    return JsonResponse(response_data, safe=False)

def hostel_allotment(request):
    floor = request.GET.get('floor')
    room_number = request.GET.get('room_number')

    rooms = RoomAllot.objects.filter(floor=floor, room_number=room_number)

    response_data = []
    for room in rooms:
        response_data.append({
            'name': room.name,
            'usn': room.usn,
        })

    if not response_data:
        response_data.append({
            'name': 'Not found',
            'usn': 'Not found',
        })

    context = {
        'show_footer': False  
    }
    return render(request, 'hostel_allotment.html', context)

def admin_work(request):
    return render(request, 'admin_work.html')

def applicant(request):
    hostel_apps = HostelApp.objects.all()
    return render(request, 'applicant.html', {'hostel_apps': hostel_apps})

def accept_application(request, id):
    application = get_object_or_404(HostelApp, id=id)
    application.status = 'Accepted'
    application.save()
    return redirect('applicant')

def delete_application(request, id):
    application = get_object_or_404(HostelApp, id=id)
    application.delete()
    return redirect('applicant')

from django.shortcuts import render, HttpResponse
from .models import RoomAllot

def admin_room_allotment(request):
    if request.method == 'POST':
        floor = request.POST.get('floor')
        room_number = request.POST.get('room_number')
        num_entries_str = request.POST.get('number-of-forms')

        try:
            num_entries = int(num_entries_str) if num_entries_str else 0
            if num_entries <= 0:
                raise ValueError("Number of entries must be greater than zero")
        except (TypeError, ValueError) as e:
            return HttpResponse("Invalid number of forms")

        for i in range(num_entries):
            name = request.POST.get(f'name-{i}')
            usn = request.POST.get(f'usn-{i}')
            if name and usn:
                RoomAllot.objects.create(
                    floor=floor,
                    room_number=room_number,
                    number_of_entries=num_entries,
                    name=name,
                    usn=usn
                )
    return render(request, 'admin_room_allot.html')


def complaint_list(request):
    complaints = ComplaintBox.objects.all()
    return render(request, 'complaint_list.html', {'complaints': complaints})

from django.shortcuts import render
from .models import Notice

def notice_list_user(request):
    notices = Notice.objects.all().order_by('-created_at')
    return render(request, 'notice_list_user.html', {'notices': notices})


def accept_complaint(request, id):
    complaint = get_object_or_404(ComplaintBox, id=id)
    complaint.status = 'Accepted'
    complaint.save()
    return redirect('complaint_list')

def delete_complaint(request, id):
    complaint = get_object_or_404(ComplaintBox, id=id)
    complaint.delete()
    return redirect('complaint_list')

def post_notice(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            admin_user_id = request.session.get('admin_user_id')
            if admin_user_id:
                notice.author_id = admin_user_id
                notice.save()
                return redirect('notice_list')
            else:
                messages.error(request, "You must be logged in to post a notice")
    else:
        form = NoticeForm()

    return render(request, 'post_notice.html', {'form': form})

def notice_list(request):
    notices = Notice.objects.all()
    return render(request, 'notice_list.html', {'notices': notices})




def delete_notice(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    notice.delete()
    messages.success(request, "Notice deleted successfully.")
    return redirect('notice_list')

def update_notice(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    if request.method == 'POST':
        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            form.save()
            messages.success(request, "Notice updated successfully.")
            return redirect('notice_list')
    else:
        form = NoticeForm(instance=notice)
    return render(request, 'update_notice.html', {'form': form})
