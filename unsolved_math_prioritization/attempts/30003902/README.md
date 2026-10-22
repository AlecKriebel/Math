# Surface automorphism dimension: a credited prior counterexample

Problem **30003902 / OWR-16408-015**, rank 873. The universal genus-one equality is **false by prior literature**. Fujiwara–Oguiso–Yu, [arXiv:2507.13726v3](https://arxiv.org/pdf/2507.13726v3), Remark 1.5(4), page 5, supplies a complex projective K3 surface with Néron–Severi lattice **⟨32⟩ ⊕ D₄(−1)** whose maximum associated-Jacobian Mordell–Weil rank is **0**, but whose full automorphism group is infinite. The included explanation and audit establish **1 ≤ vcd(Aut(S)) ≤ 4**.

The original genus-one formulation permits fibrations without sections. This witness has such a fibration and has no section-bearing genus-one fibration. Requiring a section would change the question.

## Result and review

- [Unchanged author explanation](author/RESULT.md), [one-approach ledger](author/APPROACHES.md), and [historical status](author/STATUS.json)
- [Independent mathematical audit](independent_audit/MATHEMATICAL_AUDIT.md) and [separate acceptance](independent_audit/ACCEPTANCE.md)
- [Machine-readable acceptance](independent_audit/ACCEPTANCE.json), [source inspection record](independent_audit/SOURCE_CHECKS.json), and [public corpus-verification metadata](independent_audit/CORPUS_VERIFICATION.json)
- [Publication acceptance](PUBLICATION_ACCEPTANCE.json), [static tests](PUBLICATION_TEST_RESULTS.json), and [exact package inventory](PUBLICATION_MANIFEST.json)

The independent AI audit accepts the explanation without mathematical correction. This is a review of a known counterexample, not a new counterexample or conventional human peer review. Nikulin's classification is an explicit imported theorem through the current Fujiwara–Oguiso–Yu statement; its complete proof was not re-proved. The earlier Kikuta rank-three counterexample argument is excluded.

No exact virtual cohomological dimension, zero-entropy premise, novelty, formal verification, or resolution of the separate Coble, Enriques, section-required, or positive-maximum-rank variants is claimed. The universal negative conclusion does not classify every restricted case.

## Provenance and verification

Both original ZIPs and their external manifests are preserved unchanged in `archives/`. The author packet has seven regular data files. The audit packet has eighteen regular files, including exact copies of all seven originals and the original archive and external manifest. The intact audit directory is unpacked so its documented relative replay command remains valid.

The audit contains one public reviewer-authored Python utility, `replay_author_integrity.py`. It authenticates author bytes against fixed public pins, never executes author content, and is not a mathematical proof checker. Publication replay first authenticated the complete audit payload, then ran that utility from a relocated directory under isolated Python with and without optimization. An additional sixteen corruption and safety controls per mode had their expected rejection results. The earlier audit's twenty-four positive/negative controls are separately recorded in its unchanged integrity report. Hashes and static controls do not prove the mathematics.

Source PDFs, OCR, extracts, images, raw datasets, private sources, personal data, coordination material, and private checker fingerprints are excluded. Public citations, PDF hashes and sizes, corpus hashes and byte counts, inspection history, and publicly stated manuscript status are included. Historical fields saying review or publication had not occurred describe their freeze time and remain unchanged; the separate acceptance and this wrapper record the later review/publication gate.

Only this row's Status, Turns and Findings cells are edited, to `already_solved`, `1/5`, and the bounded credited finding. All unrelated queue bytes, existing notes and chat links are preserved. Publication adds no research approach. This draft package makes no CI-pass claim.
