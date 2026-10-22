# Ambient dependence of extremal-exchangeable independence

Problem 30001182 / OWR-3392-009. Author result: a complete negative answer to ambient invariance, in one substantive proof attempt. This note is AI-assisted and is not human peer reviewed or formally certified. Historical novelty is not claimed.

## 1. The precise definition and conclusion

Let A be a unital complex *-algebra, with a state φ (a positive unital linear functional), and let B,C be unital *-subalgebras. Write F(A) = *_{n∈N} A for the unital algebraic free product, with inclusions j_n. In the C*-category use the universal unital C*-free product instead. The group of finite permutations of N acts by α_σ(j_n(a)) = j_{σ(n)}(a). A state is exchangeable if it is invariant under these actions.

Liebscher's definition on printed p. 540 of [1] says that B and C are independent in (A,φ) if some **extreme point of the convex set of all exchangeable states on F(A)**, denoted ω, satisfies

    ω ∘ ((j_1|_B) * (j_2|_C)) = φ ∘ (ι_B * ι_C)                 (1)

as states on B*C. Thus equality is required for every word, not only for second moments. Extreme means extreme among all exchangeable states, not among states having a prescribed marginal. The source does not impose faithfulness or distinctness of B and C; the main example below nevertheless has B≠C, B∩C=C1, and B,C both proper.

**Theorem 1.** There is a state-preserving unital inclusion

    (A,φ) = (C({0,1}²), ½δ_(0,0)+½δ_(1,1))  ⊂  (M₄(C),φ′)

such that the coordinate subalgebras B and C are not independent in (A,φ), but are independent in (M₄(C),φ′), in exactly sense (1). The conclusion holds for algebraic free products and universal C*-free products. The upstairs witness additionally has marginal φ′ on every entire copy of M₄, so adding that marginal condition does not remove this example (provided extremality still means extremality among all exchangeable states).

In particular the dependence on the ambient algebra is necessary in the unrestricted definition. A separate example in Section 5 also realizes the source's more specific suggested obstruction: in general algebraic *-algebras, an extreme exchangeable state need not have any positive extension to a larger ambient algebra.

## 2. Two elementary state facts

For any positive linear functional η, Cauchy–Schwarz gives

    |η(y* x)|² ≤ η(x* x) η(y* y).                               (2)

In particular η(x*x)=0 implies η(y*x)=0 for every y. This also justifies the ordinary algebraic GNS construction: the null space N={x:η(x*x)=0} is a left ideal. Indeed, if x∈N, apply (2) to x and a*a x to get η(x*a*a x)=0, hence ax∈N. Left multiplication therefore acts on the quotient pre-Hilbert space, with cyclic vector Ω=[1]. All GNS calculations below are valid algebraically, without invoking completion or faithfulness.

**Lemma 2.1 (pure states pull back through quotients).** If q:D→E is a surjective unital *-homomorphism and η is a pure state of E, then η∘q is pure among all states of D.

Proof. Suppose η∘q=tη₁+(1−t)η₂, where 0<t<1 and η₁,η₂ are states. For x∈ker q, positivity gives η_k(x*x)=0, whence η_k(x)=0 by (2). Thus each η_k factors as θ_k∘q. The θ_k are positive: if a=q(z), then θ_k(a*a)=η_k(z*z)≥0. They are unital, and η=tθ₁+(1−t)θ₂. Purity forces θ₁=θ₂=η and therefore η₁=η₂=η∘q. ∎

**Lemma 2.2 (matrix vector states are pure).** For a unit vector v∈C^d, η(a)=v*av is pure on M_d(C).

Proof. Put e=vv*. In a convex decomposition η=tη₁+(1−t)η₂, positivity and η(1−e)=0 imply η_k(1−e)=0. Equation (2) then kills all terms of η_k(a) having a factor 1−e on either end. Consequently

    η_k(a)=η_k(eae)=(v*av)η_k(e)=v*av,

since η_k(e)=1. The decomposition is trivial. ∎

The canonical **folding** quotient q_A:F(A)→A sends j_n(a) to a for every n. It commutes with permutations in the sense q_A∘α_σ=q_A. Hence η∘q_A is exchangeable for every state η and is pure, hence extremal exchangeable, whenever η is pure. This familiar pure-folding mechanism is a special case of the maximal-amalgamation construction in Dykema–Köstler–Williams [2, Proposition 8.7]; the elementary proof here also establishes extremality among all states, a stronger fact than required.

## 3. The distinct-subalgebra counterexample

Order the four points as 00,01,10,11. Inside A=C({0,1}²), set

    p(s,t)=s,           q(s,t)=t,
    B=span{1,p},       C=span{1,q},
    φ(f)=½f(00)+½f(11).

The functions 1,p,q,pq span A. B and C are distinct proper unital *-subalgebras. If a+bp=c+dq on all four points, evaluation at 00,10,01 forces a=c and b=d=0, proving B∩C=C1. The fixed joint law satisfies

    φ(p)=φ(q)=φ(pq)=φ(qp)=½.                                  (3)

### 3.1 No extremal exchangeable witness in A

Assume ω is any exchangeable state on F(A) satisfying (1). Let

    P_i=π_ω(j_i(p)),         Q_i=π_ω(j_i(q))

in its GNS representation, and retain Ω for the cyclic unit vector. These are self-adjoint projections on the GNS domain. By (1), (3), and exchangeability,

    ⟨Ω,P_iΩ⟩=⟨Ω,Q_jΩ⟩=½,
    ⟨Ω,P_iQ_jΩ⟩=⟨Ω,Q_jP_iΩ⟩=½            whenever i≠j.

Therefore

    ||P_iΩ−Q_jΩ||²=½+½−½−½=0               whenever i≠j.       (4)

For any two indices i,k, choose j distinct from both. Then (4) gives P_iΩ=Q_jΩ=P_kΩ. For any j choose i≠j to obtain Q_jΩ=P_iΩ as well. Thus all P_iΩ and all Q_jΩ are one common vector v₀.

If R is any P_i or Q_i, then RΩ=v₀ and, because R²=R,

    Rv₀=R²Ω=RΩ=v₀.                                           (5)

Inductively, every nonempty word R₁⋯R_m in these generators sends Ω to v₀. Its ω-moment is thus ⟨Ω,v₀⟩=½. These words and 1 span the algebraic free product, because 1,p,q,pq span each copy of A.

Let χ₀ and χ₁ be the characters on F(A) obtained by evaluation at 00 and at 11, respectively, in every copy. They are positive unital exchangeable states. Every nonempty word in the p- and q-generators has χ₀-value 0 and χ₁-value 1. The preceding moment computation proves the identity of states

    ω=½χ₀+½χ₁.                                                (6)

For the C*-free product, equality on the dense algebraic free product extends by continuity. The states in (6) differ on j_1(p), so ω is not extremal exchangeable. Every possible witness was covered; hence no extremal witness exists in A.

Notice that checking only that one natural witness is nonextremal would not suffice. Equations (4)–(6) prove uniqueness of the possible witness and exclude all alternatives.

### 3.2 A pure witness after embedding A into M₄

Embed A as the diagonal matrices in the specified point order. Write e_00 and e_11 for the corresponding standard basis vectors and put

    v=(e_00+e_11)/√2,            φ′(T)=v*Tv.

Then φ′ restricted to A is exactly φ. The state φ′ is pure by Lemma 2.2. Let

    ω′=φ′∘q_{M₄}

on F(M₄). Lemma 2.1 makes ω′ pure among all states, and folding makes it exchangeable. In particular it is an extreme exchangeable state.

For any word w in B*C, folding its B-letters placed in copy 1 and C-letters placed in copy 2 simply multiplies the original matrices in their original order. Since those matrices lie in A,

    ω′(((j_1|_B)*(j_2|_C))(w))
       = φ′((ι_B*ι_C)(w))
       = φ((ι_B*ι_C)(w)).                                    (7)

This proves the full state identity (1), not merely its degree-two consequences. Also ω′∘j_n=φ′ for every n. Thus B,C are independent upstairs. Together with Section 3.1 this proves Theorem 1. ∎

One can see the change of extremality directly: restriction of ω′ to F(A) is exactly (6). The same state is pure upstairs and a nontrivial exchangeable mixture downstairs. There is no contradiction, since restriction of a pure state to a subalgebra need not be pure or extremal invariant.

## 4. A smaller example and exact scope

If coincident subalgebras are allowed, the example reduces to A=B=C=C² diagonally embedded in M₂. Use φ(a,b)=(a+b)/2 and its pure extension associated with (1,1)/√2. Writing r=(0,1), equation (1) forces ω(r_i)=ω(r_i r_j)=½ for i≠j. Thus (r_i−r_j)Ω=0; the same induction gives the unique state ½χ₀+½χ₁ downstairs. Pure folding supplies the witness upstairs. This version has a faithful state on the smaller algebra. The main four-point construction avoids coincident subalgebras entirely.

The source uses unqualified states. The larger-algebra vector state is not faithful, and the four-point state is not faithful; neither property is required by the printed definition. The theorem does not resolve modifications requiring faithful states everywhere, extremality only within a fixed-marginal slice, tracial witnesses only, a trivial tail algebra, or exclusively commutative ambient extensions. Those are different definitions. The larger ambient states here are normal (finite-dimensional), but the note does not posit any particular W*-free-product convention.

If one merely requires the witness to have the prescribed full marginal, both examples still meet that additional condition. If instead one changes the **convex set in which extremality is tested**, the nontrivial components χ₀,χ₁ no longer share the prescribed mixed marginal, so the nonextremality argument cannot be reused. This distinction is essential.

## 5. The source's literal non-lifting concern in the algebraic category

The report motivates ambient dependence by a possible failure of extreme exchangeable state extension. This is a stronger and directionally different concern from the restriction failure in Theorem 1. Here is a separate example proving that the concern can occur for algebraic *-algebras.

Let R=C[x] with x*=x, and let S=C[x,x⁻¹] with (x⁻¹)*=x⁻¹. The inclusion R⊂S is unital and injective. Evaluation at 0 is a character on R; applying it to every copy gives a character χ on F(R), which is pure by Lemma 2.1 applied to its quotient onto C. It is exchangeable.

Suppose a positive unital state η on F(S) restricted to χ. In the first copy set X=j_1(x) and Y=j_1(x⁻¹). Then

    X*=X,     Y*=Y,     XY=1,     η(X²)=0.

Cauchy–Schwarz gives

    1=|η(XY)|² ≤ η(X²)η(Y²)=0,

a contradiction. Thus χ has no positive extension at all, and in particular no extreme exchangeable extension. Both R and S themselves admit states, e.g. evaluation at 1, so the ambient inclusion can also be viewed as an inclusion of algebraic probability spaces using that common marginal. The nonextendible χ is not that marginal; the assertion concerns the source's unrestricted sets of extreme exchangeable states.

This polynomial example is not a C*-algebra counterexample. In fact, for an equivariant unital inclusion D⊂E of C*-algebras with an action of the locally finite permutation group, every extreme invariant state of D has an extreme invariant extension to E. To see this, extend the state to E by the ordinary C*-state extension theorem. Average that extension over the finite symmetric groups S_n and take a weak-* cluster point; the result is invariant and still restricts to the original state. The compact convex fiber of invariant extensions is nonempty. If the original invariant state is extreme, this fiber is a face of the invariant state space of E. An extreme point of the fiber (by the compact-convex extreme-point theorem) is therefore extreme in that whole space. This argument uses C*-state extension and compactness, which are absent for arbitrary algebraic *-algebras.

Only these standard C*-facts enter the last contextual paragraph; neither counterexample depends on them. In particular the existence of extreme extensions in a C*-setting would not imply ambient invariance, because Theorem 1 exhibits the opposite-direction failure under restriction.

## 6. Attribution and verification

The pure-folding construction is established mathematics: [2, Proposition 8.7] treats it within quantum symmetric states, and [2, Theorem 8.1] relates that extremality to extremality in the ordinary symmetric-state space. The present argument proves the necessary special case directly, without importing the paper's classification or tail-algebra machinery. The GNS moment collapse and Laurent-polynomial Cauchy–Schwarz obstruction are elementary. No claim is made that these observations or their application to Liebscher's question are historically new.

The exact script verify.py checks the four-point algebra, its subalgebras, the matrix density projection, moments of finite words, the two-character decomposition, and finite instances of the projection-collapse identities. These are auxiliary controls. The proof for every word, every copy, and all candidate states is Sections 2–3; no finite search certifies those quantifiers.

### References

[1] Volkmar Liebscher, “On Quantum Independence,” open-problem contribution, pp. 540–541, in B.V.R. Bhat, Uwe Franz and Michael Skeide (organizers), *Mini-Workshop: Product Systems and Independence in Quantum Dynamics*, Oberwolfach Reports 6 (2009), pp. 493–548. [DOI 10.4171/OWR/2009/09](https://doi.org/10.4171/OWR/2009/09). [Official report](https://publications.mfo.de/bitstream/handle/mfo/3111/OWR_2009_09.pdf?isAllowed=y&sequence=1).

[2] Kenneth J. Dykema, Claus Köstler and John D. Williams, *Quantum symmetric states on free product C*-algebras*, Trans. Amer. Math. Soc. 369 (2017), 645–679. [DOI 10.1090/tran6661](https://doi.org/10.1090/tran6661). [Author preprint, v3](https://arxiv.org/abs/1305.7293v3), Proposition 8.7 and Theorem 8.1.
