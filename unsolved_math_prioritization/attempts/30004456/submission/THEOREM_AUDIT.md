# Theorem-application and adversarial ledger

## Scope checks

1. Original source: Gardam's *Computing fibrings*, joint work with Kielak, OWR 16/2020, pp. 898–900, conjecture on p. 899. The page was checked as PDF pixels. Its minimization is over the base group A, not over a rank of an assumed free edge group.
2. Resolving source: arXiv:2606.31774v2, title/authors/version checked against the current arXiv record and the PDF. Corollary 1.5 on PDF p. 3 was checked visually. The authors themselves identify the Gardam–Kielak problem on p. 2.
3. Group hypotheses: finite-rank free-by-cyclic implies torsion-free, finitely presented, and b₁⁽²⁾(G)=0. Index one meets “virtually.” No atoroidality, hyperbolicity, geometric monodromy, or one-relator hypothesis is introduced.
4. Character hypotheses: nonzero is explicit in JKS. Primitive normalization changes neither kernel nor admissible normalized splittings. Zero is outside the intended conjecture; the catalogue omits that qualifier.
5. Euler hypotheses: finite generation alone does not generally imply an Euler characteristic is defined. Here Feighn–Handel Theorem 1.2 gives finite classifying spaces, so the conversion is justified.
6. Infinite kernels: the proof uses degreewise higher L² vanishing for arbitrary subgroups and never assumes finite generation of the kernel or finite first Betti number of S∩F_n. Finiteness of b₁⁽²⁾(ker φ) comes from the attaining JKS splitting.
7. Base/edge mismatch: JKS Theorem 3.3(ii) squeezes the base value between the equal kernel and optimal edge values. The graph-of-spaces Euler identity is a separate cross-check.
8. Boundary n=0: G=Z, trivial kernel and base, and both requested Euler quantities equal −1; b₁ by itself would miss b₀(1)=1. Rank n=1 is retained and includes both automorphisms of Z.
9. Attainment: Corollary 1.5 supplies a finite-generation splitting; this is not an inference that an arbitrary infimum is attained.
10. Credit/status: the public arXiv record gives v1 on 30 June 2026 and v2 on 31 August 2026. The author's publications page lists it under preprints. No publication or peer-review status is invented.

## Noncircular proof architecture inspected in JKS

- Theorem 3.3(ii), pp. 12–16: augmentation-ideal sequence for a dual HNN splitting; kernel expressed as a directed union of finite lines of conjugate base groups. Its conclusions are inequalities for arbitrary admissible splittings, without assuming optimality.
- Theorem 1.3(ii), pp. 16–17: choose minimal edge b₁; an edge not L²-compressed has a finitely generated overgroup with smaller b₁. Enlarge the base by its stable-letter conjugate. The explicit mutually inverse maps verify that the changed HNN presentation still describes the same G. This avoids merely assuming an improvement exists. The second edge embedding is treated with the reversed orientation.
- Theorem 1.4, p. 31: a finitely generated L²-closure is supplied by Theorem 7.7 and Corollary 7.6. The relevant first module Betti number equals the difference between H's and its closure's first group L²-Betti numbers. Compression forces this nonnegative number to vanish.
- Theorem 7.7, pp. 29–31, has deep ring-theoretic inputs from Sections 5–7 and the cited subgroup-rigidity literature. These are stated dependencies, not results independently re-established by this packet.
- Corollary 1.5's proof on p. 31 assembles Theorems 1.3 and 1.4. It is a theorem of the preprint, not a conjectural assumption or just an abstract announcement.

The packet's logical dependence on the general theorem is explicit. The complete elementary application in PROOF.md is what is independently checked here; accepting the underlying literature theorem is the ordinary theorem-reuse step.

## Rejected false shortcuts

- Do not regard the catalogue's August 2026 “open” label as a proof of current status.
- Do not extrapolate the older two-generator one-relator result to all free-by-cyclic groups.
- Do not assume all finitely generated subgroups, or all character kernels, are free.
- Do not identify a homogeneous norm at dφ with the unscaled Euler invariant of ker(dφ).
- Do not insert φ=0 into a theorem explicitly quantified over nonzero characters.
- Do not claim a fresh solution on the strength of a theorem already posted in June 2026.
- Do not treat a finite collection of direct-product graph checks as a proof for arbitrary automorphisms.

## Remaining limitations

No mathematical gap remains in the application to the normalized nonzero-character target, conditional on the accurately cited literature results. A full independent referee-style verification of all external foundations of JKS is not claimed. The zero-character catalogue wording must be disclosed whenever an “already_solved” outcome is used. Searches did not produce a correction invalidating the cited theorem, but the searches are not an exhaustive proof that no such correction exists. Fresh independent package review and root acceptance were pending when this packet was frozen.
