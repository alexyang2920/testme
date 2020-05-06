from zope import interface

from zope.container.folder import Folder
from zope.container.contained import Contained

from zope.schema.fieldproperty import createFieldProperties

from persistent import Persistent

from testme.dictionary.interfaces import IWord, IWordContainer

from testme.models.base import Base


@interface.implementer(IWordContainer)
class WordContainer(Folder):

    def store_word(self, word):
        self[word.word] = word
        return word


@interface.implementer(IWord)
class Word(Base, Persistent, Contained):

    createFieldProperties(IWord)

    def __init__(self, word):
        Base.__init__(self)
        self.word = word
