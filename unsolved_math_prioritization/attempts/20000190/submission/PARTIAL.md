# Exact focal-feasibility controls for a seven-point pencil

Problem 20000190 / AIM-ALGEBRAIC_GEOMETRY-0190. Disposition: **unsolved, 5/5**.
This is a partial audit, not a claimed resolution or a novelty claim.

## 1. Target and inherited result

The primary AIM 1.5 question asks whether one can efficiently anticipate nonreal
focal estimates before constructing the fundamental matrix. It does not specify
an estimator, a noise model, a calibration convention, or a complexity measure.
The catalogue's seven-point-certificate title describes its imported partial
report, not an additional theorem requested by AIM.

The imported report already gives a four-query Sturm--Tarski formula for generic
seven-point data, assuming simple rank-two determinant roots and nonzero focal
numerators and denominators. That construction and its mixed-sign example are
prior work; neither is presented here as a new discovery. The following are
independently constructed controls and a classical zero-aware extension.

We use real centered image coordinates, known principal points, zero skew,
unit aspect ratio, and two independently variable focal lengths. Their numerical
values need not differ. The epipolar convention is x2^T F x1 = 0. Positive focal
squares mean positive finite real focal lengths; they do not impose cheirality
on every correspondence. For real F a negative rational focal square yields
imaginary, rather than negative real, focal lengths. A zero denominator is a
separate event.

## 2. Same determinant polynomial, different focal signs

Let

    B = [-7,  2,  16; 5, -4, 4; -20, 25, -70],
    G = diag(1,2,3),  H = diag(2,1/2,1),
    F(z) = B + zG,  Fhat(z) = H^(-T) F(z).

Both pencils have exactly the determinant

    p(z) = 6 z^3 - 194 z^2 + 1854 z.

The quadratic factor has negative discriminant, so the only real root is zero;
it is simple. Both root matrices have rank two. Using the modified Bougnoux
quartics (Kocur--Kyselica--Kukelova, supplement, equation (1)), all denominators
at that root are nonzero, and the focal-square pairs are

    B:       (4,25),
    H^(-T)B: (-112/377, -1925/67).

These are pencils coming from actual seven-correspondence design matrices, not
arbitrary formal cubics. Take x=(u,v,1)^T at

    (-1,0), (-1,1), (-2,0), (-2,1), (-3,-1), (-3,2), (-4,1),

and y=(Bx) cross (Gx). The seven y vectors are respectively

    (-3,-19,-1), (35,-50,45), (-18,-30,-12), (-20,-86,44),
    (-91,0,-91), (-217,-243,107), (-130,-278,12).

Every y has a nonzero last coordinate; the bilinear equations with B and G
hold exactly. The resulting design matrix has rank seven. Replacing y by Hy
gives another rank-seven design with nullspace spanned by H^(-T)B and H^(-T)G.
The verifier performs both exact rank computations.

There is also an explicit real-camera realization of B. Let t=(1,3,2)^T,
K1=diag(2,2,1), K2=diag(5,5,1), and

    U = (1/3) [2,-1,2; 2,2,-1; -1,2,2].

Then U^T U=I, det U=1 and B=30 K2^(-T)[t]_cross U K1^(-1).
No cheirality claim is made for this particular set of cross-product matches.

Thus a decision rule using only det(F(z)) for a supplied pencil cannot recover
its focal-sign labels. This is stronger than merely showing that the sign of
the cubic discriminant is insufficient. H is anisotropic: it does not preserve
the square-pixel calibration assumption. We compare two input datasets under
the same fixed intrinsic convention; this is not a failure of coordinate
invariance when the calibration convention is transformed too. Nor does it
assert impossibility for a procedure that uses more of the design matrix.

## 3. Zero-aware root-free chart count

Assume a real independent pencil F(z)=B+zG with p=det F not identically zero.
Let r be the monic squarefree part of p, so repeated determinant roots are
counted once. Let N_i,D_i be the quartics of the displayed Bougnoux chart and
q_i=N_i D_i. Define the real rank guard

    R(z) = sum of the squares of all nine 2 by 2 minors of F(z).

At every real determinant root, R is nonnegative and R>0 is equivalent to
rank exactly two. Write T(h) for the sum of sign h over the distinct real
roots of r. The number of real rank-two roots on which q1>0 and q2>0 is

    C = (1/4) sum over a,b in {1,2} of T(R q1^a q2^b).        (A)

This counts positive values of this rational chart. A zero q is reported as
unclassified by the chart, not classified as incompatible. In particular,

    rank-two root count = T(R),
    rank-two count with q1*q2 nonzero = T(R q1^2 q2^2),
    unclassified rank-two count = their difference.

Proof: for s in {-1,0,1}, the indicator of s=1 is (s^2+s)/2.
Multiply the two indicators by sign R, then sum. This proves (A), including
roots at which a numerator or denominator vanishes, and rank-one roots.
No assumption about nonvanishing at nonreal roots is needed. The imported
formula instead uses (1+s)/2 and therefore requires nonzero signs.

For an exact coefficient-only implementation, let C_r be multiplication by z
in Q[z]/(r). The Hermite matrix for h has entries

    Herm_r(h)[i,j] = trace(h(C_r) C_r^(i+j)), 0<=i,j<deg r.

Its signature equals T(h). For completeness, over R the squarefree quotient
splits into one R factor for each real root and one C factor for each nonreal
conjugate pair. A real factor contributes sign h(alpha). A complex factor is
the real quadratic form 2 Re(h(alpha)w^2): if h(alpha) is nonzero it has one
positive and one negative direction, and otherwise it is zero. Thus complex
pairs contribute zero signature. This proves the identity used by verify.py.
It is classical Hermite/Tarski machinery, also documented in Gaillard--Safey
El Din, Theorem 2.4 and equation (2); we claim no new general sign theorem.

Only matrices of size at most three are needed. Rational congruence computes
their signatures without root isolation or approximation. A nonzero off-
diagonal entry when all diagonal entries vanish is handled by the basis vector
e_i+e_j; there is no unsupported nonzero-principal-minor assumption. The
verifier tests this case independently.

Projective infinity must be treated separately: in F(z)=B+zG, infinity is G.
If det G=0, evaluate its rank and chart directly and add its contribution once.
For example, reversing the pencil in Section 2 gives G+zB, whose determinant
has no finite real root; its positive root is precisely the infinity point B.
Ignoring it would turn the count from one into zero. If p is identically zero,
there is a positive-dimensional determinant locus, and this finite-root routine
explicitly refuses the input. If rank A<7, the nullspace need not be a pencil.

Equation (A) and the rank/infinity handling extend the implementation of the
inherited generic count. They do not resolve camera criticality at q=0.

## 4. Undefined focal chart with a genuine positive family

Let

    T = [0,0,0; 0,0,-1; 0,1,0],  Fcrit(z)=T+zG.

Then det Fcrit = z(6z^2+1), and zero is its only real determinant root. T has
rank two but N1=D1=N2=D2=0. Formula (A) therefore reports one unclassified
root and zero positive-in-chart roots. It must not reject the input.

For every a>0, K=diag(a,a,1) satisfies KTK=aT, an essential matrix. Hence T
admits positive focal lengths with f1=f2=a for an entire positive continuum.
This is genuine nonuniqueness, not merely a removable denominator in a formula
for a unique focal pair.

Again this is an exact rank-seven sample, and now a cheiral realization is
explicit. Use the same seven (u,v) above, all with u<0. Set

    u' = -(2v^2+3)/u,  x=(u,v,1),  y=(u',v,1),
    Z = 1/(u'-u),  X=(uZ,vZ,Z).

Then Z>0, x is the projection of X by [I|0], and y is its projection by
[I|(1,0,0)^T]. Both camera depths are positive. The epipolar equations for T
and G hold, and the seven-row design has rank seven. The example shows why a
formula pole cannot be silently translated into a negative focal verdict.

## 5. An exact radical-free feasibility reduction

For real rank-two F and positive numbers a,b, put A=diag(a,a,1),
B=diag(b,b,1). The following polynomial matrix vanishes exactly when the
positive calibrations f1=sqrt(a), f2=sqrt(b) make F essential:

    W(F,a,b) = 2 F A F^T B F - trace(F A F^T B) F = 0.        (B)

Proof: set E=K2 F K1 with K1=diag(sqrt(a),sqrt(a),1) and analogously K2.
The standard cubic essential equation 2EE^T E-trace(EE^T)E=0, multiplied by
K2^(-1) and K1^(-1), is exactly (B). For real rank-two E, use a real SVD.
The equation holds precisely when its two nonzero singular values agree,
which is equivalent to a real nonzero-baseline essential matrix. Positivity
and rank are essential hypotheses in this argument.

Consequently, for a seven-point pencil a chart-free existential formulation is

    exists real z,a,b:
       p(z)=0, R(z)>0, a>0, b>0, W(F(z),a,b)=0,

together with the corresponding infinity test. A nonpencil kernel can be
parametrized too, with normalization charts to exclude its zero matrix.
Real quantifier elimination supplies a theoretical decision method; this
packet does not implement or benchmark that complete method. General
fixed-variable decidability is not a new camera result or demonstrated
practical advantage over generating and checking a cubic's roots.

For T from Section 4, (B) reduces exactly to a=b. For diag(1,2,0), it contains
-3ab and 6ab, so no a,b>0 are possible. Merely allowing a=0 or b=0 would
incorrectly accept it. For both matrices in Section 2, their signed rational
focal values satisfy (B); only the first pair has a,b>0. Thus satisfying
polynomial essential equations over signed or complex parameters is not a
real positive-calibration test by itself.

## 6. Conditioning near a pole

Consider the rank-two family

    M(t) = [1,2,1; 2,1,2; t+2,2t+1,t+2].

Its first two rows have a nonzero 2 by 2 minor. The chart returns

    f1^2 = -(t+2)(2t-1)/(4(t-1)(t+1)),
    f2^2 = -(t+2)(2t+1)/4.

At t=-1 the first denominator is zero and its numerator nonzero; the second
square has finite value 1/4. For every 0<epsilon<1/2, M(-1-epsilon) has both
squares positive, whereas M(-1+epsilon) has first square negative and second
positive. Their entrywise maximum distance is 4 epsilon. The verifier checks
six rational epsilon values, including 1/1,000,000, and verifies (B) at each.
The all-epsilon sign statement follows directly from the displayed factors.

This blocks a uniform fixed absolute perturbation margin separating the two
classes near a pole. It does not refute adaptive-precision certification away
from the boundary, and it does not claim an impossibility theorem for all
robust estimators. Exact rank-seven assumptions are not automatically inherited
by noisy overdetermined input.

## 7. Exact remaining gap

The primary question remains **unsolved by this attempt**. Generic pre-root
sign counting is already present in the imported partial report. We now have
an exact zero-aware finite-root implementation and independently constructed
failure controls, but no complete, tested, practically efficient pre-candidate
procedure that classifies all critical positive-calibration fibers and an
explicit noisy estimator. The broad source question does not fix those choices;
no convenient stronger or weaker formulation is silently substituted for it.
No independent review, peer review, speed benchmark, or priority guarantee is
claimed. The original five routes stop here.
