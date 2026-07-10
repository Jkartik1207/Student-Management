import os

source_path = r'c:\Users\Mahes\Desktop\DEVELOPMENT\PYTHON\odoo hackathon practice\Team-Project-1\facultyerp\frontend_ui\stitch_ai_driven_faculty_management_system\main_dashboard_academia_ai\code.html'
dest_path = r'c:\Users\Mahes\Desktop\DEVELOPMENT\PYTHON\odoo hackathon practice\Team-Project-1\facultyerp\core\templates\core\base.html'

with open(source_path, 'r', encoding='utf-8') as f:
    content = f.read()

header_end = content.find('<!-- Content Grid -->')
if header_end == -1:
    header_end = content.find('<div class="p-lg')

base_content = content[:header_end] + '''
    {% if messages %}
        <div class="px-lg py-sm">
            {% for message in messages %}
                <div class="p-4 mb-4 text-sm {% if message.tags == 'error' %}text-red-800 bg-red-50{% else %}text-green-800 bg-green-50{% endif %} rounded-lg" role="alert">
                    {{ message }}
                </div>
            {% endfor %}
        </div>
    {% endif %}

    {% block content %}
    {% endblock %}
</main>
</div>
</body>
</html>
'''

with open(dest_path, 'w', encoding='utf-8') as f:
    f.write(base_content)

print('base.html created')
