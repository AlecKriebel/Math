## Credited negative answer

This draft publishes an AI-assisted audit of Alper Ferudun's prior negative answer to Heinig's spanning near-square question, corpus problem 30002470 / OWR-12861-021. Ferudun's version 1.0 is dated 28 September 2026 and is an unrefereed preprint.

The nine-vertex host K_{4,4,1} has minimum degree 5 and excludes C_9² minus every three-edge matching. The authored audit supplies a complete elementary triangle-cover and odd-cycle proof of that stronger claim, already stated in Ferudun's Remark 3.5. Because every deletion yielding the specified target degree sequence is a three-edge matching, the original universal statement is false regardless of the unresolved meaning of “periphery.”

The audit also verifies Ferudun's construction for every odd n ≥ 7 under the two explicitly defined periphery readings R1 and R2. It makes no negative claim about the separate Hamilton-generated cycle-space question.

## Sources and reading limits

- Alper Ferudun, [Dirac Graphs Without a Spanning Near-Square of an Odd Cycle: A Negative Answer to a Question of Heinig](https://zenodo.org/records/23004012), DOI 10.5281/zenodo.23004012, version 1.0, 2026-09-28. All five PDF pages were read in text; pages 2–4 were visually inspected. PDF: 86,693 bytes; SHA-256 `02ea0f37da91ece4bf3dcab399ef2dbe52f891b5cddc649ab3845ce3efed6824`.
- Peter Heinig's Question 2 in [Combinatorics, Oberwolfach Reports 11 (2014), Report 01/2014](https://ems.press/content/serial-article-files/46491), DOI 10.4171/owr/2014/01. Question 2 and the adjoining Question 1 were inspected; PDF page 78, printed page 82, was visually inspected. The whole workshop report was not audited.
- Peter C. Heinig, [On prisms, Möbius ladders and the cycle space of dense graphs](https://arxiv.org/abs/1112.5101v1), arXiv:1112.5101v1. Definition 28, Figure 4, Proposition 30 and adjacent discussion on printed pages 30–31 were inspected. This was not a full article or journal-version re-audit.

SOURCE_MANIFEST.json records public versions, PDF sizes and hashes, retrieval history, dataset hash/match metadata and precise inspection limits. The claimant's deposited verification report was read as claimant-reported history. Its external-review claims and computational runs were not adopted as independent evidence.

## Verification and limitations

The audit records independently authored finite checks under normal, -O and -OO modes: structural checks for odd orders 7–51, direct embedding checks for orders 7, 9, 11 and 13, positive controls, and all 177 three-edge matchings with all nine deleted-vertex choices. These supplement the complete analytical proofs. The checker and raw enumeration output are excluded from this prose/metadata edition, so those computational runs cannot be replayed from these three files alone.

Our review is AI-assisted internal mathematical verification, not external human peer review or formal proof-assistant certification. Credit for the counterexamples and prior nine-vertex claim remains with Ferudun. No first-solution, novelty or absolute-priority claim is made. The claimant's SAT runs, small-order optimal-threshold enumeration and broader cycle-space literature status were not independently reproduced.

## Exact publication scope

Exactly three files, totaling 22,061 bytes, are added under unsolved_math_prioritization/attempts/30002470/:

- MATHEMATICAL_AUDIT.md: 13,149 bytes; SHA-256 `1153d35a02a720b787d10fab963d14b4429e3197e73ecb56e58c9010aebf71c8`.
- ACCEPTANCE_REPORT.json: 2,894 bytes; SHA-256 `a5652acb4d882ceea8a81d4508640d39f5973ad3775db4e8a6fa34d5ef567d9d`.
- SOURCE_MANIFEST.json: 6,018 bytes; SHA-256 `9987ca87655c54ea086f6fde77a0da7e6a249c79f1b48f5ee771ad24481c81de`.

Base commit: `4b27092a448d53b61408355ce44ec38d103a1ce4`. QUEUE.md, main and unrelated paths are unchanged. Source copies, source text, dataset contents, code, raw enumerations and private coordination material are excluded. Draft only; no merge, release or outreach.
