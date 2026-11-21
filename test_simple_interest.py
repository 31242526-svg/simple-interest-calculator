"""Tests for simple_interest.py. Run with: python -m unittest -v"""

import unittest
from decimal import Decimal

from simple_interest import simple_interest


class SimpleInterestTests(unittest.TestCase):
    def test_whole_numbers(self):
        interest, total = simple_interest(Decimal("10000"), Decimal("5"), Decimal("3"))
        self.assertEqual(interest, Decimal("1500.00"))
        self.assertEqual(total, Decimal("11500.00"))

    def test_fractional_rate(self):
        interest, total = simple_interest(Decimal("2500"), Decimal("7.5"), Decimal("2"))
        self.assertEqual(interest, Decimal("375.00"))
        self.assertEqual(total, Decimal("2875.00"))

    def test_fractional_time(self):
        interest, total = simple_interest(Decimal("1200"), Decimal("4"), Decimal("1.5"))
        self.assertEqual(interest, Decimal("72.00"))
        self.assertEqual(total, Decimal("1272.00"))

    def test_zero_rate_returns_principal(self):
        interest, total = simple_interest(Decimal("800"), Decimal("0"), Decimal("5"))
        self.assertEqual(interest, Decimal("0.00"))
        self.assertEqual(total, Decimal("800.00"))

    def test_rounds_half_up_to_two_places(self):
        interest, total = simple_interest(Decimal("1000"), Decimal("3.333"), Decimal("1"))
        self.assertEqual(interest, Decimal("33.33"))
        self.assertEqual(total, Decimal("1033.33"))


if __name__ == "__main__":
    unittest.main()
