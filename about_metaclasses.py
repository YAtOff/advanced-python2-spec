"""
A metaclass is any callable that takes paremeters for:
    - the class name
    - the class's bases
    - the class's attribures

`type` is the default metaclass.

Metaclasses create classes.
Classes create objects.
Classes are objects.
=> Metaclasses are classes' classes.

Everything is an object in Python, and they are all either instances of
classes or instances of metaclasses.

Except for `type`.

`type` is actually its own metaclass. This is not something you could
reproduce in pure Python, and is done by cheating a little bit at the
implementation level.


>>> class String(Struct):
...
...     data = StringField(10)
...     length = IntField()


>>> s = String(data='helloworld', length=3)
>>> s.schema
[('data', 'char[]'), ('length', 'int')]
>>> repr(s.packed)
"'helloworld\\\\x03\\\\x00\\\\x00\\\\x00'"
>>> s.data = 'hello'
>>> s.length = 5
>>> repr(s.packed)
"'hello\\\\x00\\\\x00\\\\x00\\\\x00\\\\x00\\\\x05\\\\x00\\\\x00\\\\x00'"
>>> s2 = String(data="foobar", length=6)
>>> repr(s2.packed)
"'foobar\\\\x00\\\\x00\\\\x00\\\\x00\\\\x06\\\\x00\\\\x00\\\\x00'"

Before considering to use metaclasses read that:

        Metaclasses are deeper magic than 99% of users should ever worry
        about. If you wonder whether you need them, you don't (the people
        who actually need them know with certainty that they need them,
        and don't need an explanation about why).

        Python Guru Tim Peters
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
