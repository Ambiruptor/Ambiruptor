import pickle
import xml.sax
import os.path
import re

class DataMining :
    """ Class for wiki mining with a xml dump file. """
    
    def __init__(self) :
        """ Inititialize the wiki-miner """
        self.links = {}
        self.backlinks = {}
    
    def build(self, filename) :
        """ Build the wiki-miner. """
    
        class Handler(xml.sax.handler.ContentHandler) :
            page_regex = re.compile("\[\[([^\[\]|]*)(?:\|[^\[\]|]*)?\]\]")
            def __init__(self) :
                self.links = {}
            def startDocument(self) :
                self.title = ""
                self.text = ""
                self.content = []
            def characters(self, content) :
                self.content.append(content)
            def startElement(self, name, args) :
                if name in ("title", "text"):
                    self.content = []
            def endElement(self, name) :
                if name in ("title", "text") :
                    self.title = "".join(self.content)
                elif name == "page" :
                    self.links[self.title] = self.page_regex.findall(self.text)
        
        handler = Handler()
        xml.sax.parse(filename, handler)
        self.links = handler.links
        
        self.backlinks = {}
        for title in self.links :
            for link in self.links[title] :
                if not link in self.backlinks :
                    self.backlinks[link] = []
                self.backlinks[link].append(title)
                
    
    def export(self, filename) :
        """ Store the wini-miner into a binary file """
        f = open(filename, "wb")
        pickle.dump((self.links, self.backlinks), f)
        f.close()
    
    
    def load(self, filename) :
        """ Load the wini-miner from a binary file """
        f = open(filename, "rb")
        self.links, self.backlinks = pickle.load(f)
        f.close()
    
    
    def get_corpus(self, word) :
        """
        Get the corpus
        @return : to be defined...
        """
        if not word in self.links :
            raise Exception("Article not found.")
        
        result = []
        for x in self.links[word] :
            if x in self.backlinks :
                result.extend([(x,y) for y in self.backlinks[x]])
        return list(set(result))
        
