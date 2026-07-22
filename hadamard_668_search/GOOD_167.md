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

## Exact CP-SAT model

`search_good_167_cp_sat.py` encodes:

1. 332 structural half-sequence bits (83 per sequence), with `A[1]=1`;
2. one of the two exact row-sum profiles;
3. 83 five-literal XORs from the product theorem; and
4. all 83 independent periodic-correlation equations.

For the last item, if a Boolean denotes whether a sign is negative, the cyclic
Hamming distance `d_X(k)` satisfies `PAF_X(k)=167-2*d_X(k)`.  Complementarity
is therefore the exact cardinality equation

```text
d_A(k)+d_B(k)+d_C(k)+d_D(k) = 334
```

at each lag `k=1,...,83`.  No floating-point Fourier test is used as a proof.

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
  --profile 0 --time-limit 3600 --workers 1 --max-memory-mb 2048 --fixed-search \
  --output output/good_167_profile_0.json

../tmp/hadamard-env/bin/python search_good_167_cp_sat.py \
  --profile 1 --time-limit 3600 --workers 1 --max-memory-mb 2048 --fixed-search \
  --output output/good_167_profile_1.json
```

If either returns a candidate:

```bash
python3 verify_good_167.py output/good_167_profile_0.json
```

Matched 20-second, one-worker runs on both order-167 profiles returned
`UNKNOWN`.  Automatic search made about 765,500 branches; the primary-only
fixed search made about 222,250 branches and 4,100 conflicts.  No candidate
was produced.  These are bounded feasibility runs, not exhaustive results.

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
