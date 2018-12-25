"""
Script that takes a list of origin cities and destination resorts and automate info gathering.

Will collect data on
* flight prices (if relevant)
* rental car prices
* lodging prices
* ski ticket prices
* travel times
"""

import datetime
from typing import Collection

from data.city import City
from data.resort import Resort


def run_info_gather(
        origin_cities: Collection[City],
        destination_resorts: Collection[Resort],
        start_date: datetime.date,
        end_date: datetime.date
):
    routes = get_all_routes(origin_cities, destination_resorts)

    unique_flight_routes = None
    flight_costs = get_flight_route_costs(unique_flight_routes, start_date, end_date)

    unique_drive_routes = None
    rental_costs = get_car_rental_costs(unique_drive_routes, start_date, end_date)

    unique_misc_routes = None
    misc_costs = get_misc_costs(unique_misc_routes, start_date, end_date)

    lodging_costs = get_lodging_costs(destination_resorts, start_date, end_date)

    lift_ticket_costs = get_lift_ticket_costs(destination_resorts, start_date, end_date)

    all_costs = [
        flight_costs,
        rental_costs,
        misc_costs,
        lodging_costs,
        lift_ticket_costs
    ]
    cost_summary = get_summarized_costs(routes, all_costs)

    return cost_summary


def main():
    pass


if __name__ == '__main__':
    main()
