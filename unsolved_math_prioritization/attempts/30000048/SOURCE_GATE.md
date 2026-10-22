# Exact source gate: positive virtual characters

Problem 30000048 / OWR-722-001, queue rank 315. 2026-10-01. Source-only checkpoint, 0/5 substantive author turns.

## Original target

Jean-Pierre Serre, *On the values of the characters of compact Lie groups*, OWR 12/2004, printed pp. 666–667, §2, asks the following. Let G be a connected simply connected compact Lie group and f a virtual complex character, meaning a finite integer linear combination of characters of finite-dimensional continuous complex representations. Assume f(g) is real and nonnegative for every g in G, and its integral against Haar measure of total mass one is 1. Must f equal chi times its complex conjugate for some irreducible complex character chi of G?

Virtual coefficients may be negative. Pointwise nonnegativity is not positive-definiteness or nonnegative irreducible coefficients. The normalization is Haar mean one, not degree one or L2 norm one. Zero values are allowed. G need not be simple; products of simply connected simple compact groups are included. A torus is compact and connected but is not simply connected unless trivial. The trivial group has only f=1 and causes no difficulty. Counterexamples for disconnected finite groups or for non-simply-connected quotients would not settle the question.

The complete two-page original contribution was read, both as an author-hosted PDF and within the full official report; the precise positivity and rank-one statement were visually checked. It already announces the affirmative answer for SU(2), with a trigonometric-polynomial hint. That special case is known prior work, not a new campaign result.

## Current primary source and full rank-one proof

Serre's final *Zéros de caractères*, L'Enseignement Mathématique 71 (2025), 433–457, DOI 10.4171/LEM/1095, published June 16, 2025, revisits the issue. Sections 4–5 were read in full. Definition 4.4, printed p. 446, calls such virtual characters S-characters; the nonnegative glyph was visually checked because text extraction renders it as a strict greater-than sign.

Problem 4.6 asks the connected-group version, allowing the irreducible character on a connected finite covering group. For a simply connected G, a connected covering is trivial, so this includes the exact 2004 target. The source explicitly retains it as a problem. The example for SU(n)/N explains why the covering qualification matters outside our hypotheses. Finite-group counterexamples in the adjacent prime-power-zero Problem 4.10 concern a different statement.

Proposition 4.8, proved as Proposition 5.8 on pp. 450–451, establishes the SU(2) case. Its input is the extremal coefficient bound and equality case for nonnegative one-variable integral Laurent polynomials, Proposition 5.2 and Corollary 5.4, pp. 448–449. Multiplication by the rank-one Weyl density gives constant Laurent coefficient 2; equality forces the square of a rank-one irreducible character. These exact definitions, signs and the full proof are the starting source inputs, not an assumed general-rank factorization theorem.

The same final paper proves that a connected torus has no S-character other than 1, but that is not the higher-rank simply connected semisimple case. Targeted later searches found work on finite-group S-characters and on adjoint trace bounds; those do not resolve this classification question. This bounded check is not a certification of worldwide status beyond the explicit 2025 source.

## Prior campaign gate and success condition

Exact ID, source code and title PR searches were empty; target branch search and both main attempt-directory histories were empty. The local all-ref target history is empty. The complete pinned imported record was read; its attached prior report is empty, and related-target-group screening found no match. The upstream literature paragraph is not an earlier Alec campaign proof attempt.

A full affirmative result must cover every connected simply connected compact Lie group under the stated virtual/pointwise/Haar conditions. A negative answer needs an explicit such group and virtual character with a rigorous global nonnegativity certificate, exact Haar mean one, and proof that no irreducible square has that character. Grid positivity, rank-one verification, finite-group examples or a non-simply-connected quotient are insufficient.

Five substantive author turns remain available. Independent full review is required before any result PR. Repository-required completion estimate at this source checkpoint: 10%, subjective and uncalibrated; not a probability of correctness or a user-facing verdict.
