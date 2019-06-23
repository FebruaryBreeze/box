import unittest

import box


class MyTestCase(unittest.TestCase):
    def test_model_loader(self):
        @box.register
        class MockModule:
            schema = {}

        model_class = box.load('MockModule')
        self.assertIsNotNone(model_class)
        self.assertTrue(isinstance(model_class(), MockModule))

        box.register(int, name='MockModule')

    def test_tag(self):
        @box.register(tag='augmentation')
        class MockAugmentation:
            @classmethod
            def factory(cls, **_):
                return cls()

        self.assertEqual(box.load(name='MockAugmentation', tag='augmentation'), MockAugmentation)
        self.assertEqual(box.load(name='MockAugmentation'), None)
        self.assertEqual(box.Box.list(tag='augmentation'), {
            'MockAugmentation': MockAugmentation
        })

        augmentation = box.factory(config={
            'type': 'MockAugmentation',
        }, tag='augmentation')
        self.assertIsInstance(augmentation, MockAugmentation)
        box.erase(name='MockAugmentation', tag='augmentation')


if __name__ == '__main__':
    unittest.main()
