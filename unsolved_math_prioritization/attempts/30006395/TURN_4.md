# Turn 4: a likelihood distribution and exact testing law for fixed c>e

**Partial result: the high-mean-degree square-root window is characterized, but the original mean-degree transition is not.** Author turn 4, 2026-10-01. Unknown uniform labelled-tree mixture throughout. This uses standard Bernoulli Fourier expansions, the moment method, and Gaussian Wick/Hermite identities; no novelty claim.

## 1. Statement

Fix c>e and suppose

    k/sqrt(n)→a∈[0,infinity), p=c/n.

Let L_n=dQ/dP for the unknown-tree experiment. Define

    A(c)=sum_(s≥2) c^(1−s) s^s/s!,
    sigma²=a² A(c).                                (1)

Under the null,

    L_n ⇒ exp(sigma Z−sigma²/2), Z~N(0,1).          (2)

Moreover the first absolute moments converge, so

    TV(P,Q) → 2 Phi(sigma/2)−1,
    optimal sum of testing errors → 2 Phi(−sigma/2). (3)

For finite a, the two sequences of laws are mutually contiguous. When a=0, (2)–(3) reduce to the indistinguishability already proved in Turn 1. For a>0 the limiting total variation is strictly between zero and one: weak detection is possible, while strong detection is impossible.

The square-root-size regime with k/sqrt(n)→infinity remains covered by Turn 1's classical edge-count test. None of these statements asserts a limiting law in Turn 3's c=e window. The fixed-size tree expansion used here loses uniform summability at that point.

## 2. Orthogonal tree and forest coordinates

For each edge e, put

    psi_e=(1_(e∈G)−p)/sqrt(p(1−p)),
    psi_F=product_(e∈F) psi_e.

Under P, the psi_F over all edge subsets are an orthonormal basis. Conditional on a planted tree, the expectation of psi_F is zero unless every edge of F is forced. Hence the Fourier coefficient of L_n is zero for cyclic F, and for a forest with v nonisolated vertices, r components, m=v−r edges and component sizes s_1,...,s_r it is exactly

    ell_n(F)=[(1−p)/p]^(m/2)
       [(k)_v/(n)_v] k^(−m) product_j s_j.         (4)

This is the same classical forest-containment count as Turn 1. Parseval recovers its exact second moment.

Let H be an unlabelled tree with h≥2 vertices and automorphism number aut(H). There are

    N_H(n)=(n)_h/aut(H)

distinct copies as edge sets in the complete graph. Define the normalized connected-tree statistic

    X_(H,n)=N_H(n)^(−1/2) sum_(copies C of H) psi_C. (5)

It has mean zero and variance one, and different tree types are exactly orthogonal. For a finite multiplicity vector m=(m_H), let Y_(m,n) be the sum of products of psi_C over ordered choices of m_H copies of each H, **all vertex-disjoint across all types**, divided by product_H N_H(n)^(m_H/2). This ordered-copy convention is important; the corresponding unlabelled forest has product_H m_H! representations.

## 3. Fixed-degree Gaussian/Wick lemma, with diagram proof

For any fixed finite collection of tree types, the vector (X_(H,n)) converges to independent standard normals (Z_H). For every fixed multiplicity vector,

    Y_(m,n) − product_H He_(m_H)(X_(H,n)) →0 in L²(P), (6)

where He_j is the probabilists' Hermite polynomial, defined by

    exp(tx−t²/2)=sum_(j≥0) He_j(x)t^j/j!.

Here the number and sizes of the tree copies are fixed before n tends to infinity.

### Proof of the fixed-degree lemma

Expand a mixed moment into tuples of connected tree copies. Let r be the total number of tree occurrences in the tuple, counting every component of each Y-factor separately. For one overlap pattern, write v,e,u for the numbers of vertices, edges, and connected components of their union graph. Let b_f be the multiplicity of an edge f in the product.

An edge appearing once has mean zero. For b_f≥2, fixed b_f and p=c/n,

    |E_P psi_f^b_f|=O(n^(b_f/2−1)).               (7)

If the tree occurrences have vertex sizes h_1,...,h_r, the sum of their edge counts is sum_j h_j−r. Counting label assignments and including the normalizations in (5), the contribution of this fixed pattern is therefore

    O(n^[v−e−r/2]).                               (8)

Each union component must contain at least two tree occurrences, or it would have a singly occurring edge. Thus u≤r/2. Every connected graph satisfies vertices−edges≤1, so v−e≤u. The exponent in (8) is nonpositive.

Equality can occur only when the union is a forest, u=r/2, and each union component consists of exactly two occurrences. Their edge sets must then be identical, since no edge can occur once. Thus the only surviving patterns pair identical copies of the same tree type. Each pair contributes covariance one by the exact normalization. Different surviving pairs have disjoint vertices to leading order; the label collisions discarded in this assertion have at least one fewer union component or vertex and belong to the vanishing patterns above.

There are finitely many patterns for a fixed moment. All other patterns are O(n^(−1/2)) or smaller. This proves the Gaussian pairing formula for every joint moment of the X-statistics. The normal distribution is moment-determinate, so the multivariate moment method yields their joint Gaussian limit.

For moments involving Y_(m,n), its disjointness rule forbids a surviving pair between two components inside the same Y-factor. The remaining pairings are exactly the Wick/Hermite pairing formula for product_H He_(m_H)(Z_H). Applying this to the finite expansions of Y², Y times the corresponding Hermite polynomial in X, and the square of that polynomial shows that the L² norm in (6) tends to zero. This argument uses only finitely many moments for each fixed m; it does not invoke moment determinacy of a high-degree polynomial of a Gaussian.

This proves the lemma. The checker includes exact small overlap diagrams and explicit first Wick identities as controls, not substitutes for this general argument.

## 4. Fixed-forest likelihood coefficients

For a forest multiplicity vector m, write v=sum_H m_H h and r=sum_H m_H. Its contribution to the Fourier expansion is theta_(n,m)Y_(m,n), where

    theta_(n,m)=ell_n(F)
         product_H N_H(n)^(m_H/2)/product_H m_H!.

For fixed m and a>0, equation (4) gives

    theta_(n,m) → product_H gamma_H^m_H/m_H!,
    gamma_H=a h c^(−(h−1)/2)/sqrt(aut(H)).          (9)

The same limit is zero for each nonempty m when a=0, but that endpoint is already covered directly by Turn 1.

Cayley's labelled-tree count and orbit-stabilizer give

    sum_(H: |V(H)|=h) 1/aut(H)=h^(h−2)/h!,

so

    sum_H gamma_H²=a² sum_(h≥2)c^(1−h)h^h/h!
                  =sigma²<infinity.               (10)

Let independent normals Z_H be indexed by all finite unlabelled tree types. The Gaussian Hermite expansion with the limiting coefficients in (9) is

    L_infinity=exp(sum_H gamma_H Z_H−sigma²/2).     (11)

The series sum_H gamma_H Z_H converges in L² to N(0,sigma²). The Hermite series of (11) converges in L² as well: the sum of its squared coefficient norms is

    product_H sum_(m≥0) gamma_H^(2m)/m!
      =exp(sigma²)<infinity.

Thus its truncation by total component vertices v≤D tends in L² to (11) as D tends to infinity.

## 5. The uniform tail that permits likelihood convergence

Let L_(n,≤D) be the Fourier projection retaining forests with at most D nonisolated vertices, including the empty forest. Parseval and the exact formula of Turn 1 give

    E_P |L_n−L_(n,≤D)|² = sum_(v>D)^k R(v)b_v,     (12)

where b_v are the coefficients in Turn 3. For 2k≤n, R(v)≤1. Choose any fixed z with

    1<z<c/e.

The nonnegative generating function gives

    sum_(v>D)^k R(v)b_v
      ≤z^(−D) exp[(k²/n) A_c(z)],
    A_c(z)=sum_(s≥2)c^(1−s)(s^s/s!)z^s<infinity.  (13)

The factor rho=(1−c/n)/c was bounded above by 1/c. Since k²/n is bounded, the right side tends to zero uniformly for all sufficiently large n as D tends to infinity.

For fixed D, Sections 3–4 give the convergence in distribution of L_(n,≤D) to the corresponding finite Hermite sum. The uniform L² bound (13) and the Gaussian L² convergence in Section 4 then prove (2), for example by testing against bounded Lipschitz functions and sending n to infinity before D.

This is the substantive difference from simply knowing a nontrivial second-moment limit: the entire likelihood is approximated uniformly by fixed-degree coordinates with a proved joint limit. In particular E_P L_n² is uniformly bounded (indeed it tends to exp(sigma²)), so |L_n−1| is uniformly integrable.

## 6. Total variation, errors, and contiguity

By uniform integrability and (2),

    TV(P,Q)=(1/2)E_P |L_n−1|
       →(1/2)E |exp(sigma Z−sigma²/2)−1|.

The last quantity is 2Phi(sigma/2)−1: split the integral where Z=sigma/2 and complete the square in the exponentially tilted normal density. This proves (3).

Bounded E_P L_n² gives Q-contiguity with respect to P by Cauchy–Schwarz. Conversely, for any event B and any epsilon>0,

    P(B)≤P(L_n≤epsilon)+Q(B)/epsilon.

The limiting likelihood in (2) is strictly positive almost surely. First send n to infinity, then epsilon to zero, proving P-contiguity with respect to Q. This proves mutual contiguity; no positivity of a finite-n likelihood on all null observations is assumed.

For a>0, the likelihood-ratio test at threshold one has asymptotic type-I and type-II errors both Phi(−sigma/2). Under Q the limiting likelihood is the size-biased version of (11); this follows from E_Q f(L_n)=E_P L_n f(L_n) and uniform integrability. Equal-prior average error is Phi(−sigma/2); the sum of errors is twice that number.

For fixed c,a and fixed approximation accuracy, a sufficiently large but fixed D makes (13) small. The statistic L_(n,≤D) is a finite graph polynomial computable by enumerating at most D vertices. Thus fixed-degree polynomial statistics approximate this high-c testing risk arbitrarily well. No uniform algorithmic statement as c approaches e is made, and this does not solve the source's low-c hairy-path running-time question.

## 7. Closed form and the obstruction at c=e

Let tau∈(0,1) be the smaller solution of tau e^(−tau)=1/c. The classical exponential generating function of rooted labelled trees, T(z)=z exp(T(z)), gives

    A(c)=c tau/(1−tau)−1.                         (14)

Indeed zT'(z)=T(z)/(1−T(z))=sum_(s≥1)s^s z^s/s!, and one subtracts the s=1 term at z=1/c. Formula (14) is equivalent to the convergent series, not an extra assumption.

At c=e the series A(c) diverges and no z>1 satisfies z<c/e. Therefore the uniform fixed-vertex tail bound (13) fails. In Turn 3's k≈n^(4/9) regime, each fixed tree coefficient tends to zero; the nontrivial second moment instead comes from growing tree supports of order sqrt(k). The fixed-diagram lemma has constants depending on those sizes and supplies no uniform bound for them.

Consequently the present lognormal law cannot be transported to c=e or c_n→e without a new growing-support argument. It neither proves nor disproves weak detection in the exact L² window, and leaves the c_h-to-e mean-degree gap unresolved. This limitation is a specific missing uniformity step, not a license to infer total variation from Turn 3's moments.
