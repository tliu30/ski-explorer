import datetime
from typing import Iterable, MutableMapping

from costs.interface import get_cost_from_browser_and_manual_input
from data.transit_times import TransitRoute
from scraper.kayak_url_builder import get_kayak_flight_search_url
from settings import config


def get_flight_route_cost(route: TransitRoute, start_date: datetime.date, end_date: datetime.date) -> float:
    url = get_kayak_flight_search_url(
        config.KAYAK_URL,
        route.origin,
        route.destination,
        start_date,
        end_date
    )
    prompt = 'Please input price for flight from {origin} to {destination} ({start_date} to {end_date}): '.format(
        origin=route.origin.name,
        destination=route.destination.name,
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat(),
    )
    return get_cost_from_browser_and_manual_input(url, prompt)


def get_flight_route_costs(
        routes: Iterable[TransitRoute],
        start_date: datetime.date,
        end_date: datetime.date
) -> MutableMapping[TransitRoute, float]:
    return {route: get_flight_route_cost(route, start_date, end_date) for route in routes}
