"""
1. Metaclasses create classes.
2. Classes create objects.
3. Classes are objects.
=> Metaclasses are classes' classes.

Everything is an object in Python, and they are all either instances of
classes or instances of metaclasses.

Except for `type`.

`type` is actually its own metaclass. This is not something you could
reproduce in pure Python, and is done by cheating a little bit at the
implementation level.

A metaclass is any callable that takes paremeters for:
    - the class name
    - the class's bases
    - the class's attribures

`type` can do that too.
`type` is the default metaclass.

Since `type` is a class, a metaclass could be created by subclassing type
(see about_metaclasses_example.py).

Before considering to use metaclasses read that:

        Metaclasses are deeper magic than 99% of users should ever worry
        about. If you wonder whether you need them, you don't (the people
        who actually need them know with certainty that they need them,
        and don't need an explanation about why).

        Python Guru Tim Peters
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
