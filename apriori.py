from collections import Counter
import argparse
import itertools
import sys


def apriori(source_file, minsup):
    with open(source_file) as file:
        lines = [line.strip().split() for line in file.readlines()]

    minsup = float(minsup)
    n = len(lines)

    F = sorted([k for k, v
              in Counter(list(itertools.chain.from_iterable(lines))).iteritems()
              if float(v) / n > minsup]) # make sure it is counted correctly

    candidates = gen_candidate(lines)

def gen_candidate(l):
    candidates = []
    l = sorted(ensure_list_of_lists(l))
    prefixes = sorted([list(x) for x in set(frozenset(i) for i in (set(i[:-1]) for i in l))])

    for prefix in prefixes:
        postfixes = [p[-1:] for p in l if p[:-1] == prefix]
        postfixes = list(itertools.chain.from_iterable(postfixes))
        comb = list(itertools.combinations(postfixes,2))

        for c in comb:
            candidates.append(prefix + list(c))

    return candidates


def restricted_float(infloat):
    infloat = float(infloat)
    if infloat < 0.0 or infloat > 1.0:
        raise argparse.ArgumentTypeError("%r not in range [0.0, 1.0]" % (infloat,))
    return infloat


def ensure_list_of_lists(F):
    if not isinstance(F[0], list):
        return [[x] for x in F]
    else:
        return F


def main(argv):
    parser = argparse.ArgumentParser(description='Apriori algorithm')
    parser.add_argument("source", help="Source transaction file location")
    parser.add_argument("minsup", help="Minimum support", type=restricted_float)
    args = parser.parse_args()

    apriori(args.source, args.minsup)

if __name__ == "__main__":
    main(sys.argv[1:])
