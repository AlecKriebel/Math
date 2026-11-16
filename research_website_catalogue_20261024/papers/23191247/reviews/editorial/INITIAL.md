# Source-first editorial INITIAL — row 152 / 23191247

Frozen first-pass purpose: identify the actual manuscript's claim and editorial constraints before opening current root or peer scientific findings. This is an informed editorial role, not a new blind scientific review, publication clearance or a replacement proof review. Earlier work in my own source/scope family on this same paper and its then-authorized primary-source interfaces is prior exposure. I have not reopened those findings, other review packets or foreign mathematical bodies during this phase.

The actual 255-line controlling TeX was read in full. All four original manuscript pages were personally inspected through the specifically authorized original root PNGs, without reading root review text. A read-only installed Poppler text extraction of the actual native PDF was also read completely. The manuscript necessarily supplies its own proof, verification description, dated source-audit assertions and opinions about contribution. These are source exposure, not independent acceptance. The native public API Description was read only after the whole manuscript; it necessarily exposes the author's summary and bounded-audit assertion. That exposure is disclosed, not treated as a scientific verdict. No support README, archived audit summary, acceptance/result body, project program, verifier, compiler or existing builder was opened or executed.

## Exact original abstract

Reznik, Garcia and Koiller observed that the sums of the distances from the two foci of an ellipse to their respective antipedal vertices agree along every closed elliptic billiard orbit. We prove this equality for every regular closed orbit tangent to a strictly nested confocal ellipse, including odd primitive periods, star orbits and repeated traversals. The difference of the two ordinary positive antipedal distances on each edge is a fixed coefficient times the vertical displacement of that edge. Closure therefore gives the equality without a parity restriction.

This is the complete abstract printed on manuscript page 1 and delimited by the TeX abstract environment. The native Zenodo Description is a distinct two-paragraph summary: it restates the theorem and verification, adds a dated bounded-literature assertion, background credit, literature/version limits and AI/unrefereed disclosure. It is not the original abstract and must not substitute for that abstract or be duplicated wholesale in a later light article. Its exact native bytes remain in the pinned record response. No current article copy has been drafted at this checkpoint.

## Quantifiers, object and construction

Fix real a > b > 0 and 0 < lambda < b^2. The outer ellipse is
E: x^2/a^2 + y^2/b^2 = 1,
and the strictly nested confocal elliptic caustic is
E_lambda: x^2/(a^2-lambda) + y^2/(b^2-lambda) = 1.
Let c = sqrt(a^2-b^2) and f_sigma = (sigma c,0), sigma in {+1,-1}.

Conditional on a regular closed orbit existing for these parameters, the theorem quantifies over every such finite cyclic list P_1,...,P_N on E. Consecutive endpoints must be distinct, every edge must be tangent to this same E_lambda, and continuation at every vertex must use the other of its two caustic tangents. Immediate retracing is excluded. P_(N+1)=P_1. The list may self-intersect, have any admissible winding, have odd primitive period, or repeat a shorter regular orbit. There is no parity restriction or convex-polygon/vertex-order restriction. This is not an existence statement for every integer period or every caustic parameter.

For each edge and each focus, Q_(sigma,i) is the intersection of the two full lines through P_i and P_(i+1), perpendicular respectively to P_i-f_sigma and P_(i+1)-f_sigma. It is an antipedal vertex of the original orbit polygon. The summand is the ordinary Euclidean norm q_(sigma,i)=||Q_(sigma,i)-f_sigma||, not a signed radial value, pedal foot, sideline height, original edge length or antipedal side length.

The exact claim is that all these antipedal vertices exist uniquely, their distances are finite and strictly positive, and
sum_(i=1)^N q_(+,i) = sum_(i=1)^N q_(-,i).
Thus the ratio of the two positive sums is 1 for every member of every admitted Poncelet family. Neither individual sum is asserted constant as the orbit varies.

## Source-first mechanism reconstruction

For noncollinear A,B,f the two perpendicular-line equations, after translating f to zero, are Q.A=||A||^2 and Q.B=||B||^2. With A=(r,0), B=(s cos(alpha),s sin(alpha)), r,s>0 and sin(alpha) nonzero, the positive norm is
||Q|| = ||A-B||/|sin(alpha)| = rs/h,
where h=dist(f,line(A,B))>0. Taking the positive root matters. This is an intersection of full lines, not rays or segments.

The manuscript's local other-tangent argument propagates a consistent side of the strictly convex caustic around the whole regular orbit. After choosing the caustic on the left, set outward unit normal n=(u,v), tangent t=(-v,u), support distance rho>0, K=a^2 u^2+b^2 v^2 and rho^2=K-lambda. The endpoints are
A=M-ell t, B=M+ell t,
M=(a^2 rho u/K,b^2 rho v/K), ell=ab sqrt(lambda)/K.
Substitution of M+z t into the outer ellipse gives constant rho^2/K, no linear term and quadratic coefficient K/(a^2 b^2); hence z=+/-ell. This reconstructs the chord formula within the stated domain.

The focal heights h_sigma=rho-sigma c u have product b^2-lambda>0 and sum 2rho>0, so both are strictly positive. Equivalently the foci lie strictly inside E_lambda because c^2<a^2-lambda. Thus no admitted edge passes through either focus; the distance lemma applies and gives finite positive ordinary norms. This positivity is a domain consequence, not an empirical convention or a signed-height substitution.

For an endpoint on E, its focal distance is a-sigma c x/a >= a-c>0. Multiplying endpoint distances and using the chord formula yields
R_sigma=(a^2 h_sigma^2+b^2 lambda)/K,
q_sigma=(a^2 h_sigma+b^2 lambda/h_sigma)/K.
Consequently
q_+ - q_- = (2cu/K)(-a^2+b^2 lambda/(b^2-lambda)),
while y_B-y_A=2ab sqrt(lambda) u/K. The common edge identity is
q_+ - q_- = Gamma (y_B-y_A),
Gamma = c/(ab sqrt(lambda))(-a^2+b^2 lambda/(b^2-lambda)).
The same parameters and Gamma apply around the consistently oriented orbit. Summing coordinate differences gives zero by actual cyclic closure. Positive summands make the ratio's denominator nonzero. This is the written universal telescoping mechanism; finite verifier cases cannot replace its all-real-parameter and all-admitted-period domain.

Orientation must remain explicit: reversing an edge leaves both antipedal intersections and q_+-q_- unchanged but negates its vertical displacement. In the reverse, caustic-on-right convention the displacement coefficient is -Gamma. A later summary must not claim the geometric norm difference is odd under reversal, nor apply a single left-convention coefficient to independently reversed edges.

## Finite editorial hand controls and boundaries

These are direct hand checks of the source formulas and wording, not a new scientific program or a new scientific acceptance campaign.

- A horizontal chord has u=0 and y_B-y_A=0. Its two focal norm values agree by the displayed difference identity, which never divides by u or by vertical displacement.
- For a=5, b=3, lambda=4, take outward n=(0,1). Then rho=sqrt(5), K=9, A=(10/3,sqrt(5)), B=(-10/3,sqrt(5)), both heights=sqrt(5), and both q=161/(9 sqrt(5))>0. This checks that a zero norm difference does not mean a zero ordinary norm.
- For the same parameters and n=(1,0), rho=sqrt(21), K=25, A=(sqrt(21),-6/5), B=(sqrt(21),6/5), h_+h_-=5, Gamma=-178/75, and q_+-q_-=-712/125=Gamma*(12/5). Reversing these endpoints preserves the norm difference but needs coefficient +178/75 with displacement -12/5.
- Gamma vanishes at lambda=a^2 b^2/(a^2+b^2), strictly within (0,b^2). This makes the two edge norms equal and does not make either norm vanish or invalidate the theorem. Its sign change is admitted.
- Closure, rather than an even-period pairing, cancels the sum. A repeated traversal simply repeats summands. The theorem includes admitted odd primitive periods and stars without asserting existence for every possible period.
- The strict inequalities are substantive. lambda=0 is the coincident-caustic/chord limit; lambda=b^2 is a degenerate caustic boundary where the focal-height product can vanish. Hyperbolic caustics, other degenerate limits, two-bounce limits and a=b circles are not included. No continuity extension to these cases is supplied by the stated theorem.
- The construction uses the original polygon. Replacing it by its outer tangent polygon, using pedal feet, side perimeters, signed lengths, or separately claiming either focal sum is constant changes the claim.

No defect, repair or narrower replacement is being proposed in this editorial INITIAL. Scientific acceptance and any current root conclusion remain unopened. The aim here is to prevent an article from silently broadening or misdescribing the source.

## Credit, priority and source-access limits to preserve

The observation is k603 of Reznik, Garcia and Koiller (D. Reznik, R. Garcia and J. Koiller in the actual bibliography). The manuscript cites their arXiv:2004.12497v11 (29 October 2020), sections 3.5/3.7 and Table 7, and the journal final Fifty New Invariants of N-Periodics in the Elliptic Billiard, Arnold Mathematical Journal 7 (2021), 341-355, section 3.7/Table 7, page 349. It attributes experimental discovery to May 2020 and the proof-unknown marker to that dated table. That historical marker supplies no present-open or exclusive-priority claim.

The manuscript credits classical negative-pedal/polarity geometry to Salmon, A Treatise on the Higher Plane Curves, third edition (1879), Articles 121-122, pages 105-107; the known focal sideline-height product to Bialy and Tabachnikov, Dan Reznik's identities and more, Lemma 4.2, European Journal of Mathematics 8 (2022), 1341-1354; central inversion for centrally paired orbits; and ordinary telescoping as familiar. Its proposed contribution is the ordinary norm-difference/coordinate-increment identity and resulting full-period proof, particularly odd primitive periods, not discovery of the invariant or invention of antipedals, the height product or telescoping.

The source distinguishes Roitman/Garcia/Reznik focal inverse perimeters from these summands, and Garcia/Koiller/Reznik spatial averages from this finite norm difference. Its 6 October 2026 bounded audit assertion includes selected final/precursor comparison, final-book versus author-source boundaries, unread historical/experimental material, finite corpus and version limits. Those are source-reported historical limits at this checkpoint, not a newly rerun literature search. There is no absolute-first, exhaustive-literature or continued-open-status guarantee. None may be inferred from missing results. No foreign primary body has been newly opened in this editorial phase.

## Native identity, order, rights and disclosure

Title: A telescoping proof of the focal antipedal sum invariant. Author: Alec Kriebel, Independent researcher, ORCID https://orcid.org/0009-0001-9320-500X. DOI: 10.5281/zenodo.23191247; concept DOI: 10.5281/zenodo.23191246. Both the manuscript and native record declare version 1.0 and 6 October 2026. Native created: 2026-10-06T14:46:33.214104+00:00; updated: 2026-10-10T21:28:59.670909+00:00. The later update timestamp is not evidence of another manuscript version. Resource type is Preprint/publication/preprint, access open, language eng, state done. The native is_published field is absent; absence must stay absence, not be converted to a native false/null/true assertion.

There are exactly two native asset entries, literally PDF then ZIP in both record.files and the dedicated entries array: focal_antipedal_sum.pdf (65,142 bytes, four pages), then focal_antipedal_sum_support.zip (113,446 bytes). The dedicated custom order is literally [] and default_preview is null. The ZIP lists 33 members; only names, sizes and dates were read as inventory, not support opinions or result bodies. The embedded PDF has the same byte hash as the separately deposited actual PDF. Native API content links, names, checksums and order are in SOURCE_PINS; any later local reader/downloads must preserve unchanged native files.

The actual targeted LICENSE was read completely. Copyright 2026 Alec Kriebel; the manuscript and all original authored support files are CC BY 4.0. This includes authored support code under that actual notice; no unsupported MIT split from a different paper may be imported. Preserve attribution, indicate adaptations, and retain cited third-party works' independent rights. Their full bodies are not distributed in the native package. The record also declares cc-by-4.0.

The manuscript discloses extensive AI use in solving, deriving, drafting, literature checking, code generation, verification and adversarial checking. Independent checks include AI agents and are not conventional human peer review. The manuscript is unrefereed and has not received conventional human peer review. These material status facts must remain in later copy.

## Gate and checkpoint

Source-first editorial pass: 100% complete. Overall private editorial packet: approximately 20%, with article drafting gated on root's concrete authority after reading this actual INITIAL. AA, canonical/base/production URL and publication authority remain absent/null/false as applicable; follow-up defaults to null. No W, Git, Sheet, source, old packet, live/deployment, external contact or prepared-outreach changes occurred. All files for this effort remain in the new owned editorial directory. Freeze these initial files and wait for root; do not open current scientific judgments or draft a page on source-only authority.
