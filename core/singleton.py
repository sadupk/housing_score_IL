"""Base Singleton Class for inheritance

Lifted from https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
"""

class Singleton(object):
    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    def _initialized(self):
        """
        Helps us know if we have already initialized our Singleton
        to prevent us from clobbering values during __init__

        1st check during __init__ should return False, all subsequent
        should return True
        """
        retval = False
        if hasattr(self, '_singleton'):
            retval = True

        self._singleton = True

        return retval
