"""Shared arithmetic for the EC Rank checkers. Standard library only."""

import math
import sys
from fractions import Fraction
from functools import cache

# Tate normal form E(b, c): y^2 + (1 - c)xy - by = x^3 - bx^2, with (b, c) polynomial in t.
FAMILIES = {
    "Z4": lambda t: (t, 0),
    "Z5": lambda t: (t, t),
    "Z6": lambda t: (t * t + t, t),
    "Z7": lambda t: (t**3 - t**2, t**2 - t),
    "Z9": lambda t: (t**2 * (t - 1) * (t**2 - t + 1), t**2 * (t - 1)),
}


@cache
def primes(lo, hi):
    return [
        p
        for p in range(max(lo, 2), hi)
        if all(p % q for q in range(2, math.isqrt(p) + 1))
    ]


def model(family, t):
    b, c = FAMILIES[family](t)
    return (1 - c, -b, -b, 0, 0)


def disc(a):
    a1, a2, a3, a4, a6 = a
    b2, b4, b6 = a1 * a1 + 4 * a2, a1 * a3 + 2 * a4, a3 * a3 + 4 * a6
    b8 = a1 * a1 * a6 + 4 * a2 * a6 - a1 * a3 * a4 + a2 * a3 * a3 - a4 * a4
    return -b2 * b2 * b8 - 8 * b4**3 - 27 * b6 * b6 + 9 * b2 * b4 * b6


@cache
def squares(p):
    chi = [0] + [-1] * (p - 1)
    for x in range(1, p):
        chi[x * x % p] = 1
    return chi


def ap(a, p):
    """a_p = p + 1 - #E(F_p) of y^2 + a1xy + a3y = x^3 + a2x^2 + a4x + a6 mod p, or None if singular."""
    a1, a2, a3, a4, a6 = a = [v % p for v in a]
    if disc(a) % p == 0:
        return None
    if p == 2:
        return 2 - sum(
            (y * y + a1 * x * y + a3 * y - x**3 - a2 * x * x - a4 * x - a6) % 2 == 0
            for x in (0, 1)
            for y in (0, 1)
        )
    b2, b4, b6 = a1 * a1 + 4 * a2, a1 * a3 + 2 * a4, a3 * a3 + 4 * a6
    chi = squares(p)
    return -sum(chi[(((4 * x + b2) * x + 2 * b4) * x + b6) % p] for x in range(p))


def singular(family, u, v):
    return disc(model(family, Fraction(u, v))) == 0


def score(family, u, v, bound):
    """S(B) at t = u/v: the sum over primes 5 <= p < B, p not dividing v, where the model at
    t = u v^-1 mod p is nonsingular, of -a_p log(p) / p."""
    return sum(
        -a * math.log(p) / p
        for p in primes(5, bound)
        if v % p and (a := ap(model(family, u * pow(v, -1, p)), p)) is not None
    )


def read(path):
    text = open(path, encoding="ascii").read()
    return text if text.endswith("\n") else text + "\n"


def verdict(ok, line):
    print(("PASS " if ok else "FAIL ") + line)
    sys.exit(0 if ok else 1)
