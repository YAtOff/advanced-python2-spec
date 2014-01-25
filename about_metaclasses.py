"""
Befor dealing with metaclasses, we should know more about `type`.
See `describe_type` first.

A metaclass is any callable that takes paremeters for:
    - the class name
    - the class's bases
    - the class's attribures

`type` can do that too.
`type` is the default metaclass.

1. Metaclasses create classes.

>>> NewType = type('NewType', (object,), {'answer': 42})
>>> n = NewType()
>>> n.answer
42

2. Classes create objects.

>>> n = NewType()
>>> isinstance(n, object)
True

3. Classes are objects.

>>> isinstance(NewType, object)
True

=> Metaclasses are classes' classes.

>>> class MyMetaclass(type): pass
>>> class MyClass(object):
...     __metaclass__ = MyMetaclass
>>> MyClass.__class__.__name__
'MyMetaclass'

Note: Since `type` is a class, a metaclass could be created by subclassing
`type`.

Everything is an object in Python, and they are all either instances of
classes or instances of metaclasses.

Except for `type`.

`type` is actually its own metaclass. This is not something you could
reproduce in pure Python, and is done by cheating a little bit at the
implementation level.
"""

from expecter import expect


# hera are some facts about `type`
class describe_type:

    def it_can_create_new_types_dynamically(self):
        NewType = type('NewType', (object,), {'answer': 42})
        n = NewType()
        expect(n.answer) == 42

    # the signature of the `type` in that case is:
    # type(name of the class,
    #   tuple of the parent class (for inheritance, can be empty),
    #   dictionary containing attributes names and values)

    def it_tells_the_type_an_object_is(self):
        nums = [1, 2, 3]
        expect(type(nums)) == list

    def it_is_the_type_a_class(self):
        expect(type(list)) == type

    def it_is_the_type_of_itself(self):
        expect(type(type)) == type

"""
Before considering to use metaclasses read that:

        Metaclasses are deeper magic than 99% of users should ever worry
        about. If you wonder whether you need them, you don't (the people
        who actually need them know with certainty that they need them,
        and don't need an explanation about why).

        Python Guru Tim Peters
"""
