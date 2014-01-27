from expecter import expect


def when_not_found(f):
    return f

def rule_number(n):
    def wrapper(f):
        return f
    return wrapper

"""
First, what's descriptor?
-------------------------

* A descriptor is any object that implements at least one of methods named
  `__get__()`, `__set__()`, and `__delete__()`.
* A data descriptor implements both `__get__()` and `__set__()`.
  Implementing only `__get__()` makes you a non-data descriptor.


After we know about descriptors, let's define the rules for attribute access
in eitht simple rules.
"""


class BarNonDataDescriptor(object):

    def __get__(self, obj, type=None):
        return "from non-data descriptor"


class BarDataDescriptor(object):

    def __get__(self, obj, type=None):
        return "from data descriptor"

    def __set__(self, obj, value):
        pass


class describe_accessing_attribure_bar_of_object_foo:

    @rule_number(1)
    def it_first_gives_the_result_of__get__method_of_data_descriptor(self):

        class Foo(object):
            bar = BarDataDescriptor()

            def __init__(self):
                self.bar = "from instance __dict__"

        foo = Foo()
        expect(foo.bar) == "from data descriptor"

    # Note: foo.__dict__["bar"] is shadowed; this could be useful


    @when_not_found
    @rule_number(2)
    def it_tries_the_instance__dict__(self):

        class Foo(object):
            bar = BarNonDataDescriptor()

            def __init__(self):
                self.bar = "from instance __dict__"

        foo = Foo()
        expect(foo.bar) == "from instance __dict__"


    @when_not_found
    @rule_number(3)
    def it_tries_the__get__method_of_non_data_descriptor(self):

        class FooBase(object):
            bar = "from base class"

        class Foo(FooBase):
            bar = BarNonDataDescriptor()

        foo = Foo()
        expect(foo.bar) == "from non-data descriptor"


    @when_not_found
    @rule_number(4)
    def it_tries_the_class__dict__(self):

        class FooBase(object):
            bar = "from base class"

        class Foo(FooBase):
            bar = "from class __dict__"

        foo = Foo()
        expect(foo.bar) == "from class __dict__"


    @when_not_found
    @rule_number(5)
    def it_tries_each_type_in_the_mro_until_it_finds_a_match(self):

        class FooBase(object):
            bar = "from base class"

        class Foo(FooBase): pass


        foo = Foo()
        expect(foo.bar) == "from base class"

    @when_not_found
    @rule_number(6)
    def it_calls__getattr__(self):

        class Foo(object):
            def __getattr__(self, name):
                if name == "bar":
                    return "from __getattr__"
                else:
                    raise AttributeError

        foo = Foo()
        expect(foo.bar) == "from __getattr__"


class describe_assigning_to_attribute_bar_of_object_foo:

    @rule_number(1)
    def it_creates_entyr_in_instance__dict__(self):

        class Foo(object): pass

        foo = Foo()
        foo.bar = "must go in instance __dict__"

        expect(foo.__dict__["bar"]) == "must go in instance __dict__"

    @rule_number(2)
    def it_unless_there_is_data_descripor_with__set__method(self):

        class Foo(object):
            bar = BarDataDescriptor()

        foo = Foo()
        foo.bar = "must call data descriptor __set__"

        expect(foo.__dict__).does_not_contain("bar")
        expect(foo.bar) == "from data descriptor"


class describe___slots__:

    """
    By default, instances of both old and new-style classes have a dictionary
    for attribute storage. This wastes space for objects having very few
    instance variables. The space consumption can become acute when creating
    large numbers of instances.
    The default can be overridden by defining __slots__ in a new-style class
    definition. The __slots__ declaration takes a sequence of instance
    variables and reserves just enough space in each instance to hold a value
    for each variable. Space is saved because __dict__ is not created for each
    instance.
    """

    def it_allows_only_attributes_listed_in__slots__to_be_assigned(self):

        class Eggs(object):
            __slots__ = ["spam"]

        eggs = Eggs()
        eggs.spam = True
        with expect.raises(AttributeError):
            eggs.bacon = True

    def it_doesnt_work_when_inheriting_from_class_without__slots__(self):

        class Breakfast(object): pass

        class Eggs(Breakfast):
            __slots__ = ["spam"]

        eggs = Eggs()
        eggs.spam = True
        eggs.bacon = True

    def it_works_for_subclasses_only_if_redefined(self):

        class Breakfast(object):
            __slots__ = ["bread"]

        class Eggs(Breakfast):
            __slots__ = ["spam"]

        eggs = Eggs()
        eggs.spam = True

        class Bacon(Breakfast): pass

        bacon = Bacon()
        bacon.eggs = True
