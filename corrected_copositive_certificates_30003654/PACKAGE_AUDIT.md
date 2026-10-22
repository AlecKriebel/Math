# Independent publication-package audit

Date: 2026-10-21 UTC. Disposition: ACCEPT within the scope below. Problem 30003654 / OWR-15957-007 remains **UNSOLVED, 5/5**.

## Mathematical acceptance

Independently reviewed the theorem, compact-penalty argument, dual argument, and examples in RESEARCH.md. The fixed-degree correction is sound for closed S contained in a pointed closed convex cone, nonzero h of degree m at most d nonnegative on S, and coefficient closure in the finite-dimensional degree-at-most-d space. The correct horizon test uses the ambient degree-d component, including zero when the actual degree is smaller.

The positive linear functional makes the normalized homogenized section compact and supplies multipliers for odd as well as even degree gaps. Closedness of S recovers its finite points; normalized horizon directions recover its infinite points. Nonnegativity of H and compactness justify the penalty. In the dual proof, evaluation on L^d bounds total mass and closes the evaluation cone; annihilation of H L^(d-m) confines positive evaluation support to H=0. Empty S and zero h are explicitly separated. Constant nonzero h and degree zero cause no additional obstruction.

The literal-source linear counterexample, degree-four separator, nonexact quadratic boundary example, and empty-zero-set origin exception are algebraically consistent. The lifting discussion retains strong positivity and representation-dependent assumptions. No repaired all-set geometric equivalence is asserted without proof.

## Executed package checks

Independently ran both `python -B verify.py` and `python -B -O verify.py`; both exited successfully. Each execution checked:

- Exact package inventory and every manifest-listed SHA-256 and byte count.
- Original authored-script provenance and all 22 assertion records across both scripts, including conditions and recorded control-flow ancestry. The transformed ASTs agree exactly except for assertion replacement by explicit conditional RuntimeError checks. No residual assert statements remain.
- Entire deterministic outputs of both scripts against their committed reference files, in normal and optimized Python: four complete-output comparisons per verifier execution.
- Three actual mathematical input mutations, each in normal and optimized Python: changing the linear example, changing the constraint example, and changing the separator. All six were rejected by the intended mathematical checks rather than syntax errors or a generic artificial failure.
- Rejection of an added nested MANIFEST.json. Inventory also excludes unlisted files, directories, and symlinks; the root manifest alone is excluded from its own hash list.

The observed mutation failures were respectively the actual-leading-form assertion, the counterexample identity, and the separator's diagonal identity. Optimization did not disable them.

## Publication hygiene and limitations

Reviewed all packaged text and JSON for copied third-party documents, raw dataset records, extracted-record hashes or sizes, private filesystem paths, chat links, and private coordination material. None were found. Metadata retained consists of full public-corpus hashes and sizes, public scholarly-PDF metadata and URLs, match results, and inspection history. The source embedded in PUBLICATION_PROVENANCE.json is the authored algebra-check code, not third-party source-document text. Mathematical explanations and paraphrases are authored analysis.

This audit did not freshly retrieve scholarly PDFs or re-establish historical retrieval claims. Those claims remain recorded provenance, not outputs of verify.py. The independent mathematical review and exact symbolic replay are not formal proof-assistant certification and do not certify novelty, solve the exploratory OWR program, establish unconditional SOS completeness, or imply finite convergence or polynomial-time optimization.

The successful inventory runs preceded replacement of this audit placeholder. Regenerate MANIFEST.json after this file is saved, rerun both verifier modes, and record the root manifest's external SHA-256 as the final freeze identifier. This audit itself makes no queue edits or external publication.
