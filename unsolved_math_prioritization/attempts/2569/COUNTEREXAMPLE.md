# A central-double-cover counterexample to the modular semiperfectness criterion

**Target:** Kourovka Notebook 21.60, catalogue ID 2569.  
**Proposed answer:** No. Take `G = SL(2,5)` and `p = 2`.  
**Validation status:** Complete candidate proof with reproducible exact checks; specialist human verification has not occurred. No novelty beyond the checked literature is asserted.

The result concerns the Grothendieck-group criterion in KOU-21.60, not the distinct uniqueness-of-decomposition formulations of Kourovka 4.55.

## Theorem

Let `R = Z_(2)` and `k = F_2`. Every projective indecomposable `k SL(2,5)`-module has its class in the nonnegative-integer span of reductions of simple rational representations. Nevertheless, `R SL(2,5)` is not semiperfect.

The positive condition is proved for all three simple-module types over the stated base field `F_2`, including the type which is not absolutely simple.

## 1. A central-square-zero lemma

Let a finite group `G` have a central involution `z`, and put `H=G/<z>` and `t=z-1` in `kG`. Then `t^2=0`, and

- `kG/tkG` is `kH`;
- the kernel and image of multiplication by `t` on `kG` are both `tkG`;
- multiplication by `t` identifies `kG/tkG` with `tkG` as `kH`-modules.

To check this, choose a representative `g` of each coset of `<z>`. On the two-dimensional span of `g,zg`, multiplication by `t` has kernel and image both spanned by `g+zg`.

Let `P` be projective over `kG`. Applying a direct-summand projector to a free module preserves the kernel-image identity, giving

`P/tP ≅ tP`.

The isomorphism is induced by multiplication by `t` and is `G`-equivariant, with the action factoring through `H`.

The ideal `(t)` is nilpotent. Primitive idempotents correspond modulo a nilpotent ideal, up to the usual equivalence, so projective indecomposables of `kG` correspond to those of `kH` under `P ↦ P/tP`. Equivalently, a primitive projective has the same simple top after quotienting, and its quotient is projective over `kH`. Thus if `Q=P/tP`,

`[P] = 2[Infl_H^G Q]` in `G_0(kG)`.                                            (1)

This equality uses an actual short exact sequence. It does not apply the nonexact coinvariant functor to an arbitrary Grothendieck equality.

## 2. Positive witnesses for every projective indecomposable

Take `G=SL(2,5)`, `z=-I`, and `H≅A_5`. Write the three simple `F_2 A_5`-modules as

- `1`: dimension one;
- `U`: dimension four, with endomorphism field `F_4`; over an algebraic closure it splits into the two distinct degree-two simples;
- `S`: dimension four and absolutely simple.

Let `V_1,V_4,V_5` be the rational irreducible `A_5`-modules of the indicated degrees. The ordinary/modular data in Johnston–Rumynin, Example 3.4, give

`d(V_1)=[1]`, `d(V_4)=[S]`, `d(V_5)=[1]+[U]`,

and

`[P_H(1)]=4[1]+2[U]`,
`[P_H(U)]=4[1]+3[U]`,
`[P_H(S)]=[S]`.

Here `d` means reduction in the Grothendieck group; it does not assert that the reductions are direct sums. These quotient data are credited inputs, not claimed as a new calculation. Combining them with (1) gives the following explicit witnesses for `G`:

| G-projective | Composition class | Rational witness, inflated from H | Dimension |
|---|---|---|---|
| `P_G(1)` | `8[1]+4[U]` | `4V_1 ⊕ 4V_5` | 24 |
| `P_G(U)` | `8[1]+6[U]` | `2V_1 ⊕ 6V_5` | 32 |
| `P_G(S)` | `2[S]` | `2V_4` | 8 |

Inflation preserves rational irreducibility. Each witness is therefore a nonnegative combination of precisely the kinds of modules allowed in KOU-21.60. This verifies the hypothesis for every projective indecomposable.

As a dimension check, the regular `F_2G`-module has decomposition multiplicities `1,2,4` for these projectives, respectively: `24+2·32+4·8=120`. The middle multiplicity is two because `End(U)=F_4`, rather than `F_2`.

## 3. The degree-four quotient simple

The module `S` can be seen independently as the augmentation summand of the permutation module of `A_5` on five letters. Since five is odd, the permutation module splits as a trivial line plus this four-dimensional summand over `F_2`.

A Sylow-two subgroup `V_4` fixes one letter and acts regularly on the other four. Projection onto those four coordinates identifies the augmentation summand with the regular `F_2 V_4`-module. It is consequently projective over `F_2 A_5`, by the Sylow restriction criterion for projectivity. The included exact checker computes that the matrices of `A_5` on this summand span all of `M_4(F_2)`, verifying absolute irreducibility. This also provides a direct check of `P_H(S)=S`.

Let `chi_+` be its ordinary rational augmentation character, inflated to `G`.

## 4. A faithful quaternionic constituent

The binary icosahedral group `SL(2,5)` has a natural two-dimensional complex representation as a finite subgroup of `SU(2)`. Its symmetric cube has character `chi_-`, of degree four. The group identification and symmetric-power construction are also described in Chung–Kostant–Sternberg [5], Sections 2 and 4. If `x` is the trace of the natural representation, this character has trace `x^3-2x`.

The resulting values depend only on element order, as shown below. The two order-five classes and the two order-ten classes have the same values in these rows.

| Element order | 1 | 2 | 3 | 4 | 5 | 6 | 10 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Number of elements | 1 | 1 | 20 | 30 | 24 | 20 | 24 |
| `chi_+` | 4 | 4 | 1 | 0 | -1 | 1 | -1 |
| `chi_-` | 4 | -4 | 1 | 0 | -1 | -1 | 1 |

These values also agree with the faithful degree-four row in the academic GroupNames character table. Independently of that table, the checker constructs all 120 binary icosahedral unit quaternions over `Q(sqrt(5))`, verifies all 14,400 products, evaluates the symmetric-cube trace formula, and computes

`<chi_-,chi_-> = (16+16+20+24+20+24)/120 = 1`.

Since this is the character of an actual representation, the norm shows that it is irreducible. Its Frobenius–Schur indicator is

`nu(chi_-) = (4+4+20-120-24+20-24)/120 = -1`.                    (2)

For this sum, squaring elements of orders `1,2,3,4,5,6,10` produces orders `1,1,3,2,5,3,5`, respectively. Thus `chi_-` is quaternionic. In the complexification of any real representation, a quaternionic irreducible has even multiplicity. In particular this parity condition holds for every rational representation.

## 5. The eight-dimensional projective cannot lift

Put `E=P_G(S)`. By (1), its Brauer character on odd-order elements is `2 chi_+`. Suppose `E` had a projective `RG`-lattice lift `L`.

Let `Psi` be the ordinary character of `Q⊗_R L`. Two standard facts about projective integral representations determine it:

1. On two-regular elements, its ordinary character is the Brauer character of `E`.
2. On two-singular elements, its ordinary character vanishes.

For clarity, the vanishing is not a conjectural lifting assertion. Restrict a projective lattice to the cyclic subgroup generated by a two-singular element, complete at two, and extend scalars unramifiedly to split the odd-order part. Each component is a projective module over the local group algebra of the cyclic two-part, hence free. Its trace at an element with nontrivial two-part is zero, as for the regular representation. Summing components gives the assertion.

It follows that `Psi` has values `8,0,2,0,-2,0,0` in the order columns above. Hence

`Psi = chi_+ + chi_-`.                                                        (3)

The two characters in (3) are distinct: the central involution acts trivially in one and as minus the identity in the other. Therefore `chi_-` occurs with multiplicity exactly one in the rational representation `Q⊗L`, contradicting (2) and the real-representation parity condition.

Thus `E` admits no projective `RG`-lift. If `RG` were semiperfect, the standard idempotent/projective-cover lifting criterion would supply such a lift for every projective indecomposable `kG`-module. Therefore `Z_(2)SL(2,5)` is not semiperfect. Together with Section 2, this proves the stated counterexample. ∎

## Scope and source dependency

The core proof does not rely on the general rational-descent lemma from the research attempts, on any classification of local Schur indices, or on Johnston–Rumynin Proposition 3.3. It uses the credited `A_5` modular data, the elementary central-square-zero lemma, the standard character theory of projective lattices and Frobenius–Schur indicators, and the explicitly constructed degree-four character.

A separate research note tests the Ext-lifting step in Proposition 3.3 and records a concrete obstruction. That note is not needed for the counterexample theorem.

## References

1. E. I. Khukhro and V. D. Mazurov, *The Kourovka Notebook*, 21st edition, October 2026 revision, Problem 21.60, printed page 186. [Editors' update](https://kourovkanotebookorg.wordpress.com/2026/09/30/october-2026-update-for-the-21st-edition/); [current PDF](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt.pdf).
2. D. Johnston and D. Rumynin, *On a question by Roggenkamp about group algebras*, Journal of Algebra 687 (2026), 776–791, especially Conjecture 9 and Example 3.4. [DOI](https://doi.org/10.1016/j.jalgebra.2025.09.014); [arXiv v2](https://arxiv.org/abs/2507.21316v2).
3. T. Dokchitser, GroupNames: [SL(2,5)](https://people.maths.bris.ac.uk/~matyd/GroupNames/97/SL(2,5).html), ordinary character values and symplectic type; used as an independent published-data cross-check.
4. C. W. Curtis and I. Reiner, *Methods of Representation Theory*, Vol. I, Wiley, 1981. Standard projective-character and integral-representation background, also cited in [2].

5. F. R. K. Chung, B. Kostant and S. Sternberg, *Groups and the Buckyball*, Sections 2 and 4, [author-hosted paper](https://fanchung.ucsd.edu/wp/groupb.pdf). The binary-icosahedral group identification and actual symmetric-power construction support the character calculation.

The exact finite verification is `verify_counterexample.py`; its machine-readable output is `counterexample_results.json`. The script confirms finite arithmetic and stated constructions. The mathematical proof above, rather than the script alone, supplies the implication to nonsemiperfectness.
