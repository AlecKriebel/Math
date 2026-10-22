# Independent adversarial review: 5100062 / k903,a

**Verdict: PASS_COMPLETE_SOURCE_TARGET. No mandatory mathematical correction.**

Reviewed unchanged CANDIDATE.md SHA256:
`c4c2c5399d46f8aa30c4580160ea15a1375939eab3a2ba390d74abdce9a30905`.
Final author FROZEN_MANIFEST.json SHA256:
`1c77a8ba7eb2ef7ffe695c8fb68fce20b3378750767e207889a5d94b82a8f307`.
All twelve artifact entries and five primary PDF hashes match. One source
DOI typo was identified during review and corrected by the author, with a
preserved SOURCE_CORRECTION.json receipt; the mathematical proof did not
change. This reviewer did not contribute to the author proof route.

## 1. Exact source identity, normalization, and known results

The complete pinned statement and source-context audit were read. I checked
arXiv2004.12497v11 Section3.9 and visually inspected Table10, p12. The
actual target is **k903,a**, the product of the two signed areas obtained
by unit-circle inversion of the *original orbit vertices* about the two
original ellipse foci. Straight edges join the inverted vertices in
inherited order. No outer-vertex inverse, focus of a derived ellipse,
caustic inverse, arc-enclosed area, or polar/dual area is substituted.

The shorter final *Fifty New Invariants* has no k903 row. Its numbering
cannot validate this target. The author explicitly records that difference.
I also visually inspected arXiv2012.03020v2 p6: Proposition7 gives the
known three-period result and Conjecture1 states the general odd-period
product. The full bicentric paper's Table1, p629, marks the odd inverse-area
product as experimental and unproved there. Its correct DOI ends in
**00188-6**, not00188-y; the final source audit now has the right suffix.

The source requires the strict noncircular confocal ellipse setting,
ordinary fixed focal inversions, signed traversal areas, and odd primitive
period. These are the candidate's hypotheses, including primitive stars.
The proof does not claim the neighboring even-period product or an
unsigned filled-region area invariant. The N=3 result is credited.

Primary sources:
- https://arxiv.org/pdf/2004.12497v11
- https://arxiv.org/pdf/2012.03020v2
- https://armj.math.stonybrook.edu/pdf-Springer-final/021-0188.pdf
- https://armj.math.stonybrook.edu/pdf-Springer-final/020-0154.pdf

## 2. Flag framework and orientation character

The submitted complex intersection/transversality calculation is correct
and verifies the published flag-curve hypotheses for every strict pair
under consideration. The projection to E is branched at the four simple
points E∩C, so the smooth connected compact flag curve has genus one.
The conventions sigma=other point, tau=other tangent, T=tau sigma match
the Chavez-Caliz p98 framework. The exact-order translation has no fixed
points for a nonidentity power.

Each inversion area is rational in the ordered vertex coordinates and
is therefore meromorphic on this curve. T-invariance is cyclic relabeling.
The relation tau T^i=T^(−i)tau reverses the vertex order while preserving
the chosen focal center. Consequently each signed area is tau-odd.
Since sigma=T^(−1)tau, it is also sigma-odd. This is a holomorphic
involution character, not complex conjugation, and it is valid for the
inverted polygon with straight edges. The two determinant conventions
in real and complex coordinates agree exactly.

## 3. Special contacts and all possible singular vertex indices

I independently checked the four contacts
P=(epsilon a²/c, eta i b²/c). They lie on E, their tangent normals are
isotropic, and their E tangents satisfy the C dual equation. Subtracting
the two normalized dual equations proves the converse; no additional
common tangent is missing. Their C-equation residual is
−lambda²/(alpha²beta²), so projection of flags is unramified there.

For each contact the common-tangent flag s is sigma-fixed and its second
flag is tau s=Ts. If T^j s is also sigma-fixed, then T^(2j)s=s. Oddness
and exact order force j=0. Hence distinct sigma-fixed flags have disjoint
T-orbits, including the two distinct contacts belonging to the same focus.
This conclusion is genuinely different from the even-period case.

Along the orbit of any such s, a vertex can be a special contact only at
indices0 and1, up to relabeling. This uses both flags over every contact;
it does not overlook the second sheet of the projection. Those two
vertices approach the same point. There are no additional opposite-focus
contacts in this orbit. The argument covers N=3 and arbitrary larger odd
primitive star periods without a convexity assumption.

## 4. Focal inversion poles and their exact orders

The complex formulas U=f+1/(W−f), V=f+1/(Z−f) are exactly the rational
complexification of Euclidean unit inversion. I checked them by direct
algebra. At either original infinite point, Z and W have simple poles
with nonzero coefficients a−b and a+b, so U,V are regular and both tend
to f. There is no overlooked inversion-area pole at infinity, even if
several original vertices become infinite at one flag.

For f=c, Z=c is tangent to E at (a²/c,i b²/c), and W=c at its conjugate.
Their intersection multiplicity is exactly two. One way to check the
multiplicity is to substitute y=i(x−c) into the conic equation:

  x²/a² − (x−c)²/b² −1 = −c²/(a²b²)(x−a²/c)².

The negative focus has the corresponding formula with signs reversed.
The other denominator at each contact equals ±2b²/c and is nonzero.
Thus only one of U,V has an order-two pole at a given contact; the other
is holomorphic. The unramified projection preserves that order on X.

For an area term involving both singular vertices0 and1, the singular
coordinate type is the same for both, because they converge to the same
contact. The complex shoelace determinant is V_i U_j−U_i V_j; it never
multiplies the two singular coordinates. Hence every area term has order
at most two. In particular there is no order-four or order-three pole
hidden in the adjacent pair. Every other determinant has at most one
singular factor. These observations exhaust all rational denominator
zeros and both points at infinity.

## 5. Local oddness, the opposite zero, and compactness

The local involution argument is valid and supplies the required
multiplicity reduction. At a fixed point of the nonidentity holomorphic
involution sigma, its derivative is−1: derivative+1 would contradict
order two at the first nonzero nonlinear coefficient in characteristic
zero. For a local coordinate z, (z−z∘sigma)/2 then gives a coordinate t
with sigma(t)=−t. Sigma-oddness of the focal area eliminates every even
Laurent power. Combined with the established order bound two, this leaves
at most a **simple** pole, rather than merely an unspecified cancellation.

At a pole candidate for the positive-focus area, the negative-focus area
is holomorphic by the disjoint-orbit result and the infinity analysis.
Its own sigma-oddness forces its value at the fixed flag to vanish.
Thus its zero has order at least one, enough to remove the at-most-simple
pole of the other factor. If that area vanishes identically, the product
conclusion is immediate. The same argument handles the other focus and
all T-translates.

The product is therefore a globally holomorphic function on a compact
connected curve and is constant. No division by either area, generic
nonvanishing assumption, or unproved nonzero residue is required. The
restriction to the real Poncelet family gives exactly the source invariant.
Real inversions are defined at every orbit vertex since the foci are
strictly interior to E. Sign reversal and radius scaling are handled
correctly, with the unit normalization retained in the theorem.

## 6. Reproducibility and adversarial controls

The author checker was inspected and replayed separately. Its **91 exact
assertions** passed, and its JSON output is byte-identical to the frozen
receipt. The genuine triangle incidence, caustic tangency, and reflection
checks reproduce both products5/256. The even negative controls have
unequal products1/36 and625/20736. I additionally verified both four-period
controls are primitive, satisfy the reflection law, and share the same
strict confocal caustic; the negative control is not just two arbitrary
inscribed quadrilaterals.

A separately authored checker passes **3,553 exact assertions**, covering
universal inversion/determinant identities, exact double contact,
unramified/common-tangent equations, odd-orbit and two-index completeness
for1,001 odd periods, even-parity countercontrols, and formal Laurent
order cancellation. These finite controls do not replace the geometric
proof above.

Separately, **1,296 numerical diagnostics at100 digits** pass for54
primitive families using N=3,5,7,9,11,15 and allowed star turning numbers.
They compare direct bilinear focal inversions and signed areas at real
and complex phases, test fixed-focus reversal and radius scaling, and
probe within about10^(-9) of sigma-fixed pole phases. The opposite focal
area vanishes there, the local focal-area Laurent character is odd, and
the product remains constant. Maximum scaled residual is about1.43e-70.
These are diagnostics, not validated interval certificates.

## 7. Disposition and limits

The full source target is proved by the unchanged candidate. The requested
source DOI correction is completed and independently verified; no further
mandatory correction remains. Preserve the arXiv-only k903 identification,
known triangle result credit, classical flag-framework credit, primitive
odd/star/signed-area/strict-ellipse/unit-focus-inversion scope, and absence
of a historical-novelty assertion.

This is an independent AI audit. It is neither a human peer review nor an
exhaustive literature/priority certificate. The separate k303,a proof was
previously audited by this reviewer, but no result from it is assumed in
this proof or in this review's odd-orbit argument.
