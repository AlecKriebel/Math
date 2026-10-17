# Stage 1 alternative argument: collective seed compression and the exact LP barrier

Public mathematical edition. The source problem remains UNSOLVED by this five-stage study. Historical statements with residual swap bound 2m and Azuma denominator 8km² remain valid conservative estimates; the final synthesis uses the sharpened m and 2km² bounds. Stage labels record provenance, not additional assumptions. No claim of external peer review or priority is made.


Date: 14 October 2026. Mathematical study stage 1.

Status: rigorous restricted-algorithm exclusions, not a resolution. The requested event still permits an arbitrary function of the whole random set.

## 1. Exact model and useful new conclusion

Let p tend to infinity through primes, k=floor(sqrt(p)), and A be uniformly distributed among the k-element subsets of G=Z/pZ. For a fixed C>0 set m=floor(C sqrt(p)). The contract uses C=100. A translating set T is successful when A+T=G.

**Seed-compression theorem.** For each p, let F_p be an arbitrary deterministic map from subsets B of G of size at most s_p to subsets F_p(B) of G of size at most m. Suppose s_p=o(k). Then

Pr[there exists B subset A, |B|<=s_p, A+F_p(B)=G] -> 0.

The conclusion remains true for a predetermined family of L_p=exp(o(k)) such maps, with both the map and B selected after seeing all of A. The map may perform completely arbitrary collective computation on B and has no complexity, algebraic, symmetry, or efficiency restriction. The seed is an unordered subset: adaptive ordering, extra numerical values, or other information about A must be counted as advice rather than silently supplied to the decoder. Independent decoder randomness can be conditioned on, so a randomized decoder chosen independently of A satisfies the same success bound.

Thus a successful construction cannot, with high probability, be reconstructed from a vanishing fraction of the sampled points plus an exp(o(k))-size advice menu. This is a lower bound on sample compression, not a statement that all adaptive constructions are compressible.

This extends the predetermined-small-menu barrier in a distinct direction. For example, s=k/sqrt(log k) is o(k), while the possible seed domain has logarithmic cardinality

log binom(p,s) = (1+o(1)) k sqrt(log k),

which is much larger than k. The theorem does not union-bound over all possible outputs. It counts only seeds that actually occur inside the random A. For C>1 and large p, the seed domain injects into the family of allowed m-sets, so maps can indeed have that many distinct outputs.

It also differs from the bounded-elementwise-map exclusion: F_p may depend collectively on every relation among the seed points, but it receives only a small subset of A. A fully collective function of the entire A is not covered.

## 2. Finite conditional-completion bound

The following lemma is valid in every finite abelian group of order n, without primality.

Let 0<=s<k<=n and m>=1, let B subset G have size s, and let T be a fixed set of size t<=m. Condition a uniform k-set A on B subset A, writing A=B union R, where R is a uniform (k-s)-subset of G\\B. Put

W=G\\(B+T),
q(n,k,s,t)=binom(n-s-t,k-s)/binom(n-s,k-s).

If n-s-t<k-s, the numerator is zero by convention. For x in W, the set x-T is disjoint from B and has t points. Therefore

E[|G\\(A+T)| | B subset A] = |W| q(n,k,s,t).       (2.1)

There is no independence assumption among the different x.

If R and R' differ by one exchange, their two union sizes after adding B each differ from the common-core union size by a number in [0,t]. Consequently the uncovered-point count changes by at most t, and hence by at most m.

Expose a random ordering of R. At an exposure step, couple completions after two possible next values u,v by transposing u and v in the remaining universe. The completed unordered sets agree or differ by one exchange. The corresponding conditional expected uncovered counts differ by at most m, so every Doob increment has absolute value at most m. Azuma therefore gives, for any z>=0,

Pr[U<=E U-z | B subset A] <= exp[-z^2/(2(k-s)m^2)], (2.2)

where U=|G\\(A+T)|. We use the safe constant, with no optimization.

Assume m>=1, sm<n and m<=n-k. Since |W|>=n-st>=n-sm and q is decreasing in t, equations (2.1)-(2.2) imply

Pr[A+T=G | B subset A]
 <= exp[-D(n,k,m,s)],                              (2.3)

D(n,k,m,s)
 = ((n-sm) q(n,k,s,m))^2 / (2(k-s)m^2).             (2.4)

If T is empty, coverage is impossible and (2.3) remains a valid upper bound. When the displayed conditions fail, the bound is not asserted to be informative; replacing n-sm by its positive part gives a trivial version.

Importantly, T may be any predetermined function of the conditioned seed B. After B is fixed, it is a fixed set in the conditional probability calculation.

## 3. Counting seeds inside A, including fully adaptive selection

For each s, let F_{p,j} be predetermined maps on s-subsets, j=1,...,L. Define the number of successful seed/map witnesses by

Z_s(A)=sum_j sum_{B subset A, |B|=s} 1[A+F_{p,j}(B)=G].

For a uniformly chosen B of size s, every B has the same probability binom(p-s,k-s)/binom(p,k) of lying in A. Double counting gives exactly

E Z_s = binom(k,s) sum_j E_B Pr[A+F_{p,j}(B)=G | B subset A].

Applying (2.3) uniformly over B and j yields

Pr[Z_s>=1] <= L binom(k,s) exp[-D(p,k,m,s)].         (3.1)

This calculation permits B to be selected with complete knowledge of A. It does not condition on an adaptively selected B and then incorrectly assume the completion is uniform. Instead it averages over fixed B first and counts witnesses.

Allowing sizes 0<=s<=s_p, the exact bound is

Pr[there exists successful map/seed of size <=s_p]
 <= L sum_{s=0}^{s_p} binom(k,s) exp[-D(p,k,m,s)].    (3.2)

If s_p=o(k), uniformly over that range,

q(p,k,s,m)=product_{i=0}^{k-s-1}(1-m/(p-s-i))
          =exp[-C+o(1)],
p-sm=(1-o(1))p,
D(p,k,m,s)=(e^(-2C)/(2C^2)+o(1))k.                 (3.3)

The product estimate uses sum of its linear terms = C+o(1) and sum of its squared terms = O(p^(-1/2)); k/sqrt(p)->1 and m/sqrt(p)->C handle the floor convention.

Finally,

log(sum_{s=0}^{s_p} binom(k,s))=o(k).

For example, for 1<=s_p<=k/2 the sum is at most (s_p+1)(ek/s_p)^s_p, whose logarithm is o(k). Combining this with log L=o(k) proves the theorem, with an exponentially small error exp[-(e^(-2C)/(2C^2)+o(1))k]. At C=100 the constant is very small but strictly positive. The asymptotic theorem is not a useful numerical threshold claim.

### 3.1 Residual holes and repairs after seed decoding

The same proof gives more than failure of exact coverage. For every fixed epsilon in (0,e^(-C)), with probability tending to one every permitted decoder/seed output satisfies

|G\\(A+F_{p,j}(B))| >= (e^(-C)-epsilon)p.          (3.4)

Indeed, conditional mean U is uniformly at least (e^(-C)-o(1))p, so violation of (3.4) requires a downward deviation at least epsilon p/2 for sufficiently large p. Its conditional probability is at most

exp[-epsilon^2 p^2/(8(k-s)m^2)]
 = exp[-(epsilon^2/(8C^2)+o(1))k],

which again beats the exp(o(k)) seed/advice count.

Any additional translating set R, now allowed arbitrary dependence on the entire A, covers at most k|R| of these residual points. Therefore an actual repair needs

|R| >= (e^(-C)-epsilon)p/k.

In particular, adding o(k) completely unrestricted repair translations cannot turn one of the permitted decoded outputs into a cover. This is still a restricted initial-construction theorem. It does not exclude an unrestricted repair of a small fixed positive multiple of k, or a wholly collective initial construction.

## 4. A quantitative linear-seed tradeoff

The same proof permits a small fixed positive seed fraction. Suppose s/k->alpha with 0<=alpha<min(1,1/C), and log L/k->rho. Define binary entropy in natural logarithms by

h(alpha)=-alpha log alpha-(1-alpha)log(1-alpha),

gamma_C(alpha)
 = (1-C alpha)^2 exp[-2C(1-alpha)] / [2(1-alpha)C^2].

Then (3.1) gives

limsup (1/k) log Pr[Z_s>=1]
 <= rho+h(alpha)-gamma_C(alpha).                   (4.1)

Whenever rho+h(alpha)<gamma_C(alpha), success probability tends to zero exponentially. Since h(0)=0 and gamma_C(0)>0, some positive alpha is allowed for every fixed C. The admissible alpha from this unoptimized estimate is extraordinarily small when C=100.

This is a sufficient exclusion region. Equality or the opposite inequality does not predict success. In particular, no claim is made for alpha near 1/C or for a seed containing essentially all of A.

## 5. Ordinary fractional covering and packing cannot detect the target gap

For every nonempty fixed A of size k, consider the natural fractional set-cover program:

minimize sum_t z_t,
subject to z_t>=0 and sum_{a in A} z_{x-a}>=1 for every x.

Summing the p covering constraints gives k sum_t z_t>=p. Conversely z_t=1/k for every t is feasible and has objective p/k. Thus the fractional optimum is **exactly p/k for every A**, independently of its randomness or structure.

The dual assigns y_x>=0 with sum_{x in A+t} y_x<=1 for every t and maximizes sum_x y_x. Summing those p inequalities gives k sum_x y_x<=p, while y_x=1/k attains p/k. Therefore no choice of ordinary nonnegative dual weights can certify a lower bound larger than p/k. Any proof that tau(A)>100 sqrt(p) must use integral information beyond this standard linear-programming dual, such as valid higher-order inequalities or a cover-specific structural argument.

Likewise the fractional matching relaxation of the translate hypergraph has optimum p/k: assigning weight 1/k to every translate is feasible, and summing the vertex constraints is the matching upper bound. This says nothing about the integral matching number. It therefore does not repair the growing-uniformity nibble issue already identified by the other arguments.

These exact equalities do not imply an integral cover within a constant factor. The general greedy/rounding bound still loses a logarithmic factor, and such a factor is too large for the contract.

## 6. Screening of other routes and precise unresolved step

- Random Cayley domination is exactly the target when formulated as coverage by the union of open outgoing neighborhoods in the directed difference graph, retaining loops exactly when 0 belongs to A. Selected vertices are not automatically covered; using the usual closed-neighborhood convention would change A to A union {0}. The independent-edge random-graph model is not a valid substitute: all edges with one difference share a single membership bit of A.
- Rodgers--Sahay's current primary paper proves its VC-dimension estimate at **fixed** Bernoulli density. Remark 1.2 explicitly leaves the decreasing-density range unpursued; Remark 1.8 discusses fixed-regularity models separately. It cannot be substituted at density p^(-1/2) and exact size k without a new argument. Its covering Lemma 6 is the general logarithmic BJR bound, not a constant-multiplicity construction.
- Alon--Pham's primary random-Cayley theorem concerns independence under independently sampled symmetric differences, or the corresponding sum graph. Its structured sumset families are not families of T with A+T=G. The square-root-density arithmetic-progression theorem for A+A is not a domination theorem. No transfer was found.
- A small codegree-to-degree ratio alone does not provide an applicable growing-edge matching theorem, as the other audit's projective-plane example already shows. The LP equalities above isolate an additional limitation of trying to turn fractional matching/covering into the desired conclusion without a new integral theorem.

The seed theorem leaves a sharply stated route open: a successful cover, if one exists, may require information that cannot be reconstructed from o(k) actual points of A with subexponential advice. Neither a theorem forcing that form of compression nor an adaptive construction escaping it while eliminating every residual hole has been proved here.

## 8. Finite formula checks

The historical companion seed-formula checker verified 22,121 exact conditional-mean identities, 15,900 exact one-exchange comparisons, and seven exact adaptive-seed double-counting identities, including nonzero witness counts at p=11. It also performs 22,121 floating-point diagnostics of the exponential tail bound, with tolerance 1e-12; those diagnostics are not interval-certified. Explicit runtime guards remain active under Python -O and -OO, and all three interpreter modes passed; the historical receipt records those results. That larger historical run is not part of the lightweight public replay. These checks test formulas and implementation on small cases. The asymptotic theorem is established by the proof above, and the checks are not numerical evidence for a resolution of the main problem.

