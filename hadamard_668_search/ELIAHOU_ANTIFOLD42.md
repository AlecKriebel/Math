# The orientation-free anti-fold at the distance-41 boundary

## Status

The adjacent-42 sum fold has an exact complementary partner.  Reducing the
base-sequence norm modulo `z^42+1` produces a length-42 **anti-fold**.  On the
minimum-distance shell, choosing the lower or upper endpoint of a
separation-42 pair has the same anti-fold effect: it zeros that cell.

Consequently, the only open special-distance-41 lane

```text
39 s-only changes + one reciprocal pair of q-only changes
```

splits into two stages:

1. an orientation-free binary support problem with 39 selected cells;
2. only after a support survives, a signed endpoint-orientation lift back
   through the adjacent-42 sum fold.

This removes all `2^39` endpoint orientations from the first exact test.  The
39 root-compatible reciprocal `q` pairs give only 30 distinct anti-fold
instances, because the 18 short pairs occur in nine identical mirrored
pairs.

The completed certificate status is now:

- the long `q` instance with representative 0 is **certified UNSAT** even
  without either root profile; a standalone CaDiCaL run emitted a binary
  DRAT proof that passed independent `drat-trim` replay;
- all nine canonical short instances `S02,S04,...,S18` are excluded by a
  complete exact-integer census; and
- the other twenty long instances remain open.

Long representative 2 was solver-reported UNSAT in one historical run but
has no checked proof, so it remains an observation rather than a theorem.
Thus ten of the thirty anti-fold support instances are closed.  No theorem
excluding all distance-41 repairs is claimed.

The dependency-free checker `verify_eliahou_antifold42.py` verifies the
mathematical reduction.  The separate exploratory encoder
`search_eliahou_antifold_sat.py` constructs the finite support instances.

## 1. Reduction modulo `z^42+1`

For a row `X` of length 84 or 83, define

```text
D_X(j) = X_j - X_(j+42),       0 <= j < 42,
```

where the missing endpoint of a short row is zero.  This is ordinary
polynomial reduction modulo `z^42+1`.

If `R_k` denotes the summed aperiodic correlation of the four base rows and
`Q_k` the summed negacyclic norm coefficients of the four anti-folds, then

```text
Q_0 = R_0 - 2 R_42,

Q_k = R_k - R_(42-k) - R_(42+k) + R_(84-k),
                                      1 <= k <= 20,

Q_21 = 0,
Q_(42-k) = -Q_k.                                  (1)
```

Thus every `BS(84,83)` obeys

```text
sum_X N_-(D_X) = 334       in Z[z]/(z^42+1),       (2)
```

where `N_-` is the negacyclic norm.

Equation (2) is independent of the adjacent-42 sum-fold equation.  Together
they are the two evaluations of every separation-42 pair:

```text
sum fold:          X_j + X_(j+42),
anti-fold:         X_j - X_(j+42).
```

## 2. The seed anti-fold

For Eliahou's base rows, the anti-fold energy is 654.  Its only nonzero
summed norm coefficients are

```text
k :   0    4     8    12    16    26    30    34    38
Q : 654 -512   384  -256   128  -128   256  -384   512.
```

The zero-lag value has a direct pair interpretation.  The seed has 163
opposite separation-42 pairs, three equal pairs, and two short singletons:

```text
Q_0 = 2 + 4*163 = 654.
```

An exact target has 83 opposite and 83 equal pairs, so

```text
Q_0 = 2 + 4*83 = 334.
```

This is the anti-fold version of the adjacent-fold distance bound.

## 3. Why endpoint orientation disappears

Let a seed-opposite pair be

```text
(X_j, X_(j+42)) = (x,-x).
```

Flipping its lower endpoint gives

```text
(-x)-(-x) = 0,
```

whereas flipping its upper endpoint gives

```text
x-x = 0.
```

Both orientations therefore produce the same anti-fold coefficient.

At special distance 41, each of the 39 `s` changes zeros one anti-fold cell
in each of two rows.  The two `q` changes zero one cell each in the active
product row.  Exactly 80 anti-fold entries of magnitude two disappear:

```text
654 - 80*4 = 334.
```

The zero-lag equation is automatic.  The remaining exact problem is to make
the 20 independent nonzero coefficients in (2) vanish.

## 4. Binary support parameterization

Write `L` for the selected long half-pair cells and `S` for the selected
short half-pair cells.  Before the reciprocal `q` pair is removed, their
available cells are

```text
long:   0,1,...,40             (41 cells),
short:  1,2,...,39             (39 cells).
```

The two active `q` cells are unavailable to the `s` support.  In 38 of the
39 cases this leaves 78 support cells.  The long pair with representative
index 0 uses one boundary cell that was already unavailable, so it leaves
79.  In every case,

```text
|L| + |S| = 39.                                   (3)
```

Once `(L,S)` is chosen, all four anti-fold rows are fixed: start with the
seed anti-fold, zero the two active `q` cells in row `B` or `D`, and zero
every cell of `L` in both long rows and every cell of `S` in both short
rows.  The exact support equation is then simply (2).

Only a support satisfying (2) proceeds to endpoint signs.  The root profiles
from the adjacent-fold theorem then prescribe the signed sums on the even
and odd selected cells.

## 5. The short-pair collapse: 39 pairs become 30 instances

A short reciprocal pair with representative `j` zeros anti-fold cells

```text
{j, 40-j}.
```

The representative `40-j` zeros the same unordered set.  Since endpoint
orientation is invisible, their entire anti-fold support problems are
identical.  The 18 surviving short representatives pair as

```text
(2,38), (4,36), (6,34), (8,32), (10,30),
(12,28), (14,26), (16,24), (18,22).
```

Hence

```text
21 long instances + 9 short instances = 30
```

distinct binary problems.

## 6. Exact encoding

The exploratory SAT encoder uses one Boolean variable for each available
support cell, with `true` meaning that the anti-fold entry is zeroed.
Equation (3) is an exact cardinality constraint.

For each lag `1,...,20`, every product of two retained anti-fold entries is
represented exactly.  The resulting signed weighted sum is constrained to
zero.  Products are linked to their two primary support literals by the
three-clause Boolean `AND` equivalence.  Negative weights are converted by

```text
-w*x = w*(not x) - w,
```

so the pseudo-Boolean encoder receives only positive weights.

The equation at lag 21 is omitted because it vanishes identically in a
real negacyclic norm.  The coefficients at lags `42-k` are the negatives of
those at `k`.

As a redundant Hensel layer, every integer equation is divided by its exact
coefficient gcd and reduced modulo two.  The resulting parity equations are
added as XOR chains.  An optional modulo-four one-hot chain is also
available.  Both are consequences of the integer equations; they do not
strengthen the mathematical problem.  On the closed index-0 instance the
modulo-four chain was slower, so the resumable census defaults to the
modulo-two layer only.

Every SAT output is accepted only after reconstructing the four physical
anti-fold rows and directly checking all 42 integer coefficients.  UNSAT
claims require the completed census and independent certificate checks.

For long `q` index 0, the support-only formula was independently reported
UNSAT more than once.  An initial PySAT proof capture was rejected by
independent replay and removed.  The replacement certificate uses the
canonical formula with the redundant modulo-four Hensel layer:

```text
CNF:       39,580 variables, 127,589 clauses
CNF SHA:   f3eb29b1ea9c386e53b03726349fe0c38577d7e187b56aa19f86412c8749755d
solve:     CaDiCaL, 200.17 seconds, 163.9 MB
proof:     binary DRAT, zstd-compressed, 90,490,737 bytes
proof SHA: efd8abd9d80d50365822754f36345f368d7cff8f2740ca33b9cab7d5866aa519
raw SHA:   7ab546776c7b0c199d524a952f51015a045c4aa7433b8eaa78d471e34129a374
check:     drat-trim VERIFIED, 75.00 seconds, 471.1 MB
core:      824,251 / 4,451,261 lemmas; 73,135,509 resolution steps; 0 RAT
```

The checked artifacts are
`output/antifold42_q0_proof/antifold_00.cnf` and
`output/antifold42_q0_proof/antifold_00.drat.zst`.  Because the modulo-four
layer is derived from the exact integer equations, its addition preserves
every support solution.  The verified UNSAT result therefore excludes the
entire index-0 support instance, not merely one root profile.

All nine canonical short instances have since been exhaustively excluded.
Their complete production certificate records
`3,710,853,316,608` modular join rows, `88,927,740` exact integer and
physical survivor replays, and zero exact supports; see
`eliahou_short_block_census/NINE_CASE_COMPLETION_CERTIFICATE.json`.

The next canonical long instance, `q` index 2, was solver-reported UNSAT in
1218.051 seconds (33,553 variables and 104,689 clauses).  This is a single
unproved observation.  Interrupted runs on other long instances yield no
mathematical information.  The historical
`ELIAHOU_ANTIFOLD42_CENSUS.json` ledger preserves formula hashes and
resumption commands, but its old short-case UNKNOWN statuses are superseded
by the exact nine-case certificate.

## Reproduction

The reduction itself uses only the Python standard library:

```sh
python3 verify_eliahou_antifold42.py
python3 -m unittest -v test_eliahou_antifold42.py
```

The exploratory support census additionally requires `python-sat`:

```sh
python search_eliahou_antifold_sat.py \
  --ignore-profiles --start 0 --stop 30 --modulus 42 \
  --time-limit 1800
```

The deterministic formulas can be listed without solving:

```sh
python search_eliahou_antifold_sat.py \
  --ignore-profiles --start 0 --stop 30 --list-instances
```

No exact `BS(84,83)` or Hadamard matrix is claimed here.
