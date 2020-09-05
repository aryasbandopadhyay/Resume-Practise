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
import jinja2
#from spellchecker import SpellChecker
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from pickle import dump, load
from nltk.corpus import brown
from itertools import dropwhile
from nltk import word_tokenize, pos_tag
import language_check

import spacy
nlp = spacy.load('en_core_web_sm')

#spell = SpellChecker()
#nltk.download('stopwords')
#nltk.download('punkt')



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
match=""
@app.route('/uploads/<filename>')
def uploaded_file(filename):
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
        match = docx(file_name)
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
    skillsets=1
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
    t=Tagger()
    count_passive=0
    co_pa=0
    for i in line1:
        if(t.is_passive(i)):
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
        
    
    
    
        
    #end of check
    #print(pro_msg,edu_msg,sections['redundancy'],vol_msg,cert_msg,link_msg,ach_msg,act_msg)
    return render_template('services.html', results=sections,pro_msg=pro_msg,edu_msg=edu_msg,matched_comment= rev,jd_msg=jd_msg,score= sections['Score'],email=email,education=edu,rud_mdg=sections['redundancy'],vol_msg=vol_msg,cert_msg=cert_msg,link_msg=link_msg,ach_msg = ach_msg,count_pass=co_pa,count_tense=co_ta,act_msg=act_msg,para=sections['paragraph'],depth=int(((ac+rd)/30*100)),pres=int(pres/25*100),impact=int(impact/45 *100))
    #return render_template('display.html', results=sections)   


def docx(name):
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
    text =[resume, jd]
    # print(get_year(resume,resume))
    text_main = resume
    kk = analyser(text)
    return kk
def pdf(name):
    global text_main,length
    c=""
    with pdfplumber.open(name) as pdf:
        for pages in pdf.pages:
            c +="\n" + str(pages.extract_text())
    # f = open('jd.txt', 'r')
    jd= session['data']  
    # print(txt)
    text =[c, jd]
    
    pdf = PdfFileReader(open(name,'rb'))
    page = pdf.getNumPages()
    length = page
    print("Number of Pages ",page)
    if(page > 2):
        print("Try to shorten your CV below 2 pages")
    kk = analyser(text)
    text_main = c
    return kk
def analyser(text):
    cv =CountVectorizer()
    count_matrix = cv.fit_transform(text)
    matched= cosine_similarity(count_matrix)[0][1]*100
    matched= round(matched,2)
    doc1 = nlp(text[0])
    doc2 = nlp(text[1])
    sim = doc1.similarity(doc2)*100
    sim= round(sim,1)
    # print("Your resume is about "+str(sim)+"%")
    if(sim > 80):
        sim=sim*0.9

    l = str(sim)
    return l
def Find(string): 
    regex = r"(?:https?:)?\/\/(?:[\w]+\.)?linkedin\.com\/in\/(?P<permalink>[\w\-\_À-ÿ%]+)\/?"
    url = re.findall(regex,string)
    return url

def actionwords(string):
    #count=0
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
    No_of_actionVerbs = len(res)
    print("Total number of acyion verbs used: ",No_of_actionVerbs)
    return(No_of_actionVerbs)

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
    for i in text:
        c+=i+" "
    for key in c:
        year = re.findall('((?:19|20)\d\d)', c)
    year.sort()
    return(year)

class Tagger:
    def __init__(self):
        if os.path.exists("tagger.pkl"):
            with open('tagger.pkl', 'rb') as data:
                tagger = load(data)
            self.tagger = tagger
        else:
            tagger = create_tagger()
            self.tagger = tagger
            self.save()

    def save(self):
        with open('tagger.pkl', 'wb') as output:
            dump(self.tagger, output, -1)

    def tag(self, sent):
        return self.tagger.tag(sent)

    def tag_sentence(self, sent):
        """Take a sentence as a string and return a list of (word, tag) tuples."""
        tokens = nltk.word_tokenize(sent)
        return self.tag(tokens)

    def is_passive(self, sent):
        return is_passive(self, sent)

def passivep(tags):
    """Takes a list of tags, returns true if we think this is a passive
    sentence.

    Particularly, if we see a "BE" verb followed by some other, non-BE
    verb, except for a gerund, we deem the sentence to be passive.
    """
    
    after_to_be = list(dropwhile(lambda tag: not tag.startswith("BE"), tags))
    nongerund = lambda tag: tag.startswith("V") and not tag.startswith("VBG")

    filtered = filter(nongerund, after_to_be)
    out = any(filtered)

    return out

def create_tagger():
    """Train a tagger from the Brown Corpus. This should not be called very
    often; only in the event that the tagger pickle wasn't found."""
    train_sents = brown.tagged_sents()

    # These regexes were lifted from the NLTK book tagger chapter.
    t0 = nltk.RegexpTagger(
        [(r'^-?[0-9]+(.[0-9]+)?$', 'CD'), # cardinal numbers
         (r'(The|the|A|a|An|an)$', 'AT'), # articles
         (r'.*able$', 'JJ'),              # adjectives
         (r'.*ness$', 'NN'),              # nouns formed from adjectives
         (r'.*ly$', 'RB'),                # adverbs
         (r'.*s$', 'NNS'),                # plural nouns
         (r'.*ing$', 'VBG'),              # gerunds
         (r'.*ed$', 'VBD'),               # past tense verbs
         (r'.*', 'NN')                    # nouns (default)
        ])
    t1 = nltk.UnigramTagger(train_sents, backoff=t0)
    t2 = nltk.BigramTagger(train_sents, backoff=t1)
    t3 = nltk.TrigramTagger(train_sents, backoff=t2)
    return t3

def is_passive(tagger, sent):
    tagged = tagger.tag_sentence(sent)
    tags = map(lambda tup: tup[1], tagged)
    return bool(passivep(tags))

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

if __name__ == '__main__':
    app.run()
