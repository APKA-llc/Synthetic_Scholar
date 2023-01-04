import openai
import requests

import textwrap
import re
import time

API_KEY = "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"
model_engine = "text-davinci-003"


def main():
    # Set the API key and model
    openai.api_key = API_KEY
    temperature = 1

    # Set the prompt and temperature

    # Get the generated text
    # generated_text = response["choices"][0]["text"]

    subjects = open('ListOfClasses.txt', 'r')

    current_subject = ""
    list_of_topics = []
    current_topic = ""

    for line in subjects.readlines():
        time.sleep(5)
        current_subject = repr(line).replace("\\n", "").replace("'", "")
        list_of_topics = topic_generator(current_subject)
        print(current_subject + ":" + str(list_of_topics))
        #print(list_of_topics)

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


def generate_pdf(text, topic, subjec):
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

    final_text = filename + "\n\n" + text
    splitted = final_text.split('\n')

    for line in splitted:
        lines = textwrap.wrap(line, width_text)

        if len(lines) == 0:
            pdf.ln()

        for wrap in lines:
            pdf.cell(0, fontsize_mm, wrap, ln=1)



    pdf.output(filename, 'F')


if __name__ == "__main__":
    main()
