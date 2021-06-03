import numpy as np
import time
import math

class FaultInjection():
    x = 0
    xConvertedBit = 0
    newBitVal = ""
    faultTimeOut = 0
    risk = 0.01

    def setNewValue(self):
        np.random.seed(int(time.time()))

        newBitVal = ""

        for x in self.xConvertedBit:
            randVal = np.random.randint(math.ceil(1 / self.risk))
            if randVal == 0:
                if x == "1":
                    newBitVal = newBitVal + "0"
                else:
                    newBitVal = newBitVal + "1"
            else:
                newBitVal = newBitVal + x
        self.newBitVal = newBitVal

    def recover(self):
        time.sleep(self.faultTimeOut)
        self.newBitVal = self.xConvertedBit

    def getX(self):
        return int(self.newBitVal, 2)

    # x = fallible int var
    # timeout = if transient error timeout refer correction time in seconds
    # risk = the risk of bit flip
    def __init__(self, x, timeout, risk):
        self.x = x
        self.faultTimeOut = timeout
        self.risk = risk
        self.xConvertedBit = format(x, "b")
        self.setNewValue()
        if timeout != 0:
            self.recover()


class DoubleExecutionPatttern:

    def __init__(self, code):
        self.code = code

    def exec(self, *argv):
        a = self.code(*argv)
        time.sleep(0.01)
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
    else:
        print(x)

# a = FaultInjection(32767, 0, 0.05)
# print(a.xConvertedBit)
# print(a.newBitVal)
# print(a.getX())
