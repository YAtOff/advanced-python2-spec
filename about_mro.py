"""
In this example we will use the following class herarchy:

                          6
                         ---
Level 3                 | O |                  (more general)
                      /  ---  \
                     /    |    \                      |
                    /     |     \                     |
                   /      |      \                    |
                  ---    ---    ---                   |
Level 2        3 | D | 4| E |  | F | 5                |
                  ---    ---    ---                   |
                   \  \ _ /       |                   |
                    \    / \ _    |                   |
                     \  /      \  |                   |
                      ---      ---                    |
Level 1            1 | B |    | C | 2                 |
                      ---      ---                    |
                        \      /                      |
                         \    /                      \ /
                           ---
Level 0                 0 | A |                (more specialized)
                           ---

source: http://www.python.org/download/releases/2.3/mro/

Whats is the MRO of clase `A`?

>>> A.mro()
[<class 'about_mro.A'>, <class 'about_mro.B'>, <class 'about_mro.C'>,\
 <class 'about_mro.D'>, <class 'about_mro.E'>, <class 'about_mro.F'>,\
 <type 'object'>]

But where that comes from?
MRO is calculated with the C3 algorithm.
To understand the C3 algotithm, we will implement it in Python.
"""

O = object
class F(O): pass
class E(O): pass
class D(O): pass
class C(D,F): pass
class B(D,E): pass
class A(B,C): pass


from collections import deque
from expecter import expect


def C3(cls, herarchy):
    """
        * `cls` is the name or the class, whose MRO we are searching
        * `herarchy` is in the form:
            {
                class_name: [..., base_class_name, ...]
                ...
            }
          but we will refer to it as head -> tail
    """

    def get_all_classes(classes):
        if not classes:
            return []
        superclasses = [sc for c in classes for sc in get_all_classes(herarchy[c])]
        return classes + superclasses

    def is_good(head):
        tails = sum((get_all_classes(herarchy[p]) for p in pending), [])
        return all(head not in tail for tail in tails)

    mro = [cls]
    bases = herarchy[cls]
    pending = deque(bases)
    while pending:
        head = pending.popleft()
        if is_good(head):
            mro.append(head)
            tail =  herarchy[head]
            if tail:
                pending.appendleft(tail[0])
                pending.extend(t for t in tail[1:] if is_good(t))

    return mro


class describe_mro:

    def it_is_calculated_by_c3(self):
        expected_mro = [c.__name__ for c in A.mro()]
        expect(C3('A', {
            'A': ['B', 'C'],
            'B': ['D', 'E'],
            'C': ['D', 'F'],
            'D': ['object',],
            'E': ['object',],
            'F': ['object',],
            'object': []
        })) == expected_mro

    def it_works_with_another_herarchy(self):
        O = object
        class F(O): pass
        class E(O): pass
        class D(O): pass
        class C(D,F): pass
        class B(E,D): pass
        class A(B,C): pass

        expected_mro = [c.__name__ for c in A.mro()]
        expect(C3('A', {
            'A': ['B', 'C'],
            'B': ['E', 'D'],
            'C': ['D', 'F'],
            'D': ['object',],
            'E': ['object',],
            'F': ['object',],
            'object': []
        })) == expected_mro
