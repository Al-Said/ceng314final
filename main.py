import numpy as np
import time
import math

#x = integer value
#x converted binary
class FaultInjection():
    x = 0
    xBinary = 0
    newBinary = ""
    faultTimeOut = 0
    risk = 0.01

    def setNewValue(self):
        np.random.seed(int(time.time()))
        newBinary = ""

        for x in self.xBinary:
            randVal = np.random.randint(math.ceil(1 / self.risk))
            if randVal == 0:
                if x == "1":
                    newBinary = newBinary + "0"
                else:
                    newBinary = newBinary + "1"
            else:
                newBinary = newBinary + x
        self.newBinary = newBinary

    def recover(self):
        time.sleep(self.faultTimeOut)
        self.newBinary = self.xBinary

    def getX(self):
        return int(self.newBinary, 2)

    # x = fallible int var
    # timeout = if transient error timeout refer correction time in seconds
    # risk = the risk of bit flip
    def __init__(self, x, timeout, risk):
        self.x = x
        self.faultTimeOut = timeout
        self.risk = risk
        self.xBinary = format(x, "b")
        self.setNewValue()
        if timeout != 0:
            self.recover()


class DoubleExecutionPatttern:

    def __init__(self, code):
        self.code = code

    def exec(self, *argv):
        a = self.code(*argv)
        time.sleep(0.1)
        b = self.code(*argv)

        if a == b:
            return a
        else:
            raise Exception("Mismatch results:", a, b)

def code(a, b):
    a = FaultInjection(a, 0, 0.01)
    b = FaultInjection(b, 0, 0.01)
    return a.getX()+b.getX()

pattern = DoubleExecutionPatttern(code)

for i in range(0, 100):
    try:
        x = pattern.exec(32767, 32767)
    except Exception as e:
        print(e)
        #tolerate fault
    else:
        print(x)
