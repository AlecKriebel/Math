# Independent derivation and adversarial mathematical checks

## Claim assessed

For rational square factors, with g=1-x²-y²-z², f the displayed Scheiderer quartic, p=1+f, and all degree-at-most-four moments specified by m000=1, m400=-1 and zero elsewhere, the claim is a fixed normalized separator p∈1+Q_R(g) but p∉1+Q_Q(g) at every finite factor degree. It is an affirmative existence instance of the printed OWR question, not a universal failure for every separator, every normalization, or PSD input. The quartic and local mechanism are credited classical ingredients.

## Quartic field and geometry

The polynomial h=t⁴-t+1 is positive for t≤0, t≥1, and 0<t<1 by the manuscript's disjoint interval argument. In characteristic two it has neither a root nor a quadratic irreducible divisor: reducing modulo t²+t+1 gives remainder 1. Thus h modulo two is irreducible and squarefree (its derivative is 1). In characteristic three h=(t+1)(t³-t²+t+1), and the cubic has values 1,2,1 at 0,1,2; it also does not vanish at -1. These factors are distinct and squarefree. The unramified factorization-cycle theorem consequently supplies a four-cycle and a three-cycle in Gal(h/Q)⊆S4. Its order divides 24 and is divisible by 12. The only index-two subgroup of S4 is A4: in any surjection S4→C2, conjugate transpositions have the same nontrivial image and generate S4. A4 has no four-cycle. Therefore the order is 24.

As an independent finite consistency check, all 6 four-cycles and 8 three-cycles were paired, their generated subgroups closed explicitly, and each of the 48 subgroups had 24 elements. Single-cycle controls generate proper groups, so dropping either ingredient genuinely loses the conclusion. This enumeration supplements the group proof rather than replacing the factorization theorem.

The multiplication matrix of x+ty+t²z in the basis (1,t,t²,t³), with t⁴=t-1, is

```text
[ x   0  -z  -y  ]
[ y   x   z  y-z ]
[ z   y   x   z  ]
[ 0   z   y   x  ].
```

Its determinant independently expands to the exact nine-term f. Separability gives its product over the four conjugate linear forms ℓ_i=x+α_i y+α_i²z. Each triple's determinant is a nonzero Vandermonde product. Complex conjugation partitions the roots into two pairs, and choosing one linear factor from each pair writes f as the squared modulus of a complex quadratic, hence two real quadratic squares.

Each conjugate-pair intersection is a conjugation-stable one-dimensional complex vector space and hence has a real nonzero representative. If f were a sum of rational quadratic squares, evaluating at such a real representative would make every factor zero. The algebraic projective intersection is defined over the splitting field, and homogeneous vanishing is independent of the representative. Rational coefficients allow every Galois automorphism to transport this zero. The S4 action is transitive on unordered root pairs, giving all six intersections. Triple independence makes these six intersections distinct and puts three distinct ones on each line. A quadratic restricted to a projective line has at most two distinct zeros unless it is identically zero. Thus every one of the four distinct linear factors divides each rational quadratic, forcing it to vanish identically. No numerical root approximation is needed.

For arbitrary polynomial SOS without weights, the largest-degree homogeneous terms are a sum of real squares and cannot cancel identically. Every factor therefore has degree at most two. The constant coefficient of f=0 forces the constant factors to vanish; the degree-two identity forces all linear factors to vanish. This reduces exactly to the excluded homogeneous quadratics. It is important that this maximum-degree argument is applied only to unweighted sums.

## Explicit real identity and arbitrary-degree module obstruction

For β³-4β-1=0, the signs at -2 and -1 are -1 and 2, so a root β∈(-2,-1) exists and is nonzero. The displayed U,V satisfy 4β²f=(βU)²-β(βV)² after exact reduction using β³=4β+1. An independently organized reduction of all expanded coefficients verified this identity; changing one coefficient leaves a nonzero remainder. Therefore f=(U/2)²+(sqrt(-β)V/2)² over R.

Suppose f=Σa_i²+gΣb_j² with rational polynomial factors of arbitrary finite degrees. At 0, g=1 and f=0, so all constant factors vanish. The degree-two component is the sum of squares of all linear jets, which also must vanish. With every factor of order at least two, the degree-four component is precisely Σ(a_i^[2])²+Σ(b_j^[2])²: multiplying b_j² by g-1 first affects degree six, and higher jets cannot affect degree four. This is the rational quadratic SOS excluded above. The argument does not transfer the difficulty to an unproved degree bound.

The negative control

```text
(x³)²+(x²y)²+(x²z)²+g(x²)²=x⁴
```

shows explicitly that higher weighted degrees can cancel. It was verified exactly. Any review route trying to impose degree two on all weighted factors would be invalid; the manuscript explicitly avoids that route. A second valid explanation is the rational binomial square root sqrt(g)∈Q[[x,y,z]] and the same leading-form obstruction in that formal ring. Scheiderer 2000 supplies the classical leading-form and completion mechanism, and Benoist 2022 records its rational homogeneous-quartic consequence.

## Moment data, normalization and limits

There are binomial(7,3)=35 indices. A nonnegative measure cannot have fourth moment -1. Since p's constant and x⁴ coefficients are both 1, L_m(p)=1-1=0. Also p≥1 globally, with p(0)=1, and the real SOS for f gives normalized real membership. The ball is compact/nonempty and the sole rational generator itself is the Archimedean ball witness.

The same vector has q=1+x⁴ with L_m(q)=0 and q-1=(x²)² over Q. Its M2 diagonal indexed by x² is -1, so PSD fails. Merely asking the real-SOS multipliers to have rational polynomial coefficients already succeeds using σ0=f, σ1=0; this weaker interpretation cannot be called obstructed.

Powers' actual Theorem 7 allows an additional rational SOS multiple of N-Σx_i². Here N=1 and that polynomial is exactly the existing generator, so both its multipliers combine in Q_Q(g). Since p≥1, the theorem gives p∈Q_Q(g). For rational c>1, cp-1≥c-1>0 on K and gives cp∈1+Q_Q(g); L_m(cp)=0 follows from linearity. For every real c<1, cp(0)-1=c-1<0, excluding even real normalized membership. At c=1 the proved obstruction holds. No certificate degree is predicted by this use of Powers.

For h∈Q_Q(g)∩-Q_Q(g), evaluating both representations on K makes h=0 throughout the ball. Its nonempty Euclidean interior forces h to be the zero polynomial. Hence the support is zero and the quotient is Q[x,y,z], of Krull dimension three. The currently inspected zero-dimensional-support descent regime does not apply; the example is already rationally Archimedean. The unavailable corrected journal body's Appendix B.1 statement remains unknown, rather than being inferred from a lead-in or from the older arXiv version.

## Source interpretation and proof boundary

The whole actual OWR contribution's pp. 802–804 define nonnegative representing measures, discuss strict positivity of p rather than p-1, and ask whether irrational fixed membership certificates can occur. The example's p≥1 is strictly positive. No PSD-input hypothesis or min p>1 condition is printed in that question. The companion arXiv v1 Corollary 2 explicitly rescales to min p>1 and is a sufficient algorithmic regime; the current note carefully stays outside it. The rational-square convention is stated as our precise interpretation, because the printed contribution does not formalize that distinction.

The finite checker cannot certify all degrees by search, any global priority absence, or formal correctness of outside source computations. The manuscript does not make those claims. Established ingredients and prior irrational Gram and strongly infeasible SDP applications receive specific citations. The bounded novelty comparison may be reopened on a verified exact predecessor; no worldwide-firstness or present-openness claim is accepted here.
