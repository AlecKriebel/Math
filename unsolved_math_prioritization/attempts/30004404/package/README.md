# Figure-eight obstruction for problem 30004404

A complete author candidate gives a negative answer to the literal universal question in OWR-17471-010: the figure-eight knot has no finite nonmeridional surgery, while its zero-filling group is metabelian and cannot contain F₂.

- PROOF.md: full deduction, explicit nontrivial kernel word, and exhaustive no-finite-surgery check
- STATEMENT_AND_SCOPE.md: source quantifiers and distinction from the existential hyperbolic-knot problem
- SOURCES.md: source provenance, exact locations, typography warnings, priority limitations
- RESEARCH_LOG.md and turns.json: one substantive proof approach and chronological checkpoints
- controls/check.py and controls/expected.json: reproducible exact algebra/arithmetic controls
- FROZEN_MANIFEST.json: SHA-256 identities for all public candidate files except the manifest itself

Run `python3 controls/check.py` from this directory. It uses only the Python standard library and prints deterministic JSON. These bounded checks support the proof; they do not independently certify the topological surgery classification or constitute formal proof verification.

Status at author freeze: complete counterexample candidate; independent audit pending. Recommended queue disposition after a passing audit: claimed_solved, 1/5. No novelty or first-priority claim; the argument is a short consequence of classical facts. No claim that any existential persistent-subgroup question is settled.

This package was researched and drafted with extensive OpenAI assistance. It is unrefereed. Source PDFs, whole source texts, screenshots and imported corpora are deliberately excluded.
