
from sentence_transformers import SentenceTransformer
from sentence_transformers import SentenceTransformer, util
import google_search as gs

# model = SentenceTransformer('distilbert-base-nli-mean-tokens')
model = SentenceTransformer("C:\\Users\\Asus\\Desktop\\smartBotFlask\\Project - Chitti\\sentence-transformers_all-MiniLM-L6-v2")

def similarity(sen1, sen2):
    sentences = [sen1, sen2]
    sentence_embeddings = model.encode(sentences)
    return util.pytorch_cos_sim(sentence_embeddings[0], sentence_embeddings[1])

def classify(sen):
    sentences = [['Tell me about some facts on me about who is who is', 'who is name'], 
                 ['web think about web opinion web thoughts', 'internet opinion think about on', '--'],
                 ['Tell me a story random story story'],
                 ['I like games', 'i hate subject', 'i love subject'],
                 ['recommend me some movies to watch', 'recommend a movie to watch', 'what movies should i watch'],
                 ['what is your name', 'who are you', 'tell me about yourself', 'who created you', 'what are you']]
    
    if len(gs.bot(sen)) != 0:
        return 6
    
    s = []
    for i in range(len(sentences)):
        p = 0
        for j in range(len(sentences[i])):
            if p < similarity(sen, sentences[i][j])[0][0].item():
                 p = similarity(sen, sentences[i][j])[0][0].item()
        s.append(p)
    if max(s) > 0.3:
        return s.index(max(s))
    else:
        return -1
    