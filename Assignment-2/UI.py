import time
from matplotlib import pyplot as plt
from matplotlib import image as mpimg


while True:
    choice = input('Type 1 to generate a new image or 2 to exit.\n')
    if choice == "1":
        f = open("prng-service.txt", "w")
        f.write("run")
        f.close()
        time.sleep(5.0)
        f = open("prng-service.txt", "r")
        foo = f.readline()
        f.close()
        g = open("image-service.txt", "w")
        g.write(foo)
        g.close()
        time.sleep(5.0)
        g = open("image-service.txt", "r")
        bar = g.readline()
        f.close()
        g.close()
        plt.title("Random Pokemon")
        plt.xlabel("X pixel scaling")
        plt.ylabel("Y pixels scaling")
        image = mpimg.imread("."+bar)
        plt.imshow(image)
        plt.show()
    # output
    elif choice == "2":
        quit()
    else:
        print("unknown option")
