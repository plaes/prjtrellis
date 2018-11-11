import pip_classes
import extract_ncl_routing
import parse_sdf
import sys


def get_equations(ncl, sdf):
    signals, bels = extract_ncl_routing.parse_ncl(ncl)
    sdf = parse_sdf.parse_sdf_file(sdf)
    wire_fanout = {} # (wire, pipclass) -> fanout
    path_pip_classes = {} # (src, dest) -> [(wire, pipclass)]
    for name, sig in sorted(signals.items()):
        nd = extract_ncl_routing.net_to_dict(sig, bels)
        drivers, loads, route = sig
        if len(drivers) != 1:
            continue
        if nd is None:
            continue
        drv = drivers[0]
        for load in loads:
            path = []
            if load not in nd:
                continue
            wire = nd[load]
            skip = False

            while wire != drv:
                path.append(wire)
                if wire not in nd:
                    skip = True
                    break
                wire = nd[wire]
            if skip:
                continue
            path.reverse()
            path_pip_classes[drv, load] = []
            for i in range(len(path) - 1):
                pip_src = path[i]
                pip_dst = path[i+1]
                pip_class = pip_classes.get_pip_class(pip_src, pip_dst)
                if pip_class is None:
                    skip = True
                    break
                path_pip_classes[drv, load].append((pip_src, pip_class))
                wire_fanout[pip_src, pip_class] = wire_fanout.get((pip_src, pip_class), 0) + 1
            if skip:
                del path_pip_classes[drv, load]
                continue
    for k, v in sorted(path_pip_classes.items()):
        src, dst = k
        pname = "({}.{}, {}.{})".format(src[0], src[1], dst[0], dst[1])
        print("{} = {}".format(pname, " + ".join(x[1] for x in v)))


def main():
    get_equations(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
