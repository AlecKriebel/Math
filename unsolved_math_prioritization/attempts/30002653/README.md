# Audited partial results: perfect-cone Prym indeterminacy

Problem **30002653**, rank 724, OWR-13109-004. The full target remains **unsolved after 5/5 approach families**. This draft preserves the original author packet in `safe/` and the independent audit in `audit/` byte-for-byte. Read this controlling guide before the frozen research note: it incorporates the audit's coordinate clarification and supersedes historical statements that independent review or publication is still pending.

## Accepted result and remaining gap

The retained infinite-subfamily theorem applies to an actual admissible double cover whose irreducible covering components are all invariant under the involution. It includes branchwise-fixed nodes, handled by contraction, and uses the published perfect-cone metric criterion and exact Friedman–Smith degeneration characterization. Within that class, nonextension is equivalent to membership in the union of the **closures of FS2 and FS3**. The closure qualification is essential; this is not merely a classification of generic two-component covers.

Genuinely exchanged covering components with coupled coedges remain unresolved. The gluing lemma and metric certificates do not reduce every such cover to the proved class. There is no all-genus solution, counterexample to the full target, established novelty, or global-openness certificate here.

## Controlling ambient-basis clarification

In `safe/RESEARCH.md`, Approach 3's phrase “integral basis (3)” must be read as the **ambient integral coordinates used to display (3)**, not as a claim that its full coedge list is an integral basis. Put e1=(t1+...+tn)/2 and ei=ti for i>=2. These e vectors form the ambient integral lattice basis. The coedges a=2e1-e2-...-en, e2,...,en have index two. The displayed Q_n is the Gram matrix in the ambient e basis; its first diagonal entry is n/4, other first-row entries are 1/2, and remaining diagonal block is the identity. Ray equalities are evaluated on the actual coedge vectors in those coordinates.

No retained metric, primitive-coedge criterion, sign-average, or proper-face calculation assumes a unimodular full coedge basis. The proper-face argument appends e1 deliberately to obtain determinant one. See `audit/AUDIT.md`, section 7, and `audit/BINDING.json` for the audited interpretation. The frozen originals are retained without silently rewriting them.

## Lattice and geometric qualifications

- Use the dual of the **projected** anti-invariant homology lattice. Replacing it with the dual of integral anti-homology changes the lattice and can give the wrong answer.
- After contracting branchwise-fixed edges, bridge coedges require half-primitive normalization. An actual separating covering edge instead has zero coedge and is omitted.
- An involution graph without edge inversion is not automatically a realizable admissible cover. Fixed-branch degree at each invariant component must be even. Of 3,848 fixed-edge algebraic configurations tested, 424 satisfy this condition and are geometrically realizable with suitable component genera. The rest are algebraic stress tests only.
- Finite enumeration supports the proof but is not a universal proof: the author checked 772 simple graphs with 5,325 assertions; the independent controls checked 27,476 simple graphs with 578,827 assertions. The independent minimal-edge-deletion bond comparisons run through five vertices, not all six-vertex graphs.

## Source boundary

Primary OWR Question 3 and the corresponding JEMS Question 7.4 were inspected as recorded in the frozen source metadata. Frinak's 2018 thesis has a later genus-indexing inconsistency; only its unambiguous introductory theorem is used, and its complete computational enumeration was not replayed. Zakharov's July 2026 manuscript is a preprint concerning base genus four and target dimension three, not an all-genus result. The exact catalogue website page returned 403 and was not inspected; raw AI corpora were absent and uninspected. The bounded literature search found no complete resolution, which does not establish present global openness.

## Replay

Python 3.10+ and the standard library suffice. From any working directory, run:

    python3 /path/to/30002653/verify_publication.py --expected-manifest SHA256_FROM_PR

Use the externally recorded SHA-256 of this directory's `MANIFEST.json` from the PR description. The verifier checks the exact file inventory and all hashes, the separately pinned author and audit manifests, assertion activity, both mathematical replays, and their mutation controls. It imports no primary-source material. Add `--queue /path/to/unsolved_math_prioritization/QUEUE.md` to verify the published queue bytes. The queue patch changes only this problem's Status to unsolved and Turns to 5/5; all other bytes are preserved.

The manifest excludes only itself. Its digest is an external binding, not a self-authenticating claim. Publication and remote-byte replay receipts remain separate from these frozen materials. Historical `remote_mutations: false` fields describe their original research/audit stages. Zero GitHub CI checks, if observed, mean no checks were available; they are not a CI pass.

Only authored analysis, audit, code, results, and public-source verification metadata are included. No PDFs, extracted primary-source text, images, raw corpus records, or private coordination files are included. No merge, release, DOI, or external outreach is part of this draft publication.
