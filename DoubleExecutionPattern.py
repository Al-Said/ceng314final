import time

class DoubleExecutionPattern:

    def __init__(self, code):
        self.code = code

    def exec(self, *argv):
        a = self.code(*argv)
        time.sleep(1)
        b = self.code(*argv)

        if a == b:
            return a
        else:
            raise Exception("Mismatch results:", a, b)