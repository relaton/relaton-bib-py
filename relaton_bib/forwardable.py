class Forwardable(object):
    """https://www.linkedin.com/pulse/forwardable-python-vivek-soundrapandi/"""

    def __init__(self, *args, **kwargs):
        self._delegates = []
        return super().__init__(*args, **kwargs)

    @property
    def delegates(self):
        return self._delegates

    @delegates.setter
    def delegates(self, delegates):
        self._delegates = delegates

    def __getattr__(self, name):
        # EX: delegates = [("q", "enqueue", "append")]
        # iterate through to delegate items
        for attr in self.delegates:
            # check if the current lookedup attribute is in any of the delegates
            if name == attr[1] and hasattr(getattr(self, attr[0]), attr[2]):
                # delegate the call to composed object
                return getattr(getattr(self, attr[0]), attr[2])
        # raise AttributeError to mimick system default
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")