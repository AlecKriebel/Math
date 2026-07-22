# Circulant good matrices of order 167

This is a third, independent structured route to `H(668)`.  It does not fix
Eliahou's sequence `q`, and it is not the length-333 Legendre-pair model.

Status: active search; no circulant good quadruple of order 167 has been found.

## Exact equivalence

Let `A,B,C,D` be length-167 sign sequences.  Normalize

- `A[0]=1` and `A[-i]=-A[i]` (skew), and
- `B[0]=C[0]=D[0]=1` with `X[-i]=X[i]` for `X=B,C,D`
  (symmetric).

Their circulants are good matrices precisely when

```text
PAF_A(k) + PAF_B(k) + PAF_C(k) + PAF_D(k)
    = 668  if k=0,
    = 0    otherwise.
```

The Goethals-Seidel array then gives a skew Hadamard matrix of order 668.
The independent verifier checks the structural conditions, all periodic
correlations, the product theorem, and every row product of the resulting
`668 x 668` matrix.

## Arithmetic reduction at 167

Evaluation at the trivial character forces

```text
sum(B)^2 + sum(C)^2 + sum(D)^2 = 667.
```

Because a normalized symmetric sequence has row sum congruent to `167 mod 4`,
there are only two profiles, up to permuting `B,C,D`:

```text
(-21, -1, 15)
(-9, 15, 19)
```

Thus there is no three-square obstruction.

Bright, Djokovic, Kotsireas, and Ganesh proved the additional necessary
identity

```text
A[k] B[k] C[k] D[k] = -A[2k mod 167]   (k != 0).
```

The multiplicative order of 2 modulo 167 is 83.  Modulo the identification
`k ~ -k`, doubling therefore runs through all 83 independent positions in a
single cycle.  Once `B,C,D` and one entry of `A` are fixed, the theorem fixes
the other 82 independent entries of `A`.  The cycle-closing parity is already
implied by either of the two row-sum profiles.  Consequently the effective
Boolean dimension is 250 (the 249 independent entries of `B,C,D`, plus one
seed entry of `A`) before their three cardinality constraints.

The safe symmetry break `A[1]=1` removes that final seed bit: applying the
index automorphism `i -> -i` fixes the symmetric sequences and negates every
off-diagonal entry of `A`.

There is still an exact common-decimation quotient of order 83.  The classes
of nonzero multipliers modulo sign form one doubling cycle.  In each profile,
exactly one symmetric sequence has row sum 15 and hence half-weight 38.  Write
its negative-entry bits in doubling-cycle order and require that word to be
lexicographically maximal among all 83 cyclic rotations.  For any multiplier
class, choosing its sign according to the skew entry restores `A[1]=1`, while
the symmetric anchor sees the same rotation.  Thus this necklace leader
removes the full residual factor of 83 without losing a solution.

## Exact CP-SAT model

`search_good_167_cp_sat.py` encodes:

1. 332 structural half-sequence bits (83 per sequence), with `A[1]=1`;
2. one of the two exact row-sum profiles;
3. 83 five-literal XORs from the product theorem;
4. the exact common-decimation necklace leader; and
5. all 83 independent periodic-correlation equations.

For the last item, if a Boolean denotes whether a sign is negative, the cyclic
Hamming distance `d_X(k)` satisfies `PAF_X(k)=167-2*d_X(k)`.  Complementarity
is therefore the exact cardinality equation

```text
d_A(k)+d_B(k)+d_C(k)+d_D(k) = 334
```

at each lag `k=1,...,83`.  The implementation halves this layer exactly.  Pair
the directed edges `i -> i+k` under `i -> -i-k`.  A symmetric sequence has 83
doubled representative XORs and a fixed zero edge.  The skew sequence has 82
doubled representatives; its fixed edge and the exceptional pair incident
with zero contribute a constant two.  Dividing the complementarity equation
by two gives

```text
sum of the 82 + 3*83 representative XORs = 166.
```

This first reduces the PAF auxiliaries from 55,444 to 27,473.  Across all
lags, every unordered pair of half bits occurs exactly twice in each sequence.
The skew occurrences have opposite polarity; a symmetric sequence also has
one direct singleton per lag.  Caching one XOR for each unordered pair reduces
the auxiliaries again to `4*binom(83,2)=13,612`, with complemented occurrences
represented by negated cached literals.  Exhaustive order-7 assignments and
all order-167 descriptor multiplicities test this identity directly.  No
floating-point Fourier test is used as a proof.

The old uncached full directed-edge model had 55,777 variables and 55,614
constraints.  After both exact reductions, the half-edge model without the
necklace has 13,945 variables and 13,782 constraints.  With the exact 83-fold
necklace quotient enabled, the default model has 20,669 variables and 54,126
mostly Boolean-clause constraints.  The
lexicographic encoding was exhaustively truth-table tested through width four;
the edge reduction was checked directly at orders 7 and 167.

The model is deliberately parameterized by odd order and is regression-tested
at order 7, where it finds a quadruple that the independent exact checker
accepts.

Run the arithmetic, encoding, and small-order regression checks with:

```bash
python3 verify_good_167.py --self-test
../tmp/hadamard-env/bin/python -m unittest -v test_good_167.py
```

Run the two order-167 profiles separately:

```bash
../tmp/hadamard-env/bin/python search_good_167_cp_sat.py \
  --profile 0 --time-limit 3600 --workers 1 --max-memory-mb 256 \
  --output output/good_167_profile_0.json

../tmp/hadamard-env/bin/python search_good_167_cp_sat.py \
  --profile 1 --time-limit 3600 --workers 1 --max-memory-mb 256 \
  --output output/good_167_profile_1.json
```

The independently verified structured local checkpoints can also guide the
same exact model.  `--hint` first verifies the nonexact checkpoint, permutes
its symmetric sequences into the model's sorted row-sum order, and applies a
common doubling decimation so that both `A[1]=1` and the row-sum-15 necklace
leader hold.  It then hints exactly the 332 primary bits.  OR-Tools repairs
the infeasible hint for a bounded number of conflicts before resuming ordinary
exact feasibility search; it never fixes a hinted value or relaxes a PAF
equation:

```bash
../tmp/hadamard-env/bin/python search_good_167_cp_sat.py \
  --profile 0 --hint output/good_167_local_steepest_profile0.json \
  --hint-conflict-limit 1000 --time-limit 3600 --workers 1 \
  --max-memory-mb 256 --output output/good_167_hint_profile0_candidate.json
```

The profile-0 checkpoint canonicalizes with doubling shift 27 and multiplier
162; profile 1 uses shift 2 and multiplier 4.  Regression tests pin the four
resulting masks for each profile, preserve the complete residual multiset and
energy, check common-decimation orbit invariance, and confirm that the model
contains 332 distinct Boolean hints and no hinted auxiliaries.

Build or compare the exact encodings without searching:

```bash
../tmp/hadamard-env/bin/python search_good_167_cp_sat.py --build-only
../tmp/hadamard-env/bin/python search_good_167_cp_sat.py \
  --build-only --full-directed-edges --no-common-decimation-necklace
```

If either returns a candidate:

```bash
python3 verify_good_167.py output/good_167_profile_0.json
```

Matched 20-second, one-worker runs on both order-167 profiles returned
`UNKNOWN`.  Automatic search made about 765,500 branches; the primary-only
fixed search made about 222,250 branches and 4,100 conflicts.  No candidate
was produced.  These are bounded feasibility runs, not exhaustive results.

The reduced model was then run for 60 seconds per profile, sequentially, with
one worker and a 256 MiB solver cap.  Profile 0 (seed 1668) ended `UNKNOWN`
after 2,121,259 branches and 1,451 conflicts at 272.7 MB whole-process peak
RSS.  Profile 1 (seed 2668) ended `UNKNOWN` after 2,256,669 branches and 1,543
conflicts at 285.3 MB.  Both used zero swap.  These outcomes certify neither
infeasibility nor existence; they only show the stronger exact model remains
search-hard at this budget.

Matched 60-second repaired-hint runs were also executed sequentially.  Profile
0 ended `UNKNOWN` after 1,024,840 branches and 1,429 conflicts at 337.4 MB
whole-process peak RSS.  Profile 1 ended `UNKNOWN` after 1,572,158 branches and
1,241 conflicts at 339.0 MB.  Both used zero swap and emitted no candidate.
The extra peak is consistent with OR-Tools' temporary repair model; these are
again bounded search outcomes, not infeasibility certificates.

After unordered-pair caching, profile 0 was rerun from its energy-752 hint
with a 10,000-conflict repair allowance.  It ended `UNKNOWN` after 39,844
branches at 287.0 MB peak RSS; the repair/presolve phase extended solver wall
time to 77.591 seconds despite the nominal 60-second setting.  Profile 1 was
rerun from the improved energy-728 checkpoint with the 1,000-conflict setting
and ended `UNKNOWN` after 168,484 branches and 3,539 conflicts at 279.6 MB
peak RSS in 60.004 seconds.  Both used one worker and zero swap and emitted no
candidate.

## Stronger A,B -> GF(2) -> C,D reducer

There is a much sharper exact two-stage formulation.  Permute the three
symmetric sequences so that `sum(B)=15` (half-weight 38), possible in both
profiles.  Once skew `A` and symmetric `B` are fixed, define

```text
S[0] = 1,
S[i] = -A[i] A[2i] B[i]  for i != 0.
```

The product theorem forces `D=S*C`, and `S` is symmetric.  At lag `l`,

```text
PAF_C(l)+PAF_D(l)
  = 2 sum_{i : S[i]=S[i+l]} C[i]C[i+l]
  = -PAF_A(l)-PAF_B(l).
```

The involution `i -> -i-l` pairs the selected correlation edges and has one
fixed edge, whose C-product is `+1`.  Choose one representative from each
nonfixed pair.  Writing `C[j]=(-1)^X[j]`, reduction modulo four gives one
sparse linear equation over `GF(2)` at every lag.  `good_167_linear.py` builds
and row-reduces all 83 equations, imposes the exact C and D weights, and then
checks every survivor in the original integer PAF equations.  Thus the linear
stage is only a necessary filter; no construction is claimed before the exact
check passes.

Reproducible bounded scans are:

```bash
../tmp/hadamard-env/bin/python good_167_linear.py \
  --profile 0 --trials 1000 --random-seed 668
../tmp/hadamard-env/bin/python good_167_linear.py \
  --profile 1 --trials 1000 --random-seed 669
```

For all 2,000 sampled `(A,B)` pairs the linear system had rank 82.  It was
inconsistent for 505/1,000 and 473/1,000 pairs.  After the weight filters,
only 23 and 14 pairs respectively left a vector for the exact PAF check; none
was exact.  Rank is always at most 82: the negative-entry mask of `S` is a
known homogeneous null vector, because adding it swaps `C` with `D`.  The
claim that the rank is *exactly* 82 for all inputs remains empirical.  At rank
82 the two affine solutions are precisely the `C,D` swap pair, so distinct
target row sums retain at most one orientation.  The
reducer is independently regression-tested on a good quadruple of order 7,
where it recovers the correct `C,D` and verifies the resulting skew `H(28)`.

## Constant-memory streaming reducer

`search_good_167_stream.cpp` is a dependency-free, single-threaded C++20
implementation of the same exact filter.  It uses two 64-bit limbs for every
83-bit vector, fixed arrays for all equations, and streaming Gray-code affine
enumeration.  No table grows with the number of trials.  A built-in test
exhausts every normalized order-7 `(A,B)` pair and agrees with direct brute
force on all nine pairs that extend to good matrices.  Sixteen frozen
order-167 samples also give identical outcomes under the direct and factored
reducers.  ASan and UBSan passed the self-test and 10,000 order-167 trials.

The faster parameterization searches by the symmetric product quotient `S`
and `B`.  In negative-entry bits along the doubling cycle,

```text
a(2i) = 1 + s(i) + b(i) + a(i)  (mod 2).
```

Since doubling has order 83 modulo 167 and visits one member of every
`{i,-i}` pair, `A[1]=+1` makes this recurrence bijective precisely when the
half-weight of `S` is odd.  The exact `C,D` weights restrict that weight to

```text
profile 0: 5,7,...,77
profile 1: 7,9,...,81.
```

The doubling-cycle word of `S` is made lexicographically maximal among its 83
rotations, giving the exact common-decimation quotient.  For fixed `S`, the
83 GF(2) coefficient rows are fixed too.  The engine carries an 83-bit row
transform through Gauss-Jordan elimination and reuses that factorization for
256 independently sampled fixed-weight `B` masks.  Only the right-hand side,
weight tests, and exact integer PAF check change.  High-nullity systems are
reported as deferred if their affine space exceeds the explicit cap; they are
never counted as rejections.

Compile, self-test, and run one profile at a time:

```bash
clang++ -std=c++20 -O3 -Wall -Wextra -Wpedantic -Werror \
  search_good_167_stream.cpp -o ../tmp/search_good_167_stream
../tmp/search_good_167_stream --self-test

../tmp/search_good_167_stream --parameterization sb --profile 0 \
  --seconds 60 --trials 0 --inner-batch 256 --random-seed 5668 \
  --checkpoint output/good_167_stream_sb_profile0_60s.json \
  --output output/good_167_sb_profile0_candidate.json
```

Every saved near-miss is independently replayed by Python:

```bash
../tmp/hadamard-env/bin/python verify_good_167_stream.py \
  output/good_167_stream_sb_profile0_60s.json
```

The direct and factored 60-second shards produced:

| parameterization | profile | samples | exact-PAF stage | best energy | bad lags | max quarter residual |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `(A,B)` | 0 | 442,374 | 6,494 | 3,200 | 66 | 16 |
| `(A,B)` | 1 | 441,506 | 7,157 | 3,296 | 55 | 16 |
| `(S,B)`, factored | 0 | 2,890,277 | 36,143 | 2,752 | 60 | 12 |
| `(S,B)`, factored | 1 | 2,871,527 | 49,035 | 3,264 | 59 | 16 |

The factored runs sustained about 48,000 samples/second.  Whole-process peak
RSS was 1.44 MB or less and every measured run used zero swap.  All non-early
systems in these shards had rank 82; that remains an observation, not a
theorem.  No exact candidate was found.  The checkpoint verifier recomputes
the product quotient, GF(2) equations and rank, exact weights, product theorem,
all 83 PAF residuals, and the saved RNG transition.  Candidate and checkpoint
writes use checked close and atomic replacement.

## Connected structured local search

The same executable also has a complete connected local parameterization by
fixed-weight masks `B,C,D`, with `S=C xor D`.  Their half-weights are

```text
profile 0: (38,42,47)
profile 1: (38,44,37).
```

Consequently `S` always has odd weight, the doubling recurrence recovers the
unique normalized `A`, and the product theorem and every row sum hold after
every move.  Three atomic exchanges change one of `B,C,D`; their Johnson
graphs make the state space connected.  Three coupled exchanges change
`B,C`, `B,D`, or `C,D` together while keeping `A` fixed.  Every proposal is
checked by direct integer PAF recomputation.  Optional compound proposals
compose several valid moves before acceptance, and a shadow penalty can favor
the exact mod-16 correlation surface without treating it as sufficient.

Run annealing from a verified reducer checkpoint, then exhaust its complete
two-coordinate neighborhood:

```bash
../tmp/search_good_167_stream --parameterization local --profile 0 \
  --seconds 60 --trials 0 --moves-per-restart 10000 \
  --start-temperature 256 --end-temperature 0.25 \
  --initial output/good_167_stream_sb_profile0_60s.json \
  --checkpoint output/good_167_local_profile0_60s.json

../tmp/search_good_167_stream --parameterization local --profile 0 \
  --steepest-polish --initial output/good_167_local_profile0_60s.json \
  --checkpoint output/good_167_local_steepest_profile0.json

../tmp/search_good_167_stream --parameterization local --profile 1 \
  --triangle-polish --initial output/good_167_local_steepest_profile1.json \
  --checkpoint output/good_167_local_triangle_profile1.json

../tmp/hadamard-env/bin/python verify_good_167_local.py \
  output/good_167_local_steepest_profile0.json
```

The local verifier requires a versioned `near_miss`, checks canonical 83-bit
masks, exact weights, `S=C xor D`, the `S,B -> A` recurrence, product theorem,
all 166 nonzero PAF lags and reflection, and every recorded metric.  Its
success banner deliberately reads `VERIFIED NONEXACT CHECKPOINT — NOT H(668)`;
zero energy is rejected and routed to the full `668x668` exact verifier.

Starting from the factored checkpoints, profile 0 reached energy 808 in
1,659,072 moves and then 752 in a cold reheat.  Profile 1 reached energy 752
in 1,657,915 moves.  Complete steepest scans evaluated 7,742 and 7,682 valid
atomic/coupled neighbors and found no strict improvement.

`--triangle-polish` extends the exact descent by choosing three half-indices,
leaving a different one of `B,C,D` unchanged at each, and toggling the other
two.  Each of the six assignments preserves all three weights and fixes
`B xor C xor D`, hence fixes `A`.  Alternating complete pair and triangle
scans left profile 0 at energy 752 after 77,144 evaluations.  Profile 1 fell
to energy 728 after 73,261 evaluations and stopped after a complete second
round totaling 155,008 evaluations.  The new checkpoint has 58 bad lags,
maximum absolute quarter residual 6, and passes the strict nonexact verifier.
The profile-1 run took 5.60 seconds at 1.47 MB RSS with zero swap.  These are
local minima for the pair-plus-triangle union, not a global lower bound.  Hot
restarts, sampled compound moves, and shadow objectives remain bounded
heuristics and produced no exact state.

Separately, exact GF-surface scans evaluated all 5,113 one-exchange `B` and
two-toggle `S` neighbors of each factored incumbent.  Only 64 and 65 states,
including the centers, survived exact recovery; none improved energies 2,752
and 3,264.  Thus those centers are local minima on this defined GF
neighborhood too.  Production local runs used at most 1.49 MB RSS and zero
swap; the sanitized 10,000-move run used 17.9 MB and reached verified energy
976.  No exact candidate was found.

## Assessment and limitation

This lane is worth pursuing because the product theorem makes it much smaller
than unrestricted cyclic supplementary difference sets.  It also targets a
skew `H(668)`, a stronger outcome than required.

The decisive limitation is that 167 is prime.  The compression stage that
made the published SAT+CAS searches practical for composite orders has no
nontrivial analogue here.  The 2019 exhaustive computation only reached odd
orders through 69 (for the divisible-by-three cases); the literature found in
this audit contains neither a good quadruple of order 167 nor a nonexistence
proof.  A short `UNKNOWN` CP-SAT run is therefore evidence only about search
difficulty, never about nonexistence.

## Williamson and unrestricted cyclic-SDS audit

The same trivial-character equation for four unrestricted cyclic blocks has
ten positive row-sum profiles, hence ten canonical GS parameter sets.  The
script

```bash
python3 analyze_sds_167.py
```

enumerates them and checks the SDS identity

```text
sum_i k_i(k_i-1) = lambda * 166,   lambda = sum_i k_i - 167.
```

Requiring all four blocks to be symmetric gives the Williamson subfamily.
After setting all four initial signs to `+1`, the sign of each row sum is
forced modulo four.  Williamson's odd-order product theorem says that each
independent coordinate has either one or three negative entries.  All ten
profiles pass the resulting parity/count test, so this produces no arithmetic
nonexistence proof.  An exact Williamson SAT model would have 332 half-signs,
83 product XORs (eliminating one whole sequence), 83 PAF equations, and ten
row-sum shards.  This is viable but less focused than the good-matrix model's
two shards.

There is, however, a rigorous dead end for the standard common-multiplier
orbit search.  Since `167-1 = 2*83`, the only useful proper multiplier-subgroup
orders are 2 and 83.  For a subgroup of order 83, every nonzero orbit has size
83 and `{0}` is the only singleton, so every block size must be `0` or `1`
modulo 83.  None of the ten GS parameter sets passes this test.  The remaining
order-2 subgroup is `{+1,-1}` and merely imposes symmetric blocks - precisely
the Williamson-style restriction already discussed.  Thus there is no
medium-sized orbit compression for cyclic SDS at this prime.

## Primary sources

- C. Bright, D. Z. Djokovic, I. Kotsireas, V. Ganesh,
  [*A SAT+CAS Approach to Finding Good Matrices: New Examples and
  Counterexamples*](https://arxiv.org/abs/1811.05094), AAAI 2019.  Theorem 7
  is the product identity; Section 4 describes their compression/SAT method.
- H. Kharaghani, A. Mohammadian, B. Tayfeh-Rezaie,
  [*A Search for Hadamard Matrices of Williamson Type*](https://arxiv.org/abs/2605.08661),
  2026.  Its near-Williamson search supplies the mod-four linearization
  pattern adapted here to the good-matrix product quotient `D=S*C`.
- D. Z. Djokovic, I. S. Kotsireas,
  [*Goethals-Seidel Difference Families with Symmetric or Skew Base
  Blocks*](https://doi.org/10.1007/s11786-018-0381-1), Mathematics in
  Computer Science 12 (2018), 373-388.
- D. Z. Djokovic, O. Golubitsky, I. S. Kotsireas,
  [*Some New Orders of Hadamard and Skew-Hadamard Matrices*](https://arxiv.org/abs/1301.3671),
  Journal of Combinatorial Designs 22 (2014), 270-277.  This gives the cyclic
  SDS matching framework and records 167 among the unresolved base orders.
