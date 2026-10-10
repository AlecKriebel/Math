# A normalization obstruction for categorical trisection invariants

Problem 30006636 / OWR-14299913-005. Authored research note, 8 October 2026.

## Result and scope

There is an admissible instance of the Meusburger--Mulevicius--Torzewska (MMT) invariant whose **unchanged** closed-manifold values cannot be the partition function of an ordinary complex oriented four-dimensional TQFT. Its value on `S^1 x S^3` has cube 4. This contradicts the categorical-trace axiom, which makes that value a nonnegative integer.

The obstruction is genuinely a normalization obstruction. For the same family we give an explicit, strong symmetric monoidal Euler TQFT after a constant rescaling on connected closed manifolds. Consequently this note does **not** settle the workshop question if “extension” permits changing the connected closed-manifold normalization. Nor does it classify the general categorical input or construct its boundary state spaces. No novelty priority is asserted.

Precisely, an ordinary complex oriented four-dimensional TQFT here means a strong symmetric monoidal functor

    Z : Bord_4^or -> Vect_C^fd,

where objects are closed oriented smooth 3-manifolds, morphisms are compact oriented smooth 4-dimensional bordisms up to boundary-preserving diffeomorphism, composition is gluing, and monoidal product is disjoint union. The empty 3-manifold is the monoidal unit and its state space is identified with C by the unit isomorphism. No unitarity, semisimplicity of Z, or extension to corners is assumed. Any more extended ordinary complex theory restricting to such a functor is subject to the same obstruction.

## 1. Source and target normalization

The originating source is Catherine Meusburger's contribution “Trisection invariants of four-manifolds,” joint with Vincentas Mulevicius and Fiona Torzewska, printed pp. 767--768 of Oberwolfach Report 12/2026 [OWR]. Its first open question asks about extension to a 4d TQFT and separately mentions boundary-gluing and fusion-2-category issues. It specifies neither the target category nor an equivalence relation allowing renormalization.

The associated manuscript [MMT], Theorem 4.28 (PDF p. 32), uses

    I(T) = xi^(-g) av(T),       xi^3 = C_st != 0.

Definition 4.26 fixes `C_st` by the punctured standard stabilizing diagram. We keep these exact values and every permitted cube-root choice. The input is `(A,B,C,M,Phi)`: spherical fusion categories over C, an indecomposable finite semisimple `(C,B)`-bimodule category with bimodule trace, and a pivotal functor into its bimodule endofunctors. This note specializes the admissible finite-group construction in Section 6.2, with `Phi=id`. These source results, not a conjectural TQFT extension, are the dependencies used below.

## 2. A fully admissible input

Let G be a finite group of order N. Use trivial cocycles and put

    C = Vec_G,  B = Vec,  M = Vec,
    A = End_(Vec_G,Vec)(Vec),  Phi = id_A.

The left action of a graded vector space on M tensors with its underlying ungraded vector space; the right Vec action is the usual tensor product. Both associativity structures are the usual ones. The trace on M is the ordinary matrix trace. It is cyclic, its composition pairing is nondegenerate, and compatibility with both partial traces is the ordinary partial-trace identity. There is one simple object of M, with trace dimension 1, so M is finite semisimple and indecomposable.

This is the one-point transitive G-set case of [MMT], Section 6.2.1. Concretely a Vec_G-module endofunctor of Vec is tensoring by a vector space V together with the coherent G-action on V. Thus A identifies with Rep(G), with its standard spherical structure. Equivalently one may keep A literally equal to the endofunctor category, avoiding any choice of equivalence; its identity functor is pivotal. All categories here are spherical fusion categories. For the eventual counterexample take `G=C_2`, so the two simple objects of A are the trivial and sign representations and all simple dimensions are 1.

The remaining stabilizing hypothesis will be checked numerically and exactly below: `C_st=N^4`, and therefore it is nonzero.

## 3. Computing this entire family

Write `(g,k)` for the balanced trisection parameters and `T` for its diagram. The surface has g red, g blue and g green curves. In the finite-group evaluation of [MMT], Definition 6.12 and Proposition 6.13 (PDF p. 58), blue labels come from the trivial group, all region labels come from the one-point set, and green labels are elements of G. The only constraints are that the ordered signed green-crossing word around each red curve is the identity. There is no quotient of label assignments by conjugation.

**Lemma 1.** The number of admissible labellings is `N^k`.

**Proof.** Ignore the unit-labelled blue curves. The red-green pair is a genus-g Heegaard diagram for `#_k(S^1 x S^2)` by the definition of a balanced trisection. Cutting the green handlebody along its meridian disks gives the usual g-generator presentation: each red meridian supplies a relator whose word is its ordered signed list of crossings with the green meridians. Hence an admissible assignment is exactly a homomorphism from the presented fundamental group to G. This is the free group of rank k, so its homomorphisms to G are in bijection with G^k. Changing basepoints conjugates relators and changing orientations inverts them; neither changes the solution set. This is a count of based homomorphisms, not conjugacy classes. Therefore the count is `N^k`. QED.

There are g red curves. Each red character sum contributes N times the identity-word constraint. To see the factor, decompose the regular representation of G into irreducibles: its character equals `sum_rho dim(rho) chi_rho(h)`, which is N for h=1 and zero otherwise. Thus

    av(T) = N^g N^k = N^(g+k).

This also recovers the specialized formula in [MMT], Corollary 6.14 (PDF p. 59), without treating an unspecified normalization as free.

For the standard balanced stabilizing diagram of S^4, `(g,k)=(3,1)`. Puncturing in a region does not introduce an extra choice because M has only one simple object, of dimension 1. Therefore

    av_m(T_st') = N^4,       C_st = N^4.

This proves the missing stabilizing hypothesis directly. For any permitted cube root xi of N^4, define `a=xi/N`. Then `a^3=N`. Using `chi(X)=2+g-3k`, obtained either from the trisection handle counts or inclusion-exclusion, gives

    I_a(X) = (N a)^(-g) N^(g+k)
           = a^(3k-g)
           = a^(2-chi(X))                                      (1)

for every connected closed oriented smooth four-manifold X. In particular `I_a(S^4)=1` and `I_a(S^1 x S^3)=a^2`.

### Direct check of the counterexample diagram

The standard `(1,1)` diagram is a torus with three disjoint parallel essential curves, one of each color. Each two-color diagram is the genus-one splitting of `S^1 x S^2`. It represents `S^1 x S^3`: see [GK], Remark 5(2), printed p. 3099; the absence of 2-handles when g=k gives this identification. Thus it is a **balanced** trisection, not one of the unbalanced genus-one stabilizations of S^4.

For G=C_2 there are two possible green labels, one blue label and one region label. The red curve meets no green or blue curve, so its word is empty and both green choices are admissible. Directly at the character level the two red simple labels each have dimension 1 and contribute the character at the identity, also 1. Hence the four `(red,green)` choices each contribute 1 and `av(T)=4`.

For the standard genus-three stabilizer, the red-green diagram has two transverse meridian pairs and one parallel pair. The two transverse pairs force their green labels to be the identity; the remaining green label is free. There are two admissible labels and three factors 2 from the red character sums, so `av(T_st')=16`. Equivalently the raw character sum is

    sum_(r1,r2,r3,c1,c2,c3 in {0,1}) (-1)^(r1*c1+r3*c3) = 16.

The precise sign of either crossing is immaterial for C_2. The source's stabilizer was visually inspected in [MMT], Example 2.3, PDF p. 6. Consequently, without extracting any approximate cube root,

    I(S^1 x S^3)^3 = 4^3/16 = 4.                              (2)

## 4. Trace obstruction

**Lemma 2.** For every ordinary complex oriented four-dimensional TQFT Z and closed oriented 3-manifold Y,

    Z(Y x S^1) = dim_C Z(Y).

**Proof.** In the bordism category, the trace of the identity cylinder of Y is obtained by closing the cylinder, giving `Y x S^1`. The evaluation and coevaluation bordisms express the duality of Y and its orientation reversal. A strong symmetric monoidal functor preserves this trace. For a finite-dimensional vector space V, evaluation composed with the symmetry and coevaluation of `id_V` is `sum_i e^i(e_i)=dim V`. This computation does not depend on choosing special duality maps: the zig-zag identities identify them with the usual duality through an isomorphism. Therefore the partition function is the stated nonnegative integer. QED.

Even replacing `Vect_C^fd` with all algebraic complex vector spaces does not evade the conclusion: the coevaluation is a finite sum of simple tensors, and the zig-zag identity forces those finitely many first factors to span V. Dualizability therefore forces V to be finite-dimensional.

**Theorem 3 (unchanged-normalization nonextension).** For the data in Section 2 with G=C_2, no choice of xi allowed by [MMT], Theorem 4.28, yields the closed partition function of an ordinary complex oriented four-dimensional TQFT.

**Proof.** If such a TQFT existed, put `d=dim Z(S^3)`, a nonnegative integer. Equation (2) and Lemma 2 give `d^3=4`. But d=0 or 1 has cube at most 1, and d>=2 has cube at least 8. This is impossible. The argument treats all three xi choices simultaneously. QED.

The obstruction already occurs for semisimple, unitary standard finite-group data and the simplest nontrivial group. It does not rely on exotic smooth structures, nonsemisimplicity, or a conjecture about fusion 2-categories.

## 5. What normalization changes can and cannot do

Changing the selected cube root does not help Theorem 3. Scaling the Hopf integrals compatibly with xi is also not an independent remedy: the genus factors cancel, as in [MMT], Remark 3.15. The ordinary bimodule trace was fixed in Section 2. Rescaling that trace changes the categorical input; no invariance under that operation is claimed.

Multiplication of I by a pure Euler factor `q^chi(X)` with q nonzero leaves its value on `S^1 x S^3` unchanged, since that manifold has Euler characteristic zero. Thus that specific operation alone also cannot remove the obstruction.

In contrast, multiplying by a nontrivial constant on each **connected closed** four-manifold can remove it. For each root a in (1), define

    J_a(X) = a^(-2) I_a(X) = a^(-chi(X))

on connected closed X, and extend multiplicatively to disconnected closed manifolds, taking J(empty)=1. Here is a complete functor realizing J.

**Theorem 4 (rescaled Euler TQFT).** Assign `E_a(Y)=C` to every closed oriented 3-manifold Y, including the empty manifold. For every bordism `W:Y0 -> Y1`, let `E_a(W)` be multiplication by `a^(-chi(W))`. Give this functor the unit isomorphism `C -> E_a(empty)` equal to the identity and the tensor isomorphism `C tensor C -> C` given by ordinary multiplication.

This defines a strong symmetric monoidal functor `Bord_4^or -> Vect_C^fd`, and its connected closed partition function is J_a.

**Proof.** Euler characteristic is invariant under diffeomorphism. Every closed oriented 3-manifold has Euler characteristic zero, so a cylinder has Euler characteristic zero and maps to the identity. If W and W' glue along Y, then

    chi(W' composed W)=chi(W')+chi(W)-chi(Y)=chi(W')+chi(W).

Therefore the scalar for the composite equals the product of scalars. Euler characteristic is additive under disjoint union, giving compatibility with the displayed tensor isomorphism. Those standard multiplication isomorphisms satisfy unit, associativity and symmetry coherence. The empty bordism has Euler characteristic zero and scalar 1. Finally on a closed X, its scalar is exactly `a^(-chi(X))`. QED.

For G=C_2 and the positive root, the needed connected-component constant is `2^(-2/3)`. It changes the S^4 value from 1 to `2^(-2/3)` and the `S^1 x S^3` value from `2^(2/3)` to 1. This is an actual change of the closed invariant, not a basis change in state spaces or a choice of the strong monoidal unit isomorphism.

## 6. External dependencies, claim limits and attempt accounting

The constructor and its finite-group evaluation are the published mathematical inputs from [MMT]; they are not reproved in complete generality. Their specialization and all algebra after it are explicit above. [GK] supplies the standard trisection interpretation. The TQFT trace obstruction and the rescaled functor are proved here from definitions. Finite executable checks supplement, and do not replace, these proofs.

The latest arXiv entry inspected on 8 October 2026 lists v1, submitted 24 November 2025. Targeted public literature searches did not locate a later general construction or this particular obstruction. This is a bounded search statement, not a proof of current openness or priority.

One substantive mathematical approach was used: the categorical-trace obstruction, evaluated on an explicit admissible finite-group specialization. It produced a rigorous counterexample to unchanged extension, so no artificial five-approach padding is supplied. Source recovery, literature checking, exact tests and independent audit are not additional attempts. The Euler construction establishes the exact limitation of that obstruction. The workshop's broader, normalization-unspecified question remains unresolved here.

## References

[OWR] Catherine Meusburger, “Trisection invariants of four-manifolds,” joint with Vincentas Mulevicius and Fiona Torzewska, in *Higher Structures from Symmetries in Quantum Field Theory*, Oberwolfach Reports 23 (2026), report 12, pp. 767--768 within pp. 737--794. https://doi.org/10.4171/OWR/2026/12 . Open original: https://publications.mfo.de/handle/mfo/4446 .

[MMT] Catherine Meusburger, Vincentas Mulevicius and Fiona Torzewska, *Categorical 4-manifold invariants from trisection diagrams*, arXiv:2511.19384v1 (2025), 68 pp. https://arxiv.org/abs/2511.19384v1 . Key locators: Definition 4.26 and Theorem 4.28, PDF p. 32; Section 6.2.1, pp. 53--56; Definition 6.12 and Proposition 6.13, p. 58; Corollary 6.14, p. 59; Example 2.3, p. 6. PDF equation (55) is the normalization formula; HTML renumbering calls it (95).

[GK] David T. Gay and Robion Kirby, *Trisecting 4-manifolds*, Geometry & Topology 20 (2016), 3097--3132. https://msp.org/gt/2016/20-6/gt-v20-n6-p02-s.pdf . Remark 5(2), printed p. 3099.
