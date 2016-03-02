# Downloading dependancies
import nltk
nltk.download("stopwords")
nltk.download("punkt")

# Setup of ambiruptor package
from setuptools import setup
setup(name='ambiruptor',
      version='0.1',
      description='Disambiguation tool',
      author='Ambiruptor',
      license='GNU GENERAL PUBLIC LICENSE',
      packages=['ambiruptor',
                'ambiruptor.base',
                'ambiruptor.library',
                'ambiruptor.library.learners',
                'ambiruptor.library.miners',
                'ambiruptor.library.preprocessors',
                ],
      zip_safe=False)
