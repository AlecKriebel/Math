# Positive pressing-connectivity appendix

This appendix supplements [the pressing normalization report](../3100089/README.md) for database problem 3100089 (AMR-030-0089) in [draft PR #1313](https://github.com/AlecKriebel/Math/pull/1313). It contains complete authored proofs and independent correctness audits of several positive structural results. No novelty or general-conjecture resolution is claimed.

## Results and exact hypotheses

Let A be any symmetric n-by-n matrix over F_2 with rank r, and assume it admits a successful pressing word. A legal press at v requires M_vv=1 and changes the full current matrix to M+(Me_v)(Me_v)^T. A successful word ends at the zero matrix. Every successful word has length r.

The successful-word graph here joins distinct words S,T when LCS(S,T)≥r−4: at most four deletions and four insertions, or eight insertion/deletion edits in total.

1. **Every rank:** any vertex with nonzero original row can replace the pivot at its last nonzero Gram–Schmidt coordinate, preserving every full matrix state. Each exact trajectory fiber is precisely a Cartesian product of disjoint nonempty layers. Single-position replacements connect each fiber.
2. **Rank at most five, arbitrary n:** the original-bound successful-word graph is connected. It is complete for r≤4 and has diameter at most two for r=5. Rank-deficient matrices and words omitting different vertices are included.
3. **Every pair of realized trajectories:** the greatest achievable LCS between their fibers is exactly the longest strictly increasing chain of nonempty layer intersections. For distinct trajectories this gives the exact quotient-edge criterion.
4. **Every rank under a strong additional hypothesis:** if every norm-one vector of V=F_2^n/ker(A) is the image of an actual original coordinate vertex, the original-bound successful-word graph is connected. Successful-word existence remains an explicit hypothesis. A proved generation lemma connects ordered orthonormal bases using swaps and four-position sum-of-the-other-three moves. Richness makes every intermediate basis representable by original labels.

The fourth hypothesis is representation of **every** norm-one quotient vector. Merely spanning the quotient does not suffice for this proof. Extra zero, repeated, and norm-zero coordinate images are allowed. No unproved transfer through congruence or unordered feasible-set exchange is used.

## Relation to the earlier counterexample

The parent report's six-vertex, rank-six example has exactly two successful words at insertion/deletion distance eight. It disproves the stricter combined budgets four and six, while its two words are adjacent at the original Bixby–Flint–Miklós bound. The positive results here use that original bound, so they do not conflict with the counterexample. Neither packet resolves the general original conjecture. The existing eight-file normalization packet is preserved byte-for-byte; this appendix is an addition in its own sibling directory. The original closed-directory manifest remains valid because no files or subdirectories are added inside 3100089/.

## Proofs, audits, and verification

- [Structural proofs](STRUCTURAL_LEMMAS.md): complete accepted Sections 1–4, with a short scope/source appendix.
- [Inter-fiber proofs](INTER_FIBER_LEMMAS.md): exact LCS identity, elementary orthogonal generation, and conditional all-rank connectivity.
- [Structural audit](STRUCTURAL_AUDIT.md) and [inter-fiber audit](INTER_FIBER_AUDIT.md): complete independent mathematical reconstructions and bounded-check descriptions.
- [Acceptance](ACCEPTANCE.json): exact accepted claims, hypotheses, and limitations.
- [Verification metadata](VERIFICATION.json): bounded scopes, aggregate counts, fresh three-mode reruns, and byte/hash pins.
- [Source metadata](SOURCE_METADATA.json): public primary citation, normalization inspection, and PDF pin; no copied source document.
- [Editorial mapping](EDITORIAL_MAP.json), [scope review](SCOPE_REVIEW.md), and [closed manifest](MANIFEST.json): exact edition relationship and publication boundary.

The mathematical review is AI-assisted and unrefereed. It is not external human peer review or proof-assistant certification. The finite computations corroborate complete proofs; they do not establish general connectivity by experiment. Executable checkers and raw outputs are excluded, so the public packet does not claim to be a self-contained executable reproduction bundle. No new comprehensive literature review is claimed.
