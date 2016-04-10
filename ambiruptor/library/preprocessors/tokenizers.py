import re

tokenizer = re.compile(r"(\W+)", re.UNICODE)

def word_tokenize(s):
    return tokenizer.split(s)
