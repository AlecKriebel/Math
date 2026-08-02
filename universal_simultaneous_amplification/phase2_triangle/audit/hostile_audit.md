# Hostile audit of the phase-two weighted-triangle classification

**Date:** 2026-08-01 (America/Los_Angeles)

**Audited artifacts:** `triangle_classification.md`, `derive_certificate.py`,
and `crosscheck_exact_solver.py`

**Method:** first-principles exact algebra only; no literature search.

## Verdict

**PASS, with one reproducibility-label caveat and no mathematical
correction.**  I found no erroneous Markov equation, symmetric-polynomial
coefficient, determinant factor, SOS identity, sign, or equality condition.
The theorem is exact:

\[
 \rho_{\rm dB}(G(a,b,c),r)\le \rho_{\rm dB}(K_3,r)
 \qquad(a,b,c>0,\ r>1),
\]

with equality exactly when `a=b=c`.  Every nonuniform positive weighted
triangle is therefore a strict dB suppressor for every beneficial fitness.

The caveat is terminological rather than mathematical:
`crosscheck_exact_solver.py` imports `build_six_state_system` and
`formula_difference` from `derive_certificate.py`.  Its subset transition
builder is independent because that part comes from `src/exact_markov.py`,
and it genuinely catches an incorrect reduced Markov system.  It is not,
however, a fully independent reimplementation of the claimed `P`, `H`, or
SOS formulas.  The new audit verifier closes that gap by importing neither
phase-two code nor the project solver.

## Claim-status table

| Claim | Status | Hostile check |
|---|---|---|
| Six reduced first-step equations | Correct | Independently rebuilt from dead-target/parent loops |
| Strict diagonal dominance and `det(M)>0` | Correct | Row gap is exactly one; homotopy preserves it |
| All seven reciprocal coefficients of `P` | Correct | Extracted separately from `det(M)L/3` |
| `det(M)=3P/L` and `P>0` | Correct | Exact generic identity plus positivity proof |
| Difference `-r(r-1)H/[3(r+1)P]` | Correct | Independent full subset-state solution over `QQ(r,x,y)` |
| Reciprocal form of `H` | Correct | Direct algebra after `z=r+1/r` |
| Gap identities (8)--(9) | Correct | Every expanded residual is zero |
| Numerator identities (10) | Correct | Every expanded residual is zero |
| `H>0` off the uniform ray | Correct | `E=4s2(3s2U+V)>0` when `U>0` |
| Equality iff `a=b=c` | Correct | Uniform weights kill all gaps; nonuniform weights force `E>0` |
| Neutral factor `r-1` | Correct | Exact formula and direct chain agree at `r=1` |
| Existing scripts are completely independent | Overstated | Cross-check imports its expected formulas from derivation module |
| Boundary or extreme ratios reveal a counterexample | Falsified | Exact symbolic limits and extreme rational tests stay negative |

## 1. Re-derivation of the six-state system

Let the edge weights be

\[
 w_{12}=a,\qquad w_{13}=b,\qquad w_{23}=c.
\]

Write `F_i` for singleton mutant `i` and `G_i` for unique resident `i`.
From singleton `i`, if `i` dies the mutant becomes extinct.  If resident `j`
dies, the competing sources are mutant `i` and resident `k`, so the gain
probability conditional on that death is

\[
 u_{ij}=\frac{r w_{ij}}{r w_{ij}+w_{jk}}.
\]

Removing holdings and multiplying by three gives

\[
 (1+u_{ij}+u_{ik})F_i=u_{ij}G_k+u_{ik}G_j.
 \tag{A1}
\]

In state `G_i`, the resident's death fixes immediately.  If mutant `j` dies,
resident `i` replaces it with conditional probability

\[
 v_{ij}=\frac{w_{ij}}{r w_{jk}+w_{ij}},
\]

leaving singleton mutant `k`.  Thus

\[
 (1+v_{ij}+v_{ik})G_i=1+v_{ij}F_k+v_{ik}F_j.
 \tag{A2}
\]

The target/source indices and the singleton left by a loss are all correct in
the manuscript.  The independent audit code does not encode (A1)--(A2)
directly: it loops over all six transient bit masks, all dead targets, and all
possible parents.  It nevertheless produces the same linear system after a
simultaneous state permutation.

## 2. Determinant sign and denominator positivity

In the order `(F_1,F_2,F_3,G_1,G_2,G_3)`, every off-diagonal coefficient in
`M` is minus a conditional state-change probability.  Each row has the form

\[
 M_{ii}=1+\sum_{j\ne i}|M_{ij}|.
\]

Therefore `M` is strictly row diagonally dominant, with positive diagonal.
For

\[
 M(t)=I+t(M-I),\qquad 0\le t\le1,
\]

the diagonal-dominance gap remains exactly one:

\[
 M(t)_{ii}-\sum_{j\ne i}|M(t)_{ij}|=1.
\]

Hence `det(M(t))` never vanishes.  It is real and continuous and starts at
`det(I)=1`, so `det(M)>0`.  This proves positivity, rather than merely
nonsingularity.

Set

\[
 L=\prod_{u\ne v}(ru+v),\qquad u,v\in\{a,b,c\}.
\]

There are six ordered factors, and all are positive for positive weights and
fitness.  A direct generic determinant calculation from the audit's bit-mask
system gives exactly

\[
 \frac{L\det(M)}3=P.
 \tag{A3}
\]

Consequently `P>0`.  This argument is robust even if an individual expanded
coefficient of `P` is not assigned a separate sign; coefficientwise
positivity is neither used nor needed.

## 3. Audit of every coefficient of `P`

With

\[
 s_1=a+b+c,\qquad s_2=ab+ac+bc,\qquad s_3=abc,
\]

the independently cleared determinant in (A3) has the following coefficients
as a polynomial in `r`:

| Power of `r` | Independently obtained coefficient |
|---:|---|
| `6` and `0` | `9 s3^2` |
| `5` and `1` | `12 s1 s2 s3 - 36 s3^2` |
| `4` and `2` | `12 s1^3 s3 - 56 s1 s2 s3 + 12 s2^3 + 72 s3^2` |
| `3` | `-24 s1^3 s3 + 12 s1^2 s2^2 + 80 s1 s2 s3 - 24 s2^3 - 90 s3^2` |

These are exactly `9s3^2`, `B5`, `B4`, and `B3` in the manuscript.  The audit
also checks each displayed coefficient under all six permutations of
`(a,b,c)`.  The reciprocal pattern is exact, not inferred from sampled
values.

At the uniform point, the claimed specialization also checks:

\[
 P(1,1,1;r)=9(r+1)^2(r^2+3r+1)^2>0.
\]

## 4. Independent audit of the rational difference

The audit builder solves its directly generated transient subset system for
weights `(a,b,c)=(1,x,y)`.  Without importing either existing phase-two
script, it obtains

\[
 \rho_{\rm dB}(G(1,x,y),r)-\frac{2r}{3(r+1)}
 =-\frac{r(r-1)H(1,x,y;r)}{3(r+1)P(1,x,y;r)}.
\]

The comparison is an identity in `QQ(r,x,y)`.  Since `P` and `H` are both
homogeneous of degree six in the weights, this normalized identity is exactly
the stated homogeneous formula for arbitrary positive `a,b,c`.

No sign was inferred from the symbolic solver: the sign is established
separately by the SOS certificate below.

## 5. Reciprocal numerator and SOS identities

The three coefficients of

\[
 H=A(r-1)^4+Dr(r-1)^2+Er^2

\]

were checked term by term:

\[
 \begin{aligned}
 A&=3s_3(s_1s_2-9s_3),\\
 D&=12s_1^3s_3-45s_1s_2s_3+4s_2^3-27s_3^2,\\
 E&=4s_2(3s_1^2s_2-3s_1s_3-8s_2^2).
 \end{aligned}
\]

Dividing by `r^2` and using

\[
 z-2=\frac{(r-1)^2}{r},\qquad z=r+r^{-1},
\]

gives exactly

\[
 H/r^2=E+D(z-2)+A(z-2)^2.

\]

For the sign certificate, put

\[
 U=s_1^2-3s_2,\quad V=s_2^2-3s_1s_3,\quad
 W=s_1s_2-9s_3,\quad Z=s_2^3-27s_3^2.

\]

With `X=ab`, `Y=ac`, and `Z0=bc`, direct expansion independently confirms

\[
 \begin{aligned}
 U&=\tfrac12\{(a-b)^2+(a-c)^2+(b-c)^2\},\\
 V&=\tfrac12\{(X-Y)^2+(X-Z_0)^2+(Y-Z_0)^2\},\\
 W&=c(a-b)^2+b(a-c)^2+a(b-c)^2,\\
 Z&=s_2V+3\{Z_0(X-Y)^2+Y(X-Z_0)^2+X(Y-Z_0)^2\}.
 \end{aligned}
 \tag{A4}
\]

Every multiplier is nonnegative, and all edge-based multipliers are positive
under the theorem's hypotheses.  The numerator identities also expand
exactly to

\[
 A=3s_3W,\qquad
 D=12s_1s_3U+3s_2V+Z,\qquad
 E=4s_2(3s_2U+V).
 \tag{A5}
\]

Thus `A,D,E>=0`.  More importantly, if the weights are nonuniform then
`U>0`, so

\[
 E=4s_2(3s_2U+V)>0

\]

because `s2>0`.  It follows that

\[
 H\ge Er^2>0\qquad(r>0)

\]

off the uniform ray.  If `a=b=c`, every square in (A4) vanishes, hence
`A=D=E=H=0`.  This proves the equality classification in both directions.

For `r>1`, the exact difference has a negative leading sign because
`r(r-1)>0`, `r+1>0`, `P>0`, and `H>0`.  At `r=1`, the explicit `r-1` factor
forces the correct neutral tie.

## 6. Edge, extreme-ratio, and equality stress tests

The theorem assumes complete positive support, but approaching its boundary
does not reveal a hidden interior sign change.  Setting `a=0` while keeping
`b,c>0` gives a connected path and the exact factors

\[
 \begin{aligned}
 P|_{a=0}
 &=12b^2c^2r^2(b+cr)(br+c)>0,\\
 H|_{a=0}
 &=4b^2c^2r\{bc(r-1)^2+r(3b^2-2bc+3c^2)\}>0.
 \end{aligned}

\]

The last quadratic is positive because, for example,
`3b^2-2bc+3c^2=2(b-c)^2+b^2+c^2`.

For three exact one-parameter rays, the boundary limits of the fixation
difference are:

| Weights | `t -> 0+` | `t -> infinity` |
|---|---:|---:|
| `(1,t,1)` | `-(r-1)/[9(r+1)]` | `-(r-1)/[3(r+1)]` |
| `(1,t,t)` | `-(r-1)/[3(r+1)]` | `-(r-1)/[9(r+1)]` |
| `(1,t,1/t)` | `-(r-1)/[3(r+1)]` | `-(r-1)/[3(r+1)]` |

All are strictly negative for `r>1`.  Some limiting supports are disconnected,
so their path-dependent limits are not additional theorem cases; they are
only hostile stress tests.

Near equality, along `(a,b,c)=(1,1+epsilon,1)`, the exact quadratic departure
is

\[
 \rho_{\rm dB}(G,r)-\rho_{\rm dB}(K_3,r)
 =-\frac{2r(r-1)}{9(r+1)(r^2+3r+1)}\,\epsilon^2
 +O(\epsilon^3).

\]

The coefficient is strictly negative for `r>1`, confirming that the uniform
equality point is isolated modulo common scaling.

The independent verifier additionally solved the full chain in exact
rationals for 120 deterministic pseudorandom nonuniform cases and three
extreme cases, including weights with ratios up to `10^24`, fitness
`1000001/1000000`, fitness `10^6`, and a near-uniform triple of size
`10^15`.  Every direct difference equaled the formula exactly and was
strictly negative.  Uniform scale variants tied exactly.

## 7. Script-independence audit

`derive_certificate.py` is independent of `src/exact_markov.py`.  It manually
constructs (A1)--(A2), solves them, and verifies the determinant, rational
difference, and SOS identities.  This is an exact derivation, not numerical
evidence.

`crosscheck_exact_solver.py` uses a genuinely separate transition builder in
`src/exact_markov.py`; comparing all six transient values therefore catches
wrong state equations or source/target indexing.  But the cross-check imports
the reduced system and claimed formula from `derive_certificate.py`.  It
should be described as an independent **transition-chain cross-check**, not as
a fully independent certificate implementation.

The audit verifier `independent_triangle_audit.py` closes this modest gap.  It
imports neither existing script nor any project module.  It:

1. builds all transient equations from masks, dead targets, and parents;
2. clears the generic determinant and checks every coefficient of `P`;
3. solves the normalized symbolic chain and checks the `H/P` identity;
4. expands all SOS residuals independently;
5. verifies boundary and near-equality limits symbolically; and
6. performs exact rational random and extreme tests.

Run it from the repository root with

```sh
PYTHONDONTWRITEBYTECODE=1 python phase2_triangle/audit/independent_triangle_audit.py
```

The stdout is stored verbatim in `phase2_triangle/audit/verification_output.txt`.
At the time of this audit, the reproducibility hashes are

```text
c3f06ff526e637e5b3d1a7a5bb2ad0560e08193aed01698288613d389ad0d610  phase2_triangle/audit/independent_triangle_audit.py
aa87ee6f4bddb13c33d912acad5fd42d7ead5f01bad4a629fe1a620de2dcb34b  phase2_triangle/audit/verification_output.txt
5809b777d3569da8c480a1ab7220997564b64fb14cd83e5bce90dfd93824eea2  phase2_triangle/derive_certificate.py
1530fc89e0199892a56d1b99a327cec7056860e93ab149b8e87dca8f0402cf63  phase2_triangle/crosscheck_exact_solver.py
```

The audit output file hash equals the hash of freshly generated stdout.

## Required action

No mathematical correction is required.  For maximum precision, revise only
the prose label around `crosscheck_exact_solver.py` from an unqualified
"independent exact verification" to "independent transition-chain
cross-check," or state explicitly that it imports the expected reduced system
and formula from the derivation module.  The theorem and its proof certificate
stand unchanged.
