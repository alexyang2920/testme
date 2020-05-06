from zope.container.interfaces import IContainer
from zope.location.interfaces import IContained

from zope.schema import Number
from zope.schema import TextLine


class IWord(IContained):

    word = TextLine(title="the word",
                    required=True)

    createdTime = Number(title="The utc timestamp.",
                         required=True)



class IWordContainer(IContainer):
    """
    Keyed by word.
    """
