all: setup data/wikidump.xml

setup:
	python setup.py install

clean:
	rm dist build ambiruptor.egg-info -R

realclean: clean
	rm data -R

WIKIDUMP = http://dumps.wikimedia.org/enwiki/20160204/enwiki-20160204-pages-meta-current1.xml-p000000010p000030303.bz2
data/wikidump.xml:
	mkdir -p data/
	wget -O $@.bz2 $(WIKIDUMP)
	bzip2 -d $@.bz2
