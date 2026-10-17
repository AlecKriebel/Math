# Stage 4: unrestricted amplification of near-covers

Public mathematical edition. The source problem remains UNSOLVED by this five-stage study. Historical statements with residual swap bound 2m and Azuma denominator 8km² remain valid conservative estimates; the final synthesis uses the sharpened m and 2km² bounds. Stage labels record provenance, not additional assumptions. No claim of external peer review or priority is made.


Date: 14 October 2026. Mathematical study stage 4. Exact model and cap remain k=floor(sqrt(p)), A uniform among k-subsets of F_p, and c=floor(100 sqrt(p)).

## Decision

A genuine collective construction was proved conditionally on a near-cover: shifted copies of the same near-cover can be combined, without any independent-A assumption, to reduce its holes multiplicatively. This gives new sufficient expectation bounds at smaller centre budgets that would settle the affirmative target. Those expectation bounds have not been proved. No positive lower bound of the required order for the full-budget optimal residual was obtained either.

The resulting unrestricted bridges are:

- `E R_(49k)=o(p^(3/4))` would imply the required covering probability tends to one.
- `E R_(33k)=o(p^(5/6))` would also suffice. The stronger hypothesis `E R_(33k)=O(p^(3/4))` gives a quantitative failure bound, polynomial by Markov and exponentially small using the existing concentration theorem.
- In the opposite direction, `E R_c>=a c sqrt(k)` for a fixed a>0 along arbitrarily large primes would supply the required negative answer.

These statements concern different budgets. None follows merely from a corresponding estimate at another budget.

## 1. Deterministic multiplicative residual inequality

For any fixed nonempty A subset F_p, let

`R_m(A)=min_{|T|<=m}|F_p\(A+T)|`.

For nonnegative integer budgets m,n,

`R_(m+n)(A) <= floor(R_m(A) R_n(A)/p)`.

Proof. Choose centre sets T and S achieving the two minima, and write U and V for their hole sets. For every shift d,

`F_p\[A+(T union (S+d))] = U intersection (V+d)`.

The exact translation average is

`sum_d |U intersection (V+d)| = |U||V|`.

Some d therefore gives an intersection at most `|U||V|/p`. The cardinality is an integer, so it is at most the floor. The combined centre set has at most m+n elements. All choices, including d, may depend on every element of A.

This is not a product-model substitution: the same A occurs in both near-covers. Only the hole sets are relatively translated.

### Iteration and explicit repair

For every positive integer r,

`R_(rm)(A) <= floor(R_m(A)^r/p^(r-1))`.

One may prove this by induction from the two-budget inequality. Equivalently, start with any m-centre near-cover having u holes and repeatedly add a shifted copy of its centre set, each time choosing a shift whose new hole intersection is at most its translation average. After r copies, at most `floor(u^r/p^(r-1))` holes remain.

Fix a_0 in A. Each remaining hole x can be covered by adding centre x-a_0. Hence

`tau(A) <= rm + floor(R_m(A)^r/p^(r-1))`.

The repair is deterministic and covers every point. Repeated centres, if any, only reduce the cost. This construction is valid for an arbitrary near-cover, not merely for an independently sampled or small-description centre set.

## 2. Exact probability bridge

Let A have any probability law on nonempty subsets, and put `mu_m=E R_m(A)`. Fix integer c,r,m with r>=1 and rm<=c. Set b=c-rm. If tau(A)>c, the deterministic bound forces

`R_m(A)^r/p^(r-1) >= b+1`.

Consequently

`Pr(tau(A)>c) <= min(1, mu_m / [(b+1)p^(r-1)]^(1/r))`.

This is a direct application of Markov's inequality after the deterministic construction. No interchange of optimization and expectation is used.

### Two-copy bridge at 49k

Choose m=49k and r=2. Since `100k<=c`, the repair slack satisfies b>=2k. Thus

`Pr(tau(A)>c) <= mu_(49k) / sqrt((2k+1)p)`.

In particular, `mu_(49k)=o(p^(3/4))` proves the affirmative target. In concrete terms, two adaptively aligned near-covers use at most 98k centres; the assumed mean bound makes their remaining holes o(k) in probability, fitting the available repair margin.

### Three-copy bridge at 33k

Choose m=33k and r=3. Now b>=k, and

`Pr(tau(A)>c) <= mu_(33k) / [(k+1)p^2]^(1/3)`.

Thus `mu_(33k)=o(p^(5/6))` is sufficient. If `mu_(33k)=O(p^(3/4))`, this failure bound is `O(p^(-1/12))`.

The same implication can be phrased as `R_(33k)=o_p(p^(5/6))` under the stronger O(p^(3/4)) mean premise. Three shifted copies then leave o_p(k) holes, and 99k centres plus repair fit within 100k, hence within the operational cap.

### Concentration strengthens the conditional three-copy rate

The previously proved exact uniform-k exposure bound is

`Pr(R_m >= mu_m+u) <= exp(-u^2/(8km^2))`.

For m=33k, the repair threshold `B=[(b+1)p^2]^(1/3)` has order p^(5/6). Under `mu_m=O(p^(3/4))`, eventually B-mu_m>=B/2. Therefore

`Pr(tau(A)>c) <= exp(-B^2/(32km^2)) = exp(-Omega(p^(1/6)))`.

This is a conditional consequence of the stated mean assumption, not a proved probability estimate for the original random A.

### General fixed-r statement

For a fixed positive integer r and a fixed positive budget margin eta, suppose `rm<=(100-eta)k`. Then a sufficient condition is

`mu_m=o(p^(1-1/(2r)))`.

The exact Markov formula above gives the rounding control. A fixed margin is retained deliberately; an unspecified error at the coefficient-100 endpoint is not sufficient.

## 3. The negative mean bridge remains at the full budget

Let `mu_c=E R_c(A)`. The audited optimum-residual concentration theorem gives

`Pr(tau(A)<=c) = Pr(R_c=0) <= exp(-mu_c^2/(8kc^2))`.

If `mu_c>=a c sqrt(k)` for fixed a>0 along arbitrarily large primes, then the probability of a cover is at most `exp(-a^2/8)<1` on that sequence. This is exactly a valid negative answer to the original convergence-to-one assertion. If `mu_c/(c sqrt(k))->infinity`, the same argument gives noncoverage with high probability.

The new positive bridge and this negative bridge meet the p^(3/4) scale at different budgets: roughly 49k versus 100k. A bound on mu_c alone cannot be moved to mu_(49k), whose optimum has fewer centres. No such comparison has been established.

## 4. What interpolation actually justifies

To make the size parameters explicit, write

`mu(a,m)=E[R_m(A_a)]`,

where A_a is a uniform a-subset of F_p.

### Valid cardinality comparisons

For 0<=a<=a+s<=p, couple uniform subsets by an ordering. Removing s points from a larger set can remove at most sm sumset points from any fixed m-centre cover. Comparing with a minimizing centre set gives

`0 <= mu(a,m)-mu(a+s,m) <= sm`.

Likewise, deleting s centres from an optimal (m+s)-centre set loses at most sa points, so

`0 <= mu(a,m)-mu(a,m+s) <= sa`.

These comparisons allow arbitrary optimizer changes. They are too coarse to transfer a p^(3/4)-scale estimate over a change of Theta(k) in the centre budget: their error is of order p.

Taking expectations in the multiplicative residual inequality gives only

`mu(k,m+n) <= E[R_m(A)R_n(A)]/p`.

Replacing the expectation of the product by the product of means is not justified by that proof. Both residuals are functions of the same A; no independence has been created by the shift averaging.

### Pointwise diminishing returns in A is false

For p=7, m=2 and A={0,1}, the optimum covered size is four. Adjoining x=3 or y=5 separately raises it to five; adjoining both raises it to seven. Indeed each of the two three-point sets has all nonzero differences, so two distinct translates intersect and can cover at most five points, while their translates by 0 and 1 achieve five. For {0,1,3,5}, the same two shifts cover all seven points.

Thus the optimized coverage function F satisfies

`F(A union {x})+F(A union {y})=10 < 11=F(A)+F(A union {x,y})`.

It is not submodular. This refutes an attempt to justify expectation interpolation by pointwise diminishing returns; it does not by itself refute a separately proved average-law inequality.

## 5. Strongest estimates actually obtained at the target budget

For every fixed A of size k and uniform c-subset T, averaging gives

`E_T holes(A,T)=p binom(p-k,c)/binom(p,c)`.

Therefore, deterministically for every A,

`0 <= R_c(A) <= floor[p binom(p-k,c)/binom(p,c)]`

for all sufficiently large p with c+k<=p. In this regime the upper bound is `(exp(-100)+o(1))p`.

The lower bound established for the unrestricted target remains only zero. The trivial positive lower bound `p-km` applies when km<p but gives nothing at c. The new amplification theorem does not improve the displayed target mean estimate without an improved near-cover at a smaller budget: amplifying merely the usual constant-density-hole bound a fixed number of times still leaves a positive-density bound asymptotically.

Likewise, the Stage 3 O(p) variance under random centre sampling does not become a variance estimate for the optimum under random A, and it does not lower-bound the optimum's mean. Those probability spaces and optimizations remain distinct.

## Disposition

The collective amplification construction and exact probability bridges are valid unrestricted results, with complete coverage and explicit cap control. They expose useful sufficient positive estimates, rather than excluding another subclass of algorithms. Neither the necessary smaller-budget upper mean nor the full-budget p^(3/4)-scale lower mean has been proved. The original question remains unresolved by this pass.

