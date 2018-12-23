from enum import Enum
import logging
import os
from typing import Dict, List, MutableSequence, NamedTuple, Sequence, TextIO, Union

from settings.cities import Cities
from settings.resorts import Resorts

logger = logging.getLogger(__name__)

TRANSIT_TIMES_PATH = os.path.join(os.path.dirname(__file__), 'transit_times.csv')
TRANSIT_TIMES_EXPECTED_HEADER = {
    'LOCATION_01',
    'TYPE_01',
    'LOCATION_02',
    'TYPE_02',
    'TRANSIT_TIME',
    'TRANSIT_TYPE'
}


class TransitType(Enum):
    CAR = 1
    PLANE = 2
    TAXI = 3
    METRO = 4


class TransitRoute(NamedTuple):
    origin: Union[Cities, Resorts]
    destination: Union[Cities, Resorts]
    transit_time: float
    transit_type: TransitType


def _read_simple_csv(filelike: TextIO, sep: str=',') -> List[Dict[str, str]]:
    lines = [line.strip().split(sep) for line in filelike.read().split('\n') if line]

    if not lines:
         raise AssertionError('No rows found in file!')

    if len(lines) == 1:
        raise AssertionError('Only a header was found in file!')

    header = lines[0]
    return [dict(zip(header, line)) for line in lines[1:]]


def _parse_into_location(location_name: str, location_type: str) -> Enum:
    if location_type == 'CITY':
        return Cities[location_name]
    elif location_type == 'RESORT':
        return Resorts[location_name]
    else:
        raise ValueError('Did not recognize location_type found ({})'.format(location_type))


def _parse_time_into_hours(time_hhmm: str) -> float:
    hours, minutes = time_hhmm.split(':')
    return float(hours) + float(minutes) / 60


def read_transit_times_csv(filelike: TextIO) -> Sequence[TransitRoute]:
    data = _read_simple_csv(filelike)

    example_header = data[0].keys()
    if TRANSIT_TIMES_EXPECTED_HEADER != set(example_header):
        raise AssertionError('Bad header found: {}'.format(example_header))

    routes: MutableSequence[TransitRoute] = []
    for row in data:
        routes.append(TransitRoute(
            origin=_parse_into_location(row['LOCATION_01'], row['TYPE_01']),
            destination=_parse_into_location(row['LOCATION_02'], row['TYPE_02']),
            transit_time=_parse_time_into_hours(row['TRANSIT_TIME']),
            transit_type=TransitType[row['TRANSIT_TYPE']]
        ))

    return routes


def read_default_transit_times() -> Sequence[TransitRoute]:
    logger.info('Reading transit times from %s', TRANSIT_TIMES_PATH)
    with open(TRANSIT_TIMES_PATH, 'r') as f:
        return read_transit_times_csv(f)
