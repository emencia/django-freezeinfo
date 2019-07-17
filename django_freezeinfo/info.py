class FreezeInfo(object):
    def __init__(self):
        self.wrapper = None

    def output(self):
        raise NotImplementError
        #return self.wrapper.output()
