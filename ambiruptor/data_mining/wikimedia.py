import urllib
import json

class DataMining :
    """Wiki-mining using the media-wiki API"""
    
    def __init__(self) :
        """ Initialize the wiki-miner. """
        pass
    
    def get_corpus(self, word) :
        """
        Get the corpus
        @return : to be defined...
        """
        url_api = "http://en.wikipedia.org/w/api.php?format=json"
        req = url_api + "&action=parse&prop=links&page=" + word
        with urllib.request.urlopen(req) as response:
            data_json = response.read()
        data = json.loads(data_json.decode("utf8"))
        
        senses = [ x["*"] for x in data["parse"]["links"] ]
        
        progress = 0
        self.backlinks = []
        url = url_api + "&action=query&list=backlinks&bllimit=500&bltitle="
        for sense in senses :
            print("\rGetting backlinks :", int(progress), "%", end="", flush=True)
            req = urllib.parse.quote(url + sense, ":/?&=")
            with urllib.request.urlopen(req) as response:
                data_json = response.read()
            data = json.loads(data_json.decode("utf-8"))
            for x in data["query"]["backlinks"] :
                self.backlinks.append(x["title"])
            progress = progress + 100/len(senses)
        print()
        
        return self.backlinks
        
