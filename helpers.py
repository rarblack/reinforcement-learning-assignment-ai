def increase(variable, amount=1):
    variable += amount

def decrease(variable, amount=1):
    variable -= amount

def fib(n):    # write Fibonacci series up to n
    a, b = 0, 1
    while a < n:
        a, b = b, a + b

    return b

def parse_board_string(string):
    moves = {}
    splitted = string.split('\n')
    size  = len(splitted[0])

    for x, row in enumerate(splitted):
        for y, sign in enumerate(row):
            if not sign.__eq__('-'): 
                moves[(x,y)] = sign

    return (size, moves)

