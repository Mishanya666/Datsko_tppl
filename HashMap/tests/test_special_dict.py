import unittest
from special_dict import SpecialDict, ConditionError

class TestSpecialDict(unittest.TestCase):
    def setUp(self):
        self.special_map = SpecialDict()
        self.special_map["value1"] = 1
        self.special_map["value2"] = 2
        self.special_map["value3"] = 3
        self.special_map["1"] = 10
        self.special_map["2"] = 20
        self.special_map["3"] = 30
        self.special_map["1, 5"] = 100
        self.special_map["5, 5"] = 200
        self.special_map["10, 5"] = 300

    def test_iloc_access(self):
        self.assertEqual(self.special_map.iloc[0], 10)
        self.assertEqual(self.special_map.iloc[2], 300)
        self.assertEqual(self.special_map.iloc[5], 200)
        self.assertEqual(self.special_map.iloc[8], 3)

    def test_iloc_out_of_range(self):
        with self.assertRaises(IndexError):
            _ = self.special_map.iloc[9]

    def test_ploc_simple_condition(self):
        result = self.special_map.ploc[">=1"]
        expected = {'1': 10, '2': 20, '3': 30}
        self.assertEqual(result, expected)

    def test_ploc_multiple_conditions(self):
        result = self.special_map.ploc[">0, >0"]
        expected = {'1, 5': 100, '5, 5': 200, '10, 5': 300}
        self.assertEqual(result, expected)

        result = self.special_map.ploc[">=10, >0"]
        expected = {'10, 5': 300}
        self.assertEqual(result, expected)

    def test_ploc_complex_conditions(self):
        self.special_map["1, 5, 3"] = 400
        result = self.special_map.ploc["<5, >=5, >=3"]
        expected = {'1, 5, 3': 400}
        self.assertEqual(result, expected)

    def test_ploc_invalid_conditions(self):
        with self.assertRaises(ConditionError):
            _ = self.special_map.ploc["invalid"]

        with self.assertRaises(ConditionError):
            _ = self.special_map.ploc["==5"]

    def test_ploc_ignored_invalid_keys(self):
        self.special_map["invalid_key"] = 999
        result = self.special_map.ploc[">0, >0"]
        expected = {'1, 5': 100, '5, 5': 200, '10, 5': 300}
        self.assertEqual(result, expected)

    def test_sorted_keys_after_update(self):
        self.special_map["0"] = 0
        self.assertEqual(self.special_map.iloc[0], 0)

        del self.special_map["0"]
        self.assertEqual(self.special_map.iloc[0], 10)

if __name__ == "__main__":
    unittest.main()
