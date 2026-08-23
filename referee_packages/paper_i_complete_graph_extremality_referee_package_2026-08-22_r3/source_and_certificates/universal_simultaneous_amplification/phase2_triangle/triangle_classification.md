# Complete dB classification of positive weighted triangles

Timestamp: 2026-08-01 (America/Los_Angeles)

**[SCOPE]** This report starts only from the death--birth update definition in
the research prompt.  No literature search or external graph catalogue was
used.

**[STATUS KEY]** `PROVED` marks a mathematical deduction given below;
`EXACTLY DERIVED` marks symbolic algebra from the displayed Markov equations;
`CERTIFIED IDENTITY` marks a polynomial identity replayed by
`derive_certificate.py`; and `INDEPENDENTLY VERIFIED` marks agreement with the
separate full subset-state solver in `src/exact_markov.py`.

## Classification theorem

**[PROVED] Theorem.**  Give the three edges of an undirected triangle positive
weights

```text
w_12 = 1,   w_13 = x,   w_23 = y,       x>0, y>0.
```

For uniformly random single-mutant initialization and every `r>1`,

```text
rho_dB(G(1,x,y),r) <= rho_dB(K_3,r) = 2r/[3(r+1)].
```

Equality holds if and only if `x=y=1`.  Hence every nonuniform
complete-support weighted triangle is a strict dB suppressor for every
beneficial fitness value.  There is no dB-amplifying parameter region.

**[PROVED] Scale reduction.**  For arbitrary positive edge weights

```text
w_12=a, w_13=b, w_23=c,
```

multiplying all three by the same positive constant cancels from every dB
parent-selection probability.  Therefore setting `x=b/a`, `y=c/a` loses no
generality.  The uniform case is exactly `x=y=1`.

## Six equations from the update definition

**[DEFINITION]** Let `F_i` be the fixation probability when vertex `i` is the
unique mutant.  Let `G_i` be the fixation probability when vertex `i` is the
unique resident.  These are all six transient states of a triangle.

**[EXACTLY DERIVED]** For distinct vertices `i,j,k`, define

```text
u_ij = r w_ij/(r w_ij+w_jk).
```

Starting from singleton `i`, death of the mutant gives extinction with
probability `1/3`.  If resident `j` dies, mutant `i` wins the competition
against resident `k` with probability `u_ij`, conditional on that death, and
the new state is `G_k`.  Deleting self transitions and multiplying the equation
by three gives

```text
(1+u_ij+u_ik) F_i = u_ij G_k + u_ik G_j.          (1)
```

**[EXACTLY DERIVED]** In state `G_i`, vertices `j,k` are mutant.  Define

```text
v_ij = w_ij/(r w_jk+w_ij),
v_ik = w_ik/(r w_jk+w_ik).
```

If resident `i` dies, fixation is immediate.  If mutant `j` dies, resident
`i` replaces it with conditional probability `v_ij`, leaving singleton `k`;
the analogous event for mutant `k` leaves singleton `j`.  The state-change
equation is

```text
(1+v_ij+v_ik) G_i = 1 + v_ij F_k + v_ik F_j.      (2)
```

**[PROVED] Matrix positivity fact.**  Put equations (1)--(2) in the order
`(F_1,F_2,F_3,G_1,G_2,G_3)` and call the coefficient matrix `M`.  Every
off-diagonal entry is nonpositive, and every row satisfies

```text
M_ii = 1 + sum_{j != i} |M_ij|.
```

Thus `M` is strictly row diagonally dominant.  The homotopy
`I+t(M-I)`, `0<=t<=1`, stays strictly diagonally dominant, so its determinant
never vanishes.  Since the determinant starts at one and is real and
continuous, `det(M)>0`.

## Exact rational comparison

**[DEFINITION]** For the unnormalized weights `a,b,c`, put

```text
s1 = a+b+c,
s2 = ab+ac+bc,
s3 = abc.
```

Define

```text
B5 = 12 s1 s2 s3 - 36 s3^2,

B4 = 12 s1^3 s3 - 56 s1 s2 s3 + 12 s2^3 + 72 s3^2,

B3 = -24 s1^3 s3 + 12 s1^2 s2^2 + 80 s1 s2 s3
     -24 s2^3 - 90 s3^2,

P  = 9 s3^2 (r^6+1) + B5(r^5+r) + B4(r^4+r^2) + B3 r^3.       (3)
```

**[CERTIFIED IDENTITY] Denominator certificate.**  Let

```text
L = product_{u != v; u,v in {a,b,c}} (r u+v).
```

Direct determinant expansion of (1)--(2) gives

```text
det(M) = 3P/L.                                      (4)
```

All factors in `L` are positive, and `det(M)>0` by strict diagonal dominance.
Consequently

```text
P>0                                                  (5)
```

for all positive `a,b,c,r`.  Script
`derive_certificate.py` verifies (4) as an exact rational-function identity.

**[DEFINITION]** Define the three symmetric edge polynomials

```text
A = 3 s3(s1 s2-9s3),

D = 12 s1^3 s3 - 45 s1 s2 s3 + 4 s2^3 - 27 s3^2,

E = 4 s2(3 s1^2 s2 - 3 s1 s3 - 8 s2^2),
```

and

```text
H = A(r-1)^4 + D r(r-1)^2 + E r^2.                 (6)
```

**[EXACTLY DERIVED] Exact difference.**  Solving the six equations over the
rational-function field and averaging `(F_1+F_2+F_3)/3` gives

```text
rho_dB(G(a,b,c),r) - 2r/[3(r+1)]
   = - r(r-1) H / [3(r+1)P].                       (7)
```

Both `H` and `P` are homogeneous of degree six in `a,b,c`, so (7) is invariant
under common rescaling of the edge weights.  The script derives (7) after
normalizing `a=1`, and verifies its homogeneous symmetric form exactly.

**[CERTIFIED IDENTITY] Reciprocal-polynomial check.**  Equivalently, if
`z=r+1/r`, then

```text
H/r^2 = E + D(z-2) + A(z-2)^2,
z-2 = (r-1)^2/r.
```

This explains the palindromic quartic in `r` produced by direct elimination.

## Replayable sign certificate

**[DEFINITION]** Set

```text
U = s1^2-3s2,
V = s2^2-3s1s3,
W = s1s2-9s3,
Z = s2^3-27s3^2.
```

**[CERTIFIED IDENTITY] First three nonnegative gaps.**  With
`X=ab`, `Y=ac`, `Z0=bc`, exact expansion gives

```text
U = [(a-b)^2+(a-c)^2+(b-c)^2]/2,

V = [(X-Y)^2+(X-Z0)^2+(Y-Z0)^2]/2,

W = c(a-b)^2 + b(a-c)^2 + a(b-c)^2.                (8)
```

Thus `U,V,W>=0`, and `U>0` exactly when the edge weights are nonuniform.

**[CERTIFIED IDENTITY] Fourth nonnegative gap.**  The remaining gap has the
weighted-square decomposition

```text
Z = s2 V
    + 3[ Z0(X-Y)^2 + Y(X-Z0)^2 + X(Y-Z0)^2 ].       (9)
```

Hence `Z>=0` for positive weights.

**[CERTIFIED IDENTITY] Numerator certificate.**  The coefficients in (6)
satisfy

```text
A = 3 s3 W,

D = 12 s1 s3 U + 3 s2 V + Z,

E = 4 s2(3 s2 U+V).                                (10)
```

Equations (8)--(10) prove `A,D,E>=0`.  If the weights are nonuniform, then
`U>0` and `s2>0`, so `E>0`.  Therefore (6) gives

```text
H >= E r^2 > 0                                      (11)
```

for every positive `r` and every nonuniform positive weighting.  If
`a=b=c`, all four gaps vanish and `H=0`.

**[PROVED] Sign classification.**  For `r>1`, every factor in the denominator
of (7) is positive by (5), while `r(r-1)>0`.  Equation (11) therefore makes
the right side of (7) strictly negative for every nonuniform weighting.  For
uniform weights, `H=0` and the difference is identically zero.  This proves
the theorem with no numerical inference or unclassified parameter cases.

**[EXACT CONSEQUENCE] Neutral endpoint.**  Equation (7) also displays the
factor `r-1`, so all positive weightings tie at the neutral value `r=1`, as
required for a uniformly averaged initial mutant.

## Independent exact verification

**[EXACTLY COMPUTED] Manual derivation script.** The certified package launcher
runs this program. For an individual development invocation from the project
root with its prepared environment, use:

```bash
PAPER1_DEV_PYTHON=python3.14
"$PAPER1_DEV_PYTHON" phase2_triangle/derive_certificate.py
```

It independently constructs (1)--(2), solves the six equations over
`QQ(r,x,y)`, verifies (4), (6)--(10), and checks the exact difference (7).

**[INDEPENDENT TRANSITION-CHECK] Full subset-state cross-check.**  Run:

```bash
PAPER1_DEV_PYTHON=python3.14
"$PAPER1_DEV_PYTHON" phase2_triangle/crosscheck_exact_solver.py
```

This second script uses `src/exact_markov.py`, which independently constructs
all eight subset-state transition rows directly from the update rule.  It
checks exact row sums, compares all six transient fixation values against
(1)--(2), compares the symbolic uniform-singleton average against (7), and
checks several rational specializations without floating point.  It imports
the expected reduced equations and formula from the derivation module, so it
is an independent transition builder rather than a fully independent
certificate implementation.

**[INDEPENDENTLY VERIFIED] Hostile replay.**  The no-import script
`audit/independent_triangle_audit.py` independently rebuilds the bit-mask
chain, determinant coefficients, rational comparison, and SOS residuals. It
also checks boundary and near-uniform limits and 123 exact stress cases.

**[INDEPENDENTLY VERIFIED] Result.**  All three scripts complete successfully
under SymPy 1.14.0. The independently generated full chain and the manually
reduced six-equation derivation agree identically in `r,x,y`, and the hostile
replay confirms the complete certificate without importing project code.
