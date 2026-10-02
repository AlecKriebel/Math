# Independent full review: 5100022 / k404

## Verdict and exact version

**PASS_COMPLETE_SOURCE_TARGET. No mandatory correction.**

The verdict binds `PROOF.md` SHA-256 `b8edd78d03dac33a7be77837649eef7a8558900b3499774725174836fa54d462` and `FROZEN_MANIFEST.json` SHA-256 `28281e6da84af174e91478d020518b041c18b72b72fddfdaa4250a3ac86b5140`. All eleven author files and all three primary PDFs match the frozen hashes. The complete analytic argument and real-domain statement were reviewed independently. This reviewer supplied no author proof ingredient to this target.

The accepted theorem is the constant ratio of **original-orbit focal antipedal signed area to original-side focal pedal signed area**, for either original focus and primitive periods N=2 modulo4, including every primitive star winding in the strict noncircular confocal elliptical-caustic setting. The denominator is everywhere strictly positive in the chosen orientation, and all antipedal intersections are finite. No nonzero numerator, circular/degenerate/hyperbolic-caustic extension, or novelty claim is certified.

## 1. Source, attribution and normalization

I verified the k404 row in both source editions: [arXiv v11 Table5](https://arxiv.org/pdf/2004.12497v11), printed7, and [published Table5](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf), printed348. The table images were inspected; they state A*_m/A_m, N=2 modulo4 and the two original foci. The definitions use original vertex focal rays for the antipedal and original side-line feet for the pedal. Signed traversal areas are required. The source's introductory ensemble consists of two confocal ellipses, with a>b>0 in its preliminary notation.

The pinned published Stachel Theorem4.3/equation4.9 supplies the canonical coordinates with modulus equal to the caustic eccentricity. Normalizing its major semiaxis to1 makes the foci (+/-k,0), since (D²-b0²)/C²=k². Uniform scaling preserves the ratio. The [DLMF periods/poles/shifts](https://dlmf.nist.gov/22.4) and [addition formulas](https://dlmf.nist.gov/22.8) confirm the characters used below.

The prior pedal-trace mechanism and the parallel even-period focal-antipedal lemma are expressly disclosed in RELATED_WORK.md. They are author inputs/overlapping work, not independent reviews or independent discoveries. I checked the full reproduced focal proofs rather than treating an earlier campaign verdict as a substitute. The source-target parity specialization is distinct from the adjacent 0-modulo4 product target.

## 2. Direct geometry and all antipedal-coordinate poles

I independently built the original endpoints from the Jacobi addition formulas and used homogeneous Cramer intersections of their actual lines

    (P-F) dot X=(P-F) dot P.

Reducing by the Jacobi quadratic identities reproduces both coordinates in(6) and the exact determinant(7). This independently checks the cancellation of the apparent factor1+ks. The resulting rational identity extends meromorphically from its dense nonsingular domain. It is not legitimate to retain a spurious pole from the uncanceled derivation, and the candidate does not do so.

For real phases, t,C,D,b0,d are positive,1+ks>=1-k>0, and L>=1-k²t²>0. Thus the original two lines have a nonzero determinant and finite unique intersection. This holds for star traversals too; no convexity of the antipedal is assumed.

The only possible coordinate poles in(6) are the two roots of L. The function sn² has one double pole in its2K,2iK' cell, so L has exactly two zeros counted with multiplicity. The p-shift identity locates them at p+v,p-v; for example L'(p+v)=2CD/t is nonzero. At a common Jacobi pole, each coordinate numerator has order at most two, matched by L's double pole, so that apparent singularity is removable. Fixed coefficients b0,C do not vanish in the strict domain. This is a complete pole classification.

Under u=w+v+j delta, the two families become p-j delta and p-(j+1)delta. They are the same cyclic vertex-pole classes. Each coordinate has at most a simple pole, so its cyclic area has at most double poles. This explicit focal coordinate calculation is essential; the origin-antipedal's separate midpoint-pole analysis cannot simply be transferred here.

## 3. Symmetry, quotient lattice and the double-pole cancellation

Write N=2m. Primitive even traversal implies tau odd and gcd(tau,m)=1. The shift m delta is2K modulo4K, hence it cyclically relabels the centrally opposite original vertices. A derived cyclic area at a fixed focus has period2K by that relabeling. Central inversion also interchanges the two foci and preserves signed area, proving equality of their antipedal areas.

The reflection P(w)->P(-w) is reflection in the y-axis together with reversal of the index order. The antipedal index becomes-j-1. Reflection and reversal each negate signed area, so their combination gives B_F(-w)=B_-F(w)=B_F(w), with the correct plus sign. The imaginary shift2iK' reflects in the x-axis, fixes the focus, and retains traversal order; it negates area. Consequently B_F(p+z)=-B_F(p-z). Since its pole order was bounded by two, oddness eliminates the double Laurent coefficient and leaves only a possible simple pole. This is an exact character argument, not a numerical cancellation.

Periods delta and2K generate h=2K/m by Bezout. On the torus C/(h Z+4iK' Z), the possible poles are precisely p and3p. All translations are covered by the real period and the imaginary anti-period. No larger hidden pole class remains.

The trace S=sum_(j=0)^(N-1)dn(w+j delta) has exactly two simple poles on this torus. At p there are two contributing terms, j=0,m; their arguments differ by2K tau and their residues are equal and add. The residue at the other torus pole3p is its negative, by the anti-period. This distinguishes the two equal contributors from the two opposite total residues. Matching the first residue of B_F with b_F S matches the second automatically. The holomorphic remainder on the compact torus is constant and anti-periodic, hence zero. The real constant b_F may be zero.

The original-area identity(16) also checks: summing the Jacobi addition identity for dn counts each original vertex twice and gives exactly the stated coefficient abtC/D. There is no missing factor of two. The even-period antipedal/original-area proportionality is therefore supported by the written proof; it is not inferred solely from the parallel author's message.

## 4. Pedal poles and the source parity

The focal projection formula(17) was independently checked by its incidence on n dot X=1 and by parallelism of q-F to n. Its simplification is exact. Common poles of sn and cn are removable. The remaining coordinate poles occur where sn=1/k, a subset of the dn-zero translates, and have order at most two. At r=K+p the quarter-period formulas make q(r+z) even. Its two neighbors are regular because0<delta<2K. Thus the combined incident-area expression(19) is an at-most-double-pole even vector paired with an O(z) odd holomorphic vector, giving at most a simple pole. Nonadjacent terms are added rather than multiplied and cannot increase that order.

The cyclic area has the same real period h and imaginary anti-period as S(u+K). Its complete possible pole set therefore permits the same residue-matching/holomorphic-remainder argument, proving(20). The actual pedal's midphase is w+v. Exactly when m and tau are both odd, K+v=((m+tau)/2)h is an integer period. Hence N=2 modulo4 aligns both factors with S(w), as needed for the ratio. For N divisible by4 the shift is a half-integer multiple instead; the proof does not erase this distinction.

## 5. Strictly positive denominator, including closing star edges

The focus lies strictly inside the caustic. Each pedal displacement from F is a positive multiple of its outward unit normal:1-n dot F>0. Independently, det(n,n')=dn(u)/b0>0. The normal angle has a strictly increasing lift and advances exactly pi over2K. Since delta lies strictly between0 and2K, each consecutive normal-angle increment lies strictly between0 and pi. Thus every consecutive determinant of the displaced feet is positive.

This remains true on the last edge, using the parameter u+N delta and the lifted angle before reducing modulo2pi. It does not assume a star polygon bounds a positive simple region. The shoelace area is half the sum of these positive determinants, and translating by F changes none of the total area. Therefore A_F>0 everywhere, including all primitive stars. Since S>0 on real phases, equation(21) implies p_F>0, justifying division by it and by the actual pedal area. A zero antipedal numerator would merely give gamma=0.

The same area constant applies at both foci by central inversion. Reversal negates both signed areas; repetition of an already admissible primitive traversal scales both equally. No change of primitive parity is inferred. N=2 is automatically excluded by the strict caustic and positive integer winding assumptions.

## 6. Reproducibility and disposition

The unchanged author receipt replays byte-identically: **27,524 exact controls**, with **27,320 separately labeled90-digit diagnostics**. Independent homogeneous-line/symbolic and quotient-lattice controls pass **14,382 exact assertions**. A separate85-digit direct-geometry script passes **10,161 diagnostics** across21 primitive families, checking both foci, every named line, every positive star-pedal cross product, phase ratios and complex reflection/anti-period characters. Floating checks are not interval certificates and do not establish the universal theorem.

The full exact source/domain claim passes after one author turn. Preserve the strict ellipse ensemble, primitive2-modulo4 parity, signed ratio, everywhere-positive denominator, prior/shared-method disclosures and no-novelty language. No author revision is required. The campaign owner retains publication approval.
