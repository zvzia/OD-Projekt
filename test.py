import threading
import time

def threadFunc(text):
    time.sleep(1)
    print(text)
    for i in range(0,30):
        print(i)


txt="txr"
th = threading.Thread(target=threadFunc, args=(txt,))
th.start()

for character in 'abcdefghijklmnoprstuwxyz':
    print(character)