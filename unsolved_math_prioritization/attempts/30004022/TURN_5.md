# Turn 5: tail-controlled extension of the matrix construction to arbitrary laws

**Final author disposition: original source problem unresolved, five of five substantive turns complete.** This turn removes the bounded-input restriction from the matrix-valued workaround by an explicit truncation estimate. It does not produce the requested new scalar/positive-factor representation. The existing general linearization/subordination method remains credited, and no novelty certification is made.

## 1. Unbounded variables and the meaning of the commutator

Realize arbitrary Borel probability measures mu_a,mu_b on R as free self-adjoint affiliated operators a,b in a faithful finite tracial von Neumann algebra, with trace normalized to one. One can use the reduced free product of the two commutative probability spaces. The affiliated measurable operators form a *-algebra under closures of sums and products. Consequently c=i(ab-ba), formed in that algebra, is self-adjoint and has a probability distribution even without moments.

The affiliated-operator algebra fact is standard Murray–von Neumann theory. An explicit source checked here is [Ando–Matsuzawa, Existence of infinite-dimensional Lie algebra for a unitary group on a Hilbert space and related aspects](https://www.impan.pl/shop/en/publication/transaction/download/product/86036), Section 2. No unrestricted sum/product of arbitrary closed operators on an unrelated Hilbert space is assumed to have these properties.

Define clipping by f_T(x)=max(-T,min(x,T)), T>0. Put a_T=f_T(a), b_T=f_T(b), and c_T=i(a_T b_T-b_T a_T). Functional calculus preserves the freeness of the two input algebras; ||a_T||,||b_T||<=T. The clipped laws are determined separately from mu_a and mu_b. Set

    q_a(T)=mu_a({x:|x|>T}),
    q_b(T)=mu_b({x:|x|>T}),
    delta_T=min(1,2q_a(T)+2q_b(T)).

The strict tail convention is important: clipping changes no mass at x=+/-T.

## 2. Rank control in the finite tracial algebra

For an affiliated operator X let rk_tau(X) be the trace of its range support, equivalently the trace of the support of |X|. Equality follows from polar decomposition. The elementary support inequalities are

    rk_tau(X+Y) <= rk_tau(X)+rk_tau(Y),
    rk_tau(XY) <= min(rk_tau(X),rk_tau(Y)).       (1)

The first follows because the range of a sum lies in the closed sum of the ranges. The bound by rk_tau(X) in the product follows from range containment, and the bound by rk_tau(Y) follows by passing to adjoints and using equality of left and right support traces. These statements extend to affiliated products through their closed ranges and the *-algebra structure. In particular they do not require finite moments.

The exact algebraic identity

    c-c_T=i[(a-a_T)b-b(a-a_T)
                +a_T(b-b_T)-(b-b_T)a_T]

and (1) show

    rk_tau(c-c_T) <= delta_T,                   (2)

because rk_tau(a-a_T)=q_a(T) and likewise for b. Using the sum of two commutator differences, rather than bounding four independent tails, is what supplies the stated coefficient two.

## 3. A Cauchy-transform estimate without moment assumptions

For any two self-adjoint affiliated operators H,K and z with eta=Im(z)>0, their resolvents R_H=(z-H)^(-1), R_K=(z-K)^(-1) are bounded by 1/eta. The resolvent identity in the affiliated algebra gives

    R_H-R_K=R_H(H-K)R_K.

Thus the difference has rank at most rk_tau(H-K) by (1), and operator norm at most 2/eta by the triangle inequality. For a bounded operator V,

    |trace(V)| <= trace(|V|) <= ||V|| rk_tau(V).

Combining these observations with (2) proves the uniform bound

    |G_c(z)-G_c_T(z)| <= 2 delta_T / eta.       (3)

This proof does not use a density, a moment expansion, a matrix approximation, or a spectral-distribution convergence theorem. It applies to arbitrary self-adjoint affiliated inputs; freeness is needed only for recovering G_c_T from the separate clipped laws.

## 4. Explicit matrix representation with two controlled limits

For the clipped laws, use Turn 4's three-by-three pencil and credited subordination fixed point. Denote its exact regularized output by

    H_(T,epsilon)(z)
      = [G_(M tensor a_T + N tensor b_T)
                   (Lambda_epsilon(z)-Q0)]_11.

The subordination theorem computes this from the two clipped input measures as a convergent matrix fixed-point limit. Combining (3) with Turn 4's bound, using A=B=T, gives

    |G_c(z)-H_(T,epsilon)(z)|
      <= 2 delta_T/eta
           + 2T^2(epsilon^2+epsilon)
                    /[(1+epsilon^2)eta^2].      (4)

Both terms are explicit from the input tail masses, T, epsilon and eta. For example, for T>=1 choose epsilon=T^(-3). Then

    |G_c(z)-H_(T,T^(-3))(z)|
      <= 2 delta_T/eta + 2(T^(-4)+T^(-1))/eta^2,

which tends to zero for every eta>0, because probability tails tend to zero. The convergence is uniform on Im(z)>=eta_0>0. Thus an explicit fixed-size matrix construction recovers the commutator Cauchy transform for arbitrary Borel input laws, without assuming a variance or any moment.

The inner fixed-point limit must be taken for each fixed T,epsilon before the outer T limit. No statement here bounds a finite number of matrix fixed-point iterations or permits exchanging those limits without control. A finite numerical output would additionally need a certified fixed-point error and controlled evaluation of the input integrals. The representation and estimate (4) are mathematical statements, not an implementation claim for an arbitrary measure supplied without an effective oracle.

## 5. Why this still does not resolve the exact source request

The source contribution already knows general commutator characterizations and seeks extension of particular positive-factor and scalar analytic representations beyond their symmetry/free-square-root restrictions. A larger matrix system obtained from pre-existing general polynomial machinery does not automatically provide that extension. Turns 1–3 show that two unchanged continuations are in fact impossible; Turn 5 supplies a rigorously controlled alternative in a broader representation class. No reduction of this system to the requested new scalar structure is established.

Accordingly this work does not claim a complete positive or negative answer to every possible reformulation intended by the source. The precise remaining gap is a suitable genuinely nonsymmetric scalar representation with justified analytic mapping, normalization and uniqueness properties, or a rigorous full-target impossibility theorem covering the allowed revised representation class. Neither is present.

## 6. Boundary cases, tests and final scope

- If both input laws are supported in [-T,T], delta_T=0 and (4) reduces exactly to the bounded regularization estimate
- If an input is deterministic, the commutator is zero; clipping and all bounds remain valid without division by variance
- Atoms at +/-T do not enter the tails; atoms outside do, regardless of how large their locations are
- The tail/rank estimate is independent of freeness and survives arbitrarily large outliers. Its use in the representation is combined only afterward with preserved freeness of clipped inputs
- No claim about pointwise real-axis densities or support recovery follows uniformly as eta down to zero

`verify_turn5.py` checks exact clipping, commutator-difference and resolvent identities, finite-dimensional rank controls, rational Cauchy-transform bounds, boundary atoms and the one-parameter regularization schedule. Those matrices test only deterministic identities and inequalities; they are not asserted to be free. The affiliated-operator proof and the existing subordination theorem carry the infinite-dimensional statement.

Final best-guess completion toward the original source goal: 25%, low confidence. Five genuine turns have been used. The author packet is to be frozen for independent source/proof review; no sixth search turn is authorized by this packet. Proposed original disposition is **unsolved, 5/5**, with the precise scoped claims above.
