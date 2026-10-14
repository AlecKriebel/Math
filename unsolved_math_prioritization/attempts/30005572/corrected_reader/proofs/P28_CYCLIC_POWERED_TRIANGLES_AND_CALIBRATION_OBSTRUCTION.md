# Exact cyclic-powered triangles and a geometric calibration obstruction

14 October 2026. FINAL shared PASS5/5, row 1777 / 30005572. Coefficients are R = Z[1/6]. This is a partial result, not a solution of the frozen construction contract. No novelty claim is made.

## 1. Results

1. For every positive integer n and every point P of exact order n on a characteristic-zero elliptic curve, the accepted scalar-powered values U_n satisfy every nondegenerate cyclic triangle exactly in K2(k) tensor R. The order-seven result extends to every cyclic order, without inverting any level prime. An explicit finite sum of Steinberg wedges witnesses the identity. The cancellation occurs in the exterior square of a universal unit group before specialization, never in K2.
2. There is a structural obstruction to a direct geometric endpoint-primitive construction on a CM square. For every nonzero ideal c, coordinate projection is injective on the SL2(O)-invariant finite cycles supported on E[c]^2. Consequently no nonzero invariant torsion cycle can be a sum of external products of degree-zero divisors. In particular the standard auxiliary cycle cannot acquire a fiber-supported cusp primitive by adding corrections of this form. This addresses an attempted route to the actual shear comparison, rather than constructing another zero-absolute relative map.
3. For the valid unpowered CM levels, the genuine ray field has no retained root-of-unity torsion at primes dividing the level exponent. Thus unit-root ambiguity is absent there. Nevertheless it is not legitimate to cancel the level in K2. At cyclic order seven the cross-ratio/evenness calculus alone has a genuine residual quotient of order seven. These are precise bounds on the remaining method, not nonvanishing of the actual CM triangle.

The moved/sheared geometric cocycle has not been compared with the prescribed unpowered pair on all balanced absolute chains. No all-component relative homology map, unpowered all-level triangle, or full-contract solution is claimed.

## 2. Accepted inputs and conventions

Use the exact definitions, family-unit specialization, evenness, and cross-ratio identities in the accepted PASS3 proof `INTEGRAL_THETA_NORMALIZATION_AND_RELATIONS.md`. In particular U_n is defined using scalar auxiliary functions and a Bezout identity after proving exchange over Q(Y1(e)); the withdrawn divided CM-powered construction is not used.

Write multiplicative groups additively. For an even unit-valued system h on a finite group G, put h(0)=0 for bookkeeping only, not as a theta evaluation. Set

    B_h(x,y) = h(x+y)+h(x-y),
    Psi_h(a,b) = h(a) wedge h(b) + h(b) wedge h(-a-b)
                 + h(-a-b) wedge h(a),
    phi_h(x,y,z) = B_h(z,x) wedge B_h(y,x)
                   + B_h(y,x) wedge B_h(z,y)
                   + B_h(z,y) wedge B_h(z,x).

For four points define

    M_h(a,b,c,d) = B_h(c,a)+B_h(d,b)-B_h(c,b)-B_h(d,a),
    delta_h(a,b,c,d) = M_h(a,b,c,d) wedge M_h(a,c,b,d).

If the four points are pairwise distinct modulo sign, let

    u(a,b,c,d) = ((x(c)-x(a))(x(d)-x(b)))
                / ((x(c)-x(b))(x(d)-x(a))),

with the usual limiting interpretation for x(0)=infinity. The accepted identity is

    M_(U_n)(a,b,c,d) = n [u(a,b,c,d)].                 (2.1)

Here the square brackets mean the unit viewed in additive notation. Moreover 1-u(a,b,c,d)=u(a,c,b,d). If sign classes repeat, delta_h is identically zero for every even h, by direct bilinear expansion. No cross-ratio at a degenerate quadruple will be evaluated.

All symbol identities use the usual alternating Milnor symbol after tensoring with R. They do not alter the prior source inverse-tame sign convention for geometric cocycles. The support argument below is in degrees zero and one, where that degree-two sign conversion is irrelevant.

## 3. An explicit finite exterior-square identity

Let G be any finite abelian group of size g. For fixed a,b let c=-a-b. The accepted free-exterior identities give

    sum_d delta_h(A,B,C,d) = g phi_h(A,B,C),           (3.1)

    sum_x phi_h(x,-b-x,a-x)
       = g Psi_h(a,b) + R_c(a)+R_b(c)+R_a(b),         (3.2)

    4 R_u(v) = sum_x phi_h(0,v,u+2x),
    R_u(v) = sum_x Psi_h(u+2x,v).                     (3.3)

For completeness, (3.1) follows by summing

    delta_h(A,B,C,d) = phi_h(A,B,C)+phi_h(C,d,A)
                      +phi_h(B,A,d)+phi_h(d,C,B),

and using sum_x phi_h(x,y,z)=0. The cancellation uses translation, evenness, antisymmetry and division by two only. Equations (3.2)-(3.3) are direct bilinear expansions; these are identities in the exterior square before imposing Steinberg relations.

Multiplying (3.2) by g and substituting (3.1) and (3.3) gives the exact identity

    g^2 Psi_h(a,b)
      = sum_(x,d) delta_h(x,-b-x,a-x,d)
        - (1/4) sum_((u,v)=(c,a),(b,c),(a,b))
                     sum_(x,d) delta_h(0,v,u+2x,d).   (3.4)

The sums include all x,d in G. There is no division by g.

Define beta(A,B,C,D) to be [u(A,B,C,D)] wedge [1-u(A,B,C,D)] when the four sign classes are distinct, and zero otherwise. Define W(a,b) by the right side of (3.4), replacing every delta_h by beta. Thus W is an explicit R-linear sum of Steinberg wedges, with coefficients 1 and -1/4 only.

## 4. Exact triangle theorem for every scalar-powered cyclic system

### Theorem 4.1

Let E/k be an elliptic curve over a characteristic-zero field, and let P in E(k) have exact order n. For a,b in Z/n with a,b,a+b nonzero, the actual accepted values satisfy

    {U_n(aP),U_n(bP)} + {U_n(bP),U_n((-a-b)P)}
       + {U_n((-a-b)P),U_n(aP)} = 0
                      in K2(k) tensor R.             (4.1)

More strongly, there is the exterior-square Steinberg witness Psi_(U_n)(a,b)=W(a,b). It specializes at every such elliptic curve, including fields containing arbitrary level-primary roots of unity.

### Proof

For n=1 there is no nondegenerate triangle. For n=2 or 3 there is no triangle with three distinct nonzero sign classes, so evenness and alternation give the assertion directly. Assume n>=4.

Work on the universal exact-order-n pair over K=Q(Y1(n)). This modular curve is geometrically integral over Q, and K has constant field Q. The group K^times/{1,-1} is free abelian: on a smooth projective model the divisor map has kernel Q^times, its image is a subgroup of a free divisor group and hence free, and Q^times/{1,-1} is free on the rational primes. The resulting short exact sequence splits as abelian groups. Therefore K^times tensor R is free over R, and its exterior square over R is torsion-free.

Apply (3.4) to G=Z/n and h(a)=U_n(aP). For each nondegenerate quadruple, (2.1) and its 1-u counterpart give

    delta_(U_n)(A,B,C,D) = n^2 beta(A,B,C,D).

The same equation holds for a degenerate quadruple because both sides were defined to be zero. Since |G|=n, (3.4) becomes

    n^2 Psi_(U_n)(a,b) = n^2 W(a,b).

Cancellation in the torsion-free universal exterior square, BEFORE quotienting by Steinberg relations, yields

    Psi_(U_n)(a,b)=W(a,b).                            (4.2)

All participating U_n values and all nondegenerate cross-ratios are units on Y1(n). The former is the accepted family-unit property; for the latter, distinct sign classes have distinct x-coordinates on every smooth elliptic fiber. Thus (4.2) specializes at every characteristic-zero exact-order-n moduli point. Equivalently, one can carry out the same torsion-free cancellation in the submodule of units regular at that point before applying the evaluation homomorphism. Passing to K2 kills every term in W by the Steinberg relation, proving (4.1).

The target field k need not have torsion-free units or torsion-free K2. No cancellation is performed there. In particular no seventh root, arbitrary K2 division, or general CM-powered value is introduced.

If n divides m, the accepted U_m=(m/n)U_n identity shows that all triangles of U_m on this cyclic subgroup vanish as well.

### Scope of the improvement

The PASS3 proof established exact scalar-powered triangles only at order seven, in addition to unpowered 2,3-primary cases. Theorem 4.1 gives the scalar-powered triangle for every cyclic order, with an explicit integral Steinberg witness. It does not imply the unpowered triangle: where U_n=n theta exists, it gives n^2 Psi_theta=0. Cancellation in K2 would still be a new, unjustified step.

The cyclic hypothesis is used exactly at |G|=n and at the rational constant field of Y1(n). It is not silently extended to a rank-two marked torsion group, whose modular parameter space can have cyclotomic constants and whose cardinality is different from its exponent.

## 5. An obstruction to external-product geometric calibration

This section concerns the same-curve product E x E with maximal CM by O and the full geometric group SL2(O). It does not assert that arbitrary smaller congruence groups or mixed-component groups have the same invariant cycles.

Let c be a nonzero proper ideal and T=O/c. After passing to an algebraic closure, identify E[c] with the free rank-one T-module. Write R[T^2] for the free R-module on the torsion points. Coordinate projection induces

    pi_*: R[T^2] -> R[T],    [x,y] -> [y].

### Theorem 5.1: invariant projection is injective

The restriction of pi_* to R[T^2]^(SL2(T)) is injective. The same assertion holds for invariants under the actual reduction of SL2(O).

### Proof for a prime power

Let T=O/q^r and Q=Norm(q). The SL2(T)-orbits on T^2 are indexed by

    j=min(v_q(x),v_q(y)),  0<=j<=r,

where j=r denotes (0,0). Indeed a primitive row can be completed to determinant one over the local ring, and multiplying by a fixed uniformizer power gives the other orbits. Let a_j be the coefficient at each point in orbit j.

For y of valuation k<r, the coefficient b_k of [y] in pi_* is

    b_k = sum_(j<k) (Q-1)Q^(r-j-1) a_j + Q^(r-k) a_k.

For y=0,

    b_r = sum_(j<r) (Q-1)Q^(r-j-1) a_j + a_r.

This is a lower-triangular map on orbit coefficients with diagonal entries Q^r,Q^(r-1),...,Q,1. They are nonzero divisors in R. If every b_k is zero, successive substitution gives every a_j=0. No Q is inverted.

### General ideal and actual geometric reduction

For c=product q^r, CRT identifies T with the product of the local rings. Both the orbit indexing and projection matrix are the products of the local constructions. The resulting matrix is the tensor product of the injective local matrices and has nonzero determinant over Q, so it is injective over the torsion-free ring R.

Over a finite semilocal ring SL2(T) is generated by elementary matrices: locally Gaussian elimination works because a unimodular row has a unit entry; CRT combines the local elementary factors. Every elementary matrix over T lifts to an elementary matrix over O. Therefore reduction SL2(O)->SL2(T) is surjective, and the asserted invariant modules coincide. This addresses the actual full geometric group, rather than relying only on invariance under an artificially enlarged group.

### Corollary 5.2: no nonzero invariant external-product cycle

Suppose Z is a finite sum of external products D_i x D'_i of degree-zero divisors on E, is supported on E[c]^2, and is SL2(O)-invariant. Then Z=0.

Indeed pi_*(D_i x D'_i)=deg(D_i) D'_i=0, so Theorem 5.1 applies. The individual divisors may have larger supports that cancel in Z; only the final support and invariance are needed. Finite field-extension traces of such expressions also have zero marginal, so do not evade the conclusion.

Every finite torsion support is contained in E[c]^2 for some c. Consequently enlarging the auxiliary torsion support does not remove this obstruction while retaining full SL2(O)-invariance and zero marginals.

For the standard auxiliary cycle with m=Norm(c),

    e_c = m^2[0,0] - [E[c]^2],
    pi_* e_c = m^2[0] - m[E[c]]
               = m(m[0]-[E[c]]) != 0.               (5.1)

The last inequality is an inequality of actual free divisor cycles for a proper c.

A Gersten C1 chain supported only on fibers E x {T} has boundary of pi-projection zero: on each proper elliptic fiber a rational function has divisor of degree zero. For fibers {T} x E the same statement holds for the first-coordinate projection. Since e_c has the same nonzero marginal in both directions, it admits no primitive supported only on fibers of either single coordinate projection. More generally no nonzero full-group invariant torsion smoothing cycle can be built from external products of degree-zero theta divisors so as to support this simple endpoint-primitive method.

### Relevance to the actual comparison

The accepted primitive eta_c deliberately uses two different coordinate directions. Its changes under a swap are exactly calibrated, but its shear changes remain genuine terms. The preceding obstruction shows why replacing eta_c by a finite, fiber-supported, cusp-indexed external-product correction cannot by itself supply the missing shear transition.

Sharifi–Venkatesh's universal elliptic construction, sections 6.3-6.4, uses a corrected product cycle and rational integral matrices. Its invariance group is smaller than the full CM SL2(O); its rank-based torsion orbits cannot simply be treated as invariant under the latter. Theorem 5.1 states the exact finite-cycle obstacle to that direct specialization. It does not prohibit more general moving chains, corrections with other supports, arithmetic specialization identities, or the relative construction in the frozen contract.

## 6. What still survives at an unpowered CM level

### 6.1 No retained level-root ambiguity in the genuine ray field

Suppose the accepted criterion I_N=R holds, and let n be the additive exponent of O/N. For every p>=5 dividing n, p splits as q qbar, with precisely one of q,qbar dividing N. The genuine ray field L=F(N) is unramified at the other prime. But F(mu_p)/F is ramified at that other prime: since p splits in F, the local base is Q_p and adjoining mu_p has ramification degree p-1. Consequently mu_p is not contained in L.

Thus multiplication by n is injective on L^times tensor R. Its possible torsion is the retained part of the finite root-of-unity group, and no prime divisor of n occurs in that part. Whenever the accepted theta values have been descended to this genuine ray field, theta is therefore the UNIQUE solution of U_n=n theta there.

This excludes a unit-root ambiguity in that field. It does not make multiplication by n injective on K2(L) tensor R. The universal cancellation in Theorem 4.1 proves an exterior identity for U_n; it does not divide a Steinberg relation inside the CM field.

### 6.2 A sharp order-seven bound on the cross-ratio method

For G=Z/7 let A=h(P), B=h(2P), C=h(3P). There are exactly four sign classes, namely 0,1,2,3. Up to permutation, every nondegenerate cross-ratio is therefore the one from (0,P,2P,3P). For an unpowered system, its two monomials are

    X=-A+3B-2C,
    Y= 2A+B-3C.

Their wedge is

    X wedge Y = -7 Psi,
    Psi=A wedge B+B wedge C+C wedge A.              (6.1)

Permuting a cross-ratio replaces u by one of u,1-u,1/u,1/(1-u),u/(u-1),(u-1)/u. After -1 is killed in R, each corresponding Steinberg wedge is plus or minus X wedge Y. Degenerate quadruples contribute zero. Therefore the relation submodule generated solely by evenness and these cross-ratio Steinberg wedges is exactly R(7 Psi) inside the free exterior square on A,B,C.

The vector Psi is primitive. Its class in the resulting quotient consequently has exact order seven. Explicitly the functional sending A wedge B to 1 and A wedge C,B wedge C to 0 maps to R/7R, kills every cross-ratio relation, and sends Psi to 1.

This is a nonzero FORMAL quotient, not a nonzero K2 class for an elliptic curve or a CM ray field. Additional Steinberg relations or geometric/arithmetic information can still kill its image. It proves that the finite cross-ratio/evenness calculus alone cannot discharge this remaining unpowered case. Passing to a ray field without mu_7 does not change that formal calculation.

## 7. Final comparison status

The new exact cyclic-powered theorem removes the powered triangle gap in all cyclic orders. The finite-cycle theorem rules out a broad direct external-product approach to the missing full-geometric endpoint primitive. The order-seven quotient identifies a genuinely retained unpowered method obstruction.

What remains unproved is the equality, with the accepted inverse-tame source sign, between the moved arithmetic cocycle and the correctly three-term-smoothed unpowered theta sums on balanced absolute chains. The raw swap value is still not that comparison. Full unpowered odd-level relations, noncyclic markings, nonprincipal component transport, integral absolute values, and all other unmet clauses of the construction contract are not supplied by these results.

This is the final shared mathematical pass. No sixth pass, accepted-proof edit, ledger edit, queue edit, or remote operation was performed in this lane.

## 8. Verification and sources

- Accepted PASS3 input: `pass3_relative_theta/INTEGRAL_THETA_NORMALIZATION_AND_RELATIONS.md`, SHA-256 8c1b6b0877e0b99569da58f99bf7abc112056a5538c16f44d5ce5aec4b1a7534, with its independent acceptance. The present proof uses its already-proved universal scalar values and free-exterior identities, not any withdrawn general CM-powered construction.
- Accepted PASS4 input: `pass4_symbol_calibration/EXACT_SWAP_AND_CYCLIC_FOUR.md`, SHA-256 66165ae9b3288126e9906221329a7d7f896afdd5e4808058fcb54998414e669f, and the independent source-sign clarification.
- Sharifi–Venkatesh, *Eisenstein cocycles in motivic cohomology*, retained primary text, sections 6.3-6.4 and 7.3, https://math.ucla.edu/~sharifi/eisensymbol.pdf . The present comparison describes the support and group of their construction, not an integral Bianchi theorem attributed to that source.
- LSSW, *Eisenstein cocycles for imaginary quadratic fields*, retained primary text, sections 3.1-3.4, https://arxiv.org/pdf/2504.19125v1 . The standard CM auxiliary cycle and full geometric-group setup are used at their stated scope.

The companion checker tests the exact finite exterior identity, the order-seven formal obstruction, and the local/product projection matrices. It supplies algebraic checks; it does not compute a number-field K2 group or claim global homology calibration.
