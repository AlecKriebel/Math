# Changelog

## Displayed-tree clarification revision -- 12 August 2026

This is a clarification and verification revision. No mathematical parameter or conclusion changed.

- Assigned `S` explicitly to both arcs `p->r2` and `p->r3` everywhere the construction is introduced.
- Assigned `T` explicitly to both arcs `q->r2` and `q->r3` everywhere the construction is introduced.
- Replaced the inaccurate description "four pendant rooted edges" with "four common K-edges" in the technical summary. The distinct phrase "suppressed pendant edge" remains where it correctly describes the effective leaf-1 edge after root suppression.
- Derived the common Fourier factor `K_x K_(y+z) K_y K_z = K_x^2 K_y K_z` from the labelled descendants of the four `K`-edges.
- Added the complete four-switching table and derived the four terms defining `M` from the retained parents at `r2` and `r3`.
- Added `verify_k2p_displayed_trees.py`, which literally deletes the unselected incoming reticulation arcs and reconstructs descendant sets, edge labels, and monomials from graph data.
- Added an independent exact ordinary-state pruning check for the simple `Q(sqrt(71))` witness. It compares all 64 network probabilities with the comparison tree, Fourier inversion, and the stored certificate.
- Recorded the exact source-convention cross-check reproducing all five displayed Fourier coordinates in Lemma 4.1 of arXiv:2607.12919v2.
- Corrected the technical summary's edge placement, common-edge terminology, K3P reuse of `M`, replay instructions, and public-status wording.
- Corrected confidentiality and notification language to match the public repository and recorded the pre-clarification public history without rewriting it.
- Added diagnostic fingerprints `M_(A,C)=151/1440` and `M_(C,C)=71/1600`.

Unchanged results include the simple and strict continuous-time K2P witnesses, the matrix `M`, factors `P` and `R`, comparison-tree vectors, minimum pattern probability, induction-order diagnosis, K2P rank and collision-family results, the K3P witness, the K3P rank/Jacobian calculation, and the analytic continuous-time K3P extension.
