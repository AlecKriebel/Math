# Findings: independent falsification of the PR 630 priority candidate

Completed UTC: 2026-10-15T04:03:19.355514+00:00
Assigned review completion estimate: 100%.
Pinned original head: `810cd5c148bbae7c7c5a47423c375ada98e903b6`; all 28 original artifact identities are preserved in SOURCE_BINDINGS.json.

## Result

The proposed prior-example implication survives independent falsification. The central negative answer to the literal universal IM replacement already follows, by an explicit admissible parameter choice and differentiation, from the directly relevant 2009 Example 1. This is a mathematical prior implication, not a finding that the source named the identical 2007 question, not a finding of earliest priority, and not an allegation of copying.

The exact calculation is B=2b in the source's g_B=(B/4)z^2, yielding g=bz^2/2, g'=bz, and g''=b. At a=0 and k=2, the zero sets of g and g' are both {0}, their multiplicities differ, g'=b occurs at z=1, and the higher derivative condition holds identically. The proposed nonzero exponential form is zero-free and therefore fails. The catalogue's extra b!=a also holds.

## Source and scope attacks

- **Actual printing:** Independently inspected complete relevant page images and independently re-rendered the local publisher PDFs. The 2009 p.68 formula really has coefficient b/4. Printed 2007 pp.501-503 were read in full; p.503 independently states k>=2 and b!=0 with no a!=0 restriction in Theorem H.
- **Parameter mismatch:** Renaming the source parameter B avoids conflating it with the target b. B=b would fail the target because g''=b/2. B=2b is permitted and fixes exactly that mismatch.
- **Different predicates:** The source's condition is g'=B implies g=B, whereas the target is g'=b implies g''=b. The argument does not substitute one for the other. It proves the second directly from the formula.
- **IM versus CM:** Both sources define IM by equality of fibers; multiplicities two and one are permitted for IM and forbidden for CM. The CM theorem is not contradicted.
- **Universal versus fixed order:** The k=2 instance alone disproves the literal universal assertion. The source quadratic does not work for k>2. Any assertion that this source alone gives the PR's all-order family would overstate it.
- **Literal versus intended:** The permitted a=0 reading is verified. A conjecture that a!=0 was intended is not used either to validate the PR or to establish priority. The strengthened question remains open within this packet.
- **Prior example versus resemblance:** This is a dated, explicit zero-IM counterexample in the same entire-function/derivative uniqueness setting that instantiates to the identical target witness. Direct global checks establish every target predicate. The evidence is more specific than recognizing a familiar quadratic, but less than a documented prior statement of this exact original problem's answer.

## Reasonable repair assessment

The PR's all-order monomials and complete polynomial classification are correct. They prove stronger statements than the existence of one counterexample to the universal assertion: at every fixed k>=2 and b!=0 the displayed polynomial is a witness, and there are no other polynomial instances. Those stronger quantifiers must remain explicit. I did not find a prior source stating that exact all-order result verbatim.

The polynomial structure is specifically covered by an earlier theorem, not dismissed on grounds of ease: Novikov-Yakovenko's author manuscript Proposition 7, p.27, attributed to Chademan, makes a polynomial with sole critical value zero a translated monomial. Zero IM sharing puts every critical point over zero. The remaining target-specific steps exclude nonzero a and select degree k and coefficient b/k! by degree/root-fiber counts. Thus a classification-focused repair would be a direct application with an additional target-condition computation. This narrows the claim of new structure while preserving the exact target statement's unresolved historical priority.

The squared-exponential shape is explicit in 2009 Example 3 and Theorem 1.2(d). The PR's exact lambda calibration is a valid additional derivative-value computation, with historical priority undetermined. Known shape does not itself prove prior occurrence of the exact derivative resonance, and coordinate scaling does not license transferring a different pointwise implication.

These facts support rejecting a claim that the packet provides a *new resolution of the original universal assertion*: that assertion's negative answer is already supplied by the prior explicit quadratic after the displayed checks. They do not justify the broader assertion that every supporting formula or exact refinement was previously published, or that no separate attributed incremental note could have originality. A note centered on the all-order classification or calibration would require a separately stated contribution and priority assessment. It would not restore novelty to the already implied universal yes/no answer. This conclusion does not rely merely on the arguments being elementary or on failure to find a first historical statement.

## Closure-comment review

Final reviewed candidate SHA256: `efd589fe0fe26040c36713b3c02999138eef3b9244e6db8c6e5cb57aaa234a73`.

There are no mandatory or optional open wording edits at this SHA. The root adopted the earlier optional clarification that a separately scoped attributed note might focus on classification, parameter calibration, or source clarification. The final candidate accurately limits the prior-example implication, preserves valid refinements, disclaims identical-question attribution and earliest priority, and leaves exact target specializations' historical priority undetermined. Its polynomial-corollary sentence is supported by independently checked Proposition7 and direct derivation. No statement that every exact refinement was published verbatim has been introduced.

## Exact remaining gaps

No gap remains in the direct k=2 mathematical implication. The audit does not establish earliest historical recognition of the literal question; the exact 2003 theorem's full text or its authors' intended scope; prior publication of the complete all-order target classification or precise lambda calibration; or any result for the strengthened a!=0 problem, transcendental k=2 problem, or full entire-function classification. Those uncertainties do not undo the explicit prior witness to the universal negative answer, and they must not be promoted into negative findings about every conceivable separate contribution.

## Provenance and independence

INDEPENDENT_DERIVATION.md was saved at 2026-10-15T03:58:47.628610+00:00 before any other new priority report was read. Subsequently only a root-supplied primary-source lead and the requested closure candidate were considered. No other new priority review was read at any stage. No Git operation, remote write, external outreach, paper, release, or disposition was performed.

Primary links: [2009 publisher PDF](https://www.impan.pl/shop/en/publication/transaction/download/product/84815), [2007 publisher report](https://ems.press/content/serial-article-files/46093?nt=1), [Novikov-Yakovenko author manuscript](https://pi.math.cornell.edu/~novikov/Papers/redundant.pdf). Exact source-file and rendered-page hashes are in SOURCE_BINDINGS.json; full temporary source copies are ignored beneath this review's tmp directory.

## Final supplement: 2004 exact all-order formula lead, limited provenance

Recorded UTC: 2026-10-15T04:03:19.355514+00:00. Following completion of the central review, the root supplied another primary-source lead. I independently opened the author-uploaded 2004 article through the web PDF reader and inspected its extracted Lemma 5 on printed pp.323-324 (the browser reported a 19-page article, Spring 2004, volume 48, pp.319-337). The article is Chang-Fang-Zalcman, Normal families of holomorphic functions. Its Lemma 5 assumes an entire function of order at most 1, zeros of multiplicity at least k, a nonzero parameter B, and implications g=0 => g^(k)=B and g^(k)=B => g^(k+1)=0. It prints g=B(z-z0)^k/k! for k!=2 and the quadratic B(z-z0)^2/2 among the alternatives for k=2.

These lemma hypotheses differ from the target's hypotheses and the lemma is not invoked as a target necessity theorem. The displayed formula itself, with B=b, gives the same all-order polynomial family. For every k>=2 its zero set and its derivative's zero set are {z0}, its kth derivative is identically b, and its derivative's b-fiber has k-1 distinct points. Thus the same direct checks already given above make each displayed prior formula a target counterexample. This is an additional prior-explicit-formula implication for the all-order construction, beyond the independently byte-bound 2009 quadratic implication. It does not establish that the exact target theorem/classification or target application was published verbatim.

Provenance limitation: direct downloading through the local HTTP client returned403; no complete 2004 PDF bytes or SHA256 were obtained. Web PDF text was independently accessible; screenshot requests returned references without usable image pixels in this tool bridge, so this review does not claim an independent visual or byte-level check of the 2004 source. URL: https://www.researchgate.net/profile/Lawrence-Zalcman/publication/258233263_Normal_families_of_holomorphic_functions/links/555b0fb008ae6fd2d828632a/Normal-families-of-holomorphic-functions.pdf . The central disposition and final comment do not rely on this supplementary lead. I made one bounded source check and stopped.
