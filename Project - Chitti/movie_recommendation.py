from bs4 import BeautifulSoup as SOUP
import re
import requests as HTTP
import random
  
def url(emotion):
  
    if(emotion == "Sad"):
        urlhere = 'http://www.imdb.com/search/title?genres=drama&title_type=feature&sort=moviemeter, asc'

    elif(emotion == "Disgust"):
        urlhere = 'http://www.imdb.com/search/title?genres=musical&title_type=feature&sort=moviemeter, asc'

    elif(emotion == "Anger"):
        urlhere = 'http://www.imdb.com/search/title?genres=family&title_type=feature&sort=moviemeter, asc'

    elif(emotion == "Neutral"):
        urlhere = 'http://www.imdb.com/search/title?genres=thriller&title_type=feature&sort=moviemeter, asc'
  
    elif(emotion == "Fear"):
        urlhere = 'http://www.imdb.com/search/title?genres=sport&title_type=feature&sort=moviemeter, asc'

    elif(emotion == "Happy"):
        urlhere = 'http://www.imdb.com/search/title?genres=thriller&title_type=feature&sort=moviemeter, asc'

    elif(emotion == "Surprise"):
        urlhere = 'http://www.imdb.com/search/title?genres=film_noir&title_type=feature&sort=moviemeter, asc'

    response = HTTP.get(urlhere)
    data = response.text

    soup = SOUP(data, "lxml")

    title = soup.find_all("a", attrs = {"href" : re.compile(r'\/title\/tt+\d*\/')})
    return title
  
# Driver Function
def bot(emotion):
    emotion_dict = {0:'Anger', 1:'Disgust', 2:'Fear', 3:'Happy', 4:'Neutral', 5:'Sad', 6:'Surprise'}
    emotion = emotion_dict[emotion]
    a = url(emotion)
    count = 0
    ans = []
  
    if(emotion == "Disgust" or emotion == "Anger"
                           or emotion=="Surprise"):
  
        for i in a:

            tmp = str(i).split('>;')
  
            if(len(tmp) == 3):
                ans.append(tmp[1][:-3])
  
            if(count > 13):
                break
            count += 1
    else:
        for i in a:
            tmp = str(i).split('>')
  
            if(len(tmp) == 3):
                ans.append(tmp[1][:-3])
  
            if(count > 11):
                break
            count+=1
    return ans[random.randint(0, len(ans)-1)]

# if __name__ == '__main__':
#     print(bot(4))