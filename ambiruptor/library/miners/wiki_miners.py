import sqlite3
import pickle
import xml.sax
import re

from ambiruptor.base.core import Miner


class DataMining(Miner):
    """Abstract class for data mining"""

    def __init__(self):
        """Init"""
        self.wikidump_filename = None
        self.database_filename = None
        pass
    
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
        req = '''select count(*) from sqlite_master where type = "table"'''
        if conn.execute(req).fetchone()[0] > 0 :
            print("The database has already been build.")
            conn.close();
            return
        
        # Otherwise, let's build the database
        print("Let's build the database =)")
        
        # Create the main table
        req = '''CREATE TABLE articles
                 (id         INTEGER,
                  title      TEXT,
                  text       TEXT,
                  namespace  INTEGER)'''
        conn.execute(req)
        
        # Create the links table
        req = '''CREATE TABLE links
                 (id_from INTEGER,
                  id_to   INTEGER)'''
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
                    req = '''INSERT INTO articles VALUES (?,?,?,?)'''
                    param = (int(self.data["id"]), self.data["title"], self.data["text"], self.data["ns"])
                    conn.execute(req, param)
                    
        
        handler = Handler()
        xml.sax.parse(self.wikidump_filename, handler)

        conn.commit()
        conn.close()
        
        """regex = re.compile("\[\[([^\[\]|]*)(?:\|[^\[\]|]*)?\]\]")
        links = regex.findall(self.data["text"])"""

    def get_corpus(self, word):
        """Get the corpus"""
        
        conn = sqlite3.connect(self.database_filename)
        req = '''SELECT COUNT(*) FROM articles'''
        result = conn.execute(req).fetchone()[0]
        conn.close()
        return result
