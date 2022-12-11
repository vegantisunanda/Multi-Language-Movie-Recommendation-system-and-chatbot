""" from gettext import install
import os
# hide TF warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  """

import os
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import random

app = Flask(__name__)

uname = ''
question_number = 0
language = ''
actor = ''
genre = ''
year = ''

import os
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd 

print(os.listdir())

# read csv file using pandas
df1 = pd.read_csv('English, Arabic_Dataset.csv')
df2 = pd.read_csv('Telugu_dataset .csv')

df1.rename(columns = {'title/الفيلم':'Title','cast/تمثيل':'Cast','genres/النوع':'Genre','Year/السنة':'Year','original_language/اللغة':'Language',},inplace = True)
df2.rename(columns = {'సినిమా పేరు':'Title', 'దర్శకుడు':'Director', 'నటులు':'Cast', 'శైలి':'Genre', 'తేదీ':'Date','సంవత్సరం':'Year','నెల':'Month','భాష':'Language','Soup/సూప్':'Soup' }, inplace = True)
df2['Language'] = 'te'

# remove brackets
df1['Cast'] = df1['Cast'].str.strip('[]')
df1['Genre'] = df1['Genre'].str.strip('[]')

# remove quotes
df1["Cast"] = df1["Cast"].str.replace(r"^'|,'$", "").str.replace("'", '')
df1["Genre"] = df1["Genre"].str.replace(r"^'|,'$", "").str.replace("'", '')

# inorder to add year into soup we need to conevrt into string formte
df1['Year']= df1['Year'].apply(str)
df2['Year']= df2['Year'].apply(str)

df1 = df1[~df1.Title.isin(df1[df1.duplicated(subset=['Title'])].Title.unique())].reset_index(drop=True)
df2 = df2[~df2.Title.isin(df2[df2.duplicated(subset=['Title'])].Title.unique())].reset_index(drop=True)

data_ref = pd.concat([df1[['Title', 'Cast', 'Year', 'Genre', 'Language']], df2[['Title', 'Cast', 'Year', 'Genre', 'Language']]]).dropna()

df1['Cast'] = df1['Cast'].str.replace(" ", '')

# create the new soup
df1['Soup'] = df1['Cast']+ '  ' + df1['Genre']+ '  ' + '  ' + df1['Language']

# Lower casing
df1['Soup'] = df1['Soup'].apply(lambda x: ' '.join(x.lower() for x in x.split()))

# remove comma from soup
# df1['Soup'] = df1['Soup'].str.replace(',', '')
df2['Soup'] = df2['Cast']+ '  ' + df2['Genre']+ '  ' + df2['Language']

data = pd.concat([df1[['Soup']], df2[['Soup']]]).dropna()

count = TfidfVectorizer(stop_words='english')
count_matrix1 = count.fit_transform(data['Soup'])

@app.route('/', methods=['GET', 'POST'])
def home():

    global uname, question_number, language, actor, genre, year
    question_number += 1

    if request.method == 'POST':
        print(request.form)
        if question_number==1:
            if request.form['reply_val']:
                uname = ' ' + request.form['reply_val'].title()
            return render_template('index.html', td=30, ed=20, ntd=3000, data=[["I am Multilingual Movie Recemmendation Bot So What language You want to be commincated with? 'en' for English 'ar' for Arabic, 'te' for Telugu "]], fixed=f"Hello{uname}! ")
 
                  
        if question_number==2:
            if 'ar' in request.form['reply_val'].lower():
                language = 'ar'
            elif 'te' in request.form['reply_val'].lower():
                language = 'te'
            elif 'en' in request.form['reply_val'].lower():
                language = 'en'
            else:
                ''
            if language=='ar':
                return render_template('index.html', td=200, ed=100, ntd=2000, data=[["شكرا لاختيارك العربية", "هل انت مستعد" ]], fixed=f"اختيار جيد يا{uname}! ")
            if language=='te':
                return render_template('index.html', td=200, ed=100, ntd=2000, data=[["తెలుగును ఎంచుకున్నందుకు ధన్యవాదాలు", "సరే మొదలు పెడదాం?"]], fixed=f"మంచి ఎంపిక{uname}! ")
            else:
                return render_template('index.html', td=200, ed=100, ntd=2000, data=[["I am really excited!", "Are you ready?"]], fixed=f"Great choice{uname}! ")
            
        # copy this for random chit-chat
        if question_number==3:
             if language=='ar':
                 return render_template('index.html', td=40, ed=80, ntd=3000, data=[["لكي اساعدك في ايجاد فلم في لغتك المفضلة", "اريدك ان تجيب على اسالة عن الفلم "]], fixed=f"اولا: ")
             if language=='te':
                 return render_template('index.html', td=200, ed=100, ntd=2500, data=[["మెరుగైన సమాధానాలతో నేను మీకు సహాయం చేయగలను", "కాబట్టి దయచేసి కొన్ని ప్రశ్నలకు సమాధానం ఇవ్వండి"]], fixed=f" ")
             else:
                 return render_template('index.html', td=200, ed=100, ntd=2000, data=[["So I can help you better!", "I need you to answer some questions plz!"]], fixed=f"First: ")
             #Input Entry
             
        if question_number==4:
            if language=='ar':
                return render_template('index.html', td=50, ed=80, ntd=3000, data=[["هل يوجد ممثل محدد؟", "لا تقلق، قاعدة بياناتي تملك اكثر من ١٠٠ ممثل و ممثلة"]], fixed=f"السؤال الاول: ")
            if language=='te':
                return render_template('index.html', td=200, ed=100, ntd=2000, data=[[":మీరు ఎవరి నటుడి సినిమాని చూడటానికి ఆసక్తిగా ఉన్నారు?"]] , fixed=f":1వ ప్రశ్న ")
            else:
                return render_template('index.html', td=200, ed=100, ntd=2000, data=[["Who is your favourite actor?", "Come on, you should have at least one favourite actor."]], fixed=f"Question 1: ")
            

        if question_number==5:
            if request.form['reply_val']:
                actor = ' ' + request.form['reply_val'].strip().title() + ' '
            if language=='ar':
                return render_template('index.html', td=200, ed=100, ntd=2000, data=[[f"ما هو نوع الفلم؟{' للـ '+actor if actor else ''} "]], fixed=f"السؤال الثاني: ")
            if language=='te':
                return render_template('index.html', td=200, ed=100, ntd=2000, data=[[f"మీకు ఏ సినిమా జానర్‌పై ఆసక్తి ఉంది?{' యొక్క'+actor if actor else ''} ", f"I can think of some {['comedy', 'romance', 'action', 'thriller', 'romcom'][np.random.randint(0,5,1)[0]]} ones..."]], fixed=f"2వ ప్రశ్న: ")
            else:
                return render_template('index.html', td=200, ed=100, ntd=2000, data=[[f"Which movie genre{' of'+actor if actor else ''} did you like most?", f"I can think of some {['comedy', 'romance', 'action', 'thriller', 'romcom'][np.random.randint(0,5,1)[0]]} ones..."]], fixed=f"Question 2: ")
            

        if question_number==6:
            if request.form['reply_val']:
                genre = request.form['reply_val'].strip()
            # return render_template('index.html', td=200, ed=100, ntd=2000, data=[make_reco(language + ' ' + actor.lower().replace(' ', '') + ' ' + genre)], fixed=f"We recommend ")
            if language == 'en':
                searchTerms = language + ' ' + actor.lower().replace(' ', '') + ' ' + genre
            else:
                searchTerms = language + ' ' + actor.replace(' ', '') + ' ' + genre
            print('---------------')
            print(language + ' ' + actor.lower().replace(' ', '') + ' ' + genre)
            print('---------------')
            if language=='ar':
                return render_template('index.html', td=10, ed=5, ntd=5000, data=[make_reco(searchTerms)], fixed=f"اقترح عليك مشاهدة: ")
            if language=='te':
                return render_template('index.html', td=10, ed=5, ntd=5000, data=[make_reco(searchTerms)], fixed=f":మేము సలహా ఇస్తున్నాము")
            else:
                return render_template('index.html', td=10, ed=5, ntd=5000, data=[make_reco(searchTerms)], fixed=f"We recommend ")
            


    question_number = 0
    return render_template('index.html', td=30, ed=20, ntd=3000, data=[["I am Regis and my job is to recmmend you movies in 3 languages" , "Provide me your name plz?"]], fixed="Hello!")

def make_reco(searchTerms):
    count_matrix2 = count.transform([searchTerms])
    cosine_sim2 = cosine_similarity(count_matrix1, count_matrix2) #getting a similarity matrix
    print(sorted(list(enumerate(cosine_sim2)), key=lambda x: x[1], reverse=True)[:10])
    idx = [i[0] for i in sorted(list(enumerate(cosine_sim2)), key=lambda x: x[1], reverse=True)][:5]
    print([data_ref.iloc[i]['Title']+' ('+data_ref.iloc[i]['Year']+') | ('+data_ref.iloc[i]['Genre']+') | '+data_ref.iloc[i]['Cast'] for i in idx])
    return [data_ref.iloc[i]['Title']+' ('+data_ref.iloc[i]['Year']+') | ('+data_ref.iloc[i]['Genre']+') | '+data_ref.iloc[i]['Cast'] for i in idx]




if __name__ == "__main__":
    app.run(debug=True, port=5001)
