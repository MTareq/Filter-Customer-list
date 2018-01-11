import unittest
from filter_customers import find_distance, within_reach


class TestFilterCustomers(unittest.TestCase):

    def setUp(self):
        self.effel_tower = (48.8584, 2.2945)
        self.big_ben = (51.5007, -0.1246)
        self.statue_of_liberty = (40.6892, -74.0445)
        pass

    def test_find_distance(self):
        "Abslute Distance between Effel Tower(48.8584, 2.2945) and Big Ben(51.5007, -0.1246) is 340.5 km"
        self.assertEqual(format(find_distance(self.effel_tower, self.big_ben), '.1f'), '340.5')
        """Abslute Distance between Effel Tower(48.8584, 2.2945) and
            the Statue of Liberty (40.6892, -74.0445) is  5,837.4 km"""
        self.assertEqual(format(find_distance(self.effel_tower, self.statue_of_liberty), '.1f'), '5837.4')

    def test_within_reach(self):
        self.assertEqual(within_reach(10), True)
        self.assertNotEqual(within_reach(2000), True)


if __name__ == '__main__':
    unittest.main()
