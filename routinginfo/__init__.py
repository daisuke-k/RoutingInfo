import mrtparse
import radix
import logging

class PrefixASPath:
    def __init__(self, filename):
        self.reader = mrtparse.Reader(filename)

    def __iter__(self):
            return self

    def __next__(self):
        for m in self.reader:
            mrt = m.mrt
            prefix = None
            prefixlen = None
            aspaths = []

            if mrt.subtype == mrtparse.TD_V2_ST['RIB_IPV4_UNICAST']:
                prefix = mrt.rib.prefix
                prefixlen = mrt.rib.plen

                for entry in mrt.rib.entry:
                    for attr in entry.attr:
                        if attr.type == mrtparse.BGP_ATTR_T['AS_PATH']:
                            for path_seg in attr.as_path:
                                if path_seg['type'] == mrtparse.AS_PATH_SEG_T['AS_SEQUENCE']:
                                    aspaths.append(path_seg['val'])
            if prefix is not None:
                return prefix, prefixlen, aspaths

class PrefixInfo:
    def __init__(self, filename=None):
        self._rtree = radix.Radix()

        if filename is not None:
            self.__read(filename)

    def __iter__(self):
        return self._rtree.__iter__()

    def __read(self, filename):
        c = 0
        for m in mrtparse.Reader(filename):
            mrt = m.mrt
            prefix = None
            prefixlen = None
            aspaths = []
            rnode = None

            c += 1

            if mrt.subtype == mrtparse.TD_V2_ST['RIB_IPV4_UNICAST']:
                prefix = mrt.rib.prefix
                prefixlen = mrt.rib.plen

                for entry in mrt.rib.entry:
                    for attr in entry.attr:
                        if attr.type == mrtparse.BGP_ATTR_T['AS_PATH']:
                            for path_seg in attr.as_path:
                                if path_seg['type'] == mrtparse.AS_PATH_SEG_T['AS_SEQUENCE']:
                                    aspaths.append(path_seg['val'])
            if prefix is not None:
                self.add(prefix, prefixlen, aspaths)

            if c % 1000 == 0:
                logging.debug("read {} records".format(c))
#                break

    def read(self, filename, clear=False):
        if clear:
            self._rtree = radix.Radix()
        self.__read(filename)

    def add(self, prefix, prefixlen, aspaths):
        rnode = self._rtree.add(prefix, prefixlen)
        rnode.data["aspaths"] = aspaths

        if len(aspaths) > 0:
            rnode.data["originases"] = list(map(lambda x: x[-1], aspaths))

    def search_best(self, ipaddr):
        return self._rtree.search_best(ipaddr)


