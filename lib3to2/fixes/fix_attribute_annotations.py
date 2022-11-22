"""
Fixer to remove attribute annotations
"""

from lib2to3 import fixer_base
from lib2to3.pgen2 import token
from lib2to3.pytree import Leaf


class FixAttributeAnnotations(fixer_base.BaseFix):
    PATTERN_LINE_REMOVE = r"""
        simple_stmt< expr_stmt< name=any annotation=annassign< ':' any > > '\n' >
    """
    PATTERN = fr"""
        simple_stmt< expr_stmt< any annotation=annassign< ':' any assignment=( '=' any ) > > '\n' any* > |
        suite<
            any*
            {PATTERN_LINE_REMOVE}
            to_remove=simple_stmt< STRING '\n' >
            any*
        > |
        suite<
            any*
            to_remove={PATTERN_LINE_REMOVE}
            any*
        >
    """

    def transform(self, node, results):
        if 'assignment' in results:
            results['annotation'].replace(results['assignment'])
            return node
        else:
            new = node.clone()

            # The pattern will only match a single line at a time; first docstrings following a to-be-removed
            # attribute, and then the attributes themselves. Keep re-matching until there is nothing more to remove.
            while (r := self.match(new)):
                r['to_remove'].remove()

            # Check whether this left the suite with any valid lines; if not, add a 'pass' statement.
            if [c.type for c in new.children] == [token.NEWLINE, token.INDENT, token.DEDENT]:
                new.children[2:2] = [
                    Leaf(token.NAME, 'pass'),
                    Leaf(token.NEWLINE, '\n'),
                ]

            # For the first line of the suite the indentation is converted into an INDENT token. All subsequent lines
            # have their indentation stored in the prefix attribute. Ensure that the first line (which is in index 2 as
            # it is preceded by NEWLINE INDENT) has an empty prefix, as a non-empty prefix will result in excessive
            # indentation.
            new.children[2].prefix = ''

            return new
