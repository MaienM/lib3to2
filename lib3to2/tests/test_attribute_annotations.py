from lib3to2.tests.support import lib3to2FixerTestCase

class Test_attribute_annotations(lib3to2FixerTestCase):
    fixer = "attribute_annotations"

    def test_class_annotation_with_value(self):
        b = """
            class Foo():
                bar: int = 42
                baz: int = 21
        """
        a = """
            class Foo():
                bar = 42
                baz = 21
        """
        self.check(b, a)

        b = """
            class Foo():
                bar: int = 42
                class Bar():
                    baz: int = 21
        """
        a = """
            class Foo():
                bar = 42
                class Bar():
                    baz = 21
        """
        self.check(b, a)

    def test_class_annotation_without_value(self):
        b = """
            class Foo():
                foo: int
                bar: int
                other1 = 1
                baz: int
                other2 = 2
        """
        a = """
            class Foo():
                other1 = 1
                other2 = 2
        """
        self.check(b, a)

        b = """
            class Foo():
                foo: int
                bar: int
                other1 = 1
                class Bar():
                    baz: int
                    other2 = 2
        """
        a = """
            class Foo():
                other1 = 1
                class Bar():
                    other2 = 2
        """
        self.check(b, a)

    def test_class_annotation_without_value_becomes_emtpy(self):
        b = """
            class Foo():
                bar: int
                baz: int
        """
        a = """
            class Foo():
                pass
        """
        self.check(b, a)

        b = """
            class Foo():
                class Bar():
                    bar: int
                    baz: int
        """
        a = """
            class Foo():
                class Bar():
                    pass
        """
        self.check(b, a)

    def test_class_annotation_with_docstrings(self):
        b = """
            class Foo():
                ''' Class. '''
                bar: int
                ''' Attribute bar. '''
                other1 = 1
                ''' Attribute other1. '''
                baz: int
                ''' Attribute baz. '''
                other2 = 2
                ''' Attribute other2. '''
        """
        a = """
            class Foo():
                ''' Class. '''
                other1 = 1
                ''' Attribute other1. '''
                other2 = 2
                ''' Attribute other2. '''
        """
        self.check(b, a)

        b = """
            class Foo():
                ''' Class. '''
                bar: int
                ''' Attribute bar. '''
                other1 = 1
                ''' Attribute other1. '''
                class Bar():
                    baz: int
                    ''' Attribute baz. '''
                    other2 = 2
                    ''' Attribute other2. '''
        """
        a = """
            class Foo():
                ''' Class. '''
                other1 = 1
                ''' Attribute other1. '''
                class Bar():
                    other2 = 2
                    ''' Attribute other2. '''
        """
        self.check(b, a)
