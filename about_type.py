from expecter import expect


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
