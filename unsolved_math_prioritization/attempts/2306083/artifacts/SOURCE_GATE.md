# Source and scope gate

## Target and primary statement

[Catalogue problem 2306083](https://www.unsolvedmath.com/problems/2306083), AMR-022-6083, is Hayman and Lingham's Problem 6.83, proposed by P. L. Duren. It asks for a characterization of sequences on which distinct normalized univalent functions in the disk agree.

The live catalogue request returned HTTP 403 on 2026-10-03. A pinned catalogue record was used only to identify the primary source. Generated summaries and status fields were not accepted as mathematical evidence. The exact question and its update were then read in the primary collection, including the page image.

- W. K. Hayman and E. F. Lingham, [Research Problems in Function Theory, arXiv:1809.07200](https://arxiv.org/abs/1809.07200), Problem and Update 6.83, printed p. 146 (PDF page 147). Update 6.83 explicitly points to Overholt's partial result, reference [621], identified on printed p. 240.
- M. Overholt, [Sets of Uniqueness for Univalent Functions](https://doi.org/10.4153/CMB-2000-016-x), Canadian Mathematical Bulletin 43 (2000), 105–107. The entire three-page paper, including its proof and references, was read. It supplies the reciprocal-difference Dirichlet-space reduction reconstructed in PROOF.md. Its further reported existence statements invoke older Dirichlet zero-set literature; this note does not reproduce or newly certify those subsidiary existence proofs.
- P. Lappan, [Points where univalent functions may coincide](https://doi.org/10.1080/17476938508814124), Complex Variables 5 (1985), 17–20. This related article is bibliographically confirmed by Overholt's reference list. The publisher PDF endpoint returned an HTTP 403 challenge. No theorem from an incomplete abstract or inaccessible full text is assumed. In particular, the sufficient construction here is proved in full without claiming priority over Lappan.

The downloaded primary PDFs have SHA-256 digests:

- Hayman and Lingham: `8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0`
- Overholt: `92b4b79f9f5879b3e813c8450c77f3d09e85777f78d5d797eee8dba80854a49d`

## Mathematical classification

**Partial results; the requested general characterization is unresolved in this investigation.**

The verified conclusions are a necessary Dirichlet-space condition, a sufficient weighted boundary-damping condition, a complete answer restricted to sequences in finitely many fixed Stolz regions, and two explicit obstructions to proposed converse arguments. The 2018 primary update is a historical partial-result statement. Bounded searches on 2026-10-03 did not establish a later complete solution; that negative search is not a proof of present-day open status.

The core known result is credited to Overholt. No novel solution, novelty of the restricted-class construction, or new research priority is claimed. The classical compactness theorem for S, used only to formulate the remaining separation gap, has its standard Koebe-growth/Montel/Hurwitz dependencies stated explicitly.

## Prior-work repository check

The live main-branch row at rank 529 in [QUEUE.md](https://github.com/AlecKriebel/Math/blob/main/unsolved_math_prioritization/QUEUE.md) was `queued`, `0/5`; the retrieved file blob was `24545d98c2c211548377ed2f2555d6a129abfc69`. This alone was not used to conclude that the problem had never been attempted.

All-state pull-request searches in AlecKriebel/Math for `2306083`, `AMR-022-6083`, `6.83`, and the paired terms `coincidence` and `univalent` returned no matches. A branch search for `2306083` returned no matches. Default-branch code searches for `2306083`, `FunctionTheory6.83`, and `univalent coincidence` returned no matches. These are bounded negative checks, not an exhaustive proof that no artifact could exist under another name.

## Reproduction and redistribution

Only the authored proof note, research log, source gate, status, verifier, and verifier output belong to this deliverable. Third-party PDFs, extracted text, page images, catalogue data, and repository-query receipts are not redistributed. The verification script uses exact rational arithmetic and clearly separates finite regression checks from the analytic proof. It does not purport to solve the unrestricted problem.
