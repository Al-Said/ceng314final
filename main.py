from DoubleExecutionPattern import DoubleExecutionPattern
from FaultInjection import FaultInjection
import time

def code(a, b):
    a = FaultInjection(a, 0.1, 0.5)
    b = FaultInjection(b, 0, 0.02)
    #If execution of following steps are faster than recover time
    #We cannot observe recovered a value
    time.sleep(0.2)
    print("---a value is recovered: ", a.getX())
    print("---b value is: ", b.getX())
    return a.getX()+b.getX()


pattern = DoubleExecutionPattern(code)

for i in range(0, 100):
    try:
        x = pattern.exec(32767, 32767)
    except Exception as e:
        print(e)
        #tolerate fault
    else:
        print("Results matched: ", x)
