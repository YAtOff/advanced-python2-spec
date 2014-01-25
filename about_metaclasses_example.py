"""
Here is an example that demonstrates how metaclasses and descriptors
could make code more readable and flexible.
Using metaclasses and descriptors we can define a `Struct` class, that
represents a structure in the C programming language. We can use it
as a normal object in Python, and when needed we can pack it to a binary
representation, that could be read in a C program.

>>> class Message(Struct):
...
...     data = StringField(10)
...     length = IntField()


>>> m = Message(data='helloworld', length=3)
>>> m.schema
[('data', 'char[]'), ('length', 'int')]
>>> repr(m.packed)
"'helloworld\\\\x03\\\\x00\\\\x00\\\\x00'"
>>> m.data = 'hello'
>>> m.length = 5
>>> repr(m.packed)
"'hello\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x05\\\\x00\\\\x00\\\\x00'"
>>> m2 = Message(data="foobar", length=6)
>>> repr(m2.packed)
"'foobar\\\\x00\\\\x00\\\\x00\\\\x00\\\\x06\\\\x00\\\\x00\\\\x00'"

"""

import struct
import inspect


class ValidationError(Exception): pass


class Field(object):

    _creation_counter = 0

    def __init__(self):
        self.creation_order = Field._creation_counter
        Field._creation_counter += 1

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        return obj.__dict__[self.name]

    def __set__(self, obj, value):
        self.validate(value)
        obj.__dict__[self.name] = value

    def pack(self, value):
        return struct.pack(self.format, value)

    def validate(self, value):
        if not isinstance(value, self.type):
            raise ValidationError()


class IntField(Field):

    format = 'i'
    type = int
    ctype = 'int'


class LongField(Field):

   format = 'l'
   type = int
   ctype = 'long'


class DoubleField(Field):

   format = 'd'
   type = float
   ctype = 'double'


class BoolField(Field):

    format = '?'
    type = bool
    ctype = '_Bool'


class CharField(Field):

    type = str
    format = 'c'
    ctype = 'char'

    def validate(self, value):
        super(CharField, self).validate(value)
        if len(value) != 1:
            raise ValidationError()


class StringField(Field):

    type = str
    ctype = 'char[]'

    def __init__(self, max_length):
        super(StringField, self).__init__()
        self._max_length = max_length

    def validate(self, value):
        super(StringField, self).validate(value)
        if self._max_length < len(value):
            raise ValidationError()

    @property
    def format(self):
        return '{}s'.format(self._max_length)


class StructMetaclass(type):

    def __new__(metaclass, classname, bases, class_dict):
        # __new__ is the method called before __init__
        # it's the method that creates the object and returns it
        # while __init__ just initializes the object passed as parameter
        # you rarely use __new__, except when you want to control how the
        # object is created.
        # here the created object is the class, and we want to customize it
        # so we override __new__
        # you can do some stuff in __init__ too if you wish

        cls = type.__new__(metaclass, classname, bases, class_dict)
        fields = sorted(
            inspect.getmembers(cls, lambda o: isinstance(o, Field)),
            key=lambda i: i[1].creation_order
        )
        for f in fields:
            f[1].name = f[0]
        cls._fields = [f[0] for f in fields]
        return cls


class Struct(object):

    __metaclass__ = StructMetaclass


    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k ,v)

    @property
    def packed(self):
        return ''.join(
            (getattr(type(self), f).pack(getattr(self, f)) for f in self._fields))

    @property
    def schema(self):
        return [(f, getattr(type(self), f).ctype) for f in self._fields]
