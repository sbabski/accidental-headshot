from extractor import *
from pprint import pprint

parse_page('ratchet and clank', 'franchise')
parse_page('kikaider', 'series')
parsed = parse_page('family guy', 'western animation')
pprint(parsed)
