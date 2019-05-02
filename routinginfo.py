import mrtparse

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
