# Independent physical and exact geometry audit of PR210 / 5100033

**Verdict: no mandatory or optional correction found within this audit's mathematical scope.** This is an initial independent physical-geometry audit, not a replacement for a priority investigation, a whole-package review, or proof of public repository custody.

## Independence and inputs

I read only the pinned candidate manuscript and preserved submitted proof before freezing my claim map and writing fresh checks. I did not read any historical audit report, mathematical clearance or the new meromorphic auditor's output at any stage. All calculations below were newly authored. Input hashes and the dated independence declaration are in INPUTS.json and FROZEN_INDEPENDENT_CLAIM_MAP.json.

The theorem audited is precisely this: for a strictly nested proper confocal elliptical caustic, odd primitive period N>=3 and any admitted coprime winding, project the two ORIGINAL foci orthogonally onto the ordered SIDE LINES of the OUTER tangent polygon. The product of the two signed shoelace areas is phase-independent. Hyperbolic, collapsed and grazing caustics are excluded. A repeated traversal of an odd primitive family is addressed separately.

## Fresh physical mechanism

No Jacobi function occurs in physical_geometry.py or its propagation routine.

Let D=diag(a^-2,b^-2), let P be on the boundary and let d be an inward unit direction. Its next boundary intersection is obtained directly from the quadratic:
    
    t = -2(P^T D d)/(d^T D d),   P_next=P+t d.

At that next point, n=D P_next, and the outgoing unit direction is
    
    d_next=d-2(d.n)n/(n.n).

For alpha^2=a^2-lambda and beta^2=b^2-lambda, a line through P with normal h is tangent to the caustic exactly when
    
    (h.P)^2=alpha^2 h_x^2+beta^2 h_y^2.

For unit d this equivalently gives
    
    lambda=a^2 d_y^2+b^2 d_x^2-det(P,d)^2.

Thus at P=(a,0), a positive-direction inward launch is
d=(-sqrt(lambda)/b,sqrt(1-lambda/b^2)).
I solve lambda by the lifted eccentric-anomaly winding after N actual physical reflections. Every sampled phase separately checks closure, winding tau, distinct vertices, caustic support, boundary membership and unit directions. This is a physical shooting construction of fixtures, not substitution of the manuscript's canonical vertices.

For each resulting polygon, I solve the two tangent-line equations to obtain the actual outer vertices V_j. I project the original focus onto the line through V_(j-1),V_j using the Euclidean affine projection formula, and only then compare with the candidate focal-foot map and compute signed shoelace. Consequently these tests cannot silently replace outer side lines with original billiard chords.

## Exact checks

The Sympy calculation makes 245 exact zero assertions, including full boundary, unit-vector reflection, common-caustic tangency, actual outer-side membership, perpendicularity, auxiliary-circle identities, focal-foot formula and area comparisons.

For a^2=21,b^2=16,lambda=336/25, the two triangles in the manuscript give exactly:

| Phase | B_plus | B_minus | Product |
|---|---|---|---|
| H | (49 sqrt(21)+7 sqrt(5))/10 | (49 sqrt(21)-7 sqrt(5))/10 | 12544/25 |
| V | 112/5 | 112/5 | 12544/25 |

The independent projections onto ORIGINAL CHORDS instead give product 7225344/390625, and original-vertex unit inversions give 1/324. Exact B_e=(2016/5)D_(-e) is checked for these two phases only; these finite checks do not prove the universal transfer asserted in the separate bridge.

For a=2,b=1,lambda=4/5, both the diamond and the corrected rectangle in the candidate satisfy exactly the boundary, reflection and same-caustic conditions. The two areas are respectively 4,4 and 5,5, yielding products 16 and 25. Each has four distinct vertices. This is an exact counterexample to dropping the odd primitive hypothesis.

A separate polynomial-ideal calculation verifies the universal rational projection map and its auxiliary circle. On x^2/a^2+y^2/b^2=1, c^2=a^2-b^2 and e^2=1, direct perpendicular projection from (ec,0) reduces to

    Q_e=(a^2(x+ec)/(a^2+ecx), a^2 y/(a^2+ecx)),   Q_e.Q_e=a^2.

The checker clears denominators and reduces the exact numerators by a Groebner basis of the three defining polynomial relations. This is not a numerical fit. In the stated real domain, a^2+ecx >=a(a-c)>0, and the normal length is positive, so the cleared denominators introduce no real-domain exception.

## Physical diagnostics and stability limits

RESULTS.json records 21 independently shot physical families, 7 phases apiece: 18 odd primitive families and 3 even negative controls. The final main replay makes 17,934 numerical assertions at 125 decimal digits. Tested odd pairs include (N,tau)=(3,1),(5,1),(5,2),(7,1),(7,2),(7,3),(9,2),(9,4),(11,5),(15,7),(21,10), with boundary ratios 1.000001,1.2,2 and8. All odd products pass relative tolerance1e-70 across their phases. Every even fixture has equal focal areas and a clearly nonconstant square.

The smallest tested caustic minor/major axis ratio is about2.37417e-13; the most extreme physical-step normalized residuals remain below7e-116. Every phase checks actual closure and coprime winding as well as pairwise vertex separation. Literal reversal negates each signed area, and literal triple traversal triples it. Signed-star order is retained throughout.

PRECISION_SENSITIVITY.json repeats the two hardest fixtures, (a/b,N,tau)=(8,11,5) and(2,21,10), at190 decimal digits with680 bisections. Relative product changes from125-digit values are approximately3.84e-108 and1.10e-106. This addresses precision sensitivity of these computations.

**These are noninterval arbitrary-precision diagnostics.** Neither a small residual nor agreement under added precision is an interval certificate, an existence theorem, or evidence of universal coverage of every period. The all-period conclusion rests on the analytic proof examined below.

## Logical reconstruction of the main proof

I challenged the geometry and every connection needed to apply the supplied analytic argument, and checked the argument's pole/period logic as written.

1. **The target area really is T.** At a real phase the tangent normal is(-sn/a,cn/b), and direct projection gives the displayed Q. The side through V_(j-1),V_j is exactly that tangent. Real canonical phase is injective modulo4K; a step strictly between0 and2K gives distinct nonantipodal endpoints, so consecutive tangents meet finitely. Three distinct tangents of a nonsingular conic cannot concur, since their dual points would be three intersections of a line and a conic; hence no such outer side collapses. These conclusions hold for trajectory-order stars as well as convex polygons.

2. **The coordinate theorem has the needed scope.** The cited Stachel Theorem4.3 explicitly concerns elliptical caustics and canonical billiard stepping, with arbitrary coprime turning number; it is not restricted to triangles or winding1. For a given proper confocal pair, cn(v)=beta/b uniquely selects0<v<K; the displayed a relation follows from dn^2=1-k^2 sn^2 and alpha^2-beta^2=c^2. Minimality is precisely coprimality after real period4K. Thus the canonical coordinates do not smuggle in a different family or use uniform eccentric anomaly.

3. **The two foci are correctly related.** Central half-period changes P to-P; direct focal projection gives Q_-(w)=-Q_+(w+2K). Central negation has determinant+1, so the second area is T(w+2K), with no hidden orientation reversal.

4. **There is no omitted double pole.** The two possible finite-denominator zeros in each imaginary row differ by the actual step2v. At a singular phase precisely two cyclic vertices are singular because the N phase classes are distinct. They are adjacent, including at the cyclic cut. Their residues are opposite collinear vectors, so det(R,-R)=0 cancels the only possible double Laurent coefficient. The other incident edges have one singular endpoint. N=3 is not an exception: the two other edges share one regular vertex but still have at most simple poles. Common sn/cn poles are removable in the rational foot map. The proof retains the vector period4iK', instead of incorrectly promoting2iK' to a full vector period.

5. **The reflection signs and complementary zeros are consistent.** Q(w+2p)=JQ(w) gives area sign-, while Q(2K-w)=JQ(w) combines reflection sign- with cyclic reversal sign- and therefore leaves T unchanged. Since2v is a T period, this centers evenness at b0=K-v. Coprimality gives reduced real period L=4K/N. Thus F(z)=T(b0+z) has possible simple poles only at p,3p, is even, and has antiperiod2p. At the regular point p+L/2, evenness plus real periodicity and the antiperiod force F=-F, hence zero; similarly at3p+L/2. The product F(z)F(z+L/2) has no poles, including when T is identically zero, and is constant on the compact torus. No division by an area or by a residue is required.

6. **Parity and boundary cases match geometry.** For odd N,2K is L/2 moduloL; for even N it is0 moduloL. This gives the odd product and the even equality respectively, in agreement with the exact counterexample. Repetition and reversal are direct signed-edge counting facts. The circle is separate because k=0 degenerates the complex setup: its tangent feet are the original regular-star vertices, with area(Na^2/2)sin(2pi tau/N), so the focal product is constant by rotation. Collapsed, hyperbolic and grazing endpoints are excluded rather than claimed by a nonuniform limiting argument.

I found no unsupported geometric bridge or logical defect in these steps. This is a human-readable mathematical audit using ordinary symbolic tools, not formal proof-assistant verification.

## Fresh primary-source target check

I checked the following primary sources through read-only web retrieval; PRIMARY_SOURCE_CHECKS.json records URLs, passages and limitations.

- [RGK arXivv11](https://arxiv.org/pdf/2004.12497v11), Table7, printed p.9: k605,a is the odd primed focal-area product. Section3.7 distinguishes original and outer pedals.
- [Published RGK](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf), Table7, printed p.349: k606 is that primed odd product; published k605 is the unprimed product. Section2 defines signed area; Figure1 and Sections3.4/3.7 specify the outer construction and focal feet.
- [Stachel, Theorem4.3 and(4.9)](https://link.springer.com/article/10.1007/s40879-021-00524-2): the canonical stepping and arbitrary coprime turning-number scope used above are present.

The web PDF screenshot endpoint failed to render these documents, so this audit's source comparison uses extracted primary-source text, not a claimed visual screenshot. I did not conduct a novelty or priority search and make no historical-first finding.

## Scope and result

Mandatory findings: [].
Optional findings: [].

The strongest verified result in this audit is that the candidate's exact target geometry, low-period examples, primitive parity boundary, and core proof-to-geometry connections withstand independent reconstruction and falsification attempts. New physical computations support the claimed theorem without duplicating its Jacobi construction. Unreviewed matters here include the full supplementary Landen/bicentric and inversion-transfer derivations, literature priority, frozen-publication byte custody, document layout, upload/tracker state, native repository scope and operational integration. Those require their own checks; this report grants no authority for service mutations or repository writes.
