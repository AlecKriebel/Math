# Hochman's first Pingree problem: negative answer already in the literature

## Exact scope

Let X = {0,1}^Z and let Y be the subset of {0,1,2}^Z whose adjacent coordinates are unequal. Both alphabets are discrete; the ambient sequence spaces have the product topology. On both spaces use the left shift, (sigma z)_i = z_{i+1}. For either space Z, define

Per(Z) = {z in Z : there exists an integer n >= 1 with sigma^n z = z},

and give Z* = Z \ Per(Z) the subspace topology. The question is whether there exists a homeomorphism h : X* -> Y* satisfying h sigma = sigma h everywhere on X*. In particular, both h and its inverse must be continuous. These are two-sided sequences. Only periodic points are removed; nonperiodic points with periodic tails remain. No invariant measure or ergodicity assumption is imposed.

The exact problem is Mike Hochman's item 1 on page 1 of the 22 November 2010 Pingree list [P]. The additional measure-theoretic remarks there do not weaken this topological question. The appearance of “Pre” in its final remark does not change the explicitly defined Per in the question.

## Established input

Use Ville Salo's extension theorem, Theorem 1 of [S], published page 1683: for any two infinite transitive two-sided shifts of finite type, a shift-equivariant homeomorphism of their nonperiodic parts extends uniquely to a shift-equivariant homeomorphism of the full shifts. This is an existing theorem, not a new lemma claimed here. Its two-sided proof is in Section 3, pp. 1685–1687. The paper explicitly discusses the present binary and proper-three-coloring example on p. 1682.

## Complete deduction for the exact target

1. X and Y are shifts of finite type. X has no forbidden words. Y is specified by the three forbidden words 00, 11, and 22. Their adjacency matrices are

A = [[1,1],[1,1]],
B = [[0,1,1],[1,0,1],[1,1,0]].

2. They are infinite. In X, all binary words occur. In Y, there are 3 times 2^(n-1) words of every positive length n: the first coordinate has three choices, and each subsequent coordinate has two. Each such finite proper word extends indefinitely to both sides, since there are two permissible next symbols at every step. Thus the numbers of admissible words in both systems grow without bound, ruling out finite systems.

3. They are topologically mixing, hence transitive. For X any two finite words can be joined across any prescribed gap. For Y, B^2 = [[2,1,1],[1,2,1],[1,1,2]] has every entry positive. Moreover, multiplication of a strictly positive matrix by B remains strictly positive: each entry is a sum of two positive entries. By induction every B^m for m >= 2 is positive. Its (a,b) entry counts paths of m transitions from a to b, by induction on m using matrix multiplication. Consequently, for any two allowed words and any sufficiently long intervening gap, one can connect their endpoint symbols through a path of the needed length. The resulting concatenation is allowed. This is the cylinder-set mixing criterion and proves the required transitivity directly.

4. Suppose that h as in the question existed. The hypotheses in steps 1–3 permit applying Salo's theorem, so h extends to a conjugacy H : X -> Y.

5. If x is fixed by sigma, then sigma H(x) = H(sigma x) = H(x). Thus H sends fixed points of X to fixed points of Y. But the two constant binary sequences belong to X and are fixed, whereas every shift-fixed sequence over three symbols is constant and violates Y's adjacent-inequality condition. Hence Y has no fixed point. This contradiction proves that the requested h does not exist.

This settles every quantifier of Hochman's item 1 negatively, conditional only on the cited established extension theorem. It is a prior-literature resolution, not a novel proof of that theorem. No missing mathematical statement remains for this exact problem.

## Checks and distinctions

The shared entropy is consistent with the original premise: for n >= 1, the language counts are 2^n and 3 times 2^(n-1), respectively; (1/n) log of either tends to log 2. Equal entropy alone does not supply a conjugacy.

For any n >= 1, the counts of points fixed by sigma^n in the full systems are trace(A^n) = 2^n and trace(B^n) = 2^n + 2(-1)^n. Indeed a point fixed by sigma^n corresponds bijectively to its first n symbols with the extra wrap-around transition; the adjacency-matrix trace counts exactly those closed walks. The eigenvalues of A are 2 and 0; those of B = J_3-I_3 are 2, -1, -1, proving the formulas. These are counts of period dividing n, not of least period n. In the nonperiodic parts both fixed-point counts are zero for every n, so applying this obstruction directly there would be invalid. The extension theorem is the essential bridge.

A uniform finite-window rule for an arbitrary continuous map on a noncompact subspace has not been assumed. Nor is a merely Borel isomorphism, continuous bijection, continuous injection, or continuous surjection substituted for a homeomorphism. The conclusion here is not asserted for different deletion sets, arbitrary sofic shifts, or any adjacent question in the Pingree list.

The finite tests independently check adjacency identities, legal words, closed walks, least-period arithmetic, and relabeling controls. They do not verify the infinite-space extension theorem. The mathematical proof is the deduction above, not a numerical extrapolation.

## References

[P] Open Problems, 3rd Pingree Workshop on Dynamical Systems, 22 November 2010, Mike Hochman, problem 1, p. 1. https://math.huji.ac.il/~mhochman/open-problems/pingree-open-problems.pdf

[S] Ville Salo, Conjugacy of transitive SFTs minus periodic points, Proceedings of the London Mathematical Society (3) 127 (2023), 1681–1692. Theorem 1, p. 1683. https://doi.org/10.1112/plms.12567

[S-preprint] https://arxiv.org/abs/2104.09860v3 (first submission 20 April 2021; v3 22 September 2023).
