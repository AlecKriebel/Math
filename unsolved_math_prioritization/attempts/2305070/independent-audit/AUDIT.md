# Independent adversarial audit: Function Theory 5.70

Problem: **2305070 / AMR-022-5070**, queue rank **580**. Audit date: **2026-10-04 UTC**.

## Verdict

**Accept the frozen package as an unsolved, five-approach auxiliary-results report.** No mathematical correction, refreezing, or change to the proposed **unsolved 5/5** disposition is required. This is not acceptance of a solution, a novelty claim, or a verified statement that the problem remains open in 2026.

The explicit example in Proposition 2 does exactly what the report says: one regular modulus level has infinite total Euclidean length, while every connected component of that level has finite length. It does not solve the original single-component problem. The other auxiliary arguments are valid within their stated scopes.

There is one nonblocking verifier-hardening observation, recorded separately in CORRECTIONS.md. A strict independent inventory confirms that it does not affect the actual frozen package.

## Frozen material and independence

Reviewed all ten files in the public directory, including the nine files listed in its manifest and the manifest itself. Pinned inputs:

- SHA256SUMS.json: 1,273 bytes; SHA-256 `f6a39e0a6792db78f658e80dcc6f6efbc1299e1975aea31c1f06f24581aaf4ab`.
- PROOF.md: 14,121 bytes; SHA-256 `1e9ce20ecb43599cc42bda704730e67390008fd1a679779961ecf28293d7c347`.

The full proofs, code, checks, attempt log, status, source manifest, and source gate were inspected. Source records and recorded repository responses were also checked. This audit independently rederived the crucial component and length calculations and replayed the finite controls. No helper was used, no remote write was made, and no frozen byte was edited. New audit artifacts are confined to this separate directory.

The five unsuccessful approaches were already complete at freeze. The audit did not continue the unfinished mathematical search or assert a sixth substantive approach.

## Exact target and source fidelity

The target is one bounded, nonconstant holomorphic function on the open unit disc, one positive modulus, and one maximal connected component of that modulus level which has infinite Euclidean one-dimensional Hausdorff measure and has no branch point. Total length summed over different components is insufficient. A curve's repeated traversal and hyperbolic length do not replace Euclidean set length.

The complete Problem 5.70 and its update were checked in [Hayman–Lingham's primary source](https://arxiv.org/abs/1809.07200), printed page 111, PDF page index 111. The report faithfully preserves the distinction from the older highly branched example. The 2018 no-progress update is historical evidence only. A fresh download matches the archived PDF exactly.

Nonconstancy and a positive modulus are appropriate explicit conventions: zero sets of a nonconstant analytic function are discrete, while a constant function does not furnish the intended one-dimensional regular component.

## Proposition 2: adversarial component audit

Write W(z)=(1+z)/(1-z), G=exp(-W), and F=exp(G). The Cayley map is a homeomorphism and conformal bijection from the disc onto the open right half-plane. Therefore F and its reciprocal are bounded, F is zero-free, and

    F'(z) = -2 F(z) G(z)/(1-z)^2

never vanishes. In W=x+iy coordinates, the modulus-one equation is exp(-x) cos(y)=0. Thus the level is exactly the disjoint union of horizontal half-lines

    H_k = {x+i*pi*(k+1/2): x>0}, k in Z,

pulled back by the inverse Cayley map.

The maximal-component step is essential and correct. If A is any connected subset of the union of the H_k, the continuous imaginary-coordinate image Im(A) is connected and lies in the discrete set pi*(Z+1/2). It is a singleton. Consequently A is contained in a single H_k. Each H_k is connected, so it is a maximal connected component; the homeomorphism preserves that fact. Mere disjointness of the H_k would not have sufficed, but the proof supplies the required extra argument.

For b_k=pi*(k+1/2), the injective parametrization z_k(x)=(x+i*b_k-1)/(x+i*b_k+1) has speed

    |z_k'(x)| = 2/((x+1)^2+b_k^2).

The length is consequently

    L_k = (2/|b_k|)*(pi/2-arctan(1/|b_k|))
        = 2*arctan(|b_k|)/|b_k| < infinity.

No b_k is zero. For k>=0, arctan(b_k)>=pi/4 yields L_k>=1/(2k+1), whose sum diverges. The components are relatively closed Borel subsets of the disc and hence ambient Borel subsets. Countable additivity of Hausdorff measure applies; the parametrizations are injective, so this is not length obtained by repeated traversal.

At x tending to infinity all these curves approach the same boundary point 1, but that point is absent from the domain and the level. It cannot join their components. Negative k merely gives the reflected partner L_(-k-1)=L_k; the positive-index subfamily alone establishes divergence.

**Quantifier conclusion:** for the particular level {|F|=1}, every component is finite and their union has infinite length. The proof does not infer the existence of an infinite component from an infinite sum. The statement need not be read as a theorem about every modulus of F. This audit accepts exactly the modulus-one assertion used in the report.

## Remaining mathematical assertions

### Local normal form and compact components

The local logarithm exists because the level modulus is positive. Factoring its first nonzero term and taking a local analytic root gives the conformal coordinate with level Re(w^m)=0. There are 2m distinct local rays. All their incident arms belong to the same component at the common point; a critical point cannot be made harmless by selecting one pair of arms and calling it a maximal component. Thus unbranchedness is equivalent to F' being nonzero along the component.

On sufficiently small compact coordinate neighborhoods the inverse derivative is bounded, giving finite local length, including at branch points. Finite compact covers then establish finite length inside compact subsets of the disc. The zeros of a nonzero analytic derivative are discrete and countable, so only countably many positive critical moduli are excluded. A compact regular connected component is a compact one-manifold without boundary, hence a circle. For a zero-free F, a global logarithm and the maximum principle exclude such a circle. These claims retain the nonconstant ambient hypothesis.

### Polynomial and rational bounds

The Crofton normalization is correct: integration over unoriented line normals theta in [0,pi) has factor 1/2. The t-range for lines meeting the unit disc has length 2; the almost-everywhere intersection count is at most d. The resulting bound is pi*d. Passing to a square-free polynomial preserves the zero set, does not increase degree, and reduces the singular locus of a plane algebraic curve to finitely many points. Those points have zero one-dimensional measure. Lines lying in the zero set constitute a measure-zero exceptional family. Exhaustion by finite collections of compact regular arcs justifies the passage to the full set.

The modulus and real-part equations for R=P/Q have degree at most 2n. They cannot vanish identically for a nonconstant rational R, by the open mapping theorem. A nonreduced presentation only adds possible polynomial zeros and cannot invalidate the upper bound. Applying the real-part case to Re(R)=log(c) gives the claimed bound for modulus levels of exp(R). No boundedness of exp(R) was silently needed for this auxiliary statement. A pole of R on the boundary does not invalidate algebraic degree counting inside the disc.

### Univalent pullbacks and the simple covering

[Hayman–Wu, Theorem 1, page 366](https://www.researchgate.net/publication/226448362_Level_sets_of_univalent_functions) was freshly checked in the author-uploaded primary article text. It gives a universal finite length estimate for preimages of lines or circles under univalent maps. Its hypotheses cover the report's stated applications to F or to a univalent logarithmic parameter. The proof is an explicitly cited external dependency; this audit does not claim to reprove its 38-page argument. Local univalence alone is not substituted for global injectivity.

For S_a=exp(-aW), the modulus-level equation really is Re(W)=s, not a family indexed by covering windings. The inverse image is a circle with center s/(s+1) and radius 1/(s+1), with the point 1 omitted. Its length is 2*pi/(s+1). The formula and the Euclidean/hyperbolic distinction check.

### Herglotz tails

The assumptions |zeta_j|=1, a_j>0, and finite total mass imply the displayed locally uniform majorant. The positive Poisson kernel proves Re(H)>0, and exponentiation supplies a bounded zero-free analytic function. Termwise differentiation is justified locally, and the derivative majorant is exactly 2*T_N/(1-r)^2. The finite truncations have rational degree at most N and are covered by the preceding 2*pi*N estimate.

The report correctly restricts implicit-function persistence to fixed compact regular pieces. It does not turn that local assertion into a global component-preservation theorem. The caveat to maintain nonconstancy is conservative and does not create a gap; the positive purely atomic setup is more restrictive than arbitrary Herglotz measures.

### Prescribed arc and compact-limit example

For gamma(t)=1-1/t+i*sin(t^2)/t, t>=2, the strictly increasing real coordinate gives injectivity and the positive real part of gamma'(t) gives regularity. Since 1+sin(t^2)^2<=2<2t, the curve is inside the open disc. Its successive alternating extrema occur at t_n=sqrt(pi/2+n*pi), n>=1, all in the parameter domain; the sum of vertical displacements diverges like the sum of n^(-1/2). Its length divergence is therefore a set-length assertion for an embedded curve.

The complex inverse function theorem supplies the stated local level realization. Nothing in that theorem provides a single bounded extension to the whole disc, and the report explicitly acknowledges the gap. The equivalence with a bounded harmonic real part in the zero-free, bounded-reciprocal subclass is correct.

For F_n=exp(z^n-exp(-n^2)), the uniform e bound and convergence to 1 on compact subsets hold. The vertical chord Re(w)=exp(-n^2) avoids 0; its inverse under z^n has exactly n disjoint inverse branches. Each arc has two ends of limiting radius 1, and contains a point of radius exp(-n). Total radial variation gives length at least 2*(1-exp(-n)) per arc. The derivative is nonzero along those arcs; when n=1 there is no critical point at all. The limit's constancy is precisely why these finite-stage bounds do not settle the target.

## Reproduction and provenance

- `python3 public/verify.py` succeeds. Its stdout agrees **byte-for-byte** with frozen CHECKS.json.
- `python3 public/verify_manifest.py` succeeds and reports nine listed files.
- `independent_checks.py` separately verifies the exact ten-file inventory, lack of symlinks, every frozen size and hash, nine independently chosen exact Cayley/circle cases, and ten signed-index component-length quadratures. The latter are expressly floating diagnostics; the written argument above proves the relevant infinite statements.
- `source_recheck.json` records fresh HTTP 200 retrievals of both pinned source corpora, the Hayman–Lingham PDF, and the Nicolau–Reijonen PDF. All four byte counts and SHA-256 values match the frozen source manifest. Both selected corpus records agree with the saved record/report. No raw corpus or PDF was retained in the audit directory.
- Recorded repository responses support the source gate's stated snapshot: main df9f2c05f61cad48f851c2d2ba7a63611a0acfa0; the exact queued 0/5 row; no selected-ID state entry or group membership; empty matching-PR result; and a 404 per-ID attempt directory. These are checks of the recorded read snapshot, not a guarantee about subsequent repository state or differently named materials.

The fresh corpus digests are:

- problems.json, 68,931,837 bytes: `04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf`.
- research_results.json, 80,334,822 bytes: `8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b`.

The fresh scholarly PDF digests are:

- Hayman–Lingham, 1,706,228 bytes: `8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0`.
- Nicolau–Reijonen, 355,623 bytes: `5a16540ad388835640633dbe1de68ef71ab3d3a491bd98748c0744dcc26842c1`.

[Nicolau–Reijonen's final discussion](https://mat.uab.cat/~artur/data/nicolau_reijonen_nou-1.pdf), author PDF page 9, concerns total level length and a different inner-function question. It does not assert the missing single-component conclusion. The report's distinction is accurate.

Fresh attempts at the [Barth–Clunie publisher PDF](https://www.ams.org/journals/proc/1982-085-04/S0002-9939-1982-0660605-9/S0002-9939-1982-0660605-9.pdf) failed with 403. The [Jones publisher page](https://projecteuclid.org/journals/michigan-mathematical-journal/volume-27/issue-1/Bounded-holomorphic-functions-with-all-level-sets-of-infinite-length/10.1307/mmj/1029002311.full) did not expose its article proof. Their proofs have not been independently reconstructed. Neither is needed to validate Proposition 2 or the remaining self-contained auxiliary arguments. The historical branched-example description is supported by the primary problem list; the Jones scope is explicitly secondary to the cited later primary article.

Additional exact-phrase and bibliographic searches did not establish a later resolution. This bounded negative search does not certify current open status or novelty. The frozen package already states this limitation correctly.

## Disposition and stopping condition

The artifact's full-target-resolved, complete-candidate-proof, and novelty flags are all false and agree with the proofs. The five approaches are distinct but acknowledged to originate in one research pass; they are not falsely represented as five independent discoveries or audits. Their numerical completion estimates are labeled subjective planning values.

The remaining task is still exactly the original global component problem. None of the auxiliary results closes it, and no result should be promoted to a full solution. The current campaign coordinator confirmed **unsolved 5/5** as the required publication label; a different label in older saved repository guidance is an administrative mismatch resolved by the current campaign instruction, not a reason to alter the frozen report.

**Acceptance:** publishable as the stated unsuccessful attempt with proved auxiliary controls, subject to the root's normal publication gate. No further proof-search turn is authorized by this audit.
