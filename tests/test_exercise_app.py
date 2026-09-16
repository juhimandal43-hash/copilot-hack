import unittest
from datetime import datetime

from exercise_app import UserProfile, next_reminder, profile_label, recommend_exercises, validate_profile


class ExerciseLogicTests(unittest.TestCase):
    def test_valid_profile_and_bmi(self):
        profile, errors = validate_profile("30", "70", "175")
        self.assertEqual(errors, [])
        self.assertAlmostEqual(profile.bmi, 22.86, places=1)
        self.assertEqual(profile_label(profile), "Within the usual BMI range")

    def test_invalid_profile_reports_all_fields(self):
        profile, errors = validate_profile("x", "10", "300")
        self.assertIsNone(profile)
        self.assertEqual(len(errors), 3)

    def test_older_or_higher_bmi_gets_low_impact_route(self):
        suggestions = recommend_exercises(UserProfile(70, 90, 170))
        self.assertEqual(suggestions[0]["name"], "Steady walk")

    def test_next_reminder_rolls_to_tomorrow(self):
        now = datetime(2026, 9, 16, 9, 0)
        result = next_reminder("08:30", now)
        self.assertEqual(result, datetime(2026, 9, 17, 8, 30))

    def test_bad_reminder_time(self):
        self.assertIsNone(next_reminder("25:99"))


if __name__ == "__main__":
    unittest.main()
