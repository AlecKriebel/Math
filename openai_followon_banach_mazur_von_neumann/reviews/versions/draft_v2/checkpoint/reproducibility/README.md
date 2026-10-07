# Reproduction and evidence scope

The main artifact is an explicitly conditional research draft, not a Zenodo-cleared full solution. Review and publication gaps are recorded in publication/PENDING_ACTIONS.md.

## Manuscript and PDF

The only required source is manuscript/main.tex, with an embedded bibliography and no external image input. Open this source in the Codex built-in LaTeX editor. Its compiler confirmed success. The exported downloadable PDF is output/pdf/paper.pdf (four pages), produced independently by Tectonic0.16.9 and inspected after Poppler26.08.0 rendering. In a clean directory containing a copy of main.tex, run `tectonic -X compile main.tex --outdir .`; this generates main.pdf. Compare extracted text with the supplied paper.pdf; PDF byte hashes may change with metadata timestamps.

## Finite exact checks

Run `python3 research/cohomology_adversary_checks.py` with Python3 (tested3.14.6; standard library only). It writes cohomology_adversary_checks.json and reports5,461 exact central-homotopy equations,16 Catalan leading counts and7 ordered-block endpoint cases. These are falsification checks on finite proof mechanisms, not a computational proof of the infinite-dimensional theorem.

Run `python3 research/draft_whole_review_1_checks.py` for the independent noncommutative central-homotopy check on M2(C) direct-sum C. Its 260,416 exact scalar equations passed on independent root replay. It uses only the Python standard library and does not establish the full theorem. The clean standalone TeX reproduction, including exact extracted-text comparison with the exported PDF, is recorded in receipts/clean_draft_reproduction.json.

## Pinned manuscript and static Lean audit

The included upstream family295 source is unchanged from OpenAI Math commit adc7f1241b42e322a6451854ab7e4b4c146bf78a and retains Apache-2.0 license and author attribution. Verify its listed SHA256 hashes against receipts/pinned_sources.json. OpenAI's manuscript-specific citation is preserved in its README. Locally retrieved CIRM/arXiv PDFs and text extractions lacking identified redistribution permission are excluded from the published project tree; download the primary URLs in research/roydor_primary.md and verify that report's hashes.

For static Lean reproduction, acquire upstream commit adc7f124 and preserve the372 paths/hashes in research/lean_audit/import_closure.json. `static_audit.py` reads the manifest's source paths (adjust a local copy of the path prefix for a different checkout) and ignores nested comments and strings before its source-token scan. Root separately verified every hash in receipts/root_lean_source_hash_check.json. Neither scan executes Lean or computes proof-term dependencies.

## Fresh kernel build remains unverified

The aborted setup used Lean4.34.1 and mathlib d13f23b723b8a846827a245b89c10fc7d3f11612. Small setup/probe/failure records are under receipts/lean_attempt_*. The exact OAI source copy is local-only under research/lean_audit/build; recreate it from the pinned upstream if absent. Read research/lean_audit/kernel_build_report.md before retrying. Dependency setup failed for disk space, before successful MainResult compilation/import or any #print axioms result. The present evidence therefore cannot be cited as kernel reproduction. The final formal statement's direct scope is abstract Banach-predual algebras; the general concrete-to-abstract bridge is unfinished in the pinned mathlib.

Formal reproduction is optional additional validation if relying on the independently checked mathematical proof. It is required before any claim of reproduced formal verification. The mandatory remaining dependency for full publication is the unread Roydor journal theorem/proof, not a nonexistent blanket requirement to formalize the follow-on.
