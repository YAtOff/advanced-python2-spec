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


Whats is the MRO of clase `A`?

>>> A.mro()
[<class 'about_mro.A'>, <class 'about_mro.B'>, <class 'about_mro.C'>,\
 <class 'about_mro.D'>, <class 'about_mro.E'>, <class 'about_mro.F'>,\
 <type 'object'>]

But where that comes from?
MRO is calculated with the C3 algorithm.
To understand the C3 algotithm, implement one.
Or see the implementation on https://github.com/mikeboers/C3Linearize.git
"""

O = object
class F(O): pass
class E(O): pass
class D(O): pass
class C(D,F): pass
class B(D,E): pass
class A(B,C): pass
