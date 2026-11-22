# Checkers for public EC Rank side tasks

Two standard-library Python checkers for shareable tasks in the EC Rank methods note:
`survivors.py`, a survivor list from a parameter box (the paid task), and `table.py`, a sieve table
(task 4), kept as an unpaid end-to-end task. A Busy Forest source runs one as
`python3 ./<entry> <args> <submission>`. Each reads the submission as data and runs nothing from
it. Exit 0 passes; any other status fails, including a traceback on a malformed file. Each prints
one line, which the Souk discards. `ec.py` holds the shared arithmetic.

A Busy Forest source record names this repo, a commit, `entry: survivors.py` or `entry: table.py`,
and `runner: python3`. The source of truth is `templates-private/busy-forest/checkers/` in souk-co/souk;
this repo is its public export.

## Conventions

- **Families**, in Tate normal form `y^2 + (1 - c)xy - by = x^3 - bx^2` with `(b, c)` in t:
  `Z4` (t, 0), `Z5` (t, t), `Z6` (t^2 + t, t), `Z7` (t^3 - t^2, t^2 - t),
  `Z9` (t^2(t - 1)(t^2 - t + 1), t^2(t - 1)).
- **a_p** = p + 1 - #E(F_p) of that model at t mod p. `x` marks t where the model's
  discriminant vanishes mod p; no minimal model is taken.
- **S(B)** at t = u/v is the sum over primes 5 <= p < B, skipping primes dividing v and `x`
  primes, of -a_p log(p) / p, with a_p read at t ≡ u·v⁻¹ mod p (the −a_p sign the solvers' notes
  use, so high rank means large S).

## Survivor list

Args `FAMILY B U0 U1 V0 V1 CUT K`. The file has K lines `u v S`: distinct parameters t = u/v with
U0 <= u <= U1, V0 <= v <= V1 and gcd(u, v) = 1, each with S(B) >= CUT. Each line must equal
`f"{u} {v} {S:.6f}"` of the recomputed S, so no padded integers, signs or other spellings.
A fibre singular over Q (such as Z7 at t = 1, where b = c = 0) is refused. Only the listed rows are
recomputed; finding them takes a sweep of the box.

Example args `Z5 200 1 30 1 30 9.8 3`: [good](examples/survivors-good.txt) passes,
[bad](examples/survivors-bad.txt) (22/1 scores 8.43, below the cut) fails.

A task sized for pay, measured on zed (12 cores, Python 3.10, one core used): args
`Z5 1000 1 5000 1 2000 21.5 10`. The box holds 10⁷ (u, v) pairs, 6.1·10⁶ of them coprime, and
11 have S(1000) >= 21.5, so ten of them take nearly the whole box. A pure-Python sweep that first
builds a_p[t mod p] for every p < 1000 (18 s) and then adds one table entry per prime per pair
(249 s) took 267 s; calling the checker's `score` per pair (about 20 ms) would take over a day. Checking the ten rows
took 0.2–0.3 s. A staged cut (S(300) first) or numpy would sweep faster; a C or GPU sieve, as the
solvers run, would take seconds, so size the box to the reward and the solvers' tools.

## Sieve table

Args `FAMILY B`. The file has one line per prime p < B, in order: `p: v_0 v_1 ... v_{p-1}`, where
v_r is a_p at t ≡ r mod p, or `x`, separated by single spaces (a final newline is optional). The
checker builds the whole table and compares the text, so the task has one answer that the checker
itself produces; it is for testing the PR path, not for pay. Building costs about B³; B = 300
checks in 0.4 s and B = 1000 in 22 s, under the source run's 60 s timeout.

Example args `Z5 30`: [good](examples/table-good.txt) passes, [bad](examples/table-bad.txt) (one
entry at p = 23 changed) fails.

## Proposing one as a source

The source prompt copies `good` and `bad` out of the proposal, and the program refuses examples that
are not substrings of the proposal's text. Paste each example file verbatim, newlines included;
inside a JSON string its newlines become `\n` and the record is refused.

## Limits

- A survivor list proves its rows score above the cut, not that the box held nothing better or
  that any row has high rank.
- Task args allow only letters, digits, `_` and `.`, so a box cannot reach negative t.
- Next task kind: points on a fibre (independent points on the curve at a listed t), which needs a
  height pairing or `gp` to check.
- A calibration set (methods note task 10) is left out: what makes one worth paying for is that its
  fibres are record curves, and checking ranks needs `gp`, which a source run can't fetch.
