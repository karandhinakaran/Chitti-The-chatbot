from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration

path = "C:\\Users\\Asus\\Desktop\\smartBotFlask\\Project - Chitti\\blenderbot-400M-distill"
model = BlenderbotForConditionalGeneration.from_pretrained(path)
tokenizer = BlenderbotTokenizer.from_pretrained(path)

def bot(content):
    message = content
    inputs = tokenizer([message], return_tensors='pt')
    reply_ids = model.generate(**inputs) # type: ignore
    return f"{tokenizer.batch_decode(reply_ids, skip_special_tokens=True)[0]}"

