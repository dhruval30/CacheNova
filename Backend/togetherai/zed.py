#Needs to have the following commands:
#cleanprompt = zed.cleanprompt(prompt)

#getsubjects Dependent on cleanprompt

#for each subject
#getsubfields Dependent on subject and cleanprompt
#for each subfield
#threadchaos Dependent on cleanprompt, subject, subfield
import requests
import json
from openai import OpenAI
openai_client = OpenAI()
import random
import string
from gottadealwithfrontend import converter
from pymongo import MongoClient
import threading
client = MongoClient('localhost', 27017)
db = client['Nova']
#subficol = db['subfields']

endpoint = 'https://api.together.xyz/v1/chat/completions'

def cleanprompt(prompt, maxlength=20):
    sysprompt = "You are a prompt generalizer. Your job is to generalize the given prompt to the nearest academic titles and subjects. You will be tipped 20 dollars for the job. Return a string with the academic titles and subjects."
    res = requests.post(endpoint, json={
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "max_tokens": maxlength,
        "prompt": f"<|im_start|>system\n{sysprompt}.<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n",
        "request_type": "language-model-inference",
        "temperature": 0.1,
        "top_p": 0.7,
        "top_k": 50,
        "repetition_penalty": 1,
        "stop": [
            "<|im_start|>",
            "<|im_end>",
            "</s>"
        ],
        "promptObj": {
            "prompt": prompt
        }
    }, headers={
        "Authorization": "Bearer f7e58960014e29d3c334f16508842b8d4ec53debc023f3579812dd9a62ab49e1",
    })
    return res.json()['choices'][0]['message']['content']

def getsubjects(prompt: str) -> list:  #["Physics", "Mathematics", "Chemistry"]
    response = openai_client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    response_format={ "type": "json_object" },
    messages=[
        {"role": "system", "content": "You are a librarian that helps students find books. Your job is to find the most relevant and non-overlapping subjects to the given prompt."},
        {"role": "user", "content": f"The student's prompt is {prompt}. You are supposed to find the most relevant and non-overlapping subjects to the given prompt. The subjects should not be a part of one another. You will be tipped 20 dollars for the job. Return a json with incrementing numbers as keys(starting from 0) and subject names as values."},
    ]
    )
    return list(json.loads(response.choices[0].message.content).values())


def getsubfields(subject, prompt) -> dict:   #{1: "Gravitational Constant", 2: "Gravitational Field", 3: "Gravitational Potential"}
    response = openai_client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    response_format={ "type": "json_object" },
    messages=[
        {"role": "system", "content": "You are a co-writer on a university book. Your job is to provide all of the possible sub-fields of the given subject."},
        {"role": "user", "content": f"You are supposed to write the suitable sub-fields for the subject {subject}. You will be tipped 20 dollars for a thorough job. Return a json object with incrementing numbers as keys(starting from 0) and the names of the section as values."}
    ]
    )
    return list(json.loads(response.choices[0].message.content).values())

def getsubtopics(subfield, subject, prompt) -> dict:   #{1: "Gravitational Constant", 2: "Gravitational Field", 3: "Gravitational Potential"}
    response = openai_client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    response_format={ "type": "json_object" },
    messages=[
        {"role": "system", "content": "You are a co-writer on a university book. Your job is to decide subtopics on a field of the given subject to be put in a book."},
        {"role": "user", "content": f"You are supposed to write all the important subtopics for an academic book on {subfield} of subject {subject}. You will be tipped 20 dollars for the job. Return a json object with incrementing numbers as keys(starting from 0) and the names of the section as values."},
    ]
    )
    return list(json.loads(response.choices[0].message.content).values())

def generate_random_string(length=10):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for i in range(length))

def get_subsections(subject, subfield, subtopic):
    response = openai_client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    response_format={ "type": "json_object" },
    messages=[
        {"role": "system", "content": "You are a co-writer on a university book. Your job is to decide subsections for a chapter that covers every topic important to gaining extremely deep understanding of the topic"},
        {"role": "user", "content": f"You are supposed to write the suitable sub-sections for the sub-chapter {subtopic} for the chapter {subtopic} for the book of {subject}. You will be tipped 20 dollars for the job. Return a json object with incrementing numbers as keys(starting from 0) and the names of the section as values."},
    ]
    )
    return list(json.loads(response.choices[0].message.content).values())


'''

def generatepages(subject:str, subfield:str, subtopics: list, subtopiclinks: list, navbarcontent: list):
    listoflinks_tosubtopicpages=[]
    subficol = db[subfield]
    print(subtopics)
    for subtopic in subtopics:
        #implement the following
        #if subtopic in db:
        #   listoflinks_tosubtopicpages.append({subtopic: db[subtopic]})
        #else:

        filename = subtopiclinks[subtopic]
        with open(f"/Users/ciscorrr/Documents/CisStuff/curr/CacheNova/Backend/mddatacluster/{filename}.md", "w") as md_file:  # Open a markdown file for writing
            subsections = get_subsections(subject, subfield, subtopic)
            for i in range(len(subsections)):
                if i!=len(subsections)-1:
                    sec = subsections[i]
                    res = openai_client.chat.completions.create(
                    model="gpt-3.5-turbo-0125",
                    messages=[
                    {"role": "system", "content": "You are a co-writer on a university book. When asked to write a section, you will write an extremely lengthy, detailed, and well-researched section on the topic, properly formatted with markdown format"},
                    {"role": "user", "content": f"You are a co-writer on a university book. When asked to write a section, you will write a lengthy, detailed, and well-researched section on the topic. You are supposed to write the section {sec} of the main section of the sub-chapter {subtopic} in the chapter of {subfield} for the book of {subject}. End the section by setting up a smooth transition into the next topic: {subsections[i+1]}. Make sure the output is in pure markdown."},
                    ]
                    )
                    md_file.write(res.choices[0].message.content + "\n\n")  # Write the content to the markdown file
                else:
                    sec = subsections[i]
                    res = openai_client.chat.completions.create(
                    model="gpt-3.5-turbo-0125",
                    messages=[
                    {"role": "system", "content": "You are a co-writer on a university book. When asked to write a section, you will write an extremely lengthy, detailed, and well-researched section on the topic, properly formatted with markdown format"},
                    {"role": "user", "content": f"You are a co-writer on a university book. When asked to write a section, you will write a lengthy, detailed, and well-researched section on the topic. You are supposed to write the section {sec} of the main section of the sub-chapter on {subtopic} in the chapter of {subfield} for the book of {subject}. This is the last section of the the sub-chapter. End the sub-chapter with a proper concluding paragraph. Make sure the output is in pure markdown."}
                    ]
                    )
                    md_file.write(res.choices[0].message.content + "\n\n")  # Write the content to the markdown file
                    md_file.close()
                    subficol.update_one(
                        {"subfield": subfield},
                        {"$push": {"subtopics": {"title": subtopic, "link": converter.convplease(f"/Users/ciscorrr/Documents/CisStuff/curr/CacheNova/Backend/mddatacluster/{filename}.md", navbarcontent)}}},
                        upsert=True
                        )
                    listoflinks_tosubtopicpages.append({subtopic: f"/Users/ciscorrr/Documents/CisStuff/curr/CacheNova/Backend/mddatacluster/{filename}.md"})

    #listoflinks_tosubtopicpages = [{'title': subtopic, 'link': converter.convplease(f"/Users/ciscorrr/Documents/CisStuff/curr/CacheNova/Backend/mddatacluster/{filename}.md", navbarcontent)} for subtopic in subtopics]
    return listoflinks_tosubtopicpages'''



import threading

def generate_subtopic_page(subject, subfield, subtopic, filename, navbarcontent):
    subsections = get_subsections(subject, subfield, subtopic)
    with open(f"/Users/ciscorrr/Documents/CisStuff/curr/CacheNova/Backend/mddatacluster/{filename}.md", "w") as md_file:
        for i in range(len(subsections)):
            if i != len(subsections) - 1:
                sec = subsections[i]
                next_sec = subsections[i + 1]
            else:
                sec = subsections[i]
                next_sec = None

            prompt = f"You are a co-writer on a university book. When asked to write a section, you will write a lengthy, detailed, and well-researched section on the topic. You are supposed to write the section {sec} of the main section of the sub-chapter {subtopic} in the chapter of {subfield} for the book of {subject}."
            if next_sec:
                prompt += f" End the section by setting up a smooth transition into the next topic: {next_sec}."
            else:
                prompt += " This is the last section of the sub-chapter. End the sub-chapter with a proper concluding paragraph."
            prompt += " Make sure the output is in pure markdown."

            res = openai_client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[
                    {"role": "system", "content": "You are a co-writer on a university book. When asked to write a section, you will write an extremely lengthy, detailed, and well-researched section on the topic, properly formatted with markdown format"},
                    {"role": "user", "content": prompt}
                ]
            )
            md_file.write(res.choices[0].message.content + "\n\n")

    subficol = db[subfield]
    subficol.update_one(
        {"subfield": subfield},
        {"$push": {"subtopics": {"title": subtopic, "link": converter.convplease(f"/Users/ciscorrr/Documents/CisStuff/curr/CacheNova/Backend/mddatacluster/{filename}.md", navbarcontent)}}},
        upsert=True
    )
    return {subtopic: f"/Users/ciscorrr/Documents/CisStuff/curr/CacheNova/Backend/mddatacluster/{filename}.md"}

def generatepages(subject: str, subfield: str, subtopics: list, subtopiclinks: list, navbarcontent: list):
    listoflinks_tosubtopicpages = []
    threads = []

    for subtopic in subtopics:
        filename = subtopiclinks[subtopic]
        thread = threading.Thread(target=generate_subtopic_page, args=(subject, subfield, subtopic, filename, navbarcontent))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # After all threads have completed, gather the links
    # This part needs to be adjusted based on how you collect the results from threads
    # For simplicity, assuming each thread updates a shared or global structure (be cautious with thread safety)
    # Alternatively, you could use a thread-safe structure like queue.Queue to collect results from threads

    return listoflinks_tosubtopicpages