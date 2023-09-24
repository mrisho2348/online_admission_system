from django.http import HttpResponse
from django.template.loader import get_template
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def generate_pdf(request):
    # Create a context dictionary with field values
    context = {
        'first_name': '______________________',
        'last_name': 'Doe',
        # Add other fields here
    }

    # Create a response object with PDF MIME type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="student_form.pdf"'

    # Create a PDF document using reportlab
    doc = SimpleDocTemplate(response, pagesize=letter)

    # Create a table to layout the form fields and placeholders
    data = []
    data.append(['First Name:', context.get('first_name', '')])
    data.append(['Last Name:', context.get('last_name', '')])
    # Add other fields and values to the table

    # Define table style to add underlines
    table_style = [
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('TEXTFONT', (0, 0), (-1, -1), 'Helvetica'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]

    # Create the table and apply the style
    student_table = Table(data)
    student_table.setStyle(TableStyle(table_style))

    # Build the PDF document
    elements = []
    elements.append(student_table)
    doc.build(elements)

    return response
