from infi.unittest import TestCase
from infi.unittest import parameters

class EqualityTest(TestCase):
    @parameters.iterate('a', [2, 1+1])
    def setUp(self, a):
        super(EqualityTest, self).setUp()
        self.a = a
    @parameters.iterate('b', [2.0, 2, 1 + 1])
    def test__equality(self, b):
        self.assertEquals(self.a, b)
    @parameters.iterate('b', [3, 'a', None])
    def test__inequality(self, b):
        self.assertNotEquals(self.a, b)
