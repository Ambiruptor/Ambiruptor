""" """
import sys
import re
import mwparserfromhell


def load_text(file):
    with open(file, "r") as f:
        data = f.read()
    return data

def remove_thumbs(text):
    return re.sub(".+\|.+", "", text)

def clean(text):
    wikicode = mwparserfromhell.parse(text)
    raw_text = wikicode.strip_code()
    print(remove_thumbs(raw_text))


if __name__ == '__main__':
    wikitext = load_text(sys.argv[1])
    text = clean(wikitext)
