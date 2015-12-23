import sqlite3
import hashlib
import xml.sax
import re

from ambiruptor.base.core import Miner

class Wikipedia :

    def id_from_title(title) :
        if type(title) not in [ bytes, str ] :
            raise TypeError("bytes or str expected")
        if type(title) == str :
            title = title.encode("utf8")
        # TODO : Wikipedia namin conventions...
        return int(hashlib.sha1(title).hexdigest(), 16) % (2 ** 31 - 1)
    
    def get_links(text) :
        regex = re.compile("\[\[([^\[\]|]*)(?:\|[^\[\]|]*)?\]\]")
        return regex.findall(text)

class DataMining(Miner):
    """Abstract class for data mining"""

    def __init__(self):
        """Init"""
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
        
        # Create the main table
        req = """CREATE TABLE articles
                 (id         INTEGER PRIMARY KEY,
                  title      TEXT,
                  text       TEXT,
                  namespace  INTEGER)"""
        conn.execute(req)
        
        # Create the links table
        req = """CREATE TABLE links
                 (id_from INTEGER,
                  id_to   INTEGER,
                  PRIMARY KEY(id_from, id_to))"""
        conn.execute(req)
        
        # Create the backlinks table
        req = """CREATE TABLE backlinks
                 (id_from INTEGER,
                  id_to   INTEGER,
                  PRIMARY KEY(id_to, id_from))"""
        conn.execute(req)
        
        # Handler for xml.sax parser.
        class Handler(xml.sax.handler.ContentHandler):
            def __init__(self):
                self.content = []
                self.data = {}

            def characters(self, content):
                self.content.append(content)

            def startElement(self, name, args):
                if name in ["title", "text", "ns", "id"] :
                    self.content = []
                if name == "page" :
                    self.data = {}

            def endElement(self, name):
                if name in ["title", "text", "ns", "id"] :
                    self.data[name] = "".join(self.content)
                if name == "page":
                    req = """INSERT INTO articles VALUES (?,?,?,?)"""
                    param = (Wikipedia.id_from_title(self.data["title"]),
                             self.data["title"],
                             self.data["text"],
                             self.data["ns"])
                    conn.execute(req, param)
                    
                    links = Wikipedia.get_links(self.data["text"])
                    id_act = Wikipedia.id_from_title(self.data["title"])
                    params = [(id_act, Wikipedia.id_from_title(x)) for x in links]
                    
                    req = """INSERT INTO links VALUES (?,?)"""
                    conn.executemany(req, list(set(params)))
                    
                    req = """INSERT INTO backlinks VALUES (?,?)"""
                    conn.executemany(req, list(set(params)))
                    
        
        handler = Handler()
        xml.sax.parse(self.wikidump_filename, handler)

        conn.commit()
        conn.close()
        

    def get_corpus(self, word):
        """Get the corpus"""
        
        conn = sqlite3.connect(self.database_filename)
        
        req = """SELECT id_to FROM links WHERE id_from=%s"""
        param = str(Wikipedia.id_from_title(word))
        senses_ids = [ x[0] for x in conn.execute(req % param).fetchall()]
        
        req = """SELECT id_from FROM backlinks WHERE id_to IN (%s)"""
        param = ",".join([str(x) for x in senses_ids])
        corpus_ids = [ x[0] for x in conn.execute(req % param).fetchall()]
        
        req = """SELECT title FROM articles WHERE id IN (%s)"""
        param = ",".join([str(x) for x in corpus_ids])
        corpus = [ x[0] for x in conn.execute(req % param).fetchall()]
        
        conn.close()
        return corpus
