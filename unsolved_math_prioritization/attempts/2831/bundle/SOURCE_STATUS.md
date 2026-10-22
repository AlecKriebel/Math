# Source, literature, and repository checks

Checked 2026-10-04. This is a bounded literature check, not proof that no later or unindexed solution exists.

## Identity and source correction

- Catalogue URL: https://www.unsolvedmath.com/problems/2831 . The direct request returned HTTP 403 (Vercel denial); no access restriction was bypassed. The exact record was recovered from the already-authorized, immutable upstream corpus.
- Dataset: ulamai/UnsolvedMath, revision 37e53eabe540fb458758e198be61634bd02ee008. Numeric identity 2831, code KP-3.33, title Kirby Problem 3.33.
- problems.json: 68,931,837 bytes; SHA-256 04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf.
- research_results.json: 80,334,822 bytes; SHA-256 8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b.
- Both corpus hashes were checked locally against the live repository manifest. There is no KP-3.33 entry, and no KP-prefixed entry, in the 6,701-key research-results corpus. The selected problem's complete background/dated triage and its repository desk assessment were read separately.
- The background's https://aimath.org/pastworkshops/kirbylistrep.pdf is a four-page workshop summary, not the 2026 problem book. It does not establish Problem 3.33's exact statement. Correct primary source: Baykur–Kirby–Ruberman, K3 author version at https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf , printed/PDF p.155; statement and remarks visually checked.
- K3 still presents this general degree-one Heegaard-genus inequality as a conjecture and describes a torus-pinching partial result. Historical K2 problem numbering is different; an unrelated reference to “Kirby Problem 3.33” must not be conflated with K3 3.33.

## Literature scope and exact dependencies

- Li 2022, https://doi.org/10.1112/topo.12253 ; preprint https://arxiv.org/abs/2007.14534v2 . Introduction, Theorem 1.3, and Remark 2.2 were read. Its theorem has a specific knot-exterior/homology-sphere replacement hypothesis. It does not claim the universal result. It explicitly describes the general handlebody-pinching formulation as equivalent to the full conjecture.
- Li 2013, https://doi.org/10.1090/S0894-0347-2013-00767-5 ; https://arxiv.org/abs/1106.6302v2 . Introduction and theorem statement checked: rank below Heegaard genus occurs for closed hyperbolic manifolds; the gap can be arbitrarily large. These examples are not degree-one counterexamples.
- Boileau–Wang 2005, https://doi.org/10.2140/agt.2005.5.1433 . Theorem 1 and its smallness hypotheses were read. The rigidity statement is not a general proof of the present conjecture.
- Gadgil 2007, https://doi.org/10.1112/blms/bdm019 ; https://arxiv.org/abs/0809.3102v1 . Theorem 1.1 gives a surgery characterization. Individually unknotted components are not asserted to remain unknotted during sequential surgery. The preprint is posted in 2008; the published article is from 2007. An internal generated date in the PDF is not used as its publication date.
- Searches combined the exact conjecture/degree-one-map terminology with 2024, 2025, and 2026 and checked the primary works above. No complete general resolution was verified. “Unsolved” is this attempt's outcome, supported by the current book's formulation; it is not an exhaustive literature certificate.

## Live repository check

Repository: https://github.com/AlecKriebel/Math . Main was 25aaa7146e257ef5276e80aae60429cf3f4765f9 at the 10:28 UTC read (commit timestamp 10:11:46 UTC).

The queue row was rank 594, status queued, 0/5. state.json had no record for 2831. The exact attempts/2831 path returned 404. All-state PR searches for “2831” and “Heegaard” returned no results; indexed code search for “KirbyProblem3.33” returned none. No related-target group contained 2831. The prior individual assessment in reviews_5.json already warned that rank alone cannot prove genus monotonicity. Two recursive-tree reads failed with transport closure, so there is no claim of an exhaustive path scan. These checks found no duplicate active attempt.

Related record 2833/KP-3.35 concerns rank versus genus; its existing open subquestions are not solved by this package. No changes to it are proposed. There were no remote writes, external communications, branch changes, commits, pushes, or releases during this investigation.

## Rights and private material

The original PDFs, extracted full text, screenshots, source-corpus extracts, and tool response records remain outside this release bundle. The K3 author PDF explicitly prohibits reposting without permission; it is not redistributed. The bundle contains original derivations, brief attributed summaries, bibliographic URLs, and hashes only. No source licensing is inferred from the dataset's general CC-BY metadata.

## Primary PDF integrity identifiers

These identify privately inspected source versions; the PDFs are not in the bundle.

- k3-2026.pdf: SHA-256 ae56518166fe38aaaf555c58614329228afe734e743b111badec4060877fa12f
- li-2022.pdf: SHA-256 a46b271ca3774c5e6f4678f6ade002f2035b1630922118111aa7a804b0d318a5
- li-rank-2013.pdf: SHA-256 90768f44faff332233d4922ac104869bee4a376be63845962fb7944e03e9956e
- boileau-wang-2005.pdf: SHA-256 04f477eb28e1b10ddd66991c2282dcd4754ab41259a6af9e758481050faaf39f
- gadgil-2007.pdf: SHA-256 90a7b9a12992d40f0bddc5e48804c6e0a5d89cd84853fc08b1182100bf324dac
