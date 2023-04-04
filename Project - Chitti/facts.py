import wikipedia

def bot(content):
    remove = ['tell', 'me', 'about', 'facts', 'Who', 'is']
    for i in remove:
        content = content.replace(i, '')
    try:
        k = wikipedia.search(content, results = 4)
        for i in k:
            try:
                answer = wikipedia.summary(k[0])
                break
            except:
                answer = 'I do not know'
    except:
        answer = 'I do not know'
    return answer

