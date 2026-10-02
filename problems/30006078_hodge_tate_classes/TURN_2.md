# Author turn 2: unweighted vanishing and tensor covariance

**Substantive turn 2/5.** The new mechanism is the filtered flat bundle of Petrov Proposition 5.1 and the tensor-product identity for primitive Lie cocycles. The main results here are restricted to **smooth proper** X over a finite extension K/Q_p. They do not assume good reduction. The original formula remains unproved.

## 1. A credited unweighted consequence

Write E(V)=direct sum_m E_m(V), where E_m=gr^m D_HT(V).

**Proposition.** If V is a Hodge–Tate Q_p-local system on smooth proper X/K, then

    ch(E(V)) = rank(V) in H_dR^{even}(X/K).                         (1)

Only the sum over weights is asserted; the separate E_m may have nonzero positive Chern character.

**Proof.** We use the published construction in Petrov, *Geometrically irreducible p-adic local systems are de Rham up to a twist*, arXiv:2012.13372v3, Theorem 2.4, Proposition 3.5, Lemma 3.6, and Proposition 5.1 (printed pp. 12–13, visually checked). With empty boundary, Proposition 5.1 supplies, over K_infinity, a vector bundle A(V) of rank r with an integrable connection and a finite filtration by subbundles, whose associated graded, after forgetting its grading, is the decompleted Higgs bundle H(V). Its construction only requires integral Hodge–Tate weights; it does not require V to be de Rham.

Extend scalars to C, a completed algebraic closure of K. The Hodge–Tate comparison for V identifies H(V)_C, as an ungraded vector bundle, with E(V)_C: the weight summands differ by constant Tate lines, whose underlying O_{X_C}-line bundles are trivial. This follows also from Theorem 2.4(iv) together with the semisimple integral Sen criterion of Lemma 3.6(ii). Consequently in K_0(X_C),

    [E(V)_C]=[H(V)_C]=[gr A(V)_C]=[A(V)_C].                       (2)

The use of ordinary algebraic K_0 in (2) is justified by proper rigid GAGA. The bundle, finite filtration and connection on the proper analytification algebraize, and the connection is integrable after algebraization. Alternatively the finite algebraic data descend to a finite stage wherever needed before extending to C.

A vector bundle with integrable connection on a smooth characteristic-zero variety has vanishing positive-degree de Rham Chern character. This standard Chern–Weil fact can be checked after spreading the finite algebraic data to a finitely generated characteristic-zero field, embedding that field into the complex numbers, and applying the zero-curvature formula and algebraic/analytic de Rham comparison. Faithful scalar extension descends the zero class. This is a statement about de Rham classes, not rational Chow classes.

Applying this fact to A(V)_C, then (2), gives ch_j(E(V)_C)=0 for j>0. Proper algebraic de Rham cohomology commutes with extension K->C, and the extension of scalars is injective. This proves (1). Components can be treated separately. □

This proposition is recorded as a **consequence of Petrov's existing theorem**, not as a new p-adic comparison theorem. We deliberately state it for proper X: no additional algebraization-at-infinity assertion is needed for the conclusions in this turn.

## 2. Tensor-product identity for the primitive classes

For arbitrary local systems V,W of ranks r,s, respectively, and every i>=1,

    ell_i(V tensor W)=s ell_i(V)+r ell_i(W).                      (3)

For i=1 this is the determinant identity. Here is the cochain calculation for i>1. The differential of the tensor representation is

    (A,B) |-> A tensor I_s + I_r tensor B.

Let q=2i−1. Evaluate the alternating trace cocycle on q such pairs and expand. Pure A terms give s times the A cocycle, and pure B terms give r times the B cocycle. In each mixed term, designate the nonempty subset of arguments supplying A and the nonempty complementary subset supplying B. Matrices in distinct tensor factors commute and the trace factors. Alternation over permutations within the two subsets factors through the alternating trace in a arguments of A and that in b arguments of B, where a+b=q. One of a,b is positive even.

For an even number h of matrices, the alternating trace is zero: cyclically rotating a product leaves its trace unchanged but induces sign (−1)^{h−1}=−1 in the alternating sum. In characteristic zero it cancels with itself. Every mixed term is therefore zero. This proves (3) at Lie-cocycle level. Naturality of Lazard comparison on a small open subgroup and injectivity of restriction with rational coefficients transfer it to continuous cohomology exactly as in turn 1. Stabilizing small ranks is harmless.

The same calculation gives

    ell_i(V dual)= (−1)^i ell_i(V),                              (4)

because the dual differential is A |-> −A^t. Reversal of q arguments has sign (−1)^{q(q−1)/2}; together with (−1)^q this is (−1)^i.

## 3. Weighted Chern characters obey the same law

For a graded bundle define the two finite-degree formal expressions

    C(V)=sum_m ch(E_m(V)),
    T(V)=sum_m m ch(E_m(V)).

The Hodge–Tate functor is tensor-compatible, so E_m(V tensor W) is the direct sum of E_a(V) tensor E_b(W) for a+b=m. Multiplicativity of the Chern character gives, before using (1),

    C(V tensor W)=C(V) C(W),
    T(V tensor W)=T(V) C(W)+C(V) T(W).                            (5)

By (1), for Hodge–Tate V,W on proper X, C(V)=r and C(W)=s. Taking the degree 2(i−1) part in (5) and multiplying by (i−1)! yields

    W_i(V tensor W)=s W_i(V)+r W_i(W).                           (6)

For duals, E_m(V dual)=E_{−m}(V)^dual and ch_j(F dual)=(−1)^j ch_j(F). Therefore

    W_i(V dual)=(−1)^i W_i(V).                                  (7)

For a Tate twist V(t), in the source grading convention E_m(V(t))=E_{m+t}(V). Hence

    W_i(V(t))=W_i(V)−t(i−1)! ch_{i−1}(E(V)).                     (8)

In particular W_i(V(t))=W_i(V) for i>=2. In degree one the correction is −t r, so one must not silently extend that invariance to i=1.

## 4. Consequences for the actual defect

Let

    Delta_i(V)=alpha_X(ell_i(V))−W_i(V).

For smooth proper X and i>=2, the preceding formulas show:

- Delta_i is additive in exact sequences of Hodge–Tate local systems (turn 1).
- Delta_i(V tensor W)=s Delta_i(V)+r Delta_i(W).
- Delta_i(V dual)=(−1)^i Delta_i(V).
- Delta_i(V(t))=Delta_i(V).

Thus the class of systems satisfying the target in a fixed higher degree is closed under extensions, sums, duals, and tensor products. This is not an assertion that every local system is generated by the examples already settled.

If U is a nonzero Hodge–Tate G_K-representation pulled back to X, then turn 1 gives ell_i(U)=W_i(U)=0 for i>=2. Therefore

    Delta_i(V tensor U)=rank(U) Delta_i(V).                      (9)

Tensoring by such an arithmetic factor neither removes nor creates a higher-degree defect. This includes arithmetic Hodge–Tate factors which are not de Rham. Conversely, a proof of the formula after tensoring by one such U implies it before tensoring, by division by its nonzero rank.

For End(V)=V tensor V dual, one obtains

    Delta_i(End(V))=r(1+(−1)^i) Delta_i(V).                       (10)

Consequently an End(V)-reduction detects the defect for **even i** but is identically blind to it for **odd i**. No equivalence in odd i follows from passing to the adjoint or endomorphism local system.

## 5. Why this does not solve the source question

Equation (1) kills the unweighted Chern character, not T(V). A filtration on a flat bundle can have graded terms with nonzero Chern classes which cancel only when the weights are omitted. The identification with A(V) does not identify the arithmetic odd regulator with its weighted graded expression; that is exactly the comparison still required.

In a ring with x^2=0, take a formal two-step graded bundle with ch(E_0)=1+x and ch(E_1)=1−x. Its unweighted Chern character is 2, while the degree-two weighted expression is −x. This simple formal model is a witness to the failure of the inference “unweighted vanishing implies weighted vanishing.” It is not asserted to arise from a p-adic local system, and is not a counterexample to the original problem.

The tensor/dual identities constrain any possible defect, but they supply no value for a genuinely varying geometrically irreducible system. Petrov Theorem 5.2 already makes a Hodge–Tate system with scalar geometric endomorphisms de Rham; this does not calculate its odd classes. There is no claim here that arbitrary systems admit a global decomposition into such systems times arithmetic factors.

**Next route:** quantify the exact information lost by multiplication by the fixed Bloch–Kato class, including the base-field degree and de Rham comparison. Merely repeating cancellation by that class is ruled out.

## 6. Verification scope

The portable verifier independently expands the alternating trace under tensor representations, checks the dual signs, and checks the formal graded Chern-character identities with exact rational arithmetic. It also preserves the nonzero formal weighted example. These finite identities support the algebra, not the published p-adic comparison theorems, which remain explicitly cited dependencies.
