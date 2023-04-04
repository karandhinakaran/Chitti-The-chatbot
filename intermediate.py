# -*- coding: utf-8 -*-
"""Intermediate.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16AHTIUPiI_HNS4elYfgYKN2F1yEXq1-1

# Chitti the roboBot

Required installations for the Project
### The required installations
"""

# installing the required libraries for the project

# !pip install snscrape
# !pip install vaderSentiment
# !pip install TextBlob
# !pip install wikipedia 
# !pip install gtts
# !pip install keytotext
# !pip install spacy

"""### Disabling warnings """

import warnings
warnings.filterwarnings('ignore')

"""### Required import libraries"""

# all the import folders 
import pandas as pd
import snscrape.modules.twitter as sntwitter
import re
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import wikipedia
import random
from gtts import gTTS
import os
import requests, lxml
from bs4 import BeautifulSoup
import joblib
import string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import TfidfTransformer,TfidfVectorizer
from sklearn.pipeline import Pipeline
import spacy

"""### Connect the google drive"""

# from google.colab import drive
# drive.mount('/content/gdrive')

"""### Downloading nltk dependencies

"""

import nltk
nltk.set_proxy('https://proxy.example.com:3128', ('USERNAME', 'PASSWORD'))
nltk.download()
# nltk.download('stopwords')
# nltk.download('omw-1.4')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')

"""### For the general conversation bot created by me"""

def cleaner(x):
    return [a for a in (''.join([a for a in x if a not in string.punctuation])).lower().split()]

# PIPELINE PREVIOUSLY TRAINED ON GENERAL CONVERSATIONS


#Don't have the file.
# Pipe = joblib.load('/content/gdrive/MyDrive/Colab Notebooks/CHITTI_BRO/general_conversations/gen_conv.pkl')

"""### Google direct answer box scraping (not working)"""

##google direct answer box scrapper

headers = {
  "User-agent":
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}



def get_calculator_answerbox(content):
    # try: 
    params = {"q": content}
    html = requests.get('https://www.google.com/search', headers=headers, params=params)
    soup = BeautifulSoup(html.text, 'lxml')

    math_expression = soup.select_one('.XH1CIc').text.strip().replace(' =', '')
    calc_answer = soup.select_one('#cwos').text.strip()

    return "Expression: " + math_expression + '\n' + 'Answer: ' + calc_answer
    # except: 
    #     return 'sorry unable to process'




def get_weather_answerbox(content):
    try: 
        params = {
                "q": content + " weather", # query
                "gl": "uk"             # country to search from (United Kingdom)
                }
        response = requests.get('https://www.google.com/search', headers=headers, params=params)
        soup = BeautifulSoup(response.text, 'lxml')

        location = soup.select_one('#wob_loc').text
        weather_condition = soup.select_one('#wob_dc').text
        tempature = soup.select_one('#wob_tm').text
        precipitation = soup.select_one('#wob_pp').text
        humidity = soup.select_one('#wob_hm').text
        wind = soup.select_one('#wob_ws').text
        current_time = soup.select_one('#wob_dts').text

        return 'Weather condition: ' + weather_condition + '\n' + 'Temperature: ' +  tempature + '°C\n'
            #f'Current time: {current_time}\n'
    except:
        return 'sorry unable to process'


##add stocks, date, time, dictionary also



def get_converter_answerbox(content):
    try:
        params = {
            "q": content,
            "gl": "us"
        }
        html = requests.get('https://www.google.com/search', headers=headers, params=params)
        soup = BeautifulSoup(html.text, 'lxml')

        conversion = soup.select_one('.SwHCTb').text
        conversion_currency = soup.select_one('.MWvIVe').text
        return f"{conversion} {conversion_currency}"
    except: 
        return 'sorry unable to process'




def get_organic_result_answerbox(content):
    try:
        params = {
            'q': content,
            'gl': 'us'
        }
        html = requests.get('https://www.google.com/search', headers=headers, params=params)
        soup = BeautifulSoup(html.text, 'lxml')

        answer = soup.select_one('.XcVN5d').text
        return f"{answer}"
    except:
        return 'sorry unable to process'


params = {
    'q': 'hello in french',
    'gl': 'us'
}



def get_sport_matches_answerbox():
    try:
        html = requests.get('https://www.google.com/search', headers=headers, params=params)
        soup = BeautifulSoup(html.text, 'lxml')

        title = soup.select_one('.ofy7ae').text

        if soup.select_one('.mKwiob'):
            league = soup.select_one('.mKwiob').text
        else: league = 'Not mentioned'

        print(title, league, sep='\n')
        print()

        # zip() will get data in parallel but it will find all needed elements at once
        for first_team, second_team, first_score, second_score, status, match_date, video_highlight in zip(
            soup.select('.L5Kkcd+ .L5Kkcd span'),
            soup.select('.L5Kkcd:nth-child(5) span'),
            soup.select('.L5Kkcd:nth-child(5) .imspo_mt__t-sc .imspo_mt__tt-w'),
            soup.select('.imspo_mt__lt-t .imspo_mt__tt-w'),
            soup.select('.imspo_mt__match-status'),
            soup.select('.imspo_mt__ms-w div div :nth-child(1)'),
            soup.select('.BbrjBe')):

            match_status = status.text
            match_game_date = match_date.text
            match_video_highlight = video_highlight.select_one('a')['href']

            return match_status+ '\n' + match_game_date + '\n' + f"{first_team.text}: {first_score.text}" + '\n'  + f"{second_team.text}: {second_score.text}" + '\n'
    except:
        return 'sorry unable to process'

"""### For the general conversation bot
more advanced trained on 400M dataset
"""

# ! pip -q install transformers

from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
# import torch

model = BlenderbotForConditionalGeneration.from_pretrained("facebook/blenderbot-400M-distill")
tokenizer = BlenderbotTokenizer.from_pretrained("facebook/blenderbot-400M-distill")

def gen_conv(content):
    message = content
    inputs = tokenizer([message], return_tensors='pt')
    reply_ids = model.generate(**inputs)
    return f"{tokenizer.batch_decode(reply_ids, skip_special_tokens=True)[0]}"


print(gen_conv('Hello how are you'))



"""### For the tweets and mining opinions"""

#for the tweets

def clean_tweet(tweet):
    '''
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


def get_tweet_sentiment(tweet):
    '''
    Utility function to classify sentiment of passed tweet
    using textblob's sentiment method
    '''
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet))
    # set sentiment
    if analysis.sentiment.polarity > 0.3:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

key_word_detect = spacy.load('en_core_web_sm')

"""### Find names in the given input """

english_nlp = spacy.load('en_core_web_sm')

text = 'Tell me about Rohit Sharma.'

def remove_names(text):
    text += '.'
    no_name = text
    spacy_parser = english_nlp(text)
    for entity in spacy_parser.ents:
        if entity.label_ == 'PERSON':
            no_name = no_name.replace(entity.text, '')
        #print(f'Found: {entity.text} of type: {entity.label_}')
    return no_name

"""### The universal sentence encoder model for finding sentence similarity """

import tensorflow_hub as hub
from sklearn.metrics.pairwise import cosine_similarity
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

def similarity(sen1, sen2):
    sentences = [
    sen1,
    sen2,
    ]
    model = embed(sentences)
    return cosine_similarity(model)[0][1]

#test the model
sen1 = "tell me about"
sen2 = "Tell me about Rohit Sharma."
print(remove_names(sen2))
similarity(sen1, remove_names(sen2))

"""### The bot class"""

# all the required functions 

class bot(object):
    def __init__ (self):
        self.content = ''
        self.answer = ''

    def voice_recognition(self):
        self.content = input()

    def content_recognizer(self):
        #1-wikipedia,  2-twitter, 3-story
        sentences = ['Tell me about', 'What is your opinion on', 'Tell me a story']
        results = []
        ans = 3
        for i in sentences:
            results.append(similarity(i, remove_names(self.content)))
        ind = results.index(max(results))
        if results[ind] < 0.5:
            ans = 3
        else:
            ans = ind
        return ans
    #return the wikipedia summary for a given queiry
    def wikipedia_facts(self):
        try:
            k = wikipedia.search(self.content, results = 4)
            for i in k:
                 try:
                    self.answer = wikipedia.summary(k[0])
                    break
                 except:
                     pass
        except:
            self.answer = 'I do not know'

    # if user asks for links of any kind
    def google_scraper(self):
        pass

    #for general conversations
    # def gen_conversation(self):
    #     self.answer = Pipe.predict([self.content])[0]
    
    #bot trained on transformers
    def conversation(self):
        self.answer = gen_conv(self.content)
        
    ##opinion bot gives the opinion of the internet on a given topic
    def twitter_bot(self):
        scraper = sntwitter.TwitterSearchScraper(self.content)
        pos = 0
        neg = 0
        for i, tweet in enumerate(scraper.get_items()):
            if i>1000:
                break
            if get_tweet_sentiment(tweet.rawContent) == 'positive':
                pos += 1
            if get_tweet_sentiment(tweet.rawContent) == 'negative':
                neg += 1
        if pos >= neg:
            self.answer = 'The web has a positive opinion on the topic'
        else:
            self.answer = 'The web has a negative opinion on the topic'


    def story_bot(self):
        when = ['A few years ago', 'Yesterday', 'Last night', 'A long time ago','On 20th Jan']
        who = ['a rabbit', 'an elephant', 'a mouse', 'a turtle','a cat']
        name = ['Ali', 'Miriam','daniel', 'Hoouk', 'Starwalker']
        residence = ['Barcelona','India', 'Germany', 'Venice', 'England']
        went = ['cinema', 'university','seminar', 'school', 'laundry']
        happened = ['made a lot of friends','Eats a burger', 'found a secret key', 'solved a mistery', 'wrote a book']
        self.answer = random.choice(when) + ', ' + random.choice(who) + ' that lived in ' + random.choice(residence) + ', went to the ' + random.choice(went) + ' and ' + random.choice(happened)



    def initiator(self):
        initiate = ['Hello, how can i help you.', 
                    'Hello, how was the day today.',
                    'Hello, yoy can ask me anything you want.', 
                    'Hey, you still there.']
        self.answer = random.choice(initiate)

    def return_answer(self):
        print('chitti: ', self.answer)

    def text_to_voice(self):
        language = 'en'
        my_text = self.answer
        myobj = gTTS(text=my_text, lang=language, slow=False)
        myobj.save('recent_answer.mp3')
        os.system('mpg321 recent_answer.mp3')

    def main(self):
        while self.content != 'exit':
            os.system('cls')
            self.answer = ''
            self.voice_recognition()
            if self.content == 'exit':
                self.answer = 'GOOD BYE Have a great day'
            else:
                ans = self.content_recognizer()
                if ans == 0:
                    self.wikipedia_facts()
                elif ans == 1:
                    self.twitter_bot()
                elif ans == 2:
                    self.story_bot()
                elif ans == 3:
                    self.conversation()
            self.return_answer()

"""### Main"""

chitti = bot()
chitti.main()

