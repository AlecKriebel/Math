# Reproduction and verification package

A two-tail obstruction to ambient conjugation in Dlab groups
Alec Kriebel — ORCID 0009-0001-9320-500X
Version 1.0.0; 17 October 2026.

The paper gives an affirmative answer to the corrected ambient-conjugation formulation of Kourovka Notebook 21.149. The construction acts on G=D_<2>([0,1]) and defeats every embedding into the standard real Dlab families, with no restriction on the ambient slope group or group order.

## Contents

- paper.pdf: complete typeset proof and exact source attribution.
- main.tex: complete self-contained LaTeX source; ordinary TeX packages only.
- exact_constructions.py and exact_constructions_result.json: standard-library exact-rational checks of finite formulas.
- audits/: mathematical reviews, source-scope reconciliation and priority-search records.
- source_manifest.json: authoritative Notebook source URLs and cached-file checksums, without redistributing the books/articles.
- LICENSE.txt: paper, prose and accompanying code are licensed CC BY 4.0.

## Reproduce

Compile with `tectonic -X compile main.tex`, or use a LaTeX installation with amsmath, amsthm, mathtools, lmodern, microtype, hyperref and enumitem. Run twice if using pdflatex.

Run `python3 exact_constructions.py`. No third-party package or network access is needed for this verifier. Do not use Python optimization flags; optimized mode is deliberately refused.

The verifier checks 1,562 exact segment interpolations, 3 prescribed tuple maps, 200 bump intervals, 441 conjugated affine germs, and 36 affine-group cases. These finite checks supplement the displayed general identities. They do not prove simplicity, quantify over embeddings, or replace the infinite proof. No validated computation is used as a premise of the main theorem.

## Dependencies and source boundaries

Dlab (1968) Theorem 4.3 supplies simplicity of G and its interval copies. His Theorem 4.1 identifies its two bi-orders; the required positive-cone/order preservation is also checked in the paper. Other support/germ/embedding deductions are proved in the paper. Zenkov–Medvedev (1999) §2 establishes that full and reflected real Dlab groups have the required eventual affine left germ. That source passage was independently reproduced from primary indexed full-page text; the downloadable PDF endpoint timed out. The audit reports this access limitation. The current official Notebook update is dated 6 October 2026, 21st edition, p. 199. The paper credits Gong–Yang–Zeng arXiv:2609.18630 for the earlier rank-one six-family theorem and one-tail mechanism, and the original-formulation solution/formalization of van Doorn–Judin–Monticone–Morrison.

## Review and priority status

AI tools were used extensively in discovery, development, writing and verification. Separate AI adversaries checked the proof; their reports are supplementary evidence, not a substitute for proof or independent human peer review. This preprint has not undergone independent human peer review. No Lean/formal proof-assistant verification of this new theorem is claimed. The cited Lean source for the original problem formulation was compared only for its theorem scope, not rebuilt.

Literature searches through 17 October 2026 found no prior result covering the unrestricted ambient quantifiers. The audit is bounded: inaccessible subscription databases, indexing lag and unpublished work cannot be ruled out. The specific earlier theorems and source restrictions are documented. No claim that a reviewer established first priority is made.

Audit reports are dated checkpoint records. Earlier pending-gate statements describe their historical checkpoint; later scope reconciliations and final package reports record the subsequent disposition. The manuscript remains the authoritative mathematical argument.
