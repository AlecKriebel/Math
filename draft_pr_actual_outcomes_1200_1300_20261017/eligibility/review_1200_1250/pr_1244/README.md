# Hyperarithmetical degrees and skip two-cycles

This is an AI-assisted, unrefereed mathematical draft. Acceptance records one internal AI mathematical reconstruction of a credited prior result, with explicit foundational imports. It is not human peer review or formal proof-assistant certification. This is a prose proof-and-audit edition, not a computational reproduction package. No novelty, priority, or worldwide-current-openness claim is made.

## Accepted prior-result component

For every enumeration degree b, b has a hyperarithmetical representative if and only if b is below every enumeration degree a whose double skip equals a. The equality is enumeration-degree equality; the skip of A is the degree of the complement of K_A. Skip is neither the Turing jump nor the enumeration jump. Such cycles exist, so the universal statement is not vacuous.

The converse characterization is credited to Jun Le Goh, as reported in Mariya Soskova’s contribution to Oberwolfach Report 21/2021 and her WDCM 2021 slides. The lower bound and cycle existence are credited to Andrews, Ganchev, Kuyper, Lempp, Miller, Alexandra A. Soskova and Mariya I. Soskova. The analytic basis theorem is due to Harrington, Shore and Slaman. This edition reconstructs the relevant arguments and does not claim a new theorem.

## Remaining target

The separate question asks for an arithmetical degree all of whose finite skips are nontotal, equivalently with no comparison from any skip to the next. This edition neither constructs such a degree nor proves that none exists. Every skip two-cycle is nonhyperarithmetical, hence nonarithmetical; existing cycles cannot answer that arithmetic question. A source reformulation dropping the adjective “arithmetical” must not be used to discard this restriction. A third source question, first-order definability of skip, lies outside the selected two-component target.

## Complete argument and audit

- [PROOF.md](PROOF.md) contains the full authored proof: exact set fixed points, a single uniform operator on all valid ordinal notations, successor jump transport, effective limit joins, the HSS witness-fusion lemma and Goh’s common-lower-cone characterization.
- [AUDIT.md](AUDIT.md) records the logical checkpoints and imports for that same single reconstruction. It is not a second independent mathematical audit.
- [ACCEPTANCE.md](ACCEPTANCE.md) and [ACCEPTANCE.json](ACCEPTANCE.json) state the exact accepted claim, attribution and unresolved boundary.
- [SOURCES.json](SOURCES.json) preserves public bibliographic data, PDF hashes and sizes, selective inspection history and version limits.
- [VERIFICATION.json](VERIFICATION.json) distinguishes artifact authentication and finite checks from mathematical proof.
- [MANIFEST.json](MANIFEST.json) names all eight files and hashes the other seven; its own digest is independently pinned in the draft-PR body.

Only authored mathematical prose and public verification metadata are distributed. Source PDFs or text, dataset contents, page images, executable code, raw outputs and private coordination material are excluded. The complete files of four sources were retained in the original audit, but only the specified pages were inspected. The author-hosted AGKLMSS and HSS versions were not byte-compared with publisher editions. No new source inspection or proof search is represented by editorial preparation.
