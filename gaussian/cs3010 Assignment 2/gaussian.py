# Yitian Huang, 02/23/2022
import sys

def main() -> None:
    '''
    Main function, reads and process args and argv
    '''
    # process args
    argv = sys.argv
    sppFlag = None
    inputFile = None
    if len(argv) == 1:
        print('Usage: gaussian.py <input file>')
        return
    elif len(argv) == 2:
        inputFile = argv[1]
    elif len(argv) == 3:
        sppFlag = argv[1]
        inputFile = argv[2]
        if sppFlag != '--spp':
            print('Usage: gaussian.py --spp <input file>')
            return
    
    if not inputFile.endswith('.lin'):
        print('Error: Input file must be a .lin file')
        return
    
    # read input file
    matrixSize, coeffMatrix, constants  = readInputFile(inputFile)
    
    # calculate result
    result = None
    if sppFlag:
        result = sppGaussian(coeffMatrix, constants)
    else:
        result = naiveGaussian(coeffMatrix, constants)
    
    # fix result from -0.0 to 0.0
    for i in range(len(result)):
        if result[i] == -0.0:
            result[i] = 0.0

    # output result to filename.sol
    with open('{}.sol'.format(inputFile[:-4]), 'w') as f:
        f.write(f'{result[0]}')
        for i in range(1, len(result)):
            f.write(f' {result[i]}')

def naiveGaussian(coeffMatrix: list[list[float]], constants: list[float]) -> list[float]:
    '''
    Apply naive gaussian elimination by running forward elimination and then back substitution
    '''
    solution = [0.0] * len(coeffMatrix)
    # forward elimination
    fwdElimination(coeffMatrix, constants)

    # back substitution
    backSubstitution(coeffMatrix, constants, solution)

    return solution

def fwdElimination(coeffMatrix: list[list[float]], constants: list[float]) -> None:
    '''
    Naive Forward Elimination
    '''
    n = len(coeffMatrix)
    for k in range(n-1):
        for i in range(k+1, n):
            mult = coeffMatrix[i][k] / coeffMatrix[k][k]
            for j in range(k, n):
                coeffMatrix[i][j] -= mult * coeffMatrix[k][j]
            constants[i] -= mult * constants[k]

def backSubstitution(coeffMatrix: list[list[float]], constants: list[float], solution: list[float]) -> None:
    '''
    Naive Back Substitution
    '''
    n = len(coeffMatrix)
    solution[n-1] = constants[n-1] / coeffMatrix[n-1][n-1]
    for i in range(n-2, -1, -1):
        sum = constants[i]
        for j in range(i+1, n):
            sum -= coeffMatrix[i][j] * solution[j]
        solution[i] = sum / coeffMatrix[i][i]

def sppGaussian(coeffMatrix: list[list[float]], constants: list[float]) -> list[float]:
    '''
    Apply scaled partial pivoting gaussian elimination
    '''
    solution = [0.0] * len(coeffMatrix)
    index = [i for i in range(len(coeffMatrix))]
    
    # spp forward elimination
    sppFwdElimination(coeffMatrix, constants, index)

    # spp back substitution
    sppBackSubstitution(coeffMatrix, constants, solution, index)

    return solution

def sppFwdElimination(coeffMatrix: list[list[float]], constants: list[float], index: list[float]) -> None:
    '''
    Scaled Partial Pivoting Forward Elimination
    '''
    n = len(coeffMatrix)

    # find scaling for each row
    scaling = [0.0] * n
    for row in range(n):
        smax = 0
        for col in range(n):
            smax = max(smax, abs(coeffMatrix[row][col]))
        scaling[row] = smax
    
    # scale, pivot and forward elimination for each col k from 0 to n-1
    for k in range(n-1):
        rmax = 0
        maxIndex = k

        # scale and pivot
        for row in range(k, n):
            r = abs(coeffMatrix[index[row]][k] / scaling[index[row]])
            if (r > rmax):
                rmax = r
                maxIndex = row
        if maxIndex != k:
            index[k], index[maxIndex] = index[maxIndex], index[k]

        # forward elimination
        for i in range(k+1, n):
            mult = coeffMatrix[index[i]][k] / coeffMatrix[index[k]][k]
            for j in range(k, n):
                coeffMatrix[index[i]][j] -= mult * coeffMatrix[index[k]][j]
            constants[index[i]] -= mult * constants[index[k]]

def sppBackSubstitution(coeffMatrix: list[list[float]], constants: list[float], solution: list[float], index: list[float]) -> None:
    n = len(coeffMatrix)
    solution[n-1] = constants[index[n-1]] / coeffMatrix[index[n-1]][n-1]
    for i in range(n-2, -1, -1):
        sum = constants[index[i]]
        for j in range(i+1, n):
            sum -= coeffMatrix[index[i]][j] * solution[j]
        solution[i] = sum / coeffMatrix[index[i]][i]

def readInputFile(file: str) -> tuple[int, list[list[float]], list[float]]:
    '''
    Read input file and return matrix size, matrixA and matrixB
    '''
    matrixSize = 0
    matrixA = []
    with open(file, 'r') as f:
        # read matrix size
        matrixSize = int(f.readline())

        # read matrixA
        for i in range(matrixSize):
            line = f.readline()
            row = [float(x) for x in line.split()]
            matrixA.append(row)
        
        # read matrixB
        line = f.readline()
        matrixB = [float(x) for x in line.split()]

    return matrixSize, matrixA, matrixB
    


if __name__ == "__main__":
    main()