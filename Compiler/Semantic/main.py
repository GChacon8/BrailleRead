from Syntax.parser import *
from Semantic.semantic import *

with open("code.txt", "r") as file:
    data = file.read()

    try:
        res = systax_analysis(data)
    except:
        pass

    if not lexical_errors:
        if not syntax_errors:
            print(res)
            program = semantic_analysis(res)
            if not program.getErrors():
                print("\nFile compiled successfully!!!")
            else:
                for error in program.getErrors():
                    print(error)
        else:
            for error in syntax_errors:
                print(error)
    else:
        for error in lexical_errors:
            print(error)