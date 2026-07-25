# Independent adversarial audit of the degree-11 cap certificate

## Verdict

No mathematical or certificate flaw was found.  The exact payload in
`certificates/one_sided_cap_degree11_bound.json` proves
\[
B(5)\leq 34.
\]

This audit was performed independently of the numerical SDP output.  The
self-contained test
`tests/test_one_sided_cap_degree11_independent_audit.py` imports neither
the degree-10 verifier nor the degree-11 verifier.  It reconstructs the
rational polynomial, diagonal subdivision, and complete three-variable
Bernstein tree directly from the degree-11 JSON file.

## Kernel normalization

Put
\[
a=(1-u^2)^{1/2},\quad b=(1-v^2)^{1/2},\quad
z=\frac{t-uv}{ab}.
\]
For \(a,b\ne0\), recurrence (3) in the proof gives exactly
\[
Q_k(u,v,t)=(ab)^kP_k^{(4)}(z).
\]
Indeed the normalized \(S^3\) zonal recurrence is
\[
(k+1)P_k^{(4)}(z)
=2kzP_{k-1}^{(4)}(z)-(k-1)P_{k-2}^{(4)}(z),
\]
and multiplication by \((ab)^k\) produces the displayed recurrence for
\(Q_k\).  Both sides are polynomials, so the identity extends to \(a=0\)
or \(b=0\).

The homogeneous-harmonic addition formula on \(\mathbb R^4\) therefore
writes \(Q_k\) as a positive constant times
\(\sum_aH_{k,a}(r_x)H_{k,a}(r_y)\).  Multiplying these features by *any*
real height functions preserves positivity of their ordered Gram sum.
Consequently the chosen
\[
p_k(u)=(P_0^{(5+2k)}(u),\ldots,P_{11-k}^{(5+2k)}(u))
\]
requires no additional positive constants.  The pole cases are included:
homogeneous harmonics of positive degree and the polynomial \(Q_k\) both
vanish there as required.

For a symmetric block \(F_k\), contracting with the symmetrized matrix
uses coefficient
\[
(F_k)_{ij}\bigl(p_i(u)p_j(v)+p_j(u)p_i(v)\bigr)
\]
for \(i<j\).  The independent reconstruction uses exactly this factor,
so there is no lost factor of two.

## Exact PSD and arithmetic

Each stored block is reconstructed as
\[
F_k=\frac{A_kA_k^{\mathsf T}}{10^{18}}.
\]
This is an identity over the rationals, not a numerical eigenvalue test.
The independently reconstructed factor payload has SHA-256
`723d5521951ce45d236116016a69e7e8e510b8e7ba1f0338f7c1d6fffe507257`.
The floating discovery scale, source eigenvalues, and entry-change
diagnostics are never used.

The diagonal and off-diagonal targets give
\[
1+\frac{1647/50}{969/1000}
=\frac{11303}{323}
=35-\frac2{323}<35.
\]
Thus the strict separation from 35 is exact; no decimal rounding is
involved.

## Closed domain and Bernstein coverage

The matrix
\[
\begin{pmatrix}
1&u&v\\u&1&t\\v&t&1
\end{pmatrix}
\]
has all one- and two-dimensional principal minors nonnegative when
\(0\leq u,v\leq1\) and \(-1\leq t\leq1/2\).  Adding
\(\Delta=1+2uvt-u^2-v^2-t^2\geq0\) therefore makes it PSD.  Conversely,
every geometric triple has these properties.  Its rank is at most three,
so every matrix in the stated domain is realizable already in
\(\mathbb R^3\subset\mathbb R^5\).  Hence the audited domain loses no
five-dimensional pair.

After the exact map \(t=-1+3s/2\), the independent audit reconstructed
degree-11 tensor Bernstein coefficients for both
\[
H=-969/1000-F
\quad\text{and}\quad\Delta.
\]
It rebuilt the cyclic \(u,v,s\) midpoint tree from the root rather than
reading a leaf list.  Its results were:

```text
total leaves                 5995
determinant-infeasible       2848
proved H >= 0                3147
maximum depth                  31
ordered leaf digest
3ffd08afa66bcd12e52399e392c09fda237f8bab18fc1af9a8090e76f1f81f65
```

The infeasibility sign is in the safe direction: a box is discarded only
when the *maximum* Bernstein coefficient of \(\Delta\) is strictly
negative.  A zero maximum is not pruned.  A feasible box is accepted only
when the *minimum* Bernstein coefficient of \(H\) is nonnegative.  Exact
de Casteljau children are closed and cover their parent, including their
shared face.  Thus \(\Delta=0\), \(t=1/2\), and all coordinate faces remain
covered.

The independent diagonal reconstruction terminates in three closed
intervals at maximum depth two and proves
\(1647/50-F(u,u,1)\geq0\) for all \(0\leq u\leq1\).

## Targeted adversarial checks

The independent exact test additionally checks:

- \(u,v=0\) and \(u=1\) pole faces;
- \(t=1/2\) contact points;
- determinant-zero triples, including
  \((u,v,t)=(3/5,3/5,-7/25)\);
- the formerly missed exact dyadic point
  \((4791/65536,5/64,-113/128)\);
- an exact rational grid along \(u=v\) around the formerly missed ridge;
- symmetry under \(u\leftrightarrow v\);
- the full 27-point closed-hemisphere subset of the exact \(D_5\) root
  code, including every diagonal and distinct ordered pair.

For the \(D_5\) cap it also evaluates the complete ordered kernel sum
exactly and obtains a nonnegative rational value.  This is a useful
normalization/sign sanity check independent of the abstract addition
formula.

The packaged degree-11 verifier reuses polynomial primitives by importing
the degree-10 verifier source.  That is a software dependency, not a
mathematical dependency on the degree-10 certificate.  The independent
test removes it as a trust bottleneck by reimplementing all primitives and
using no degree-10 file.

## Reproduction

```sh
python3 verifiers/verify_one_sided_cap_degree11.py
python3 -m unittest \
  tests.test_one_sided_cap_degree11_independent_audit -v
```

Both routes use only Python's standard library and exact
`fractions.Fraction` arithmetic.
