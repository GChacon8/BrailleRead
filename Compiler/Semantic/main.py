from Syntax.parser import *
from Semantic.semantic import *
from IDE.Translator import *

with open("code.txt", "r") as file:
    data = file.read()

    try:
        res = systax_analysis(data)
    except:
        pass

    if not lexical_errors:
        if not syntax_errors:
            program = semantic_analysis(res)
            if not program.getErrors():
                translator = Translator(program.programOutput)
                translator.Translate()
                if program.getPrints():
                    print("\n")
                    for ele in program.getPrints():
                        print(ele)
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