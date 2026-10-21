# Source and status gate: weak-order growth of Grothendieck Schubert supports

Checked 2026-10-21. Queue row 1873; problem 30006522 / OWR-14299904-004.

## Decision

PASS for research on the original, general Schubert-support growth conjecture. No general solution or counterexample was verified. This is not a solved-in-literature claim. Known special cases and a recent monomial-support preprint must not be mistaken for the requested general theorem.

## Source and scope

The primary source is Anna Weigandt's contribution, joint with Judy (Hsin-Hui) Chiang, in *Enumerative Combinatorics*, Oberwolfach Reports 23 (2026), pp. 132–133, specifically Conjecture 2 on p. 133: https://doi.org/10.4171/OWR/2026/2 . The report PDF was retrieved and inspected.

Write G_w = sum_u a_u S_u and A_w = {u : a_u != 0}. The target asks whether every u in A_w with length below deg(G_w) has a left simple-reflection ascent s_k u still in A_w. The cleaned statement preserves this scope; its explicit left-order subscript is justified by the surrounding source. Repeated prose in the corpus original_statement field is extraction noise, not additional hypotheses.

The report announces the conjecture for Grassmannian permutations, shifted dominant permutations 1 x v, and inverse fireworks permutations. It does not assert the arbitrary-permutation case.

## Current literature and non-equivalences

- Mészáros–Setiabrata–St. Dizier, *On the support of Grothendieck polynomials*, https://arxiv.org/abs/2201.09452 : inspected PDF. Its support is the set of monomial exponent vectors, ordered componentwise, not the permutation indices of the Schubert expansion.
- Chou–Yu, *Grothendieck polynomials of inverse fireworks permutations*, https://arxiv.org/abs/2403.12186 : inspected PDF v2. This provides inverse-fireworks monomial-support results and top-degree formulas, not a general solution to this row.
- Nguyen-Dang–Wang, *Chern flow and Chern moment algebras*, https://arxiv.org/abs/2609.02850v4 : September 2026 preprint; inspected PDF, especially introduction pp. 1–5. It claims ordinary monomial-support augmentation and generalized-polymatroid results. No Schubert-basis left-weak growth theorem was located. This gate does not audit or certify its proof. Even acceptance of its monomial statements does not supply the missing implication to this stronger basis-dependent target.
- Weigandt, *Changing Bases with Pipe Dream Combinatorics*, https://arxiv.org/abs/2506.07306 : abstract inspected. It provides change-of-basis formulas, including Bruhat-chain formulas. This is a promising research input, not a verified solution of the left-weak ascent conjecture.
- Chiang's current public research page, https://sites.google.com/view/judy-chiang/research , lists *Schubert Supports of Grothendieck Polynomials* with Weigandt as a paper in progress. This supports the bounded status assessment; it is not evidence of nonexistence of an unpublished proof.

## Duplicate and prior-result checks

The complete supplied problems corpus contains related records 30006520 and 30006521 (the weaker existence of any larger support element) and 30006523 (left-weak interval convexity). These are related scopes, not exact duplicates of the one-step target. The first two are mutually duplicate formulations. Combining their weaker growth assertion with the convexity assertion would imply the one-step assertion, but neither is verified generally here.

There is no research_results entry under OWR-14299904-004. A broad full-corpus phrase search returned three unrelated geometric representation-theory records; inspection ruled them out. The workspace filename scan found no pre-existing package for ID30006522. These are bounded duplicate checks, not a guarantee about every historical artifact.

## Research acceptance boundary

A valid solution must address every permutation, preserve Schubert-basis support rather than substitute monomial support, and produce a length-increasing left simple reflection for every non-top support element. A finite computation is evidence only. Known structured-family cases are not new resolution. A new special case should be explicitly labeled partial progress.

No publication or QUEUE edit was made. Copied source PDFs, extracted text, and corpus records are excluded from public deliverables.
