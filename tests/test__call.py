import unittest
from infi.unittest.call import Call

class CallTest(unittest.TestCase):
    def test__call_objects(self):
        for example_args, example_kwargs in [
            ((), {}),
            ((1, 2, 3), {}),
            ((), dict(a=())),
            (([],), dict(b=2)),
            (([1, 2, 3],), dict(b=[2, 3])),
            ((object(), {}), dict(b=[], c={})),
            ]:
            obj1 = Call(*example_args, **example_kwargs)
            obj2 = Call(*example_args, **example_kwargs)
            with self.assertRaises(TypeError):
                hash(obj1)
            for equal_object in [obj1, obj2]:
                self.assertTrue(obj1 == equal_object)
                self.assertFalse(obj1 != equal_object)
            for unequal_object in [1, "a", True, 0.5, object(), Call(1, 2, 3, d=object(), e=[])]:
                self.assertFalse(obj1 == unequal_object)
                self.assertTrue(obj1 != unequal_object)

