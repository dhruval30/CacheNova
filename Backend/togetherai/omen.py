from pymongo import MongoClient
from . import zed
import threading
import string
import markdown2
import time
import random
#connect to the db
client = MongoClient('localhost', 27017)
db = client['Nova']

def generate_random_string(length=10):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for i in range(length))



def generatemarkdown_for_subject(subject, subfields):
    #generates markdown for the subject page
    #subfields is a list of strings
    #subject is a string
    #return a string
    markdown = f"# {subject}\n\n"
    for subfield in subfields:
        markdown += f"## {subfield}\n\n"
    return markdown

def convert_subject_markdown_to_html(markdown_content, subject):
    # Convert Markdown to HTML
    html_content = markdown2.markdown(markdown_content, extras=["mathjax"])

    # Fetch subfields and their corresponding links from the database
    subcol = db[subject]
    subject_data = subcol.find_one({"type": "subject", "subject": subject})
    subfields = subject_data["subfields"]

    subfield_links = {}
    for subfield in subfields:
        subficol = db[subfield]
        subfield_data = subficol.find_one({"type": "subfield", "subfield": subfield})
        subfield_links[subfield] = subfield_data["subfieldpage"]

    # Replace subfield names in HTML content with links
    for subfield, link in subfield_links.items():
        html_content = html_content.replace(f"## {subfield}", f"<a href='{link}.html'>## {subfield}</a>")

    # HTML template without navbar and with glossary styling
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link href='https://fonts.googleapis.com/css?family=Aldrich' rel='stylesheet'>
        <link href='https://fonts.googleapis.com/css?family=Asap' rel='stylesheet'>
        <link rel="stylesheet" href="glossary.css">
        <meta content="width=device-width, initial-scale=1, shrink-to-fit=no" name="viewport">
        <title>{subject} Glossary</title>
    </head>
    <body>
        
        <main id="main-doc">
            {html_content}
        </main>
        
    </body>
    </html>
    """

    # Determine the new HTML file path and write the final HTML content
    html_file_path = f"/Users/ciscorrr/Documents/CisStuff/curr/CacheNova/Backend/subjecthtmldatacluster/{subject}.html"

    # Write the final HTML content to the new file
    with open(html_file_path, "w", encoding='utf-8') as file:
        file.write(html_template)
    return html_file_path
'''
def threadchaos(prompt, subject):
    #ignore prompt for now, just use subjects
    #subjects is a list of strings
    #prompt is to build dynamic pages in the future

    #get the subfields for each subject
    
    subfields = zed.getsubfields(subject, prompt) #returns a list of strings
    subcol = db[subject]
    subjectfile = f"/Users/ciscorrr/Documents/CisStuff/curr/CacheNova/Backend/subjecthtmldatacluster/{subject}.html"
    #subfieldfiles = [{'title': subfield, 'link': generate_random_string()} for subfield in subfields]
    subcol.insert_one({"type": "subject", "subject":subject, "subjectpage": subjectfile, "subfields": subfields})
    for subfield in subfields:
        #implement the following
        #if subfield in db:
        #   listoflinks_tosubfieldpages.append({subfield: db[subfield]})
        #else:
        
        subficol = db[subfield]
        subtopics = zed.getsubtopics(subfield, subject, prompt)
        subtopiclinks={subtopic: generate_random_string() for subtopic in subtopics}
        subfieldpage = subtopiclinks[subtopics[0]]  #this is the link to the subfield page

        #lets gen navbar content

        navbarcontent = [{'title': subtopicname, 'link': subtopiclinks[subtopicname]} for subtopicname in subtopics]
        
        #for each subtopic, call omen.createpage(subtopic)
        #return the link to the page
        #add the following to the subfield collection
        #subfield:[{subtopic1, link1}, {subtopic2, link2}, {subtopic3, link3}]
        subficol.insert_one({"type": "subfield", "subfield":subfield, "subfieldpage": subfieldpage, "subtopics":[]})
        linkstosubtopic=zed.generatepages(subject, subfield, subtopics, subtopiclinks, navbarcontent) #should return a list of dicts of name of subtopic as key and link as value
        #holds the form [{subtopic1: link1}, {subtopic2: link2}, {subtopic3: link3}]

    
        #subficol.insert_one({"subfield":subfield, "subfieldpage": subfieldpage, "subtopics":linkstosubtopic})
        #add the following to the subject collection
        #linkstosubtopic holds list of dicts of title key holding subtopic, link key holding entire path to subtopic
    with open(f'/Users/ciscorrr/Documents/CisStuff/curr/CacheNova/Backend/subjectmddatacluster/{subject}.md', "w", encoding='utf-8') as file:
        file.write(generatemarkdown_for_subject(subject, subfields))
    convert_subject_markdown_to_html(f'/Users/ciscorrr/Documents/CisStuff/curr/CacheNova/Backend/subjectmddatacluster/{subject}.md', subject)
        
    
    return None


    
'''


    
'''

def threadchaos(prompt, subject):
    subfields = zed.getsubfields(subject, prompt)  # returns a list of strings
    subcol = db[subject]
    subjectfile = f"/Users/ciscorrr/Documents/CisStuff/curr/CacheNova/Backend/subjecthtmldatacluster/{subject}.html"
    subcol.insert_one({"type": "subject", "subject": subject, "subjectpage": subjectfile, "subfields": subfields})

    for subfield in subfields:
        subficol = db[subfield]
        subtopics = zed.getsubtopics(subfield, subject, prompt)
        subtopiclinks = {subtopic: generate_random_string() for subtopic in subtopics}
        subfieldpage = subtopiclinks[subtopics[0]]  # this is the link to the subfield page

        navbarcontent = [{'title': subtopicname, 'link': subtopiclinks[subtopicname]} for subtopicname in subtopics]
        
        subficol.insert_one({"type": "subfield", "subfield": subfield, "subfieldpage": subfieldpage, "subtopics": []})
        linkstosubtopic = zed.generatepages(subject, subfield, subtopics, subtopiclinks, navbarcontent)

        # After processing each subfield, regenerate and update the subject HTML file
        # This ensures the HTML file is updated with the latest subfield information
        markdown_content = generatemarkdown_for_subject(subject, subfields)
        with open(f'/Users/ciscorrr/Documents/CisStuff/curr/CacheNova/Backend/subjectmddatacluster/{subject}.md', "w", encoding='utf-8') as file:
            file.write(markdown_content)
        convert_subject_markdown_to_html(markdown_content, subject)'''


def process_subfield(subject, subfield, prompt):
    subficol = db[subfield]
    subtopics = zed.getsubtopics(subfield, subject, prompt)
    subtopiclinks = {subtopic: generate_random_string() for subtopic in subtopics}
    subfieldpage = subtopiclinks[subtopics[0]]  # this is the link to the subfield page

    navbarcontent = [{'title': subtopicname, 'link': subtopiclinks[subtopicname]} for subtopicname in subtopics]
    
    subficol.insert_one({"type": "subfield", "subfield": subfield, "subfieldpage": subfieldpage, "subtopics": []})
    linkstosubtopic = zed.generatepages(subject, subfield, subtopics, subtopiclinks, navbarcontent)

    # After processing each subfield, regenerate and update the subject HTML file
    # This ensures the HTML file is updated with the latest subfield information
    markdown_content = generatemarkdown_for_subject(subject, [subfield])
    with open(f'/Users/ciscorrr/Documents/CisStuff/curr/CacheNova/Backend/subjectmddatacluster/{subject}.md', "a", encoding='utf-8') as file:
        file.write(markdown_content)
    convert_subject_markdown_to_html(markdown_content, subject)

def threadchaos(prompt, subject):
    subfields = zed.getsubfields(subject, prompt)  # returns a list of strings
    subcol = db[subject]
    subjectfile = f"/Users/ciscorrr/Documents/CisStuff/curr/CacheNova/Backend/subjecthtmldatacluster/{subject}.html"
    subcol.insert_one({"type": "subject", "subject": subject, "subjectpage": subjectfile, "subfields": subfields})

    threads = []
    for subfield in subfields:
        thread = threading.Thread(target=process_subfield, args=(subject, subfield, prompt))
        threads.append(thread)
        thread.start()
        time.sleep(60)
        thread.join()
    

    # After all threads have completed, update the subject HTML file one final time to ensure it contains all updates
    markdown_content = generatemarkdown_for_subject(subject, subfields)
    with open(f'/Users/ciscorrr/Documents/CisStuff/curr/CacheNova/Backend/subjectmddatacluster/{subject}.md', "w", encoding='utf-8') as file:
        file.write(markdown_content)
    convert_subject_markdown_to_html(markdown_content, subject)