from os import listdir
from os.path import isfile, isdir, join
from sys import argv
from typing import List

from compiler.lexer import Token, lexer


def format_nj(code: List[str]) -> List[str]:
    new_code: list[str] = []
    tokens = lexer(code, "format.nj")
    indent = 0
    line = ""
    p = Token("symbol", "")
    for i in tokens:
        if i.type == "symbol":
            if i.content == "{":
                line += " {"
                new_code.append("    " * indent + line)
                indent += 1
                line = ""
            elif i.content == "}":
                if line != "":
                    new_code.append("    " * indent + line)
                indent -= 1
                new_code.append("    " * indent + "}")
                line = ""
            elif i.content == ";":
                line += ";"
                new_code.append("    " * indent + line)
                line = ""
            elif i.content in ")]:,.[":
                line += i.content
            elif i.content in "(":
                if p.content in ("if", "elif", "for", "while") or (p.type == "symbol" and p.content not in "()[]."):
                    line += " " + i.content
                else:
                    line += i.content
            else:
                if p.content in "([":
                    line += i.content
                else:
                    line += " " + i.content
        elif i.type in ("string", "integer", "symbol", "keyword", "float", "char", "identifier"):
            if line == "" or p.content in "([.":
                line += i.content
            else:
                line += " " + i.content
        p = i
    return new_code


def format_vm(code: List[str]) -> List[str]:
    def check_label(i: str) -> bool:
        if (
            i.startswith("label if")
            or i.startswith("label elif")
            or i.startswith("label for")
            or i.startswith("label while")
            or i.startswith("label loop")
        ):
            return True
        return False

    new_code: list[str] = []
    indent = 0
    f = False
    for i in code:
        i = i.strip()
        if f and i.startswith("label") and not (check_label(i)):
            indent -= 1
        f = False
        if i.startswith("debug-label end"):
            indent -= 2
        new_code.append("    " * indent + i)
        if i.startswith("label") and not (check_label(i)) or i.startswith("debug-label start"):
            indent += 1
        elif not i.startswith("debug-label start"):
            f = True
    return new_code


def main(path: str, type_: str = "") -> None:
    new_code = []
    if isfile(path):
        paths = [path]
    elif isdir(path):
        paths = [join(path, i) for i in listdir(path)]
    else:
        print("Invalid path")
        return

    for i in paths:
        if not isfile(i):
            continue
        if not i.endswith(".vm") and not i.endswith(".nj"):
            continue
        if type_ == "":
            if i.endswith(".vm"):
                type_ = "vm"
            elif i.endswith(".nj"):
                type_ = "nj"
        with open(i, "r") as f:
            code = f.readlines()
        if type_ == "vm":
            new_code = format_vm(code)
        elif type_ == "nj":
            new_code = format_nj(code)
        else:
            print("Invalid type")
            continue
        with open(i, "w") as f:
            f.write("\n".join(new_code))


if __name__ == "__main__":
    match len(argv):
        case 0:
            main(*input("file path: ").split(maxsplit=1))
        case 1:
            print("file path is required")
        case 2:
            main(path=argv[1])
        case _:
            main(path=argv[1], type_=argv[2])
