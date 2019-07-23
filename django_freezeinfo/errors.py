class BuildoutError(Exception):     
    def __init__(self):
        self.value = "The buildout wrapper needs an 'eggs' path."

    def __str__(self):
        return self.value
