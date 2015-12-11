import sys
import os.path
import pickle

class DataMining :
    """Abstract class for data mining"""
    
    def __init__(self) :
        """Init the learning model"""
        self.wikipedia_file = ""
        self.wikipedia_fpos = {}
        self.backlinks_file = ""
        self.backlinks_fpos = {}
        pass
    
    def build_wikipedia_file(self) :
        print("Use the Makefile !")
    
    def load_wikipedia_file(self, filename) :
        if not os.path.isfile(filename) :
            raise Exception("Wikidump not found")
        self.wikipedia_file = filename
    
    def build_wikipedia_fpos(self) :
        if not os.path.isfile(self.wikipedia_file) :
            raise Exception("wikipedia_file hasn't been build.")
        
        f = open(self.wikipedia_file, "rb")
        f.seek(0, os.SEEK_END)
        size = f.tell()
        f.seek(0, os.SEEK_SET)
        
        mode_none = 0        
        mode_title = 1
        mode_text = 2
        
        current_mode = mode_none
        last_checkpoint = 0
        current_article = (0, 0)
        
        tag_title_str = b'<title>'
        tag_text_str = b'<text xml:space="preserve">'
        tag_title_pos = 0
        tag_text_pos = 0
        tag_title_size = len(tag_title_str)
        tag_text_size = len(tag_text_str)
        
        buff_str = ""
        buff_size = 0
        buff_pos = 0
        
        result = []
        
        for i in range(size) :
            
            if 100 * i % size < 100 :
                print("\rProcessing wikipedia dump :", 100 * i // size, "%", end="", flush=True)
            
            buff_pos = buff_pos + 1
            if buff_pos >= buff_size :
                buff_pos = 0
                buff_str = f.read(1<<20)
                buff_size = len(buff_str)
            c = buff_str[buff_pos]
            
            if c == ord('<') :
                if current_mode == mode_title :
                    current_article = (last_checkpoint, i - last_checkpoint)
                if current_mode == mode_text :
                    result.append((current_article, (last_checkpoint, i - last_checkpoint)))
                current_mode = mode_none
            
            if c == tag_title_str[tag_title_pos] :
                tag_title_pos = tag_title_pos + 1
                if tag_title_pos == tag_title_size :
                    current_mode = mode_title
                    last_checkpoint = i+1
                    tag_title_pos = 0
            else :
                tag_title_pos = 0
            
            if c == tag_text_str[tag_text_pos] :
                tag_text_pos = tag_text_pos + 1
                if tag_text_pos == tag_text_size :
                    current_mode = mode_text
                    last_checkpoint = i+1
                    tag_text_pos = 0
            else :
                tag_text_pos = 0
        
        print()
        self.wikipedia_fpos = {}
        print(len(result))
        for (a,b),y in result :
            f.seek(a, os.SEEK_SET)
            self.wikipedia_fpos[f.read(b)] = y
            
    
    def load_wikipedia_fpos(self, filename) :
        f = open(filename, "rb")
        self.wikipedia_fpos = pickle.load(f)
        f.close()
    
    def export_wikipedia_fpos(self, filename) :
        f = open(filename, "wb")
        pickle.dump(self.wikipedia_fpos, f)
        f.close()
    
    def build(self, word) :
        """
        Build a corpus for the ambiguous word
        @param(word) : string
        """
        # Downloading wikipedia
        filename = "enwiki-20151201-pages-meta-current.xml"
        print(os.path.relpath(os.path.dirname(__file__)))
        #if !os.path.isfile(filename)
    
    def get_corpus(self) :
        """
        Get the corpus
        @return : to be defined...
        """
        pass
