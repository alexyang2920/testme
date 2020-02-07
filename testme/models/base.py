# https://docs.pylonsproject.org/projects/pyramid/en/1.5-branch/narr/renderers.html#using-a-custom-json-method

class Base(object):

    def __json__(self, request):
        json_exclude = getattr(self, '__json_exclude__', set())
        return {k:v for k, v in self.__dict__.items()
                    if not k.startswith('_') and k not in json_exclude }
