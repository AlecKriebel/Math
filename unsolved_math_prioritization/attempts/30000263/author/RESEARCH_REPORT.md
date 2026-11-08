# Discrete interaction matrix inequalities in three dimensions

Problem 30000263, OWR-1050-014. Research date: 2026-10-05.

## Conclusion and scope

**PARTIAL RESULTS; NO FULL RESOLUTION.** The target is the Bahri–Xu inequality.
The published range is arbitrary point counts on a line, and at most
five points in any dimension. This report independently supplies a real-variable
proof of collinear zero exclusion and a geometric proof through five points.
The uniform conclusion uses the published collision/escape reduction.
It also gives elementary restricted-case
estimates, a quantitative extension to vectors supported on at most five points,
a six-point reduction to the plane, and an exclusion of a symmetric two-ring
ansatz. It also identifies a false geometric step in an older author-hosted
manuscript claiming the six-point case. None of these results establishes the
inequality for arbitrary signed vectors and arbitrary point counts in R^3.

The analytic arguments below are the primary evidence. Numerical searches are
finite, floating-point explorations, and have no general proof status. No
novelty or priority claim is made for these deductions and reformulations.

## Exact question and normalization

Let x_1,...,x_p be pairwise distinct points of R^3. Put r_ij=|x_i-x_j|,
A_ii=0, A_ij=1/r_ij for i≠j, and, for u in R^p, define

    P_i = sum_{j≠i} u_j/r_ij,
    F_i = sum_{j≠i} u_j (x_i-x_j)/r_ij^3,
    G_i = -2 u_i F_i,
    D = sum_{i≠j} u_j^2/r_ij^2,
    N = sum_i P_i^2 + max_{i,k} |G_i^k|.

Both indices in D are summed: it is an ordered-pair sum. Direct differentiation
gives G_i^k=u^T(∂A/∂x_i^k)u. The target asks whether N≥c(p)D for a positive
constant depending only on p. The inequality is trivial for u=0. For p≥2 and
u≠0, D>0. Both N and D scale by t^2/λ^2 under u↦tu and x↦λx.

The original OWR display at printed p. 1658 abbreviates the supremum index
range. The question here uses the all-point/all-coordinate maximum in the
catalog, consistent with the subsequent Bahri–Xu formulations. The later
papers use max_i |G_i|_2 instead. If N_2 denotes that version, then

    N ≤ N_2 ≤ sqrt(3) N.

Consequently the existence assertions are equivalent; a vector-norm constant
c transfers to the coordinate version as c/sqrt(3). In particular, no
dimension-dependent norm convention is silently treated as an identical
numerical constant.

The live problem URL returned HTTP 403 during this review. The complete local
problem record, not a shortened statement, was checked against the original
OWR PDF and later papers. Its complete-record-plus-report hash, with a missing
report represented by {}, is recorded in TARGET_REVIEW.json. Source PDFs and
their extracts are excluded from this package.

## Literature status checked against primary sources

The original question occurs in Abbas Bahri's contribution to OWR 29/2005,
printed pp. 1658 and 1660 [1]. Xu proved the three-point case [2].
Chen, Ge, Jia and Lu prove the collinear case for every p (Theorem 3.2),
the cases p=4,5 in any dimension (Theorem 3.3), and an inductive equivalence
between uniform coercivity and absence of nonzero solutions of

    P_i=0 and u_i F_i=0 for every i.                         (Z)

The equivalence is Theorem 1.1 in the arXiv version and Theorem 1.4 in the
final journal version; its induction includes collision and escape
limits [3]. Pointwise absence of zeros alone is not being substituted for that
compactness theorem.

An author-hosted Lan–Lu manuscript dated March 9, 2011 claims p≤6, while its
introduction claims a broader result. Its pp. 11–12 contain unfinished steps
and the defective geometric assertion analyzed below [4]. It is not accepted
here as a verified resolution. The official publication record for [3] and its
author's publication list were checked. Targeted searches did not locate a
later full proof; this is a bounded literature finding, not a proof that no
such paper exists.

## Approach 1 Direct estimates and the spectral obstruction

### Same sign and strongly unbalanced signs

If all nonzero u_i have the same sign, expansion row by row gives

    |Au|^2 = D + 2 sum_i sum_{j<k; j,k≠i} u_j u_k/(r_ij r_ik) ≥ D.

Thus c=1 works on either same-sign cone, in every dimension and for every p.

There is also a quantitative open cone around this situation. Write u=v-w,
where v,w≥0 have disjoint supports, and let D_+=D(v), D_-=D(w). Each row of A
has p-1 entries, so Cauchy–Schwarz gives |Aw|^2≤(p-1)D_-; the same-sign result
gives |Av|≥sqrt(D_+). Hence, when D_->=0 and
sqrt(D_+)≥sqrt((p-1)D_-),

    N ≥ (sqrt(D_+) - sqrt((p-1)D_-))^2.

For example, if D_-≤D_+/(4(p-1)), then

    N ≥ [(p-1)/(4p-3)] D.

The signs may be interchanged. This leaves the balanced mixed-sign regime.

### Why an estimate using only Au cannot work uniformly

Take three collinear points 0, ε, 1, with 0<ε<1, and charges

    u=(-ε/(1-ε), -ε, 1).

Then

    Au=(0,0,-2ε/(1-ε)),
    D=(4-4ε+4ε^2)/(1-ε)^2,
    |Au|^2/D=ε^2/(1-ε+ε^2) → 0.

In contrast, G_1=2, G_2=-2/(1-ε)^2, and
G_3=2ε(2-ε)/(1-ε)^2 along the line. These forces sum to zero, as translation
invariance requires. For 0<ε<1, max_i|G_i|=2/(1-ε)^2, so the full ratio is

    N/D = (4ε^2+2)/(4-4ε+4ε^2) → 1/2.

This is a rigorous obstruction to the proposed Au-only shortcut, not a
counterexample to the target inequality. It also shows why simply invoking
invertibility of a fixed interaction matrix does not give a uniform proof.

## Approach 2 A quantitative support transfer lemma

Let S={i:u_i≠0}, |S|=s≥2. Write D_S for the ordered-pair sum on S, and N_S for
the same left-hand side using the s-point configuration. Suppose its class of
active configurations has a uniform coordinate-norm estimate

    N_S ≥ c_s D_S.                                         (1)

Set C=1+4(2s-1)(p-s). Then the entire p-point configuration, with completely
arbitrary distinct inactive points, satisfies

    N ≥ min(c_s/C, 1/2) D.                                 (2)

Proof. Fix an inactive point x_k and choose j in S nearest to it. Set
b_i=u_i/|x_k-x_i| and P_k=sum_{i in S} b_i. For i≠j, the triangle inequality
and the choice of j yield

    |x_i-x_j|≤|x_i-x_k|+|x_j-x_k|≤2|x_i-x_k|,
    sum_{i in S\{j}} b_i^2≤4D_S.

Since b_j=P_k-sum_{i≠j}b_i,

    b_j^2≤2P_k^2+2(s-1)sum_{i≠j}b_i^2,
    sum_{i in S}b_i^2≤2P_k^2+4(2s-1)D_S.

Adding over inactive k proves

    D≤C D_S + 2 sum_{k outside S} P_k^2.

The forces at inactive indices vanish, while all forces at active indices
equal those of the restricted configuration. Likewise the active potential
rows are unchanged. Thus N=N_S+sum_{k outside S}P_k^2. Substituting (1) gives
D≤max(C/c_s,2)N, which proves (2). For s=1, directly N=|Au|^2=D. For s=0,
both sides vanish. These also cover all support boundary cases.

Consequences. The published p≤5 theorem gives a positive constant depending
only on p for all u with support at most five, even when there are arbitrarily
placed zero-charge points. A finite minimum over s=1,...,min(5,p) gives one
constant for that whole class. Collinear active supports of any fixed size
are handled in the same way using the published collinear theorem, even if
the inactive points are not on that line. With support size two and p>2 the
explicit constant 1/[1+12(p-2)] works, since N_S≥D_S; for p=2 use c=1.

This deduction does not handle a sequence whose every vector has six or more
nonzero entries. It is not a uniform extension from sparse vectors to all
vectors by continuity.

## Approach 3 Real variable zero exclusion and the six point planar gap

### A collinear proof by a cubic identity and inversion

Here is a direct proof that (Z) has only the zero solution on a line. Restrict
to the nonzero support. Support size one is impossible in a p≥2 zero system:
the potential at any other point would be nonzero. Thus s≥2. Order the
active coordinates x_1<...<x_s, and suppose a
nonzero solution exists. Every active force F_i is zero. Pairing symmetric
terms gives the algebraic identity, valid for arbitrary real charges,

    sum_i u_i x_i^3 F_i - (3/2) sum_i u_i x_i^2 P_i
      = -(1/2) sum_{i<j} u_i u_j |x_i-x_j|.                (3)

Indeed the numerator for each pair on the left is
(x_i^2+x_i x_j+x_j^2)-(3/2)(x_i^2+x_j^2)
=-(x_i-x_j)^2/2, divided by |x_i-x_j|. Under (Z), its distance energy
therefore vanishes.

The charges cannot all have the same sign, because an active potential
would then be nonzero. Thus some adjacent nonzero charges u_l,u_(l+1) have
opposite signs. On the interval (x_l,x_(l+1)), the continuous function

    f(a)=sum_i u_i/(x_i-a)^2

tends to infinities of opposite signs at the two endpoints. There is an
a in that interval with f(a)=0. Invert at a, with transformed points
y_i=a+1/(x_i-a) and transformed charges v_i=u_i/|x_i-a|. The Kelvin identity
proved below preserves (Z), so applying (3) to (y,v) gives

    0=sum_{i<j} v_i v_j |y_i-y_j|
     =sum_{i<j} w_i w_j |x_i-x_j|,
    w_i=u_i/(x_i-a)^2,   sum_i w_i=0.                    (4)

For any real weights summing to zero at ordered distinct points,

    sum_{i<j} w_i w_j(x_j-x_i)
      = -sum_{k=1}^{s-1} (x_(k+1)-x_k)
           (sum_{i≤k} w_i)^2.                           (5)

To see this, split each interval x_j-x_i into consecutive gaps. Across gap
k the coefficient is (sum_{i≤k}w_i)(sum_{j>k}w_j), the negative square in
(5). Every gap is positive. Equations (4)–(5) force all prefix sums, and
therefore all w_i and u_i, to vanish, a contradiction. This proves collinear
zero exclusion for every s. Combined inductively with the published
collision/escape equivalence, it gives the collinear uniform inequality.

No compactness step is claimed to follow from (3)–(5) alone. This proof is
independent of the complex-weight manipulation in the existing collinear
proof and is not presented as a novelty claim.

### A two off hyperplane obstruction

Assume every u_i is nonzero and (Z) holds, so that F_i=0. Suppose all but two
points lie in an affine hyperplane H and the remaining points a,b lie strictly
on the same side. Let their heights above H be h_a,h_b>0. For each i in H,
the normal component of F_i=0 implies

    u_a h_a/|x_i-a|^3 + u_b h_b/|x_i-b|^3=0.

Thus u_a,u_b have opposite signs and there is one K>0 with
|x_i-b|=K|x_i-a| for every i in H. The potential equations at a,b read

    sum_{i in H}u_i/|a-x_i| + u_b/|a-b|=0,
    (1/K)sum_{i in H}u_i/|a-x_i| + u_a/|a-b|=0.

They give u_b=K u_a, contradicting opposite signs. A single off-hyperplane
point is even easier: any force equation at a point of H forces its nonzero
charge to vanish. Both statements require at least one point in H.

### An enclosing sphere lemma with the needed hypothesis

Every finite set affinely spanning R^d admits an enclosing closed ball whose
boundary contains d+1 affinely independent members of the set. Here is a
proof which does not use a false claim about a minimum-radius ball. Lift each
x to (x,|x|^2) in R^(d+1). If the lifted set has affine dimension d, it lies
on the graph of one affine function (projection has rank d), so the original
set is cospherical. Otherwise its convex hull is full-dimensional. Its upper
boundary above the interior of the projected hull contains a nonvertical
facet with supporting plane t=2c·x+b, with every lifted point on or below it.
The facet's projection has dimension d and therefore includes d+1 affinely
independent original vertices. The inequalities |x|^2≤2c·x+b are exactly
|x-c|^2≤|c|^2+b, and equality holds at those vertices. The radius is positive
because the original set contains distinct points. This proves the lemma.

### Kelvin invariance and the reduction

For an inversion about a point N different from every x_i, put

    y_i=N+(x_i-N)/|x_i-N|^2,   v_i=u_i/|x_i-N|.

The identity |y_i-y_j|=|x_i-x_j|/(|x_i-N||x_j-N|) shows that the transformed
potential at y_i is |x_i-N|P_i. At a zero of P_i, the chain rule for the
external potential gives transformed force |x_i-N|^3 Q_i F_i, where Q_i is
the orthogonal reflection in the radial direction. Thus (Z) is preserved,
including nonvanishing of each charge. This also follows from [3,
Proposition 2.3]. A sphere through N becomes a hyperplane, and its interior
becomes one strict half-space.

For completeness, the same geometry proves zero exclusion through five
points, without using a complex collinear argument. For a smallest-support
nonzero solution with s≤5, all charges are nonzero. Its affine dimension is
at most s-2: if the s-1 difference vectors from one point were linearly
independent, its force equation would force all other charges to vanish.
For dimension d≥2, the enclosing-sphere lemma puts at least d+1 points on a
sphere. When s≤5 and d is 2 or 3, there are at most two interior points.
Inversion and the off-hyperplane obstruction either contradict the equations
or place every point in dimension d-1. Repetition reaches the line, where
(3)–(5) give the contradiction. The cases of one or two active points are
immediate. The same affine-dimension argument covers arbitrary ambient
dimension, since d≤s-2≤3. The published collision/escape equivalence then
converts this pointwise result into the p≤5 uniform theorem.

Now consider a nonzero six-point solution of (Z) in R^3. By p≤5 zero exclusion,
it must have full support: restricting to the support would otherwise give
a smaller nonzero solution. If the points are already coplanar, stop.
Otherwise take an enclosing sphere through at least four points using the
lemma. Choose N on that sphere but outside the finite point set. After
inversion, at least four points lie in one plane and at most two others lie
strictly on one side. The one- and two-off-plane obstructions rule out every
case except all six lying in the plane. Consequently any six-point null
configuration can be taken planar by a similarity and inversion.

Together with the published inductive zero-system criterion and the known
smaller cases, this shows that the six-point conjecture in R^3 is equivalent
to the six-point conjecture in R^2. This reduction follows the geometric
mechanism of the existing p≤5 proofs; it is not represented as a novel full
solution.

In the remaining planar case an enclosing circle need touch only three
points. Inversion then leaves three points on a line and three on one side.
The two-off-line argument no longer applies. If the line coordinates are
t_1,t_2,t_3 and the off-line points are (a_j,h_j), h_j>0, j=4,5,6, their
normal-force equations give

    sum_{j=4}^6 K_ij u_j=0,
    K_ij=h_j/[(t_i-a_j)^2+h_j^2]^(3/2), i=1,2,3.

Nonsingularity of K excludes that configuration, but no proof of universal
nonsingularity or of exclusion after imposing the other equations is given.
This is a concrete remaining gap, already at six active points.

### Audit of the older manuscript

The 2011 manuscript's p. 12 attempts to obtain four contact points from a
minimum-radius enclosing ball. The following exact six-point configuration
refutes that geometric assertion:

    (1,0,0), (-3/5,4/5,0), (-3/5,-4/5,0),
    (0,0,1/2), (0,0,-1/2), (0,1/4,0).

It spans R^3. Its unique smallest enclosing ball is the unit ball at the
origin, with exactly the first three points on its boundary. Those three
are not collinear. Weights 3/8,5/16,5/16 are positive, sum to one, and give
weighted center zero. For any proposed center c,

    sum_{i=1}^3 weight_i |x_i-c|^2 = 1+|c|^2.

Every enclosing radius therefore has R^2≥1+|c|^2≥1. The remaining squared
radii are 1/4,1/4,1/16, strictly below one. The circumcenter of the three
boundary points is zero, so the manuscript's division by its norm is also
undefined in this example. The general enclosing-sphere lemma above repairs
that geometric substep by allowing a non-minimal ball. It does not repair
the subsequent six-point planar step with three interior points. The
configuration is not claimed to satisfy (Z), and it refutes neither the
conjecture nor the claimed six-point theorem itself.

There is also a useful caution in reading the collinear argument of [3].
Its arXiv p. 24 / journal p. 1739 passes from a complex-weighted circle
identity to a signed sum by taking a real inner product. That implication
does not hold for unrestricted complex weights, including weights of the
displayed phase form. For y_1=1,y_2=i,y_3=-1, s=1, take
w_2=(1-i)/sqrt(2) and w_3=i sqrt(2). Then

    (y_2-y_1)w_2/|y_2-y_1|^2
      +(y_3-y_1)w_3/|y_3-y_1|^2 = 0,
    w_2+w_3=(1+i)/sqrt(2) ≠ 0.

These weights are w_k=exp(-i alpha_k/2)v_k with real v_2=1,v_3=-sqrt(2).
This example tests that local algebraic inference, not all the simultaneous
equations in the paper, and is not a counterexample to its theorem. Equations
(3)–(5) give an independent real-variable route to the same collinear
conclusion, so none of the corollaries here depends on that inference.

## Approach 4 A two ring symmetric ansatz cannot give an exact zero

Consider two coplanar concentric regular n-gons, n≥3. Their radii are 1 and
t, 0<t<1, and their relative rotation is θ. Give all outer points the same
charge α and all inner points the same charge β. Define

    L = sum_{k=1}^{n-1} [2 sin(πk/n)]^(-1),
    S(t)=sum_{k=0}^{n-1}[1+t^2-2t cos(θ+2πk/n)]^(-1/2).

Every outer potential is Lα+Sβ; every inner potential is Sα+(L/t)β.
If both vanish with nonzero charges, S=L/sqrt(t) and β=-sqrt(t)α.
Neither charge can be zero in a nontrivial zero-potential vector.

The quadratic energy is

    E(t)=u^TAu=nLα^2+nLβ^2/t+2nS(t)αβ.

When differentiating, the charges α,β are held fixed. At a zero-potential
configuration, substitution of the relations above gives

    E'(t)=-2nα^2 H'(t),
    H(t)=sqrt(t)S(t)
        =sum_k [t+t^(-1)-2cos(θ+2πk/n)]^(-1/2),
    H'(t)=(t^(-2)-1)/2
           * sum_k [t+t^(-1)-2cos(θ+2πk/n)]^(-3/2)>0.

Hence E'(t)≠0. If all coordinate forces G_i vanished, differentiating E
along this radial motion of the inner polygon would instead give E'(t)=0.
This contradiction rules out exact zeros for this entire ansatz, including
two concentric triangles (six points). Radii in the opposite order are
handled by interchanging rings and rescaling.

For equal radii and distinct points, the configuration lies on one circle;
inverting about another point of the circle turns it into a collinear
configuration. The known collinear theorem and Kelvin invariance rule out
an exact zero there as well. Colliding points are excluded by the problem.

This is an exact zero-exclusion result with a symmetry restriction on the
charges. It supplies no all-configuration coercivity constant, and arbitrary
charges on the two polygons are outside this argument.

## Approach 5 Finite variational exploration

search_numeric.py runs deterministic seeded starts for (p,dimension) equal to
(6,2), (6,3), (7,3), and (8,3). Each optimization uses a smooth nonnegative
residual with the same zero set as (Z); NUMERIC_RESULTS.json reports the
actual coordinate-max ratio N/D separately. The coordinate gauge fixes the
first two points and normalizes charges during evaluations. No point data
were taken from a third-party dataset.

Only finitely many starts and finite evaluation budgets are used. Local
termination, positive output values, or small residuals establish neither
a positive global lower bound nor a genuine zero. The outputs are preserved
to expose what was tested, not to promote a numerical conjecture to a proof.

## Final unresolved task

No proof or counterexample for all p has been produced. The sharpest specific
remaining obstacle isolated here is the planar, mixed-sign, full-support
six-point zero system, especially the three-on-line/three-on-one-side case
after inversion. For arbitrary p one must exclude all nonzero systems (Z)
with at least six active points and use a valid uniformity argument. Neither
the sparse estimates nor the symmetric ansatz excludes those configurations.

## References

[1] Thomas Bartsch and Andrew Dancer, organizers, *Topological and Variational
Methods for Differential Equations*, Oberwolfach Reports 2 (2005), 1601–1678,
published June 30, 2006. Bahri contribution at pp. 1658–1660.
https://ems.press/journals/owr/articles/1050
https://ems.press/content/serial-article-files/46004
DOI: https://doi.org/10.4171/OWR/2005/29

[2] Yongzhong Xu, *Note on an inequality*, Ann. Inst. H. Poincaré Anal.
Non Linéaire 23 (2006), 629–639.
https://ems.press/journals/aihpc/articles/4077561
https://www.numdam.org/article/AIHPC_2006__23_5_629_0.pdf
DOI: https://doi.org/10.1016/j.anihpc.2005.07.002

[3] Hong Chen, Jianquan Ge, Kai Jia and Zhiqin Lu, *On a Conjecture of
Bahri–Xu*, Acta Mathematica Sinica, English Series 37 (2021), 1721–1742.
https://arxiv.org/abs/2101.10023
https://arxiv.org/pdf/2101.10023
https://lu.math.uci.edu/pdfs/publications/2021-2025/66.pdf
https://actamath.cjoe.ac.cn/Jwk_sxxb_en/EN/lexeme/showArticleByLexeme.do?articleID=23863
DOI: https://doi.org/10.1007/s10114-021-0027-0

[4] Shiwei Lan and Zhiqin Lu, *On a Conjecture of Bahri-Xu*, author-hosted
manuscript internally dated March 9, 2011, 13 pages. No publication status
is inferred from its search-index crawl date.
https://lu.math.uci.edu/pdfs/publications/other-papers/barhi-5.pdf
