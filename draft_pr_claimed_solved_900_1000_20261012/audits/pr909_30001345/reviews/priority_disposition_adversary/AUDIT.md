# PR909 independent adversarial disposition audit

## Outcome

**Do not promote this packet as a novel, decisive resolution of a currently open mathematical problem under the requested publication framing.** The core geometric example and deformation mechanism are prior mathematics. The strongest verified outcome is an explicit, reproducible classical corollary giving a negative answer to the unrestricted **summed rough-invariant reading** of the 2009 question.

This is a priority/framing sufficiency judgment. It is **not** a mathematical rejection, a proof that the precise invariant observation was previously printed, or a claim that de Jong–van Straten stated the rough-M theorem in 1998. A properly attributed classical-corollary or expository note is a real and reasonable repair of the document. Whether that outcome belongs in the user's `claimed_solved` acceptance/publication workflow is a goal decision for the root agent; the exact requested “original, unsolved, open math problem” framing is stronger than the verified evidence supports. I favor declining that promotion, while preserving the sound result and provenance. Do not automatically relabel the queue or make any external change from this audit.

## Independence and scope

The candidate proof, research charter and immutable PR description were read before any current priority-family conclusion. The 1998 complete primary PDF was independently downloaded from the author-hosted Mainz URL. The complete relevant definition/example pages were read. Complete printed pages 476 and 503 were visually inspected. For the 2023 primary PDF, complete printed pp.1109 and1194 were read and visually inspected, with1195 read for surrounding context. The 2009 contribution pp.2446–2448 and 2014 pp.573–578 were read; pp.2446–2447 were visually inspected to verify the barred invariant and scope. No current priority-family verdict was used to reach this conclusion, and no source-search claim is made beyond the listed inspections. The other families' supplied mathematics PASS is the premise for this disposition audit, not an independently repeated full math audit.

Only PR909/problem30001345 was considered. No original file, Git state, PR, release, Zenodo record, tracker, or other person's account was changed. No external contact was attempted. The original candidate is exact head `d186dea31791cd3e8acf6829e0b65d01849623b8`; frozen proof SHA256 `561b189c2091eaeccccf89fdd933b2300ec676a871d7229ebfaf8c806962fe8b`.

## Verified primary evidence

1. **de Jong and van Straten (1998), Duke Math. J.95(3),451–522.** Definition4.2, p.476, requires a delta-constant decorated-curve deformation and writes the simultaneous-normalization product. Definition4.6, p.480, defines picture deformations. Example6.5, pp.501–502, degenerates a nine-line configuration to concurrent lines by parallel shifts. Example6.6, pp.503–504, explicitly uses the dual flex configuration: nine lines, twelve ordinary triple intersections, and no other intersections. AppendixA.5, p.518, relates delta constancy and simultaneous normalization. The inspected passage does **not** state any rough-M comparison.
2. **Plamenevskaya and Starkston (2023), Geometry & Topology27,1083–1202.** Definition2.7, p.1109, makes the delta-constant/simultaneous-normalization setting explicit. Example8.7, p.1194, explicitly scales the constant terms of straight-line equations to zero to pass to a pencil. This predates the candidate and confirms that the scaling step is established, elementary deformation practice. Its particular example has eleven lines; the stated mechanism applies to arrangements generally. It does **not** assert the present rough-M inequality.
3. **Borodzik (2014), Osaka J. Math.51,573–583.** Definition3.3, p.576, is the rough invariant used by the candidate. Definition2.1, p.575, makes “parametric” both rational and unibranched. Conjecture3.8, p.577, assumes parametricity. Page578 uses degree scaling to an ordinary multiple-point type and explicitly uses the ordinary-d formula d−2. These facts make the new invariant computation elementary. One should not infer that arbitrary prescribed ordinary-d analytic germs are analytically equivalent to `x^d−y^d`; tangent-direction moduli matter. The actual cone construction has its own prescribed distinct directions and needs only its ordinary topological type.
4. **Borodzik (2009 report, published2010), pp.2446–2448.** The bar and displayed `K(K+D)` definition are visible on2446. Questions2–3 there do not state a unibranch condition. Page2447 explicitly compares several nearby singularities in a fixed-ball setting, supporting the summed reading; the question itself does not literally write a sum. The later one-branch and cuspidal/node statements are restricted. Thus the candidate's guarded reading is defensible; asserting that it settles every intended or later conjecture is not.

Primary URLs, file hashes and page mapping are recorded in SOURCE_MANIFEST.json. Raw PDFs, extracts and rendered pages are excluded from public artifacts.

## Checkable corollary bridge

Choose a projective line at infinity missing all twelve intersections of the classical dual Hesse arrangement. Its nine affine lines then have distinct directions. Write them as `a_i x+b_i y+c_i=0` and form

`F_t(x,y) = product_i(a_i x+b_i y+t c_i)`.

For nonzero t the curve is a homothetic copy of the arrangement. At zero it is nine distinct concurrent lines. A generic spatial coordinate makes the polynomial monic up to a nonzero constant, giving flatness. The disjoint union of the nine line-component families gives finite simultaneous normalization. In a fixed sphere transverse to the central cone, sufficiently small t keeps every scaled intersection inside and preserves transversality. Thus this classical construction gives the required local deformation without a new geometric mechanism.

For an ordinary r-fold point, a single blowup for r≥3 has `K=E`, `E²=−1`, and `E.C'=r`. Consequently rough-M=`E.(C'+2E)=r−2`; delta=`r(r−1)/2`. Therefore central delta is36 and rough-M is7; nearby totals are12×3=36 and12×1=12. This exact inequality follows directly from the established geometry and standard invariant formulas. The candidate's coefficients and radius make it especially explicit, but are not needed for existence. The classical Fermat counts similarly give the optional excess `n²−4` without a new deformation idea.

## Attempts to falsify an overly aggressive priority rejection

- **“An old ingredient makes a new theorem impossible.”** False as a general rule. A new application, observation or bridge can be a mathematical contribution even when its construction and formulas are old. There is no journal-style significance threshold in the user's instructions. The exact invariant observation might be previously unprinted.
- **“The identical theorem was proved in1998.”** Not established. The 1998 source provides the exact incidence geometry in the relevant deformation setting; no inspected page prints the rough-M statement. The inference to that statement is transparent, but historical recognition and explicit publication are separate claims.
- **“The original candidate dishonestly claims novelty.”** False. Its title and scope disclaim arrangement novelty, global novelty, and present-day literature status. The concern arises when promoting it to the user's stronger new open-problem preprint framing.
- **“The construction is mathematically invalid because the central point has many branches.”** False for its stated unrestricted multibranch theorem. It does invalidate any attempted claim about the explicitly unibranched 2014 conjecture.
- **“Closure is the only possible reasonable repair.”** False for the document considered alone. Adding the 1998 and2023 provenance, recasting it as a classical consequence, and retaining exact reproducibility produces an honest useful note. The issue is whether that note satisfies the selected research/publication goal.

These objections defeat categorical claims of plagiarism, mathematical failure, or proved prior publication of the exact theorem. They do not establish a novel/currently open target or restore a new central mechanism.

## Attempts to falsify inflated novelty or open-problem claims

- Crediting only the classical projective arrangement understates the priority evidence: the relevant deformation setting and constant-term scaling are also prior mathematics.
- Fixed-radius estimates, the convenient infinity `X+2Y+4Z`, explicit coefficients, exact enumeration and package hardening improve reproducibility and exposition. They do not demonstrate a new mathematical obstruction, construction, or proof strategy.
- The comparison7<12 and the all-n arithmetic may be newly recorded observations, but this audit has no evidence establishing firstness for those statements. They must not be sold as a newly discovered deformation result.
- Moving the claim to the later parametric conjecture is not a wording repair. Nine central branches fail its hypothesis and a new proof would be required.
- The 2009 literal broad question and the later precise restricted conjecture must remain distinct. Calling the result simply “Borodzik's conjecture solved” would erase the essential distinction.

## Reasonable repair and disposition

A safe repaired statement is: *The classical picture-deformation construction for the dual Hesse arrangement, together with the ordinary multiple-point formula, gives the explicit counterexample7<12 to summed rough-M upper semicontinuity for unrestricted reduced multibranch delta-constant deformations. This addresses the unrestricted summed reading of the2009 question; it does not address the later parametric conjecture. We make no firstness or present-openness assertion.* The current proof already contains most of these limits; it needs stronger geometric-deformation attribution.

That repair preserves a full proof of the literal broad negative statement, so it is reasonable if the user accepts classical-corollary notes as the outcome. It does not by itself substantiate a novel resolution of an actually open problem. Under the exact requested publication framing and overall novel-contribution goal, I recommend **no promotion as `claimed_solved` open-problem research**. If the root elects closure, the explanation should say that the core result is a direct corollary of established constructions and does not support the intended new-open-problem framing. It should acknowledge that the scoped theorem is correct and that no earlier source stating the exact rough-M inequality was located. It should not say the inequality was literally proved in1998.

## Exact residual uncertainty

The unresolved historical question is whether the precise rough-M negative observation, rather than its geometric construction, has appeared before. This audit cannot prove its absence or presence. It also cannot determine an unstated2009 author intention. The remaining policy question is whether an honest elementary classical corollary is an acceptable result for this user's selected workflow. Those uncertainties should remain explicit; neither a categorical historical-priority claim nor a new-open-problem claim follows from the inspected evidence.
