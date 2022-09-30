import time

while True:
    time.sleep(1.0)
    f = open("image-service.txt", "r")
    foo = f.readline()
    print(foo)
    f.close()
    try:
        foo = int(foo)
    except:
        pass
    if type(foo) == int:
        bar = foo % 30
        f = open("image-service.txt", "w")
        f.write("/images/" + str(bar) + ".jpg")
        print("/images/" + str(bar) + ".jpg")
    f.close()
