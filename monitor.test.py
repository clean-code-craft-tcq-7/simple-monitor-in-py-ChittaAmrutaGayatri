# monitor.test.py
import unittest
from unittest.mock import patch
from monitor import (
    VITALS,
    display,
    sensorStub,
    translate,
    is_vital_ok,
    check_vitals,
    get_vital_state,
    report_vitals,
    vitals_ok
)

class MonitorTest(unittest.TestCase):

    @patch("monitor.display", return_value=False)
    def test_display(self, mock_display):
        self.assertFalse(display("sample error message"))
        mock_display.assert_called_once()

    def test_sensorStub(self):
        stub = sensorStub()
        self.assertIsNotNone(stub)
        self.assertTrue(all(v in stub for v in [v["name"] for v in VITALS]))

    def test_translate(self):
        self.assertEqual(translate("Good Morning", "german"), "GUTEN MORGEN")

    def test_is_vital_ok(self):
        self.assertTrue(is_vital_ok(96, 95, 102))
        self.assertFalse(is_vital_ok(110, 95, 102))

    @patch("monitor.display", return_value=False)
    def test_check_vitals(self, mock_display):
        self.assertTrue(check_vitals(96, 95, 102, "sample error message!"))
        self.assertFalse(check_vitals(110, 95, 102, "sample error message!"))

    def test_get_vital_state(self):
        self.assertEqual(get_vital_state(VITALS[0], 94), "HYPO")
        self.assertEqual(get_vital_state(VITALS[0], 95), "HYPO")
        self.assertEqual(get_vital_state(VITALS[0], 98), "NORMAL")
        self.assertEqual(get_vital_state(VITALS[0], 102), "HYPER")

    @patch("monitor.display", return_value=False)
    def test_vitals_ok_all_good(self, mock_display):
        stub = {v["name"]: (v["minvalue"] + v["maxvalue"]) // 2 for v in VITALS}
        self.assertTrue(vitals_ok(stub))

    @patch("monitor.display", return_value=False)
    def test_vitals_ok_with_bad_values(self, mock_display):
        for vital in VITALS:
            stub = {v["name"]: (v["minvalue"] + v["maxvalue"]) // 2 for v in VITALS}
            stub[vital["name"]] = vital["maxvalue"] + 10  # out of range
            self.assertFalse(vitals_ok(stub))

    @patch("monitor.display", return_value=False)
    def test_report_vitals_runs(self, mock_display):
        stub = {v["name"]: (v["minvalue"] + v["maxvalue"]) // 2 for v in VITALS}
        # just make sure it runs without error
        report_vitals(stub)

if __name__ == "__main__":
    unittest.main()
