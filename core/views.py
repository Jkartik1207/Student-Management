import os
import random
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Faculty, Student, Attendance, Marks, Assignment, AssignmentSubmission, Notification, ParentCommunication
from django.contrib import messages
import google.generativeai as genai
from django.http import JsonResponse
import json

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(user, otp):
    send_mail(
        'Your OTP for Faculty ERP',
        f'Your OTP code is {otp}. It is valid for 10 minutes.',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        department = request.POST.get('department')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'core/signup.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'core/signup.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        otp = generate_otp()
        faculty = Faculty.objects.create(
            user=user, 
            name=name, 
            department=department, 
            otp_code=otp, 
            otp_created_at=timezone.now()
        )
        send_otp_email(user, otp)
        request.session['verify_user_id'] = user.id
        return redirect('verify_otp')
        
    return render(request, 'core/signup.html')

def verify_otp(request):
    user_id = request.session.get('verify_user_id')
    if not user_id:
        return redirect('login')
        
    user = get_object_or_404(User, id=user_id)
    faculty = user.faculty

    if request.method == 'POST':
        if 'resend' in request.POST:
            otp = generate_otp()
            faculty.otp_code = otp
            faculty.otp_created_at = timezone.now()
            faculty.save()
            send_otp_email(user, otp)
            messages.success(request, "A new OTP has been sent.")
            return redirect('verify_otp')

        otp_input = request.POST.get('otp')
        if faculty.otp_code == otp_input:
            if timezone.now() < faculty.otp_created_at + timedelta(minutes=10):
                faculty.is_verified = True
                faculty.save()
                del request.session['verify_user_id']
                messages.success(request, "Account verified! You can now log in.")
                return redirect('login')
            else:
                messages.error(request, "OTP has expired. Please request a new one.")
        else:
            messages.error(request, "Invalid OTP.")
            
    return render(request, 'core/verify_otp.html', {'email': user.email})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if hasattr(user, 'faculty'):
                if not user.faculty.is_verified:
                    request.session['verify_user_id'] = user.id
                    return redirect('verify_otp')
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "This login page is for faculty. Please use the student portal.")
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'core/login.html')

def student_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if hasattr(user, 'student'):
                login(request, user)
                return redirect('student_dashboard')
            else:
                messages.error(request, "This login page is for students. Please use the faculty portal.")
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'core/student_login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    batch_filter = request.GET.get('batch', 'All')
    students = Student.objects.all()
    if batch_filter != 'All':
        students = students.filter(batch=batch_filter)
        
    batches = Student.objects.values_list('batch', flat=True).distinct()
    
    student_stats = []
    for student in students:
        total_attendance = Attendance.objects.filter(student=student).count()
        present_attendance = Attendance.objects.filter(student=student, status='Present').count()
        attendance_percentage = (present_attendance / total_attendance * 100) if total_attendance > 0 else 0
        
        marks = Marks.objects.filter(student=student)
        total_marks = sum([m.marks_obtained for m in marks])
        avg_marks = (total_marks / marks.count()) if marks.count() > 0 else 0
        
        student_stats.append({
            'student': student,
            'attendance_percentage': round(attendance_percentage, 2),
            'avg_marks': round(avg_marks, 2)
        })
        
    return render(request, 'core/dashboard.html', {
        'student_stats': student_stats,
        'batches': batches,
        'selected_batch': batch_filter,
        'total_students': students.count(),
        'total_faculty': Faculty.objects.count()
    })

@login_required
def attendance_view(request):
    batch_filter = request.GET.get('batch', 'All')
    students = Student.objects.all()
    if batch_filter != 'All':
        students = students.filter(batch=batch_filter)
        
    batches = Student.objects.values_list('batch', flat=True).distinct()
    today = timezone.now().date()
    
    if request.method == 'POST':
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            if status in ['Present', 'Absent']:
                Attendance.objects.update_or_create(
                    student=student,
                    date=today,
                    defaults={'status': status, 'marked_by': request.user.faculty}
                )
        messages.success(request, "Attendance saved successfully.")
        return redirect(f"{request.path}?batch={batch_filter}")
        
    # Pre-fetch today's attendance to populate the form
    today_attendance = {
        a.student_id: a.status 
        for a in Attendance.objects.filter(date=today, student__in=students)
    }
    
    return render(request, 'core/attendance.html', {
        'students': students,
        'batches': batches,
        'selected_batch': batch_filter,
        'today': today,
        'today_attendance': today_attendance
    })

@login_required
def generate_questions(request):
    generated_text = None
    
    if request.method == 'POST':
        subject = request.POST.get('subject')
        topic = request.POST.get('topic')
        difficulty = request.POST.get('difficulty')
        marks = request.POST.get('marks', '50')
        
        prompt = f"""Generate exactly 5 {difficulty} questions about {topic} for the subject {subject}. 
The total marks for this assessment are {marks}. 
CRITICAL INSTRUCTION: You must ONLY output raw HTML. Do NOT use markdown formatting (NO asterisks ** for bold, NO backticks ` for code). 
Use standard HTML tags for all formatting: <strong> for bold, <code> for code snippets, <p> for paragraphs, and <br> for line breaks.
Format the overall output strictly as an ordered list using <ol class="list-decimal pl-6 space-y-8 text-lg"> and <li class="pl-2"> tags.
Each <li> should contain the question text appropriately formatted with HTML, followed by a <span class="block text-sm text-gray-500 mt-3 font-semibold"> (Marks: [X])</span> indicating the marks for that question."""
        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            messages.error(request, "GEMINI_API_KEY environment variable is not set.")
        else:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(
                    'gemini-2.5-flash',
                    system_instruction="You are a helpful assistant for creating academic questions."
                )
                response = model.generate_content(prompt)
                generated_text = response.text
                if generated_text.strip().startswith("```html"):
                    generated_text = generated_text.strip().removeprefix("```html")
                    if generated_text.strip().endswith("```"):
                        generated_text = generated_text.strip().removesuffix("```")
            except Exception as e:
                messages.error(request, f"Error generating questions: {str(e)}")
                
    return render(request, 'core/generate_questions.html', {
        'generated_text': generated_text,
        'subject': request.POST.get('subject', '') if request.method == 'POST' else '',
        'topic': request.POST.get('topic', '') if request.method == 'POST' else '',
        'difficulty': request.POST.get('difficulty', 'Medium') if request.method == 'POST' else 'Medium',
        'marks': request.POST.get('marks', '50') if request.method == 'POST' else '50'
    })
def get_gemini_response(prompt):
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        return 'GEMINI_API_KEY environment variable is not set.'
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    return response.text

@login_required
def ai_analytics(request):
    analytics_report = None
    if request.method == 'POST':
        batch_filter = request.POST.get('batch', 'All')
        students = Student.objects.all()
        if batch_filter != 'All':
            students = students.filter(batch=batch_filter)
        
        data_summary = []
        for s in students:
            total = Attendance.objects.filter(student=s).count()
            present = Attendance.objects.filter(student=s, status='Present').count()
            data_summary.append(f"{s.name}: {present}/{total} days present.")
        
        prompt = f"Analyze this attendance data for students and identify any at-risk students who might be falling behind on attendance, along with a brief summary: {', '.join(data_summary)}"
        analytics_report = get_gemini_response(prompt)
        
    batches = Student.objects.values_list('batch', flat=True).distinct()
    
    # We must also fetch the currently filtered students to pass to the template
    batch_filter = request.POST.get('batch', 'All') if request.method == 'POST' else request.GET.get('batch', 'All')
    students = Student.objects.all()
    if batch_filter != 'All':
        students = students.filter(batch=batch_filter)
        
    return render(request, 'core/ai_analytics.html', {
        'analytics_report': analytics_report, 
        'batches': batches, 
        'selected_batch': batch_filter,
        'students': students
    })

@login_required
def assignments_list(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        max_marks = request.POST.get('max_marks', 100)
        due_date = request.POST.get('due_date')
        creation_type = request.POST.get('creation_type')
        
        assignment = Assignment(
            title=title,
            max_marks=max_marks,
            due_date=due_date,
            created_by=request.user.faculty
        )
        
        if creation_type == 'ai':
            topic = request.POST.get('topic')
            prompt = f"Generate a comprehensive assignment description for the topic '{topic}'. Provide a clear objective, questions/tasks, and expected deliverables."
            description = get_gemini_response(prompt)
            assignment.description = description
            assignment.save()
            messages.success(request, "Assignment generated by AI and saved successfully!")
        
        elif creation_type == 'upload':
            description = request.POST.get('description', '')
            assignment_file = request.FILES.get('assignment_file')
            assignment.description = description
            if assignment_file:
                assignment.assignment_file = assignment_file
            assignment.save()
            messages.success(request, "Assignment uploaded successfully!")
            
    assignments = Assignment.objects.all().order_by('-created_at')
    return render(request, 'core/assignments.html', {'assignments': assignments})

@login_required
def evaluate_assignment(request, pk):
    from django.shortcuts import get_object_or_404
    assignment = get_object_or_404(Assignment, pk=pk)
    submissions = AssignmentSubmission.objects.filter(assignment=assignment)
    
    if request.method == 'POST':
        sub_id = request.POST.get('submission_id')
        submission = get_object_or_404(AssignmentSubmission, pk=sub_id)
        
        prompt = f"Evaluate the following student submission for the assignment '{assignment.title}'. Description: '{assignment.description}'. Max Marks: {assignment.max_marks}. Submission text: '{submission.submitted_text}'. Provide a score out of {assignment.max_marks} and brief feedback. Format exactly as: 'Score: [number]\nFeedback: [text]'"
        ai_response = get_gemini_response(prompt)
        
        try:
            score_line = [line for line in ai_response.split('\n') if 'Score:' in line][0]
            score = int(''.join(filter(str.isdigit, score_line)))
            submission.ai_score = min(score, assignment.max_marks)
            submission.ai_feedback = ai_response
            submission.save()
            Notification.objects.create(faculty=request.user.faculty, message=f"Evaluated {submission.student.name}'s assignment.")
            messages.success(request, f"Evaluated {submission.student.name}")
        except Exception as e:
            messages.error(request, f"Failed to parse AI response: {e}")
            
    return render(request, 'core/evaluate_assignment.html', {'assignment': assignment, 'submissions': submissions})

@login_required
def timetable_view(request):
    timetable = None
    if request.method == 'POST':
        constraints = request.POST.get('constraints')
        prompt = f"Generate a 5-day academic timetable (Monday-Friday) based on these constraints: {constraints}. STRICTLY format the output as a clean HTML <table> with classes 'w-full text-left border-collapse'. Do NOT wrap it in markdown code blocks. Include headers for Monday to Friday."
        timetable = get_gemini_response(prompt)
        if timetable.strip().startswith("```html"):
            timetable = timetable.strip().removeprefix("```html")
            if timetable.strip().endswith("```"):
                timetable = timetable.strip().removesuffix("```")
    return render(request, 'core/timetable.html', {'timetable': timetable})

@login_required
def academic_report(request):
    from django.shortcuts import get_object_or_404
    students = Student.objects.all()
    report = None
    selected_student = None
    
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        selected_student = get_object_or_404(Student, pk=student_id)
        
        total = Attendance.objects.filter(student=selected_student).count()
        present = Attendance.objects.filter(student=selected_student, status='Present').count()
        absent = total - present
        attendance_percentage = int((present / total * 100)) if total > 0 else 0
        attendance_offset = 364.4 - (364.4 * attendance_percentage / 100)
        
        marks = Marks.objects.filter(student=selected_student)
        marks_str = ", ".join([f"{m.subject}: {m.marks_obtained}/{m.max_marks}" for m in marks])
        
        # Calculate grade for each mark
        marks_list = []
        for m in marks:
            score = (m.marks_obtained / m.max_marks * 100) if m.max_marks > 0 else 0
            if score >= 90: grade, status = 'A+', 'Distinction'
            elif score >= 80: grade, status = 'A', 'Distinction'
            elif score >= 70: grade, status = 'B+', 'Passed'
            elif score >= 60: grade, status = 'B', 'Passed'
            elif score >= 50: grade, status = 'C', 'Passed'
            else: grade, status = 'F', 'Failed'
            
            marks_list.append({
                'subject': m.subject,
                'obtained': m.marks_obtained,
                'max': m.max_marks,
                'grade': grade,
                'status': status,
                'status_color': 'bg-green-100 text-green-800' if status != 'Failed' else 'bg-error text-white'
            })
        
        prompt = f"Write a professional end-of-semester academic report for {selected_student.name}. Attendance: {present}/{total} days. Marks: {marks_str}. Provide personalized encouraging feedback in HTML format. Do NOT wrap the response in markdown code blocks."
        report = get_gemini_response(prompt)
        if report.strip().startswith("```html"):
            report = report.strip().removeprefix("```html")
            if report.strip().endswith("```"):
                report = report.strip().removesuffix("```")
        
        return render(request, 'core/academic_report.html', {
            'students': students, 
            'report': report, 
            'selected_student': selected_student,
            'marks_list': marks_list,
            'total_attendance': total,
            'present_attendance': present,
            'absent_attendance': absent,
            'attendance_percentage': attendance_percentage,
            'attendance_offset': attendance_offset
        })
        
    return render(request, 'core/academic_report.html', {'students': students, 'report': report, 'selected_student': selected_student})

@login_required
def parent_communication(request):
    from django.shortcuts import get_object_or_404
    students = Student.objects.all()
    draft = None
    
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        tone = request.POST.get('tone')
        student = get_object_or_404(Student, pk=student_id)
        
        total = Attendance.objects.filter(student=student).count()
        present = Attendance.objects.filter(student=student, status='Present').count()
        
        prompt = f"Draft a {tone} email to the parents of {student.name} regarding their academic progress. They have attended {present} out of {total} days."
        draft = get_gemini_response(prompt)
        
        if 'send' in request.POST:
            ParentCommunication.objects.create(student=student, subject=f"Academic Update - {student.name}", message_body=draft)
            messages.success(request, "Communication logged successfully.")
            
    return render(request, 'core/parent_communication.html', {'students': students, 'draft': draft})

@login_required
def accreditation_view(request):
    report = None
    if request.method == 'POST':
        total_students = Student.objects.count()
        total_faculty = Faculty.objects.count()
        prompt = f"Draft an accreditation overview (NAAC/NBA style) for a department with {total_faculty} faculty members and {total_students} students. Mention our focus on AI-driven analytics."
        report = get_gemini_response(prompt)
    return render(request, 'core/accreditation.html', {'report': report})

@login_required
def ai_chat_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            if not user_message:
                return JsonResponse({'error': 'Message is required'}, status=400)
            
            prompt = f"The user is asking a question in a faculty/student academic portal context: {user_message}\nProvide a concise and helpful response."
            reply = get_gemini_response(prompt)
            
            return JsonResponse({'reply': reply})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def faculty_dashboard(request):
    faculty = request.user.faculty
    assignments = Assignment.objects.filter(created_by=faculty).count()
    notifications = Notification.objects.filter(faculty=faculty).order_by('-created_at')[:5]
    
    return render(request, 'core/faculty_dashboard.html', {'assignments_count': assignments, 'notifications': notifications})

def student_signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        roll_number = request.POST.get('roll_number')
        username = request.POST.get('username')
        password = request.POST.get('password')
        batch = request.POST.get('batch')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'core/student_signup.html')
            
        user = User.objects.create_user(username=username, password=password)
        Student.objects.create(user=user, name=name, roll_number=roll_number, batch=batch)
        messages.success(request, "Student account created! You can now log in.")
        return redirect('student_login')
    return render(request, 'core/student_signup.html')

@login_required
def student_dashboard(request):
    if not hasattr(request.user, 'student'):
        return redirect('dashboard')
    
    student = request.user.student
    total_classes = Attendance.objects.filter(student=student).count()
    present_classes = Attendance.objects.filter(student=student, status='Present').count()
    attendance_pct = (present_classes / total_classes * 100) if total_classes > 0 else 0
    
    marks = Marks.objects.filter(student=student)
    
    return render(request, 'core/student_dashboard.html', {
        'student': student,
        'attendance_pct': round(attendance_pct, 2),
        'marks': marks
    })

@login_required
def student_assignments(request):
    if not hasattr(request.user, 'student'):
        return redirect('dashboard')
        
    student = request.user.student
    assignments = Assignment.objects.all().order_by('-created_at')
    
    return render(request, 'core/student_assignments.html', {
        'student': student,
        'assignments': assignments
    })

@login_required
def student_report(request):
    if not hasattr(request.user, 'student'):
        return redirect('dashboard')
        
    student = request.user.student
    total_classes = Attendance.objects.filter(student=student).count()
    present_classes = Attendance.objects.filter(student=student, status='Present').count()
    attendance_pct = (present_classes / total_classes * 100) if total_classes > 0 else 0
    attendance_offset = 364.4 - (364.4 * attendance_pct / 100)
    
    marks = Marks.objects.filter(student=student)
    marks_list = []
    for m in marks:
        score = (m.marks_obtained / m.max_marks * 100) if m.max_marks > 0 else 0
        if score >= 90: grade, status = 'A+', 'Distinction'
        elif score >= 80: grade, status = 'A', 'Distinction'
        elif score >= 70: grade, status = 'B+', 'Passed'
        elif score >= 60: grade, status = 'B', 'Passed'
        elif score >= 50: grade, status = 'C', 'Passed'
        else: grade, status = 'F', 'Failed'
        
        marks_list.append({
            'subject': m.subject,
            'obtained': m.marks_obtained,
            'max': m.max_marks,
            'grade': grade,
            'status': status,
            'status_color': 'bg-green-100 text-green-800' if status != 'Failed' else 'bg-error text-white'
        })
        
    return render(request, 'core/student_report.html', {
        'student': student,
        'marks_list': marks_list,
        'total_attendance': total_classes,
        'present_attendance': present_classes,
        'absent_attendance': total_classes - present_classes,
        'attendance_percentage': int(attendance_pct),
        'attendance_offset': attendance_offset
    })
