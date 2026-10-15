# Exact translation from regular multiplication matrices to earlier criteria

Audit date: 2026-10-01 UTC. This derivation was established before reading any exact-question priority verdict. It is an independent reconstruction of the mechanism, not a claim that the following notation appeared verbatim in an earlier paper.

## Target and assumptions

Let `P=C[x_1,...,x_d]`, let `I` be proper of finite positive colength `N`, and let the `M_i` be the regular multiplication representation on `A=P/I` in any common basis. The target is `I` generated globally by exactly `d` polynomials, the condition in Shekhtman's 2015 Definition 5. No degree-form, homogenization, reducedness, or smoothability condition is included.

The following two translations provide finite characterizations in terms of these matrices. Neither relies on the candidate's `D_2`-rank theorem. They use earlier local complete-intersection tests and Mohan Kumar's global theorem.

## A. Recover the exact polynomial input of KLR Algorithm 3.6

Define the matrix algebra

`B=C[M_1,...,M_d] ⊆ Mat_N(C)`.

The map `A→B` sending `a` to multiplication by `a` is injective: an operator which is zero sends `1` to zero. It is onto by definition. Hence `B≅A`, `dim_C(B)=N`, and

`I = ker(P→B, f↦f(M_1,...,M_d))`.

This argument uses the regular-representation hypothesis, but does not require that the coordinates of `1∈A` be supplied.

Choose a degree-compatible multiplicative monomial order. Enumerate monomials in increasing order and retain each `t` exactly when `t(M)` is linearly independent of the previously retained evaluations. The retained monomials form an order ideal `O`, meaning it is closed under divisors. Indeed, if `t(M)` depends on earlier evaluations, multiplication by any `M_i` expresses `(x_i t)(M)` through evaluations of monomials earlier than `x_i t`; dependence therefore propagates to multiples. Thus a retained monomial has retained divisors.

This is finite. Let `F_e` be the span of matrix evaluations of monomials of degree at most `e`. If `F_e=F_{e+1}`, then every `M_i F_e⊆F_e`, so `F_e=B`. Until that happens the dimension strictly increases from `dim F_0=1`. Consequently `F_{N-1}=B`. Enumerating degrees through `N-1` recovers exactly `N` independent monomial evaluations.

For each border monomial `b∈∂O=(⋃_i x_i O)\O`, solve the finite linear system

`b(M)=Σ_{t∈O} c_{bt} t(M)`.

Set `g_b=b−Σ_t c_{bt}t`. These are in `I`, and they generate `I`. One verification is terminating monomial division: the coefficients of any `t>b` vanish, since `b(M)` already lies in the span of earlier retained monomials. Thus every `g_b` has leading term `b`. A monomial outside the divisor-closed `O` is divisible by a border monomial; division reduces every polynomial modulo `(g_b)` to the span of `O`. The quotient by `(g_b)` therefore has dimension at most `N`. Its surjection to `P/I`, in which `O` is independent of dimension `N`, is an isomorphism. This proves exact equality of the ideals, including nilpotents and every support component.

Now apply the already-published KLR Algorithm 3.6 to this recovered presentation. Its primary components are the exact `I`-components, not the components of `sqrt(I)`. At a point `λ`, the maximal ideal has the regular sequence `x_1−λ_1,...,x_d−λ_d`; the local criterion tests whether its primary component is CI. Every operation uses the recovered coefficients and hence is determined by the original `M_i`.

KLR Algorithm 3.6 returns all-local-CI. The next subsection proves that this output is exactly the global target over the stated polynomial ring.

## B. An entirely matrix-based version of the older Wiebe test

One can use Wiebe's criterion directly, without reconstructing polynomial generators or a primary decomposition.

Recover a basis `B_1,...,B_N` of `B` as above, with `B_1=Id`. For each joint support point `λ`, set `T_i=M_i−λ_i Id`. Define a linear map

`E_λ:C^{dN}→Mat_N(C)`,

`(c_it)↦Σ_{i=1}^d Σ_{t=1}^N c_it T_i B_t`.

Compute a `C`-basis `z^(1),...,z^(r)` of its kernel. For every column `α` set

`U_{iα}=Σ_t z^(α)_{it} B_t∈B`.

These entries commute, and `Σ_i T_i U_{iα}=0`. Let `U_λ` be the `d×r` matrix with entries in the commutative ring `B`. For any `d` distinct columns `α_1,...,α_d`, its determinant is the usual alternating sum of products of the commuting `N×N` matrices `U_{iα_j}`. Denote that resulting `N×N` matrix by `Δ_{λ;α_1,...,α_d}`.

The earlier-criterion matrix characterization is:

> `I` is generated globally by `d` polynomials if and only if, for each joint support point `λ`, at least one `Δ_{λ;α_1,...,α_d}` is nonzero.

Proof of the local step: let `J_λ=(T_1,...,T_d)B`. The map `B^d→J_λ` is onto. Its kernel is exactly the coefficient kernel used above. A `C`-basis of this kernel also generates it over `B`, since its scalar coefficients already belong to `B`. Thus

`B^r --U_λ→ B^d → J_λ →0`

is a finite module presentation. The determinant matrices generate `Fitt_0^B(J_λ)`. Their matrix nonzeroness is their algebra nonzeroness because `B` is represented faithfully.

Write the Artinian algebra as `B=∏_{η∈V(I)} B_η`. At `η=λ`, the ideal `J_λ B_λ` is the maximal ideal of `B_λ`. At `η≠λ`, one coordinate difference `η_i−λ_i` is nonzero, so `T_i` is a unit in `B_η` and `J_λB_η=B_η`. The zeroth Fitting ideal of the free rank-one module `B_η` is zero. Fitting ideals commute with localization. Therefore `Fitt_0^B(J_λ)` is nonzero precisely when the zeroth Fitting ideal of the maximal ideal of `B_λ` is nonzero.

[Wiebe's original Satz 3](https://gdz.sub.uni-goettingen.de/download/pdf/PPN235181684_0179/LOG_0075.pdf), printed p. 260 (1969), says that this last condition is equivalent to `B_λ` being a zero-dimensional local complete intersection. No minimality requirement on the chosen `d` coordinate generators enters the Fitting definition. This also follows explicitly from [Simon–Strooker Theorem 2.4 and Corollary 2.7](https://arxiv.org/pdf/math/0703880) (2007), which permit nonminimal maximal-ideal generators. The equivalence with `I P_m` being generated by a regular sequence in the given ambient polynomial local ring is also explicit in [KLR Proposition 3.2](https://arxiv.org/pdf/1903.09563v1), p. 8. Thus an intrinsically CI quotient has not been substituted for a different fixed-embedding condition.

The joint support is itself matrix-determined: it is the finite set of `λ` for which `[T_1 ... T_d]` has rank below `N`. In the regular representation, the cokernel is `A/(x_1−λ_1,...,x_d−λ_d)A`, which is `C` at support and zero elsewhere. Thus `rank E_λ=N−1` at support and `r=(d−1)N+1`. Nilpotent parts have never been discarded.

## C. The exact global bridge, already published in 1978

[Mohan Kumar's original Theorem 4](https://gdz.sub.uni-goettingen.de/download/pdf/PPN356556735_0046/LOG_0020.pdf), printed p. 234, applies to any locally complete-intersection ideal in a polynomial ring over a field and bounds its global number of generators by the number of variables. Apply it to `I⊂C[x_1,...,x_d]`. Since `ht(I)=d`, the height theorem gives the reverse inequality. Therefore

`all local factors CI ⇔ I locally CI ⇔ μ_P(I)=d`.

For the reverse implication, `d` global generators localize to at most `d` generators of an ideal primary to a maximal ideal in a regular local ring of dimension `d`. Such a system of parameters is a regular sequence, so every local factor is CI.

This closes the global step without assuming local CI automatically implies global CI in arbitrary affine rings. It covers `d=1` as well. Independently, Theorem 5 on the same page closes the candidate's stronger arbitrary-generator-count formula in its stable range; that additional formula is not needed for the Boolean target here.

## D. Kähler-different translation in characteristic zero

There is a second prior local test in [KLR Remark 5.6(e)](https://arxiv.org/pdf/1903.09563v1), p. 22. Starting from the exact border generators in A, compute the maximal Jacobian minors `h_j` and evaluate `h_j(M)`. For each principal idempotent `e_λ∈B` of a support factor, check that some `e_λ h_j(M)` is nonzero. Equivalently, the ideal generated by these evaluated minors has nonzero image in every local factor. This is the local-CI test in characteristic zero and hence, by C, answers the same global question. The projective/strict variants of the different test must not be substituted for this local affine version.

## What is and is not concluded

An earlier equivalent solution mechanism is explicit and checkable. The first route uses the published 2019 algorithm (2022 journal publication), the second uses the original 1969 theorem, and the common global bridge is original 1978. The matrix-only route does not depend on an allegedly novel block formula or on a conjectural global theorem.

No assertion is made that Wiebe, Mohan Kumar, or KLR referred to Shekhtman's named 2015 problem. No earlier source with the candidate's exact `D_2` block notation was located in this bounded audit. An explicit convenient rank formulation may still be useful exposition or an implementation improvement. That is different from a first resolution of the underlying characterization problem.

The word algorithm presumes exact arithmetic and the ordinary effective coefficient/root operations used by the prior algebraic algorithms. For arbitrary uneffectively specified complex entries this is a finite mathematical criterion, as is the candidate's rank-at-all-support-points statement; no extra numerical decidability claim is made. The regular multiplication hypothesis is essential throughout, and the result is not asserted for an arbitrary commuting tuple.

Executable consistency check: `python3 priority/equivalent_methods/check_prior_translation.py`. Its eight exact cases include similarity invariance, nilpotents, multiple supports, affine CI failing the strict condition, and Gorenstein failing CI. They corroborate the translation; the proofs above establish the general statement.
