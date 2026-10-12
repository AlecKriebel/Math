# Additional qubit manuscript metadata review — record 21699069

Checkpoint: 2026-10-10 21:21:13 UTC / 14:21:13 America/Los_Angeles. Exact-source reading and initial metadata proposal: 100% complete. Independent cross-review is assigned to another agent; publication: 0% by this reviewer. No draft discard, draft edit, metadata write, publication, file mutation, external communication to an individual, or Git commit was performed by this reviewer.

## Authoritative source and checksum provenance

I retrieved the **published native record**, using a read-only GET of `https://zenodo.org/api/records/21699069` with the native media type. The snapshot is `papers/21699069/native_public_record.json`. It identifies an already published preprint with DOI **10.5281/zenodo.21699069**, title **Minimum Bell-Setting Complexity for Qubit POVM–PVM Separation**, one PDF, and the original date 2026-07-30. The incomplete account edit's empty legacy file listing is not the source for this review.

The sole public file is `kriebel-2026-minimum-bell-setting-complexity-review-v1.1.0.pdf`, size **251,541 bytes**, MD5 **a5a7a0d08c99e864159de09a7866f6ab**. Both the archived release file in `qubit_povm_pvm_minimum_settings/submission/zenodo-v1.1.0/publication/` and the website's `docs/papers/minimum-bell-setting-complexity/review.pdf` match that digest exactly. I copied the matching archived file into `papers/21699069/` and extracted its exact text with `pdftotext -layout`. The current working `qubit_povm_pvm_minimum_settings/paper/review.pdf` has a different MD5 and was not used. Full paths, public content URL, retrieval timestamp and digest evidence are in `papers/21699069/SOURCE_PROVENANCE.json`.

The preserved PDF has 34 pages. I read the entire extraction (1,816 physical text lines; 14,621 extracted words), including model definitions, main proofs, all nine appendices A–I, attribution, AI disclosure and references. I also rendered and inspected the first page to confirm the title, sole author and review-format line numbering. This is the author's line-numbered manuscript, not an external referee report or proof certificate.

## Scientific content and boundaries

The abstract and Main Theorem, extraction lines 11–39, claim equality of the **shared-randomness convex hulls** of fixed-qubit POVM and PVM behaviors for every bipartite architecture with two inputs per party and arbitrary finite, input-dependent output alphabets. The model at lines 145–231 fixes local Hilbert-space dimension at most two, permits zero projectors and stochastic output postprocessing, and excludes a dimension-increasing Naimark dilation. Linearity identifies Bell support functions while preserving the distinction from the raw nonconvex strategy images.

The explicit rational 3×2 Bell functional and Theorem 3.1, lines 234–429, combine a CHSH term with a three-state discrimination term. An exact rank-one qubit POVM strategy attains `L0 = 20 sqrt(2) + 16/25`, above the global PVM upper certificate `U = 20 sqrt(2) + 3/5 + (4 + 3 sqrt(2))/250`. The strict gap is `3(2 - sqrt(2))/250`. Neither certificate is claimed as the exact global optimum. Appendix B gives a stronger algebraic attained value, but proves its optimality only within its stated one-parameter family.

The equality proof first establishes one-binary-party simulation through Lorentz-cone circuits (lines 432–539), then reduces a hypothetical separator to a pure entangled strategy with one binary PVM and one extremal ternary rank-one POVM per party (lines 541–652). Its remaining argument builds an exact physically realizable Lorentz-incidence model (lines 655–850), uses finite POVM duality to force positive determinant multipliers (854–971), computes the weighted second form with inertia (4,12) (974–1069), and exhausts all ranks of the metric differential (1091–1197). Rank at least two gives an uphill physical direction, rank one is excluded by projective-fiber rigidity, and rank zero admits a deterministic bounded-transportation simulation. The finite exact checkers supplement these universal deductions; Appendix I, lines 1700–1725, explicitly records what computation does not prove.

The discussion and limitations, lines 1200–1248, exclude raw-set equality, same-state simulation, operator-level projective simulability of individual POVMs, exact global optima, and private-randomness entropy bounds. Higher local dimensions, multipartite experiments, sequential measurements and experimentally robust witnesses remain separate questions. The introduction and reference 4 explicitly credit Vértesi–Bene's earlier 3×2 POVM advantage. Extensive generative-AI assistance, the human author's responsibility, and absence of prior independent expert human verification remain explicit.

## Comparison with primary paper 21699161

The previously reviewed primary deposited text is `papers/21699161/kriebel-2026-minimum-bell-setting-complexity-v1.1.0.txt`. A fresh read-only native GET confirms its primary DOI **10.5281/zenodo.21699161**, identical manuscript title and standard publication PDF checksum **9ab44afe416cfabc1d065de0c62647b5**; the snapshot is `papers/21699069/primary_native_public_record.json`.

Removing exactly 1,038 sequential left-margin line numbers from the review extraction gives 99.9853% token-sequence agreement with the primary extraction. All remaining differences are the placement of the two entries `c-dot` and `0` within the extraction order of the displayed tangent-metric matrix H; no scientific prose or theorem has changed. The exact comparison and its two difference windows are saved in `papers/21699069/PRIMARY_CONTENT_COMPARISON.json`. I do not claim byte-identical PDFs.

The [author's paper website](https://aleckriebel.github.io/Math/papers/minimum-bell-setting-complexity/) explicitly lists 21699161 as the primary publication PDF and 21699069 as the line-numbered PDF for page/line references. Thus **isVariantFormOf** accurately links two presentations of the same manuscript. [DataCite's format guidance](https://support.datacite.org/docs/connecting-versions-with-related-identifiers) recommends that relation for different formats or presentations of one resource. A read-only Zenodo vocabulary GET confirmed native identifier `isvariantformof`, saved in `papers/21699069/RELATION_VOCABULARY.json`. This relation does not claim a new version, successor result or external review.

## Proposed metadata and rationale

The proposal is `patches/21699069.json`. It changes only **keywords, language, creators and related_identifiers**.

- Add the same 16 grounded specialist terms used for the primary paper: Bell nonlocality, Bell inequalities, quantum correlations, qubit measurements, positive-operator-valued measurements, projection-valued measurements, POVM, PVM, shared randomness, convex behavior sets, dimension-constrained quantum correlations, measurement-setting complexity, Lorentz cone, nonprojective measurements, quantum foundations and state discrimination. The original published record has no subjects. These tags track the operational question, exact model, proof mechanism and separating witness without implying the excluded conclusions.
- Add missing English (`eng`).
- Add Alec Kriebel's user-supplied ORCID **0009-0001-9320-500X**. The patch retains the existing author name and the native translator copies the complete original creator object, preserving given/family names and the existing **researcher** role. No affiliation is invented.
- Add **isVariantFormOf** → primary manuscript DOI `10.5281/zenodo.21699161`.
- Add **isSupplementedBy** → the [exact source/verification release](https://github.com/AlecKriebel/Math/releases/tag/qubit-povm-pvm-minimum-settings-v1.1.0), already named in the original description and verified to exist at commit 773356a1de85290c3e85a361e0019f5f82b8e6d9. This points to supporting artifacts; the codebase deposit is not being updated.
- Add **isDocumentedBy** → the matching paper website, whose content identifies both formats, assumptions, verification boundary and all relevant archives.
- Add **cites** → `10.1103/PhysRevA.82.062115`, the explicitly credited prior Vértesi–Bene article in reference 4 (extraction 1740–1742). The [APS publisher page](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.82.062115) confirms the article title, authors and DOI. This supports scholarly attribution and citation discovery; it does not imply dependence on that paper's numerical optimization.

The original description already explains the central theorem and its important limitations, including AI assistance and unreviewed status. It is **retained verbatim**, including the source release. Title, publication date, version, publisher, license/rights and access are untouched. No DOI or generated identifier field is patched.

## Local preservation checks and remaining handoff

The record has a native creator role and nonempty `custom_fields` (`code:codeRepository`), so root must use the native preservation workflow after its authorized handling of the pre-existing unfinished edit. A legacy metadata projection would be unsafe.

I ran only the native translator locally against the saved PUBLIC record. `papers/21699069/native_target_metadata.json` records the intended full native metadata. `reviews/EXTRA_QUBIT_PATCH_QA.json` confirms that the protected record view—record ID, PIDs, parent, version history, file IDs/checksum/size/access/default preview, record access and custom fields—is equal before and after this local translation, that only ORCID was added to the original creator, and that description/title/date/rights are unchanged. The four-field patch has 16 distinct tags and SHA-256 **baad5f244f5158307d5560d22813a0da699e1d1e0fc7c3678dd2f56840e0d908**.

These local checks do not certify a remote update. Independent content cross-review and root's final public readback must still verify DOI **10.5281/zenodo.21699069** and the deposited PDF checksum **a5a7a0d08c99e864159de09a7866f6ab** remain unchanged, along with parent/version history and all other protected native fields. This reviewer has neither discarded nor reused the pending edit and has performed no remote mutation.
