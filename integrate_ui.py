import os

base_dir = r'c:\Users\Mahes\Desktop\DEVELOPMENT\PYTHON\odoo hackathon practice\Team-Project-1\facultyerp\frontend_ui\stitch_ai_driven_faculty_management_system'
templates_dir = r'c:\Users\Mahes\Desktop\DEVELOPMENT\PYTHON\odoo hackathon practice\Team-Project-1\facultyerp\core\templates\core'

mapping = {
    'main_dashboard_academia_ai': 'dashboard.html',
    'attendance_analytics_academia_ai': 'ai_analytics.html',
    'assignments_grading_academia_ai': 'assignments.html', # We'll need to manually fix evaluate vs assignments
    'timetable_optimization_academia_ai': 'timetable.html',
    'report_card_generator_academia_ai': 'academic_report.html',
    'parent_communication_academia_ai': 'parent_communication.html',
    'accreditation_assistant_academia_ai': 'accreditation.html',
    'my_productivity_academia_ai': 'faculty_dashboard.html',
    'question_paper_generator_academia_ai': 'generate_questions.html',
    'mark_attendance_academia_ai': 'attendance.html',
    'faculty_login_academia_ai': 'login.html',
    'verify_your_account_academia_ai': 'verify_otp.html'
}

for folder, tmpl in mapping.items():
    code_path = os.path.join(base_dir, folder, 'code.html')
    if not os.path.exists(code_path):
        print(f"Skipping {folder}, no code.html")
        continue
        
    with open(code_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    header_end = content.find('</header>')
    if header_end != -1:
        start_idx = header_end + len('</header>')
    else:
        # Some pages like login might not have header
        main_start = content.find('<main')
        if main_start != -1:
            start_idx = content.find('>', main_start) + 1
        else:
            start_idx = content.find('<body')
            start_idx = content.find('>', start_idx) + 1
            
    end_idx = content.find('</main>')
    if end_idx == -1:
        end_idx = content.find('</body>')
        
    extracted = content[start_idx:end_idx].strip()
    
    # Prepend and append Django tags
    if tmpl not in ['login.html', 'verify_otp.html']:
        final_html = "{% extends 'core/base.html' %}\n{% block content %}\n" + extracted + "\n{% endblock %}"
    else:
        final_html = "{% extends 'core/base.html' %}\n{% block content %}\n" + extracted + "\n{% endblock %}"
        
    out_path = os.path.join(templates_dir, tmpl)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
        
    print(f"Processed {folder} -> {tmpl}")

