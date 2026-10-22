# Publication edition: complete independent mathematical audit

This is an AI-assisted, unrefereed mathematical edition. Acceptance means an independent internal AI audit of the full theorem under its explicit curve and density conventions. It is not external human peer review, journal acceptance, formal proof-assistant certification, or a novelty or priority claim.

The full authored proof and complete mathematical audit are retained in PROOF.md and AUDIT.md. Copied source documents, source text and images, executable code, raw datasets, raw search responses, independent preparatory material and private coordination material are not distributed. This is a written proof-and-audit edition, not a computational reproduction package.

Source retrieval and inspection statements describe the candidate and independent audit of October 11, 2026 UTC. Editorial preparation authenticated their sealed bytes and checked repository publication scope, but performed no new scholarly-source retrieval, source-body inspection, literature survey or mathematical execution. Hashes authenticate bytes; mathematical acceptance comes from reading the written arguments.

The original audit below is preserved in full mathematical substance. Its original manuscript reference is identified as historical, and one private coordination digest plus the associated source-inventory phrase are omitted. Every mathematical argument, qualification, challenge and source-inspection limitation is unchanged.

# Independent mathematical acceptance report

**Target:** 2307058 / AMR-022-7058; Hayman–Lingham Problem 7.58.

**Verdict:** ACCEPTED for the full theorem under the explicitly stated all-connecting-curves, extended-Borel-density, 2-modulus conventions. No mathematical correction to the frozen proof is required. This verdict is a mathematical audit result, not a claim of priority, exhaustive literature coverage, or a formal proof-assistant certificate.

**Original audited proof (retained in PROOF.md):** 16,705 bytes, SHA-256 `33e2393c52e0b01b099cabf8696d9bd32aef5fae94903f9e8b1bc8c4af7e533d`.

**Audited candidate manifest:** 1,159 bytes, SHA-256 `df44ee0674b3e6de3d29eea9445a830930199995597b01f5012933e50edb9307`.

The proof was read in full after the pins were supplied. All five candidate members were independently checked against their byte counts and hashes. No supplied proof-author or source-author code was executed. Mathematical acceptance comes from the argument review below, not from these byte checks.

## 1. Exact result and scope

For every compact E⊂[0,1] embedded in the real axis, with F=R\\E taken within that axis, the proof establishes

M₂(Γ(E,∂B(0,2)))>0 ⇒ M₂(Γ(E,F))=∞.

Both curve families are taken in the whole plane. Curves are continuous, may be merely locally rectifiable away from their endpoints, and have nonnegative line integrals defined by increasing interior-subcurve limits. Every compact rectifiable connector is included. Admissibility applies to every curve, and densities may take the value infinity on sets of planar measure zero. The proof also works if only globally rectifiable connecting curves are used consistently throughout.

The source formulation was checked in the authenticated PDF page image and the current public arXiv HTML. No positive-length or interval hypothesis replaces positive capacity. The proof's final step explicitly handles compact sets of zero length and positive capacity. It does not substitute the planar complement for F, use a bounded surrogate for F, or silently discard exceptional curves.

This scope is explicit because the source itself does not spell out every endpoint convention. The audit does not claim to settle additional interpretations that change the stated connecting-curve family.

## 2. Dependency review

### Lemma 1: pointwise lower-semicontinuous majorant — PASS

The construction majorizes h=ρ² using relatively open covers of its dyadic superlevel sets. The sum defining H is lower semicontinuous, the square-root preserves this property, and g≥max(ρ,1) holds at every point. In particular a point where ρ=∞ belongs to every superlevel set and retains g=∞. This is essential; an almost-everywhere replacement of a density would not suffice for every-curve admissibility.

The arithmetic checks: Σ_{k≥0} 2^{k+1}1_{h>2^k}≤4h, and the open-cover error contributes Σ_{k≥0} 2^{-k-3}=1/4. Thus ∫g²≤|Q|+4∫ρ²+1/4. This does not rely on an unjustified L² triangle inequality for the dyadic series.

### Lemma 2: path distance and measurability — PASS

The auxiliary paths lie in compact Q and start in compact E. The lower bound g≥1 bounds ordinary length by weighted cost. Nearly minimizing paths therefore admit uniformly Lipschitz parametrizations on a common interval. Uniform limits preserve the required endpoints and remain rectifiable in Q.

The proof supplies the needed weighted-length lower-semicontinuity argument rather than assuming it for arbitrary Borel weights. For continuous weights, the partition lower sums are continuous under uniform convergence and their supremum equals weighted length. Uniform continuity of the weight and approximation of curve variation justify the equality. Increasing continuous approximants to the lower-semicontinuous extended-valued g then give the conclusion by monotone convergence. The displayed infimal-convolution approximants are finite, continuous, increasing, and converge pointwise even at g=∞.

Consequently d is lower semicontinuous, including infinite-distance points, and u=min(1,d) is Borel. Neither attainment of every distance nor continuity of u is assumed.

### Path inequality, plate values, and Sobolev regularity — PASS

Near minimization plus concatenation yields the truncated path inequality for all rectifiable connections in Q. Infinite distances cause no failure: a finite-cost connection from a finite-distance point would make the other distance finite; otherwise the inequality is immediate after truncation.

Constant paths give u=0 at every point of E. Every auxiliary path ending at F∩Q is a member of the original admissible family, giving u=1 there. These are actual point values, not values assigned to an arbitrary representative of a Sobolev class.

Fubini gives integrable restrictions of g on almost every coordinate line. Applying the path inequality to every subsegment proves absolute continuity of the actual potential on those lines, with coordinate derivatives bounded by g. Slice integration by parts identifies weak derivatives. The proof correctly uses the sufficient bound |∇u|²≤2g²; a sharper gradient bound is unnecessary.

### Actual trace identification — PASS

The cutoff η equals one near the entire segment [0,1]×{0} and is supported inside Q. Therefore w=η(1−u), extended by zero, is compactly supported W¹,². Along almost every vertical line its actual value at height zero is 1_E. The excluded lines form a set of one-dimensional measure zero, which suffices for the L² trace. No claim that this exceptional set has zero conformal capacity is made or needed.

This is the correct distinction between a Sobolev trace class and prescribed values on a possibly positive-capacity null set. The later circle argument, not an invalid trace-to-capacity inference, treats that null set.

### Lemma 3: Fourier trace estimate and limit passage — PASS

For smooth w, integrating the derivative of |W(ξ,y)|² over y>0 gives the stated estimate. Multiplication by |ξ| and 2ab≤a²+b² produce the horizontal-plus-vertical Dirichlet energy. The ξ=0 case presents no division or singularity.

For general w, mollification converges in W¹,². The separate one-dimensional estimate of the L² trace proves that the smooth traces converge to the actual vertical ACL trace. Fourier L² convergence supplies a subsequence converging almost everywhere, and Fatou passes the weighted estimate to w. Thus the proof does not identify a trace merely by pointwise convergence of mollifications on the axis.

Plancherel, Tonelli, and the substitution t=ξh give the claimed difference-quotient identity. The constant is positive and finite, since its integrand is bounded at zero and decays quadratically at infinity.

### Lemma 4: characteristic rigidity — PASS

The proof correctly telescopes in L¹, where translation preserves the norm. For 0<h<1 and N=ceil(2/h), the supports of f and its Nh-translate are disjoint and N≤3/h. Hence

||f(·+h)−f||²₂=||f(·+h)−f||₁≥(2/3)|E|h.

Integrating after division by h² forces logarithmic divergence whenever |E|>0. This quantitative argument works for every measurable subset of [0,1], including positive-length sets with no intervals. It is not the incorrect assertion that length zero and conformal capacity zero are equivalent.

### Lemma 5: finite augmented-cost paths and small circles — PASS

The augmentation q=ρ+1_{B(0,3)} is globally square integrable and remains admissible. If an E-to-radius-2 connector has finite q-cost, its portion before the first outer-circle hit has finite ordinary length, including endpoint behavior, because q≥1 throughout that portion. This legitimizes arclength parametrization even when the original family admits infinite Euclidean length near endpoints.

For the resulting specific starting point e∈E, polar integration gives ∫₀^δA(r)dr<∞. Since |E|=0, e+r∈F for almost every r. Removing those exceptional radii leaves full measure, so logarithmic divergence of ∫dr/r forces a decreasing sequence of good radii with rA(r)→0. The selection is made separately for the actual starting point; no uniform almost-everywhere assertion over E is used.

The first-exit arclength parameters tend to zero because an arclength-parametrized nonconstant curve has no constant initial interval. Finite q-cost then makes the initial costs tend to zero. The full-circle Cauchy–Schwarz bound is √(2πrA(r)), so a circular arc adds cost tending to zero. The concatenation is an actual globally rectifiable E-to-F curve, and eventually violates admissibility. Extended density values do not spoil this estimate on the selected finite-integral circles.

### Final modulus implication — PASS

Lemma 5 rules out finite q-cost for every E-to-outer-circle curve. Therefore q/n is admissible for that entire family for every positive integer n, while its energy tends to zero. Curves with infinite q-cost are included in this final admissibility statement. The proof uses the definition of modulus directly; no touching-plate capacity identity, quasi-everywhere boundary theorem, or unproved equivalence is hidden in this step.

The empty set is correctly separated, and finite modulus supplies at least one finite-energy admissible density without any assumption that an extremal density exists.

## 3. Independent challenges

The following possible failure modes were specifically tested against the written argument:

- Densities infinite on the real line, on E, or on a dense null set: covered by pointwise majorization and actual curve integrals.
- Fat Cantor-type E with positive length and no interval: covered by the arbitrary-measurable-set translation bound.
- Zero-length E with positive capacity: not dismissed by trace theory; handled by the separate small-circle contradiction.
- Infinite distances and nonattained path infima: covered by truncation, near minimizers, compactness, and lower semicontinuity.
- Positive-capacity exceptional trace points: no capacity conclusion is drawn from the null family of exceptional vertical lines.
- Infinite Euclidean length or pauses near a curve endpoint: controlled by q≥1 before the first outer-circle hit and arclength reparametrization.
- Infinite winding, retracing, and many returns to e: do not prevent first-exit parameters from tending to zero in arclength.
- Exceptional radii depending on e: harmless because the proof fixes the endpoint before using polar integration.
- Noncompact F: no compactness of F is required; the actual endpoint e+r belongs to the original F.

No explicit obstruction or counterexample to the stated theorem was found. The audit includes an independent reconstruction of the argument and a complete exact-text review. The author's self-review was not treated as independent validation.

## 4. Source and novelty boundaries

The current arXiv record still identifies version 2, dated 21 September 2018. The target statement on printed page 178 / PDF page 179 agrees with the live HTML. Its historical update cannot establish the problem's worldwide status in 2026. [Hayman–Lingham record](https://arxiv.org/abs/1809.07200), [public problem text](https://arxiv.org/html/1809.07200v2).

The later 2019 Springer book and its Miscellaneous chapter were verified through the publisher. The chapter page is subscription-only for the problem text in this access route. A non-primary search result suggested an additional editorial warning about unclear terminology, but the relevant 2019 page was not authenticated from a primary source. The audit therefore does not attribute that warning to the publisher as an established fact; it retains the explicit convention boundary. [Publisher book record](https://link.springer.com/book/10.1007/978-3-030-25165-9), [chapter record](https://link.springer.com/chapter/10.1007/978-3-030-25165-9_7).

The critical characteristic-rigidity principle is established background mathematics. Brezis's author-hosted paper explicitly discusses integer-valued critical fractional Sobolev functions and measurable-set rigidity. The candidate gives its own short proof of the special case it needs. [Brezis, *How to recognize constant functions. Connections with Sobolev spaces*, Corollaries 1–2 and Remark 3](https://sites.math.rutgers.edu/~brezis/PUBlications/180.pdf).

The flat trace theorem and Fourier/Gagliardo equivalence are also standard and are corroborated by Propositions 3.8 and 3.4 of Di Nezza–Palatucci–Valdinoci. The candidate proves the specific estimates it uses instead of importing an unchecked theorem. [*Hitchhiker's guide to the fractional Sobolev spaces*](https://arxiv.org/abs/1104.4345).

A bounded current search using the numbered problem, the Gonchar/Vuorinen attribution, real-axis complement, modulus, and capacity did not locate a directly matching later resolution. This is not an exhaustive literature review and does not establish novelty or priority. No third-party source text or source PDF is incorporated into this report.

## 5. Acceptance conditions and recommendation

The exact pinned theorem and proof are mathematically accepted with the scope above. Required mathematical revisions: none. Remaining unresolved matters are historical interpretation beyond the stated convention and scholarly priority, not a proof gap in the audited statement.

Any later change to the theorem, proof, or curve conventions requires a fresh check of the changed bytes. Hash validation by itself is not mathematical acceptance, and this report does not certify unrelated candidate files or later revisions as proofs.
