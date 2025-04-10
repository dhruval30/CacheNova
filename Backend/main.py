import threading
from togetherai import omen, zed
from pymongo import MongoClient
import random
import string
#import axios
from flask import Flask, request, jsonify
import json
import asyncio
from threading import Thread
import time
#from gottadealwithfrontend import subjectlink
client = MongoClient('localhost', 27017)
db = client['Nova']
userdb = db['users']

def generate_random_string(length=10):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for i in range(length))

#app = Flask(__name__)


def chaos(prompt, session_id):
    if prompt =="" or prompt == None:
        return "Please provide a prompt"
    cleanprompt = zed.cleanprompt(prompt) 
    subjects = zed.getsubjects(cleanprompt) #will return a list of all subjects related to prompt, might need to be semantic searched       
    print(cleanprompt)
    print(subjects)
    
    subjectlink =  [generate_random_string() for subject in subjects]#returns a link to html file that contains only the relevant subjects
    userdb.update_one({"userid": session_id}, {"$set": {"status": "Processed", "link": subjectlink}})
    
    def run_threadchaos(cleanprompt, subject):   #sends only one of the subjects to the threadchaos function
        omen.threadchaos(cleanprompt, subject)

    for subject in subjects:
        print(subject)
        thread = threading.Thread(target=run_threadchaos, args=(cleanprompt, subject))
        thread.start()
        thread.join()
        
        
    return "Processing complete"

'''
@app.route('/process_prompt', methods=['GET'])
def process_prompt():
    prompt = request.args.get('prompt')
    session_id = request.args.get('session_id')  # Not used currently, but captured
    userdb.update_one({"userid": session_id}, {"$set": {"status": "Processing"}}) #set this user's status to processing, change back as soon as 
    #subject page is made
    
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    thread = threading.Thread(target=chaos, args=(prompt,session_id))
    thread.start()
    
    return jsonify({"message": "Processing your request. Please wait..."}), 202
'''
            
   

if __name__ == '__main__':
    chaos("Transformer Models and LLMs", "123")