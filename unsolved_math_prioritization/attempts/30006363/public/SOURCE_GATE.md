# Source and status gate

Problem **30006363**, code **OWR-14299512-001**, rank **557**.
Checked **2026-10-04 UTC**.

## Catalogue and exact scope

The requested catalogue URL is
https://www.unsolvedmath.com/problems/30006363 . Direct retrieval returned
HTTP 403; the web retrieval also failed. This was an access failure, not
evidence about the mathematical status.

The matching record was recovered from the public Ulam AI UnsolvedMath dataset,
pinned at revision 372682f27c1b0d3d39e75fa63ad7932c7a2e1bde:

https://huggingface.co/datasets/ulamai/UnsolvedMath/blob/372682f27c1b0d3d39e75fa63ad7932c7a2e1bde/problems.json

The local dataset bytes have SHA-256
37067f43734b76ee886b032469836767c34d892de14397ce6aa71da01500e252.
A fresh read of the pinned dataset tree endpoint confirmed the same LFS object
hash and size, 69,291,427 bytes. The matching record's ID, code, and title agree.
Its generated literature assessment and partially-solved label were treated
only as leads, not as proof or independent evidence.

The primary source is Oliver Edtmair's contribution, joint with Sobhan
Seyfaddini, in *Dynamische Systeme*, Oberwolfach Report 31/2025, printed
pp. 1664–1665:

- Report DOI: https://doi.org/10.4171/OWR/2025/31
- Official PDF: https://ems.press/content/serial-article-files/52240
- PDF SHA-256:
  8ba4df2a9edad4311ff99a7f9d03d15ab7873869c81990233ac6f65f54848ca2

Printed p. 1664 is PDF page 18, zero-based page 17. The page was rendered and
visually inspected as well as read in extracted text. Question 1 asks whether
helicity is preserved by topological conjugacy. The preceding definition
requires an orientation- and volume-preserving homeomorphism intertwining
the flows at the same time on a closed three-manifold. The fields are smooth
and exact; they are not assumed nowhere zero. The question additionally asks
about extending helicity to topological flows. PROOF.md preserves these
requirements and does not claim to resolve either unrestricted question.

## Current primary mathematics and proof inspection

Oliver Edtmair and Sobhan Seyfaddini, *A universal extension of helicity to
topological flows*, arXiv:2508.10609v1, submitted 14 August 2025:

- https://arxiv.org/abs/2508.10609v1
- https://arxiv.org/pdf/2508.10609v1
- PDF SHA-256:
  fcbe11426065224c39471d8ca02c89e47a11087e4d848f85c5c38f0e6e54c432

The current arXiv page lists v1 as its only version. Theorem 1.3 gives the
nonsingular case. Relevant definitions and complete printed arguments were
read, including Theorem 3.1; Lemmas 4.6, 4.8–4.10 and 5.7–5.8; Theorems
6.1 and 6.11 with their internal lemmas; Sections 7.1–7.3; and Section 8's
flow correspondence and final proof. Some inputs are stated with omitted or
sketched proofs by the authors, notably Propositions 2.1–2.2 and Claim 8.22;
this packet does not supply those missing details or re-prove cited external
foundations. The theorem is used as a literature result, not certified anew.

The crucial obstruction to direct application at a zero is concrete:
$\iota_X\mu$ there is zero and has three-dimensional kernel. It does not
define the everywhere one-dimensional characteristic foliation required for
the paper's Hamiltonian-structure machinery. Restricting to the complement
of the zero set also removes the closed-manifold hypothesis.

## Search for a later resolution

Read-only searches included the exact title, ID/code, Edtmair/Seyfaddini with
helicity and singularities, fixed points and conjugacy, and Lipschitz helicity
invariance. The author's [research list](https://oedtmair.github.io/) points to
the same preprint. The
[16 January 2026 IAS seminar](https://www.ias.edu/video/topological-invariance-helicity)
and [9 April 2026 MIT seminar](https://calendar.mit.edu/event/symplectic-seminar-9)
still describe the nonsingular result. They are update checks, not substitutes
for reading the proof.

No full singular-case resolution was located. This is a bounded literature
search result, not a proof that no such result exists or a novelty claim for
the elementary restricted statements in this packet. Results about rough
weak Euler solutions, helicity uniqueness, or orientation-reversing maps do
not answer the source question under its exact hypotheses.

## Actual prior-attempt checks

Repository: https://github.com/AlecKriebel/Math . Checks on 2026-10-04 found:

- unsolved_math_prioritization/QUEUE.md, fetched blob
  c87c275c638939b8008fd58db80657491d14971e, had row 557 as queued, 0/5,
  with blank Chat and Findings cells.
- All-state issue/PR searches for 30006363, OWR-14299512-001, and helicity
  returned no matching prior PR or issue.
- Branch search for 30006363 returned no matches.
- Commit search for 30006363 returned no matches.
- Repository code searches for 30006363 and helicity returned no matching
  attempt artifacts.

Code search is not exhaustive: it did not return even the known queue row.
The prior-attempt determination therefore does not rely solely on code
search or on the word queued. No actual prior attempt was located by these
independent checks.

## Submission boundary and status

Five substantive approaches have been documented in ATTEMPT_LOG.md. The
recommended row outcome is unsolved, 5/5, meaning this investigation did
not solve the full problem. No exhausted status, script edit, or unrelated
queue-row change is requested. The default proposed queue edit affects only
this row's Status and Turns cells.

Only the files listed in the public SHA-256 manifest are proposed for
publication. They contain original mathematics, bibliography and provenance,
and small reproducible symbolic checks. No source PDF, extracted source text,
rendered page, catalogue record, corpus, private context, or tool transcript
belongs to that payload. No remote write was performed before submission for
independent review. A manifest is an integrity record, not a mathematical
validation or a resolution claim.
