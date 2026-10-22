# Bóna source convention pin

Primary source: Miklós Bóna, *Exact enumeration of 1342-avoiding permutations: a close link with labeled trees and planar maps*, arXiv:math/9702223v1, 11 February 1997, 13 pages. https://arxiv.org/pdf/math/9702223

Recovered PDF SHA-256: `025bff1c9cbf96bea53ed78545c300f986029a46f3396f2624963576bba0de85`.

Exact locations supporting the accepted draft's combinatorial inputs:

1. Page 2, Section 1.2: the source defines indecomposability using a cut with all preceding values larger than all following values. This is skew indecomposability.
2. Page 4, Definition 1: leaves have label zero; the root label is the sum of its children's labels; internal labels are at most one plus that sum. Thus no forced-root relabeling is needed to apply the draft's definitions. Other beta-tree conventions in other papers are not imported.
3. Page 6, Lemma 2: the unlabeled plane tree is put in correspondence with a132-avoider ending at its maximum. The child blocks get decreasing value intervals and are followed by the largest entry. The following reading-order paragraph describes children-first traversal, which is postorder despite the source's “preorder” terminology.
4. Page 7, Definitions 2 and3: normalization retains both the values and the positions of the left-to-right minima. Corollary1 states that normalization of an indecomposable permutation ends at its maximum.
5. Page 8, proof of Theorem1: the tree for N(p) is formed first; entries of p are placed on the same node positions; left-to-right minima remain unchanged. The next paragraph explicitly preserves that underlying shape when adding labels.
6. Page10, conclusion of the proof of Theorem1: the underlying unlabeled tree determines the left-to-right minima. Corollary2 extends to forests.
7. Page11, equation(4): the tree generating function T is the expression used in the accepted draft. The nearby incompatible closed coefficient formula is not used. The same page's decomposition proof confirms the ordered-sequence relation A=1/(1-T), independently of its mistyped expanded denominator.

The erased shape has exactly n vertices for a permutation of length n. Changing only the numerical labels cannot shift vertex count, leaf positions, traversal order, or minima positions. The author draft's leaf-depth identity is separately proved, so no tree-height-to-geometry claim is being imported without argument.
