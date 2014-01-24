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

>>> import struct
>>> import inspect
>>> from collections import OrderedDict


>>> class ValidationError(Exception): pass


>>> class Field(object):
...
...     _creation_counter = 0
...
...     def __init__(self):
...         self.creation_order = Field._creation_counter
...         Field._creation_counter += 1
...
...     @property
...     def value(self):
...         return self._value
...
...     @value.setter
...     def value(self, v):
...         self.validate(v)
...         self._value = v
...
...     @property
...     def packed(self):
...         return struct.pack(self.format, self._value)
...
...     def validate(self, v):
...         if not isinstance(v, self.type):
...             raise ValidationError()


>>> class IntField(Field):
...
...     format = 'i'
...     type = int
...     ctype = 'int'


>>> class LongField(Field):
...
...    format = 'l'
...    type = int
...    ctype = 'long'


>>> class DoubleField(Field):
...
...    format = 'd'
...    type = float
...    ctype = 'double'


>>> class BoolField(Field):
...
...     format = '?'
...     type = bool
...     ctype = '_Bool'


>>> class CharField(Field):
...
...     format = 'c'
...     ctype = 'char'
...
...     def validate(self, v):
...         if not isinstance(v, str) or len(v) != 1:
...             raise ValidationError()

>>> class StringField(Field):
...
...     type = str
...     ctype = 'char[]'
...
...     @property
...     def format(self):
...         return '{}s'.format(len(self.value))


>>> class StructMetaclass(type):
...
...     def __new__(metaclass, classname, bases, class_dict):
...         cls = type.__new__(metaclass, classname, bases, class_dict)
...         cls._fields = OrderedDict(sorted(
...             inspect.getmembers(cls, lambda o: isinstance(o, Field)),
...             key=lambda i: i[1].creation_order
...         ))
...         return cls


>>> class Struct(object):
...
...     __metaclass__ = StructMetaclass
...
...
...     def __init__(self, **kwargs):
...         for k, v in kwargs.iteritems():
...             if k in self._fields:
...                 self._fields[k].value = v
...
...     @property
...     def packed(self):
...         return ''.join((f.packed for f in self._fields.itervalues()))
...
...     @property
...     def schema(self):
...         return [(n, f.ctype) for n, f in self._fields.iteritems()]


>>> class String(Struct):
...
...     data = StringField()
...     length = IntField()


>>> s = String(data='abc', length=3)
>>> s.schema
[('data', 'char[]'), ('length', 'int')]
>>> repr(s.packed)
"'abc\\\\x03\\\\x00\\\\x00\\\\x00'"
>>> s.data.value = 'hello'
>>> s.length.value = 5
>>> repr(s.packed)
"'hello\\\\x05\\\\x00\\\\x00\\\\x00'"

Before considering to use metaclasses read that:

        Metaclasses are deeper magic than 99% of users should ever worry
        about. If you wonder whether you need them, you don't (the people
        who actually need them know with certainty that they need them,
        and don't need an explanation about why).

        Python Guru Tim Peters
"""
