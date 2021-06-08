import numpy as np
import time
import math
import threading


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

    def recover(self, event):
        event.wait(self.faultTimeOut)
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
            event = threading.Event()
            thread = threading.Thread(target=self.recover, args=(event, ))
            thread.start()

