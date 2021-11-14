import re
def solve(input):
    # Print the original string
    input = input.splitlines()[0]
    input = input.replace(" ","")
    print("The original string is : " + input)

    # Delimitator
    operators="+-*/"
    
    if input[0] in operators:
        return "[ ! ] Incorrect syntaxis"
    elif input[len(input)-1] in operators:
        return "[ ! ] Incorrect syntaxis"

    for c in range(len(input)):
        if input[c] in operators:
            if c != len(input)-1:
                if input[c+1] in operators:
                    return "[ ! ] Incorrect syntaxis"

    # Regular expresion
    reg="([-+]?[0-9]*\.?[0-9]+[\/\+\-\*])+([-+]?[0-9]*\.?[0-9]+)" # (1+2/3*4-5)
    if re.fullmatch(reg, input):
        solution = eval(input)
        print("*** Correct syntaxis ***")
        return "Answer: "+str(float(solution))
    else:
        return "[ ! ] Incorrect syntaxis"

print(solve("1+1"))