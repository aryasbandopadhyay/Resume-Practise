import os
from flask import Flask, render_template, request, session, redirect,flash,url_for
from werkzeug.utils import secure_filename
# from flask_mail import Mail
import json
import os
import math
from datetime import datetime
from flask_caching import Cache
from flask import jsonify
from flask import json
import requests
from flask import send_from_directory
import docx
import docx2txt
# import PyPDF2 
import math 
import pdfplumber # pip install tika
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PyPDF2 import PdfFileReader
from flask import Flask
import re
import json
#import jinja2app
#from spellchecker import SpellChecker
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from pickle import dump, load
from nltk.corpus import brown
from itertools import dropwhile
from nltk import word_tokenize, pos_tag
# =============================================================================
# from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
# from pdfminer.converter import TextConverter
# from pdfminer.layout import LAParams
# from pdfminer.pdfpage import PDFPage
from io import StringIO
# =============================================================================
#import codecs

from pdfminer.high_level import extract_text
import spacy
nlp = spacy.load('en_core_web_sm')
from spacy.matcher import Matcher
import datetime
import numpy as np
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt

import base64
from io import BytesIO
import plotly.io as pio

#spell = SpellChecker()
#nltk.download('stopwords')
#nltk.download('averaged_perceptron_tagger')

#nltk.download('all')

UPLOAD_FOLDER='./uploads/'
ALLOWED_EXTENSIONS ={'pdf','docx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.secret_key = 'development key'

# app.config['MYSQL_HOST'] = 'dataly.database.windows.net'
# app.config['MYSQL_USER'] = 'dataly'
# app.config['MYSQL_PASSWORD'] = 'uG5qMZxv'
# app.config['MYSQL_DB'] = 'dataly'
#mysql = MySQL(app)





def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower()in ALLOWED_EXTENSIONS



keyword = "N"
text_main=""
length = 0
match=0
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    try:
        f_name = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        # return f_name
        global text_main,length,match,keyword
        file_name = f_name
        print(f_name)
        impact = 0
        pres =0
        text_main = ""
        edu_msg =0 
        vol_msg=0
        pro_msg=0
        jd_msg=""
        if(file_name[-3:]=="pdf"):
            print("File is in pdf")
            pdf(file_name)
            #print(text_main)
            #text_main=re.sub(r'[^\\x00-\x7f]',r'', text_main)
            #text_main=re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', text_main)
            # if (float(match) == 0):
            #     jd_msg = "If it shows zero, probably you have not specified the JD in it field. Try adding a JD to check how accurately your resume matches with the Job."
            # elif (float(match) < 50):
            #     jd_msg = "With " +str(match) + "% score you might need to add more skills related to the Job you have been looking for. Try aiming for a score above 80%"
            # else:
            #     jd_msg ="With " +str(match) + "% score you seem to be an apt fit for the Job you have been looking for. "
        elif(file_name[-4:] == "docx" or file_name[-3:] == "doc" ):
            print("File is in docx")
            docx1(file_name)
            #text_main=re.sub(r'[^\x00-\x7f]',r'', text_main)
            # if (float(match) == 0.0):
            #     jd_msg = "If it shows zero, probably you have not specified the JD in it field. Try adding a JD to check how accurately your resume matches with the Job."
            # elif (float(match) < 50):
            #     jd_msg = "With " +str(match) + " % score you might need to add more skills related to the Job you have been looking for. Try aiming for a score above 80%"
            # else:
            #     jd_msg ="With " +str(match) + " % score you seem to be an apt fit for the Job you have been looking for. "
        else:
            print("Invalid Fileformat - Supported docx or pdf")
        #print (text_main)
        
        text_count=text_main.split(" ")
        word_count=len(text_count)
        liness=[]
        line=""
        line1=[]
    # =============================================================================
    #     for i in text_main:
    #             
    #         if(i!='\n'):
    #             line+=i
    #         else:
    #             liness.append(line)
    #             line=""
    #         
    #     for line in liness:
    #         if len(line)!=0:
    #             line1.append(line)
    # =============================================================================
    # =============================================================================
        if(file_name[-4:] == "docx" or file_name[-3:] == "doc" ):
            for i in text_main:
                
                if(i!='\n'):
                    line+=i
                else:
                    liness.append(line)
                    line=""
            
            for line in liness:
                if len(line)!=0:
                    line1.append(line)
        elif(file_name[-3:]=="pdf"):
            liness=text_main.split("\\n")
    # =============================================================================
    #         for i in range(len(text_main)-1):
    #             if(text_main[i]=="\\" ):
    #                if(text_main[i+1]=='n'):
    #                    liness.append(line)
    #                    line=""
    #                else:
    #                    line+=text_main[i]
    # =============================================================================
                    
            
            for line in liness:
                if len(line)!=0:
                    line1.append(line)

        
        
        phone=re.findall(r"(?<!\d)\d{10}(?!\d)", text_main)
        email=re.findall(r"([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)",text_main)
        #print(email)
        links= re.findall(r"(^(http\:\/\/|https\:\/\/)?([a-z0-9][a-z0-9\-]*\.)+[a-z0-9][a-z0-9\-]*)",text_main)
        mlink=[]
        for link in links:
            if 'facebook' in link:
                mlink.append(link)
            elif 'github' in link:
                mlink.append(link)
            elif 'linkedin' in link:
                mlink.append(link)
            else:
                links.remove(link)
        links=list(set(mlink))
        section=[]
        sections={}
        line2=[]
        titles=['education','Licensures', 'Professional Qualification', 'academic qualification', 'Educational Qualification', 'academia', 'education and professional development', 'academic credentials', 'educational summary', 'academic profile', 'Experience', 'work experience', 'Job Titles held', 'Position Description and purpose', 'Professional Experience', 'Professional Summary', 'Profile', 'Qualifications', 'Employment History', 'history', 'previous employment', 'organisational experience', 'employers', 'positions of responsibility','Position of Responsibilities', 'employment scan', 'past experience', 'organizational experience', 'career', 'experience and qualification summary', 'relevant experience', 'experience summary', 'career synopsis', 'career timeline', 'banking IT experience', 'AML & FCM Suite Experience', 'employment details', 'Skill','skills', 'Technical Skills', 'Soft Skills', 'Key Skills', 'Design Skills', 'Expertise', 'Abilities', 'Area of Expertise', 'Key attributes', 'Computer Skills', 'IT Skills', 'Technical Expertise', 'Technical Skills Set', 'Functional Skill Set', 'functional skills', 'strengths', 'areas of expertise', 'banking knowledge', 'Award', 'Honours and awards', 'Key achievements', 'Accomplishments', 'Highlights', 'Affiliations', 'Achievements', 'Extra Curricular activities and achievements', 'awards and recognition','awards/achievements', 'Certificate', 'Most proud of', 'Specialization', 'Certifications', 'Certification/training','Coursework','other credentials', 'professional accomplishments', 'certification & trainings', 'scholastics', 'professional credentials and certifications','Project','projects', 'Additional Activities', 'Activities', 'Major Tasks', 'Responsibilities', 'key accountabilities', 'Contributions', 'Personal Projects', 'Key Contributions', 'Strategic Planning and execution', 'Academic projects', 'Key projects', 'projects/trainings', 'key implementations','Volunteer', 'Volunteer Experience', 'Affiliations', 'Misc','Extra Curricular Activities', 'Community Service','EDUCATIONAL BACKGROUND','INTERNSHIPS EXPERIENCE','WINNING PORTFOLIO','AWARDS & RECOGNITIONS','CORE COMPETENCIES','PROJECTS ADMINISTERED','TECHNICAL SKILLS','CERTIFICATIONS','VOLUNTEERING','PERSONAL DOSSIER','Licensure', 'Professional Qualifications', 'academic qualifications', 'academics qualification', 'academics qualifications',  'Educational Qualifications', 'education and professional developments', 'academic credential', 'academics credential', 'academics credentials', 'educational summaries', 'academic profiles', 'academics profile','Experiences', 'work experiences', 'Position Descriptions and purpose', 'Positions Description and purpose', 'Positions Descriptions and purpose', 'Professional Experiences', 'Profiles', 'Qualification', 'Employment Histories', 'previous employments', 'organisational experiences', 'organizational experiences', 'organizational experience', 'employer', 'positions of responsibilities', 'position of responsibility', 'position of responsibilities', 'employment scans', 'past experiences', 'organizational experiences', 'organisational experience', 'organisational experiences', 'careers', 'experiences and qualifications summary', 'experience and qualifications summary', 'experiences and qualification summary', 'relevant experiences', 'career timelines', 'banking IT experiences', 'AML & FCM Suite Experiences', 'employment details', 'employment detail','Skills', 'Technical Skill', 'Soft Skill', 'Key Skill', 'Design Skill', 'Expertises', 'Ability', 'Areas of Expertises', 'Areas of Expertise', 'Area of Expertises', 'Key attribute', 'Computer Skill', 'IT Skill', 'Technical Expertises', 'Technical Skill Set', 'Technical Skill Sets', 'Functional Skills Set', 'Functional Skill Sets', 'Functional Skills Sets', 'functional skill', 'strength', 'area of expertise', 'area of expertises','Awards', 'Key achievement', 'Accomplishment', 'Highlight', 'Affiliation', 'Achievement', 'Extra Curricular activities and achievements',  'Extra Curricular activity and achievements',  'Extra Curricular activities and achievement',  'Extra Curricular activity and achievement', 'awards and recognitions',  'award and recognition',  'award and recognitions', 'Certificates', 'Specializations', 'Certification', 'Certifications/trainings', 'Certifications/training', 'Certification/trainings', 'other credential', 'professional accomplishment', 'certifications & trainings', 'certifications & training', 'certification & training', 'scholastic', 'professional credential and certification', 'professional credential and certifications', 'professional credentials and certification','Project', 'Additional Activity', 'Activity', 'Major Task', 'Responsibily', 'key accountability', 'Contribution', 'Personal Project', 'Key Contribution', 'Strategic Plannings and executions', 'Strategic Plannings and execution', 'Strategic Planning and executions', 'Academic project', 'Key project', 'project/training', 'projects/training', 'project/trainings', 'key implementation','Volunteer', 'Volunteer Experiences', 'Affiliation', 'Community Services' ]
        titles1=[x.lower() for x in titles]
        for i in line1:
            if i[-1]==" ":
                line2.append(i[:-1])
            else:
                line2.append(i)
        #print(titles1)
        line1=line2
        temp = '\t'.join(titles1)
        for x in line1:
            #print(x.lower() in titles1, x.lower())
            global keyword
            if(x==line1[-1]):
            
                section.append(x)
                sections[keyword] = section
                keyword = x
                    #print(sections)
                section =[]
                break
            elif x.lower() not in temp:
                section.append(x)
                #print(x)
                #print(section)
            elif (len(x.split(" "))>=4):
                section.append(x)
                #print(section)  
            
                
            else :
                if(len(section)!=0):
                    sections[keyword] = section
                    keyword = x
                    #print(sections)
                    section =[]
                else:
                    sections[keyword]=[]
                    keyword=x
                    section =[]
                    #print(sections)
        #print(sections.keys())
        sections['phone']=list(set(phone))
        sections['links']=mlink
        if (len(mlink) != 0):
            impact+=5
        #imp_sec=["education","experience","expertise","role","career","skill","award","certificat","projects",'volunteer']
        ed_list=['Education', 'Licensures', 'Professional Qualification', 'academic qualification', 'Educational Qualification', 'academia', 'education and professional development', 'academic credentials', 'educational summary', 'academic profile','EDUCATIONAL BACKGROUND','Licensure', 'Professional Qualifications', 'academic qualifications', 'academics qualification', 'academics qualifications',  'Educational Qualifications', 'education and professional developments', 'academic credential', 'academics credential', 'academics credentials', 'educational summaries', 'academic profiles', 'academics profile']
        ex_list=['Experience', 'work experience', 'Job Titles held', 'Position Description and purpose', 'Professional Experience', 'Professional Summary', 'Profile', 'Qualifications', 'Employment History', 'history', 'previous employment', 'organisational experience', 'employers', 'positions of responsibility', 'employment scan','past experience', 'organizational experience', 'career', 'experience and qualification summary', 'relevant experience', 'experience summary', 'career synopsis', 'career timeline', 'banking IT experience', 'AML & FCM Suite Experience', 'employment details','INTERNSHIPS EXPERIENCE','Experiences', 'work experiences', 'Position Descriptions and purpose', 'Positions Description and purpose', 'Positions Descriptions and purpose', 'Professional Experiences', 'Profiles', 'Qualification', 'Employment Histories', 'previous employments', 'organisational experiences', 'organizational experiences', 'organizational experience', 'employer', 'positions of responsibilities', 'position of responsibility', 'position of responsibilities', 'employment scans', 'past experiences', 'organizational experiences', 'organisational experience', 'organisational experiences', 'careers', 'experiences and qualifications summary', 'experience and qualifications summary', 'experiences and qualification summary', 'relevant experiences', 'career timelines', 'banking IT experiences', 'AML & FCM Suite Experiences', 'employment details', 'employment detail', 'career progression']
        sk_list=['Skill', 'Technical Skills', 'Soft Skills', 'Key Skills', 'Design Skills', 'Expertise', 'Abilities', 'Area of Expertise', 'Key attributes', 'Computer Skills', 'IT Skills', 'Technical Expertise', 'Technical Skills Set', 'Functional Skill Set', 'functional skills', 'strengths', 'areas of expertise', 'banking knowledge','WINNING PORTFOLIO','CORE COMPETENCIES','TECHNICAL SKILLS','skills','Skills', 'Technical Skill', 'Soft Skill', 'Key Skill', 'Design Skill', 'Expertises', 'Ability', 'Areas of Expertises', 'Areas of Expertise', 'Area of Expertises', 'Key attribute', 'Computer Skill', 'IT Skill', 'Technical Expertises', 'Technical Skill Set', 'Technical Skill Sets', 'Functional Skills Set', 'Functional Skill Sets', 'Functional Skills Sets', 'functional skill', 'strength', 'area of expertise', 'area of expertises']
        aw_list=['Award' ,'Honours and awards', 'Key achievements', 'Accomplishments', 'Highlights', 'Affiliations', 'Achievements', 'Extra Curricular activities and achievements', 'awards and recognition','AWARDS & RECOGNITIONS','awards','achievements','Awards', 'Key achievement', 'Accomplishment', 'Highlight', 'Affiliation', 'Achievement', 'Extra Curricular activities and achievements',  'Extra Curricular activity and achievements',  'Extra Curricular activities and achievement',  'Extra Curricular activity and achievement', 'awards and recognitions',  'award and recognition',  'award and recognitions']
        ce_list=['Certificate', 'Most proud of', 'Specialization', 'Certifications', 'Certification/training', 'other credentials', 'professional accomplishments', 'certification & trainings', 'scholastics', 'professional credentials and certifications','CERTIFICATION','coursework', 'competencies', 'Certificates', 'Specializations', 'Certification', 'Certifications/trainings', 'Certifications/training', 'Certification/trainings', 'other credential', 'professional accomplishment', 'certifications & trainings', 'certifications & training', 'certification & training', 'scholastic', 'professional credential and certification', 'professional credential and certifications', 'professional credentials and certification',  'key accountability', 'Contribution', 'Personal Project', 'Key Contribution', 'Strategic Plannings and executions', 'Strategic Plannings and execution', 'Strategic Planning and executions',]
        pe_list=['Project', 'Additional Activities', 'Activities', 'Major Tasks', 'Responsibilities', 'key accountabilities', 'Contributions', 'Personal Projects', 'Key Contributions', 'Strategic Planning and execution', 'Academic projects', 'Key projects', 'projects/trainings', 'key implementations','PROJECTS ADMINISTERED','projects','Project', 'Additional Activity', 'Activity', 'Major Task', 'Responsibily', 'key accountability', 'Contribution', 'Personal Project', 'Key Contribution', 'Strategic Plannings and executions', 'Strategic Plannings and execution', 'Strategic Planning and executions', 'Academic project', 'Key project', 'project/training', 'projects/training', 'project/trainings', 'key implementation','Additional Activity', 'Activity', 'Major Task', 'Responsibily', 'Academic project', 'Key project', 'project/training', 'projects/training', 'project/trainings', 'key implementation']
        vo_list=['Volunteer', 'Volunteer Experience', 'Affiliations', 'Misc', 'Community Service','VOLUNTEERING','extra curricular activities','EXTRA-CURRICULAR INVOLVEMENT','Volunteer', 'Volunteer Experiences', 'Affiliation', 'Community Services']
        ed1_list=[x.lower() for x in ed_list]
        temp_ed= '\t'.join(ed1_list)
        ex1_list=[x.lower() for x in ex_list]
        temp_ex='\t'.join(ex1_list)
        sk1_list=[x.lower() for x in sk_list]
        temp_sk='\t'.join(sk1_list)
        aw1_list=[x.lower() for x in aw_list]
        temp_aw='\t'.join(aw1_list)
        ce1_list=[x.lower() for x in ce_list]
        temp_ce='\t'.join(ce1_list)
        pe1_list=[x.lower() for x in pe_list]
        temp_pe='\t'.join(pe1_list)
        vo1_list=[x.lower() for x in vo_list]
        temp_vol='\t'.join(vo1_list)
        #print(vo1_list)
        score = 0
        msg = []
        edu=0
        ed=0
        ex=0
        sk=0
        aw=0
        ce=0
        pe=0
        vo=0
        ed_date_format_list=[0,0]
        ex_date_format_list=[0,0]
        ach_msg = 0 #achievement variable message
        cert_msg = 0 #certification message flag
        sections['edu_year']=""
        sections['exp_year']=""
        sections['paragraph']=0
        #print(sections)
        for key in sections.keys():
            #print(repr(key))
            #for sec in titles1:
                #if sec == key.lower():
                    #print(sec,type(sec),"Hi")
            for i in ed1_list:
                if(i in key.lower() and ed==0 and key.lower()!='n'):
                    score +=10
                    pres+=10
                    edu = 1
                    ed=1
                    edu_msg =1
                    ed_date_format_list=date_format(sections[key])
                    #print(ed_date_format_list)
                    sections['edu_year']=extract(sections[key])
                    sections['paragraph']+=paragraph_check(sections[key])
                    #print(key,temp_ed)
                    msg.append("Education Section is Present")
                    break
                #print(score)
            for i in ex1_list:    
                if(i in key.lower() and ex==0 and key.lower()!='n'):
                    score +=20
                    ex=1
                    sections['exp_year']=extract(sections[key])
                    ex_date_format_list=date_format(sections[key])
                    impact+=20
                    sections['paragraph']+=paragraph_check(sections[key])
                            #print(dummy_exp)
                    msg.append("Experience Section is Present")
                    #print(score)
                    #print(key,temp_ex)
                    break
                
            for i in sk1_list:
                if(i in key.lower() and sk==0 and key.lower()!='n'):
                    score +=20
                    sk=1
                    msg.append("Skills Section is Present")
                    sections['paragraph']+=paragraph_check(sections[key])
                    break
            for i in aw1_list:    
                if(i in key.lower() and aw==0 and key.lower()!='n'):
                    score +=5
                    impact+=5
                    aw=1
                    ach_msg = 1
                    sections['paragraph']+=paragraph_check(sections[key])
                    msg.append("Awards/Achievement Section is Present")
                    #print(score)
                    #print(key)
                    break
            for i in vo1_list:    
                if(i in key.lower() and vo==0 and key.lower()!='n'):
                    pres+=5
                    score +=5
                    vo=1
                    vol_msg =1
                    msg.append("Volunteering Section is Present")
                    #print(score)
                    #print(key)
                    break
            for i in ce1_list:    
                if(i in key.lower() and ce==0 and key.lower()!='n'):
                    impact+=5
                    score +=10
                    cert_msg=1
                    ce=1
                    msg.append("Certificate Section is Present")
                    #print(score)
                    #print(key)
                    break
            for i in pe1_list:    
                if(i in key.lower() and pe==0 and key.lower()!='n'):
                    pres+=10
                    pe=1
                    score +=10
                    pro_msg=1
                    sections['paragraph']+=paragraph_check(sections[key])
                    msg.append("Projects Section is Present")
                    #print(score)
                    #print(key)
                    break
        list_present=[ed,ex,sk,aw,ce,pe,vo]
        fed=0
        fex=0
        fsk=0
        faw=0
        fce=0
        fpe=0
        fvo=0
        sect=[]
        
        #import os
        if os.path.exists("./templates/file.html"):
            os.remove("./templates/file.html")
        else:
            print("The file does not exist") 
        for i in range(len(list_present)):
            if i ==0 and list_present[i]==0:
                #print("education" + "is absent")
                for ik in ed1_list:
                    if ik in text_main.lower():
                        fed=1
            if i ==1 and list_present[i]==0:
                #print("experience" + "is absent")
                for ik in ex1_list:
                    if ik in text_main.lower():
                        fex=1
            if i ==2 and list_present[i]==0:
                print("skill" + "is absent")
                for ik in sk1_list:
                    if ik in text_main.lower():
                        fsk=1
            if i ==3 and list_present[i]==0:
                #print("achievement/award" + "is absent")
                for ik in aw1_list:
                    if ik in text_main.lower():
                        faw=1
            if i ==4 and list_present[i]==0:
                #print("certification" + "is absent")
                for ik in ce1_list:
                    if ik in text_main.lower():
                        fce=1
            if i ==5 and list_present[i]==0:
                #print("project" + "is absent")
                for ik in pe1_list:
                    if ik in text_main.lower():
                        fpe=1
            if i ==6 and list_present[i]==0:
                #print("volunteer" + "is absent")
                for ik in vo1_list:
                    if ik in text_main.lower():
                        fvo=1
        print(fed,fex,fsk,fsk,faw,fce,fpe,fvo)
        improper_format=[]
        if(fed==1 and ed==0):
            improper_format.append('education')
        if(fex==1 and ex==0):
            improper_format.append('experience')
        if(fsk==1 and sk==0):
            improper_format.append('skill')
        if(faw==1 and aw==0):
            improper_format.append('achievement')
        if(fce==1 and ce==0):
            improper_format.append('certification')
        if(fpe==1 and pe==0):
            improper_format.append('project')
        if(fvo==1 and vo==0):
            improper_format.append('volunteer')
        print(improper_format)
            
        #print("EDU MSG",edu_msg)
        sections['Message']=msg
        # sections['Score']=round(((score/98)*100),2)
        rev=""
        '''misspelled = spell.unknown(text_main)
        sections["Errors"]=[]
        for word in misspelled :
            if(len(word))>3:
                sections["Errors"].append(word)'''
                
        stop_words = set(stopwords.words('english')) 
        d=""
        skillsets=0
        filtered_sentence=[]
        
    
        for i in sections.keys():
            if(i.lower()=="work experience"):
                score +=5
            if(i.lower()=="core competencies"):
                score +=5            
            if 'skill' in i.lower():
                skillsets=len(sections[i])
                for j in sections[i]:
                     
                    d=d+" "+j
                d = word_tokenize(d)
                 # print("I am here 2")
                 #print(d)
                for w in d: 
                    if w not in stop_words: 
                        if(len(w)>3):
                            filtered_sentence.append(w)
    
        sections['SkCount']=skillsets
        #sections['original']=filtered_sentence
        sections['linkedin']=Find(text_main)
        ck=sections['linkedin']
        link_msg=1
        if(len(ck) == 0):
            link_msg=0
        #print(type(len(ck)))
        #print('Heyo',sections['linkedin'])
        ac=0
        rd=0
        action_list=[]
        act_msg=0
        if actionwords(text_main)[0] > 5 :
            act_msg =1
            action_list=actionwords(text_main)[1]
            ac=10
            sections['action_word']="Your resume contains Action Verbs! Strong, unique action verbs show hiring managers that you have held different roles and skill sets. They also help your accomplishments stand out and make them more impactful."
        elif actionwords(text_main)[0]<=5:
            act_msg =0
            sections['action_word']="Your resume doesnt contain much Action Verbs! Strong, unique action verbs show hiring managers that you have held different roles and skill sets. They also help your accomplishments stand out and make them more impactful. "
        elif actionwords(text_main)[0]==0:
            
            act_msg =0
            sections['action_word']="Your resume doesnt contain any Action Verbs! Strong, unique action verbs show hiring managers that you have held different roles and skill sets. They also help your accomplishments stand out and make them more impactful. "
        fct_msg=0
        filler_list=[]
        if fillerwords(text_main)[0] > 1 :
            fct_msg =1
            filler_list=fillerwords(text_main)[1]
            
            #sections['action_word']="Your resume contains Action Verbs! Strong, unique action verbs show hiring managers that you have held different roles and skill sets. They also help your accomplishments stand out and make them more impactful."
        # elif fillerwords(text_main)[0]<=5:
        #     fct_msg =0
        #     filler_list=fillerwords(text_main)[1]
        
        elif fillerwords(text_main)[0]==0:
            
            fct_msg =0
            #sections['action_word']="Your resume doesnt contain any Action Verbs! Strong, unique action verbs show hiring managers that you have held different roles and skill sets. They also help your accomplishments stand out and make them more impactful. "
        
        #print(sections['action_word'])
        
        if redundancy(text_main) > 10:
            rd=5
            sections['redundancy']="1"
        elif redundancy(text_main)<=10:
            sections['redundancy']="0"
            
        
        #sections['edu_year']=extract(sections[dummy_edu])
        #print(sections['exp_year'])
        #print(sections['edu_year'])
        #print(sections['redundancy'])
        #print(filtered_sentence)
        sections['match']=match
        # Checking of resume score for message
        if(score == 100):
            rev="the score looks perfect but to get a more accurate comparison with the job you are looking for try analysing by adding Job Description"
        elif(score < 60):
            rev="this score suggests there is a lot of room for improvement. But don't worry! We have highlighted a number of quick fixes you can make to improve your resume's score and your success rate. Try adding more skills or experience into your resume to increase your resume score to 80% or above."
        else:
            rev="your score looks good however we have highlighted a number of quick fixes you can make to improve your resume's score. Try adding more skills or experience into your resume to increase your resume score."
        sections["Review"]=rev
        sections["Length"]=length
        sections["WordCount"]=word_count
        if sections["WordCount"] <= 600 and sections["WordCount"] > 1:
            score += 5
            sections['Message'].append("Word Count of the Resume is Optimal")
        else:
            sections['Message'].append("Word Count should be less than 600")

        if sections["Length"] and sections["WordCount"] > 1:
            score += 5
            sections['Message'].append("Length of Resume is Optimal")
        else:
            sections['Message'].append("Length of Resume should not exceed 2 pages")
        sections['Score']=round(((score/100)*100),2) #calculating score out of overall score.
        if(sections['Score'] >=90 and sections['Score'] <100):
            sections["Review"]="The Resume is correctly Parsed and Optimal. There may be some room for Improvement"
        if(sections['Score'] >=75 and sections['Score']<90):
            sections["Review"]="The Resume may be Correctly Parsed and Optimal. It is advised to pass DOCX Format in ATS Checker. There is certainly Some Room For Improvement"        
        count_passive1=[]
        count_passive=0
        co_pa=0
        for i in line1:
            if(is_passive(re.sub(r'[^\x00-\x7f]',r'', i))):
                count_passive += 1
                count_passive1.append(re.sub(r'[^\x00-\x7f]',r'', i))
        
                
        if(count_passive > 0):
            co_pa= 1
        elif(len(line1)==0):
            co_pa= 1
            
        else:
            co_pa=0
            ac += 5
        #print(impact)
        count_tense1=[]
        co_ta=0
        count_tenses=0
        for i in line1:
            if(tenses_res(re.sub(r'[^\x00-\x7f]',r'', i))):
                count_tenses += 1
                count_tense1.append(re.sub(r'[^\x00-\x7f]',r'', i))
                
        if(count_tenses >= 5):
            co_ta= 1
        elif(len(line1)==0):
            co_ta= 1
            
        else:
            co_ta=0
            ac += 5
            
        if(len(line1)==0):
            sections['paragraph']=0 
        elif sections['paragraph'] <= 2:
            ac += 5
            
        
        #print(sections.keys())
        
        cont=[]
        contact_all=contact_details(text_main)
        for elem in contact_all:
            if elem:
                if len(contact_all[0]) == 0:
                    cont.append('email')
                if len(contact_all[1]) == 0:
                    cont.append('phone')
                if len(contact_all[2]) == 0:
                    cont.append('linkedin')
                if len(contact_all[0]) !=0 and len(contact_all[1])!=0 and len(contact_all[2])!=0:
                    cont.append('all')
                    break

            if elem not in contact_all:
                cont.append("none")
            
            
        management = ['budgeting', 'business planning', 'business re-engineering',
        'change management', 'consolidation', 'cost control',
        'decision making', 'developing policies', 'diversification',
        'employee evaluation', 'financing', 'government relations',
        'hiring', 'international management' ,'investor relations',
        'ipo' ,'joint ventures', 'labour relations',
        'merger & acquisitions', 'multi-sites management', 'negotiation',
        'profit & loss', 'organizational development', 'project management',
        'staff development', 'strategic partnership', 'strategic planning',
        'supervision' ]
        
        operations = ['bidding', 'call centre operations', 'continuous improvement',
        'contract management', 'environmental protection', 'facility management',
        'inventory control', 'manpower planning','operations research',
        'outsourcing', 'policies & procedures', 'project co-ordination',
        'project management'] 
        
        production = [
        'equipment design', 'equipment maintenance & repair',
        'equipment management', 'iso 9xxx / 1xxxxx', 'tqm',
        'order processing', 'plant design & layout', 'process engineering',
        'production planning', 'quality assurance', 'safety engineering']
        
        logistics= [
        'distribution', 'transportation', 'jit',
        'purchasing & procurement', 'shipping', 'traffic management',
        'warehousing']
        
        researchanddevelopment = ['design & specification', 'diagnostics', 'feasibility studies',
        'field studies', 'lab management', 'lab design',
        'new equipment design', 'patent application', 'product development',
        'product testing', 'prototype development', 'r&d management',
        'simulation dev.',' statistical analysis', 'technical writing']
        
        sales= ['account management', 'b2b', 'contract negotiation',
        'customer relations', 'customer service', 'direct sales',
        'distributor relations', 'e-commerce', 'forecasting',
        'incentive programs', 'international business development',
        'international expansion', 'new account development', 'proposal writing',
        'product demonstrations', 'telemarketing', 'trade shows',
        'sales administration', 'sales analysis', 'sales kits',
        'sales management', 'salespersons recruitment', 'show room management',
        'sales support', 'sales training']
        
        marketing = ['advertising', 'brand management', 'channel marketing',
        'competitive analysis', 'copywriting', 'corporate identity',
        'image development', 'logo development', 'market research & analysis',
        'marketing communication', 'marketing plan', 'marketing promotions',
        'media buying/evaluation', 'media relations', 'merchandising',
        'new product development', 'online marketing','packaging',
        'pricing', 'product launch']
        
        administration = [
        'contract negotiation', 'equipment purchasing', 'forms and methods',
        'leases', 'mailroom management', 'office management',
        'policies & procedures', 'reception', 'records management',
        'security', 'space planning', 'word processing']
        
        legal = [
        'contract preparation', 'copyrights & trademarks', 'corporate law',
        'company secretary', 'employment ordinance', 'ipo',
        'intellectual property', 'international agreements', 'licensing',
        'mergers & acquisitions', 'patents', 'shareholder proxies',
        'stock administration']
        
        financeandaccounting = [
        'accounting management', 'accounts payable', 'venture capital relations',
        'accounts receivable', 'acquisitions & mergers', 'actuarial/rating analysis',
        'auditing','banking relations', 'budget control',
        'capital budgeting', 'capital investment', 'cash management',
        'cost accounting', 'cost control', 'credit/collections',
        'debt negotiations', 'equity/debt management', 'feasibility studies',
        'financial analysis', 'financial reporting', 'financing',
        'forecasting', 'foreign exchange', 'general ledger',
        'insurance', 'internal controls', 'investor relations',
        'ipo', 'lending', 'lines of credit',
        'management reporting', 'payroll', 'fund management',
        'profit planning', 'risk management', 'stockholder relations',
        'tax treasury', 'investor presentations']
        
        humanresources = [
        'arbitration/mediation', 'career counseling', 'career coaching',
        'classified advertisements', 'company orientation', 'workforce forecast/planning',
        'compensation & benefits', 'corporate culture', 'training administration',
        'employee discipline', 'employee selection', 'executive recruiting',
        'grievance resolution', 'human resources management',
        'industrial relations', 'job analysis', 'labour negotiations',
        'outplacement', 'performance appraisal', 'salary administration',
        'succession planning', 'team building', 'training']
        
        informationandtechnology = [
        'algorithm development', 'application database administration',
        'applications development', 'business systems planning', 'web site editor',
        'capacity planning', 'crm', 'cad',
        'edi', 'enterprise asset management', 'eap',
        'enterprise resource planning', 'erp', 'hardware management',
        'information management', 'integration software', 'intranet development',
        'java', 'c+++', 'c language','python','r language','ruby','html','javascript','c#','objective-c','php',
            'sql','shift','portal design/development',
        'software customization', 'software development', 'system analysis',
        'system design', 'system development', 'technical evangelism',
        'technical support', 'technical writing', 'telecommunications',
        'tracking system', 'unix', 'usability engineering',
        'user education', 'user documentation', 'user interface',
        'vendor sourcing', 'voice & data communications',
        'web development/design', 'web site content writer', 'word processing']
        
        creative = [
        'character development' ,'creative writing', 'drawing',
        'musical composition', 'story line development', 'visual composition']
        
        design= [
        'colour theory', 'dreamweaver', 'flash',
        'freehand', 'illustrator', 'photoshop',
        'picasa', 'corel draw', 'typography',
        'print design & layout', 'photography']
        
        publicrelation = [
        'b2b communication', 'community relations', 'speech writing',
        'corporate image', 'corporate philanthropy', 'corporate publications',
        'corporate relations', 'employee communication', 'event planning',
        'fund raising', 'government relations', 'investor collateral',
        'media presentations', 'press release', 'risk mgt communication']
        ab = text_main.lower()
        sentence = nltk.tokenize.sent_tokenize(ab)
        comp1 = check(sentence,management)
        #converting list of lists to a flat list
        # comp1 = [item for elem in comp1 for item in elem]
        try:
            comp1_count = len(comp1)
        except:
            comp1_count = 0
        comp2 = check(sentence,operations)
        try:
            comp2_count = len(comp2)
        except:
            comp2_count = 0
        
        comp3 = check(sentence,production)
        try:
            comp3_count = len(comp3)
        except:
            comp3_count = 0
        
        comp4 = check(sentence,logistics)
        try:
            comp4_count = len(comp4)
        except:
            comp4_count = 0
        
        comp5 = check(sentence,researchanddevelopment)
        try:
            comp5_count = len(comp5)
        except:
            comp5_count = 0
        comp6 = check(sentence,sales)
        try:
            comp6_count = len(comp6)
        except:
            comp6_count = 0
        
        comp7 = check(sentence,marketing)
        try:
            comp7_count = len(comp7)
        except:
            comp7_count = 0
        
        comp8 = check(sentence,administration)
        try:
            comp8_count = len(comp8)
        except:
            comp8_count = 0
        comp9 = check(sentence,legal)
        try:
            comp9_count = len(comp9)
        except:
            comp9_count = 0
        
        comp10 = check(sentence,financeandaccounting)
        try:
            comp10_count = len(comp10)
        except:
            comp10_count = 0
        comp11 = check(sentence,humanresources)
        try:
            comp11_count = len(comp11)
        except:
            comp11_count = 0
        
        comp12 = check(sentence,informationandtechnology)
        try:
            comp12_count = len(comp12)
        except:
            comp12_count = 0
        
        comp13 = check(sentence,creative)
        try:
            comp13_count = len(comp13)
        except:
            comp13_count = 0
        
        comp14 = check(sentence,design)
        try:
            comp14_count = len(comp14)
        except:
            comp14_count = 0
        
        comp15 = check(sentence,publicrelation)
        try:
            comp15_count = len(comp15)
        except:
            comp15_count = 0

        
        
        
        match_dict = {'management' : comp1, 'operations': comp2, 'production': comp3, 'logistics': comp4,
                    'Research & Development': comp5,'Sales': comp6, 'Marketing': comp7,
                    'Administration': comp8, 'Legal': comp9, 'Finance & Accounting': comp10,
                    'Human Resources': comp11,'Information Technology': comp12,
                    'creative':  comp13,'design': comp14, 'publicrelation':comp15} 
        
        count_dict = {'management' : comp1_count, 'operations': comp2_count, 'production': comp3_count, 
                    'logistics': comp4_count,
                    'Research & Development': comp5_count,'Sales': comp6_count, 'Marketing': comp7_count,
                    'Administration': comp8_count, 'Legal': comp9_count, 'Finance & Accounting': comp10_count,
                    'Human Resources': comp11_count,'Information Technology': comp12_count,
                    'creative':  comp13_count,'design': comp14_count, 'publicrelation':comp15_count}


        count_competancies=[]
        for i in count_dict.keys():
            if(count_dict[i]!=0):
                count_competancies.append(i)
        sumaa=0
        for key in count_dict.keys():
            sumaa+=count_dict[key]
                
        print(sentence)
        print("Hey",len(match_dict))
        print(count_dict)
        print(count_competancies)
        ab = text_main.lower()
        sentence = nltk.tokenize.sent_tokenize(ab)

        barplot(count_dict)
        
        session['bared'] = count_dict
        count_dict_dict={}
        stop_words = set(stopwords.words('english')) 
        filtered_sentence = [w for w in sentence if not w in stop_words] 
        for i in filtered_sentence:
            count_dict_dict[i]=filtered_sentence.count(i)

        #wordcloud(count_dict_dict)
                
        if ed_date_format_list[1]==1:
            pres-=10
        # if ex_date_format_list[1]==1:
        #     pres-=10
        
        namee=extract_name(text_main)
        if(len(match_dict)==15):
            empty_competency = "You might want to add few competencies in your resume as it's an efficient way to provide comprehensive proof that you are qualified for a certain job. "

        # if (len(match_dict['management'] == 0) and (len(match_dict['operations'] == 0):
        #     print("Yo")
        #namee=' '.join(w.capitalize() for w in namee.split())
        #print(namee,cont,count_tense1,count_passive1,sections['edu_year'],sections['exp_year'])    
        #end of check
        print(pro_msg,edu_msg,sections['redundancy'],vol_msg,cert_msg,link_msg,ach_msg,act_msg,co_pa)
        return render_template('services.html', results=sections,empty_competency=empty_competency,name=namee,fct_msg=fct_msg,filler_list=filler_list,wc=word_count,pro_msg=pro_msg,edu_msg=edu_msg,matched_comment= rev,jd_msg=jd_msg,score= sections['Score'],email=email,education=edu,rud_mdg=sections['redundancy'],vol_msg=vol_msg,cert_msg=cert_msg,link_msg=link_msg,ach_msg = ach_msg,count_pass=co_pa,count_tense=co_ta,act_msg=act_msg,para=sections['paragraph'],action_list=list(set(action_list)),count_tense1=count_tense1,count_passive1=count_passive1,contacts=cont,edu_year=sections['edu_year'],exp_year=sections['exp_year'],imp_for=improper_format,fed=fed,fex=fex,fsk=fsk,fce=fce,fpe=fpe,faw=faw,fvo=fvo,ed_correct_year=ed_date_format_list[0],ed_incorrect_year=ed_date_format_list[1],ex_correct_year=ex_date_format_list[0],ex_incorrect_year=ex_date_format_list[1],count_dict=count_dict,match_dict=match_dict,count_competancies=count_competancies,sumaa=sumaa, depth=int(((ac+rd)/30*100)),pres=int(pres/25*100),impact=int(impact/45 *100))
        #return render_template('display.html', results=sections)   
    except Exception as e:
        print(e)
        return render_template('error.html')


def docx1(name):
    global text_main,length
    resume= docx2txt.process(name)
        # f = open('jd.txt', 'r')
        # jd= f.read()
    jd=session['data']
        # print(jd)
    # print(resume)
    res = len(resume.split())
    page = math.ceil(res/700)
    length = page
    print("Number of Pages ",page) 
    if(page > 2):
        print("Try to shorten CV below 2 pages")
        #text =[resume, jd]
        # print(get_year(resume,resume))
    text_main = resume
        #kk = analyser(text)
        #return kk
    

def pdf(name):
    global text_main,length
    c=repr(extract_text(name))
        
        #print(c)

        # f = open('jd.txt', 'r')
    jd= session['data']  
        # print(txt)
        #text =[c, jd]
        
    pdf = PdfFileReader(open(name,'rb'))
    page = pdf.getNumPages()
    length = page
    print("Number of Pages ",page)
    if(page > 2):
        print("Try to shorten your CV below 2 pages")
        #kk = analyser(text)
    text_main = c
        
    


# def analyser(text):
#     cv =CountVectorizer()
#     count_matrix = cv.fit_transform(text)
#     matched= cosine_similarity(count_matrix)[0][1]*100
#     matched= round(matched,2)
#     doc1 = nlp(text[0])
#     doc2 = nlp(text[1])
#     sim = doc1.similarity(doc2)*100
#     sim= round(sim,1)
#     # print("Your resume is about "+str(sim)+"%")
#     if(sim > 80):
#         sim=sim*0.9

#     l = str(sim)
#     return l
def Find(string): 
    regex = r"(?:https?:)?\/\/(?:[\w]+\.)?linkedin\.com\/in\/(?P<permalink>[\w\-\_À-ÿ%]+)\/?"
    url = re.findall(regex,string)
    return url

def actionwords(string):
    #count=0
    No_of_actionVerbs=[]
    test_list = ['accelerated', 'achieved', 'attained', 'completed', 'conceived', 'convinced',
             'discovered', 'doubled', 'effected', 'eliminated', 'expanded', 'expedited', 
             'founded', 'improved', 'increased', 'initiated', 'innovated', 'introduced', 
             'invented', 'launched', 'mastered', 'overcame', 'overhauled', 'pioneered', 
             'reduced', 'resolved', 'revitalized', 'spearheaded', 'strengthened', 
             'transformed', 'upgraded', 'tripled', 'addressed', 'advised', 'arranged', 
             'authored', 'co-authored', 'co-ordinated', 'communicated', 'corresponded', 
             'counselled', 'developed', 'demonstrated', 'directed', 'drafted', 'enlisted',
             'facilitated', 'formulated', 'guided', 'influenced', 'interpreted',
             'interviewed', 'instructed', 'lectured', 'liased', 'mediated', 
             'moderated', 'motivated', 'negotiated', 'persuaded', 'presented', 'promoted', 
             'proposed', 'publicized', 'recommended', 'reconciled', 'recruited', 
             'resolved', 'taught', 'trained', 'translated', 'composed','conceived','created',
             'designed', 'developed', 'devised', 'established', 'founded', 'generated', 
             'implemented', 'initiated', 'instituted', 'introduced', 'launched','opened',
             'originated','pioneered', 'planned', 'prepared', 'produced','promoted', 
             'started', 'released', 'administered', 'analyzed', 'assigned', 'chaired', 
             'consolidated', 'contracted', 'co-ordinated', 'delegated', 'developed',
             'directed', 'evaluated', 'executed', 'organized', 'planned', 'prioritized',
             'produced', 'recommended', 'reorganized', 'reviewed', 'scheduled', 'supervised', 
             'managed', 'guided', 'advised', 'coached', 'conducted', 'directed', 'guided',
             'demonstrated', 'illustrated','managed', 'organized', 'performed', 
             'presented', 'taught', 'trained', 'mentored', 'spearheaded', 'authored', 
             'accelerated', 'achieved', 'allocated', 'completed', 'awarded', 'persuaded',
             'revamped', 'influenced', 'assessed', 'clarified', 'counseled', 'diagnosed',
             'educated', 'facilitated', 'familiarized', 'motivated', 'referred', 
             'rehabilitated', 'reinforced', 'represented', 'moderated', 'verified', 
             'adapted', 'coordinated', 'developed', 'enabled', 'encouraged', 'evaluated',
             'explained', 'informed', 'instructed', 'lectured', 'stimulated', 'analyzed',
             'assessed', 'classified', 'collated', 'defined', 'devised', 'established', 
             'evaluated', 'forecasted', 'identified', 'interviewed', 'investigated', 
             'researched', 'tested', 'traced', 'designed', 'interpreted', 'verified', 
             'uncovered', 'clarified', 'collected', 'critiqued', 'diagnosed', 'examined',
             'extracted', 'inspected', 'inspired', 'organized', 'reviewed', 'summarized', 
             'surveyed', 'systemized', 'arranged', 'budgeted', 'composed', 'conceived', 
             'conducted', 'controlled', 'co-ordinated', 'eliminated', 'improved', 'investigated', 
             'itemised', 'modernised', 'operated', 'organised', 'planned', 'prepared', 'processed', 
             'produced', 'redesigned', 'reduced', 'refined', 'researched', 'resolved', 'reviewed',
             'revised', 'scheduled', 'simplified', 'solved', 'streamlined', 'transformed', 
             'examined', 'revamped', 'combined', 'consolidated', 'converted', 'cut', 'decreased', 
             'developed', 'devised', 'doubled', 'tripled', 'eliminated', 'expanded', 'improved', 
             'increased', 'innovated', 'minimised', 'modernised', 'recommended', 'redesigned', 
             'reduced', 'refined', 'reorganised', 'resolved', 'restructured', 'revised', 'saved', 
             'serviced', 'simplified', 'solved', 'streamlined', 'strengthened', 'transformed', 
             'trimmed', 'unified', 'widened', 'broadened', 'revamped', 'administered', 'allocated', 
             'analyzed', 'appraised', 'audited', 'balanced', 'budgeted', 'calculated', 'computed', 'developed', 
             'managed', 'planned', 'projected', 'researched', 'restructured', 'modelled', 'acted',
             'conceptualized', 'created', 'customized', 'designed', 'developed', 'directed', 'redesigned',
             'established', 'fashioned', 'illustrated', 'instituted', 'integrated', 'performed', 'planned', 
             'proved', 'revised', 'revitalized', 'set up', 'shaped', 'streamlined', 'structured', 'tabulated',
             'validated', 'approved', 'arranged', 'catalogued', 'classified', 'collected', 
             'compiled', 'dispatched', 'executed', 'generated', 'implemented', 'inspected',
             'monitored', 'operated', 'ordered', 'organized', 'prepared', 'processed', 'purchased', 
             'recorded', 'retrieved', 'screened', 'specified', 'systematized']
    test_string=string.lower()
    res = [ele for ele in test_list if(ele in test_string)]
    No_of_actionVerbs.append(len(res))
    No_of_actionVerbs.append(res)
    print("Total number of action verbs used: ",No_of_actionVerbs[0],type(No_of_actionVerbs[0]))
    return(No_of_actionVerbs)

def fillerwords(string):
    #count=0
    No_of_fillerwords=[]
    test_list = ['capable','scalable', 'hard-work', 'hard work', 'problem-solve', 'creative', 'problem solve', 'innovative','motivated', 'skillful', 'communication-skill','coommunication skill','highly qualified', 'highly-qualified', 'results-focussed', 'result-focussed','results focussed', 'result focussed', 'effectual leader', 'effectual-leader','energetic','confident','professional','successfully', 'team player', 'team-player','responsible for','entrepreunerial','best of breed','detail oriented','detail-oreinted','seasoned','referances available by request','ambitious','punctual','go-getter','go getter','honest','strategic thinker','synnergy']
    test_string=string.lower()
    res = [ele for ele in test_list if(ele in test_string)]
    No_of_fillerwords.append(len(res))
    No_of_fillerwords.append(res)
    #print("Total number of action verbs used: ",No_of_actionVerbs[0],type(No_of_actionVerbs[0]))
    return(No_of_fillerwords)


def redundancy(string):
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    text=string.lower()
    no_punct = ""
    for char in text:
        if char not in punctuations:
            no_punct = no_punct + char
    text_tokens = word_tokenize(no_punct)

    text = [word for word in text_tokens if not word in stopwords.words()]
    dictOfElems = RedundancyCheck(text)
    redundant_words = list(dictOfElems.values())
    count = sum(redundant_words) - len(redundant_words)
    return count
    
    
def RedundancyCheck(listOfElems):
    dictOfElems = dict()
    for elem in listOfElems:
        if elem in dictOfElems:
            dictOfElems[elem] += 1
        else:
            dictOfElems[elem] = 1    
 
    dictOfElems = { key:value for key, value in dictOfElems.items() if value > 5}
    return dictOfElems

def extract(text):
    c=""
    year=[]
    for i in text:
        c+=i+" "
    for key in c:
        year = re.findall('((?:19|20)\d\d)', c)
    year.sort()
    return(year)

def is_passive(sentence):
    matcher = Matcher(nlp.vocab)
    doc = nlp(sentence)
    passive_rule = [{'DEP': 'nsubjpass'}, {'DEP': 'aux', 'OP': '*'}, {'DEP': 'auxpass'}, {'TAG': 'VBN'}]
    matcher.add('Passive', None, passive_rule)
    matches = matcher(doc)
    count =0
    if matches:
        return True
    else:
        return False
    

def check_for_tense(sentence):
    text = word_tokenize(sentence)
    tagged = pos_tag(text)

    tense = dict()
    tense["future"] = len([word for word in tagged if word[1] == "MD"])
    tense["present"] = len([word for word in tagged if word[1] in ["VBP", "VBZ","VBG"]])
    tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]]) 
    return(tense)

def tenses_res(str):
    tenses_check = check_for_tense(str)
    new_list = list(tenses_check.values())
    if new_list[0] == 0 and new_list[1] == 0:
        return False
    elif new_list[1] == 0 and new_list[2] == 0:
        return False
    elif new_list[0] == 0 and new_list[2] == 0:
        return False
    else:
        return True
    
def paragraph_check(str):
    Counter = 0
    for i in str: 
        if i: 
            Counter += 1
            
    if Counter > 5:
        return 0
    else:
        return 1
    
def contact_details(string):
    contact = []
    phone=re.findall('(?:\+[1-9]\d{0,2}[- ]?)?[1-9]\d{9}', string)
    email=re.findall(r"([a-zA-Z0-9.-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9_-]+)",string)
    linkedin_username = re.findall(r"(?:https?:)?\/\/(?:[\w]+\.)?linkedin\.com\/in\/(?P<permalink>[\w\-\_À-ÿ%]+)\/?",string)
    if len(linkedin_username) != 0:
        linkedin_username[0] = 'https://www.linkedin.com/in/'+ linkedin_username[0]
    contact.append(email)
    contact.append(phone)
    contact.append(linkedin_username)
    return contact



def extract_name(resume_text):
    nlp_text = nlp(resume_text)
    matcher = Matcher(nlp.vocab)
    
    # First name and Last name are always Proper Nouns
    pattern = [[{'POS': 'PROPN'}, {'POS': 'PROPN'}]]
    
    matcher.add('NAME', None, *pattern)
    
    matches = matcher(nlp_text)
    
    for match_id, start, end in matches:
        span = nlp_text[start:end]
        return span.text    
def date_format(str1): 
    c=""
    for i in str1:
        c+=i+" "
    #print(str1)
    #print(c)
    keywords = ['jan', 'feb', 'mar','apr', 'may','jun', 'jul', 'aug', 'sep', 'oct','nov', 'dec']
    string = '20'
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    # file = open('dashmesh84.txt')
    # read = file.read()
    # text = str(read).lower()
    # print(text)
    
    text=c
    Text = ""
    for char in text:
        if char not in punctuations:
            Text = Text + char
            
    two_dig = re.findall(r"\b\d{2}\b", Text)
    four_dig = re.findall('((?:19|20)\d\d)', text)
    current_time=datetime.datetime.now()
    
    
    month_yyyy = []
    month_yy = []
    only_year = []
    correct_format = 0
    wrong_format = 0
    
    yyyy_mm1 = re.findall('\d{4}-\d{2}', text)
    if yyyy_mm1:
        correct_format = 1
    mm_yyyy1 = re.findall('\d{2}-\d{4}', text)
    if mm_yyyy1:
        correct_format = 1
    mm_yyyy2 = re.findall('\d{2}/\d{4}', text)
    if mm_yyyy2:
        correct_format = 1
    yyyy_mm2 = re.findall('\d{4}/\d{2}', text)
    if yyyy_mm2:
        correct_format = 1
    # print(yyyy_mm1)
    # print(yyyy_mm2)
    # print(mm_yyyy1)
    # print(mm_yyyy2)
    
    try:
        if four_dig:
            for i in four_dig:
                var = i
                li = list(Text.split(" "))
                #print(li)
    
                if var in li:
                    indexx = li.index(var)
                    prev = li[indexx-1]
                    #print(prev)
                    li.remove(i)
                    for j in keywords:
                         #print(j)
                         if j in prev:
                             month_yyyy.append(var)
                             #print(string + var)
                             break
                         else:
                             wrong_format=1
                             continue
    
        # print(month_yyyy)
        if month_yyyy:
            correct_format = 1
        
        if two_dig:
            for i in two_dig:
                a = i
                #print(a)
                li = list(Text.split(" "))
    
                indexx = li.index(a)
                prev = li[indexx-1]
                #print(prev)
                li.remove(i)
                for j in keywords:
                    #print(j)
                    if j in prev:
                        if a>int(str(current_time)[2:4]):
                            month_yy.append('19' + a)
                            #print(string + a)
                            break
                        else:
                            month_yy.append(string + a)
                     
                    else:
                        continue
   
    except:
        correct_format = 0
        wrong_format = 0
        
                        

                    
    # print(month_yy)
    if month_yy:
        wrong_format = 1
    
    
    if four_dig:
        only_year.append(four_dig)
    only_year = [ item for elem in only_year for item in elem]
    
    if only_year:
        for elem in only_year:
            if elem not in month_yyyy:
                wrong_format = 1
    k=[]
    k.append(correct_format)
    k.append(wrong_format)
    return k

def check(sent,wrd):
    c=[]
    for i in sent:
        for j in wrd:
            if j in i:
                c.append(j)
    
    return list(set(c))

def barplot(count_dict):
    #count_dict = {'informationandtechnology': 14, 'administration': 10, 'humanresources': 3, 'financeandaccounting': 6, 'legal': 3}
    length = len(count_dict)
    li =[]
    for i in range(1,length):
        li.append(i)

    keys = [k for k in count_dict]
    # print(a)
    values = [count_dict[k] for k in count_dict]
    # print(b)

    fig = go.Figure([go.Bar(x=keys, y=values)])
    fig.write_html("./templates/file.html")
    

def wordcloud(count_dict):
    wordcloud = WordCloud(width=800, height=400, background_color="black",colormap="Blues").generate_from_frequencies(frequencies=count_dict)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.margins(x=0, y=0)
    #plt.show()
    fig = plt.figure()
#plot sth

    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

    html = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Document</title></head><body>' + '<img src=\'data:image/png;base64,{}\'>'.format(encoded) + '</body></html>'

    with open('./templates/wrdcloud.html','w') as f:
        f.write(html)





    
    
@app.route('/details')
def detailed():
    return render_template('detailed.html')


@app.route('/',methods= ["GET",'POST'])
@app.route('/home',methods= ["GET",'POST'])
def resume():
    return render_template('index.html')

@app.route('/demo',methods= ["GET",'POST'])
def demo():
    return render_template('services.html')


@app.route('/barploted')
def barploted():
    return render_template('file.html')

@app.route('/wordclouded')
def wordclouded():
    return render_template('wrdcloud.html')
    

@app.route('/analyse',methods= ["GET",'POST'])
def analyse():
    if request.method == 'POST':
        session.pop('data', None)
        session['data'] = request.form['jd']
        
        print(session['data'])
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No Selected File')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename= secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            print('Success')
            return redirect (url_for('uploaded_file',filename=filename))
    return render_template('elements.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def uploadfile():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'

@app.route('/jd',methods= ["GET",'POST'])
def jd_analyse():
    if request.method == 'POST':
        session.pop('data', None)
        session['data'] = request.form['jd']
        
        print(session['data'])
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No Selected File')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename= secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            print('Success')
            return redirect (url_for('jd_file',filename=filename))
    return render_template('jd.html')

@app.route('/jd/<filename>')
def jd_file(filename):
    f_name = os.path.join(app.config['UPLOAD_FOLDER'],filename)
    # return f_name
    global text_main,length,match
    file_name = f_name
    print(f_name)
    impact = 10
    pres =0
    text_main = ""
    edu_msg =0 
    vol_msg=0
    pro_msg=0
    if(file_name[-3:]=="pdf"):
        print("File is in pdf")
        match = float(pdf(file_name))
        if (float(match) == 0):
            jd_msg = "If it shows zero, probably you have not specified the JD in it field. Try adding a JD to check how accurately your resume matches with the Job."
        elif (float(match) < 50):
            jd_msg = "With " +str(match) + "% score you might need to add more skills related to the Job you have been looking for. Try aiming for a score above 80%"
        else:
            jd_msg ="With " +str(match) + "% score you seem to be an apt fit for the Job you have been looking for. "
    elif(file_name[-4:] == "docx" or file_name[-3:] == "doc" ):
        print("File is in docx")
        match = docx1(file_name)
        if (float(match) == 0.0):
            jd_msg = "If it shows zero, probably you have not specified the JD in it field. Try adding a JD to check how accurately your resume matches with the Job."
        elif (float(match) < 50):
            jd_msg = "With " +str(match) + " % score you might need to add more skills related to the Job you have been looking for. Try aiming for a score above 80%"
        else:
            jd_msg ="With " +str(match) + " % score you seem to be an apt fit for the Job you have been looking for. "
    else:
        print("Invalid Fileformat - Supported docx or pdf")
    #print (text_main)
    text_count=text_main.split(" ")
    word_count=len(text_count)
    liness=[]
    line=""
    for i in text_main:
        if(i!='\n'):
            line+=i
        else:
            liness.append(line)
            line=""
    line1=[]
    for line in liness:
        if len(line)!=0:
            line1.append(line)
    
    phone=re.findall(r"(?<!\d)\d{10}(?!\d)", text_main)
    email=re.findall(r"([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)",text_main)
    #print(email)
    links= re.findall(r"(^(http\:\/\/|https\:\/\/)?([a-z0-9][a-z0-9\-]*\.)+[a-z0-9][a-z0-9\-]*)",text_main)
    mlink=[]
    for link in links:
        if 'facebook' in link:
            mlink.append(link)
        elif 'github' in link:
            mlink.append(link)
        elif 'linkedin' in link:
            mlink.append(link)
        else:
            links.remove(link)
    links=list(set(mlink))
    section=[]
    sections={}
    for x in line1:
        global keyword
        if ("expertise" not in x.lower()) and ("role" not in x.lower()) and ("core" not in x.lower()) and ("career" not in x.lower()) and ("technical" not in x.lower()) and ("award" not in x.lower()) and ("winning" not in x.lower()) and ("education" not in x.lower()) and ("experience" not in x.lower()) and ("project" not in x.lower()) and ("skill" not in x.lower()) and ("award" not in x.lower()) and ("project" not in x.lower()) and ("course" not in x.lower()) and ("certificat" not in x.lower()) and ("volunteer" not in x.lower()) and ("personal" not in x.lower()) and ("interest" not in x.lower()) and ("position" not in x.lower()):
            section.append(x)
            #print(section)
        elif (len(x.split(" "))>=4):
            section.append(x)
            #print(section)  
        else :
            sections[keyword] = section
            keyword = x
            section =[]
    
    sections['phone']=list(set(phone))
    sections['links']=mlink
    if (len(mlink) != 0):
        impact+=5
    imp_sec=["education","experience","expertise","role","career","skill","award","certificat","project",'volunteer']
    score = 0
    msg = []
    edu=0
    ach_msg = 0 #achievement variable message
    cert_msg = 0 #certification message flag
    sections['edu_year']=""
    sections['exp_year']=""
    sections['paragraph']=0
    for key in sections.keys():
        #print(key)
        for sec in imp_sec:
            if sec in key.lower():
                #print(sec,type(sec),"Hi")
                if(sec=="education" or sec=="school" or sec=="college"):
                    score +=10
                    pres+=10
                    edu = 1
                    edu_msg =1
                    sections['edu_year']=extract(sections[key])
                    sections['paragraph']+=paragraph_check(sections[key])
                    #print(dummy_edu)
                    msg.append("Education Section is Present")
                    break
                if(sec=="experience" or sec=="work experience" or sec=="job" or sec=="job titles" or sec=="position description" or sec=="work" or sec=="role"):
                    score +=20
                    sections['exp_year']=extract(sections[key])
                    impact+=20
                    sections['paragraph']+=paragraph_check(sections[key])
                    #print(dummy_exp)
                    msg.append("Experience Section is Present")
                    break
                if(sec=="skill"):
                    score +=20
                    msg.append("Skills Section is Present")
                    sections['paragraph']+=paragraph_check(sections[key])
                    break
                if(sec=="award"):
                    score +=5
                    impact+=5
                    ach_msg = 1
                    sections['paragraph']+=paragraph_check(sections[key])
                    msg.append("Awards/Achievement Section is Present")
                    break
                if(sec=="volunteer"):
                    pres+=5
                    score +=5
                    vol_msg =1
                    msg.append("Volunteering Section is Present")
                    break
                if(sec=="certificat"):
                    impact+=5
                    score +=10
                    cert_msg=1
                    msg.append("Certificate Section is Present")
                    break
                if(sec=="project"):
                    pres+=10
                    score +=10
                    pro_msg=1
                    sections['paragraph']+=paragraph_check(sections[key])
                    msg.append("Projects Section is Present")
                    break
    #print("EDU MSG",edu_msg)
    sections['Message']=msg
    # sections['Score']=round(((score/98)*100),2)
    rev=""
    '''misspelled = spell.unknown(text_main)
    sections["Errors"]=[]
    for word in misspelled :
        if(len(word))>3:
            sections["Errors"].append(word)'''
            
    stop_words = set(stopwords.words('english')) 
    d=""
    skillsets=0
    filtered_sentence=[]
    
    for i in sections.keys():
        if(i.lower()=="work experience"):
            score +=5
        if(i.lower()=="core competencies"):
            score +=5            
        if 'skill' in i.lower():
            skillsets=len(sections[i])
            for j in sections[i]:
                
                d=d+" "+j
            d = word_tokenize(d)
            # print("I am here 2")
            #print(d)
            for w in d: 
                if w not in stop_words: 
                    if(len(w)>3):
                        filtered_sentence.append(w)
    sections['SkCount']=skillsets
    sections['original']=filtered_sentence
    sections['linkedin']=Find(text_main)
    ck=sections['linkedin']
    link_msg=1
    if(len(ck) == 0):
        link_msg=0
    #print(type(len(ck)))
    #print('Heyo',sections['linkedin'])
    ac=0
    rd=0
    if actionwords(text_main) > 5:
        act_msg =1
        ac=10
        sections['action_word']="Your resume contains Action Verbs! Strong, unique action verbs show hiring managers that you have held different roles and skill sets. They also help your accomplishments stand out and make them more impactful."
    elif actionwords(text_main)<=5:
        act_msg =0
        sections['action_word']="Your resume doesnt contain much Action Verbs! Strong, unique action verbs show hiring managers that you have held different roles and skill sets. They also help your accomplishments stand out and make them more impactful. "
        
    
    
    #print(sections['action_word'])
    
    if redundancy(text_main) > 10:
        rd=5
        sections['redundancy']="1"
    elif redundancy(text_main)<=10:
        sections['redundancy']="0"
        
    
    #sections['edu_year']=extract(sections[dummy_edu])
    #print(sections['exp_year'])
    #print(sections['edu_year'])
    #print(sections['redundancy'])
    #print(filtered_sentence)
    sections['match']=match
    # Checking of resume score for message
    if(score == 100):
        rev="The score looks perfect but to get a more accurate comparison with the job you are looking for try analysing by adding Job Description"
    elif(score < 60):
        rev="This suggests there is a lot of room for improvement. But don't worry! We have highlighted a number of quick fixes you can make to improve your resume's score and your success rate. Try adding more missing skills into your resume to increase your match rate to 80% or above."
    else:
        rev="The score of "+ str(score)+" looks quite good however we have highlighted a number of quick fixes you can make to improve your resume's score. Try adding more missing skills into your resume to increase your match rate."
    sections["Review"]=rev
    sections["Length"]=length
    sections["WordCount"]=word_count
    if sections["WordCount"] <= 600 :
        score += 5
        sections['Message'].append("Word Count of the Resume is Optimal")
    else:
        sections['Message'].append("Word Count should be less than 600")

    if sections["Length"] <= 2 :
        score += 5
        sections['Message'].append("Length of Resume is Optimal")
    else:
        sections['Message'].append("Length of Resume should not exceed 2 pages")
    sections['Score']=round(((score/100)*100),2) #calculating score out of overall score.
    if(sections['Score'] >=90 and sections['Score'] <100):
        sections["Review"]="The Resume is correctly Parsed and Optimal. There may be some room for Improvement"
    if(sections['Score'] >=75 and sections['Score']<90):
        sections["Review"]="The Resume may be Correctly Parsed and Optimal. It is advised to pass DOCX Format in ATS Checker. There is certainly Some Room For Improvement"        
    count_passive=0
    co_pa=0
    for i in line1:
        if(is_passive(i)):
            count_passive += 1
            
    if(count_passive > 5):
        co_pa= 1
        
    else:
        co_pa=0
        ac += 5
    #print(impact)
    co_ta=0
    count_tenses=0
    for i in line1:
        if(tenses_res(i)):
            count_tenses += 1
            
    if(count_tenses >= 5):
        co_ta= 1
        
    else:
        co_ta=0
        ac += 5
        
    if sections['paragraph'] <= 2:
        ac += 5
    print("I am new")
    #end of check
    #print(pro_msg,edu_msg,sections['redundancy'],vol_msg,cert_msg,link_msg,ach_msg,act_msg)
    return render_template('service_jd.html', results=sections,pro_msg=pro_msg,edu_msg=edu_msg,matched_comment= rev,jd_msg=jd_msg,score= sections['Score'],email=email,education=edu,rud_mdg=sections['redundancy'],vol_msg=vol_msg,cert_msg=cert_msg,link_msg=link_msg,ach_msg = ach_msg,count_pass=co_pa,count_tense=co_ta,act_msg=act_msg,para=sections['paragraph'],depth=int(((ac+rd)/30*100)),pres=int(pres/25*100),impact=int(impact/45 *100))
    #return render_template('display.html', results=sections)   

@app.route('/about',methods= ["GET",'POST'])
def about():
    return render_template('about.html')


@app.route('/contact',methods= ["GET",'POST'])
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run()
