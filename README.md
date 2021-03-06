# Ambiruptor

## Environment configs 

### Requirement

The following packages are required

```
nltk==3.1
numpy==1.10.2
PyYAML==3.11
scikit-learn==0.17
scipy==0.16.1
six==1.10.0
wheel==0.26.0
```

To avoid manual installation and to easily set up development environment you may consider following the instructions below:

### Configuration using Anaconda

"Anaconda is an easy-to-install, free package manager, environment manager, Python distribution, and collection of over 150 open source packages with free community support."
* [Docs](http://docs.continuum.io/anaconda/index)
* [Downloads](https://www.continuum.io/downloads)

### Create virtual environment

```
conda create --name ambiruptor python=3
```

### Setup environment

To activate the virtual environment
```
source activate ambiruptor
```

To install required dependencies
```
conda install pip
pip install -r requirement.txt
```

## Installation

In order to install the **Ambiruptor project** you have to clone this repository.
```
git clone git@github.com:Ambiruptor/Ambiruptor.git
```
Then just use the **Makefile** to download / compile the basics needed files.

## Run tests

```
python tests/test.py
```

## Known issues

* When you launch the wiki mining tool on the entire wikipedia file, make sure you have enough space in your ```tmp``` directory.
Indeed, **sqlite3** will use temporary files to build the database. It can be fixed by changing the default ```tmp``` directory.
Example, with a debian-like OS and an external hard-drive: ```export TMPDIR=/media/usb/tmp```

## License

The **Ambiruptor project** is available under the **GNU GLPv3** license. For more informations, look at the **LICENSE** file or consult www.gnu.org/licenses/gpl-3.0.html
