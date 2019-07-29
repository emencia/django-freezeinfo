class BuildoutError(Exception):
    def __init__(self, error=None):
        self.value = "The buildout wrapper needs an 'eggs' path."
        self.error = error

    def __str__(self):
        if self.error:
            return self.error
        else:
            return self.value
