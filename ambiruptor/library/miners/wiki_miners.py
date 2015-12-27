import sqlite3
import hashlib
import xml.sax
import re
from nltk import word_tokenize

from ambiruptor.base.core import Miner

class Wikipedia :
    """Class to manipulate wikipedia data (english)"""

    def normalize_title(title) :
        if type(title) not in [ bytes, str ] :
            raise TypeError("bytes or str expected")
        if type(title) == bytes :
            title = title.decode("utf8")
        # TODO : Wikipedia naming conventions...
        return title.replace(" ", "_")
    
    def get_links(text) :
        regex = re.compile("\[\[([^\[\]|]*)(?:\|[^\[\]|]*)?\]\]")
        return regex.findall(text)
    
    def format_corpus(data) :
        return data
            

class DataMining(Miner):
    """Data mining with a wikidump file"""

    def __init__(self):
        self.wikidump_filename = None
        self.database_filename = None
    
    def set_wikidump_filename(self, filename) :
        self.wikidump_filename = filename
    
    def set_database_filename(self, filename) :
        self.database_filename = filename
    
    def build(self):
        
        # Checking if filenames have been provided.
        if self.wikidump_filename == None :
            raise Exception("No wikidump filename provided.")
        if self.database_filename == None :
            raise Exception("No database filename provided.")
        
        # SQLite database connection
        conn = sqlite3.connect(self.database_filename)
        
        # Checking if the database has already been build
        req = """SELECT COUNT(*) FROM sqlite_master WHERE type='table'"""
        if conn.execute(req).fetchone()[0] > 0 :
            print("The database has already been build.")
            conn.close();
            return
        
        # Otherwise, let's build the database
        print("Let's build the database =)")
        
        conn.execute("PRAGMA main.synchronous  = OFF")
        conn.execute("PRAGMA main.locking_mode = EXCLUSIVE")
        conn.execute("PRAGMA main.journal_mode = OFF")
        conn.execute("PRAGMA main.auto_vacuum  = NONE")
        conn.execute("PRAGMA main.page_size    = 65536")
        
        # Create the main table
        req = """CREATE TABLE articles
                 (id        TEXT,
                  text      TEXT,
                  namespace INTEGER)"""
        conn.execute(req)
        
        # Create the links table
        req = """CREATE TABLE links
                 (id_from TEXT,
                  id_to   TEXT)"""
        conn.execute(req)
        
        # Handler for xml.sax parser.
        class Handler(xml.sax.handler.ContentHandler):
            def __init__(self):
                self.content = []
                self.data = {}

            def characters(self, content):
                self.content.append(content)

            def startElement(self, name, args):
                if name in ["title", "text", "ns"] :
                    self.content = []
                if name == "page" :
                    self.data = {}

            def endElement(self, name):
                if name in ["title", "text", "ns"] :
                    self.data[name] = "".join(self.content)
                if name == "page":
                    req = """INSERT INTO articles VALUES (?,?,?)"""
                    param = (Wikipedia.normalize_title(self.data["title"]),
                             self.data["text"],
                             self.data["ns"])
                    conn.execute(req, param)
                    
                    act_title = Wikipedia.normalize_title(self.data["title"])
                    links = Wikipedia.get_links(self.data["text"])
                    links = map(Wikipedia.normalize_title, links)
                    params = [(act_title, x) for x in links]
                    
                    req = """INSERT INTO links VALUES (?,?)"""
                    conn.executemany(req, list(set(params)))
        
        
        handler = Handler()
        xml.sax.parse(self.wikidump_filename, handler)
        print("Indexes...")
        
        req = """CREATE INDEX index_articles ON articles(id)"""
        conn.execute(req)
        
        req = """CREATE INDEX index_links_from ON links(id_from)"""
        conn.execute(req)
        
        req = """CREATE INDEX index_links_to ON links(id_to)"""
        conn.execute(req)
        
        conn.commit()
        conn.close()
        

    def get_corpus(self, word):
        conn = sqlite3.connect(self.database_filename)
        
        req = """SELECT id_to FROM links WHERE id_from='%s'"""
        param = str(word)
        senses_ids = [ x[0] for x in conn.execute(req % param).fetchall()]
        
        req = """SELECT id_from FROM links WHERE id_to IN %s"""
        param = "{}".format(tuple(senses_ids))
        corpus_ids = [ x[0] for x in conn.execute(req % param).fetchall()]
        
        req = """SELECT text FROM articles WHERE id IN %s"""
        param = "{}".format(tuple(corpus_ids))
        corpus = [ x[0] for x in conn.execute(req % param).fetchall()]
        
        conn.close()
        return Wikipedia.format_corpus(corpus)
