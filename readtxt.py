import openai
import requests
import re

subjects = open('topics.txt', 'r')

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

    print(current_subject + ": " + str(list_of_topics))
