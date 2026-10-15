# Independent review of the current conditional research package

Reviewer: internal AI agent `package_review_one`. Reviewed on 2026-10-06 PDT / 2026-10-07 UTC, with final scope recorded at approximately 05:36 UTC. No external individual was contacted; no upstream source, manuscript, Git index, branch, commit, deposit or spreadsheet was changed by this reviewer.

## Verdict

**The conditional geometric transfer and conditional height consequence are mathematically sound in the reviewed version. No fatal mathematical defect in those statements or their proofs was found. The requested unconditional core theorem and production publication are not cleared.** The arithmetic antecedent is explicitly unverified, and the present package correctly says so. Unfinished upstream verification is an audit limitation, not a demonstrated false theorem or source gap.

This is a review of the current research snapshot, not acceptance of a completed unconditional publication candidate. It must not be represented as human peer review, certification of family 004, or permission to promote a future changed theorem. A future unconditional candidate requires complete-package review of that exact candidate, including its resolved arithmetic dependency and publication metadata.

The strongest independently checked result is:

> A terminating decision procedure on homogeneous-equation presentations promised smooth, projective and geometrically integral over Q would decide arbitrary-variable rational polynomial solvability. A computable height bound for one point whenever a presented variety has a point would also decide existence. Thus both undecidability conclusions follow **if** H10(Q) is undecidable.

Completion estimates for this assigned snapshot review: 100% of the conditional manuscript and described current-package scope. Neither mathematical resolution of the original unconditional target nor publication completion is certified by that percentage.

## Exact scope and versions

Read the complete original request at `/Users/alec/.codex/attachments/9614cd41-241b-4c1b-98b1-3bca99c14835/Pasted text.txt` and repository `AGENTS.md`. Read `manuscript/main.tex`, the four-page PDF text, README, theorem/dependency/approach ledgers, research log and publication status. Read the current reports on geometric transfer, priority, upstream logic, upstream arithmetic, height descent, the initial pointwise dependency audit and adversary, and the newly saved ring-limit and cyclotomic audits. Inspecting these reports checks their scope and consistency; it is not an independent reconstruction of every upstream arithmetic proof they discuss.

Read and executed the arithmetic and parity check scripts; read the checkpoint helper and source/build/push receipts. Independently accessed Poonen's author PDF, published JEMS PDF, publication page and arXiv record, and the Stacks Project global-functions criterion. No new formalization was identified or built by this reviewer, and no source-clone build was performed here.

`package_review_one_scope.json` records SHA-256 values of the exact current files included in the final scope. Principal reviewed hashes:

| File | SHA-256 |
|---|---|
| `manuscript/main.tex` | `21fd3057f06123c6131cbe6cbafc84f8632354be7e08cb6458338f8c98cfd9a7` |
| `manuscript/main.pdf` | `85822131118c19973a93cff59c3ea30478213e64c1e2bb50ebedccab239c8f30` |
| `PUBLICATION_STATUS.json` | `bdcf59f49570f87093daa8b01559ae617b094cdca4a9d94e3ae0bf8a85a3414c` |
| `sources/PINNED_INPUT.json` | `5a321cf94a8e746f97bde59e9b2b7f1907cdbcc7f80fedba3b040ed48fc1a299` |

The pinned arithmetic source is commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. Its identity is a reproducibility convention, not mathematical validation.

The package changed during this review. Initial reads found stale pending labels for the already reconstructed transfer and height proof; the lead subsequently corrected them, and I reread the corrected files. At the 05:31:44 hash measurement, `agent_notes/priority.md` had hash `c11af80a7e8686fab482d72e8c13ecd563a35ca012baac6fb1a7819fd6548c2d` and `RESEARCH_LOG.md` had hash `b11b9f4a3411f13972d26b712b30bb065f0717db11552a071b25f2d9a831bdb9`. I then reread their added chronology clarification and checkpoint 03. The final inventory distinguishes those changes. I do not assign an invented hash to the superseded ledger bytes read earlier.

## Independent reconstruction of the algorithm and promise

Primary geometric source: Bjorn Poonen, *Existence of rational points on smooth projective varieties*, JEMS 11 (2009), 529–543, [published article](https://ems.press/journals/jems/articles/1924), [author PDF](https://math.mit.edu/~poonen/papers/chatelet.pdf), [published PDF](https://ems.press/content/serial-article-files/31670?nt=1), DOI 10.4171/JEMS/159. I inspected Theorems 1.1 and 1.3, Remark 1.2, §§7–10, including the effective parameter-union step, rather than relying on the abstract.

The cited construction first excludes boundary points using a Châtelet family. For arbitrary inputs it separates the singular stratum, reduces smooth opens to affine patches, takes the relevant fiber products, and resolves while retaining the smooth rational fibers. Its initially ineffective parameter choice is replaced by finitely many distinct permissible square classes exceeding an effective bound on exceptional classes. Every output excludes the boundary, and at least one supplies every required lift. The finite disjoint union therefore has the stated rational-point image. This is inherited machinery, not the present author's new construction.

Here is my check of the contradiction algorithm in the manuscript. Form the reduced affine zero scheme of an input integer polynomial, its projective closure and the remembered affine open. Use the effective geometric theorem to obtain Y. Compute all connected components, reject the components that are not geometrically integral, present the rest by homogeneous equations, and take the OR of their decision answers. The list is produced before receiving answers. It is finite, and every submitted input satisfies the promise. Empty lists, empty schemes, constant polynomials and zero variables are handled consistently. Taking a reduction does not change rational points.

The rejection criterion is independently justified. A connected regular Noetherian scheme is integral because its distinct irreducible components are disjoint. For a connected smooth proper Q-scheme C, its finite global-functions algebra is consequently a field L. A Q-point gives a Q-algebra map L to Q, hence L=Q. After algebraic closure, smoothness gives disjoint integral components, and base change of H0 counts their number. Thus L=Q means one geometric component. Conversely a component with a nontrivial global-functions field has no Q-point. This agrees with [Stacks Project, Lemma 33.10.7](https://stacks.math.columbia.edu/tag/038L). Smoothness over Q also gives geometric reducedness. The perfect-field regular/smooth identification is valid here.

Effective coherent cohomology gives H0 together with its finite algebra operations; field factorization and idempotents give components. The manuscript also cites the effective algorithm's own component and geometric-integrality tests, so no decision oracle is being used to recognize its own promise. Homogeneous-equation presentations preserve projectivity and the rational points of these components.

The reverse implication is valid: every rational projective point lies in a standard chart, and on each chart the sum of the squares of the defining equations vanishes exactly when all equations vanish. This uses the ordering of Q. It still works with no equations, zero equations, constants, redundant equations and ambient projective dimension zero.

The proved forward reduction is a finite nonadaptive disjunctive oracle reduction. The manuscript neither asserts a single promised output nor derives many-one completeness, a Turing degree, a complexity bound or dimension preservation. A disconnected output from the effective theorem is correctly allowed before filtering.

## Height, syntax and boundary attacks

The self-delimiting integer code, finite equation and monomial counts, signed nonzero coefficients and exponent vectors give a computable finite presentation size. The primitive integer-coordinate convention makes the chosen height invariant under rational projective rescaling while retaining the specified embedding. Every bounded-height candidate can be enumerated in a finite integer box and tested exactly. A total computable bound on the height of one point when points exist therefore supplies a terminating decision procedure on all valid presentations. Its behavior on invalid presentations is immaterial. A presentation-dependent bound terminating on every valid input has the same consequence. The zero bound gives an empty candidate list, as required by positive point heights.

No stronger conclusion about all points, finite point sets, fixed dimensions, curves, surfaces, Fano varieties, general type or fixed quantitative complexity is present. There is no certificate theorem in the manuscript; the optional report's decidable verification predicate and soundness/completeness quantifiers are appropriately explicit if such a theorem is later used.

The compactification counterexample is correct: the affine equation x²+1 has no Q-solution, but its projective closure has the displayed boundary point. The normalization of x²+y²=0 is A1 over Q(i), so it loses the rational singular origin. A rational point cannot map by a Q-morphism to a target without one. The manuscript correctly distinguishes losing singular points from retaining boundary points; it does not falsely claim that a resolution morphism can create points from a pointless target.

## Arithmetic scope and priority

The manuscript's arithmetic paragraph accurately keeps the selected-twist Selmer calculation separate from finiteness of the 2-primary Tate–Shafarevich group. The equation r+dim Sha[2]=1 is not by itself a proof that r=1. Finite 2-primary Sha plus its perfect alternating Cassels–Tate pairing supplies the needed even dimension. The reports preserve the exact remaining rank-zero/divisible-Sha alternative. Their favorable local checks, repaired coefficient-5 height route and uncompleted companion reconstructions do not certify the unconditional antecedent.

The newly saved ring-limit report is explicitly scoped to the finite contractions, evaluations, derivative switches and associated outer rank argument. The cyclotomic report is explicitly conditional on residual/perfection interfaces and records its inverse-Frobenius convention repair. Neither is an end-to-end verdict on the complete pointwise theorem. The current status file and manuscript remain appropriately conditional despite these new positive checks. Absence of family 004's applicable Lean declarations is correctly a verification limit, not an argument that its theorem is false.

Attribution is appropriate: the geometric machinery belongs to Poonen, with Robinson credited through Poonen; family 004 is attributed to OpenAI using its manuscript identity and pin. The claimed geometric consequence and the elementary height argument introduce no independently established new arithmetic breakthrough. The negative corpus search is expressly not a novelty proof. Nothing in this review independently clears public priority for an unconditional note.

One chronology discrepancy was found and repaired in the notes. The [EMS landing page](https://ems.press/journals/jems/articles/1924) lists submission on **18 December 2007**; the [published PDF](https://ems.press/content/serial-article-files/31670?nt=1), first page, states receipt on **20 March 2007** and revision on **22 August 2008**. Both are preserved without reconciliation. The [arXiv record](https://arxiv.org/abs/0712.1782) gives v1 on **11 December 2007 at 17:50:46 UTC**. That is a verified public-record timestamp; the received date alone is not evidence of public disclosure. No earliest-public-disclosure date for Robinson's older route was independently established here.

## Computation, build and PDF checks

- `python3 reproducibility/arithmetic_checks.py` reproduced the expected JSON exactly: 26 selected primes, the listed four nontrivial common-order examples, the exact quadratic-field point and `all_checks_passed=true`. The script uses exact integer arithmetic. This supports finite identities only.
- `python3 agent_notes/parity_matrix_check.py` passed all 1,960 generated reciprocity-consistent cases with seed 4003 and exhausted all permitted q0–J toggles within each case. This supports the matrix interface only; it does not certify the arithmetic realization or a global theorem.
- A clean temporary directory inside this project contained only the unchanged standalone `main.tex`. Tectonic compiled it successfully without warnings. Its extracted text exactly matches the current four-page `main.pdf`. The build record is `package_review_one_build.json`; different PDF hashes can arise from document metadata, so this is not a claim of deterministic binary reproduction.
- All four latest rendered pages were visually inspected. Formulas, fonts, references, page numbers and paragraph boundaries are legible, with no observed clipping, overlap or missing glyphs. The PDF metadata names the conditional title and Alec Kriebel, consistently with the source. The author ORCID and AI/no-human-refereeing disclosure are present.

The checkpoint helper preserves the shared real index and HEAD by constructing an isolated index and pushing a fast-forward commit hash. It is not a proof-validation tool. For a future exact publication checkpoint, verify committed blobs against the reviewed payload hashes: its current hash receipt is computed before staging, so a concurrent modification of an owned file could make that receipt differ from the actual staged blob. This is a concrete reproducibility hardening suggestion, not evidence that any existing checkpoint lost work.

## Findings, repairs and remaining gates

1. **Blocking unresolved requirement, not a proved false step:** the unconditional H10(Q) input has not yet been fully validated. The present conditional note cannot discharge the user's core target. Keep the publication gate closed unless the pivotal arithmetic proof and its simultaneous interfaces are actually justified or replaced by a verified repair.
2. **Publication package incomplete by design:** no final deposit manifest, exact licensed payload set, finalized build/reproduction README, remote metadata/file inspection, public DOI receipt or tracker readback exists. These omissions are correctly reported as pending while there is no unconditional candidate. This review does not waive them.
3. **Resolved consistency issue:** stale transfer/height pending labels were corrected in the ledgers during this pass. The chronology conflict was also added to priority notes. The revised notes were reread.
4. **Minor manuscript clarity repair:** lines 65–67 say “number-field variety” but then use U(Q). Explicitly specialize the cited theorem to varieties over Q, or state the general k version before specialization. The proof only uses Q, so this is not a defect in its actual reduction.
5. **Minor manuscript scope repair:** lines 208–212 should say that l is one of the parameters selected by family 004's descent construction. The Selmer-dimension statement is about those prescribed parameters, not every curve of the displayed twist form. The current phrase “the construction gives” points in the correct direction but leaves the parameter restriction implicit.

The current conditional package is a useful verified partial artifact and candid dependency audit. No unconditional theorem, novel-method claim, production publication or completed persistent goal is warranted by this review. Revisit the full exact package after the mathematical and publication gaps are resolved; changes to the headline theorem or its dependency status are material and require a fresh complete review.

## Bounded follow-up on the two manuscript clarifications

At 05:37 UTC the lead had repaired both minor manuscript issues. I checked the changed passages: Theorem 1.3 is explicitly specialized to Q, and the Selmer-dimension assertion explicitly restricts l to family 004's selected descent parameters. The conditional theorem and unresolved arithmetic status remain unchanged.

Revised source SHA-256: `198d8ce14eb4ebf5f7445e531df26f7e669846fa2c4490085af5e0c775aa30f0`. Revised actual PDF SHA-256: `9601c1bf20ced764c2d6c115ec8005f1efb85823f7aa4710f1b61e27f6b3dd25`. An independent clean temporary Tectonic build again succeeded without warnings and exactly matched the current PDF text; see `package_review_one_revised_build.json`. I rendered the two changed PDF pages directly from that revised PDF and inspected them. They remain clean. The existing manuscript preview PNGs initially still showed the earlier wording, so this follow-up used reviewer-generated fresh renders rather than relying on those stale images. Temporary reviewer images were removed after inspection.

Findings 4 and 5 are therefore resolved in this revised version. No known mathematical or presentation issue remains in the conditional manuscript on this review's evidence. The blocking unconditional arithmetic and publication-package requirements remain. This bounded follow-up is not a new independent complete-package reviewer and does not substitute for the required fresh review of an eventual unconditional candidate.
