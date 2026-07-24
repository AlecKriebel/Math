# Round 8: 41-vector unit-norm tight-frame construction challenge

## Status

No 41-point kissing configuration was found.  This package records:

1. an exact exhaustive rejection of all cyclic real harmonic \(41\times5\)
   UNTFs, including every arbitrary choice of row signs;
2. an exact obstruction to partitioning the 40 oriented \(D_5\) roots into
   eight orthonormal bases;
3. a numerical search over the exact seven-bases-plus-simplex UNTF family;
4. a numerical search on the general equal-norm Stiefel/UNTF intersection.

The numerical failures are construction evidence only and do not imply
nonexistence.

## Exact cyclic exhaustion

For \(1\leq a<b\leq20\), define
\[
x_j=\frac1{\sqrt5}\left(
1,\sqrt2\cos\frac{2\pi aj}{41},\sqrt2\sin\frac{2\pi aj}{41},
\sqrt2\cos\frac{2\pi bj}{41},\sqrt2\sin\frac{2\pi bj}{41}
\right).
\]
Discrete character orthogonality proves exactly that all 41 rows have norm
one and
\[
\sum_jx_jx_j^{\mathsf T}=\frac{41}{5}I_5.
\]
For difference \(r\ne0\),
\[
\langle x_0,x_r\rangle
=\frac{1+2\cos(2\pi ar/41)+2\cos(2\pi br/41)}5.
\]

The checker exhausts all \(\binom{20}{2}=190\) frequency pairs and the 20
nonzero difference classes.  Directed rational Machin bounds for \(\pi\)
and alternating Taylor bounds for cosine enclose every value exactly.
No pair has maximum inner product at most \(1/2\).

This exhaustion also covers arbitrary row sign flips, which preserve the
UNTF equations.  For every frequency pair the certificate records a nonzero
difference \(r\) whose exact lower interval endpoint satisfies
\(h_r=\langle x_j,x_{j+r}\rangle>1/2\).  If signed rows
\(y_j=s_jx_j\), \(s_j\in\{\pm1\}\), obeyed the kissing constraint, then
\(s_{j+r}=-s_j\) for every \(j\).  Because 41 is prime and \(r\ne0\), adding
\(r\) cycles through all 41 indices.  Iterating the relation around this odd
cycle yields \(s_j=(-1)^{41}s_j=-s_j\), a contradiction.  The verifier
reconstructs this exact odd-cycle witness for each of the 190 frequency
pairs.

The global minimax value is enclosed in an interval of width below
\(9.71\times10^{-31}\), centered at
\[
0.8153803817470019.
\]
It is attained by the ten-pair multiplicative orbit
\[
(1,9),(2,18),(3,14),(4,5),(6,13),(7,19),(8,10),
(11,17),(12,15),(16,20).
\]
The exact lower endpoint exceeds \(1/2\) by more than \(0.315\).

## Exact \(D_5\) basis obstruction

Write each normalized oriented \(D_5\) root as \(r/\sqrt2\), where
\(r\in\mathbb Z^5\) has two entries in \(\{\pm1\}\).  If five such roots
formed an orthonormal basis and \(A\) were their integer row matrix, then
\[
AA^{\mathsf T}=2I_5,\qquad \det(A)^2=2^5=32.
\]
This is impossible because \(\det(A)\) is an integer and 32 is not a square.
An explicit orthogonal four-set exists, so the maximum orthogonal subset has
size exactly four.  In particular, the 40 roots cannot be partitioned into
eight orthonormal bases, and the proposed "delete one \(D_5\) basis and add
a rotated simplex" subfamily is empty.

## Seven bases plus a simplex

The union of seven orthonormal bases and a regular 5-simplex is automatically
a 41-vector UNTF:
\[
7I_5+\frac65I_5=\frac{41}{5}I_5.
\]
After fixing one basis by global rotation, the search optimizes seven
independent orthogonal matrices (six more bases and the simplex orientation)
using smooth maximum continuation on a product of orthogonal groups.
Across 24 deterministic asymmetric starts, the best maximum inner product
was
\[
0.5846767619542745.
\]
Its maximum row-norm residual is below \(8\times10^{-15}\), and its tight
frame Frobenius residual is below \(4\times10^{-14}\).

## General numerical UNTF search

The general search retracts asymmetric random perturbations to the
intersection of:

- unit row norms; and
- \(X^{\mathsf T}X=(41/5)I_5\).

It uses alternating exact-in-floating-point row normalization and spectral
frame whitening, with log-sum-exp continuation.  There were 24 asymmetric
random starts plus the best structured union start.  Deterministic
high-temperature polishing produced
\[
\max_{i\ne j}\langle x_i,x_j\rangle
=0.5262002628454413.
\]
The final maximum unit-norm residual is
\(1.12\times10^{-15}\), and the tight-frame Frobenius residual is
\(1.39\times10^{-14}\).  Since the maximum remains above \(1/2\), these
coordinates are not a kissing configuration.

Two additional seed families were tested.  Eighteen \(D_5\)-plus-one starts
(the five coordinate axes, the all-ones direction, and twelve asymmetric
random directions) converged to best maximum
\[
0.527354165981281.
\]
Projecting the inherited unconstrained 41-point near-miss, whose original
maximum is \(0.514994652512167\), onto the UNTF intersection raised its
maximum to \(0.5686432660\); continuation and polishing ended at
\(0.5509551849\).  Thus its unusually good spherical-code geometry does not
survive the tight-frame constraint in this search.

## Reproduction

From this directory:

```sh
python3 search_cyclic_frames.py
python3 checker.py
python3 d5_basis_checker.py

../../.venv/bin/python optimize_untf.py \
  --seed 528041 --union-starts 24 --general-starts 24 \
  --iterations 150 --output results/untf_optimization.json
../../.venv/bin/python polish_untf_result.py
../../.venv/bin/python seeded_untf_challenges.py

../../.venv/bin/python check_results.py
../../.venv/bin/python -m unittest test_results -v
```

The final checker recomputes every cyclic rational interval, the \(D_5\)
determinant obstruction, every coordinate norm, both frame operators, the
structured group Gram matrices, and both reported maximum inner products.
It also includes a coordinate-tampering test.

Artifact SHA-256 values:

- `results/cyclic_exhaustive.json`:
  `ae963e6607f16addfd972849b8742e99169343b466af18f82bff57311c8354d4`;
- `results/untf_optimization.json`:
  `2b3424dfa9bf6381c4eb97ccf651d43937679e6f690340e4b923d691c2618980`;
- `results/seeded_untf_challenges.json`:
  `02a8f8e669ffecbb28f7f6af71f0c6db591f00ffa658c9b4779d4a43f0cb63c1`;
- best structured coordinate payload:
  `4593da1b16723978f6c13628889805ce8f31d3803bea036ca40060df555a79df`;
- best general coordinate payload:
  `cee888482c239a9ff6b55e48dd09ddce53d870ff36cd68ba2855d6d749a70054`;
- best seeded coordinate payload:
  `b72205fb72c820b1e32fb6c4174787d80cb5924aac94813ba93304a914df7ca7`.
