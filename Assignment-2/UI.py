While true:
	//1 to generate new image or 2 to exit
Request for input
If input == 1:
	Open prng-service.txt
	Write “run” in prng-service.txt
Sleep for 5 seconds
	Read pseudo random number from prng-service.txt
	Open image-service.txt
	Erase data in image-service.txt
	Write pseudo random number
	Sleep for 5 seconds
	Read and output image-service.txt
	Close image-service.txt
Close prng-service.txt

else if input ==2
return
else
	print (“unknown option”)
