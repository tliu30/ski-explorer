from datetime import datetime
from enum import Enum
import logging
from typing import Sequence, Tuple, Union

from settings.cities import Cities
from settings.resorts import Resorts

logger = logging.getLogger(__name__)

BASE_URL = 'https://www.kayak.com'


# Keys for location codes

LOCATION_TO_KAYAK_CODE_PAIRS: Sequence[Tuple[Union[Cities, Resorts], str]] = (
    (Cities.BOSTON, 'BOS-a25588'),
    (Cities.NYC, 'New-York,NY-c15830'),
    (Cities.NYC_AIR, 'EWR-a15830'),
    (Cities.DENVER, 'DEN-a12493'),
    (Cities.RENO, 'RNO-a7128'),
    (Cities.HAYDEN, 'HDN-a32387'),
    (Resorts.VAIL, 'EGE-a26088'),
    (Cities.SLC, 'SLC-a31915'),
    (Cities.BOISE, 'BOI-a16735')
)


def get_kayak_code_for_location(location: Union[Cities, Resorts]) -> str:
    mapping = dict(LOCATION_TO_KAYAK_CODE_PAIRS)
    logger.debug('Using location --> kayak code mapping %s', str(mapping))

    if location not in mapping:
        raise AssertionError('Could not find kayak code for location key {}'.format(location))

    return mapping[location]


# URL Construction

class SearchType(Enum):
    CARS = 1


def _get_date_in_kayak_url_format(datetime_obj: datetime) -> str:
    return datetime_obj.strftime('%Y-%m-%d-%Hh')


def build_kayak_url(base_url: str, search_type: SearchType, location: Union[Cities, Resorts], start_datetime: datetime, end_datetime: datetime) -> str:
    url_template = '{base_url}/{search_type}/{location_code}/{start_datetime}/{end_datetime}?{addl_kwargs}'

    formatted_url = url_template.format(
        base_url=base_url,
        search_type=search_type.name.lower(),
        location_code=get_kayak_code_for_location(location),
        start_datetime=_get_date_in_kayak_url_format(start_datetime),
        end_datetime=_get_date_in_kayak_url_format(end_datetime),
        addl_kwargs=''
    )

    return formatted_url
