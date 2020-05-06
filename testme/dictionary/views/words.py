import time
from pyramid import httpexceptions as hexc
from pyramid.view import view_config

from testme.views.base import BaseView

from testme.dictionary.interfaces import IWordContainer, IWord
from testme.dictionary.model import Word


@view_config(renderer='json', 
             context=IWordContainer,
             request_method='GET')
class WordsGetView(BaseView):

    def __call__(self):
        return sorted([x for x in self.context.values()],key=lambda x: x.lastModified, reverse=True)


@view_config(renderer='json', 
             context=IWordContainer,
             request_method='POST',
             name="upsert")
class WordUpsertView(BaseView):

    def __call__(self):
        word = self.get_value('word')
        word = word.lower()
        inst = self.context.get(word)
        if not inst:
            inst = Word(word=word)
            self.context.store_word(inst)
        else:
            inst.lastModified = time.time()
        return inst


@view_config(renderer='json', 
             context=IWord,
             request_method='GET')
class WordGetView(BaseView):

    def __call__(self):
        return self.context


@view_config(renderer='json', 
             context=IWord,
             request_method='DELETE')
class WordDeletionView(BaseView):

    def __call__(self):
        del self.context.__parent__[self.context.__name__]
        return hexc.HTTPNoContent()
