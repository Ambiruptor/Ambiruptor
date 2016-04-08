import re

tokenizer = re.compile(r"\W+", re.UNICODE)

def word_tokenize(s):
    tokens = tokenizer.split(s)
    return [t for t in tokens if t is not ""]
