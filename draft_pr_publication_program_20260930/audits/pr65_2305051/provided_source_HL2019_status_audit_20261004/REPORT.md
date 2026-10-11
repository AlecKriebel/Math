# PR65: provided Hayman-Lingham 2019 status and explicitness audit

The 2019 primary book materially supersedes the genuine no-progress report in the September 2018 draft. Its Update 5.51 credits the Aleksandrov-Anderson-Nicolau 1999 construction as explicit. The cited primary theorem supplies a pure Blaschke construction satisfying the exact Holland target after an elementary normalization. The candidate may provide a useful fully prescribed effective presentation, conditional on its analytic proof passing the other audit families. The supplied source does **not** support presenting PR65 as a first/full historical resolution of a still-open explicit-construction problem.

This is a historical status, provenance, and explicitness audit. It does not certify the candidate's singular-factor proof, all-stage recursion, numerical bounds, or global novelty. No reviewer opinion was read before the independently saved [FIRST_CONCLUSION.md](FIRST_CONCLUSION.md); none was needed afterwards. Parent messages confirming independently read pages arrived only after that record was saved.

## Frozen target and artifacts

- PR65 is reported by ROOT as an open, immutable draft at head `5cc1602c05d79502defb07cec7027963149494d2`; submitted/current literal status is `claimed_solved`; original proof turns are 2/5. This family did not independently query or mutate GitHub and did not introduce a proof turn.
- Literal candidate: `publication_package_v1/verification/author/CANDIDATE.md`, SHA-256 `0a15d03ab92cbd13f17042a4708f75c3d592f4884810c7ffadc6a5f34f1cb6c4`, independently verified. Its answer is a cyclic four-adic recursion, explicitly given rational-inner stages, a compact convergence modulus, and a claimed pure Blaschke limit.
- Exposition inspected: `publication_package_v1/note.tex`, SHA-256 `7b5b13db61725d8e27293d35402d8719f97ab2db2c5380f0c65cb14d37964b56`. Its historical assertions were treated as claims to test.
- Provided 2019 book: SHA-256 `1388a8c153a3eb16156d90542d1f00e4a6203b594566540c71c5f354238e14dc`, 288 PDF pages. Full primary bodies, text and rendered pages are kept only under the private path recorded in `MANIFEST.json`.

## Page-pinned version change

| Source | Exact locator | What it establishes |
|---|---|---|
| Hayman-Lingham, arXiv:1809.07200v2, 21 September 2018 | Printed p.105 / PDF p.106 | Existence is already known. Holland asks for an explicit construction. Update 5.51 says no progress had been reported to the compilers. |
| Hayman-Lingham, Springer 2019 | Printed p.121 / PDF p.127 | Same target: a Blaschke product in the disk, B(0)=0, whose (1+B)/(1-B) is Bloch. The update introduces the 1999 AAN result [21]. |
| Same 2019 update, continued | Printed p.122 / PDF p.128 | It gives a small-derivative inner-function conclusion and adds: “Moreover, I is constructed explicitly.” It relates this to singular symmetric measures with a Zygmund condition. |
| 2019 bibliography | Printed p.246 / PDF p.250, reference [21] | Identifies AAN, *Inner functions, Bloch spaces and symmetric measures*, Proc. Lond. Math. Soc. (3) 79(2), 318-352 (1999). |

The exact 2018 version and its date were checked against [official arXiv metadata](https://arxiv.org/abs/1809.07200v2), the retained PDF title page, and a fresh official download matching the retained bytes. Its no-progress report is authentic; attributing it to the 2019 edition would be false. In 2019 that wording instead appears in neighboring Update 5.52, and it must not be transferred to 5.51.

The 2019 book does not explicitly label 5.51 “open,” “unsolved,” or “solved.” The proper positive statement is that the 2019 update credits an explicit AAN construction as relevant progress. It is not a formal status registry, and retaining the original problem statement is not evidence that no construction exists. The newer wording, together with the primary theorem below, defeats use of the 2018 no-progress sentence as present evidence for a new full historical resolution.

The imprint (PDF p.5) confirms Springer 2019, eBook ISBN 978-3-030-25165-9, [book DOI](https://doi.org/10.1007/978-3-030-25165-9), and first edition 1967. The preface ends April 2019 (PDF p.7), warns that original statements and subsequent additions remain valuable, and points to the reference tables. Neither that date nor PDF production dates certify the worldwide state of research in October 2026.

## Exact-target deduction from the cited primary theorem

AAN Theorem 2 (printed p.320 / PDF p.3), proof pp.326-327 / PDF pp.9-10, constructs an interpolating pure Blaschke covering for any admissible positive continuous gauge. The omitted countable set excludes zero. With the quadratic gauge ct^2, the covering reaches zero. Precomposition by a disk automorphism at one preimage makes B(0)=0 while preserving the derivative inequality. The Cayley derivative then obeys a Bloch bound of 8c. AAN pp.328-329 / PDF pp.11-12 already discuss the corresponding rotated Cayley functions and the same bound. [Primary author-hosted paper](https://mat.uab.cat/~artur/data/innerfunctions,blochspacesand.pdf).

The independent, checkable calculation and normalization/purity details are in [EXACT_TARGET_NORMALIZATION.md](EXACT_TARGET_NORMALIZATION.md). They distinguish the supplied book's inner-function formulation from the exact pure-Blaschke requirement. No generic Frostman shift, unidentified good parameter, or unproved assertion that every inner function is Blaschke is needed for this historical deduction. The primary paper does not name Holland here; the link to the normalized target is explicitly our deduction, while the general Cayley application is printed there.

## What “explicit” does and does not mean here

Neither the inspected 2019 problem/update nor the complete relevant chapter defines “explicit” as a closed-form zero list, as a finite-algebraic recursion, or as computability with a specified compact convergence modulus. The update's affirmative use of the word applies to a construction whose cited primary proof uses a covering domain. The historical source therefore does not justify excluding covering constructions from explicitness by definition.

The candidate states its own stronger operational specification plainly: fixed recursion and choices, rational inner stages with algebraic coefficients, and a known compact error bound. It admits that it supplies no short closed-form enumeration of the zeros. This is a reasonable declared meaning of an effective construction. It is not silently weaker in its mathematical output if purity and the Bloch proof are valid; the output is the exact requested type of function. But choosing that operational definition does not prove that it is the intended exclusive historical definition or that no earlier construction met it.

Conversely, an objection demanding a closed-form zero sequence would add a requirement absent from the source. Both the permissive and the restrictive interpretations must be labeled as interpretations. A contribution framed as a fully specified effective realization can be assessed on its actual mathematical and computational properties. A first/full historical resolution claim requires additional positive primary evidence, especially once the 2019 update expressly credits an earlier construction as explicit. Search absence cannot supply that evidence.

## Whole-chapter context and citation chain

The complete “Functions in the Unit Disc” chapter was read: printed pp.97-131 / PDF pp.103-137, including its preface, definitions, all previous problems/updates and new problems. Its Bloch definition is at printed p.111 / PDF p.117 (Problem 5.30). The later Holland problems 5.68 and 5.69, printed p.127 / PDF p.133, concern positive-real-part Bloch functions and Zygmund measures. They do not redefine 5.51 or its explicitness requirement.

The table chain was read in full: Table A.1, printed p.241 / PDF p.245, identifies source C as the 1977 *Research problems in complex analysis* collection; Table A.2, printed p.242 / PDF p.246, assigns Chapter 5 problems 38-58 to C. Thus the book maps 5.51 to that 1977 collection, not to the original 1967 list. The original 1977 article body was not fully inspected by this family, so this is a table-supported provenance statement, not a claim about the exact date when Holland first orally posed it. Table A.3, printed pp.242-244 / PDF pp.246-248, lists older progress document codes and lacks a row for 51; it does not erase the affirmative 2019 narrative update or imply current openness.

Update 5.51 cites only AAN [21]. It does not directly discuss Piranian's 1966 construction, Duren-Shapiro-Shields 1966, or Kahane 1969, and does not adjudicate whether an elementary application of those earlier constructions would already meet Holland's target. The 2019 bibliography contains Duren-Shapiro-Shields [277] at printed p.255 / PDF p.259, but associates it with Problem 6.15; that problem/update (printed pp.141-142 / PDF pp.146-147, inspected with page context) concerns univalence of integrals of powers of derivatives and pre-Schwarzian bounds. It is not a 5.51 historical-resolution attribution. Duren [271], at the same bibliography page, is the **1965** Riesz-product smoothness paper attached to Problem 5.69, not the supplied 1966 paper. Holland-Twomey [552], printed p.266 / PDF p.270, is also attached to 5.69.

The indirect AAN chain does matter: printed p.324 / PDF p.7 attributes earlier positive singular small-Zygmund measures to Piranian [17] and Kahane [13], identified at printed p.352 / PDF p.35 as the 1966 and 1969 papers. That is evidence of classical antecedents; it does not establish that those exact bodies already printed the entire normalized Holland application. AAN also notes at printed p.325 / PDF p.8 that Wayne Smith had independently obtained their Theorems 6 and 3; the cited Smith 1998 body was not separately read in this family. Neither chain licenses a first-ever singular-Zygmund-measure claim. The independent mechanism and analytic families must adjudicate the supplied 1966 bodies and any final application; this report does not substitute source-name matching for that work.

## Bounded later-primary search

The later-literature check used web queries for the exact problem/phrase, followed the author's current UAB publication links, froze full bodies privately, and inspected relevant introductions/citations. It was deliberately bounded; none of the following is a complete-body reading claim:

| Primary body retrieved | Inspected pages | Relevant result of this check |
|---|---|---|
| Nicolau, *Contractive analytic self-mappings of the disc*, author-site preprint listed 2026 | PDF/printed pp.1-4 and 26 | Uses Clark measures and explicitly recalls the AAN symmetric-measure correspondence. It supplies no historical definition of Holland's explicitness. [Primary body](https://mat.uab.cat/~artur/data/perlaweb.pdf). |
| Ivrii-Nicolau, *Analytic mappings of the unit disk with bounded compression*, arXiv:2507.15200v1, 21 July 2025 | PDF/printed pp.1-4 and 27 | Studies a different quantitative self-map class and cites AAN. [Exact author-hosted v1 body](https://mat.uab.cat/~artur/data/2507.15200v1.pdf). |
| Bampouras-Nicolau, *Inner functions, Möbius distortion and angular derivatives*, author manuscript dated 12 March 2025; author's list identifies a 2026 journal publication | PDF/printed pp.1-3 and 14 | Concerns entropy and angular derivatives; manuscript version is distinguished from the journal publication. [Exact author body](https://mat.uab.cat/~artur/data/versiowebmeva.pdf.pdf). |

Text searches across those frozen bodies were used for navigation. They are not proof that later solutions or effective algorithms do not exist. The historical disposition rests on positive 2019/1999 primary evidence, not failed search hits or publication-list completeness. These checks establish no worldwide priority for the candidate's exact final articulation or compact error modulus.

## Necessary global-package corrections and disposition

1. At `note.tex:39-52`, preserve the genuine 2018v2 no-progress statement only with its exact version/date and immediately explain its replacement in 2019. The current generic “dated no-progress” framing omits the material newer attribution.
2. Correct the now-stale read-scope assertions at `note.tex:99-103` and bibliography `note.tex:586-589`: the supplied 2019 relevant chapter/update has now been fully inspected. Do not claim the entire 288-page book was read. Integrate the other families' actual 1966 reading scope separately; this family has not read those full bodies.
3. Add the 2019 page-pinned update and exact normalization calculation to the historical discussion. The existing AAN paragraph is materially supported and should not be weakened to a bare existence citation.
4. Keep the candidate's effective finite-algebraic specification clearly distinct from the source's undefined word explicit. If asserted as novel, formulate that exact stronger contribution and supply positive prior-art comparison; do not retroactively narrow the historic request to obtain a new full-solution claim.
5. Preserve immutable submitted/current `claimed_solved` as historical metadata, while recording the current audit disposition separately. This family's strongest clearance is **retention as a classical-method effective construction/expository connection, conditional on the other mathematical audits**. It gives no publication/priority clearance for a novel full resolution, no release approval, and no basis to use the PR50 exception or add a proof turn.

The remaining research gaps are precise: correctness of the submitted construction (other audit families), exact comparison with the supplied 1966 and 1969 mechanisms, whether an earlier publication contains this precise effective realization or compact modulus, and any stronger intended original explicitness criterion. Those gaps do not prevent the adverse status finding about the 2019 source. Original documentary evidence of the poser/compiler's intended criterion could help historical interpretation; no outreach was prepared or initiated.

## Reproducibility and reading limits

Actual execution receipts record child PIDs, argv, cwd, UTC start/end, exit codes, source hashes and hashes of separate private stdout/stderr streams. The first attempted source scan failed because system Python lacked pypdf, followed by a recorder error on a mistaken note path. Its child PID was not preserved and is not invented. All relied-on work was rerun successfully with complete receipts; Poppler performed rendering/extraction. Renders of 2019 PDF pp.127-128 and p.5, 2018v2 PDF p.106, and AAN PDF pp.9-12 were directly viewed.

The complete read scope is 2019 Chapter 5; imprint/preface/contents; all appendix tables; listed bibliography pages; Problem 6.15 and immediate context; AAN PDF pp.1-5, 7-12, 16, 26, 33-35; the 2018 exact target page and context; and the bounded later-primary pages above. The complete 288-page book, complete AAN 35-page body, full 1966 bodies, complete later papers, and complete worldwide literature were **not** read by this family. `MANIFEST.json` records a stable hash inventory without embedding copyrighted full bodies or private renders in the repository. All changes remain within the assigned audit folder and its unique external private cache. No Git/index, PR, native-editor, release, or publication mutation was made.
