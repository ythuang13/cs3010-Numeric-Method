# Yitian Huang, Assignment 3, 03/09/2022
# This program is to find the roots of a polynomial
import sys

HYBRID_BISECTION_ITERATION = 5
IEE754_EPSILON = 2 ** -23
DELTA = 0.00001

def main() -> None:
    # variable declaration
    method = "bisection"
    maxIt = 10000
    p1 = 0
    p2 = 0
    polyFileName = None

    degree = 0
    vector = []

    # process command line arguments
    argc = len(sys.argv)
    if argc == 4:
        if sys.argv[1] == "-newt":
            method = "newton"
            p1 = int(sys.argv[2])
            polyFileName = sys.argv[-1]
        else:
            p1 = int(sys.argv[1])
            p2 = int(sys.argv[2])
            polyFileName = sys.argv[-1]
    elif argc == 5:
        if sys.argv[1] == "-sec":
            method = "secant"
            p1 = int(sys.argv[2])
            p2 = int(sys.argv[3])
            polyFileName = sys.argv[-1]
        else:
            method = "hybrid"
            p1 = int(sys.argv[2])
            p2 = int(sys.argv[3])
            polyFileName = sys.argv[-1]
    elif argc == 6:
        if sys.argv[1] == "-newt":
            method = "newton"
            maxIt = int(sys.argv[3])
            p1 = int(sys.argv[4])
            polyFileName = sys.argv[-1]
        else:
            maxIt = int(sys.argv[2])
            p1 = int(sys.argv[3])
            p2 = int(sys.argv[4])
            polyFileName = sys.argv[-1]
    elif argc == 7:
        if sys.argv[1] == "-sec":
            method = "secant"
            maxIt = int(sys.argv[3])
            p1 = int(sys.argv[4])
            p2 = int(sys.argv[5])
            polyFileName = sys.argv[-1]
        else:
            method = "hybrid"
            maxIt = int(sys.argv[3])
            p1 = int(sys.argv[4])
            p2 = int(sys.argv[5])
            polyFileName = sys.argv[-1]
    else:
        print("Usage: py polyRoot.py [-newt, -sec, -hybrid] [-maxIt n] initP [initP2] polyFileName")
        sys.exit(1)

    # read file
    with open(polyFileName, "r") as f:
        degree = int(f.readline())
        for num in f.readline().split(" "):
            vector.append(float(num))
    print("Degree:", degree, "Polynomial:", vector)

    # process
    root = None
    iterationCounter = 0
    outcome = None
    if method == "bisection":
        root, iterationCounter, outcome = bisection(vector, p1, p2, maxIt)
    elif method == "newton":
        root, iterationCounter, outcome = newton(vector, p1, maxIt)
    elif method == "secant":
        root, iterationCounter, outcome = secant(vector, p1, p2, maxIt)
    elif method == "hybrid":
        root, iterationCounter, outcome = hybrid(vector, p1, p2, maxIt)

    # output
    outputFileName = polyFileName[:-4] + ".sol"
    with open(outputFileName, "w") as f:
        f.write(str(root) + " " + str(iterationCounter) + " " + str("success" if outcome else "fail"))
    print(f"Root: {root}, Iteration: {iterationCounter}, Outcome: {'success' if outcome else 'fail'}")

def bisection(polyVector: list, a: float, b: float, maxIt: int) -> tuple[float, int]:
    """
    This function is to find the root of a polynomial using bisection method
    :param polyVector: the polynomial vector
    :param a: initial point
    :param b: initial point
    :param maxIt: maximum number of iterations
    :return: root and iteration counter
    """
    # variable declaration
    iterationCounter = 0
    root = 0

    fa = fOf(polyVector, a)
    fb = fOf(polyVector, b)

    if fa * fb >= 0:
        print("Inadequate values for a and b.")
        return -1.0, 0, False

    # process
    error = b - a

    while iterationCounter < maxIt:
        iterationCounter += 1

        error = error / 2
        c = a + error
        fc = fOf(polyVector, c)
        root = c

        if fc == 0 or abs(error) < IEE754_EPSILON:
            print(f"Algorithm has converged after {iterationCounter} iterations!")
            root = c
            return root, iterationCounter, True
        
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
    
    print("Max iteration reached without covergence with bisection method...")
    return root, iterationCounter, False

    
    return root, iterationCounter

def newton(polyVector: list, x: float, maxIt: int) -> tuple[float, int]:
    """
    This function is to find the root of a polynomial using Newton's method
    :param polyVector: the polynomial vector
    :param x: initial point
    :param maxIt: maximum number of iterations
    :return: root and iteration counter
    """
    # calculate derivative of f
    polyVectorDerivative = derivativeOf(polyVector)

    # variable declaration
    iterationCounter = 0

    # process
    fx = fOf(polyVector, x)
    while iterationCounter < maxIt:
        iterationCounter += 1

        fd = fOf(polyVectorDerivative, x)

        if abs(fd) < DELTA:
            print("Small slope!")
            return x, iterationCounter, False
        
        d = fx / fd
        x = x - d
        fx = fOf(polyVector, x)

        if abs(d) < IEE754_EPSILON:
            print("Algorithm has converged after", iterationCounter, "iterations!")
            return x, iterationCounter, True
        
    # output
    print("Max iteration reached without covergence with newton method...")
    return x, iterationCounter, False

def secant(polyVector: list, a: float, b: float, maxIt: int) -> tuple[float, int]:
    """
    This function is to find the root of a polynomial using secant method
    :param polyVector: the polynomial vector
    :param a: initial point
    :param b: initial point
    :param maxIt: maximum number of iterations
    :return: root and iteration counter
    """
    # variable declaration
    iterationCounter = 0
    root = 0

    fa = fOf(polyVector, a)
    fb = fOf(polyVector, b)

    if abs(fa) > abs(fb):
        a, b = b, a
        fa, fb = fb, fa
    
    while iterationCounter < maxIt:
        iterationCounter += 1

        if abs(fa) > abs(fb):
            a, b = b, a
            fa, fb = fb, fa

        d = (b - a) / (fb - fa)
        b = a
        fb = fa
        d *= fa
        
        if abs(d) < IEE754_EPSILON:
            print(f"Algorithm has converged after {iterationCounter} iterations!")
            return a, iterationCounter, True
        
        a = a - d
        fa = fOf(polyVector, a)
    
    print("Max iteration reached without covergence with secant method...")
    return root, iterationCounter, False

def hybrid(polyVector: list, a: float, b: float, maxIt: int) -> tuple[float, int]:
    """
    This function is to find the root of a polynomial using hybrid method
    First run bisection methods for a few rounds and then switch to newton method
    :param polyVector: the polynomial vector
    :param a: initial point
    :param b: initial point
    :param maxIt: maximum number of iterations
    :return: root and iteration counter
    """
    # variable declaration
    iterationCounter = 0
    root = 0

    x, iterationCounter, _ = bisection(polyVector, a, b, HYBRID_BISECTION_ITERATION)
    newtIterationCounter = 0
    if (iterationCounter < maxIt):
        print("Switching to newton method")
        root, newtIterationCounter, outcome = newton(polyVector, x, maxIt - iterationCounter)
    iterationCounter += newtIterationCounter
    
    return root, iterationCounter, outcome

def fOf(polyVector: list, x: float) -> float:
    """
    This function is to calculate the value of the polynomial at a given point
    :param polyVector: the polynomial vector
    :param x: the point
    :return: the value of the polynomial at the point
    """
    # variable declaration
    fx = 0
    l = len(polyVector)
    for i in range(len(polyVector)):
        fx += polyVector[i] * x ** (l - i - 1)
    return fx

def derivativeOf(polyVector: list) -> list:
    """
    This function is to calculate the derivative of a polynomial
    :param polyVector: the polynomial vector
    :return: the derivative of the polynomial
    """
    # variable declaration
    polyVectorDerivative = []
    l = len(polyVector)
    for i in range(l - 1):
        polyVectorDerivative.append(polyVector[i] * (l - i - 1))
    return polyVectorDerivative


if __name__ == "__main__":
    main()