# Independent full review: 5100047 / k806,a

**Verdict: PASS_COMPLETE_SOURCE_TARGET. No mandatory correction.**

This review binds author PROOF.md SHA-256 `1d6573fbcd03e3ecb24fc3675ac4902fa3b14ae0ccbd9058bbd9dd6dd8a87e3b` and FROZEN_MANIFEST.json `8f485585b18c1ef287189309a619574fda366a7c39543cd61aad0ea430d9eab0`, covering eleven author files. The exact original-focus, all-primitive-period signed-area ratio is proved throughout the stated strict elliptical-caustic domain. All author files and four primary PDF hashes match. No source-target substitution or numerical-only argument is needed.

The reviewer did not author PR207, PR211, or this candidate and did not supply an ingredient to its author route. Prior involvement was independent review of PR211, and a new independent audit of the entire PR207 proof for k817. Both full proofs were read again here; the necessary inherited identities are also reconstructed independently below. The verdict does not certify novelty, historical priority, minimality, or human peer review. Publication remains subject to the owner's gate.

## 1. Exact source and objects

ArXiv:2004.12497v11, Table 9, printed p.11, visibly gives k806,a as the primed dagger area divided by the unprimed dagger area, for all N. Section 3.9, printed pp.9–10, uses the same original billiard focus for both. The numerator comes from the outer polygon whose vertices are the intersections of consecutive original tangents. Inversion about a focus of that outer locus is separately defined and is a different object. The signed areas are those of straight-edge polygons joining the inverted vertices, including their traversal signs in star cases.

The published companion's Table 9, printed p.350, was inspected and omits k806,a. Its shorter table and the later self-intersected paper's different k806 label cannot replace this exact target. The neighboring arXiv k806,b row visibly assigns 2 to the same displayed outer/original quotient. Direct geometry below gives 1/2. This reciprocal-value error is correctly distinguished from the k806,a constancy claim.

Stachel's published Theorem 4.3 and (4.9), printed p.1614, give the canonical parameter step and the modulus determined by the caustic axes. The proof uses this modulus, rather than the outer ellipse eccentricity or a numerical library's squared parameter. Strict noncircular ellipse and strictly nested nondegenerate confocal elliptical caustic, N≥3 and coprime turning number 0<tau<N/2 are consistently imposed. All primitive stars satisfying these assumptions are included. Hyperbolic or collapsed caustics, a formal doubled period-two trajectory, and arbitrary inversion centers are not covered.

## 2. Actual geometry and inherited algebra

The proposed midpoint outer vertex satisfies both individually named tangent equations. Their determinant is `2 sn(v) cn(v) dn(u)/(ab D(u))`, positive for the real parameter range. Thus each actual tangent intersection is uniquely finite. Its corresponding semiaxes both exceed those of the original ellipse, independently of their relative order; hence the outer point lies outside the original ellipse and cannot be either original focus.

For original vertices, the Euclidean distance to the positive focus is the positive quantity `a+c sn(z)`. Squaring matches the actual norm, and the lower bound a-c>0 fixes the sign. Expanding the translated determinant and the product of these distances reproduces E(u), including the alpha scaling and q² coefficient. This is precisely the PR207 algebra, not its later parity-specific invariant taken as a black box.

For outer vertices, expanding the actual squared norm gives the factorization `(alpha²/q²)(1+k sn(z))(U+kV sn(z))`. The independent reconstruction starts from Euclidean norms and both tangent equations, then verifies the two distance-product factors and the translated determinant. Their quotient is exactly G(u), including q⁴ and the extra cn(v) in its coefficient. The first and second individual outer norms were also checked, so an opposite-side or unlabelled incidence mistake cannot be hidden by an area symmetry.

Two successive Jacobi additions independently reproduce `L0=Z dn(3v)` and `L1=Z cn(3v)`, rather than assuming the displayed triple-angle identities. The gaps

- `U²-k²V²=k'² W²>0`,
- `L0²-k²L1²=k'² Z²>0`, and
- `dn²(v)-k²cn²(v)=k'²>0`

are exact. W and Z are positive in the stated domain, and L0 is positive since dn(3v)>0 on the real line. Every real factor in E and G is therefore positive. This gives strict positivity of each inverse edge contribution and both polygon areas for the selected orientation, even for primitive stars. It is not a general claim about arbitrary inverted polygons, nor a uniform bound in a degenerating family.

All complex continuations use bilinear squared norms without conjugating the parameter. The resulting E and G are genuinely meromorphic functions of one complex variable.

## 3. Entire inherited dependencies

The PR207 input has SHA-256 `d92e9a82674b1562e0b980c78088fc48319f9fc3d9d46ec55a1a46c893e372b8`, at public head `a7f8486548122c7d545430821afeedbccf48b3e7`, Git blob `d4968f8ddfe7a5f8393252e4473132612cd4224c`. Its full proof was independently audited, including the antipodal rational formula, complete generic pole list, reflection cancellation, N=4 paired replacement, nonzero dn-trace residues, compact-torus half-shift identity, and exact primitive-period arithmetic. The k817 review records that audit at report hash `44fdaf5388eb6b1c582fe54ec0b5597435082d9b66e78c3fe2b6b344e82bbf67`. This candidate only inherits the edge algebra, which was reconstructed afresh.

The PR211 input has SHA-256 `9640ed4bc6c6b0b56f0235c0e28513e9c3ca94c53cb75d2cb2eecee5b45b075e`, public head `9d7b623203b525386da3d9d91548c79e7445a11c`, Git blob `72b412a758692f9d08708ad045bbc45581b717e6`. Its full odd-period argument was re-read: the actual outer geometry, positive edge formula, full first/triple-factor pole list, N=3 critical cancellation, nonzero two-pole trace, simple half-period zero divisor and opposite-focus shift are correct. Its final odd-period product is not used to infer an all-period ratio. Its inherited geometric and triple-angle identities have fresh exact controls in this review. Neither dependency assumes k806,a, so the inheritance is not circular.

## 4. Complete original trace pole audit

Use the sn torus `(4K,2iK')`, the full dn-compatible torus `(4K,4iK')`, p=iK' and r=3K+p. Jacobi sn has degree two on its torus, branch values ±1 and ±1/k, and the quarter shift gives `sn(r+z)=-dn(z)/(k cn(z))`.

When V is nonzero, `1+k sn(u)` has a double zero at r, canceled once by the simple dn zero. The other factor is nonzero there because U-V>0. The two roots of `U+kV sn(u)` are precisely r±delta. Their value has magnitude greater than 1/k because U>|V|, so they are finite, simple, noncritical roots. They are distinct except at the separately handled V=0 transition. Their squared occurrence allows order at most two. At a common sn/cn/dn pole, numerator and denominator each have order three, so E has no additional pole. This list is complete by the degree-two sn fiber.

Reflection about r preserves sn and reverses dn, making E odd under that reflection. Its quadratic Laurent coefficients at r+delta and r-delta are opposite. For the N-term trace, delta has exact order N modulo 4K by coprimality. Each reflected root runs through the same N locations, with equal multiplicity and unchanged translation derivative. Thus the quadratic terms cancel at every trace pole. This reasoning works in every period, including N=3 where several simple contributions merge after reduction.

For V=0, cn(delta)=0 and 0<delta<2K force delta=K; primitivity forces N=4, tau=1. The generic common-pole estimate would fail, so the explicit opposite-edge pairing is essential. Its expression as a positive-coefficient combination of dn and 1/dn has only simple poles. The remaining shift by K places all poles in the allowed two classes on the quotient real period ell=K. The proof correctly uses this replacement rather than an unproved limiting argument.

## 5. Complete outer trace pole audit

The squared first factor in G has exactly the two finite simple roots r±v. Its sn value has magnitude greater than 1/k, hence is noncritical. For L1 nonzero, the second factor has roots r±3v. These are simple except when 3v=2K. Primitivity makes that N=3, tau=1. Then its factor is Z(1-k sn(u)), with a double zero at K+p; dn has a simple zero there, leaving order at most one. Independently, the second derivative of `1-k sn` at that point is k²-1, which is nonzero. This confirms the multiplicity rather than just the location.

The two root sets cannot meet on the full sn torus: their real differences would require 2v or 4v to be a multiple of 4K, contrary to 0<v<K. At a common Jacobi pole, the numerator and denominator orders are three when L1 is nonzero, so that point is removable. The list exhausts the poles; no hidden isolated pole survives the rational cancellation.

G has the same odd reflection about r. The double coefficients at r+v and r-v are opposite and the points differ by delta. Their cyclic quadratic contributions therefore cancel with equal multiplicity for every N. The simple roots r±3v differ from r+v by delta or -2delta. All remaining poles lie in the same real reduced class.

If L1=0, the real range makes cn(3v)=0 exactly at 3v=K, so primitive N=6, tau=1. The second factor is then constant. The common Jacobi poles now have order at most one and must be retained. With ell=2K/3 and v=K/3, `(r+v)-p=5ell` and 2K=3ell. These new simple poles therefore lie in exactly the same two allowed quotient classes. The unchanged first-factor double poles still cancel. No N=6 pole is discarded by invoking the odd-period input.

## 6. Common torus, nonvanishing and the half-step

Coprimality gives real period ell=4K/N to both full traces. Their imaginary anti-period is 2iK', so they are meromorphic on the compact torus `(ell,4iK')`. The preceding audits leave at most two simple poles for F, at r and r+2iK', and for H, at r+v and r+v+2iK'. Within either pair the points are distinct on this lattice. A maximal-lattice assertion is unnecessary.

Both F and H are positive on the real axis. If their permitted poles were all removable, compactness would make them constant and anti-periodicity would make them zero, a contradiction. Anti-periodicity pairs the two residues with opposite signs. Thus both actually have two simple nonzero-residue poles. Matching the residue of H(u+v) to that of F(u) removes both poles; the difference is constant and its anti-period forces zero. Positivity on the real line makes the proportionality scalar positive and real.

The actual original inverse edges have centers w+v+jdelta. The actual outer vertices are Q(w+v+jdelta), whose inverse edges have centers w+2v+jdelta. Consequently the residue comparison H(u+v)=kappa F(u) gives exactly the displayed outer/original ratio, not a phase-misaligned surrogate. This half-step is required in every period.

Central reflection plus a 2K phase shift interchanges original foci for both actual vertex sets. Applying the already phase-independent identity shows the same kappa for the other focus, without falsely treating 2K as a cyclic relabelling in odd period. Reversal changes both signs; repetition changes both areas by the same integer. The denominator has no real zeros in the strict domain.

## 7. Four-period source correction and verification

Direct rational tangent intersections, unit inversions and signed areas for the axial four-orbit give original inverse area 2/(ab), outer inverse area 1/(ab), and ratio 1/2. Both named tangent equations and the unit-inverse norm identity were checked independently for both foci. The explicit a=5,b=3,c=4 instance agrees. Thus the neighboring printed 2 is the reciprocal value for its displayed formula. This corrects a numerical source value without changing the k806,a target.

Both author scripts were inspected before execution, and both receipts replayed byte-identically: 22,496 exact assertions and 11,629 separately labeled numerical diagnostics. The fresh independent exact checker passed **13,272 assertions**, including actual tangent and inversion identities, both triple-angle additions, critical second derivatives, Laurent reflection, reduced multiplicities, the N=3/4/6 exceptions and rational four-orbit controls. A separate independent diagnostic passed **16,281 checks** over 42 primitive families at 85 digits, with maximum scaled residual `1.917538314e-84`. These used scale alpha=1.37, direct Euclidean intersections/inversions, both named tangent incidences, both foci, signed edge positivity, complex reflection and anti-periods, and the full complex shifted comparison.

Finite enumeration does not prove the unrestricted lattice assertions; their proofs are given above. Floating computations are non-interval diagnostics, not certificates. The universal result rests on exact geometry, a complete meromorphic pole audit, coprimality and compactness. All source reading files and rendered images are excluded from the portable review package.
