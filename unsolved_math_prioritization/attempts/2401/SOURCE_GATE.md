# Source/status gate: Erdős 949 (ID 2401)

Checked 2026-10-21 UTC. Gate result: **SOURCE MATCH; GENERAL QUESTION NOT RESOLVED BY LOCATED SOURCES; EXISTING PARTIAL RESULTS MUST NOT BE RECLAIMED.** No proof-search turn, publication, or queue edit was performed.

## Identity and statement fidelity

Row 1870, ID 2401, Erdős Problem 949. The original target concerns an arbitrary sum-free real set S and a continuum-sized A outside S whose sumset A+A also avoids S, including repeated summands. Neither additive closure of A nor measurability nor a Sidon hypothesis belongs in the general question.

Primary original: Paul Erdős, *Problems and results on combinatorial number theory III*, Number Theory Day, Lecture Notes in Mathematics 626 (1977), pp. 43–72, specifically printed p. 57, PDF p. 15, Section 6. The extracted PDF text at lines 569–575 confirms both the complement target and the proposed distinct-sums variant. Source: https://www.renyi.hu/~p_erdos/1977-27.pdf . This is text-layer inspection, not a completed visual page inspection. Local download failed, so no local PDF hash or byte count is asserted.

## Resolution and duplication gate

The indexed maintained tracker labels the general question OPEN and identifies the Sidon variant as affirmative. Direct page retrieval returned HTTP 403; indexed content is not a fresh live-status certificate. Source: https://www.erdosproblems.com/949 . No exact general solution emerged from bounded searches for the problem number, sum-free real sets, continuum, and the original paper title.

The primary discussion documents a historical formulation error: replacing sumset avoidance with closure under addition. Kovač corrected this against original p. 57; Weisenberg withdrew the apparent negative resolution of the corrected question. The discussion also credits Dillies/AlphaProof with the Sidon result, using separate small-cardinality and continuum-cardinality cases. Chojecki reports the Baire-property case and notes that the small-cardinality argument does not need Sidon. These are prior work, not new contributions of this gate. Forum comments are not blanket certificates of correctness. Source: https://www.erdosproblems.com/forum/thread/949?order=oldest .

A directly inspected primary repository confirms that google-deepmind/formal-conjectures PR 1509, “prove the open variant for a Sidon set,” was merged 6 January 2026 as aed8921, with six checks reported passed. This is strong existing-result evidence for the variant, not the general question. No local Lean build was run. Source: https://github.com/google-deepmind/formal-conjectures/pull/1509 .

Search also surfaced AI working reports reproducing small-cardinality, Sidon, Baire, and measurable special cases. They were treated as duplicate-warning leads, not independent authorities establishing a full solution. In particular, any regularity-based attempt must handle diagonal sums 2a explicitly and must not silently impose regularity on arbitrary S.

## Recommended disposition

Proceed only on the unrestricted continuum-cardinality case, with full awareness of existing special cases. Do not count the Sidon proof, a small-cardinality maximality proof, or the obsolete additive-closure counterexample as a solution. A live tracker/discussion refresh and broader primary-literature review remain appropriate before a novelty claim. This bounded gate certifies neither worldwide openness nor priority.

This local frozen package contains authored arguments and public-source metadata only; source documents and private coordination material are excluded.
