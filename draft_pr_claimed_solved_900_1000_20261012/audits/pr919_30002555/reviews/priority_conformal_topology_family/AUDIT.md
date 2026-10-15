# Independent priority audit: conformal and topological mechanisms

Target: PR919, problem 30002555 / OWR-12875-003, immutable candidate head `704685791ec0053dc0a52590fdef49ed4aae61d9`; PROOF SHA-256 `78be2da0b8831461e0268eb230cf47273a629a81a9dc2db997234f9fb5036464`.

## Finding

The candidate's obstruction is a complete corollary of earlier work, with a robust published bound of APV 2021 and the needed lemmas already present in APV's public 4 July 2020 preprint. ARSVW explicitly states the flat-surface finite-isometry theorem in its 31 October 2023 v1. The candidate correctly credits the v2 version and explicitly disclaims mathematical priority. The overlap therefore does not invalidate the proof or contradict its present application framing.

No inspected primary text literally announces a negative answer to OWR2014 Question 4 or RMV2017 Question 0.2. That is a bounded historical search result, not evidence of firstness. It would be inaccurate both to call the obstruction a new general finiteness theorem and to assert that APV or a classical source literally solved the named Veech question. The complete prior-corollary implication and the literal historical statement are different findings.

The direct bridge is fully written in DIRECT_PRIOR_BRIDGE.md. There is no unsupported transfer of the central mathematical difficulty in that bridge.

## Independence and scope

I first read the exact full source record, charter, preflight, and pinned PROOF. INITIAL_ASSESSMENT.md records the search mechanisms. INDEPENDENT_PRIORITY_FINDINGS.md was saved before reading the original SOURCE_AUDIT and public README. No other priority-family conclusions or review verdicts were read. All primary bodies used here were freshly retrieved into this family's ignored private_sources directory; the shared private_sources was only inventoried. No author proof search, external communication, Git mutation, PR action, tracker edit, or release was performed. This is an AI-assisted independent audit, not human refereeing or a formal proof-assistant verification.

## Exact target and conventions

[OWR2014](https://ems.press/content/serial-article-files/46504), printed pp885–888, explicitly fixes the matrix group through derivatives of orientation-preserving affine maps. Question 4 on p887 quantifies over arbitrary closed Cantor subspaces and countable matrix subgroups without contracting elements, requiring infinite genus, tameness and no planar ends. Its neighboring realization theorem says the Veech group is precisely G. The proof concerns that embedded subgroup formulation. A counterexample for a three-point end space answers the universal existence assertion negatively; it does not classify the remaining pairs or settle the separate Jacob's-ladder lattice question.

[RMV2017](https://msp.org/agt/2017/17-1/agt-v17-n1-p15-s.pdf), pp530–532, states a wider question with nested genus-end and end spaces, conjectures positive realization, and records the finite n≥2 case as unresolved then. Taking both nested spaces to be the same three-point set gives the target subcase. Section 1.4, p539, distinguishes S from its metric completion and defines the full derivative image. PSV2011, p676, explicitly works with a Riemann surface including finite cone points and excluding infinite-angle completion points. The candidate's two convention treatments retain the exact S instead of silently replacing it by its completion.

These source statements were checked in full relevant contexts and on actual rendered pages. The OWR displayed summary has a contraction-sign problem; its Question 4 is unambiguous, and the chosen group preserves all Euclidean norms exactly. No interpretation of that summary can make the witness contracting.

## Approach-family ledger

| Family | Mechanism and evidence | Status | Exact gap |
|---|---|---|---|
| Classical uniformization/normalizer | Nonabelian π1 forces disk uniformization; its normalizer is discrete, and compact transporters are finite. Winkelmann p414 states properness for noncommutative π1; DHV Theorem 3.1.4 gives the exceptional-case classification and normalizer proof. | Verified older ingredient; complete with the core argument. | No inspected classical source literally names OWR/RMV or prints this Veech counterexample. |
| Finite-ended compact core | The connected three-boundary core cannot be displaced by any homeomorphism. APV Lemma 4.1 covers countable end spaces of degree≥3, including three points. | Verified, including arbitrary end permutations and arbitrary homeomorphisms. | None for the three-ended all-genus surface. |
| APV 2020/2021 | Lemmas 2.6 and 4.2 give compact-set properness and finiteness of every isometry subgroup with a nondisplaceable compact set; Theorem 4.3/6.2(3) packages it. Complete Poincaré metric and rotational-lift bridge close all hypotheses. | Complete direct prior corollary. | The named Veech-question negative answer is not a literal statement located in APV. |
| Mann–Rafi | Definition 2.3 uses mapping classes/geodesic intersection; Example 2.5 gives an invariant finite set of≥3 ends, but its displayed setup assumes an infinite end space. Journal and corrected author version agree on the relevant example. | Useful provenance for nondisplaceability; not cited verbatim for the finite-three-point case. | Applying Example 2.5 alone to finite end space would skip a written hypothesis; APV 4.1/direct core removes the gap. |
| ARSVW v1/v2 | v1 Theorem 1.6, Corollary 2.21, Section3.1, proof p15; v2 Theorem 1.8, Corollary 2.19, Section3.1, proof pp16–17. Isom is the full SO(2) derivative preimage. | Explicit earlier flat-surface finiteness theorem; candidate is a specialization plus explicit matrix. | No inspected passage literally identifies the OWR/RMV universal assertion as false. |
| Heins/classical classification search | Primary publisher-deposited metadata verifies Heins1946's plane-domain finite-connectivity subject and Heins1952's title/date. Full bodies were unavailable through attempted primary hosts. | Limited evidence; no theorem imported from uninspected bodies. | Cannot attribute a finite-ended infinite-genus theorem, or exclude any such remark, from metadata alone. |
| Unrestricted realization | Winkelmann's theorem realizes countable groups on a surface whose topology is allowed to depend on the group; PSV covers the one-ended tame regime. | Does not resolve the prescribed-three-end question positively. | Fixed topology and embedded derivative data cannot be substituted by abstract group realization. |

## Earliest verified complete overlap

[APV's arXiv history](https://arxiv.org/abs/2007.01982) dates v1 to 4 July 2020 and v2 to 9 March 2021. The v1 itself contains the compact-core lemma and the finite-isometry-subgroup lemma at pp22–23. The [journal paper](https://doi.org/10.1007/s00208-021-02164-z), published online 23 March 2021, retains them on p477, with compact-set properness on p468. Three-point end space has degree three, and the surface's infinite genus supplies nonabelian π1. Uniformization equips the same complex surface with a complete hyperbolic metric; its holomorphic automorphisms preserve that metric. APV then forces the full rotational affine preimage to be finite. This proves the qualitative obstruction directly, before the candidate and before ARSVW. The printed APV Corollary4.4 says rank rather than degree; this audit avoids that problematic locator and uses Lemmas 4.1–4.2 with their exact hypotheses.

[ARSVW's history](https://arxiv.org/abs/2311.00158) lists exactly v1 (31 October 2023) and v2 (23 February 2026) when retrieved. The v1 already states the relevant translation theorem. The candidate's v2 citation therefore describes an existing result correctly, but does not give its earliest public version. The v2 changes relevant numbering, retains the core theorem, adds some surrounding results, and preserves the SO(2)-preimage definition. Both bodies and their actual key pages were inspected, including the proof continuation onto v2 p17.

Current primary author pages describe ARSVW as [to appear](https://m-artigiani.github.io/research/papers/) or [accepted for publication](https://www.mathi.uni-heidelberg.de/~arandecker/research.php) by Algebraic & Geometric Topology. The current arXiv page still identifies v2 as latest. No final journal text was located or used; this does not certify that no final text exists elsewhere. The original packet's cautious version description remains supported.

## Classical and book contexts

[Winkelmann, p414](https://ems.press/content/serial-article-files/25888) explicitly records proper discontinuity for Riemann surfaces with noncommutative fundamental group and the holomorphic/Poincaré-isometry relationship. It also refers back to the classical classification of the exceptional automorphism groups. The PDF footer says Documenta Mathematica7(2002), while the current EMS landing page has6(2001); this bibliographic discrepancy is preserved rather than resolved by guessing. Either date is earlier than the target question. Its realization theorem itself does not prescribe the end space.

[DHV2024](https://arxiv.org/pdf/2403.05424v1), pp108–111, explicitly treats rotational affine maps as analytic maps and proves the classical normalizer classification. Its p119 still presents a broader prescribed-end matrix-group question and the Jacob's-ladder example as open. The public arXiv history currently has only v1, submitted 8 March 2024. An [author-hosted draft labelled mar2019](https://www.labri.fr/perso/vdelecro/infflatsurf/infflatsurf-chap3_symmetries-mar2019.pdf), linked by the book's primary webpage, has the same properness theorem and normalizer proof at pp69–71. The filename/webpage label is not independently authenticated as an immutable 2019 publication timestamp. This older-context evidence does not turn the named Veech negative answer into a literal published theorem.

Heins1946 concerns finite-connectivity plane regions; finite connectivity is not the same as finite ends with infinite genus. Heins1952's title is insufficient to infer an automorphism theorem. Searches also surfaced Greenberg's general automorphism realization and a 1998 algebraic-curve full-automorphism criterion; no unsupported negative answer is attributed to them. In particular, no1998 result is promoted here to a literal solution of a2014 question.

## Hypothesis audit and boundary checks

The direct bridge checks the original incomplete flat metric, the unchanged underlying topological surface, finite cone extension, exclusion of infinite-angle completion points from S, arbitrary homeomorphisms, end permutations, full derivative preimage and kernel, and actual embedded matrices. It uses no area bound, complete flat metric, finite cone count, finite generation of the automorphism group, or action of the matrix derivative group itself.

The n≥3 inequality is essential. The two remaining ends land in one complementary component if the core is displaced; with n=2 this gives only one end and no contradiction. Thus no obstruction to the known one-ended and Cantor-ended examples is introduced, and no conclusion about Jacob's ladder follows. Finite rotation groups remain allowed. An abstract infinite cyclic group with a nonorthogonal generator is not excluded by this argument. The exact all-n congruence proof supplies the infinite-order witness; bounded computations are not used for the historical conclusion.

## Framing recommendation and remaining gap

Retain the mathematical negative-answer statement as an explicitly attributed application of prior finiteness results. The pinned PROOF already does this, says no priority is claimed, and supplies the reduction; SOURCE_AUDIT and README reinforce that scope. I found no priority-based reason to reject that present framing. No new novelty threshold is imposed by this audit, and this family does not decide any broader project acceptance policy.

Optional improvements: cite the 2023 v1 theorem alongside the current v2; add APV2020/2021 as the older complete-corollary route; and state the bounded historical finding precisely. A suitable sentence is: “The counterexample is an explicit corollary of existing isometry restrictions; we have not established historical priority for stating this consequence as a negative answer to the prescribed matrix realization question.” The original wording is already compatible with this limitation.

Required if any future promotion changes the claims: do not call the general finiteness theorem new, do not claim firstness from search absence, and do not write that APV/Heins/DHV literally settled the named Veech question without a primary text saying so. Those are conditions on new claims, not corrections of a currently observed false claim.

The exact remaining gap is historical: whether some earlier primary publication explicitly drew this negative conclusion for prescribed embedded matrix groups. The inspected literal contexts do not close that gap. The logical implication from prior work is closed, so this is not a mathematical gap in the counterexample.

## Checkpoint and artifact integrity

All 27 original-file hashes matched at start; AUTHENTICATION_END.json records the final comparison. SOURCE_MANIFEST.json gives fresh-retrieval URLs, UTC times, bytes, SHA-256 values, page locators and actual visual-inspection metadata. QUERY_LOG.md records the search families and access limitations. The sealed MANIFEST.json is an explicit public allowlist, excludes itself, and excludes every raw third-party body, extraction and rendered page. The associated private directory is ignored by the local .gitignore. No public artifact here claims an exhaustive literature search or absolute firstness.
