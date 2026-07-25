# Exact orientation cascade for Eliahou long cases 1--20

## Scope and claim boundary

This directory contains two new exact reductions of the open
distance-41 long cases and a bounded diagnostic.  It does **not** exclude a
long case, construct `BS(84,83)`, or construct `H(668)`.

The main reduction replaces the raw `2^39` endpoint-orientation layer over a
fixed anti-fold support by:

1. a fixed binary linear system for divisibility by 16 and root parity;
2. four exact group-cardinality equations for the roots;
3. 21 exact quadratic Boolean equations for divisibility by 32.

The reduction applies separately to every exact-weight, root-feasible support.
The deterministic 200-support audit below is evidence about the resulting
fiber sizes, not a census of any case.

## 1. The positive fold modulo 8 is redundant

Fix one of long cases 1--20.  For an eligible cell `i`, let `delta_i` be the
two-row positive-fold change produced by choosing its lower endpoint.  The
upper endpoint produces `-delta_i`.  For cyclic lag `k`, expand

```text
C_k = sum_r <B_r + sum_i s_i delta_(i,r),
                   T^k(B_r + sum_i s_i delta_(i,r))>,
```

where `s_i` is `+1` or `-1`.

The verifier computes every constant, singleton, and pair coefficient over
the integers.  For all 20 cases it proves:

- every positive-fold correlation is divisible by 4 for every support;
- `C_k/4 mod 2` is independent of all endpoint orientations;
- the support-only digit `C_k/4 mod 2` is affine (its raw quadratic part is
  zero);
- restricted to the 57-dimensional anti-fold mod-2 affine code, all 21
  digits vanish identically.

Thus every anti-fold mod-2 support automatically satisfies the positive-fold
equations modulo 8, in either endpoint orientation.  This initially looked
like an extra obstruction; the exact restriction audit shows that it is
instead a linear consequence of the existing characteristic-two layer.

## 2. A fixed 23 by 78 orientation matrix at modulo 16

The stronger integer coefficient audit proves that every interaction

```text
<delta_i,T^k delta_j> + <delta_j,T^k delta_i>
```

is divisible by 8.  Consequently, after a support `S` has passed anti-fold
modulo 2, the next positive-fold digit is affine in the upper-endpoint bits
and its column for cell `i` is independent of the other 38 selected cells.

For each case there is therefore a fixed `23 x 78` binary matrix `M`:

- rows 1--21 are `C_k/8 mod 2`, `1 <= k <= 21`;
- rows 22--23 are the long- and short-block root-orientation parities.

A support merely selects the 39 columns `M_S`; its lower-orientation
positive-fold values and chosen root profile determine the right-hand side:

```text
M_S e = b_S  over F_2.                                (1)
```

In a typical sampled support, (1) has rank 22 and leaves 17 free orientation
bits.  This is an exact factor-`2^22` contraction relative to the raw
`2^39` endpoint layer.  No universal lower bound on `rank(M_S)` is claimed.

## 3. Exact roots are four cardinality equations

Let

```text
a_j = -seed_j
```

be the lower-orientation signed root contribution at selected cell `j`, and
let `e_j=1` choose the upper endpoint.  Put

```text
n_j = e_j xor [a_j=-1].
```

For each block/parity group `G` and its signed target `t_G`,

```text
sum_(j in G) a_j (-1)^e_j = |G| - 2 wt(n restricted to G).
```

Hence the exact ordinary and alternating root values are equivalent to the
four integer conditions

```text
wt(n restricted to G) = (|G|-t_G)/2.                 (2)
```

The verifier enumerates an affine solution basis of (1) in Gray-code order
and checks (2) with four masked population counts.  It also replays every
orientation which survives the next modular digit using the original root
sums.

## 4. The modulo-32 layer is exactly quadratic

Parameterize a consistent solution fiber of (1) by `d` free bits `u`.  An
orientation flip changes a fold coefficient by a multiple of four.  After
division by 16 and reduction modulo 2, terms of degree three and above
vanish.  Therefore the next 21 equations have exact quadratic ANFs:

```text
q_k(u) = 0 over F_2,       1 <= k <= 21.              (3)
```

The verifier interpolates every constant, linear, and quadratic coefficient,
checks 64 deterministic higher-weight points by direct physical replay, and
then evaluates all `2^d` points with bit-packed truth tables.

The individual polar forms have low rank, but they do not share a useful
large radical: in the 195 consistent pinned fixtures, the common radical has
dimension zero in 168, one in 25, and two in two.  Thus this sample does not
support a global common-polar decomposition.

## 5. Pinned 200-support observation

The certificate takes five deterministic exact-weight, profile-feasible
supports for each of 20 cases and two profiles, for 200 distinct supports.
All arithmetic reductions and every accepted point are replayed exactly.

Observed counts:

```text
mod-16 inconsistent supports                         5 / 200
consistent rank 22 / nullity 17                    187
consistent rank 21 / nullity 18                      8

orientation points in consistent mod-16 fibers       26,607,616
points also satisfying all four exact root counts        121,764

supports with zero mod-32 orientations              179 / 200
total mod-32 orientations across all supports                22
mod-32 orientations also satisfying exact roots               1
those also satisfying the positive fold modulo 64              0
```

The single root-exact modulo-32 point was in case 5 (`q=35`), profile 0,
and failed at modulo 64.  Consequently all 200 pinned fixtures are excluded
by this bounded cascade.  This is **not** an exclusion of any complete case:
the support spaces are enormous, and no statistical extrapolation is used.

The typical exact orientation cost after a support is supplied is now about
`2^17` truth-table points rather than `2^39`.  The unresolved bottleneck is
global support enumeration or a support-level theorem, not endpoint
orientation inside one support.

The existing exact MacWilliams count for case 1 before root-profile
conditioning is

```text
25,953,942,447,362,002 anti-mod2 supports.
```

The pinned Python cascade took about 0.47 seconds per supplied support.  A
literal support-first pass at that rate would take roughly 390 million
single-core years.  Even a hypothetical implementation sustaining one
million complete supports per second would need about 823 years for this one
support layer.  The `2^22` orientation contraction is therefore meaningful
algebra, but it does not make support-first enumeration viable; the next
method must couple support and orientation or prove a global support
obstruction.

## 6. A sparse-generation theorem for the anti-fold code

The verifier also constructs exact low-weight generators of the homogeneous
anti-fold characteristic-two code.

- In every case, the 57-dimensional code is generated by codewords of weight
  at most 6.
- In cases 6 and 14, weight at most 4 already generates all 57 dimensions.
- After adjoining the four block/parity checks, the resulting
  profile-conditioned homogeneous code has dimension 55 and is generated by
  weight at most 6 in every case.

This gives a rigorous connected local-move system for each affine support
space.  It has not yet produced a decisive global enumeration.

## 7. What the two 42-fold norms do—and do not—prove

The positive and anti folds at the same 42 split do **not** reconstruct the
full aperiodic norm.  If `R_k` are the summed aperiodic correlations, their
sum and difference recover only the cyclic residue modulo `z^84-1`:

```text
R_42 = 0,
R_k + R_(84-k) = 0,       1 <= k <= 41.              (4)
```

For example, the integral binary-parity-compatible residual
`R_1=2, R_83=-2` is invisible to both 42-fold norms and to the
ordinary/alternating norm evaluations.  Exact `BS(84,83)` equivalence needs
the other adjacent cyclic fold (the mod-83 and mod-84 adjacent-fold theorem),
or one equation from each cancellation pair.  A convenient causal half is

```text
R_43 = R_44 = ... = R_83 = 0,
```

which adds 41 equations and reconstructs every omitted coefficient.

`search_joint_ternary_cp_sat.py` therefore has two clearly separated modes:

- `--cyclic-only` is the strong necessary joint plus/anti propagator;
- the default additionally imposes all 83 original aperiodic equations and
  is an exact construction diagnostic.

Each eligible cell is one lower/upper/none trit, represented by two mutually
exclusive Booleans.  All physical sign products are expanded once and shared
by the root equations, anti-fold parity layer, cyclic images, and aperiodic
equations.  The case-1 model has 156 primary Booleans and 5,928 shared
quadratic products.  It is deliberately run with one worker and at most
6 GB RAM.  `UNKNOWN` and uncertified solver `INFEASIBLE` make no theorem.
Any assignment is reconstructed as four original rows and replayed through
all correlations.

## 8. Independent red-team agreement

The separate
`../eliahou_long_orientation_redteam/README.md` audit imports none of the
orientation-cascade code here.  It independently proves the all-case modulo-8
redundancy, derives the modulo-16 and modulo-32 orientation layers, and
replays the pinned case-5 root-exact modulo-32 point and its modulo-64
failure.

Its different deterministic 200-support control found:

```text
mod-16 inconsistent supports                   5
mod-16 exact-root points                 120,455
mod-32 survivors                              24
mod-32 survivors with exact roots              0
```

The close scale, followed by a different final intersection count, is what
one should expect from bounded controls; neither sample is promoted to a
frequency theorem.

The red-team also verifies an exact ternary formulation

```text
t_j in {-1,0,1},       u_j=t_j^2,
sum u_j = 39,
20 anti-fold equations in u,
21 plus-fold equations in t,
41 causal aperiodic equations.
```

For every long case this and the direct aperiodic system use the same 5,928
quadratic products, split equally into 1,482 each of `uu`, `ut`, `tu`, and
`tt`.  The causal equations alone touch all 5,928.  Thus the joint model is
an exact and clean representation, but there is no hidden product-inventory
collapse; the remaining advance must be mathematical rather than merely
changing the solver syntax.

## Reproduction

Quick exact audit (all 20 algebraic cases plus one orientation fixture):

```sh
PYTHONDONTWRITEBYTECODE=1 \
  /Users/alec/Documents/tmp/hadamard-env/bin/python \
  audit_orientation_cascade.py
```

Regenerate the pinned 200-support certificate (about 95 seconds and 111 MB
RSS on the 16 GB M1 Pro):

```sh
PYTHONDONTWRITEBYTECODE=1 \
  /Users/alec/Documents/tmp/hadamard-env/bin/python \
  verify_sample5_certificate.py
```

Bounded one-worker cyclic gate and exact construction diagnostic:

```sh
/Users/alec/Documents/tmp/hadamard-env/bin/python \
  search_joint_ternary_cp_sat.py \
  --case 1 --profile 0 --cyclic-only --time-limit 60

/Users/alec/Documents/tmp/hadamard-env/bin/python \
  search_joint_ternary_cp_sat.py \
  --case 1 --profile 0 --time-limit 60
```

The certificate is deterministic.  Its expected semantic hashes and compact
counts are pinned in `EXPECTED_SAMPLE5_SUMMARY.json`.

Independent exact ternary and pinned-survivor replays:

```sh
PYTHONDONTWRITEBYTECODE=1 \
  /Users/alec/Documents/tmp/hadamard-env/bin/python \
  ../eliahou_long_orientation_redteam/audit_exact_ternary_model.py

PYTHONDONTWRITEBYTECODE=1 \
  /Users/alec/Documents/tmp/hadamard-env/bin/python \
  ../eliahou_long_orientation_redteam/verify_pinned_root_survivor.py
```
