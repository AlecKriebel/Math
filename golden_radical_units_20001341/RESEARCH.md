# Scoped audit: short units in the golden-radical field

Queue 1865, database ID 20001341. Authored 2026-10-21. This is elementary partial progress and a completion-boundary audit, not a resolution of the unspecified original optimization problem or a novelty claim. Source scope is inherited from `SOURCE_STATUS_GATE.md`: Bernstein's AIM question fixes x^312−x^156−1 but does not define “short,” exclude torsion, or request a basis. All five approaches below are conditional on explicitly stated objectives.

## Approach 1: establish the field and a certified non-torsion unit

For n≥1 set phi=(1+sqrt(5))/2, a=log(phi), alpha=phi^(1/n)>1, K=Q(sqrt(5)), L=Q(alpha), f_n=X^(2n)−X^n−1.

First, O_K^×={±phi^j:j∈Z}. Here is an elementary verification of the needed fundamental-unit fact. O_K=Z[(1+sqrt(5))/2]. For any unit, multiply by a sign and power of phi to obtain a positive real value t in [1,phi). If its norm is +1, its integral trace t+1/t lies in [2,sqrt(5)), so equals 2 and t=1. If its norm is −1, its integral trace t−1/t lies in [0,1), so equals 0 and t=1; this is incompatible with norm −1 for the rational element 1. Thus only t=1 occurs.

Consequently phi is not a p-th power in K for any prime p. If b^p=phi, b is integral (root of a monic equation over O_K), and b^−1 is integral by the same argument with phi^−1. Writing b=±phi^j would imply pj=1. The exceptional obstruction phi=−4b^4 is impossible at the positive real embedding: its right side is nonpositive. One may instead take norms: N(phi)=−1 while N(−4b^4)=16N(b)^4≥0. This handles the 4-divisibility exception, not merely prime-power obstructions.

The binomial irreducibility criterion in characteristic zero says X^m−c is irreducible over F provided c is not a p-th power in F for every prime p|m, and, if 4|m, c is not −4 times a fourth power. A precise published statement is Lemma 4 in Artūras Dubickas, *Irreducibility of a Polynomial Shifted by a Power of Another Polynomial* (2020), https://doi.org/10.1155/2020/8869499, inspected 2026-10-21. Apply it over K with c=phi. Since K⊂L (phi=alpha^n), [L:K]=n and [L:Q]=2n, proving f_n irreducible; n=1 is immediate.

The identity alpha(alpha^(2n−1)−alpha^(n−1))=1 proves alpha is a unit in Z[alpha], hence in O_L. Its field norm N_L/Q(alpha) is −1. It is non-torsion because alpha>1. No identification Z[alpha]=O_L is needed or asserted.

The roots are the n roots of phi and the n roots of −phi^−1. There are n roots of modulus exp(a/n), n of modulus exp(−a/n). For odd n each block contributes one real root; for even n the positive block contributes two and the negative block none. Therefore signature is (2,n−1), unit rank n. The chosen field embeds in R, so any root of unity in it must map to ±1 and is itself ±1. At n=156: degree 312, signature (2,155), rank 156, torsion {±1}.

Outcome: exact field/unit certificate and immediately available non-torsion element. Limitation: one unit is not a shortest-unit or full-unit-group certificate.

## Approach 2: metric audit, torsion optimum, and near-AM–GM construction

Use the canonical Minkowski Euclidean norm with sqrt(2) scaling on real and imaginary coordinates of each complex place. Equivalently square the absolute values over all 2n embeddings. For alpha,

  ||alpha||_M² = n exp(2a/n)+n exp(−2a/n) = 2n cosh(2a/n).

For every unit u, the product of the 2n squared absolute embedding values is 1. AM–GM gives ||u||_M²≥2n. Equality makes all absolute values 1. In particular the fixed real embedding has u=±1, so exactly the torsion units attain equality. Thus if torsion is allowed, the canonical Minkowski shortest-unit problem is trivial: ±1 have length sqrt(2n). In logarithmic metrics they map to the zero vector; in house and height they have values 1 and 0.

If torsion is excluded and lambda is the shortest Minkowski length of a non-torsion unit, then

  sqrt(2n)<lambda≤||alpha||_M,
  1≤||alpha||_M/lambda<sqrt(cosh(2a/n)).

The weak inequality ≤ on the right is also a valid simpler certificate. The minimum exists because O_L is a discrete Minkowski lattice and alpha supplies a finite search radius. This is a certified approximation factor, not exact optimality. Its near-1 quality is partly the unavoidable sqrt(2n) baseline. The squared excess is 2n(cosh(2a/n)−1)=4a²/n+O(n^−3), and the length ratio to the torsion baseline is 1+a²/n²+O(n^−4).

Other exact alpha metrics are:

- House max_sigma|sigma(alpha)| = exp(a/n).
- Absolute logarithmic Weil height h(alpha) = a/(2n).
- Intrinsic Mahler measure M(alpha) = exp((2n)h(alpha)) = phi.
- Full-embedding log norm, equivalently sqrt(2)-weighted complex-place logs: ||ell_sqrt2(alpha)||² = 2a²/n.
- Product-formula coordinate convention, one coordinate per place and weight 2 at complex places: ||ell_2(alpha)||² = (4n−2)a²/n².

The last formula counts two real places of log magnitude a/n and n−1 complex places with coordinate magnitude 2a/n. It is valid for both parities. These conventions are different Euclidean geometries. The product-formula coordinates lie in the ordinary sum-zero hyperplane; the sqrt(2) convention lies in a weighted hyperplane. A Minkowski approximation ratio cannot be transferred to either log norm, height, or house excess above 1.

Coefficient length in the displayed power basis is 1 for alpha, but is basis-dependent and does not imply a statement about a maximal-order integral basis. No maximal order has been computed.

Outcome: exact metric values and a non-torsion canonical-Minkowski approximation guarantee. Limitation: the original source chooses none of these objectives.

## Approach 3: exact minima in the power subgroup, with Mahler degree correction

For u=±alpha^k, k∈Z, the Minkowski squared norm is 2n cosh(2ka/n), the house is exp(|k|a/n), height is |k|a/(2n), and either log norm is |k| times its alpha value. Hence k=±1 gives the minimum non-torsion value for each of those objectives within this subgroup. These do not establish minima over all O_L^×.

Intrinsic Mahler measure requires care: for k≠0 let g=gcd(n,|k|), d=n/g, m=|k|/g. Then [Q(alpha^k):Q]=2d and

  M(alpha^k)=phi^(|k|/g).

To see the degree, beta=phi^(m/d) has beta^d=phi^m. The positive number phi^m is irrational because its quadratic conjugate has absolute value phi^−m, so Q(phi^m)=K⊂Q(beta). Bezout coefficients A m+B d=1 give beta^A phi^B=phi^(1/d); thus Q(beta)=Q(phi^(1/d)), of degree 2d by Approach 1. Negative k and a sign leave degree and height unchanged. Therefore the minimum intrinsic Mahler measure in the non-torsion power subgroup is phi, attained whenever |k| divides n, not only at |k|=1. The fixed-field product over all 2n embeddings, exp(2n h(alpha^k))=phi^|k|, is a different quantity when the degree drops.

Outcome: exact restricted minima and correction of a common Mahler-measure overclaim. Limitation: this is a rank-one subgroup in a rank-n unit group.

## Approach 4: relative-norm reduction and exact nonkernel optimality

This strengthens the mere power-subgroup analysis without certifying the whole unit lattice. For u∈O_L^× write

  N_L/K(u)=epsilon phi^r, epsilon∈{±1}, r∈Z.

The exponent r=r(u) is a homomorphism. Since X^n−phi is the relative minimal polynomial,

  N_L/K(alpha)=(-1)^(n+1)phi, so r(alpha)=1.

Thus r is surjective. On units modulo torsion, its kernel has rank n−1. Every u has u=alpha^r v with r(v)=0. The class of alpha generates a primitive/saturated rank-one subgroup: if q[u]=p[alpha] in the torsion quotient, applying r gives q r(u)=p; writing p=qk then q([u]−k[alpha])=0 implies [u]=k[alpha], because the torsion quotient is free abelian. Equivalently alpha can extend to some fundamental system; this does not construct the other n−1 generators or prove any proposed list is saturated.

Partition the 2n embeddings of L into two blocks B_+, B_- lying over the two real embeddings of K. Each block has n members and

  sum_(B_+) log|sigma(u)| = ra,
  sum_(B_-) log|sigma(u)| = −ra.

Blockwise AM–GM and Cauchy–Schwarz yield:

  ||u||_M² ≥ 2n cosh(2ra/n),
  ||ell_sqrt2(u)||² ≥ 2r²a²/n,
  house(u) ≥ exp(|r|a/n),
  h(u) ≥ |r|a/(2n).

For the height bound, the sum of the positive parts of the logs is at least the positive one of the two block sums. For the house bound, the block with positive sum has a log coordinate at least |r|a/n. All four bounds are attained by alpha^r. Consequently alpha is an exact non-torsion minimizer among ALL units with r≠0, in each of these four metrics. Any strictly better non-torsion unit must lie in the relative-norm ±1 kernel r=0, which has rank 155 for the fixed field. An intrinsic-Mahler corollary requires the additional field-degree argument below. There is no claimed exact optimizer for the weight-2 log norm from this argument. The latter is not the same quadratic form used by blockwise unweighted Cauchy–Schwarz.

For intrinsic Mahler measure, let F=Q(u). If K is not contained in F, then F∩K=Q. Since K/Q is quadratic Galois, F and K are linearly disjoint, so N_(FK)/K(u)=N_F/Q(u)=±1. Taking the further norm from L gives r=0. Therefore r≠0 forces K⊂F. Put e=[L:F]; writing N_F/K(u)=±phi^s gives r=es. Hence e divides r, and [F:Q]=2n/e. The height inequality now gives log M(u)=[F:Q]h(u)≥|r|a/e≥a. Thus alpha also attains the minimum intrinsic Mahler measure phi outside the kernel, but the minimizer is not unique, as the power examples show. This argument does not give a Mahler lower bound inside the kernel.

A concrete non-torsion kernel unit for n>1 is v=alpha(1−alpha). Indeed N_L/K(1−alpha)=1−phi=−phi^−1, so r(v)=0. Its distinguished real value lies strictly between −1 and 0, since 1<alpha<phi and phi(phi−1)=1; hence it is not ±1. Existence of this witness does not establish that it is shorter than alpha or that it generates the kernel.

There is also an orthogonal decomposition for ell_sqrt2: ell_sqrt2(v) is orthogonal to ell_sqrt2(alpha), since the block sums of v vanish. Therefore

  ||ell_sqrt2(u)||² = r² ||ell_sqrt2(alpha)||² + ||ell_sqrt2(v)||².

For n>1, the shortest nonzero logarithmic length is exactly the minimum of ||ell_sqrt2(alpha)|| and the shortest nonzero kernel length. This is a reduction, not a computed kernel minimum. For n=1 the kernel modulo torsion is zero and alpha is a fundamental unit, giving the familiar quadratic case.

Outcome: saturated rank-one factor, exact nonkernel optimality, and a precise residual subproblem. Limitation: kernel lattice not enumerated or certified.

## Approach 5: extra explicit units, rank obstruction, and algorithmic boundary

For m|n set t=alpha^m and q=n/m. Then t^q=phi. Let S=1+t+...+t^(q−1). Since (t−1)S=phi−1=phi^−1, t−1 is a unit with inverse phi S. Thus 1−alpha^m is also a unit. For 1+t, if q is odd, (1+t)(1−t+...+t^(q−1))=1+t^q=1+phi=phi², giving the inverse phi^−2 times that alternating sum. If q is even, (1+t)(t^(q−1)−t^(q−2)+...+t−1)=t^q−1=phi^−1, giving inverse phi times that alternating sum. These are exact identities in the power order; negative signs do not affect unit status.

However n=156=2²·3·13 has only 12 positive divisors. Even the 24 elements 1±alpha^m together with alpha form at most 25 independent units, far short of the required rank 156. At m=n, 1+phi=phi² and 1−phi=−phi^−1 are already dependent on alpha, so the actual bound is smaller. These identities alone cannot produce a fundamental system. A genuine full computation needs additional independent generators, a certified rank calculation, and saturation/index control in the maximal order. A regulator is a full-rank logarithmic covolume (with a stated normalization), not a single log-vector length. No regulator number is claimed here.

In a prescribed power-order representation, the alpha unit can be described by X modulo f_n and its inverse by X^(2n−1)−X^(n−1). Dense output uses O(n) entries; sparse output uses constant many terms with O(log n)-bit exponent labels. This output observation is not a uniform complexity bound for exact shortest units in arbitrary prescribed fields, not a complete maximal-order computation, and not a quantum gate-count analysis. Taking n-th roots changes the field and is applicable here only because the actual AIM field has exactly this radical form.

Outcome: additional exact unit certificates and an explicit failure of the small divisor list as a full basis. Limitation: no full unit group, regulator, or all-kernel shortest-vector certificate.

## Priority and current-status audit

These arguments apply classical binomial irreducibility, quadratic-unit structure, archimedean inequalities, the relative norm, and Dirichlet unit rank. They are presented as authored verification, not as new theorems. No novelty claim for the relative-norm formulation was investigated or made. The earlier source audit documents general quantum unit-group algorithms; their output specification must not be silently replaced by this field's exact shortest-unit certificate.

Dimitrov's *The Schinzel–Zassenhaus conjecture*, https://annals.math.princeton.edu/articles/22975, was rechecked 2026-10-21: the publisher lists acceptance on 2026-08-27 and forthcoming publication. That is a degree-dependent house-type result, not Lehmer's proposed uniform positive lower bound on logarithmic Mahler measure. Here h(alpha)→0 as n→∞ but (2n)h(alpha)=log(phi) and M(alpha)=phi are constant. Neither a resolution nor a counterexample to Lehmer follows.

The original AIM prompt remains metric-ambiguous. The valid conclusion is explicit non-torsion partial progress, a very strong conditional canonical-Minkowski approximation, and an exact relative-norm reduction for several chosen metrics. This document does not assert the unspecified source problem is solved, or prove it currently open.

## Failed routes / prohibited inference ledger

1. “±1 solves it”: valid only for a torsion-inclusive metric interpretation, not evidence about the workshop's intended challenge.
2. “alpha has small house, so its log vector is shortest”: invalid without a lower bound on the rank-(n−1) relative-unit kernel.
3. “all powers are controlled, so all units are controlled”: false, rank one versus rank n.
4. “Mahler measure of alpha^k is phi^|k|”: false intrinsically when degree drops; valid only for the fixed-field product.
5. “near-AM–GM ratio transfers to log norm or height”: false; it exploits a nonzero Minkowski baseline.
6. “divisor units give a basis”: impossible by generator count at n=156, before even testing independence.
7. “one vector determines regulator”: false; a full lattice covolume needs all independent directions and index control.
8. “monic constant ±1 identifies the maximal order”: false; it proves a unit, not a maximal power order.
9. “binomial prime obstructions alone suffice”: incomplete if 4|n; the exceptional obstruction was explicitly ruled out above.
10. “small height refutes Lehmer / Schinzel–Zassenhaus acceptance settles Lehmer”: false; degree factors and objectives differ.

Independent mathematical review passed the scoped proofs and independently reran the exact checks; see `INDEPENDENT_METRIC_AUDIT.md`. This does not enlarge the stated completion boundaries.
