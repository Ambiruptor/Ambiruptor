WIKIDUMP = http://dumps.wikimedia.org/enwiki/20151201/enwiki-20151201-pages-meta-current1.xml-p000000010p000010000.bz2

all: data/wikidump.xml

data/wikidump.xml:
	mkdir -p data/
	wget -O $@.bz2 $(WIKIDUMP)
	bzip2 -d $@.bz2
	python setup.py install

