import time

while True:
    time.sleep(1.0)
    f = open("image-service.txt", "r")
    foo = f.readline()
    try:
        foo = int(foo)
    except:
        pass
    if type(foo) == int:
        bar = foo % 30
        f = open("image-service.txt", "w")
        f.write("/Users/ianmcmillan/PycharmProjects/CS361/cs361/" + str(bar) + ".jpg")
    f.close()
