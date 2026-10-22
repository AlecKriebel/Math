# Turn 5: full-algebra component obstruction and an explicit excluded twist

Problem 30006345. Fifth and final author turn. **Original unresolved, 5/5.** This turn proves an exact finite-component descent criterion and a field-degree bound for a fixed algebra, then constructs a local form of a modular group algebra which is provably not itself a group algebra over the prime field. The construction illustrates a missing condition in a counterexample search; it is not a counterexample to the source question.

## 1. The full-algebra descent criterion

Let A,B be finite-dimensional F_p-algebras which are isomorphic after extending scalars to Fbar_p. Let R be the reduced algebraic group Aut(A)_red over F_p. Concretely, automorphisms are invertible matrices satisfying the finite multiplication-table and unit equations. Over the perfect field F_p the reduction is an algebraic subgroup and smooth, as in the credited Milne statements recorded in turn 4. Let

    Pi = pi_0(R_(Fbar_p)),       c=|Pi|,

be its finite group of geometric connected components, and let tau be the automorphism of Pi induced by Frobenius F. Fix an algebra isomorphism f:A_(Fbar_p)→B_(Fbar_p), and put

    a=f^−1F(f)∈R(Fbar_p),       alpha=[a]∈Pi.                 (1)

Then A≅B over F_p **if and only if**

    alpha=x^−1 tau(x) for some x∈Pi.                         (2)

The obstruction is therefore a twisted component class in the automorphism group of the **full algebra**, not merely the commutator tensor. This is the standard finite-field forms/Lang mechanism, with the proof made explicit here. No historical novelty is claimed.

### Proof

If a=h^−1F(h) in R(Fbar_p), then f h^−1 is Frobenius-fixed and descends to an F_p-algebra isomorphism. Conversely, if f=r h with r an F_p-isomorphism, then a=h^−1F(h). Passing to components proves necessity of (2).

For sufficiency, choose h_0∈R(Fbar_p) in component x and replace f by f′=f h_0^−1. Its Frobenius discrepancy is

    a′=h_0 a F(h_0)^−1.

By (2) its component is x alpha tau(x)^−1=1, so a′∈R^0(Fbar_p). The identity component R^0 is defined over F_p and is connected. Lang's theorem supplies u∈R^0(Fbar_p) with a′=u^−1F(u). Thus f′u^−1 descends. This proves(2) without assuming that a component representative is itself Frobenius-fixed.

## 2. A bounded extension degree for the fixed algebra

There is always an integer d with

    1≤d≤c,        F_(p^d)⊗A ≅ F_(p^d)⊗B.                    (3)

Indeed the map T:Pi→Pi, T(x)=alpha tau(x), is a permutation of a set with c elements. Let d be the length of the orbit of1 under this permutation. Then

    alpha tau(alpha)⋯tau^(d−1)(alpha)=T^d(1)=1,

where d≤c. On the full group, telescoping gives

    f^−1F^d(f)=a F(a)⋯F^(d−1)(a)∈R^0(Fbar_p).

Apply Lang's theorem to R^0 with Frobenius F^d to correct f to an F^d-fixed isomorphism. Its entries lie in F_(p^d), proving(3). The displayed d need not be the minimal splitting degree, and may depend on f. The bound c does not depend on B within the geometric isomorphism class.

For the source problem, any isomorphism over an arbitrary characteristic-p field first gives a geometric isomorphism by the credited García-Lucas–del Río reduction. Thus (3) bounds a sufficient finite extension in terms of the number of components of Aut(F_pG)_red. When c=1, descent reaches F_p and the known prime-field theorem implies G≅H. But neither c=1 nor triviality of (2) has been established for arbitrary class-two exponent-p group algebras. Computing a component group, or restating the problem in terms of it, is not a solution of that missing group-algebra restriction.

The general bound can be attained: A=F_p×F_p and B=F_(p²) become isomorphic over F_(p²) but not F_p; their geometric automorphism group is the two-element permutation group, with c=2. This is an étale-algebra example, outside the p-group-algebra source family.

## 3. An explicit local twist of a group algebra

Now p is odd. Let H=H(F_p) be the order-p³ Heisenberg group and let

    S=H×H,       A=F_p[S]=F_p[H]⊗F_p[H].

Choose a nonsquare d_0∈F_p and K=F_p(s), s²=d_0, so s^p=−s. On C=K⊗A define the semilinear involution

    Theta(lambda⊗x⊗y)=lambda^p⊗y⊗x.

Swapping the two tensor factors is an algebra automorphism even though each factor is noncommutative. Let B=C^Theta be the fixed F_p-subalgebra.

This algebra has dimension p⁶ and becomes K[S] after scalar extension. To verify descent concretely, choose the group basis u_1,…,u_n of F_p[H], n=p³. An F_p-basis of B consists of

    u_i⊗u_i                                      (1≤i≤n),
    u_i⊗u_j+u_j⊗u_i,
    s(u_i⊗u_j−u_j⊗u_i)                          (i<j).        (4)

Each is fixed by Theta. A fixed coefficient matrix has diagonal coefficients in F_p and off-diagonal coefficients lambda_(ji)=lambda_(ij)^p; writing lambda=a+bs shows that (4) spans precisely the fixed subspace over F_p. There are n² vectors. On each off-diagonal pair the change-of-basis determinant is −2s≠0, so they also form a K-basis of C. Consequently K⊗B→C is an algebra isomorphism.

The augmentation ideal J of C is nilpotent. Its intersection J_B=B∩J is nilpotent, and augmentation gives B/J_B=F_p because fixed augmentations are Frobenius-fixed and every F_p scalar occurs. Thus B is a local algebra and J_B is its Jacobson radical. Dimension and scalar extension give K⊗J_B=J; hence for every j,

    K⊗J_B^j=J^j.                                            (5)

In particular the radical filtration descends correctly; no identification of an arbitrary filtration with the Jacobson filtration is assumed.

## 4. The twisted leading tensor is nonsplit

The degree-one space of gr_J(C) is the sum of the two Heisenberg degree-one spaces, K²⊕K², and the bracket-image space in degree two is K⊕K. Frobenius acts on coefficients and Theta swaps the summands. Their fixed spaces have the descriptions

    V_B={(v,F(v)):v∈K²},       W_B={(z,F(z)):z∈K}.

Equation (5), or the explicit fixed bases, identifies these with the corresponding spaces of gr_(J_B)(B). The bracket of (v,F(v)) and(w,F(w)) is

    (det(v,w),F(det(v,w))).

Its F_p-span is all W_B: determinants 1 and s are both attained. Thus the intrinsic leading commutator tensor of B is exactly the F_p-tensor of

    N=H(F_(p²)).                                             (6)

This is a statement about the intrinsic degree-one bracket of the graded algebra of B, not a claim that B itself is F_p[N].

## 5. Why the twist is not a group algebra

The center commutes with scalar extension for finite-dimensional algebras: express centrality as the kernel of the finite system of linear commutator equations in a basis and extend the field. Therefore

    dim_(F_p) Z(B)=dim_K Z(C)=(p²+p−1)².                     (7)

If B≅F_pL for a class-two exponent-p group L, turn 4's canonical graded reconstruction and (6) would give an F_p-equivalence between the commutator tensors of L and N. The Baer/presentation argument then gives L≅N. But turn 1's conjugacy count gives

    dim_(F_p) Z(F_pN)=p⁴+p²−1,

which differs from (7) by 2(p−1)²(p+1)>0. This contradiction proves that B is not the group algebra of **any group in the source's class-two exponent-p family**.

In fact the exclusion applies to every finite group. If B≅F_pL, its dimension makes |L|=p⁶, so L is a p-group. Extending scalars gives KL≅KS. The credited all-field exponent and class invariants in Margolis–Sakurai, Propositions 2.7 and 2.9 of https://arxiv.org/abs/2505.05902v2 , force L to have exponent p and class two. The preceding argument then excludes it. This last strengthening uses those published invariants, rather than assuming class/exponent can be read from an arbitrary graded algebra alone.

Thus B is a completely explicit local algebra form of K[S] which is not a prime-field group algebra. In particular B≄A. The tensor-factor swap is a genuine full-algebra automorphism; on the rank-drop lines of the leading split pencil it acts nontrivially, explaining the disconnected-component obstruction already visible in turn 4. Producing nontrivial forms is possible, but proving that such a form has a group basis remains essential. This example fails that requirement by a rigorous full-center obstruction.

## 6. What is established and what is not

- The finite component criterion (2) and extension bound (3) are proved for geometrically isomorphic finite-dimensional F_p-algebras.
- The fixed algebra (4) is explicitly constructed for every odd p, is local, and splits over a quadratic field, yet cannot be any finite group algebra over F_p.
- No two nonisomorphic groups with isomorphic full modular algebras have been produced, and no proof covers all class-two exponent-p groups. The original source remains unresolved after five substantive turns.
- The finite-field reduction, Lang theorem, Baer/Jennings methods and the published exponent/class invariants are credited inputs. No first-priority or historical novelty claim is made.

The exact checker tests finite component permutations/norms, the quadratic étale control, fixed tensor-basis spanning and multiplication, the descended leading bracket, and the center-dimension obstruction. Finite examples support the implementations; the proofs above establish arbitrary odd p and the abstract component criterion.

Final subjective completion estimate for the unrestricted source question: 3%. Five author turns are exhausted. Freeze this packet for independent full source/proof review; no sixth author search.
