from Syntax.parser import *
from Semantic.semantic import *
from Translator import *
from Communication import *
import sys
sys.path.append("..")


def compile_code(code):
    res1 = None
    try:
        res1 = systax_analysis(code)
    except:
        pass

    if not lexical_errors:
        if not syntax_errors:
            program = semantic_analysis(res1)
            if not program.getErrors():
                program.getPrints().append("File compiled successfully!!!")
                return program.getPrints()
            else:
                return program.getErrors()
        else:
            return syntax_errors
    else:
        return lexical_errors


def run_code(code):
    res2 = None
    try:
        res2 = systax_analysis(code)
    except:
        pass

    if not lexical_errors:
        if not syntax_errors:
            program = semantic_analysis(res2)
            if not program.getErrors():
                translator = Translator(program.programOutput)
                open_serial()
                send_serial(translator.Translate())
                close_serial()
                print(translator.output)
                program.getPrints().insert(0, "File compiled successfully!!!")
                return program.getPrints()
            else:
                return program.getErrors()
        else:
            return syntax_errors
    else:
        return lexical_errors
