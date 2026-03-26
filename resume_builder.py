from fpdf import FPDF

# 1. ADD THIS HELPER FUNCTION
def safe_encode(text):
    if not text: return ""
    # This converts "smart" characters into standard ones that FPDF can handle
    return str(text).encode('latin-1', 'replace').decode('latin-1')

class ResumePDF(FPDF):
    def header(self):
        self.set_font('Times', 'B', 15)
        self.set_text_color(0, 51, 102)

def generate_resume_pdf(data):
    pdf = ResumePDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Times", 'B', 20)
    pdf.cell(0, 10, safe_encode(data['name']), ln=True, align='C')
    pdf.set_font("Times", '', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 5, f"{safe_encode(data['email'])} | {safe_encode(data['phone'])}", ln=True, align='C')
    pdf.ln(10)

    sections = [
        ("Professional Summary", data['summary']),
        ("Technical Skills", data['skills']),
        ("Experience", data['experience']),
        ("Projects", data['projects']),
        ("Education", data['education']),
        ("Certifications", data['certs'])
    ]

    # Inside generate_resume_pdf in resume_builder.py
    # ... existing header code ...
    
    pdf.set_font("Times", 'B', 12)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 10, "KEY PROJECTS", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    for i in range(1, 4):
        title = data.get(f'p{i}_title')
        date = data.get(f'p{i}_date')
        info = data.get(f'p{i}_info')
        
        if title:
            pdf.set_font("Times", 'B', 10)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(140, 6, safe_encode(title), ln=0)
            pdf.set_font("Times", 'I', 10)
            pdf.cell(50, 6, safe_encode(date), ln=1, align='R')
            pdf.set_font("Times", '', 10)
            pdf.multi_cell(0, 5, safe_encode(info))
            pdf.ln(2)

    for title, content in sections:
        pdf.set_font("Times", 'B', 12)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 10, title.upper(), ln=True)
        pdf.set_draw_color(0, 51, 102)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(2)
        pdf.set_font("Times", '', 10)
        pdf.set_text_color(0, 0, 0)
        
        # 2. UPDATE THIS LINE TO USE SAFE_ENCODE
        pdf.multi_cell(0, 5, safe_encode(content)) 
        pdf.ln(5)

    output_path = f"uploads/{data['name']}_resume.pdf"
    pdf.output(output_path)
    return output_path