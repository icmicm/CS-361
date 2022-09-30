import random
import time

while True:
	time.sleep(1.0)
	f = open("prng-service.txt", "r")
	foo = f.readline()
	print(foo)
	f.close()
	if foo == "run":
		value = random.randint(1, 100)
		print(value)
		f = open("prng-service.txt", "w")
		f.write(str(value))
	f.close()
