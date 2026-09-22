import unittest

from duckfine import DuckFine


class TestDuckFine(unittest.TestCase):
    def setUp(self):
        self.fine = DuckFine("M001")

    def test_stores_member_id(self):
        self.assertEqual(self.fine.member_id, "M001")

    def test_starts_with_no_amount_owed(self):
        self.assertEqual(self.fine.total_owed, 0.0)

    def test_no_fee_for_days_within_grace_period(self):
        self.assertEqual(self.fine.charge(0), 0.0)
        self.assertEqual(self.fine.charge(2), 0.0)

    def test_charges_daily_fee_after_grace_period(self):
        self.assertEqual(self.fine.charge(5), 1.50)

    def test_deluxe_duck_doubles_the_fee(self):
        self.assertEqual(self.fine.charge(5, deluxe=True), 3.00)

    def test_caps_a_single_charge_at_maximum_fee(self):
        self.assertEqual(self.fine.charge(20), 5.00)

    def test_accumulates_fees_in_total_owed(self):
        self.fine.charge(3)
        self.fine.charge(4)

        self.assertEqual(self.fine.total_owed, 1.50)

    def test_rejects_negative_days_late(self):
        with self.assertRaises(ValueError):
            self.fine.charge(-1)


if __name__ == "__main__":
    unittest.main()
