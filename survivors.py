"""python3 survivors.py FAMILY B U0 U1 V0 V1 CUT K FILE: K parameters t = u/v in the box with S(B) >= CUT."""

import math
import sys

from ec import read, score, singular, verdict

family, bound, u0, u1, v0, v1, cut, k, path = sys.argv[1:]
task = f"survivors {family} B={bound} u={u0}..{u1} v={v0}..{v1} S>={cut} k={k}"
rows = [line.split(" ") for line in read(path).split("\n")[:-1]]
if len(rows) != int(k) or any(len(r) != 3 for r in rows):
    verdict(False, f"{task}: not {k} lines 'u v S'")
if len({(r[0], r[1]) for r in rows}) != len(rows):
    verdict(False, f"{task}: a parameter is listed twice")
for r in rows:
    u, v = int(r[0]), int(r[1])
    if not (
        int(u0) <= u <= int(u1) and int(v0) <= v <= int(v1) and math.gcd(u, v) == 1
    ):
        verdict(False, f"{task}: {r[0]} {r[1]} is not a reduced u/v in the box")
    if singular(family, u, v):
        verdict(False, f"{task}: the fibre at {u}/{v} is singular")
    s = score(family, u, v, int(bound))
    if " ".join(r) != f"{u} {v} {s:.6f}" or s < float(cut):
        verdict(False, f"{task}: S({u}/{v}) is {s:.6f}")
verdict(True, task)
