import unittest
from monitor import vitals_ok, vitals_status


class MonitorTest(unittest.TestCase):
    def test_temperature_out_of_range(self):
        self.assertFalse(vitals_ok(103, 70, 95))   # too high
        self.assertFalse(vitals_ok(94, 70, 95))    # too low

    def test_pulse_out_of_range(self):
        self.assertFalse(vitals_ok(98.6, 55, 95))  # too low
        self.assertFalse(vitals_ok(98.6, 120, 95)) # too high

    def test_spo2_out_of_range(self):
        self.assertFalse(vitals_ok(98.6, 70, 85))  # too low

    def test_all_vitals_ok(self):
        self.assertTrue(vitals_ok(98.6, 72, 96))

    def test_status_dict(self):
        status = vitals_status(103, 72, 96)
        self.assertEqual(status["temperature"], False)
        self.assertEqual(status["pulseRate"], True)
        self.assertEqual(status["spo2"], True)


if __name__ == '__main__':
    unittest.main()


