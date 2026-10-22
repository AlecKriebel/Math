# Checkable antecedent comparisons for PR 1094

Written 2026-10-14 UTC. These arguments compare the exact compact-support target with actual prior theorem interfaces. They do not prove historical firstness, and they do not replace the independently accepted general construction.

## 1. The necessary direction is a prior corollary

Let L be a smooth compactly supported real Nijenhuis operator on R^n. Identify R^n with a sphere chart and extend L by zero near infinity. Since the support is compact, this extension is smooth on S^n and remains Nijenhuis by locality. A nonreal eigenvalue would contradict the zero-point obstruction supplied by Bolsinov–Konyaev–Matveev's local splitting and holomorphic maximum-principle mechanism, as used in their [author-v2 Theorem 6.1](https://arxiv.org/abs/1903.04603v2), pp. 41–43. This necessity, together with the real semisimple and two-dimensional Jordan cases, is already credited in the [original problem](https://arxiv.org/abs/1804.03737v2), Problem 5.11 p. 29. It cannot be claimed as a new contribution here.

The application-level justification recorded by the two mathematical families avoids the source's imprecise final polynomial-reduction sentence. A point with maximal positive imaginary part and maximal cluster multiplicity admits a separated complex block. The imaginary part of its holomorphic trace reaches its maximum there, hence is constant nearby. All cluster roots then have that maximal imaginary part; after shifting by that imaginary constant, the characteristic polynomial has real coefficients which are also holomorphic, hence constant. The maximal-cluster locus is open and closed, contradicting a zero point on connected S^n. This does not claim that the publisher PDF was independently certified or that every part of the source's stronger constancy theorem was reproved in this audit.

## 2. A direct product does not supply compact support

On a product of coordinate domains, a block sum L_1(x) ⊕ L_2(y) of Nijenhuis fields depending only on their own variables is again Nijenhuis: mixed coefficient derivatives vanish, and torsion restricts to the separate blocks. This is the basic mechanism behind the spectral splitting/gluing literature, including [Bolsinov–Matveev](https://arxiv.org/abs/0904.0535), Theorem 4 and formula (10), and [BKM](https://arxiv.org/abs/1903.04603v2), Theorem 3.1.

Even if L_1 and L_2 have compact support in their respective Euclidean factors, the block sum is nonzero at every (x,y) with L_1(x) ≠ 0, regardless of y. Its support contains an unbounded cylinder when the other factor is Euclidean. Thus direct sums of known two-dimensional compact examples do not automatically prove the all-block same-dimensional compact-support theorem. Compact angular directions plus a verified transverse transition supply a separate argument. Metric gluing also imposes nondegeneracy and disjoint spectra in its stated setting; those hypotheses do not persist through the candidate's zero end bands and deliberate eigenvalue collisions.

## 3. Fixed spectral calculus cannot create Jordan blocks from semisimple examples

For a diagonalizable matrix D and a fixed polynomial or analytic function p, write D = S diag(d_i) S^-1. Then p(D) = S diag(p(d_i)) S^-1 is still diagonalizable, even when some values p(d_i) coincide. Therefore the polynomial/analytic functional calculus in [BKM Proposition 3.1](https://arxiv.org/abs/1903.04603v2), or the earlier [Bolsinov–Matveev Lemma 6](https://arxiv.org/abs/0904.0535), cannot turn previously known semisimple compact-support examples into nontrivial Jordan blocks. Functional coefficients depending on the base point require additional differential conditions; the cited fixed-calculus closure theorem does not remove them.

## 4. Local normal forms do not supply a zero transition

The [BKM author-v2 Theorem 4.5 and following remark](https://arxiv.org/abs/1903.04603v2), pp. 27–28, already give local arbitrary-type realizations at points, without assuming gl-regularity of the whole operator. The construction uses block companion matrices with functionally independent characteristic-coefficient coordinates. It is generically semisimple with distinct eigenvalues. A repeated-root/Jordan condition forces discriminant equations on those coordinates, so its occurrence at points does not supply that nonsemisimple type throughout a nonempty open domain. Even the weaker point realization still has no compact-support transition. This prior arbitrary-type observation must not be presented as a discovery of the candidate.

The [published Geometry III Theorem 1.10](https://ems.press/content/serial-article-files/40231), printed p. 161, and its proof on pp. 172–174 realize **regular** spectral layers near a nonzero nilpotent Jordan block J_0. The proof uses first companion matrices, whose superdiagonal entries are 1. Such matrices are cyclic and cannot be zero in dimension n > 1. The corresponding author-v1 locator is Theorem 1.4, not journal Theorem 1.4. The regular-layer result allows one block per eigenvalue, while the target also allows arbitrarily many blocks at the same eigenvalue.

A nonzero real-analytic tensor cannot have a zero open end band on a connected analytic domain: apply the identity theorem to each analytic coordinate coefficient. Consequently analytic local descriptions require a separate smooth globalization step. Reordering blocks, reversing a Jordan-chain convention by a constant frame permutation, or changing the numerical real eigenvalues does not eliminate that requirement.

Likewise the constant-invariant-factor hypotheses in [Thompson's Theorems 1–2](https://dml.cz/handle/10338.dmlcz/133948), [Boubel's Theorem 1.3 and Corollary 1.5](https://arxiv.org/abs/1003.0979v5), and [Derdzinski–Piccione–Terek's Theorem B](https://arxiv.org/abs/2407.04539v3) cannot hold throughout a connected domain containing both a prescribed nonzero matrix and a zero open set. If a tensor is parallel for any connection, parallel transport conjugates its values; a zero value forces it to vanish on that connected domain. These theorems are important antecedents for local Jordan frames, not a compact-support extension theorem.

## 5. The symmetry theorem is not dismissed merely because its generator is regular

[Geometry IV](https://arxiv.org/abs/2304.10626v1), Theorems 1.2 and 1.4, genuinely allows a symmetry M of a fixed gl-regular generator to be singular or zero. Its formulas use functions of one variable, but their functional coefficients obey symmetry equations. They are not arbitrary compactly supported coefficient choices.

For its constant nilpotent generator N and the local Toeplitz coordinate field U, Theorem 1.4 gives M = f_1(U) N^(n-1) + ... + f_n(U). On a size-three nilpotent example with f_3 = 0, the first superdiagonal is f_2(u^3), while the next one includes u^2 f_2'(u^3) + f_1(u^3). The latter is not periodic in an angular coordinate u^2 unless f_2' = 0. Thus directly replacing that local coordinate by a circle coordinate does not make the formula a global tensor on a torus collar. This is an obstruction to this **specific proposed immediate implication**, not a theorem that no other use of the symmetry framework could produce compact support.

The [2026 Frobenius-algebra paper](https://arxiv.org/abs/2604.03195v1), Theorems 3–4, retains the common-strong-symmetry conditions and supplies local formal/analytic parametrizations. Its smooth qualification in Remark 4.2 does not assert arbitrary smooth global coefficient freedom. The full compact-support classification was not derived from those interfaces. The broader historical relationship of the candidate's one-variable ansatz to symmetry constructions remains unknown.

## 6. Haantjes cutoff freedom is weaker than the required condition

The [2026 Haantjes paper](https://arxiv.org/abs/2606.04985v1), Theorems A–B and Example 1.1, permits arbitrary smooth functional coefficients in a Toeplitz polynomial of a constant Nijenhuis matrix, with **Haantjes** torsion zero. It does not conclude Nijenhuis torsion zero for those arbitrary coefficients.

For a concrete comparison, take L(t) = f(t) J_4(0), with t the fourth coordinate and J_4 in upper-superdiagonal convention. Its angular block is A = f J_3 and λ = 0. Direct substitution in the defining torsion formula gives

    N_L(e_3,e_4) = f f' e_1.

At f = 2 and f' = 3 this is 6 e_1, so an arbitrary scalar cutoff fails. Its Haantjes torsion is zero, in agreement with the prior Toeplitz result. The exact first-jet control program independently calculates all torsion and Haantjes components; it uses no candidate helper.

The size-three boundary case matters: for f(t) J_3(0), the angular block is f J_2, whose square is zero, so this scalar cutoff is Nijenhuis. It would be wrong to claim that **every** nilpotent scalar cutoff fails. The program checks sizes 2 through 8 and a two-dimensional diagonal matrix with eigenvalues 1 and 2. All eight controls pass in ordinary and optimized Python modes; explicit exceptions carry the checks, not removable assertions. These finite examples refute overly broad prior-corollary arguments, while the arbitrary-dimensional construction rests on its separate proof.

## 7. Unity and almost-complex rank results have different requirements

In [Antonov–Konyaev](https://arxiv.org/abs/2311.04624v1), the unity equation is Lie_e L = Id and implies e(tr L) = n. On a zero open band the left side is zero, so a unity satisfying that equation cannot exist there. Forgetting a unity after a local construction does not establish a smooth compact-support extension.

The [Coelho–Placini–Stelzig h-principle](https://arxiv.org/abs/2105.12113v3), Theorem A, concerns lower bounds on the rank of the Nijenhuis torsion of almost-complex structures. The target concerns the Jordan type of L itself with its torsion **zero**. These are different tensors and opposite differential requirements; that h-principle is not a full-target existence theorem.

## Conclusion of the comparisons

The necessary obstruction and several local ingredients are prior. No exact full classification, translated full classification, or checkable full affirmative corollary was established from the adjudicated passages. The absence of such a derivation here establishes neither worldwide openness nor firstness. Unread bodies and unexamined passages remain unknown, as recorded in the source ledger. A complete attributed proof of the printed historical problem is an eligible conservative framing; a certified new discovery is not supported by this audit.
