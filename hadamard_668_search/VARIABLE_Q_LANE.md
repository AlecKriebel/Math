# Variable-q special Golay lane: `BS(84,83)`

## Outcome

The obstruction for Eliahou's fixed `q` does not survive when both `s` and
`q` vary.  The joint problem is exactly the base-sequence problem

```text
BS(84,83).
```

This gives a concrete exact lane with 334 Boolean signs and 83 correlation
equations.  `variable_q_base.py` checks the equivalence, enumerates all
spectral margin cases, and provides the inverse map back to `(s,q)`.
`search_variable_q_cp_sat.py` implements the first exact sharded model.

This lane has not produced a solution yet.

## Exact equivalence

Let `h` be `+1` in coordinates `0,...,83` and `-1` in coordinates
`84,...,166`, so that `s'=h*s`.  For a lag `k`, the coefficient in the
summed aperiodic autocorrelation of

```text
(s, h*s, s*q, h*s*q)
```

is

```text
sum_i s_i*s_(i+k)
      (1+h_i*h_(i+k)) (1+q_i*q_(i+k)).
```

Cross-half terms vanish.  Define

```text
A = s[0:84],             |A|=84,
B = (s*q)[0:84],         |B|=84,
C = s[84:167],           |C|=83,
D = (s*q)[84:167],       |D|=83.
```

Then the special-quadruple correlation at lag `k` is twice

```text
R_k = c_k(A)+c_k(B)+c_k(C)+c_k(D).
```

For `k>=84` it vanishes automatically.  Hence the quadruple is Golay exactly
when

```text
R_k=0,  1 <= k <= 83,
```

which is the definition of `(A;B;C;D) in BS(84,83)`.  The map is bijective:

```text
s = A || C,
q = (A*B) || (C*D).
```

Thus a solver candidate has a direct, integer-only route to a special Golay
quadruple and the order-668 Goethals-Seidel matrix.

## Exact objective and Boolean constraints

For heuristic search, use the nonnegative integer objective

```text
E = sum_(k=1)^83 R_k^2.
```

It has no false zero: `E=0` is precisely the target.  L1 residual and the
number of nonzero lags are useful secondary objectives, but every reported
candidate must be ranked and verified using the exact `R_k` values.

For SAT/CP-SAT, encode each sign by a bit.  A product is `+1` iff its two bits
agree.  At lag `k`, the number of products is

```text
2*(84-k) + 2*max(83-k,0),
```

which is even.  The equation `R_k=0` therefore says exactly half of the
corresponding equality literals are true.  The prototype has 334 primary
bits, 13,778 correlation-product bits, and 83 exact-cardinality equations.

## Exhaustive spectral sharding

Evaluation of the base-sequence norm identity at `z=1` gives

```text
A(1)^2+B(1)^2+C(1)^2+D(1)^2 = 334.
```

The first two sums are even and the last two are odd.  Independent sequence
negations make the sums nonnegative; swapping the two sequences of each
length orders them.  There are exactly 12 canonical profiles:

```text
(4,2,17,5)    (6,0,17,3)    (8,6,15,3)
(10,0,15,3)   (10,4,13,7)   (10,8,11,7)
(10,8,13,1)   (12,10,9,3)   (14,4,11,1)
(14,8,7,5)    (16,2,7,5)    (18,0,3,1)
```

Evaluation at `z=-1` gives the same square equation for alternating sums.
Reversal makes the two even-length alternating sums nonnegative.  Coordinate
parity then leaves exactly 24 compatible alternating profiles for each
ordinary profile.  Therefore 288 nominal margin shards exhaust the search
after these sign, swap, and reversal normalizations.  The shard list is
generated, rather than hand-entered:

```sh
../tmp/hadamard-env/bin/python search_variable_q_cp_sat.py --list-shards
```

There is one further exact equivalence.  Multiplying every sequence coordinate
`i` by `(-1)^i` sends every residual to

```text
R_k -> (-1)^k R_k
```

and swaps the ordinary and alternating margins.  After restoring the canonical
sign, reversal, and equal-length ordering conventions, this global alternation
pairs 264 of the 288 nominal shards into 132 two-cycles and fixes 24 shards.
Thus there are 156 shard orbits.  The resume-safe scheduler searches one
representative from every orbit by default.  On a fixed shard, the CP model
retains only the lexicographically larger member of the internal alternation
pair.  Direct `--shard` runs and `--list-shards` still accept or display all
288 nominal indices.

Within each shard, the model also applies these safe symmetries:

- reverse either odd-length sequence and keep the lexicographically larger;
- reverse an even-length sequence when its alternating sum is zero;
- use negated reversal when an even-length sequence has ordinary sum zero;
- when both sums vanish, use the remaining independent negation to fix its
  first sign.

The model exposes redundant norm identities at primitive third, fourth, and
sixth roots of unity.  These are exactly the factor-28, factor-21, and
factor-14 periodic compression consequences in compact form and materially
improve propagation without excluding a solution.

There is also a sparse parity invariant.  At each positive lag, zero
correlation forces an odd number of the product terms to be negative, so the
product of all terms is `-1`.  Dividing the products at consecutive lags
telescopes to

```text
(a_k*a_(83-k)) (b_k*b_(83-k))
(c_k*c_(82-k)) (d_k*d_(82-k)) = -1,   k=0,
                                      +1,   1<=k<=82.
```

The standard base-sequence quad theorem gives an equivalent, sparser basis.
Define paired-endpoint products

```text
alpha_j = A_j A_(83-j) B_j B_(83-j),   0 <= j <= 41,
beta_j  = C_j C_(82-j) D_j D_(82-j),   0 <= j <= 40.
```

The same 83 parity consequences are exactly

```text
alpha = (-1,+1,...,+1),   beta = (+1,...,+1).
```

The default CP model uses these 83 four-literal XORs.  The command-line option
`--parity-basis endpoint` restores the original endpoint telescope, while
`--parity-basis both` exposes both redundant encodings.  These choices alter
propagation only; none is a stronger mathematical restriction.

## Relationship to the published modular seed

Mapping Eliahou's `(s,q)` to `(A,B,C,D)` gives ordinary sums

```text
(-2,0,3,-1)
```

and alternating sums

```text
(2,0,1,-3).
```

Both squared totals are 14, whereas an exact base sequence requires 334.
Its 13 nonzero base residuals are

```text
k:  4    8    12   16   26  30   34   38    42   46   50  54  58
R: -256  192 -128   64  -32  64  -96  128  -160  128  -96  64 -32
```

This explains why retaining the seed as a phase hint is reasonable but
retaining its row counts or its `q` is not.

## Completed periodic-compression reductions

Pad `C` and `D` by one trailing zero.  Exact aperiodic complementarity then
implies a periodic complementary quadruple of length 84.  The factor-14
compression to length six has been implemented as an exact four-sequence
two-pair signature join.  Exhaustive enumeration shows that all 288 nominal
margin shards survive.  Fourier inversion proves that its four PAF equations
are exactly the ordinary/alternating margins and the primitive-third- and
primitive-sixth-root constraints already exposed in the CP model.  It is a
useful independent regression but adds no mathematical pruning there.

The factor-12 compression to length seven is also implemented.  It is new
relative to the already exposed margin and small-root propagators because it
adds primitive-seventh-root information; like every periodic compression, it
is still a logical consequence of the full 83 exact base equations.  Twelve
explicit compressed PAF witnesses, one for each ordinary row-sum profile,
lift to every compatible alternating margin.  Thus all 288 nominal shards,
or 156 global-alternation orbits, survive this relaxation as well.  These are
compressed witnesses, not exact `BS(84,83)` sequences.

`search_variable_q_cp_sat.py --compression-7` exposes the four length-seven
PAF equations.  A short matched benchmark did not improve throughput, so the
flag remains optional.  The exact alphabets, witness tables, primitive-seven
PSD test, counts, and reproduction commands are in
`VARIABLE_Q_COMPRESSION.md`.

## Quad switching

Djokovic's base-sequence equivalence includes a norm-preserving transposition
of the short-pair quad labels 4 and 5.  In this implementation it negates
exactly those paired-endpoint quads of `(C,D)` and leaves the central column
fixed.  Its domain is deliberately checked: every short endpoint quad must
have product `+1`, which is the short part of the base-sequence quad parity
condition.  It must not be applied to an arbitrary near candidate that fails
that condition.

On its domain the transformation is an involution and preserves `N_C+N_D`
coefficient by coefficient, so keeping `A,B` fixed preserves the complete
base-residual vector.  `switch_variable_q_candidate.py` applies the switch and
restores the canonical margin conventions.  A switched copy of the current
parity-feasible checkpoint therefore has the same half-energy 232 and 43 bad
lags; a bounded continuation from it found no improvement.  This is a search-
basin diversification, not a construction or a local-optimality proof.

Primary source: D. Z. Djokovic,
[*Classification of base sequences BS(n+1,n)*](https://arxiv.org/abs/1002.1414),
International Journal of Combinatorics (2010), Article ID 851857.

## Reproduction and current state

```sh
cd hadamard_668_search
python3 variable_q_base.py
../tmp/hadamard-env/bin/python search_variable_q_cp_sat.py \
  --shard 0 --time-limit 60 --workers 1 --max-memory-mb 2048 --model-stats
```

The identity checker reports:

```text
PASS special/base identity; 12 profiles; 288 shards
```

The self-test also checks the 132 alternation pairs, 24 fixed shards, and 156
representatives.  The CP-SAT model validates cleanly.  No exact candidate has
been emitted.

The tracked parity-feasible checkpoint is
`output/variable_q_parity_best_canonical.json` in shard 213, with margins

```text
ordinary    = (14,4,11,1)
alternating = (14,8,5,7)
```

It has half-energy 232 and 43 nonzero lags.  The older shard-235 checkpoint is
its global-alternation partner and has the same residual quality.  Both fail
the independent exact verifier.

## Current search portfolio

Run all 156 global-alternation representatives through the resume-safe JSONL
scheduler.  Its default log and candidate files live under the repository's
ignored `tmp` directory:

```sh
../tmp/hadamard-env/bin/python run_variable_q_shards.py \
  --shards all --seed-count 2 --time-limit 300 --workers 1
```

Re-running the same command skips completed `(shard,seed_index)` attempts.
The length-seven compression is available as an optional exact propagator for
direct CP runs.  In parallel, the margin- and endpoint-parity-preserving local
engine can continue the shard-213 checkpoint or its quad-switched image.

`variable_q_parity_neighborhood.py` independently enumerates every endpoint-
parity-feasible, same-margin vector within six flips of that checkpoint.  At
Hamming distances 2, 4, and 6 it finds respectively 34, 3,646, and 159,558
distinct vectors, with minimum half-energies 272, 248, and 280.  Since the
checkpoint has half-energy 232, it is a strict local minimum in precisely this
bounded subspace.  No exact vector occurs there.  This does not cover eight
flips, another margin shard, or parity-infeasible intermediate states in an
escape path.  The complete method, checkpoint checksum, and regression tests
are in `VARIABLE_Q_PARITY_NEIGHBORHOOD.md`.

`--hint-distance R` adds an exact Hamming ball around a same-shard checkpoint.
For a genuine unquotiented neighborhood result it must be combined with
`--no-symmetry-breaking`:

```sh
../tmp/hadamard-env/bin/python search_variable_q_cp_sat.py \
  --shard 213 --hint output/variable_q_parity_best_canonical.json \
  --hint-distance R --no-symmetry-breaking --parity-basis both \
  --workers 1 --max-memory-mb 2048
```

Even an `INFEASIBLE` result from that model excludes only raw labeled
`(A,B,C,D)` vectors with the displayed shard-213 ordinary and alternating
margins and Hamming distance at most `R`.  It does not cover equally close
vectors with different margins, the shard-235 partner, or an unrestricted
334-sign neighborhood.  With symmetry breaking enabled, the bounded model
searches only the intersection of the ball with its lexicographic canonical
chamber; canonicalization can change distance from the hint, so that is not a
full-ball certificate.

The symmetry-off models at radii 4, 6, 8, 10, 12, 14, and 16 all returned
`INFEASIBLE`.  The largest run took 1,487.746 solver-seconds and 59,741,208
branches.  Therefore no exact base sequence with the displayed shard-213
margins lies within raw distance 16 of this checkpoint.  The frozen checksum,
complete solver statistics, reproduction command, and explicit exclusions
are recorded in `VARIABLE_Q_NEIGHBORHOOD.md`.

A distinct unsharded calculation starts from Eliahou's published base
quadruple rather than the shard-213 local checkpoint.  Exhaustive raw margin
images, an exact endpoint-quad dynamic program, and fixed-margin primitive-
3/4/6 root-table models exclude the complete raw Hamming ball through radius
17.  The radius-16 certificate contains 197 finite `INFEASIBLE` models, and
the exact distance-17 shell contains 276 more.  This result covers every
margin shard but only this bounded ball; its derivation, resource statistics,
and reproduction commands are in `VARIABLE_Q_SEED_DISTANCE.md`.

Every emitted candidate is checked through `base_to_special`, the exact
special-quadruple correlations, and the full Goethals-Seidel matrix.  The same
acceptance path is available independently:

```sh
python3 verify_variable_q.py output/variable_q_special_golay_167.json
```

The exact finish line remains unchanged.
