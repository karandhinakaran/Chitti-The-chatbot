import spacy

nlp = spacy.load('en_core_web_sm')

def get_subject_phrase(doc):
    for token in doc:
        if ("subj" in token.dep_):
            subtree = list(token.subtree)
            start = subtree[0].i
            end = subtree[-1].i + 1
            return doc[start:end]

def get_object_phrase(doc):
    for token in doc:
        if ("dobj" in token.dep_):
            subtree = list(token.subtree)
            start = subtree[0].i
            end = subtree[-1].i + 1
            return doc[start:end]
        

def bot(content):
    doc = nlp(content)
    object = get_object_phrase(doc)
    return object

def sub(content):
    doc = nlp(content)
    subject = get_subject_phrase(doc)
    return subject
