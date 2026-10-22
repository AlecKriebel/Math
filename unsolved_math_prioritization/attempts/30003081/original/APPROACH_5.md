# Approach 5: depth, reflexive extension and codimension-two failure

Status: a homological sufficient criterion is proved. Its hypotheses exceed those of the original question.

In the notation of Approach 4, assume:
1. F=D_X(A) and G=D_X(A+H) are locally free on a smooth complex variety X;
2. the natural restriction G -> i_*E is onto at every point of H of codimension at most one in H.
Then it is onto everywhere, so the natural deletion sequence is short exact.

## Proof

Let C=G/F(-H), viewed on X. Multiplication by a local equation z of H annihilates C, because G is a subsheaf of F and zG lies in zF. Thus C=i_*C_H for a coherent sheaf C_H on H. The kernel theorem embeds C_H into E.

At a point of H, let O be the regular local ring of X, of dimension d, and O_H=O/(z). The sequence
0 -> O^d' -> O^d' -> (C_H)_p -> 0
has free first and middle terms of equal rank d'=dim X; the map is the specified injection of logarithmic bundles, not an arbitrary rank claim. The depth lemma gives depth_O(C_H)_p >= d-1, unless the module is zero. For a module annihilated by z its depth over O equals its depth over O_H. Since O_H is regular local of dimension d-1, Auslander–Buchsbaum implies (C_H)_p is free. Thus C_H is locally free on H.

The logarithmic derivation sheaf E of a reduced divisor on the smooth variety H is reflexive. One verification is to embed it in the rational tangent sheaf and test its tangency conditions at every height-one prime; divisibility by each reduced irreducible divisor equation is completely detected there. The resulting finite torsion-free sheaf equals the intersection of its height-one localizations, the reflexivity criterion over a normal domain.

By assumption C_H -> E is an isomorphism outside a closed subset of codimension at least two. Both sides are reflexive on normal H, so each is the pushforward of its restriction to that open subset. The map is therefore an isomorphism everywhere. This proves the criterion.

## A verified source of hypothesis 2

It suffices to assume explicitly that at the codimension-one points in question the pair (A,H) is analytically a product of a plane pair satisfying the Schenck–Terao–Yoshinaga exactness hypotheses and a smooth factor. The planar exactness extends to the product. In each extra smooth tangent direction, both ambient logarithmic modules contain the unrestricted derivative, restriction maps it onto the corresponding derivative on H, and the kernel consists of its multiples by z. This follows directly by coefficient inspection. Normal-crossing pairs satisfy hypothesis 2 directly by Approach 1.

This product assertion uses flat extension of the plane derivation modules and the elementary free-factor decomposition, not a claim that every quasihomogeneous pair has such a simultaneous product form. Alternatively hypothesis 2 may be checked directly by the obstruction map of Approach 3.

## Precise limits

Higher-dimensional logarithmic sheaves need not be locally free; quasihomogeneity does not establish hypothesis 1. Even generic restrictions that miss a codimension-two defect cannot establish global exactness without a reflexivity/depth argument. Approach 2 is a concrete warning: its nonzero defect is supported at the retained projective vertex and can disappear from a general lower-dimensional section.

For hyperplane arrangements, the stronger credited free-surjection theorem of Abe and of Abe–Denham (2026, Theorem 1.2) only assumes freeness of the deletion and handles multiarrangements with the appropriate Euler multiplicity. Their result is not newly proved here; the present elementary criterion is deliberately more restrictive. It is not a theorem about arbitrary smooth hypersurface components with only quasihomogeneous singularities.

All five substantive routes have now been used. The primary OWR task remains unresolved as a general request. The packet supplies a source correction, an explicit obstruction to a natural blanket extension, and conditional positive/defect theorems. It does not manufacture a full-resolution verdict from any special case.
