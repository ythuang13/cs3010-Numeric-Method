#Yitian Huang, Feb 07, 2022
import math


def main() -> None:
    """Input assumed in the correct format.
    Either decimal numbers or scientific notation(A x 10^B)."""
    num = input("Enter number: ")
    num = parser(num)
    converter(num)

def parser(num: str) -> float:
    """parse the input string to a float"""
    if 'x' in num:
        coefficient, t = num.split('x')
        base, exp = t.split('^')
        num = float(coefficient) * (float(base) ** int(eval(exp)))
    elif '^' in num:
        base, exp = num.split('^')
        num = float(base) ** int(exp)
    elif '/' in num:
        numerator, denominator = num.split('/')
        num = float(numerator) / float(denominator)
    else:
        num = float(num)
        
    return num

def converter(num: float) -> None:
    """Convert float number in decimal to IEEE-753 32 bits float"""
    # Get the sign
    sign = 1 if num < 0 else 0

    # Get the exponent
    exp = math.floor(math.log(abs(num), 2))

    # Get the binary representation of the number
    binaryNumber = []
    # Get the binary representation of the whole number
    whole = int(abs(num) // 1)
    for i in bin(whole)[2:]:
        binaryNumber.append(i)
    # Get the binary representation of the mantissa by multiplying 2 and take the whole number 23 - exp times
    decimal = abs(num) % 1 * 2

    for _ in range(23 - exp):
        if decimal >= 1:
            binaryNumber.append('1')
            decimal -= 1
        else:
            binaryNumber.append('0')
        decimal *= 2
    mantissa = ''.join(binaryNumber[-23:])

    # calculate one more bit to see if rounding is needed
    if decimal >= 1:
        mantissa = bin(int(mantissa, 2) + 1)[2:]

    # Get the binary representation of the exponent
    exp = bin(exp + 127)[2:]
    # Get the binary representation of the sign
    sign = bin(sign)[2:]
    
    # Print the result
    # print("Sign: " + sign)
    # print(f"Exponent: {exp:0>8}")
    # print(f"Mantissa: {mantissa:0>23}")
    print(f"IEEE-754: {sign} {exp:0>8} {mantissa:0>23}")
    

if __name__ == '__main__':
    main()