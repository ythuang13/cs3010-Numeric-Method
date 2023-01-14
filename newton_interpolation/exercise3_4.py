# Yitian Huang, 04/15/2022
# polynomial interpolation using Newton's method
import random
import time

def main() -> None:
    option = input("Enter (1) for exercise 3 or (2) for exercise 4: ")
    fileInput = input("Enter a file name: ")
    if option == '1':
        exercise3(fileInput)
    elif option == '2':
        exercise4(fileInput)
    else:
        print("Invalid input!")
    print("Goodbye!")

def exercise3(fileInput: str) -> None:
    # input
    with open(fileInput, "r") as f:
        x = [float(i) for i in f.readline().split()]
        y = [float(i) for i in f.readline().split()]

    # interpolation
    n = len(x)
    c = [0 for _ in range(n)]
    coef(x, y, c)

    while True:
        userInput = input("Enter a value to evaluate for the interpolated polynomial: ")
        if userInput == 'q':
            break
        result = evalNewton(x, c, float(userInput))
        print(f"P({userInput}) = {result}")

def exercise4(fileInput: str) -> None:
    # input
    with open(fileInput, "r") as f:
        x = [float(i) for i in f.readline().split()]
        y = [float(i) for i in f.readline().split()]

    # interpolation
    n = len(x)
    c = [0 for _ in range(n)]

    while True:
        userInput = input("Enter a value to evaluate for the interpolated polynomial: ")
        if userInput == 'q':
            break
        z = float(userInput)
        start = time.perf_counter_ns()
        coef(x, y, c)
        end = time.perf_counter_ns()
        print(f"Interpolation and evaluation run time for {n} data points: {(end - start) /1000000} ms")
        start = time.perf_counter_ns()
        result = evalNewton(x, c, z)
        end = time.perf_counter_ns()
        print(f"P({z}) = {result}")
        print(f"Evaluation run time for {n} data points: {(end - start) /1000000} ms\n")


def coef(xs: list[float], ys: list[float], cs: list[float]) -> None:
    n = len(xs)
    for i in range(n):
        cs[i] = ys[i]
    
    for j in range(1, n):
        for i in range(n-1, j-1, -1):
            cs[i] = (cs[i] - cs[i-1])/(xs[i] - xs[i-j])

def evalNewton(xs: list[float], cs: list[float], z: float) -> float:
    n = len(xs)
    result = cs[n-1]
    for i in range(n-2, -1, -1):
        result = result * (z - xs[i]) + cs[i]
    return result
    
if __name__ == "__main__":
    main()