import openai
import requests

import textwrap
from fpdf import FPDF
import re
import time

from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import letter

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

API_KEY = "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"
model_engine = "text-davinci-003"

def main():
    # Set the API key and model
    openai.api_key = API_KEY
    temperature = 1

    subjects = open('topics2.txt', 'r')

    current_subject = ""
    list_of_topics = []
    current_topic = ""

    subject_pattern = re.compile("(.+):")
    topic_pattern = re.compile("(\"|')([\w\s']+),?('|\")")

    for line in subjects.readlines():
        list_of_topics.clear()

        subjects = subject_pattern.finditer(line)
        for subject in subjects:
            current_subject = subject.group(1)

        topics = topic_pattern.finditer(line)
        for topic in topics:
            list_of_topics.append(topic.group(2))


        for index, topic in enumerate(list_of_topics):
            current_topic = list_of_topics[index]
            if "CS" in current_subject:
                prompt = "Act as if you are a student studying for your final exams. Write very detailed lecture notes on " + current_topic + " for the course " + current_subject + ". Please include coding examples, key concepts, and definitions within the notes. Be descriptive and thorough in your notes. For every coding example, start with a comment saying Start of Code and end it with a comment saying End of Code."
            elif "MATH" in current_subject or "PHYS" in current_subject or "CHEM" in current_subject or "CEE" in current_subject or "ECE" in current_subject or "AE" in current_subject or "ME" in current_subject or "BIOL" in current_subject:
                prompt = "Act as if you are a student studying for your final exams. Write a very detailed study guide on " + current_topic + " for the course " + current_subject + ". Please include relevant equations, key concepts, definitions, and rules when possible. Be descriptive and thorough in your notes."
            else:
                prompt = "Act as if you are a student studying for your final exams. Write very detailed lecture notes on " + current_topic + " for the course " + current_subject + ". Please include relevant key concepts, definitions, rules, and examples within the notes. Be descriptive and thorough in your notes."
                #prompt = "Write a long free response coding test that is about " + current_topic + " for " + current_subject + " with an answer key at the end. Write the questions as code."

            response = openai.Completion.create(
                engine=model_engine,
                prompt=prompt,
                temperature=0.3,
                max_tokens=3800,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0.5
            )

            # Get the generated text and generate PDF
            try:
                generated_text = response["choices"][0]["text"]
                generate_pdf(generated_text, current_subject, current_topic)
                print("Successfully Generated " + current_subject + ": " + current_topic)
            except:
                print("Failed to Generate " + current_subject + ": " + current_topic)

            #time.sleep(10)

    # Print the generated text
    # print(generated_text)


def topic_generator(subject):
    # Set the API key and model
    openai.api_key = API_KEY

    prompt = "Create a list of topics you would study in a " + subject + " course in a bulleted format."

    # Make the request to the API
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        temperature=0,
        max_tokens=750,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Get the generated text
    generated_text = response["choices"][0]["text"]

    topic_pattern = re.compile(("(.)\s?(.+)"))
    topics_found = topic_pattern.finditer(generated_text)
    topics = []
    for topic in topics_found:
        topics.append(topic.group(2).strip())

    return topics


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