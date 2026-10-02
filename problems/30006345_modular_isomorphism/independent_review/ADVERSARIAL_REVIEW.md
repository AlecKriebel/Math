# Independent full five-turn review: 30006345

2026-10-02. **PASS for the stated partial theorems, counterchecks and conditional descent results. The original arbitrary-field modular-isomorphism problem remains unsolved after 5/5 substantive author turns.** No mandatory mathematical correction was found. This is an AI-assisted source and proof audit, not formal verification, human peer review or historical-novelty certification.

## Bound packet and exact source scope

This review binds all 37 files at author commit `bc91d72737c17e4760370c50bc3811dd3555f075`, folder `problems/30006345_modular_isomorphism`, with final author manifest SHA256 `f99e653b05401fbc7555114abf9c3d180242e4a783f68fabdff72a21de7bc1cb`. Every file was compared with the frozen local packet as raw UTF-8 content and by Git blob hash. The manifest's 36 entries also passed independent byte-length and SHA256 checks.

The exact OWR statement on printed p.1416 was independently opened and visually read. It distinguishes the classical prime-field theorem from the open question over arbitrary characteristic-p fields. The relevant nonabelian class-two exponent-p case has odd p. Neither a graded-algebra isomorphism nor a center-algebra isomorphism is the source's full-algebra hypothesis.

The pinned Margolis–Sakurai 2025 paper was independently opened. Its Section 2.2 and Question 2.10 retain the field distinction; Propositions 2.7 and 2.9 were also visually checked on printed pp.5–6. They respectively supply the exponent invariant and the class invariant needed in turn 5's final strengthening. The García-Lucas–del Río Theorem A/Corollary B reduces an existing isomorphism to some finite extension, with no assertion that the prime field suffices.

Milne's primary online *Algebraic Groups*, Proposition 1.26, Corollary 1.39 and Section 17(k), including Corollaries 17.97–17.98, were independently read. The reduced-subgroup and smoothness hypotheses over the perfect field F_p, and Lang's actual Frobenius surjectivity, match the uses in turns 4–5. The author accurately records its whole-PDF download limitation; this audit used the accessible indexed primary text for those statements.

## Turn 1: the entire graded algebra is insufficient

The Heisenberg group law, exponent and conjugacy calculations hold for every odd p. The center dimension uses the class-sum basis, valid in modular characteristic, rather than a semisimple character argument. The difference between the two center dimensions is exactly 2(p-1)^2(p+1), so the full group algebras are separated over every field of the relevant characteristic.

The ordered-monomial presentation maps onto the intrinsic radical associated graded algebra and has at most the group order in spanning monomials. Nilpotence of the augmentation radical makes the target dimension exactly the group order, establishing equality and independence. This is a valid dimension squeeze, not an assumed identification of the full algebra with its graded algebra. The quadratic splitting formulas have the correct factors of two and the correct brackets. The new pth-power relations involve only sums of commuting generators. Thus the claimed graded collision and simultaneous full-algebra noncollision both hold, with their scopes correctly separated.

## Turn 2: reconstruction within the stated family

For a Heisenberg factor, each noncentral class sum is gN. The identities N^2=0 and (z-1)N=0 give the stated square-zero augmentation module over the truncated polynomial center. In particular, the polynomial uses powers of rad(Z(kG)); it does not substitute the filtration induced from the ambient radical.

The center of a tensor product and the radical convolution arguments are valid over an arbitrary coefficient field, because the local factors have residue field k. The degree and group-order equations recover the elementary abelian rank and total field degree. Reversing the polynomial yields strictly increasing positive first correction degrees e(p-1)-1. Successively removing lower factors therefore recovers each integer multiplicity exactly. The coefficient arithmetic takes place in Z, not modulo p.

Both comparison groups must be Heisenberg products with elementary abelian factors. The packet consistently preserves that hypothesis. It does not infer membership in the family from the numerical invariant alone.

## Turn 3: the full center is also insufficient

The two determinant quadratics are irreducible over F_3, separable and coprime over its algebraic closure. Their block pencils have precisely the stated geometric rank drops: rank four at two points for the repeated pencil, versus rank six at four points for the mixed pencil. Looking only at rational parameters would miss this distinction; the proof correctly works geometrically.

Nonsingularity at every nonzero rational parameter makes every nonzero contraction onto the two-dimensional center. Thus both groups have full central cosets as their noncentral conjugacy classes, and the same complete center algebra follows. The derived subgroup and center have the claimed sizes.

The passage from a full algebra isomorphism to a graded isomorphism is intrinsic. Degree one and the bracket span in degree two recover the scalar-extended commutator tensor; the monomial dimension argument rules out hidden collapse of its central directions. The resulting geometric rank contradiction proves full-algebra nonisomorphism over every characteristic-three field. No group-only invariant is silently treated as an algebra invariant without this bridge.

## Turn 4: conditional connected-stabilizer descent

The general graded presentation and the odd-characteristic Baer model recover precisely the alternating tensor needed. Tensor equivalence over F_p gives a group isomorphism, including elementary abelian central directions. Scalar-extended tensor equivalence by itself does not provide such a prime-field equivalence.

The stabilizer is treated as an algebraic group scheme, then reduced over F_p. Reduction preserves its field points and is a smooth algebraic subgroup over this perfect base. The geometric connectedness hypothesis permits Lang's theorem. For a=g^{-1}F(g), solving h^{-1}F(h)=a and using g h^{-1} gives the correct Frobenius-fixed matrix: the multiplication order in this noncommutative calculation is correct.

The hypothesis is substantive. In the split Heisenberg product, factor swap exchanges the two geometric rank-drop lines and yields a nontrivial map to a two-element permutation group. It therefore cannot be assumed connected. The conditional conclusion is not promoted to the original unrestricted theorem.

## Turn 5: full-algebra forms and the excluded local twist

The automorphism group here is that of the full finite-dimensional algebra. Its finite component group carries the Frobenius action. The criterion alpha=x^{-1}tau(x) is necessary and sufficient: changing the isomorphism by a representative of x puts the discrepancy in the identity component, where ordinary Lang surjectivity corrects it. There is no requirement that the initial representative itself be rational.

The extension bound is valid also for a nonabelian component group. The permutation x maps to alpha tau(x), and its return time from the identity gives the ordered product alpha tau(alpha)...tau^{d-1}(alpha)=1 with d at most the number of components. The analogous discrepancy in the full group lies in its identity component, so relative Frobenius F^d supplies the correction. This gives a sufficient extension degree, not descent to F_p in general.

The semilinear tensor-factor swap is an algebra automorphism even for noncommutative factors. Its displayed fixed vectors form an F_p-basis and, after extension, a K-basis. The fixed algebra is local; its augmentation kernel extends to the full radical, and all powers extend correctly. Consequently the fixed degree-one and bracket spaces really are the intrinsic descended graded spaces. Their bracket is the nonsplit restriction-of-scalars Heisenberg tensor.

If the fixed algebra were a class-two exponent-p group algebra over F_p, this tensor would force the group to be H(F_(p^2)); its center dimension would then contradict the fixed algebra's center dimension. For an arbitrary finite-group algebra, dimension first forces group order p^6, and the verified all-field exponent/class invariants reduce it to the same excluded class. Thus the stronger exclusion of every finite-group algebra is supported. The example is a genuine local algebra form, but lacks a group basis and cannot be a counterexample to the source question.

## Reproducibility and final disposition

All five author checkers were run separately from the frozen packet and their outputs reproduced byte-for-byte: 137,676 exact assertions in total. The five replay receipts are included here. No author checker was used as a dependency of the separately written independent checker.

The additional controls passed 19,949 exact assertions: center-parameter reconstruction, actual H(F_3) class-sum multiplication, geometric F_9 pencil ranks, nonabelian S_3/S_4 component norms and twisted-class changes, and semilinear fixed-basis descent. These are supplementary bounded controls, not computations of arbitrary automorphism-group components and not substitutes for the general Lang argument.

The strongest statements above are approved with their existing hypotheses and classical credit. The exact remaining gap is unchanged: no proof that a full group-algebra isomorphism always eliminates the disconnected descent obstruction, and no pair of nonisomorphic groups with isomorphic full scalar-extended algebras. Recommended public disposition: **unsolved, 5/5**, with the full scoped packet preserved and no sixth author search.

Primary references: [OWR source](https://ems.press/content/serial-article-files/51860), [Margolis–Sakurai v2](https://arxiv.org/pdf/2505.05902v2), [finite-field reduction](https://arxiv.org/abs/2305.09355), [Milne](https://www.jmilne.org/math/Books/iAG2022.pdf).
