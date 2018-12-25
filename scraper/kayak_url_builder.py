from datetime import datetime
from enum import Enum
import logging
from typing import Iterable, Sequence, Tuple, Union

from data.city import City
from data.resort import Resort

logger = logging.getLogger(__name__)

BASE_URL = 'https://www.kayak.com'


# Keys for location codes

LOCATION_TO_KAYAK_CODE_PAIRS: Sequence[Tuple[Union[City, Resort], str]] = (
    (City.BOSTON, 'BOS-a25588'),
    (City.NYC, 'New-York,NY-c15830'),
    (City.NYC_AIR, 'EWR-a15830'),
    (City.DENVER, 'DEN-a12493'),
    (City.RENO, 'RNO-a7128'),
    (City.HAYDEN, 'HDN-a32387'),
    (Resort.VAIL, 'EGE-a26088'),
    (City.SLC, 'SLC-a31915'),
    (City.BOISE, 'BOI-a16735')
)


def get_kayak_code_for_location(location: Union[City, Resort]) -> str:
    mapping = dict(LOCATION_TO_KAYAK_CODE_PAIRS)
    logger.debug('Using location --> kayak code mapping %s', str(mapping))

    if location not in mapping:
        raise AssertionError('Could not find kayak code for location key {}'.format(location))

    return mapping[location]


LOCATION_TO_KAYAK_FLIGHT_CODE_PAIRS: Sequence[Tuple[Union[City, Resort], str]] = (
    (City.BOSTON, 'BOS'),
    (City.NYC, 'NYC'),
    (City.NYC_AIR, 'NYC'),
    (City.DENVER, 'DEN'),
    (City.RENO, 'RNO'),
    (City.HAYDEN, 'HDN'),
    (Resort.VAIL, 'EGE'),
    (City.SLC, 'SLC'),
    (City.BOISE, 'BOI')
)


def get_kayak_flight_code_for_location(location: Union[City, Resort]) -> str:
    mapping = dict(LOCATION_TO_KAYAK_FLIGHT_CODE_PAIRS)
    logger.debug('Using location --> kayak flight code mapping %s', str(mapping))

    if location not in mapping:
        raise AssertionError('Could not find kayak flight code for location key {}'.format(location))

    return mapping[location]


# URL Construction

class SearchType(Enum):
    CARS = 1
    FLIGHTS = 2


def _get_date_in_kayak_car_url_format(datetime_obj: datetime) -> str:
    return datetime_obj.strftime('%Y-%m-%d-%Hh')


def _get_date_in_kayak_flight_url_format(datetime_obj: datetime) -> str:
    return datetime_obj.strftime('%Y-%m-%d')


def _get_kayak_url(
        base_url: str,
        search_type: SearchType,
        trip_id: str,
        start_datetime_code: str,
        end_datetime_code: str,
        addl_kwargs: Iterable[str]
) -> str:
    url_template = '{base_url}/{search_type}/{trip_id}/{start_datetime}/{end_datetime}?{addl_kwargs}'

    formatted_url = url_template.format(
        base_url=base_url,
        search_type=search_type.name.lower(),
        trip_id=trip_id,
        start_datetime=start_datetime_code,
        end_datetime=end_datetime_code,
        addl_kwargs='&'.join(addl_kwargs)
    )

    return formatted_url


def get_kayak_flight_search_url(
        base_url: str,
        origin: Union[City, Resort],
        destination: Union[City, Resort],
        start_datetime: datetime,
        end_datetime: datetime
) -> str:
    trip_id = '{}-{}'.format(
        get_kayak_flight_code_for_location(origin),
        get_kayak_flight_code_for_location(destination)
    )

    return _get_kayak_url(
        base_url,
        SearchType.FLIGHTS,
        trip_id,
        _get_date_in_kayak_flight_url_format(start_datetime),
        _get_date_in_kayak_flight_url_format(end_datetime),
        []
    )
