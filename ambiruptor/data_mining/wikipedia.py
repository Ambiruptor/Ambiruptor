import pickle
import xml.sax
import os.path
import re

class DataMining :
    """Abstract class for data mining"""
    
    def __init__(self) :
        """Init"""
        self.links = {}
        self.backlinks = {}
        pass
    
    def build(self, filename) :
    
        class Handler(xml.sax.handler.ContentHandler) :
            def __init__(self) :
                self.links = {}
            def setDocumentLocator(self, locator) :
                pass
            def startDocument(self) :
                self.title = ""
                self.text = ""
                self.content = []
            def characters(self, content) :
                self.content.append(content)
            def startElement(self, name, args) :
                if name == "title" :
                    self.content = []
                if name == "text" :
                    self.content = []
            def endElement(self, name) :
                if name == "title" :
                    self.title = "".join(self.content)
                if name == "text" :
                    self.text = "".join(self.content)
                if name == "page" :
                    regex = re.compile("\[\[([^\[\]|]*)(?:\|[^\[\]|]*)?\]\]")
                    self.links[self.title] = regex.findall(self.text)
        
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
        f = open(filename, "wb")
        pickle.dump((self.links, self.backlinks), f)
        f.close()
    
    
    def load(self, filename) :
        f = open(filename, "rb")
        self.links, self.backlinks = pickle.load(f)
        f.close()
    
    def get_corpus(self, title) :
        """
        Get the corpus
        @return : to be defined...
        """
        if not title in self.links :
            raise Exception("Article not found.")
        
        result = []
        for x in self.links[title] :
            if x in self.backlinks :
                result.extend([(x,y) for y in self.backlinks[x]])
        return list(set(result))
        
