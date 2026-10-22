# Independent adversarial review: 5100007 / k115

**Verdict: PASS_COMPLETE_SOURCE_TARGET. No mandatory correction.**

Reviewed exact author proof SHA-256
`5d31111bf167822783d32aabb1e0bf2766bb372b3a5359739d9c157f8faab030`.
All ten entries of the submitted `MANIFEST.json` matched before review.
Review completed 2026-10-01. This is an independent AI mathematical audit,
not human peer review or a historical-novelty certification.

## 1. Statement and primary inputs

The two complete Reznik–Garcia–Koiller source editions were read. Their
Table 2 rows are the same **k115**: the product of distances from vertices
of the outer tangent-intersection polygon to an original ellipse focus,
for period divisible by four. I visually checked arXiv v11 p.5 and the
published table p.345. Neither caustic-contact points nor focal pedals are
substituted for those outer vertices. The source's confocal pair consists
of ellipses; signed-area conventions are irrelevant to this distance claim.

Sources: [arXiv v11](https://arxiv.org/pdf/2004.12497v11),
[published Table 2](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf).
The published canonical input was independently read at
[Stachel, Theorem 4.3 and (4.9)](https://doi.org/10.1007/s40879-021-00524-2),
printed p.1614/PDF p.13, including a rendered-page check. It supplies
P(u)=(-a sn u,b cn u), the caustic-eccentricity modulus, step 2v,
v=2K tau/N, and a=alpha dn(v)/cn(v), b=beta/cn(v). Coprimality is the
least-period convention. Its neighboring erroneous dn-shift sign is not
used. Positive caustic semiaxes and 0<v<K are essential.

The proof expressly restricts to primitive N divisible by four, while
including all admissible coprime star turning numbers. It does not infer
the parity from a multiple traversal of an excluded primitive orbit.
The focus and orientation choices are addressed by antipodal pairing.

## 2. Tangent-intersection identity checked independently

I recomputed both tangent equations using the addition formulas, without
assuming the proposed outer locus. Clearing their common denominator
1-k^2 sn^2(u)sn^2(v) yields the author's two linear equations. Substituting
X=-a dn(v)sn(u)/cn(v) and Y=b cn(u)/cn(v) satisfies both identically.
The determinant magnitude is exactly

  2 sn(v) cn(v) dn(u) / [ab(1-k^2 sn^2(u)sn^2(v))].

It is strictly positive on the real line; there is no omitted parallel
case, even for star polygons. The exterior inequality in (5) has positive
numerator excess sn^2(v)dn^2(u), so no outer vertex equals a focus and no
ordinary distance vanishes. The real outer locus is a nondegenerate ellipse;
its real parameter has period 4K and is injective modulo that period.
The absorbed midpoint phase is correct.

## 3. Paired focal-distance factorization

I expanded H directly from the two squared distances and the squared outer
semiaxes. Exact symbolic simplification independently reproduces

  H = alpha^4/(1-t)^4 · (1-kappa S)(U^2-kappa V^2 S).

No square-root sign is used in that algebra. The double-angle identities
convert U/W and V/W into dn(delta) and cn(delta), respectively. A separate
symbolic check gives

  U^2-kappa V^2 = (1-kappa)W^2,

so the real second factor, after division by W^2, is at least 1-kappa>0.
The complete factorization, positive scale, and the fourth-degree origin of
H are sound. PR149 is not required for this derivation. Its live metadata
confirms it concerns k114/original vertices/period 2 modulo four, and the
candidate appropriately credits only the organizational method.

## 4. Complex torus, zero orders, and exceptional case

I checked the actual entries of [DLMF 22.4 Tables 1–3](https://dlmf.nist.gov/22.4),
the [addition formulas](https://dlmf.nist.gov/22.8), and
[derivative table](https://dlmf.nist.gov/22.13). In particular,

  sn(z+K+iK') = dn(z)/(k cn(z)).

On T=C/(2K Z+2iK' Z), sn^2 has exactly one double pole, p=iK'.
It is sn^2 and dn^2 that descend to this lattice; the proof does not
incorrectly give sn itself real period 2K or dn itself imaginary period
2iK'. The function dn^2 has a double zero at p+K and a double pole at p.

For cn(delta) nonzero, J=dn^2(delta)-k^2 cn^2(delta)sn^2(u) has a double
pole at p. Its two exhibited zeros p+K±delta are distinct: equality would
force delta=K within 0<delta<2K. Neither is p, nor p+K. They account for
the entire degree-two zero divisor, so each is simple. There are no hidden
zeros or additional poles. Thus the full divisor (13) has the stated
multiplicities, and it is not merely a set-level cancellation.

The exceptional cn(delta)=0 condition forces delta=K. Combined with
primitive N=4n and tau=n, this implies n=1. Then J is the nonzero constant
k'^2 and H has only a double pole; the separate divisor (14) is correct.
The outer semiaxes indeed become equal in this case. No generic pole order
is incorrectly retained at N=4.

## 5. General cyclic norm and ordinary-distance recovery

The translation delta has exact order m=N/2 on T because gcd(tau,m)=1.
Since N=4n implies tau odd, n delta equals K modulo 2K. Consequently each
of the three zero families is exactly a permutation of the pole orbit.
The multiplicities are 2+1+1=4 in the generic case and 2 in the N=4 case.
This proves the norm has zero divisor for **every** admissible N and tau;
the argument is not restricted to the finite test range.

The norm is a genuine meromorphic elliptic function, not a multivalued
square root. Divisor cancellation makes it holomorphic on a compact
connected torus, hence constant. Its real value is positive. The remaining
half of the real billiard orbit is antipodal, since m delta=2K tau with tau
odd. Pairing its ordinary Euclidean distances gives exactly R_+^2=F.
The positive real square root is uniquely determined, proving constancy
and equality for both foci. This step removes the possible sign/branch
loophole, rather than assuming it away.

The separate circular case is correct and not needed for the main a>b
source scope. Hyperbolic, separatrix, collapsed-caustic, and inappropriate
repetition cases are explicitly excluded; no claim about them is passed.

## 6. Reproducible controls and limits

The author's checker was inspected and replayed in a separate directory:
**25,515 exact assertions and 702 numerical diagnostics passed**, reproducing
the author receipt. It performs no downloaded-code execution.

I authored a separate checker. It passes **34,509 exact assertions**:
raw-distance factorization, tangent substitutions and determinant by
polynomial reduction, the real-factor lower bound, divisor convolution
for 6,897 primitive turning-number cases, the N=4 equivalence, and wrong-
parity controls. These finite checks support implementation and indexing;
the universal argument is the mathematical audit above.

Separately, **10,995 numerical diagnostics at 90 decimal digits** pass.
They use direct intersections of actual tangent lines, direct ordinary
focus distances, caustic-tangency discriminants, complex zero locations,
nonzero derivatives at simple zeros, and the complex quarter shift.
The maximum scaled residual is about 4.92e-88. They are explicitly not
interval certificates and not substitutes for the divisor proof.

**Publication disposition:** the unchanged reviewed proof is suitable for
an open draft claiming resolution of this exact source target, with the
published-input, method-credit, scope, and no-novelty caveats preserved.
