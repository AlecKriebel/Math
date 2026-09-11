# A rational global projective bound for the paper's Bell functional

**Result of this continuation:** the paper's functional has the valid projective upper bound

\[
\mathcal B_{\rm PVM}\le C=\frac{289}{10}=28.9.
\]

The proof is the exact operator certificate below, together with the elementary
qubit-support reduction. Its finite rational identities and positivity certificates
have been executed independently. The associated Lean source has **not** been
compiled or kernel-checked. This document is a mathematical proof/certificate,
not a Lean build report. Neither C nor the witness value is claimed optimal.

## 1. Physical setup and support reduction

Let the state be any positive-semidefinite complex two-qubit density matrix of
trace one. For Alice's first two projective measurements, coarse-grain labels 0
and 2 and set \(A_x=I-2M_{1|x}\). For Bob set \(B_y=I-2N_{1|y}\).
These are Hermitian involutions, including scalar values \(\pm I\).

A three-label PVM on a two-dimensional space has a zero effect. Here is an
algebraic proof which includes deterministic measurements. Suppose its three
effects P,Q,R are nonzero. Cayley–Hamilton and P²=P give

\[
(1-\operatorname{tr}P)P+\det(P)I=0.
\]

Multiplying by Q and using PQ=0 shows det(P)Q=0, hence det(P)=0.
As P is nonzero, tr(P)=1. Applying the same argument to Q and R contradicts
tr(P+Q+R)=tr(I)=2. Thus some effect is zero. The remaining two effects are
complementary projections, allowing I and 0.

This proves that the auxiliary support is contained in one of {0,2}, {1,2}, or
{0,1}. Singleton supports are included in those three cases; no separate
nondegeneracy assumption is made.

Write

\[
S=A_0(B_0+B_1)+A_1(B_0-B_1),
\]

where opposite-party multiplication means the tensor product. Operators from
different parties commute; no commutation of two operators on the same party
is assumed.

## 2. Support {0,2}: the 12-word rational certificate

Put \(M_0=(I+A_2)/2\), \(M_1=0\), and \(M_2=(I-A_2)/2\).
Expanding the three probability terms in the paper gives the Bell operator

\[
\mathcal B_{02}=\frac7{20}I+10S+\frac3{20}B_0+\frac15B_1
-\frac1{20}A_2+\frac3{20}A_2B_0-\frac15A_2B_1.
\]

Use this exact ordered word vector:

\[
W=(I,A_0,A_1,A_2,B_0,B_1,A_0B_0,A_0B_1,A_1B_0,A_1B_1,A_2B_0,A_2B_1)^T.
\]

Then

\[
C I-\mathcal B_{02}=\sum_{i,j=0}^{11}Q_{ij}W_i^\dagger W_j,
\qquad Q=R/600,
\]

with the following integer matrix R. Word ordering is part of the certificate.

```text
 5127  -24    1    7    -9   -19 -1810 -1809 -1788  1788  -23   30
  -24 1670    1   -2 -1190 -1191     8    -8    20   -13   -3   -3
    1    1 1718   11 -1212  1212   -20    13   -39   -39    2   -2
    7   -2   11   27   -22    30     3     3    -2     2   -5    6
   -9 -1190 -1212 -22 1712   -18     3    -2    26    17    3    0
  -19 -1191  1212  30  -18  1723     2    21   -17   -27    0    5
-1810    8  -20    3     3     2  1283   644   628     0   18    0
-1809   -8   13    3    -2    21   644  1277     0  -629    0  -16
-1788   20  -39   -2    26   -17   628     0  1273  -625   -8    0
 1788  -13  -39    2    17   -27     0  -629  -625  1269    0   -3
  -23   -3    2   -5     3     0    18     0    -8     0   25   -1
   30   -3   -2    6     0     5     0   -16     0    -3   -1   26
```

The twelve leading principal determinants of R, computed independently using
fraction-free integer Bareiss elimination, are

```text
5127
8561514
14708674207
395923632520
317938046777
331213725184
139091716422844
73212467673772676
1777124200780697392
44864434554956614060
26211598440355917568
29164077512661700532
```

They are all strictly positive. Thus R and Q are positive definite by the real
symmetric Sylvester criterion. An alternative, explicit certificate in
`certificates/binary_pair_sos.json` gives a rational unit lower triangular L and
positive rational diagonal d with Q=L diag(d) Lᵀ. The first checker verifies all
144 entries and all 12 positive pivots. The second checker computes the displayed
determinants **without using L or d**, then compares determinant ratios to d.

Equivalently, putting \(K_k=\sum_i L_{ik}W_i\),

\[
C I-\mathcal B_{02}=\sum_k d_k K_k^\dagger K_k\succeq0.
\]

The operator identity is checked in the free *-algebra with relations
A_i²=B_j²=I and cross-party commutation. The checker preserves the order of
same-party words and compares coefficients before identifying a word with its
adjoint. It also separately expands the twelve weighted operator squares.

This is a universal algebraic identity, not a numerical eigenvalue estimate at
sampled observables. Taking expectation in any positive normalized state proves
the stated upper bound for this support.

## 3. Support {1,2}

Here take \(M_1=(I+A_2)/2\), \(M_0=0\), and \(M_2=(I-A_2)/2\).
Apply the previous certificate with

\[
(A'_0,A'_1,A'_2,B'_0,B'_1)=(-A_1,-A_0,A_2,-B_0,B_1).
\]

The CHSH operator is unchanged, while the auxiliary term becomes

\[
\frac3{20}(I+A_2)(I-B_0)+\frac15(I-A_2)(I+B_1),
\]

which is exactly the {1,2} operator. Thus the same positive Gram matrix applies.

## 4. Support {0,1}: a short certificate

Now \(M_0=(I+A_2)/2\), \(M_1=(I-A_2)/2\), \(M_2=0\), so

\[
\mathcal B_{01}=10S+\frac3{10}(I+A_2B_0).
\]

An independent small identity is

\[
\begin{aligned}
C I-\mathcal B_{01}={}&\frac{25}{7}
 \left(\frac75A_0-B_0-B_1\right)^2
+\frac{25}{7}\left(\frac75A_1-B_0+B_1\right)^2\\
&+\frac3{20}(I-A_2B_0)^2+\frac1{70}I.
\end{aligned}
\]

Each displayed factor is Hermitian. All coefficients are positive. This gives
the upper bound without a Schmidt decomposition or an optimization over states.

## 5. Convexification, labels, and strict separation

Every raw qubit PVM strategy is in one of the three cases above. Since the Bell
score is linear, the bound also holds on its shared-randomness convex hull.
Classical output postprocessing cannot improve a linear optimum: a finite
stochastic map is a mixture of deterministic maps, and a deterministic map
merges orthogonal projectors and inserts zero projectors. This last standard
postprocessing argument is stated here mathematically; a separate general
stochastic-postprocessing closure theorem is not yet supplied in the Lean project.
The formal end target uses the actual declared-output PVM convex hull.

The paper's explicit witness still attains

\[
L_0=20\sqrt2+\frac{16}{25}.
\]

Because \(707^2=499849<500000=2\cdot500^2\),
\(\sqrt2>707/500\). Consequently

\[
L_0-C=20\sqrt2-\frac{1413}{50}>\frac1{50}>0.
\]

Also the paper's original upper bound U satisfies

\[
U-C=\frac{5003\sqrt2-7071}{250}
 >\frac{1621}{125000}>0.
\]

The new bound is therefore strictly stronger than U. Numerically L₀−C is about
0.02427124746; the decimal is explanatory, not part of any proof.

## 6. Replay and Lean boundary

From the project root:

```bash
python3 scripts/sos_checks.py
python3 scripts/sos_bareiss_check.py
python3 scripts/physical_operator_checks.py
```

The first two commands use only Python's standard library. The third uses SymPy
to check universal entrywise polynomial bridges, including complex entries,
Cayley–Hamilton, projection-to-involution identities, the physical Bell-operator
expansions, tensor algebra, and the trace identities used for positive expectation.
Five deliberately corrupted SOS certificates are rejected by the first checker.

The Lean path is

```text
Quantum → Expectation → SOSAlgebra → SOSCertificate
Quantum → ProjectionSupport
SOSCertificate + ProjectionSupport → ProjectiveSOS
ProjectiveSOS + Targets + Witness → ProjectiveBound
```

`projective_global_upper_bound` and `three_by_two_separation` are now written
without an assumed global projective bound. **Their proof bodies remain
uncompiled.** This certificate does not establish the universal 2×2 equality or
the minimum-input conclusion, which requires that equality separately.

Certificate SHA-256:
`2dd1ecf2e51447fb765da64a80593389319616ef9adcf13eb47be44e57621bdd`

The floating-point search in `research/` only discovered a candidate. Neither
exact checker treats its output or any numerical positivity assertion as evidence.
