from collections import defaultdict

from fuzzconfig import FuzzConfig
import interconnect
import nets
import pytrellis
import re

jobs = [
        # Global mux connections. The relevant tiles were inferred from the
        # center_mux experiment.
        ("global_mux.txt", FuzzConfig(job="GLOBAL_MUX", family="MachXO2", device="LCMXO2-1200HC", ncl="center-ebr-cib_1200.ncl",
                  tiles=["CENTER9:CENTER8", "CENTER8:CENTER7"])),

        # Fixed connections within the global mux (as well as
        # direction select).
        # ("global_fixed.txt", FuzzConfig(job="GLOBAL_FIXED", family="MachXO2", device="LCMXO2-1200HC", ncl="center-ebr-cib_1200.ncl",
        #           tiles=["CENTER6:CENTER_EBR_CIB"])),
]


def main():
    pytrellis.load_database("../../../database")

    for job in jobs:
        net_file, cfg = job
        cfg.setup()

        netnames = [l.rstrip("\n") for l in open(net_file, "r")]
        interconnect.fuzz_interconnect_with_netnames(config=cfg, netnames=netnames,
                                                     netname_filter_union=False,
                                                     netdir_override=defaultdict(lambda : str("sink")),
                                                     full_mux_style=True,
                                                     bias=1)

    # TODO: R6C13_JA0 --> R6C13_JCE0_DCC. But TCL also claims
    # R6C13_CLKI0_DCC --> R6C13_CLKO0_DCC (pseudo = 1). Contradiction?
    # interconnect.fuzz_interconnect_with_netnames(config=cfg, netnames=["R6C13_CLKI0_DCC", "R6C13_CLKO0_DCC", "R6C13_JCE0_DCC"],
    #                                              netname_filter_union=False,
    #                                              netdir_override = {
    #                                                 "R6C13_JCE0_DCC" : "sink",
    #                                              },
    #                                              full_mux_style=True,
    #                                              bias=1)


if __name__ == "__main__":
    main()
