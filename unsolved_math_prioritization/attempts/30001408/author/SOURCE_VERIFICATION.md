# Source verification and scope

Checked 2026-10-05 UTC. This file contains public bibliographic information, public metadata, and authored verification conclusions. No source PDF, extracted text, image, dataset contents, or private coordination material is part of the publication packet.

## Primary target

- Matthias Reitzner, contribution *Affine invariant notions of surface area*, in *Mini-Workshop: Valuations and Integral Geometry*, Oberwolfach Reports 7 (2010), 141–178; relevant printed pages 147–150, especially final paragraph of p.149.
- Workshop DOI: https://doi.org/10.4171/OWR/2010/04
- Publisher landing page: https://ems.press/journals/owr/articles/4199
- Public PDF: https://ems.press/content/serial-article-files/46262?nt=1
- Downloaded 371935 bytes; SHA-256 d1aa8950672dd8217eef08eba7911e43ed3056c63eee68b889e0655aa7066b6f.
- Inspected the contribution's full relevant text and references. Visually inspected printed p.149. The target word is upper-semicontinuous. The range is R^+ union {infinity}, with no zero subscript. Neighboring conjectures and additional questions were distinguished rather than bundled into this ID.

## Published finite-valued dependency

- Monika Ludwig and Matthias Reitzner, *A classification of SL(n) invariant valuations*, Annals of Mathematics 172 (2010), 1219–1267.
- DOI: https://doi.org/10.4007/annals.2010.172.1219
- Publisher page: https://annals.math.princeton.edu/2010/172-2/p09
- Public publisher PDF: https://annals.math.princeton.edu/wp-content/uploads/annals-v172-n2-p09-p.pdf
- Downloaded 1659946 bytes; SHA-256 8e0a5459d4695ec7adc783b75a0317d57a46df8666da774dc9d29d357ccdd739.
- Inspected Theorems 3–5, surrounding definitions, discussion of the domain/dissection obstacles, and the complete Section 5 derivation of Theorem 4 from Theorems 26 and 5. Visually inspected printed pp.1221 and 1262. In particular, the degree exponent is (n-q)/(2n), and the power relation is p=n(n-q)/(n+q).
- This packet invokes the published finite-valued theorem. It does not claim to have reconstructed or independently validated every lemma in its long proof. The real-valued codomain is an essential scope limitation. No theorem concerning complex-valued, continuous, translation-invariant valuations was substituted.

## Cited extended-valued comparison and curvature bound

- Monika Ludwig, *General affine surface areas*, Advances in Mathematics 224 (2010), 2346–2360.
- DOI: https://doi.org/10.1016/j.aim.2010.02.004
- Public author manuscript: https://dmg.tuwien.ac.at/ludwig/gasa.pdf
- arXiv record: https://arxiv.org/abs/0908.2191
- Downloaded author PDF: 191681 bytes; SHA-256 7cb757d6a56d933013af123d794bf2283254795ce67c156344d8ca5f64fb2d16.
- Inspected the introduction, Theorems 1–2, 6 and 9, Corollaries 7 and 11, definitions of the three surface-area families, the curvature-measure identity/inequality (10), (16), (17), and Section 6's Conjectures 1–2. Visually inspected manuscript p.14. Those conjectures use lower semicontinuity. The OWR upper/lower discrepancy is real and is retained as unresolved source context.
- The author manuscript's introduction has a homogeneity formula with an apparent first-factor typo; this packet does not copy it. Homogeneity was derived directly from dilation and checked against the publisher's Annals statement and proof.
- Full verification of the difficult lower-semicontinuity proof is unnecessary for the exclusion used here: the manuscript gives infinity on polytopes and finiteness on balls, and the opposite upper-semicontinuity obstruction is proved directly in RESULT.md.

## Later survey/status check

- Monika Ludwig, *Geometric valuation theory*, public author manuscript: https://dmg.tuwien.ac.at/ludwig/GeoVal.pdf
- Downloaded 305904 bytes; SHA-256 42565f6895581c49bbe363ba928eaa626a5b06f0bb9b6385ffcbd9b5a532fb96.
- Inspected the affine scalar-valuation sections and the finite real-valued Theorems 2.4–2.7. The survey combines the finite polytopal theorem of Haberl–Parapatits with Ludwig–Reitzner to remove homogeneity for finite real-valued valuations. That update does not supply the extended-valued classification required here.
- Targeted web searches for the exact classification, extended-valued valuations, upper/lower semicontinuity, infinity, and the cited conjectures did not identify a subsequent theorem resolving the literal target. Search snippets and papers on other valuation domains were not treated as solutions. This is a scoped search result, not a definitive declaration that no later result exists.

## Catalogue, queue, and prior-attempt checks

- The problem landing URL https://www.unsolvedmath.com/problems/30001408 was attempted through web retrieval and direct read; it was unavailable (direct HTTP 403). No access denial was circumvented.
- The public repository catalogue's selected record supplies ID 30001408 / OWR-4199-001, title, DOI, and rank 696. Its prior machine assessment is planning context, not evidence of a theorem.
- A live repository read of unsolved_math_prioritization/QUEUE.md showed the target queued at 0/5. Observed Git blob SHA: 5d33a968894980499cb3fbb6d84fe5cca5a47aa4.
- The live attempts tree at SHA 5c2ab378a9489c4b49c1ccbf87ce85ff5b7d5393 was untruncated and had no directory named 30001408.
- GitHub code, PR, and commit searches for the exact ID, a PR search for OWR-4199, and a broader valuation PR search found no existing attempt for this target. Search indexes and branch coverage are limited; absence of a hit is not proof of absolute absence.
- The repository related-target groups file was inspected and did not contain this target or OWR-4199.
- Prior conversational-context retrieval produced no verified actual earlier attempt on this target; most retrieved items explicitly concerned other IDs. It was not treated as an authoritative duplicate check.
- The selected upstream AI report and full upstream problem/research corpora were not inspected in this attempt. No full corpus was downloaded. The primary statement governs the mathematical target; no byte-verification claim is made for uninspected corpora or report text.

## Proof and verification limits

All new propositions have complete authored proofs in RESULT.md. Published geometry is explicitly credited where used. There is no complete n>=2 classification or certified mixed-infinity example. The exact finite controls check endpoint/Boolean/exponent identities and rejected constructions; they do not validate arbitrary convex bodies by sampling. Fresh independent review remains required before remote publication.
