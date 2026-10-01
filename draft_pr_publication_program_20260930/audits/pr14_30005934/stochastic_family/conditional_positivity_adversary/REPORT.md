# Independent conditional and positivity audit

**Audited input:** `source_snapshot/CANDIDATE.md`, SHA256
`bf8d8a5dda2bfe36cd0c28b4a2d0fe9ee1d2ff0365f286de8cc4bd4daa4ccf1d`.

**Scope:** the random-initial conditional-distribution step, scalar exclusion of
negative alpha, and an elementary replacement for the imported noncentral
Wishart parameter theorem. No historical reviews or sibling audit findings were
read. This is a necessity audit conditional on the candidate's finite-rank
Laplace-transform lemma (1); the moving-test stochastic proof is outside this
slice. No solution construction or full rank classification is asserted.

**Verdict:** PASS for this slice. The conditional-version argument and negative
alpha exclusion are valid. The proposed tilt/rescale mechanism is valid, and the
weighted determinant formula has the stated normalization and sign. In fact the
tilt limit can also be taken from the unconditional random-initial transform,
removing any need to use a conditional kernel in the necessity argument.

## 1. Conditional versions and continuity

Let E be the positive trace-class cone on the separable real Hilbert space H.
The trace-class space is a separable Banach space and E is closed, so E is
standard Borel. The finite-dimensional positive semidefinite cone S_n^+ is also
standard Borel. Disintegrate the joint law of (X_0,Y), with Y=J^*X_TJ, to get a
probability kernel K(x,dy) on S_n^+ given x in E. The sample space need not itself
be standard Borel: disintegration of this joint law is enough.

For every fixed v in S_n^+, candidate (1) and the tower property give

    integral exp(-tr(vy)) K(x,dy)
      = det(I+2Cv)^(-alpha/2)
        exp(-tr[b(x) v(I+2Cv)^(-1)])

for initial-law-almost every x, where C=J^*C_TJ>0 and
b(x)=J^*S(T)^*xS(T)J. The function b is continuous in trace norm, and b(x) is a
finite positive semidefinite matrix for every x in E. In particular no moment
assumption on ||X_0||_1 is being inserted.

Choose one countable dense subset of S_n^+. Intersect the corresponding
full-measure sets of x. For each x in that single full-measure set, the left side
is continuous in v by dominated convergence. The right side is continuous as
well: I+2Cv is similar to I+2C^(1/2)vC^(1/2), so it is invertible throughout the
closed positive cone. Thus the equality extends to every v in S_n^+ for that x.
Boundary tests cause no extra issue. It is not necessary to select a single null
set valid for uncountably many J or T; the proof only needs the one deterministic
dimension and compression selected for a fixed alpha.

The apparent nonsymmetry of v(I+2Cv)^(-1) is harmless. It equals

    sqrt(v) (I+2 sqrt(v) C sqrt(v))^(-1) sqrt(v),

which is symmetric positive semidefinite, including when v is singular.

## 2. Negative alpha: pointwise and unconditional checks

In dimension one, c>0 and b(x) is finite. Therefore

    (1+2cr)^(-alpha/2) exp[-b(x)r/(1+2cr)]

tends to infinity as r tends to infinity if alpha<0: the exponential tends to
the strictly positive number exp[-b(x)/(2c)]. A probability Laplace transform is
at most one, so this excludes negative alpha.

The same check can bypass disintegration altogether. After taking expectations
in (1), the scalar transform equals the determinant factor times

    E exp[-b r/(1+2cr)].

Dominated convergence sends this expectation to E exp[-b/(2c)]>0 because b is
finite almost surely. Consequently the unconditional transform would diverge
for alpha<0. A heavy-tailed initial value does not evade the contradiction.

## 3. Whitening and the fixed-noncentrality tilt

Set M=(2C)^(1/2), Z=M^(-1)YM^(-1), and Omega=M^(-1)bM^(-1). Taking
v=M^(-1)uM^(-1) gives exactly

    L(u)=det(I+u)^(-alpha/2)
         exp[-tr(Omega u(I+u)^(-1))],  u in S_n^+.

For t>0 tilt the putative law of Z by exp(-t tr Z)/L(tI) and define
R_t=(1+t)Z under this tilted law. Its Laplace transform is

    L(tI+(1+t)u)/L(tI)
      = det(I+u)^(-alpha/2)
        exp[-tr(Omega u(I+u)^(-1))/(1+t)].

The identity follows from

    I+tI+(1+t)u=(1+t)(I+u),
    [tI+(1+t)u][I+tI+(1+t)u]^(-1)
      = I-(I+u)^(-1)/(1+t).

There is no commutation assumption on Omega and u. Differentiating at the scalar
test qI is legitimate under the tilted law since z exp(-tz) is bounded for
z>=0, and yields

    E_t tr R_t = n alpha/2 + tr(Omega)/(1+t).

After the separate exclusion of negative alpha, these expectations are bounded
for t>=1. Since R_t>=0 and ||R_t||_F<=tr R_t, their laws are tight. A weakly
convergent subsequence remains on the closed cone S_n^+ and has Laplace transform
det(I+u)^(-alpha/2). Only this necessary implication is used.

## 4. A stronger route for random initial values

The conditional kernel is valid, but is dispensable for this replacement. In
the unconditional transform the whitened Omega is a random finite PSD matrix:

    L(u)=g(u) M_0(u),
    g(u)=det(I+u)^(-alpha/2),
    M_0(u)=E exp[-tr(Omega u(I+u)^(-1))].

The same tilt and rescaling gives

    L_t(u)=g(u) M_0(tI+(1+t)u)/M_0(tI).

As t tends to infinity, both expectations in the ratio converge by dominated
convergence to A=E exp(-tr Omega)>0. Thus L_t(u) tends to g(u) for every u>=0.
Initial moments are unnecessary. Tightness can be checked without differentiating:
for q,K>0,

    P_t(tr R_t>K)
      <= [1-L_t(qI)]/[1-exp(-qK)].

Given an error tolerance, first choose q small so that g(qI) is close to one,
then t large so that L_t(qI) is close to g(qI), then K large so that the
denominator is bounded away from zero. This proves tightness along any sequence
t tending to infinity; the finitely many initial terms of a sequence can be
handled by enlarging K. A subsequential limit again has transform g. This route
is useful if the candidate is revised to remove the imported theorem entirely.

## 5. Weighted determinant identity without Wishart classification

Suppose a PSD symmetric n by n random matrix Z has transform
g_alpha(u)=det(I+u)^(-alpha/2). On the independent symmetric coordinates define

    D_ii = partial/partial u_ii,
    D_ij = (1/2) partial/partial u_ij,  i!=j.

The factor 1/2 is essential because tr(uZ) contains 2u_ij Z_ij for i<j.
Constant-coefficient derivatives commute, and

    det(-D) exp[-tr(uZ)] = det(Z) exp[-tr(uZ)].

At u=sI with s>0, all order-at-most-n derivatives can be passed under the
expectation. In a neighborhood with u>=(s/2)I, their absolute values are bounded
by a constant times (1+tr Z)^n exp[-(s/2)tr Z], a bounded function of tr Z.
This avoids assuming any unweighted determinant moment.

To evaluate the derivative, put

    P_n(alpha)=(-1)^n det(D) det(I+w)^(-alpha/2) at w=0.

This is a polynomial in alpha of degree at most n: expand
exp[-(alpha/2) log det(I+w)] to order n, noting that log det(I+w) has zero
constant term. Only its first n powers contribute to an order-n derivative.

For every integer k>=n, let G be an n by k matrix of independent N(0,1)
variables and Z_k=GG^T/2. Direct Gaussian integration gives the transform
det(I+u)^(-k/2). Cauchy-Binet and independence give

    E det(Z_k)=2^(-n) binom(k,n) n!
              =2^(-n) product_{j=0}^{n-1}(k-j).

Indeed each square n by n Gaussian minor has expected squared determinant n!:
the matching-permutation terms each contribute one and all cross-permutation
terms have a centered Gaussian variable appearing once. Thus two polynomials
of degree at most n agree at infinitely many integers, proving

    P_n(alpha)=2^(-n) product_{j=0}^{n-1}(alpha-j)

for every real alpha. This interpolation does not posit a law for noninteger
alpha. It interpolates a derivative of an explicitly defined analytic function.
Scaling I+sI+w=(1+s)[I+w/(1+s)] supplies the requested identity:

    E[det Z exp(-s tr Z)]
      = 2^(-n) product_{j=0}^{n-1}(alpha-j)
        (1+s)^(-n alpha/2-n),  s>0.

For noninteger alpha>=0, let m=floor(alpha) and n=m+2. The factors indexed by
0,...,m are strictly positive and the final factor alpha-(m+1) is strictly
negative. The right side is therefore negative, contradicting det Z>=0. For
alpha=0 or any nonnegative integer the zero factors cause no contradiction;
this audit makes no converse assertion.

## 6. Exact remaining scope

The determinant derivation requires the full matrix Laplace transform on the
PSD cone, which the candidate supplies. A trace-only transform would not
determine the off-diagonal derivatives.

An independently delegated determinant check reconstructed the same proof,
checked dimensions 1--3 directly, and produced an exact rational Taylor-jet
script. The parent of that check independently reran the script: all 144 checks
passed in dimensions 1--4, with twelve alpha values and three scale values.
See `determinant_check/report.md` and `determinant_check/check_jets.py` within this
audit folder. The computation supplements the proof; it does not certify the
stochastic lemma.

The finite-dimensional obstruction is fully supplied by the preceding
checkable argument and does not need the noncentral Wishart parameter theorem.
The candidate's stochastic lemma (1), covariance positivity, and availability
of arbitrary-dimensional domain-admissible compressions must still be checked
by the responsible stochastic audit. The present report does not promote a
process-existence classification or a novelty claim.

**Final checkpoint:** 2026-10-01T14:10:20Z; completion estimate 100% of this
assigned necessity slice. No scoped gap identified.
