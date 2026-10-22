# Scoped mathematical results and remaining gaps

## 1. Exact target and conventions

Write k for the real dimension, n for the ambient dimension, and q=n-k.
The nontrivial target is 1 <= q < k. Let F:M^k -> R^n be a connected,
smooth, complete, boundaryless isometric immersion, with an embedded image
when interpreting the source's notation M subset R^n as a submanifold.
In the oriented-current interpretation its multiplicity-one current is
locally area minimizing against all compactly supported current competitors.
This implies minimality and stability for all compactly supported smooth
normal variations. No converse is used.

With H=trace A, the Euclidean Gauss equation gives

    Scal = |H|^2 - |A|^2.

Thus for a minimal immersion Scal=-|A|^2 <= 0, and the source's critical
curvature is T(M)=integral |A|^k = integral (-Scal)^(k/2).
An alternate scalar-curvature normalization by a fixed positive dimensional
factor leaves finiteness unchanged. It does not change the exponent k/2.
Finiteness of a signed integral, or finiteness of integral |Scal| when k>2,
is a different assertion and is not substituted here.

The target asks whether T(M)<infinity and k>n/2 force A=0. For connected
complete M, A=0 implies that its image is an entire affine k-plane:
parallel transport makes the tangent plane fixed; the image lies in the
corresponding affine plane; the resulting complete local isometry covers
that plane, which is simply connected. Disconnected unions require a
componentwise formulation. Allowing arbitrary boundary or incomplete pieces
would change the question. No counterexample exploiting those omissions is
claimed. The codimension-zero case is already flat; in positive codimension
the inequality leaves no k=1 case.

## 2. Route 1: ends, monotonicity, and ordinary catenoids

Anderson's Theorems 5.1 and 5.2 in *The Compactification of a Minimal
Submanifold in Euclidean Space by the Gauss Map* give: when k>=3 and
T(M)<infinity, there are finitely many ends, each has multiplicity one at
infinity, and a one-ended M is an affine plane. This is a prior result.
The mechanism is that the normalized extrinsic volume ratio tends to 1 at
infinity for a single end, starts at 1 at a smooth point, and is monotone;
equality implies a plane.

Shen and Zhu's 1998 Main Theorem independently handles every complete
oriented stable Euclidean hypersurface with finite critical curvature.
Consequently the area-minimizing hypersurface case, including k=2,n=3,
is a credited prior affirmative special case.

### An explicit instability check

The ordinary rotational k-catenoid, k>=2, of neck radius 1 has arclength
coordinate s in R, radius r(s)>=1, and metric

    ds^2 + r(s)^2 g_(S^(k-1)).

Its profile satisfies r'^2=1-r^(-2k+2), r''=(k-1)r^(-2k+1), and its
principal curvatures are r^(-k), repeated k-1 times, and -(k-1)r^(-k).
Hence |A|^2=k(k-1)r^(-2k). Set f=r^(1-k)>0. Direct differentiation gives

    (Delta + |A|^2) f = (k-1) r^(-k-1) > 0.                 (1)

For a smooth cutoff chi_R equal to 1 for |s|<=R, zero for |s|>=2R,
and |chi_R'|<=C/R, the integration-by-parts identity is

    Q(chi_R f)
      = integral f^2 |grad chi_R|^2
        - integral chi_R^2 f (Delta+|A|^2)f.                (2)

All integrals here use the catenoid's volume form. Since r(s) is comparable
to 1+|s| at infinity, the first term tends to zero: it is O(R^(-k)) for
k>2 and O(R^(-2)) for k=2. The second term tends to

    (k-1) vol(S^(k-1)) integral_R r(s)^(-k-1) ds > 0,

a finite positive number. Thus Q(chi_R f)<0 for sufficiently large R.
The normal field can be taken inside the (k+1)-dimensional affine span,
so the same instability holds after inclusion into any larger R^n.
An ordinary catenoid cannot satisfy the target's minimizing hypothesis.

Moore's 1995 thesis and 1996 published Theorem 1 state a two-ended classification when k>=3 and
k>n/2. If that classification is taken as an input, (1)-(2) exclude the
two-ended connected nonflat minimizing case. This packet does not silently
upgrade that conditional deduction to an independently reproduced theorem;
the source audit in SOURCE_GATE.md records a nontransverse-intersection
issue in the inspected thesis and journal proofs.

**Gap:** the unconditional one-end and hypersurface conclusions do not
force a higher-codimension minimizing M to have one end. Even granting the
two-end classification, three or more ends remain untreated.

## 3. Route 2: tangent-plane cones and intersection

The source suggests using that tangent cones at infinity consist of planes
and retain area minimization. Dimension counting gives

    dim(P intersect Q) >= 2k-n > 0

for two linear k-planes. But that is not a contradiction to area minimization.

### A calibrated cone with intersecting planes

For k>=3, work in R^(k-2) times C^2 = R^(k+2), with coordinates
t_1,...,t_(k-2),x_1,y_1,x_2,y_2. Let

    P = R^(k-2) times (C times {0}),
    Q = R^(k-2) times ({0} times C).

Orient both with the product complex orientation. The constant k-form

    phi = dt_1 wedge ... wedge dt_(k-2)
          wedge (dx_1 wedge dy_1 + dx_2 wedge dy_2)

is closed and has comass one. One way to see the comass assertion is to
use the Hodge star in R^(k+2): up to orientation, star(phi) is the standard
Kahler 2-form on the C^2 factor, zero on the t-directions. Its skew operator
has norm one, so its value on every orthonormal pair has absolute value at
most one; Hodge star identifies unit simple complementary multivectors.
The form restricts to the oriented volume form of P and of Q. Therefore
the integral current [P]+[Q] is area minimizing by the calibration inequality
and Stokes' theorem for compactly supported competitors.

Here k>(k+2)/2, and P intersect Q=R^(k-2), which has positive dimension.
This is a counterexample to the proposed *cone obstruction*, not to the
question: the support is singular along P intersect Q and is not a smooth
submanifold. Integrating curvature on its regular part alone is not the
source's smooth finite-total-curvature hypothesis.

### Intersecting limits need not force intersection before the limit

In R^6 take affine 4-planes

    L_1 = span(e_1,e_2,e_3,e_4),
    L_2 = e_6 + span(e_1,e_2,e_3,e_5).

They are disjoint because their sixth coordinates are respectively 0 and
1. Their directions P_1,P_2 meet in a 3-plane. On rescaling by 1/R, their
links on S^5 are disjoint smooth 3-spheres, converging smoothly to distinct
great 3-spheres that meet in S^2. More explicitly the second link has
x_4=0, x_6=1/R, and radius sqrt(1-R^(-2)) in its four free coordinates.

The limiting intersection is nontransverse. The example only tests an
intersection inference, not the full connected-minimal hypotheses of an
end-classification theorem. If P_1+P_2=R^n, transverse intersection is
locally persistent; the inequality 2k>n does not imply this equality.

**Gap:** one needs additional information about which minimizing plane
cones can be realized by the smooth finite-curvature ends of one M.
Neither cone minimization nor dimension counting supplies that information.

## 4. Route 3: the normal stability operator

For a compactly supported normal field V on a Euclidean minimal immersion,

    Q(V)=integral ( |nabla^perp V|^2
                   - sum_(i,j) <A_ij,V>^2 ).              (3)

In codimension one a global unit normal turns (3) into scalar stability,
integral |A|^2 f^2 <= integral |grad f|^2. In higher codimension that
inequality is an additional hypothesis; the vector inequality alone does
not identify a global parallel normal direction carrying all of A.

A natural attempt is to use the normal projections of constant ambient
orthonormal vectors a_1,...,a_n. Put V_alpha=f a_alpha^perp. At any point,

    nabla_i^perp(a_alpha^perp) = -A(e_i,a_alpha^T).

Orthogonal completeness of the a_alpha yields

    sum_alpha |a_alpha^perp|^2 = q,
    sum_alpha <a_alpha^perp,A(e_i,a_alpha^T)> = 0,
    sum_(alpha,i) |A(e_i,a_alpha^T)|^2 = |A|^2,
    sum_(alpha,i,j) <A_ij,a_alpha^perp>^2 = |A|^2.

Expanding (3) therefore gives exactly

    sum_alpha Q(f a_alpha^perp) = q integral |grad f|^2.   (4)

The curvature terms cancel. This identity is valid irrespective of q<k.
It is not an instability estimate and does not force A to vanish.
The distinction is consistent with Wang's 2003 theorem for *super stable*
submanifolds, which explicitly imposes the stronger scalar condition.

**Gap:** no mechanism deriving an appropriate coercive scalar inequality,
or a negative vector test field, from the target's hypotheses was obtained.

## 5. Route 4: calibrated examples and the product trap

The holomorphic graph F:C -> C^2, F(z)=(z,z^2), is an embedded complete
nonflat minimal surface. Its induced metric is

    g=(1+4|z|^2)(dx^2+dy^2),

so completeness follows from g>=dx^2+dy^2. Its complex orientation is
calibrated by the constant Kahler form; the image is proper and hence
defines an area-minimizing locally integral current. For r=|z|, the
conformal curvature formula gives

    K=-8/(1+4r^2)^3,        |A|^2=-2K=16/(1+4r^2)^3.

Consequently

    integral |A|^2 dV
      =32 pi integral_0^infinity r/(1+4r^2)^2 dr = 4 pi.  (5)

This is a complete nonplanar calibrated finite-curvature example at the
excluded equality k=n/2=2. It does not satisfy the strict inequality.

For every k>=3, the product F(C) times R^(k-2) lies in R^(k+2), now with
k>(k+2)/2, and remains complete, embedded, and calibrated. Nevertheless
it has infinite T(M). More generally, if a smooth submanifold N has A_N
nonzero somewhere and d>=1, then on N times R^d the second fundamental
form is pulled back from N. There is a compact positive-volume patch U
and c>0 with |A_N|>=c on U. For the product dimension k=dim(N)+d,

    integral_(U times [-R,R]^d) |A|^k dV
       >= c^k vol(U) (2R)^d -> infinity.                 (6)

This argument applies to Euclidean products of nonflat Lawlor necks as
well. It does not depend on whether the integral over N itself is finite.

**Gap:** crossing the dimensional threshold by adding a Euclidean factor
destroys the required integrability. An actual smoothing or gluing would
need to control the whole curvature integral, smoothness, completeness,
and minimizing property, none of which follows from the product model.

## 6. Route 5: small-energy rigidity and scale invariance

Under dilation F -> lambda F, the metric and second fundamental-form norm
scale as dV -> lambda^k dV and |A| -> lambda^(-1)|A|. Thus

    T(lambda M)=T(M).                                    (7)

It is impossible to turn an arbitrary finite T(M) into a small one by
rescaling. Finiteness does make the energy of the complement of larger
compact sets tend to zero; it need not make the energy of the compact
core tend to zero.

For completeness, the standard small-energy route can be seen from the
Simons and Sobolev inputs, written here as explicit additional inequalities.
Put u=|A| and suppose the weak differential inequality

    u Delta u >= -c u^4

and the Sobolev inequality ||w||_(2k/(k-2))^2 <= S integral |grad w|^2
hold, with k>=3 and fixed positive c,S. For a cutoff eta and v=u^(k/2),
integration by parts, Young's inequality, and Holder's inequality give

    integral |grad(eta v)|^2
      <= c k^2/(k-1) integral u^2 (eta v)^2
         + [2k^2/(k-1)^2+2] integral u^k |grad eta|^2,

and

    integral u^2 (eta v)^2
       <= T(M)^(2/k) ||eta v||_(2k/(k-2))^2.

Hence if S c k^2/(k-1) T(M)^(2/k)<1, the main term can be absorbed.
Cutoffs with |grad eta_R|<=C/R make the remaining term tend to zero,
and exhaustion forces u=0. At zeros of u the same conclusion follows by
the usual positive regularization before taking its limit. This is a
conditional derivation from the stated standard analytic inputs, not a
new source-free proof of those inputs or a sharp constant claim.

The same absorption on an exterior region only gives exterior control;
its inner boundary is fixed and cannot be discarded. This is why curvature
decay/compactification results do not automatically imply global flatness.

**Gap:** neither the strict dimension bound nor minimization was shown to
force the global smallness required by this route. Equation (7) blocks the
proposed rescaling shortcut.

## 7. Unresolved statement

The full connected, smooth, complete, boundaryless area-minimizing problem
for 2<=q<k remains unresolved by this investigation. A nonflat example
would have more than one end by the verified Anderson result. If Moore's
two-end classification is accepted as an additional input, it must have
at least three ends. No such example is constructed here, and no proof
that it cannot exist is given. Source-based special cases and the algebraic
obstructions above are not a full resolution. All standard constructions,
identities, and cited theorems are credited; no novelty claim is made.
