import textwrap
from fpdf import FPDF

from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import letter

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def main():
    with open('sample.txt', 'r') as file:
        # Read the contents of the file
        sample_text = file.read()

    print(sample_text)

    # generate_pdf(sample_text, "Sample Subject", "Sample Topic")

    generate_pdf(sample_text, "Sample Subject", "Sample Topic")


def generate_pdf_old(text, subject, topic):
    a4_width_mm = 210
    pt_to_mm = 0.35
    fontsize_pt = 12
    fontsize_mm = fontsize_pt * pt_to_mm
    margin_bottom_mm = 25.4
    character_width_mm = 7 * pt_to_mm
    width_text = (a4_width_mm / character_width_mm)

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(True, margin=margin_bottom_mm)
    pdf.add_page()
    pdf.set_font(family='Times', size=fontsize_pt)

    pdf.set_margins(25.4, 25.4, 25.4)

    filename = "gt_guides/" + subject + " - " + topic + ".pdf"

    final_text = subject + ": " + topic + "\n\n" + text
    # final_text.encode(encoding='utf-8', errors='ignore')
    splitted = final_text.split('\n')

    for line in splitted:
        # line.encode('utf-16', 'replace').decode('utf-16')
        lines = textwrap.wrap(line, width_text)

        if len(lines) == 0:
            pdf.ln()

        for wrap in lines:
            pdf.cell(0, fontsize_mm, wrap, ln=1)

    pdf.output(filename, 'F')


def generate_pdf(text, subject, topic):
    # Create a new PDF with ReportLab

    document = []
    finaltext = text.encode('utf-8')

    # Title
    style_temp = getSampleStyleSheet()
    title_style = ParagraphStyle('Style1',
                                 fontName="Times-Bold",
                                 fontSize=14,
                                 parent=style_temp['Normal'],
                                 alignment=TA_CENTER,
                                 spaceAfter=30)
    document.append(Paragraph(subject + ": " + topic, title_style))
    document.append(Spacer(1, 5))

    code_mode = False
    for line in finaltext.splitlines():
        decoded_line = line.decode()

        char_array = list(decoded_line)
        num_spaces = 0

        for index, value in enumerate(char_array):
            if value == ' ':
                num_spaces = num_spaces + 1
            else:
                break

        print(num_spaces)
        font = ''
        size = 12
        spacer = 5

        if code_mode:
            font = "Courier"
            size = 11
            spacer = 3
        else:
            font = "Times"
            size = 12
            spacer = 9

        paragraph_style = ParagraphStyle('Style1',
                                         fontName=font,
                                         fontSize=size,
                                         leftIndent=12 * num_spaces)

        if decoded_line.lower().__contains__("start of code"):
            code_mode = True
            # do it for the comment as well
            font = "Courier"
            size = 11
            spacer = 3
            paragraph_style = ParagraphStyle('Style1',
                                             fontName=font,
                                             fontSize=size,
                                             leftIndent=12 * num_spaces)

        elif decoded_line.lower().__contains__("end of code"):
            code_mode = False

        document.append(Spacer(1, spacer))

        document.append(Paragraph(decoded_line, paragraph_style))

    SimpleDocTemplate("gt_guides/" + subject + " - " + topic + ".pdf", pagesize=letter, rightMargin=50.5,
                      leftMargin=50.5, topMargin=50.5,
                      bottomMargin=50.5).build(document)


if __name__ == "__main__":
    main()
