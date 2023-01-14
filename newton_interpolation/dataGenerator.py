import random
import math

def main():
    n = input("Enter a positive integer n for number of random data points: ")
    n = int(n)
    fileName = "random" + str(n) + "DataPoints.pnt"

    xLst = []
    yLst = []

    counter = 0
    minimum = 1
    maximum = n ** 2
    
    while counter != n:
        x = random.uniform(minimum, maximum)
        y = random.uniform(minimum, maximum)
        if x not in xLst:
            xLst.append(x)
            yLst.append(y)
            counter += 1


    with open(fileName, "w") as f:
        f.write(" ".join([str(i) for i in xLst]) + "\n")
        f.write(" ".join([str(i) for i in yLst]))

    print(f"Data points are saved in {fileName}")

if __name__ == "__main__":
    main()