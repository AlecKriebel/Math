# Source and scope gate for KP-4.48

Checked 3 October 2026. The target is ID 2924, K3 Problem 4.48. This gate does not certify a new solution: the accompanying work remains unresolved.

## 1. Identity and original question

- The requested catalogue URL, https://www.unsolvedmath.com/problems/2924, was requested directly and returned HTTP 403. It was not treated as an accessible proof source.
- Catalogue identification was checked against the supplied pinned dataset, then independently against the actual K3 book. Generated literature notes were not accepted as mathematical evidence.
- The exact primary question is on printed p. 228 of the author-hosted 436-page K3 PDF, with the remarks on p. 229. These two pages were visually inspected. It asks about the compact-open group of boundary-fixing **homeomorphisms** of a compact contractible **4-manifold**.
- The catalogue's cited AIM URL, https://aimath.org/pastworkshops/kirbylistrep.pdf, is a four-page workshop report. It is not the problem book and does not contain Problem 4.48. The correct book source is linked in PROOF.md.
- Neither a smooth substitute nor the statement in dimension 5 is counted as a resolution of this target.

## 2. Prior-attempt checks

The check was not based only on the queued row. The live repository was checked for:

- The current `unsolved_math_prioritization/QUEUE.md` row, which read queued, 0/5 for rank 535 / ID 2924.
- Actual entries in `unsolved_math_prioritization/attempts/` and `problems/`, with no matching 2924 artifact found.
- Pull requests in all states matching 2924, KP-4.48, “Kirby” with “4.48”, and contractible homeomorphisms; no matching pull request was returned.
- Branch searches for 2924, 535, and kirby; the kirby query was followed through its final cursor, with no matching target branch found.
- The public related-target-group record, which had no match for this ID/code.

A recursive tree request failed with a transport error twice, so no successful exhaustive tree-search claim is made. The successful direct-directory, PR, and branch checks found no prior attempt to supersede. These are bounded repository checks, not a proof that an unpublished or differently labeled attempt cannot exist.

## 3. Literature gate and proof-reading scope

### K3 (2026)

The question/remarks on pp. 228–229 agree with the target. The remarks record the disk case and connectedness, and cite the higher-dimensional result. K3 is evidence for the question and its recorded status, not a proof that every later result has been excluded.

### Galatius–Randal-Williams (2024)

Full accepted manuscript obtained and read at the relevant proofs: Theorems A–C and the reduction in §1.3; the first proof of Theorem C in §2, including Proposition 2.1, Lemmas 2.2–2.4, and the final convergence step.

Important distinctions:

1. Theorem A's conclusion is **weak contractibility**.
2. The theorem assumes d ≥ 6.
3. The tower calculation and the convergence theorem are different steps. Acyclicity gives the former, not the latter.
4. Remark 1.2 already points to the extension to d = 5. Its smooth dimension-4 failures are not failures of the topological statement.

### Krannich–Kupers (2026)

The final institutional PDF was obtained. The definitions in §6.1, Theorems 6.1 and 6.3, their complete proofs in §§6.2.1–6.2.2, and the full proof of Theorem 6.18 were inspected. Theorem 6.18's page 127 was also visually inspected. Section 5.4.2 identifies the parametrized topological isotopy-extension input.

The theorem extends GRW to dimension 5, including topological manifolds without assuming an already chosen boundary smoothing. Its proof uses formal smoothability and a special dimension-5 argument. The requirements m ≥ 5, k < min(m − 2, m/2), and the smoothing comparison's m ≠ 4 restriction are explicit. None is satisfied merely by declaring a contractible 4-manifold formally trivial.

### Orson–Powell (2025)

The author preprint actually obtained is arXiv:2207.05986v3, dated 14 August 2024, of the 2025 JDG article. Theorem A, its proof in §3.3, the Poincaré-variation definitions, Theorem 3.1, Proposition 6.2 with its obstruction calculation, and the complete proof of Theorem 3.1 in §6.2 were inspected.

For this application both variation groups and the relative H¹ group vanish. The cited classification is a theorem about components, not an all-parameter contraction. Its surgery and h-cobordism inputs are external established theorems; they are not re-proved or mechanically verified here.

### Gabai–Gay–Hartman–Krushkal–Powell (2026)

The published Cambridge full text was checked, and the institutional copy of arXiv:2311.11196v2, dated 1 February 2026, was read for Theorem 1.5 and its complete topological arguments in §§5–6. The proof includes the boundary decomposition, the extension of Perron's method, and the alternative correction of Quinn's proof through factorization and controlled cancellation.

This avoids assuming that Quinn's original replacement-criterion proof was sound, and avoids silently applying Perron's original no-1-handles boundary statement in greater generality. The result is a pointwise isotopy theorem, not a continuous choice over spheres of arbitrary dimension. The proof's external deep results, including disc embedding and the retained valid portions of Quinn's argument, remain cited inputs.

### Alexander trick and isotopy extension

The Alexander formula in Friedl–Nagel–Orson–Powell, Lemma 4.4, was checked. PROOF.md supplies the joint-continuity and uniform-support argument rather than relying on the source's omitted continuity verification.

Edwards–Kirby's original embedding-space deformation results, Corollaries 1.2–1.4, their proofs, and the relative refinements in §7 were checked in an accessible complete scan. The first author-hosted scan has no searchable text and was not used as a complete searchable proof source; the Glasgow-hosted scan supplies the complete readable copy. This is the standard parametrized extension input cited again in KK26 §5.4.2. PROOF.md uses only the isotopy component in its embedding-space reduction.

## 4. Scope safeguards

- No assertion that weak contractibility automatically gives actual contractibility of this G.
- No universal CW-type or ANR assertion about G.
- No smooth mapping-class counterexample presented as topological.
- No use of the smooth s-cobordism theorem in dimension 5.
- No passage from individual isotopies/extensions to a continuous selection without a proof.
- No claim that a finite calculation tests all compact contractible 4-manifolds.
- No novelty or exhaustive-literature claim.

## 5. Public materials

The shareable packet consists only of the authored proof/research report, this source gate, the attempt log, status, source hashes, exact verification program/output, README, and SHA-256 manifest. Source PDFs, page images, full extracted papers, downloaded catalogue data, and raw retrieval responses are not included. Source links and byte hashes identify the inspected versions without redistributing them.
