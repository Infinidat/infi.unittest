import itertools
from infi.unittest import TestCase as InfiTestCase
from infi.unittest.parameters import iterate

class Validator(object):
    def __init__(self, expected):
        super(Validator, self).__init__()
        self.expected = set(expected)
    def is_successful(self):
        return not self.expected

def get_test_and_validator():
    prefixes = [10, 20, 30]
    numbers1 = [2, 3, 4]
    numbers2 = [5, 6, 7]

    validator = Validator(itertools.product(prefixes, numbers1, numbers2))
    class ReturnedTest(InfiTestCase):
        @iterate('prefix', prefixes)
        def setUp(self, prefix):
            super(ReturnedTest, self).setUp()
            self.prefix = prefix
        @iterate('number1', numbers1)
        @iterate('number2', numbers2)
        def test(self, number1, number2):
            validator.expected.remove((self.prefix, number1, number2))
    return ReturnedTest, validator
