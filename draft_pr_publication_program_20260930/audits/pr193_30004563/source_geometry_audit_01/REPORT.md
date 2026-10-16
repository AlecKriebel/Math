# Independent source and geometry audit of PR 193 / problem 30004563

Audit UTC: 2026-10-15. Completion estimate: 100% of the assigned source/admissibility audit. This does not estimate historical priority or the unknown global maximum.

## Conclusion

The original candidate's mathematical counterexample survives this independent source-first audit: at alpha=16 it defines an admissible six-point boundary, one incoming realization and at least five distinct outgoing centers. No fatal admissibility or quantifier error was found for the precise realization claim. The five centers are genuine intersections of the two equation-defined construction curves sharing the focus A=(0,0), with the other foci distinct and noncollinear. Thus they contradict the at-most-three expectation in published Remark 4.8, in addition to the natural crossing-permitted reading of the OWR conjecture.

There is a concrete and unavoidable scope limitation: the fixed boundary edges [A1,A2] and [A3,A4] strictly cross. Consequently this example has no incoming or outgoing proper embedding. The candidate expressly restricts its claim to realizations and does not claim a proper embedding or a global maximum. That restriction is essential.

## Independence and provenance

Before opening candidate evidence I sealed `SOURCE_FIRST_PLAN.md`, then read exact primary definitions and sealed `SOURCE_TARGET.md`. Their SHA256 seals are retained. No prior `review/REVIEW.md`, review certificate, reviewer code, author checker, author source-audit summary, or earlier audit judgment was read. After fixing the source target I read original `CANDIDATE.md` and its author-supplied exact certificate as untrusted mathematical evidence. My checker imports neither; it rebuilds the construction from the displayed rational parameters and algebraic boundary definitions. It uses a different eighth-root algorithm (general integer bisection) and tighter independently generated intervals.

Original submitted candidate SHA256: `293f5ad9475b4a8d045121b2eccecbcf0d4937df3077e9bb430c7f9056e12f51`.

Original-head identity provided for this assignment: `b9a399eeac816dbb8f0e50e81b498c26e5acef81`; immutable queue state provided: `claimed_solved`, 2/5. Those are provenance labels and played no role in proof decisions.

## Primary-source scope

1. [OWR 35/2020](https://ems.press/content/serial-article-files/46871?nt=1), printed p.1785 (PDF p.27): Theorem 4 assumes alpha>1; its following conjecture proposes three as maximal. The accompanying explanation explicitly permits crossing edges. The term graph immersion is informal here; no separate surface-local-homeomorphism definition is supplied.
2. [Melotti--Ramassamy--Thevenin, arXiv:2003.08941v2](https://arxiv.org/pdf/2003.08941v2), Definition 2.1 p.7, Definitions 2.2--2.5 pp.8--9: a realization satisfies the ordered opposite-side power equations; properness and orientation are additional embedding requirements. The boundary comprises six distinct points, with each alternating triple noncollinear.
3. The same paper, Definition 2.7 p.10 and Remark 2.8 p.11: construction curves are exactly power-difference level sets; incoming balance makes one outgoing equation redundant. Theorem 4.7 p.27 supplies existence for alpha>1. Remark 4.8 on that page proposes a three-intersection bound for shared-focus curves.
4. [Published article](https://ems.press/content/serial-article-files/39488), Remark 4.8, printed p.811 (PDF p.31), retains that expectation without an embedding restriction.

The complete arXiv pages 8,9,11,27, OWR p.1785, and published p.811 were rendered locally and visually inspected, including Figure 6's incoming/outgoing combinatorics and Figure 7's explicit improper realization. Source PDFs, text extractions and screenshots remain private and are excluded from the safe integration allowlist.

The strongest precise source target is the paper's equation-defined realization/curve setting. The OWR's informal immersion terminology should not be silently upgraded to an oriented two-dimensional surface immersion.

## All six face equations, independently derived

Write p(P,Q)=|P-Q|^16. Reading the vertex order directly from Figure 6 yields the incoming conditions

- p(A1,A2)+p(A3,Z)-p(A1,Z)-p(A2,A3)=0;
- p(A3,A4)+p(A5,Z)-p(A3,Z)-p(A4,A5)=0;
- p(A5,A6)+p(A1,Z)-p(A5,Z)-p(A6,A1)=0.

The outgoing conditions are

- p(A2,A3)+p(A4,X)-p(A2,X)-p(A3,A4)=0;
- p(A4,A5)+p(A6,X)-p(A4,X)-p(A5,A6)=0;
- p(A6,A1)+p(A2,X)-p(A6,X)-p(A1,A2)=0.

Use the candidate's rational foci A=A2=(0,0), B=A4=(2073/10000,0), C=A6=(4719/10000,64/10000), lambda=27/1250, mu=1. Its three algebraically defined other vertices satisfy, by their defining polynomial equations,

p(A1,C)-p(A1,A)=mu,
p(A3,B)-p(A3,A)=lambda,
p(A5,C)-p(A5,B)=mu-lambda.

Thus the three outgoing equations are respectively F_B(X)=0, F_C(X)-F_B(X)=0, and -F_C(X)=0, where

F_B(X)=p(X,B)-p(X,A)-lambda,
F_C(X)=p(X,C)-p(X,A)-mu.

For incoming Z put L=p(B,A5)-p(B,A3), M=p(A,A1)-p(A,A3). The reconstructed scalar incoming root satisfies p(Z,A5)-p(Z,A3)=L and p(Z,A1)-p(Z,A3)=M. These are exactly the second and first incoming equations. The third follows because

M-L=p(C,A1)-p(C,A5),

which follows by substituting the three displayed exact boundary identities. This is a direct algebraic proof of equality; merely enclosing a residual around zero would not prove equality. The independent checker also recomputes all six residual enclosures as a consistency check.

## Exact reconstruction and numerical evidence

`independent_geometry_check.py` is self-contained standard-library Python. It uses rational interval endpoints exclusively in all decisions, and certifies every eighth-root enclosure with integer eighth-power comparisons. There is no floating-point decision, root solver, original checker import, or original JSON dependency. The decimal numbers below are explanatory approximations; exact rational bounds are in `INDEPENDENT_CERTIFICATE.json`.

For s>=0 set u=s^(1/8), v=(s+lambda)^(1/8), w=(s+mu)^(1/8). Subtracting the squared distances gives the unique coordinates

x=(b^2+u-v)/(2b),
y=(c^2+d^2+u-w-2cx)/(2d).

The residual G=x^2+y^2-u is continuous. At a zero, all three squared-distance identities hold, so the positive eighth powers yield the two F equations. Conversely every common zero has s=|X|^16 and therefore comes from this construction. Distinct s produce distinct X.

| s | independently enclosed G(s), rounded here |
|---|---:|
| 9/10000 | +0.38163874225 |
| 11/10000 | -0.27266201661 |
| 13/10000 | +0.51494142823 |
| 1/2 | -0.90263001798 |
| 1 | +9.01429653314 |
| 10^17 | -38.11780435862 |

The five disjoint sign-change intervals prove at least five centers by continuity, with no assumption of interval-root uniqueness. I refined each independently by 180 exact bisections. The selected centers lie near

(-0.386406293019, 0.519654128725),
(-0.358985635882,-0.550178293811),
( 0.089623546519,-0.940869999570),
( 0.093674241284, 0.964389828902),
( 0.103650000000, 9.758257812500).

For the algebraic boundary parameters, t maps to ((t-1)^2+h^2)^8-(t^2+h^2)^8 times |q|^16. Since g(t)=(t^2+h^2)^8 is strictly convex, g'(t) strictly increases, so g'(t-1)-g'(t)<0. The parameter polynomial is strictly decreasing and has opposite infinite limits. Therefore each defining root is unique. I bracketed each with fresh 190-step rational bisection.

For incoming Z, the independent H reduction uses A3 as common focus and the two other odd vertices as foci. Exact intervals give H(1/100)>0 (approximately 0.000370693747) and H(11/1000)<0 (approximately -0.000803344398). This proves the incoming center directly, without invoking the source flip theorem. Its entire retained box lies in (0.1677,0.1717) x (-0.0036,-0.0026).

The following strict properties were independently certified:

- All 15 boundary pairs are distinct; all 20 boundary triples are noncollinear. In particular the required even and odd determinants are respectively 0.00132672 and approximately 6.37981720345.
- Each selected center and Z is distinct from every boundary vertex. Each avoids every line through a boundary pair. Thus every face has four distinct vertices and no collinear vertex triple, all edges have positive length, and no incident pair of straight edges coincides in direction.
- All five selected center boxes are pairwise disjoint.
- Every face has nonzero signed area, although a crossed face's signed area does not imply properness.
- The determinants of the two outgoing polynomial-gradient rows exclude zero at the selected centers: approximately +1.16931245, -1.14983109, +18.1604097, -25.6012929, and +1.71446742*10^27. The incoming gradient determinant stays between 6.51*10^17 and 6.75*10^17. These are genuine transverse intersections, with no tangency needed for the example.

## Concrete topology limitation

Let orient(P,Q,R)=det(Q-P,R-P). Independent rational enclosures give the following four values for boundary segments A1A2 and A3A4:

orient(A1,A2,A3) approximately -2.64361409374,
orient(A1,A2,A4) approximately +0.97891206000,
orient(A3,A4,A1) approximately +3.57955286374,
orient(A3,A4,A2) = -0.04297329.

The strict opposite signs certify an interior crossing. This crossing belongs to the fixed boundary, so no choice of central point can convert this fixed drawing into an embedding. Additionally the incoming face A1A2A3Z crosses itself, and each selected outgoing arrangement has a crossed face:

| center (in increasing s) | strictly crossed outgoing faces |
|---|---|
| 1 | A2A3A4X, A6A1A2X |
| 2 | A4A5A6X |
| 3 | A4A5A6X |
| 4 | A2A3A4X |
| 5 | A2A3A4X |

These facts falsify any stronger proper-embedding interpretation for this specific construction. They do not falsify its realization claim: that source setting explicitly permits crossing edges and improper quads. No orientation or two-dimensional local-homeomorphism claim has been inferred from the realization equations.

## Limits, boundary cases and exact remaining gaps

The inversion requires b*d !=0, equivalently the three even foci noncollinear in these coordinates; their exact positive determinant was checked. The incoming inversion analogously requires the odd determinant nonzero. Both are strict, not near-zero assumptions left to floating point.

All root radicands used here are positive because s>0 and lambda,mu,L,M>0; the incoming and outgoing eighth roots are the positive real branches. At s=0 the outgoing G remains continuous, though its derivative need not remain finite; none of the chosen sign intervals includes zero. No division by u or s occurs. At infinity v-u and w-u tend to zero, so (x,y) tends to the even-focus circumcenter (b/2,(c^2+d^2-cb)/(2d))=(0.10365,9.7582578125), while u tends to infinity and G tends to negative infinity. The fifth center is at finite positive s; proximity to that coordinate limit is not a point at infinity or a collapsed face.

Under parameter variation, admissibility could fail when a boundary determinant vanishes, two vertices coincide, a center reaches a boundary-pair line, a face collapses, or two construction curves become tangent. All relevant exclusions are strict for this example, including the transverse-intersection check. Alpha=16 is an exact fixed value satisfying alpha>1. Nothing here supplies counts at alpha=1,2, nonpositive alpha, or infinite alpha; those cases cannot be inferred by this integer-power reduction.

The strongest verified claim is existence of at least five admissible outgoing realization centers for one directly certified incoming realization. Exact total count, a global maximum, proper-embedding multiplicity, historical novelty, and publication-priority assessment remain unproved by this audit. No outside individual was contacted and no outreach was prepared.

## Reproduction and integration boundary

Run `python3 independent_geometry_check.py` from this owned folder (or pass its absolute path). It writes only its owned `INDEPENDENT_CERTIFICATE.json`; current reconstruction reports `INDEPENDENT_EXACT_RECONSTRUCTION_PASS`. The count of interval/assertion checks is diagnostic and is not the mathematical argument.

The safe allowlist includes text/JSON/Python audit artifacts only. `private_sources/` contains licensed-source copies and rendered pages and must not be integrated or published. No Git, ref, index, PR, publication, or source-submission mutation was performed.
