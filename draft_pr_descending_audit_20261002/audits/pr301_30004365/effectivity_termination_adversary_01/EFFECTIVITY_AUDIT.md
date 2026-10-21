# PR301 effectivity and termination adversarial audit

Original immutable head: `125d90fa3f5a4f90b813fec7a7c0f1918914d885`. Problem30004365 / OWR-17466-004. Family: computability, exact PL certificate predicates, witness completeness, exceptional winding cases. This audit does not determine priority or replace the parent's other source/convention audits.

## Verdict and exact scope

**No mandatory mathematical blocker identified for the intended algorithm on nonzero finite-dimensional gentle bound quivers, with "segment inside a cut-open polygon" interpreted as a maximal portion between successive dual-dissection crossings.** The finite search can be made explicit using rational arithmetic and finite sector/ribbon incidence data; its halting proof does not assume an effective surface classifier or an implemented geometric-basis extractor. Ordinary surface classification supplies only existence, while the candidate independently specifies an exhaustive search and decidable acceptance.

The full derivation is in `INDEPENDENT_DERIVATION.md`. It was written before opening historical review/code. `INDEPENDENT_OBLIGATIONS.md` records the initial independent obligations. The historical review was read only after that derivation; its conclusions are consistent with the main effectivity route, but two passages need care as listed below.

The exact strongest result checked is a universal theoretical totality argument from a finite rational triangulated marked surface with the credited PPP dual dissection to an encoded handle certificate and APS signed winding values. The original quiver-to-surface convention and final classification key still need the independent agents' source checks. There is no full implementation, practical runtime claim, or computational test of universal halting in this packet. Those are not requirements of the original literal Problem3.4.

## Mandatory versus optional findings

| Finding | Priority within this family | Evidence and implication |
| --- | --- | --- |
| Undefined literal "segment" object | Editorial correction strongly recommended; mathematical blocker only under the literal elementary-PL-edge reading | TURN_1 §3 final bullet says every "segment" inside a D polygon separates that disk. A short elementary PL edge with interior endpoints does not separate a disk. The intended object is each maximal curve portion between successive D crossings, matching §4 and APS Lemma3.18. The exact control records an interior-endpoint rational edge; the independent proof establishes every maximal portion is a crosscut. Replace the sentence to remove the ambiguity. |
| Canonical seam coordinates | Optional precision | Locally opposite endpoint orders use t and 1-t; "identical rational edge parameters" is valid only in a shared canonical endpoint order. This is computably selectable and creates no gap. |
| Empty input | Optional scope clarification; source audit should decide standard convention | TURN_1 explicitly permits rejection of empty input but calls it outside a nonzero source class. The original Problem3.4 does not expressly discuss the zero algebra. Returning a separate zero-algebra key is an immediate total extension if needed. No nonzero input has an unhandled no-crossing peripheral case. |
| Historical verifier wording | Optional evidence correction, material if used to claim implemented verification | Historical INDEPENDENT_REVIEW §2 says "the submitted verifier does more" when discussing torus neighborhoods and planar complement. `verify_turn1.py` and `review/verify_independent.py` do not implement the full handle-certificate predicate, complement checker or enumerator. Their own docstrings and scopes are honest finite-control limitations. Read that review sentence as the mathematical acceptance specification, or rewrite it. |

There is no proven counterexample to halting or to the signed winding computation for an accepted intended certificate. The no-crossing, irrational-seam and incompatible-genericity attacks were resolved with explicit mechanisms rather than dismissed by assumption.

## Decidability and noncircular totality

An encoding has finitely many triangle labels and rational endpoints. Heights bound denominators/numerators and the total number of segments, making each stage finite. Use a shared rational edge parameter for paired seam points. Exact determinants decide intersection/overlap/collinearity, and finite sector orders decide local branch alternation. Cutting and regular neighborhoods use vertex/edge side copies and a ribbon rotation system; their component and boundary counts are finite graph traversals, and genus is `(2-h-chi)/2` on an inherited oriented 2-manifold. There is no general manifold recognition or homeomorphism test.

Surface classification supplies disjoint embedded handles with a connected planar complement. A sufficiently small simultaneous perturbation arranges all finite general-position conditions. Rational approximation is performed jointly on paired seams and within open separation/transversality margins; it preserves ambient isotopy, pair crossings and complementary topology. Every handle is nonseparating and therefore meets the dual dissection. Since finite-dimensionality excludes white punctures, each dual-complement region is a disk. Each maximal cut portion is a proper embedded interval with distinct occurrence endpoints and is consequently a disk crosscut. A one-crossing loop may have one physical crossing point but still has two distinct cut-side occurrences. This supplies a witness satisfying every intended acceptance predicate; its finite rational encoding occurs at some finite height.

Orthogonal smoothing at dual crossings is an embedded isotopy in pairwise disjoint small disks. Smoothing the remaining PL corners similarly preserves regular homotopy and side data. APS Lemma3.18 then applies. Locating the unique white mark in the left or right cut region gives the exact signed contribution, without angle arithmetic or analytic line-field computation.

The alternate route "assume an unspecified effective surface classifier and obtain a standard drawing" is **BLOCKED**: it merely transfers the extraction task to a missing algorithm. The candidate's finite-predicate search does not use that route.

## Exact edge controls

`exact_edge_controls.py` is independent of all submitted/historical verification functions. It passed239 assertions, with full source/request/start PID/UTC times/full stdout/full stderr archived under `executions/004_exact_edge_controls`. Tool-display truncation did not truncate those archives.

The230 rational seam checks exercise reversed local endpoint orders through denominator20. The remaining controls include:

- Isolated field disk: two dual crossings, winding+2 with the retained surface to the right; reversed collar gives-2. This agrees with APS Proposition3.20(5).
- Dual-numbers annulus: one crossing on each peripheral, original-boundary winding+1 and black-puncture winding-1, total0. The two ends of the cut portion are different occurrence copies of the same physical seam point.
- One vertex with two loop bands: alternating dart order gives chi=-1, one boundary and genus1; nonalternating order gives three boundaries and genus0. Across all24 cyclic order encodings there are8 torus and16 planar results. This falsifies any proposed checker that ignores sector order, while the submission explicitly preserves it.
- A rational elementary PL edge with both endpoints inside a polygon is not a proper crosscut. This supports the wording correction; it does not falsify the intended maximal-portion predicate.

These are targeted finite sanity/counterexample controls, not universal computational verification. The universal argument remains the mathematical derivation above.

## Primary evidence read

Complete PDFs and extracted text are in `primary_sources`, with actual acquisition metadata. Relevant complete sections were read, not abstracts or search snippets:

- Plamondon contribution, OWR3/2020 printed pp161-164, particularly Problem3.4 and Theorem3.3 on p163: the request is an algorithm for the stated data from the quiver with relations. Neither runtime bound nor production implementation nor ban on a geometric intermediate is stated. https://ems.press/content/serial-article-files/46842
- Final APS2023, DOI10.1007/s00029-022-00822-x: Proposition3.11 proof, Lemma3.16, Lemma3.18, Proposition3.20, Theorem4.3, Theorem7.4/Lemma7.5 and Remark7.6. Remark7.6 states the paper's methods lack a basis-walk algorithm; that is not an impossibility theorem. https://link.springer.com/content/pdf/10.1007/s00029-022-00822-x.pdf
- PPP arXiv1807.04730v2, Definitions2.2,4.6,4.8, Proposition4.9, Theorem4.10 and Remark4.11: finite blossoming/lozenge gluing, dual dissections, path-cycle punctures and genus. https://arxiv.org/pdf/1807.04730v2

OWR p163, APS p12, and PPP pp10-11 were visually inspected after local Poppler rendering. The PDF formula and gluing signs agree with the relevant text extraction. First rendering attempt failed because `fitz` is unavailable; its failure and traceback are retained. Subsequent Poppler rendering succeeded. No dependency was installed.

## Remaining gaps and exclusions

No unresolved central computability/termination gap was found in the intended nonzero/maximal-portion algorithm. Required parent work remains: reproduce and independently judge the derivation, resolve the exact input convention, complete the distinct construction/classification/priority audits, and decide whether to make the editorial clarifications. A full implemented generator/certificate checker and practical performance assessment remain absent, explicitly unclaimed and outside this literal audit verdict. Finite control counts must not be substituted for the existence/decidability proof.

All writes are inside this audit's dedicated directory. Original files were read only; no Git/index/main/shared control, services, external communication, publication, or issue/PR comments occurred.
