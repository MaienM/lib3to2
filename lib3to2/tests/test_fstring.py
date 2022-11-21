from lib3to2.tests.support import lib3to2FixerTestCase

class Test_fstring(lib3to2FixerTestCase):
    fixer = "fstring"

    def check(self, b, a, data={ 'foo': 42, 'bar': 3.14 }):
        super().check(b, a)
        bval = eval(b, globals(), data)
        aval = eval(a, globals(), data)
        self.assertEquals(bval, aval)

    def test_fstring_regular_string(self):
        b = '''"{foo}"'''
        a = b
        self.check(b, a)

    def test_fstring_simple(self):
        b = '''f"{foo}"'''
        a = """'{0}'.format(foo)"""
        self.check(b, a)

    def test_fstring_expression(self):
        b = '''f"{1 + 1}"'''
        a = """'{0}'.format(1 + 1)"""
        self.check(b, a)

    def test_fstring_conversion(self):
        b = '''f"{foo!r}"'''
        a = """'{0!r}'.format(foo)"""
        self.check(b, a)

    def test_fstring_format_spec(self):
        b = '''f"{foo:20}"'''
        a = """'{0:20}'.format(foo)"""
        self.check(b, a)

    def test_fstring_format_spec_nested(self):
        b = '''f"{bar:0{foo}0}"'''
        a = """'{0:0{1}0}'.format(bar, foo)"""
        self.check(b, a)

    def test_fstring_complex(self):
        b = '''f"{(1 + 1)!r:20}"'''
        a = """'{0!r:20}'.format(1 + 1)"""
        self.check(b, a)

    def test_fstring_debugging(self):
        b = '''f"{foo=} {bar = }"'''
        a = """'foo={0!r} bar = {1!r}'.format(foo, bar)"""
        self.check(b, a)

    def test_fstring_escaped_braces(self):
        b = '''f"{foo}{{bar}}"'''
        a = """'{0}{{bar}}'.format(foo)"""
        self.check(b, a)

    def test_fstring_escape_sequences(self):
        b = '''f"{foo}\\n\\\\n"'''
        a = """'{0}\\n\\\\n'.format(foo)"""
        self.check(b, a)

    def test_fstring_prefixes(self):
        b = '''rf"{foo}\\n"'''
        a = """'{0}\\\\n'.format(foo)"""
        self.check(b, a)

    def test_fstring_concat(self):
        b = '''"{foo}=" f"{foo}" " {bar}=" f"{bar}"'''
        a = """'{{foo}}={0} {{bar}}={1}'.format(foo, bar)"""
        self.check(b, a)

    def test_fstring_concat_multiline(self):
        b = '''("{foo}=" f"{foo}"\n" {bar}="\n\nf"{bar}")'''
        a = """('{{foo}}={0} {{bar}}={1}'.format(foo, bar))"""
        self.check(b, a)
