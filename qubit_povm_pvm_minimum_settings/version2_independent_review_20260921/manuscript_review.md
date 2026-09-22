# Independent manuscript alignment review

Checkpoint: 2026-09-22T00:49:47Z / 21 September 2026 Pacific. Completion estimate: **100% of the bounded manuscript review**. This review makes no production edits and does not publish or contact anyone.

## Scope and verdict

Reviewed the manuscript diff `cc320ba38..5ec53ad703c0aa6834f7b1f1b409a83c9c332eea`, the source directly extracted in memory from `version2_completion_20260921/archive_current/21699181-kriebel-2026-minimum-bell-setting-complexity-source-v1.1.0.tar.gz`, the September 13 v2 plan, current actual Lean declarations for the changed proof and endpoints, and the exact frozen output ZIP. The earlier favorable review was not treated as proof of correctness. Rendered PDF inspection and fresh complete Lean reproduction belong to the parent review, not this subtask.

**No newly introduced mathematical error or overclaim of full-manuscript formalization was found in this bounded review. One P2 publication-readiness issue remains: the PDF does not identify a retrievable proof-package location.** This is not a Lean validity blocker. The source continues to expose its retained manuscript-only assertions and should not be called a formalization of every displayed argument.

## Actionable finding

### P2 — Identify the formal proof package in the standalone manuscript

**Location:** `paper/main.tex:1785`–`1800` (Data, code, and verification), with the same omission in the frozen ZIP's `paper/main.tex`; `paper/appendices.tex:796`–`809` provides local commands and filenames but no retrieval link.

The data/code paragraph refers to “the accompanying repository” and `qubit_povm_pvm_minimum_settings/bell_lean`, but a reader holding only either publication PDF cannot identify that repository or the proof snapshot from these references. The author's homepage in the title block is not an explicit identification of the accompanying proof package. This matters because v2 presents formal verification as a principal evidentiary addition and gives commands requiring files the PDF does not locate.

Reproduction of the source search against the **exact final ZIP** gives zero occurrences of each of `github.com`, `zenodo`, `21699224`, `21699161`, and `21699069` in all three manuscript sources (`paper/main.tex`, `paper/appendices.tex`, `paper/references.bib`). The source has ordinary DOI links for cited literature, but no DOI identifying this work's proof companion. The manuscript's proof table and package command therefore do not supply an archive retrieval path.

**Recommended correction before public publication:** add an explicit persistent identifier for the corresponding proof companion in the code-availability paragraph and bibliography. A verified fixed-commit repository URL is suitable while this remains a local candidate; after preparing actual linked Zenodo versions, use the exact companion version DOI, and include the certified source fingerprint/receipt reference. Do not label any old v1 DOI as containing the new Lean package, and do not invent a future DOI. Rebuild both PDFs and update their package bindings after that manuscript edit. A proof-source rebuild is not automatically required merely because the paper gains a link, but its publication artifacts and correspondence hashes must be refreshed.

**No compounding false DOI claim found in package metadata:** directly inspected final ZIP members `README.md`, `CITATION.cff`, `VERSION_2.md`, and `bell_lean/README.md`. Top-level README line 13 states that no new immutable release or DOI is claimed. VERSION_2 line 3 explicitly distinguishes historical v1.1.0 Zenodo records. CITATION lines 12–13 contain the actual repository and mutable main path, not an old DOI described as v2. That file's `version: 2.0.0` is consistent with a clearly labeled local candidate. These package links do not solve standalone PDF discoverability.

## Verified alignment and scientific checks

### Archived baseline and strict-domain correction

The source extracted from the archived tarball differs from `cc320ba38` only in Definition 5.1's signature/common-cone wording. Thus reviewing only the requested Git range would omit a real archived-to-v2 change; this review inspected both comparisons.

Current `paper/main.tex:1070`–`1086` explicitly retains Lorentz signature `(1,3)`, orients the future cone with `u`, and restricts the positive-pairing/common-cone equivalence to that signature hypothesis. It states that the scalar inequalities alone do not force the signature. This fixes the archived unqualified equivalence without deleting a physical prerequisite. The archive already mentioned the signature; describe the change precisely as correcting that equivalence/definition, not introducing an entirely absent signature concept. No changed principal conclusion was detected.

### Section 3 and related work

Current lines 430–437 appropriately identify Section 3 as a supporting exact certificate in the known architecture and credit the shared dominant-CH/CHSH mechanism. The former ambiguous “Global optimum claimed / No” row is removed. The introduction and abstract retain earlier credit. The contribution list places the reductions/equality ahead of the witness. Retaining the global-bound derivation in the main text is compatible with the plan's optional, rather than mandatory, relocation of routine derivations.

The new paragraph and bibliography were checked directly against [Zhu et al., arXiv v2, 31 August 2026](https://arxiv.org/html/2608.01317v2). It correctly distinguishes their rational all-state qubit separation/Lean certificate and separate unrestricted-dimensional optimum certificate from the universal two-input question. Author names, title, date, version URL, and arXiv identifier agree. No private numerical observation is promoted to a cited theorem.

The alternative rational bound `289/10` is correctly stated as stronger than the paper's `U`, below the witness, and not an exact optimum. `Bell/ProjectiveBound.lean` quantifies over actual physical projective strategies, branches on each ternary zero-effect position, and extends linearly to the convex hull. Its certificate is appropriately distinguished from the retained physical-to-scalar deficit route.

### Replaced multiplier proof

`paper/main.tex:1394`–`1424` matches the actual structure of `Bell/DeterministicGap.lean` and `Bell/IncidenceScores.lean`. The reset preserves the sole circuit and `u`; the acted block corresponds entrywise to a physical whole-input deterministic replacement. Pairing the displayed stationarity equation with the original and reset blocks cancels normalization and gives

\[
\mathcal L(P)-\mathcal L(PR_j)=2\lambda_j r_j^TP^TQPu.
\]

The sign and factor two agree with `stationary_gap`. Positive future-null/timelike pairing supplies the positive denominator. The local hidden-variable model of the replacement gives a strictly positive deficit at a strict separator, forcing positive multipliers. This no longer depends on the general dual-attainment/pullback assertions retained immediately above it. Calling the reset block a representation of a physical behavior, rather than a genuine residual point, is correct because it can be singular.

The compact Lemma 4.1 retains the nonzero-coefficient argument: perturbation along a proper subset leaves an outside coefficient unchanged. Its circuit rank bound, extreme-ray exclusion, and same-ray cancellation distinction are coherent.

### Formal scope and remaining claims

Appendix I makes the model, ordinary finite hull, full-strategy selector, actual density/effect matrices, finite outcome conventions, stochastic convex closure, and dimension-at-most-two bridges explicit. It does not claim same-state simulation, raw POVM/PVM equality, global optimization, or priority. The named central targets were checked in production `Targets`, `Assembly`, `ProjectiveBound`, and `StrengthenedWitness`; conditional helper declarations are not misrepresented as the unconditional final endpoints.

The formal high-rank route is identified as differentiable feasible curves plus an exact quadratic score-gap argument. The manuscript's full Hessian/inertia proof remains displayed and is honestly marked as a different, unformalized argument. That distinction is scientifically appropriate, though a future journal edit could give the formal curve identity more space and move the unused route to a supplement. This is an optional presentation improvement, not a correctness finding.

The manuscript explicitly leaves the following broader arguments outside the formal coverage: general SDP dual attainment/complementary slackness and determinant pullback; the full 14-dimensional smooth manifold and inverse-metric Hessian/inertia; the arbitrary pointed-cone and mixed-state common-span formulations and general rank-square bound; selected physical-to-scalar, spectral, ideal-discrimination, and Appendix B uniqueness/dual-slack calculations. Formal certification of the endpoints does **not** settle these claims. This review did not independently reprove all of them and found no new specific counterexample. They remain mathematical claims subject to ordinary review, not merely explanatory text automatically certified by the endpoints.

### References and numbering

A fresh source scan found no duplicated labels, unresolved cross-reference labels, or missing bibliography keys. The new remark is 3.2 and does not shift later section-numbered theorems: the circuit lemma stays 4.1, strict-domain definition 5.1, multiplier positivity 7.3, equality 9.3, and minimality 9.4. Lean version `4.19.0` matches `lean-toolchain`; the listed Mathlib revision matches the package's pinned specification. Source cross-reference checks are not a substitute for the parent's PDF review.

## Minor release polish

`paper/main.tex:55` labels this a September 2026 working revision. That is honest for this local candidate. The earlier v2 plan also requested the initial deposit date and revised release date in the eventual manuscript. Add the historical 30 July 2026 deposit and actual revised-release date when finalizing public metadata; do not invent a release date now. This is prepublication metadata polish and does not undermine the proof.

## Limits

No new full kernel run or independent rebuild of Mathlib was performed here. No assertion about the correctness of every unformalized manuscript statement follows from this review. The report addresses scientific manuscript alignment and discoverability, with bounded spot-checks of actual Lean definitions and proof routes; the separate proof and package reviewers own their verification findings.
