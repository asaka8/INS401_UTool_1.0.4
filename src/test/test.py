import time

from ctypes import *

mess_try = CDLL('./src/test/test.dll')
teacher = CDLL('./src/test/scoring_sys.dll')

order = input('what want to do:\n')
if order == 'try':
    mess_try.main()
if order == 'score':
    teacher.main()


time.sleep(10)