class UnfilledMaskError(Exception):
    def __init__(self):
        self.msg = "A required mask was not properly definied!"
        
class EmptyHostImage(Exception):
    def __init__(self):
        self.msg = "The host image was not definied!"

class IFUcubeIOError(Exception):
    def __init__(self, msg):
        self.msg = msg
