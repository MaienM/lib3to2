"""
Fixer for:
f"{(1 + 1)!r}" -> "{0!r}".format(1 + 1)
"""

import re
import ast

from lib2to3 import fixer_base
from lib2to3.pgen2 import token


class FixFstring(fixer_base.BaseFix):
    order = "pre"
    run_order = 4 # Run this before bytes objects are converted to str objects

    PATTERN = "STRING"

    def transform(self, node, results):
        # String literal concatenation ("a" "b" == "ab") break if an f-string that is part of it is changed into a .format call. To work around this issue we take the entire sequence of string literals and perform the concatenation as part of this fixer if an f-string is involved.
        nodes = [node]
        current = node
        while current.next_sibling and current.next_sibling.type == token.STRING:
            current = current.next_sibling
            nodes.append(current)

        # Parse all nodes and check that at least one of them is an f-string.
        astnodes = [self._ast_parse(n.value) for n in nodes]
        if not any(isinstance(astnode, ast.JoinedStr) for astnode in astnodes):
            return node

        # Remove all succeeding string nodes, as they will all be merged into this node.
        for n in nodes[1:]:
            n.remove()

        # Join all parts into a single JoinedStr.
        joinedstr = ast.JoinedStr([])
        for astnode in astnodes:
            if isinstance(astnode, ast.JoinedStr):
                joinedstr.values += astnode.values
            elif isinstance(astnode, ast.Constant):
                joinedstr.values.append(astnode)
            else:
                raise TypeError(astnode.__class__)

        # Extract arguments, leaving the fstring with only positional arguments.
        args = []
        self._process_joinedstr(joinedstr, args)

        # Convert fstring into regular string constant.
        joinedstr = self._ast_parse(ast.unparse(joinedstr)[1:])

        # Build and return expression that uses the format function (i.e. `joinedstr.format(*args)`).
        astnode = ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=joinedstr,
                    attr='format'
                ),
                args=args,
                keywords=[],
            ),
        )
        new = node.clone()
        new.value = ast.unparse(astnode)
        return new

    @staticmethod
    def _ast_parse(text):
        astnode = ast.parse(text)
        assert isinstance(astnode, ast.Module)
        assert len(astnode.body) == 1
        assert isinstance(astnode.body[0], ast.Expr)
        return astnode.body[0].value

    @staticmethod
    def _process_joinedstr(astnode, args):
        """
        Take the values of all FormattedValue instances in the JoinedStr, replace them with simple positional arguments,
        and store the original values in the args array.

        If any of the FormattedValue instances has a format_spec (which will be a JoinedStr) this will processed the same way.
        """

        for part in astnode.values:
            if isinstance(part, ast.Constant):
                continue

            assert isinstance(part, ast.FormattedValue)

            value = part.value
            part.value = ast.Name(str(len(args)))
            args.append(value)

            if part.format_spec is not None:
                FixFstring._process_joinedstr(part.format_spec, args)
