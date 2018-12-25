import unittest

from data.transit_times import read_default_transit_times
from data.resorts import Resorts


class TestDataCompleteness(unittest.TestCase):

    def test_all_resorts_in_transit_file(self):
        """Ensure that all the resorts are represented as destinations in transit file"""
        routes = read_default_transit_times()

        expected_destinations = {x for x in Resorts}
        found_destinations = {x.destination for x in routes}
        missing_destinations = expected_destinations.difference(found_destinations)
        self.assertSetEqual(
            set(), missing_destinations, 'Destinations missing from transit file: {}'.format(missing_destinations)
        )

