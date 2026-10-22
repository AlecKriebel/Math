# Checkable classical transfers and exact gaps

This priority comparison is conditional on Root's accepted target reduction, verified at the hash in INDEPENDENT_TARGET_FREEZE.md. It does not assert novelty. Source versions and actual reading scopes are in PRIMARY_SOURCES.json.

## Classical endgame: an explicit complete conditional implication

Write k=c/alpha, p=iK', v=2K tau/N, delta=2v, L=4K/N, r0=3K+p. The accepted inverse-outer edge is of the form

    e(u)=C0 dn(u)(1-k^2 sn^2(v) sn^2(u)) /
         [(dn(v)+k cn(v) sn(u))^2 (L0+k L1 sn(u))].

Root's calculation gives F(u)=sum_j e(u+j delta), nonzero, with real period L, imaginary anti-period 2p, exactly two simple poles R=r0+v and R+2p on C/(L Z+4p Z), and odd reflection about R. This includes the exceptional triangular collision.

Choose the Jacobi modulus kappa representing this rectangular lattice, with

    K'(kappa)/K(kappa)=2K'/L,  s=2K(kappa)/L,
    rho=Res_{u=R} F(u).

Then H(u)=rho s cs(s(u-R),kappa) has exactly the same poles, residues and periodicity. F-H is holomorphic and constant, and its imaginary anti-period forces zero. Thus F=H. The old identity in KLS-II Eq. (66), visually checked on preprint p.15,

    cs(z,kappa) cs(z+K(kappa),kappa)=-sqrt(1-kappa^2),

immediately yields F(u)F(u+L/2)=-rho^2 s^2 sqrt(1-kappa^2). The original-focus reflection and odd N identify the second area with this half-real-period translate. This is a verified transfer, not merely a resemblance of methods. No new general principle is involved.

KLS-local Section 4 supplies arbitrary-pole principal-part reconstruction. But it requires the geometric observable's actual principal parts. It does not itself compute the displayed inverse-edge function, complete pole list, double cancellation, or triangular collision. A prior application to the target must supply those facts or another theorem implying them.

The unsummed e has neither fixed sign under u -> u+2K in general. One may legitimately decompose

    e_even=(e(u)+e(u+2K))/2, e_odd=(e(u)-e(u+2K))/2,

which belong to KLS-local types I and IV respectively. Eqs. (42),(45) reconstruct those components after their actual coefficients are supplied. A direct single-class substitution for e is unjustified.

## Affine ratio: what survives and what changes

In the accepted Stachel coordinates,

    P(u)=(-a sn u,b cn u), Q(u)=(-A sn u,B cn u),
    A=a dn(v)/cn(v), B=b/cn(v).

Hence Q(u)=S P(u), S=diag(dn(v)/cn(v),1/cn(v)). The actual tangent polygon has its Q phase v ahead of its P phase. For odd N cyclic reindexing and possibly central reflection align the vertex sets. AST Theorem 1.3 gives the fixed untransformed area ratio, more generally for concentric Poncelet pairs. Levi-Tabachnikov Section 5 constructs its diagonal/grid maps.

For focus f, however,

    J_f(Sz)-f = S(z-S^-1 f) /
                [(z-S^-1 f)^T S^T S (z-S^-1 f)].

The denominator is anisotropic because dn(v)<1 in this strict noncircular domain. Moreover S^-1 f=(c cn(v)/dn(v),0), not the original focus. Thus unweighted determinant area ratios do not directly transfer to inverse areas. The fresh checker falsifies ordinary affine-inversion intertwining in an exact target example.

Nor are the original foci the outer-locus foci. Put t=sn^2(v). Direct expansion gives

    (A^2-B^2)-c^2 = -alpha^2 k^2(1-k^2)t^2/(1-t)^2 < 0.

This does not assume A>B and covers reversed outer axes. An own-focus inverse theorem is a different claim.

## A genuine polar/pedal transfer, with a precise conic mismatch

Use coordinates centered at f=(c,0), with unit polarity. The tangents to the original ellipse at P_i have poles R_i on

    (x-c/b^2)^2+y^2=a^2/b^4.

The line R_i R_{i+1} is the polar of Q_i: (Q_i-f) dot r=1. Its perpendicular foot from the coordinate origin is (Q_i-f)/|Q_i-f|^2=J_f(Q_i)-f. Therefore the target inverse-outer polygon really is a pedal of this circle-inscribed polar polygon.

Its caustic is the polar of the outer locus:

    (A^2-c^2)x^2+B^2 y^2-2cx-1=0.

It is a circle only if A^2-B^2=c^2, strictly excluded above. Its center c/(A^2-c^2) differs from the outer circle center c/b^2 since A>a. This transformed pair is neither bicentric nor concentric circle-ellipse. RGR's bicentric limiting-point perimeter theorem and AST's concentric circle angular theorems do not directly apply. A special theorem for this precise nonconcentric pair remains a possible narrower bridge; none was verified here.

Directly inverted Q vertices also do not lie on a conic. With r^2=X^2+Y^2 their locus satisfies

    B^2(c r^2+X)^2+A^2Y^2-A^2B^2 r^4=0.

For odd least N the outer locus is noncircular: A^2=B^2 would require cn(2v)=0, hence v=K/2 and N=4 tau. The inversion center is strictly inside it. Birational inversion of this irreducible noncircular ellipse gives an irreducible quartic; the displayed polynomial has no extraneous factor X^2+Y^2 because A^2 differs from B^2. A conic area theorem cannot be applied by simply relabeling these inverse vertices.

## Even-period complementary area products and parity

Chavez-Caliz's final Theorem 6 (printed p.104/PDF p.14) concerns the untransformed product A(P)A(Q), even period and concentric ellipses in general position. It already uses complementary zeros/poles. Its proof uses central pairing V_{i+n/2}=-V_i. Repeating an odd orbit twice has T^{n/2}=identity, rather than central reflection. The standard geometric n-gon hypotheses cannot be enlarged to repeated odd traversals to obtain this transfer.

An exact target-specific check uses squared outer axes (21,16), caustic squared axes (189/25,64/25), common focal square 5:

    P0=[(0,4),(-21/5,-8/5),(21/5,-8/5)],
    P1=[(-sqrt21,0),(3sqrt21/5,-16/5),(3sqrt21/5,16/5)].
    Q0=[(-7,4),(0,-10),(7,4)],
    Q1=[(-sqrt21,-8),(5sqrt21/3,0),(-sqrt21,8)].

Then

    A(Q0)/A(P0)=A(Q1)/A(P1)=25/6,
    A(P0)A(Q0)=57624/25, A(P1)A(Q1)=57344/25.

Double traversal multiplies both products by 4, preserving their difference. This checks the proposed parity transfer, not a counterexample to the intended even-period theorem.

The same calculations yield target product 1/3600 and original-vertex inverse product 1/324 at both phases. Each per-focus outer/original inverse-area ratio equals 3/10 in both phases. Thus a narrow ratio route remains positively supported by finite examples. If B_±(w)=lambda_± A_±(w), with phase-independent lambda_± and a prior original-vertex product theorem, the target follows immediately. No such universal ratio theorem was verified in the read classical passages. The broad all-concentric inner-focus extension's frozen counterexamples were not used to dismiss it.

The example/ratio datum was already in the frozen manuscript. exact_transfer_checks.py supplies fresh checks in Q(sqrt5,sqrt21), using Fraction only: ellipse incidence, caustic line tangency, raw tangent intersections and signed inverse areas. It is a finite transfer test, not an all-period proof.

## Rational cyclic pushforward needs pole control

A rational observable summed over a torsion shift descends to the quotient elliptic curve E/<T>, not to a point. Rationality and cyclic invariance do not force phase constancy.

For example, G(u)=sum_j sn^2(u+j delta,k) is cyclically invariant. On the sn torus, its double poles lie in two distinct shift orbits based at iK' and 2K+iK' when N is odd. Each pole has a nonzero double coefficient and no opposite contribution to cancel it. Thus G is nonconstant. This supplies an explicit check against a generic rational-pushforward shortcut.

Schwartz-Tabachnikov's centroid argument and Chavez-Caliz's proofs use specific principal-part relations. The former paper's lamina-centroid proof is explicitly noted as having a gap by Chavez-Caliz; it is not used here as a blanket rational-observable theorem. Their framework is classical, while the target requires its own pole calculation.

## Later general invariant-form/pushforward theorem

Glutsyuk arXiv:2605.24434v1, Theorems 1.5,1.7, Corollary 1.8 and Theorem 1.9, and their Section 3.8 proofs (preprint pp.63-65), were freshly read. The invariant form is the pullback of P2(z,w)^(-3/2) dz wedge dw; the fiber differential is obtained from omega=dR wedge omega_fib. The projection pushforward produces a holomorphic differential on an elliptic level curve under the stated rational-integrability hypotheses. These are phase-space and fiber statements. The form is not the Euclidean polygon area form. No identity expressing the two focal shoelace sums or their product as the relevant invariant integral is supplied in those passages. The gap is an exact observable-to-form identity, not a denial of the valid invariant-form theorem. No full classification proof audit is claimed.
