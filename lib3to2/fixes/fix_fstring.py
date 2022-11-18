"""
Fixer for:
f"{(1 + 1)!r}" -> "{0!r}".format(1 + 1)
"""

import re
import ast

from lib2to3 import fixer_base


class FixFstring(fixer_base.BaseFix):
    order = "pre"
    run_order = 4 # Run this before bytes objects are converted to str objects

    PATTERN = "STRING"

    def transform(self, node, results):
        astnode = ast.parse(node.value)
        print(ast.dump(astnode))
        try:
            assert isinstance(astnode, ast.Module)
            assert len(astnode.body) == 1
            assert isinstance(astnode.body[0], ast.Expr)
            assert isinstance(astnode.body[0].value, ast.JoinedStr)
        except AssertionError:
            return node

        joinedstr = astnode.body[0].value
        args = []
        self._process_joinedstr(joinedstr, args)

        astnode.body[0] = ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Constant(ast.unparse(joinedstr)[2:-1]),
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
