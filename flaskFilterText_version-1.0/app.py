from flask import Flask, render_template, request
import os
import nltk
from nltk.corpus import stopwords
import openai
from openai import OpenAI
import json

app = Flask(__name__)

def dummy_results():
    dummy_response="""
1. Full Stack Development - Score 10/10
   Reason: The resume shows significant experience in designing and developing applications with C++, Java, and JavaScript, matching job requirements.
   Sample text from resume: "Design and Development of micro services using Java, ReactJS"
   Sample text from job description: "Senior Software Engineer that has a passion for full stack development."

2. Microservices Architecture - Score 9/10
   Reason: The resume shows the candidate has experience with microservice architectures, which are mentioned in the job description.
   Sample text from resume: "Design and Development of micro services using Java, ReactJS."
   Sample text from job description: "Experience working with Microservice architectures."

3. Experience with C++ and JavaScript - Score 10/10
   Reason: The resume clearly indicates that the candidate has extensive experience with both C++ and JavaScript, which are required skills for the job.
   Sample text from resume: "Solid C++/Java /Python expertise"
   Sample text from job description: "4+ years experience working with C++ [...] 4+ years experience building comprehensive, scalable, and extensible client-side apps with JavaScript."

4. Scalable Systems - Score 8/10
   Reason: The resume shows an understanding of the scalability of systems, which is something mentioned in the job description.
   Sample text from resume: "Responsible for Requirements to Deliver for VARS systems."
   Sample text from job description: "Participate in the full SDLC of various components and systems that are required to be robust and scalable."

5. Cloud Technologies and Big Data - Score 8/10
   Reason: The resume mentions experience with RedHat OpenShift, AWS and Big Data System which aligns with job requirements.
   Sample Text from resume: "Cloud Technologies RedHat OpenShift and Docker" , "Business Intelligent System Hadoop, Hive and QlikSense"
   Sample Text from job description: "Knowledge of Big Data, SQL and NoSQL Databases, and Cloud-Based Object Stores"
    """
    return (dummy_response)

def compare_files(file1_path, file2_path):
    with open(file1_path, 'r', encoding='utf-8') as f1, open(file2_path, 'r', encoding='utf-8') as f2:
        content1 = set(f1.read().split())
        content2 = set(f2.read().split())
        matching_keywords = content1.intersection(content2)
        return matching_keywords

nltk.download('stopwords')
  
def remove_articles(words):
    articles = set(stopwords.words('english'))
    return [word for word in words if word.lower() not in articles]

def using_openai(resume, jobs):
    with open(resume, 'r', encoding='utf-8') as f1, open(jobs, 'r', encoding='utf-8') as f2:
        #content1_resume = set(f1.read().split())
        #cntent2_jobs = set(f2.read().split()) 
        content1_resume = (f1.read())
        content2_jobs =  (f2.read()) 
        #print("\n========(resume)============\n")
        ##print(content1_resume)
        #print("\n=========(jobs)===========\n")
        #print(content2_jobs)
        mykeys = json.load(open('c:\workarea\mykey.json'))
        client = OpenAI(api_key=mykeys["api_key"],organization=mykeys["organization"])
        print(client)
        openai.verify_ssl_certs = False
        msg1=f"here is resume  {content1_resume}"
        msg2=f"here is job description to compare {content2_jobs}"
        messages=[
                    {'role':"user","content":"reset context"},
                    {'role':"user","content":msg1},
                    {'role':"user","content":msg2},

                    {'role':"user","content":" give in summary top 5  skills matching "
                        "resume and jobs description in the scale of 10" 
                        "give me one line reason for each matching" 
                        "also give sample text from resume and jobs description"
                        " do the verbatim  match "
                        }
        ]
        #print(messages)
        try:
            print("\n Doing the AI analysis")
            completion = client.chat.completions.create(
                #model="gpt-3.5-turbo",
                model="gpt-4",
                #model="gpt-4o",
                #model="gpt-3.5-turbo-0125",
                #model="text-embedding-3-small",
                messages=messages
                )
            print("\n Done the AI analysis")
            return (completion)
        except openai.APIConnectionError as e:
            print("The server could not be reached")
            print(e.__cause__)  # an underlying Exception, likely raised within httpx.
            print(dir(e))
            print(e.code)
            print(e.body)
            print(e.request) 
            print(e.args)
        except openai.RateLimitError as e:
            print("A 429 status code was received; we should back off a bit.")
        except openai.APIStatusError as e:
            print("Another non-200-range status code was received")
            print(e.__cause__)  # an underlying Exception, likely raised within httpx.
            print(dir(e))
            print(e.code)
            print(e.body)
            print(e.request)
            print(e.args)
        except Exception as e:
            print(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare_dummy', methods=['POST'])
def compare_dummy():
        file_to_compare = request.files['file_to_compare']
        files = request.files.getlist('files[]')

        # Save uploaded files to server
        file_to_compare_path = os.path.join('uploads', file_to_compare.filename)
        file_to_compare.save(file_to_compare_path)

        result = {}
        airesult = {}
        
        for file in files:
            print("\n===============================================================\n")
            print(f"=================== {file_to_compare} {file.filename}")
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)
            matching_keywords = compare_files(file_to_compare_path, file_path)

            matching_keywords  = remove_articles(   matching_keywords )
            ai_response_sumary = None 
            ai_response_sumary  = dummy_results()

            result[file.filename] = matching_keywords 
            if (matching_keywords is not None and  ai_response_sumary is not None ):
                result[file.filename] = matching_keywords 
                airesult[file.filename] = ai_response_sumary
            #result[file.filename] = ai_matched_resuls.choices[0].message
            #print(file.filename)
            #print(matching_keywords)
            print(ai_response_sumary)
            #print(result)

        return render_template('result-v2.html', result=result,airesult=airesult)
            #sreturn render_template('result.html', result=ai_response)
       
  

@app.route('/compare', methods=['POST'])
def compare():
        file_to_compare = request.files['file_to_compare']
        files = request.files.getlist('files[]')

        # Save uploaded files to server
        file_to_compare_path = os.path.join('uploads', file_to_compare.filename)
        file_to_compare.save(file_to_compare_path)

        result = {}
        airesult = {}
        
        for file in files:
            print("\n===============================================================\n")
            print(f"=================== {file_to_compare} {file.filename}")
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)
            matching_keywords = compare_files(file_to_compare_path, file_path)
            ai_matched_resuls = using_openai(file_to_compare_path, file_path)
            matching_keywords  = remove_articles(   matching_keywords )
            ai_response_sumary = None 
            ai_response_sumary  = ai_matched_resuls.choices[0].message.content.strip()

            result[file.filename] = matching_keywords 
            if (matching_keywords is not None and  ai_response_sumary is not None ):
                result[file.filename] = matching_keywords 
                airesult[file.filename] = ai_response_sumary
            #result[file.filename] = ai_matched_resuls.choices[0].message
            #print(file.filename)
            #print(matching_keywords)
            print(ai_response_sumary)
            #print(result)

        return render_template('result-v2.html', result=result,airesult=airesult)
            #sreturn render_template('result.html', result=ai_response)
       
  


if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
