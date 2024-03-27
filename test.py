import unittest

import vanilla


class TestVanilla(unittest.TestCase):

    def test_call(self):
        call_pv = vanilla.pv("C", 100, 100, 0.05, 0.04, 0.25, 1.0)

        self.assertAlmostEqual(call_pv, 11.7192658608191, 5)

    def test_put(self):
        call_pv = vanilla.pv("P", 100, 100, 0.05, 0.04, 0.25, 1.0)

        self.assertAlmostEqual(call_pv, 7.83722493597365, 5)


if __name__ == '__main__':
    unittest.main()
