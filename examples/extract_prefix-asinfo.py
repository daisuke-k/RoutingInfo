import sys
import logging

import routinginfo

USAGE="""
Usage: {} [mrt filename]
"""

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(USAGE.format(sys.argv[0]), file=sys.stderr)

    filename = sys.argv[1]

    logging.basicConfig(level=logging.DEBUG)

    d = routinginfo.PrefixInfo(filename)
    for rnode in d:
        print(rnode.prefix, rnode.prefixlen, rnode.data)
