from typing import Literal, Optional, Sequence, Union
import os.path


class Identifier:
    def __init__(self, location: tuple[int, int], content: str) -> None:
        self.location = location
        self.content = content

    def __str__(self) -> str:
        return self.content


class Integer:
    def __init__(self, location: tuple[int, int], content: str) -> None:
        self.location = location
        self.content = int(content)

    def __str__(self) -> str:
        return str(self.content)


class Float:
    def __init__(self, location: tuple[int, int], content: str) -> None:
        self.location = location
        self.a, self.b = content.split(".")

    def __str__(self) -> str:
        return f"{self.a}.{self.b}"


class String:
    def __init__(self, location: tuple[int, int], content: str) -> None:
        self.location = location
        self.content = content

    def __str__(self) -> str:
        return f'"{self.content}"'


class Char:
    def __init__(self, location: tuple[int, int], content: str) -> None:
        self.location = location
        self.content = content[0]

    def __str__(self) -> str:
        return f"'{self.content}'"


class Op:
    def __init__(
        self, location: tuple[int, int], content: Literal["+", "-", "*", "/", "|", "&", "<<", ">>", "==", "!=", ">=", "<=", ">", "<"]
    ) -> None:
        self.location = location
        self.content = content

    def __str__(self) -> str:
        return self.content


class Type:
    def __init__(self, location: tuple[int, int], outside: Identifier, inside: Optional["Type"] = None) -> None:
        self.location = location
        self.outside = outside
        self.inside = inside

    def __str__(self) -> str:
        if self.inside is None:
            return str(self.outside)
        else:
            return f"{self.outside}[{self.inside}]"


class Term:
    def __init__(
        self,
        location: tuple[int, int],
        content: Union[Integer, Float, Char, String, "Call", "GetVariable", "Expression", "Term", Literal["false", "true", "self"]],
        neg: Optional[Literal["-", "!"]] = None,
    ) -> None:
        self.location = location
        self.content = content
        self.neg = neg

    def __str__(self) -> str:
        if self.neg is None:
            return str(self.content)
        else:
            return f"{self.neg}({self.content})"


class Expression:
    def __init__(self, location: tuple[int, int], content: Sequence[Term | Op]) -> None:
        """content: Stores Op and Term sequences converted to reverse Polish notation"""
        self.location = location
        self.content = content

    def __str__(self) -> str:
        return " ".join(str(i) for i in self.content)


class GetVariable:
    def __init__(
        self,
        location: tuple[int, int],
        var: "GetVariable | Identifier",
        index: Optional[Expression] = None,
        attr: Optional[Identifier] = None,
    ) -> None:
        self.location = location
        self.var = var
        self.index = None
        self.attr = None
        if isinstance(var, GetVariable):
            if index is not None:
                self.index = index
            elif attr is not None:
                self.attr = attr

    def __str__(self) -> str:
        if self.attr is None and self.index is None:
            return str(self.var)
        elif self.attr is None:
            return f"{self.var}.{self.attr}"
        else:
            return f"{self.var}[{self.index}]"


class Call:
    def __init__(self, location: tuple[int, int], var: GetVariable, expression_list: list[Expression] = []) -> None:
        self.location = location
        self.var = var
        self.expression_list = expression_list

    def __str__(self) -> str:
        return f"{self.var}({(str(i) for i in self.expression_list)})"


class Variable:
    def __init__(
        self, location: tuple[int, int], name: Identifier, kind: Literal["global", "argument", "attriable", "local"], type: Type
    ) -> None:
        self.location = location
        self.name = name
        self.kind: Literal["global", "argument", "attriable", "local"] = kind
        self.type = type

    def __str__(self) -> str:
        return f"{self.kind} {self.name}: {self.type}"


class Var_S:
    def __init__(self, location: tuple[int, int], var_list: list[Variable], expression_list: list[Expression] = []) -> None:
        self.location = location
        self.var_list = var_list
        self.expression_list = expression_list

    def __str__(self) -> str:
        t = ["var_s:"]
        for v, e in zip(self.var_list, self.expression_list):
            t.append(f"{v} = {e}")
        return "\n    ".join(t)


class Do_S:
    def __init__(self, location: tuple[int, int], call: Call) -> None:
        self.location = location
        self.call = call

    def __str__(self) -> str:
        return str(self.call)


class Let_S:
    def __init__(self, location: tuple[int, int], var: GetVariable, expression: Expression) -> None:
        self.location = location
        self.var = var
        self.expression = expression

    def __str__(self) -> str:
        return f"let_s:\n    {self.var} = {self.expression}"


class Return_S:
    def __init__(self, location: tuple[int, int], expression: Optional[Expression] = None) -> None:
        self.location = location
        self.expression = expression

    def __str__(self) -> str:
        return f"return {self.expression}"


class Break_S:
    def __init__(self, location: tuple[int, int], n: Integer) -> None:
        self.location = location
        self.n = n

    def __str__(self) -> str:
        return f"break {self.n}"


class For_S:
    def __init__(
        self,
        location: tuple[int, int],
        for_count_integer: Identifier,
        for_range: tuple[Expression, Expression, Expression],
        statement_list: list["Statement"],
        else_: bool = False,
        else_statement_list: list["Statement"] = [],
    ) -> None:
        self.location = location
        self.for_count_integer = for_count_integer
        self.for_range = for_range
        self.statement_list = statement_list
        self.else_ = else_
        self.else_statement_list = else_statement_list

    def __str__(self) -> str:
        t = [f"for({self.for_count_integer}, {self.for_range[0]}; {self.for_range[1]}; {self.for_range[2]})"]
        for s in self.statement_list:
            t.append(f"    {s}")
        if self.else_:
            t.append("for-else")
            for s in self.else_statement_list:
                t.append(f"    {s}")
        return "\n".join(t)


class If_S:
    def __init__(
        self,
        location: tuple[int, int],
        if_conditional: Expression,
        if_statement_list: list["Statement"],
        elif_n: int = 0,
        elif_statement_list: list[list["Statement"]] = [],
        elif_conditional_list: list[Expression] = [],
        else_: bool = False,
        else_statement_list: list["Statement"] = [],
    ) -> None:
        self.location = location
        self.if_conditional = if_conditional
        self.if_statement_list = if_statement_list
        self.elif_n = elif_n
        self.elif_statement_list = elif_statement_list
        self.elif_conditional_list = elif_conditional_list
        self.else_ = else_
        self.else_statement_list = else_statement_list

    def __str__(self) -> str:
        t = [f"if({self.if_conditional})"]
        for s in self.if_statement_list:
            t.append(f"    {s}")
        for i in range(self.elif_n):
            t.append(f"elif({self.elif_conditional_list[i]})")
            for s in self.elif_statement_list[i]:
                t.append(f"    {s}")
        if self.else_:
            t.append("else")
            for s in self.else_statement_list:
                t.append(f"    {s}")
        return "\n".join(t)


class While_S:
    def __init__(
        self,
        location: tuple[int, int],
        conditional: Expression,
        statement_list: list["Statement"],
        else_: bool = False,
        else_statement_list: list["Statement"] = [],
    ) -> None:
        self.location = location
        self.conditional = conditional
        self.statement_list = statement_list
        self.else_ = else_
        self.else_statement_list = else_statement_list

    def __str__(self) -> str:
        t = [f"while({self.conditional})"]
        for s in self.statement_list:
            t.append(f"    {s}")
        if self.else_:
            t.append("while-else")
            for s in self.else_statement_list:
                t.append(f"    {s}")
        return "\n".join(t)


Statement = Var_S | Do_S | Let_S | Return_S | Break_S | For_S | If_S | While_S


class Subroutine:
    def __init__(
        self,
        location: tuple[int, int],
        name: Identifier,
        kind: Literal["constructor", "method", "function"],
        return_type: Type,
        statement_list: list[Statement],
        argument_list: list[Variable] = [],
    ) -> None:
        self.location = location
        self.name = name
        self.kind = kind
        self.return_type = return_type
        self.statement_list = statement_list
        self.argument_list = argument_list

    def __str__(self) -> str:
        t = [f"{self.kind} {self.name}({(str(i) for i in self.argument_list)}) -> {self.return_type}"]
        for s in self.statement_list:
            t.append(f"    {s}")
        return "\t".join(t)


class Class:
    def __init__(
        self, location: tuple[int, int], name: Identifier, attr_list: list[tuple[str, Type]], subroutine_list: list[Subroutine]
    ) -> None:
        self.location = location
        self.name = name
        self.attr_list = attr_list
        self.subroutine_list = subroutine_list

    def __str__(self) -> str:
        t = [f"class({self.name})"]
        t.append("attr:")
        for a in self.attr_list:
            t.append(f"    {a[0]}: {a[1]}")
        t.append("subroutine:")
        for s in self.subroutine_list:
            t.append(f"    {s}")
        return "\n".join(t)


class Root:
    def __init__(self, location: tuple[int, int], file: str, class_list: list[Class]) -> None:
        self.location = location
        self.name = os.path.split(os.path.abspath(file))[1].split(".")[0]
        self.file = file
        self.class_list = class_list

    def __str__(self) -> str:
        t = [f"file: {self.file}"]
        for c in self.class_list:
            t.append(f"    {c}")
        return "\n".join(t)


type_class = Type((-1, -1), Identifier((-1, -1), "class"))
type_subroutine = {
    "constructor": Type((-1, -1), Identifier((-1, -1), "constructor")),
    "function": Type((-1, -1), Identifier((-1, -1), "function")),
    "method": Type((-1, -1), Identifier((-1, -1), "method")),
}
type_int = Type((-1, -1), Identifier((-1, -1), "int"))
type_argument = Type((-1, -1), Identifier((-1, -1), "argument"))
