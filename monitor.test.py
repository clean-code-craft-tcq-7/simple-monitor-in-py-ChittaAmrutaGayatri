import unittest
from monitor import VITALS, display, sensorStub, translate, is_inrange, check_vitals, print_status, vitals_ok


class MonitorTest(unittest.TestCase):
    def test_display(self):
        self.assertFalse(display("sample error message"))

    def test_sensorStub(self):
        self.assertIsNotNone(sensorStub())

    def test_translate(self):
        self.assertEqual(translate("Good Morning", "german"), "GUTEN MORGEN")

    def test_is_in_range(self):
        self.assertTrue(is_inrange(96, 95, 102))
        self.assertFalse(is_inrange(110, 95, 102))

    def test_check_vitals(self):
        self.assertTrue(check_vitals(96, 95, 102, "sample error message!"))
        self.assertFalse(check_vitals(110, 95, 102, "sample error message!"))

    def test_print_status(self):
        self.assertTrue(print_status(VITALS[0], 99))

    def test_vitals_ok(self):
        self.assertTrue(vitals_ok(sensorStub()))

    def test_temperature(self):
        sensorstub = sensorStub()
        sensorstub["temperature"] = 103
        self.assertFalse(vitals_ok(sensorstub))

    def test_pulserate(self):
        sensorstub = sensorStub()
        sensorstub["pulserate"] = 103
        self.assertFalse(vitals_ok(sensorstub))

    def test_spo2(self):
        sensorstub = sensorStub()
        sensorstub["spo2"] = 103
        self.assertFalse(vitals_ok(sensorstub))

    def test_blood_sugar(self):
        sensorstub = sensorStub()
        sensorstub["blood-sugar"] = 112
        self.assertFalse(vitals_ok(sensorstub))

    def test_blood_pressure(self):
        sensorstub = sensorStub()
        sensorstub["blood-pressure"] = 160
        self.assertFalse(vitals_ok(sensorstub))

    def test_respiratory_rate(self):
        sensorstub = sensorStub()
        sensorstub["respiratory-rate"] = 25
        self.assertFalse(vitals_ok(sensorstub))


if __name__ == "__main__":
    unittest.main()
