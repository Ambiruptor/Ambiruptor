all: setup data/wikidump.xml

setup:
	mkdir -p data/corpora
	mkdir -p data/feature_extractors
	python setup.py install

clean:
	rm dist build ambiruptor.egg-info -R
	rm data/corpora/*

WIKIDUMP = http://dumps.wikimedia.org/enwiki/20160204/enwiki-20160204-pages-meta-current1.xml-p000000010p000030303.bz2
data/wikidump.xml:
	wget -O $@.bz2 $(WIKIDUMP)
	bzip2 -d $@.bz2
