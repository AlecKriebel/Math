# Independent adversarial audit of the flag-curve analytic route

Prepared 2026-10-16T07:46:55Z, UTC. This is a mathematical route audit, not a whole-publication clearance or a novelty/priority finding. The frozen plan predates intake of Root's route. No original PROOF.md or prior favorable verdict was read. No other PR was reviewed. All authored work is confined to this folder.

## Verdict and exact scope

**The proposed route is verified for the following precise theorem.** Let

    E: x^2/a^2 + y^2/b^2 = 1,
    C: x^2/(a^2-lambda) + y^2/(b^2-lambda) = 1,
    a>b>0, 0<lambda<b^2.

Suppose the real directed Poncelet dynamics for this pair has primitive least period N=4k. For each fixed finite real point M, let A be the signed area of the N original vertices in traversal order and B_M the signed area of the perpendicular feet of M on the N original side **lines**, in side order. Then A B_M is independent of phase. This includes every coprime winding number for which such a pair closes, both traversal orientations, and zero or negative B_M. The proof also works with M a fixed finite complex point, although the intended geometry is real.

I found no unresolved analytic gap in this route. It uses standard facts about smooth double covers, Riemann-Hurwitz, holomorphic functions on compact curves, and genus-one uniformization (or the equivalent Abel-Jacobi description of automorphisms preserving the holomorphic differential). The proof below supplies the real-component argument, all local valuations, and the branch cancellation rather than assuming them.

The word **least** is material. This theorem does not assert that an arbitrarily repeated vertex list of length divisible by four satisfies the invariant. A doubled primitive six-periodic trajectory gives a 12-entry list whose product varies with phase; a reproducible control is recorded below. Thus an unqualified interpretation of N as any repeated list length is false. The primary source's Table 3 does not literally insert a least-period qualifier, so this audit must not silently claim that the theorem resolves every possible literal repeated-list interpretation.

## Source convention checked directly

Read-only text extraction of RGK arXiv v11 PDF page 3 gives its explicit declaration that polygon areas are signed and equation (1), S=(1/2) sum_i W_i cross W_(i+1). ArXiv PDF page 6, Table 3, places k203,a at A A_m, N congruent to 0 mod 4, all M, with no claimed value and an unproved marker. The same row is present on printed journal page 346 (PDF page 6). Table 3 concerns pedals with respect to N-periodic sides, distinct from the outer-polygon pedal in Table 4. These convention checks use the files in the parent primary_source_private folder; they supply no novelty conclusion.

## 1. Explicit flag curve and branch calculations

Put

    A0=a^2, B0=b^2, p=A0-lambda, q=B0-lambda, c=A0-B0=p-q>0.

The subscript distinguishes squared semiaxes A0,B0 from the area A. In projective coordinates P=[x:y:z] and line coordinates L=[u:v:w], the incidence curve is

    X = { x^2/A0+y^2/B0-z^2=0,
          p u^2+q v^2-w^2=0,
          u x+v y+w z=0 }.

Let pi forget L and rho forget P. The map sigma exchanges the two E endpoints on a caustic tangent; tau exchanges the two caustic tangents through P. Both are regular involutions of X. The dual conics are

    C*: p u^2+q v^2-w^2=0,
    E*: A0 u^2+B0 v^2-w^2=0.

On C*, write D=u^2+v^2 and H=A0 u^2+B0 v^2. Then

    H-w^2=lambda D.                                      (1)

On a line-coordinate chart, an explicit endpoint formula is

    eta^2=A0 B0 lambda D,
    P=[-A0 u w-v eta : -B0 v w+u eta : H].              (2)

It is valid wherever the displayed triple is nonzero and extends by incidence elsewhere. Direct substitution gives L(P)=0 and x^2/A0+y^2/B0=z^2: the cross terms cancel and the remaining expression is H(w^2+lambda D)=H^2. The endpoint exchange is eta -> -eta. The double-cover discriminant is therefore D on C*.

The only zeros of D on C* are the four lines

    L_(epsilon,delta)=[1:epsilon i:delta sqrt(c)],
    epsilon,delta in {+1,-1}.                            (3)

They are exactly all common E/C tangents, by (1). On the chart u=1, v is a local coordinate there because w0!=0 and w^2=p+q v^2; dD/dv=2 epsilon i!=0. Consequently the four zeros are simple and rho branches simply at their four unique endpoint flags. There are no unlisted intersections at line-coordinate infinity: w=0 with D=0 would force c=0 or u=v=0, both impossible. In particular the isotropic tangencies are finite lines, and their E contact points are finite:

    P0=[A0: B0 epsilon i: -delta sqrt(c)].                (4)

The branch calculation proves X is a smooth double cover of the smooth conic C*, with four simple branch points. Outside them the two E intersections are transverse and the incidence map is unramified. A branched smooth degree-two cover of P1 is connected (a disconnected degree-two cover would consist of two degree-one covers and have no branch). Riemann-Hurwitz gives genus(X)=1. This establishes smoothness and connectedness globally, including charts where (2) needs cancellation.

As a separate check on the other projection, pi branches precisely at the four transverse points E intersect C:

    x^2=A0 p/c, y^2=-B0 q/c, z=1.                       (5)

All their x,y,z are nonzero, and the two conic gradients are not proportional since A0/p != B0/q. In particular pi is unramified over both E points at infinity.

One completely explicit rational base model is

    [u:v:w]=[beta(1-r^2):2 alpha r:-alpha beta(1+r^2)],
    alpha=sqrt(p), beta=sqrt(q),
    eta^2=A0 B0 lambda [q(1-r^2)^2+4p r^2].              (6)

The quartic on the right has four distinct roots for p>q>0, matching (3). This is an independently checkable genus-one model.

## 2. Dynamics, least order, real circles, and all stars

Both sigma and tau have fixed points and genus-zero quotients. Equivalently, at any simple branch point their derivatives are -1. A nonzero holomorphic differential omega on a genus-one curve has no zeros; hence sigma*omega=tau*omega=-omega. For

    T=tau sigma,

we have T*omega=omega. Under uniformization X=C/Lambda, its lift therefore has derivative 1 and is z -> z+d. Thus T is a translation. A primitive real T orbit of period N implies Nd belongs to Lambda and no smaller positive multiple does; T has exact order N on the entire complex curve. Every nonidentity power of T is fixed-point-free. This deduction also gives porism; no prior porism or area theorem is required.

Here is a real-component argument that does not assume convex vertex order. Normalize every real caustic tangent as

    n(phi)=(cos(phi)/alpha,sin(phi)/beta), w=-1,
    q0(phi)=(alpha cos(phi),beta sin(phi)),
    d0(phi)=(-sin(phi)/beta,cos(phi)/alpha).

Every endpoint is uniquely P=q0+s d0. Because q0 is strictly inside E, substituting this expression in E gives a quadratic in s with positive leading coefficient and negative constant term. Its roots are distinct, one positive and one negative, continuously periodic in phi. Thus X(R) consists of two circles labeled by sign(s), and sigma exchanges these circles.

For a fixed P on E, let h(phi)=n(phi) dot P. Its tangent equations h=1 have two distinct real solutions because P is strictly outside C. Since

    h'(phi)=s/(alpha beta),

the two solutions have opposite signs of s. Therefore tau also exchanges the two circles; T preserves each. Each circle maps homeomorphically to E(R) under pi (one of the two tangent choices at every P lies on each component). In particular a real vertex's least return period equals its flag's least return period.

Central inversion I acts by

    (P,[u:v:w]) -> (-P,[u:v:-w]).

It commutes with sigma,tau,T. It preserves each real circle: phi -> phi+pi, q0 -> -q0, d0 -> -d0, s unchanged. On that circle it is orientation preserving, because under the homeomorphism pi it is the central half-turn of the ellipse. T is orientation preserving as well: it preserves omega, whose restriction, after real scaling, is a nonvanishing real differential on each real circle.

The finite group generated by commuting T and I preserves either circle and its orientation. Its action is faithful, since an automorphism identical on a real circle is identical on the connected complex curve. A finite orientation-preserving circle group is cyclic: ordering any finite orbit cyclically embeds the group into the cyclic rotations of that orbit, since a finite-order orientation-preserving circle map with a fixed point is the identity. Consequently this group has a unique nonidentity element of order two. When N=2m is even, T^m and I are both such elements, so

    I=T^m.                                               (7)

Equality on the circle extends analytically to X. The argument uses no assumption about consecutive vertices being adjacent in convex boundary order. For a star the rotation number is r/N with gcd(r,N)=1; it is simply another faithful finite circle action. In particular when N is even its primitive numerator r is odd, consistent with (7). Reversing traversal replaces T by T^-1 and does not affect the identity.

## 3. Original area: exhaustive poles, each at most simple

Use affine Euclidean coordinates for finite vertices and define

    P_j=pi(T^j x), L_j=rho(T^j x),
    2 A(x)=sum_(j mod N) det(P_j,P_(j+1)).               (8)

These are meromorphic functions on X; T invariance follows by cyclic index shift. On E, each affine coordinate has a simple pole at the two infinities

    P_infinity,epsilon=[a:epsilon i b:0].                (9)

By (5), pi is unramified there, so pulled-back coordinates have no worse order. Let S be the union of the T orbits of the four flags above (9).

No pair of consecutive original vertices is infinite. Their common side is a caustic tangent. If they are the two distinct E infinities, their joining line is z=0, which is not tangent to C. If they coincide at one E infinity, their common side would be the E tangent at that infinity. That tangent has line coordinates [1/a:epsilon i/b:0], for which

    p/a^2-q/b^2=lambda(1/B0-1/A0)!=0;

it is not tangent to C either. These exhaust the ways a line intersects E twice at infinity, including tangency multiplicity. Hence every summand of (8) has at most one simple-pole factor. A has poles of order at most one, supported on S, even if multiple nonadjacent vertices diverge at the same flag.

At a flag x above (9), normalize v=1. Incidence gives u=-epsilon i b/a, and the two tangent choices have

    w^2=-lambda c/A0!=0.                                 (10)

Tau exchanges the signs of w. Central inversion fixes the projective P infinity and exchanges the same signs. Therefore tau x=I x=T^m x. Since tau=T sigma,

    sigma x=T^(m-1) x.                                  (11)

For an explicit infinity chart, take homogeneous x=a,

    y=epsilon i b sqrt(1-z^2),
    P_affine=(a/z,epsilon i b/z+O(z)).                    (12)

The two w solutions in (10) are simple and continue analytically as z varies. Thus z is also a local coordinate on each flag sheet, confirming the simple pole rather than assuming an unramified pullback.

## 4. Pedal-foot map and its only possible poles

For a fixed finite point M=(Mx,My), the perpendicular foot on L=[u:v:w] is the rational function

    Q_M(L)=M-[(u Mx+v My+w)/(u^2+v^2)](u,v).             (13)

It is invariant under scaling the line coordinates. The homogeneous degree-two numerator/denominator expression is regular wherever D!=0, including all line-coordinate points with w=0. Thus the only possible poles on C* are exactly the four simple zeros (3) of D. A zero numerator for a special M can cancel a pole; it cannot create a new one. For real M this includes the familiar removable poles at the foci. At every remaining point, (13) has order at most one on C*.

The pullback to X is branched, so the bound on X is order at most **two**. An explicit exact chart at any of the four branch flags is u=1 and t=eta, with

    v(t)=epsilon i sqrt(1-t^2/(A0 B0 lambda)),
    w(t)=delta sqrt(c+q t^2/(A0 B0 lambda)),
    D(t)=t^2/(A0 B0 lambda), sigma(t)=-t.                 (14)

In particular

    Q_0(t)=M-(A0 B0 lambda/t^2)
                [Mx+v(t) My+w(t)](1,v(t)).              (15)

This is an even Laurent series with order at most two. This explicit chart verifies the branch and the pole order simultaneously. Treating this pullback as unramified would be an error; the route under audit correctly avoids it.

Let R be the union of the T orbits of Fix(sigma), and write Q_j(x)=Q_M(L_j(x)). Every possible foot pole belongs to R. If z is sigma-fixed and T^j z is also sigma-fixed, the relation sigma T^j=T^-j sigma gives T^(2j)z=z. Exact translation order implies

    j=0 or m modulo N=2m.                                (16)

Thus at z only Q_0 and Q_m can be singular. They are nonadjacent for m>=2, including m=2.

## 5. Area cancellation at R, including N=4

Define the signed side-pedal area

    2 B_M(x)=sum_(j mod N) det(Q_j,Q_(j+1)).             (17)

Since rho sigma=rho,

    Q_j(sigma x)=Q_-j(x).                                (18)

In the coordinate (14), Q_0 and Q_m are even Laurent series with possible order two; the second assertion follows from -m=m mod N. Every Q_j with j!=0,m is holomorphic by (16). Equation (18) implies

    Q_1-Q_-1=O(t),
    Q_(m+1)-Q_(m-1)=O(t).                               (19)

The entire possibly singular part of (17) is

    det(Q_0,Q_1-Q_-1)
      +det(Q_m,Q_(m+1)-Q_(m-1)).                        (20)

All other edges join regular feet. Combining the order-two even poles with (19) makes (20) have order at most one. A vanishing leading coefficient for any special M only reduces this bound.

For N=4,m=2 there are no unlisted regular edges. Explicitly (20) is

    det(Q_0,Q_1-Q_3)+det(Q_2,Q_3-Q_1),

which expands to the four directed edges 0->1,1->2,2->3,3->0, each exactly once. Shared neighbors do not cause double-counting. Consequently B_M has at most simple poles, supported on R, for the smallest case as well as all higher 4k cases.

## 6. Disjoint supports and complementary regular zeros

Suppose x lies above an original infinity, so (11) holds. If T^k x were sigma-fixed, then

    T^k x=sigma T^k x=T^(m-1-k)x,
    2k=m-1 mod 2m.                                      (21)

When m is even the right-hand side is odd, so this congruence is impossible. Therefore S and R are disjoint. This parity step is exactly where N divisible by four is used.

At a sigma-fixed z in R, all P_j are finite by disjointness. Since pi tau=pi, tau=T sigma, and tau T^j=T^-j tau,

    P_j(z)=P_(1-j)(z).                                  (22)

This is reversal of the vertex cycle up to a cyclic shift. A cyclic shoelace sum changes sign under reversal, hence A(z)=0. Since A is holomorphic at z, its zero has order at least one (or A is identically zero, which is harmless).

At an original-infinity flag x, all feet are regular by disjointness. Since rho sigma=rho and (11) holds,

    L_j(x)=L_(m-1-j)(x),
    Q_j(x)=Q_(m-1-j)(x).                                 (23)

The pedal cycle is reversed up to a cyclic shift, so B_M(x)=0. It is a zero of a regular function and has order at least one. Both zero identities extend to every T translate by the cyclic invariance of the areas. They are identities of the actual side-indexed feet for the same fixed M; no transformation of M is used.

For completeness, if a cyclic list W obeys W_j=W_(c-j), its area sum S obeys

    S=sum det(W_(c-j),W_(c-j-1))=-S.

This algebra proves the reversal cancellation even with repeated vertices and for c odd or even. It does not rely on a picture or non-self-intersection.

## 7. Holomorphic product and exact conclusion

The full pole list is now exhausted. At S, A has at most a simple pole and B_M has a regular zero. At R, B_M has at most a simple pole and A has a regular zero. Elsewhere both are holomorphic. Hence A B_M is holomorphic on the connected compact curve X and is constant.

One may also descend to Y=X/<T>. Because T is an exact-order translation, its cyclic action is free; the quotient is an unramified compact genus-one quotient. Both trace areas descend. Their supports and complementary zero orders are preserved by the unramified quotient map. This descent is valid, but the direct compact-X proof already suffices and avoids making the quotient an additional dependency.

The proof never divides by A or B_M. Thus zero pedal area is included; negative signed pedal area is included; changing traversal orientation changes each signed area's sign and leaves the product unchanged. All line feet in (13) are on the entire original side lines. Nothing imposes a side-segment restriction. Arbitrary fixed M enters only in a polynomial numerator, so no generic-M assumption survives in the proof.

Circle a=b, lambda=0, the focal degeneration lambda=b^2, and other singular/nonproper complex pairs are excluded explicitly. The transversality, branch count, and disjointness arguments must not be extended to those limits without a separate limiting theorem. No such extension is needed for the precise claim.

## 8. Reproducible checks and attempted falsification

`verify_controls.py` reads the pre-existing mpmath installation in the sibling pr200 audit, runs with Python -B, writes no data, and uses 80 decimal digits. It constructs each Poncelet step from tangent incidence and the second intersection with E, solves the closure equation by bisection, computes the feet directly from consecutive vertex pairs, and tests phase variation, caustic tangency, closure, and signed reversal. These are numerical controls, not a validated-computation substitute for the proof.

For a=2,b=1 the following primitive cases were checked at four phases and M=(0,0),(2.3,-1.7),(20,13),(sqrt(3),0):

| N, winding r | lambda | maximum relative product spread |
|---|---|---|
| 4,1 | 0.8 | 2.3e-75 |
| 8,1 | 0.2677523569258437738377986406 | 5.8e-76 |
| 8,3 | 0.9987280303912020403292483407 | 2.2e-73 |
| 12,1 | 0.1246519558388970403629733 | 4.3e-76 |
| 12,5 | 0.9999934255223711728566888931 | 2.5e-71 |

The worst closure error was 3.9e-71 radians and the worst normalized tangent-equation residual 8.4e-72, in the near-degenerate 12/5 case. For 8/3, A B at M=(2.3,-1.7) was approximately -5.4153596577275083993, whereas at M=0 it was approximately +3.2044745128023725697. This explicitly exercises negative pedal area. An x-axis zero-pedal point M approximately (1.74383587227446952405575818516,0) gave maximum |A B|<1.7e-73 over the four independent phases.

An exact N=4 comparison is also available without numerical closure solving. For A0=4,B0=1,lambda=4/5:

* The diamond with vertices (2,0),(0,1),(-2,0),(0,-1) has A=4, B_M=32/25 for every M, hence A B_M=128/25. Exact Fraction arithmetic checked M=(0,0),(7/3,-5/2),(100,100).
* The same confocal pair has the axis-parallel rectangle with vertices (+/-4/sqrt(5),+/-1/sqrt(5)), cyclically ordered. It has A=16/5, B_M=8/5 for every M, again A B_M=128/25. The change of original area between these phases is a useful nontrivial control.

Outside-scope falsification: solve the primitive 6/1 closure condition and repeat that six-vertex polygon twice. It is now a 12-entry list but its least period is six. At M=0, the four phase products in script order were

    76.82533453624915, 78.63531195335193,
    78.06222695675632, 76.96299075811277.

Therefore a claim covering arbitrary repeated lists solely because their displayed length is divisible by four would fail. This does not falsify the precise primitive theorem, and the proof identifies the obstruction: m based on a repeated list is not the half-order of T.

Adversarial issues actively checked: branch pullback doubling; possible finite/line-infinity poles; common-tangent exhaustiveness; singular X; real-component switching; nonconvex winding; exact versus assumed period; central involution; adjacent infinite vertices; multiple pole indices; shared neighbors at N=4; cancellation for special M; fixed-M indexing of both reversals; quotient ramification; signed zero and negative B; and repeated-list scope. None yields a gap within the stated theorem. No AA-prime invariant or prior PR result was used.

Family record: the mechanism audited here is meromorphic pole cancellation on the tangent-incidence genus-one curve. Evidence consists of equations (1)-(23), the exact N=4 comparison, and the independent real controls. Status: verified for the precise theorem. Exact remaining mathematical gap for that theorem: none found. The failed broader route is arbitrary repeated-list length; it is blocked by the six-periodic repeated-list counterexample and should not be reopened without a changed statement or new mechanism.

## 9. Remaining limits and authorship

Mathematical route verification is complete under the explicit hypotheses. This report does not audit a submitted PROOF.md, provide a final whole-package clearance, establish priority, establish novelty, or identify the constant by a closed formula. Those are separate tasks. The root can promote this self-contained route only with its precise primitive least-period scope and stated nondegeneracy assumptions.

Author metadata supplied by the project: Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X. This audit text and script were produced by the independent adversarial agent. No external communication, Git mutation, branch/ref/index operation, upload, release, or package installation occurred.
