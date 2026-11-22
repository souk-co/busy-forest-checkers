"""python3 table.py FAMILY B FILE: the sieve table of FAMILY for primes p < B, compared whole."""

import sys

from ec import ap, model, primes, read, verdict

family, bound, path = sys.argv[1:]
want = "".join(
    f"{p}: {' '.join('x' if (a := ap(model(family, r), p)) is None else str(a) for r in range(p))}\n"
    for p in primes(2, int(bound))
)
verdict(read(path) == want, f"table {family} B={bound}")
