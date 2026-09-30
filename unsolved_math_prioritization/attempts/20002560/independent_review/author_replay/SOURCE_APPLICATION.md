# RBM(3,1): independent reconstruction of a credited exact-radius certificate

**20002560 / AIM-PROBABILITY-0002. Complete source-application candidate for forward KL, awaiting a separate campaign review.** The numerical constant and the upstream full proof/certificate are credited. This is not a new-discovery claim or human peer review.

## 1. Source, conventions and provenance

The pinned AIM record asks for the maximum divergence of RBM(3,1). The duplicated sentence is an extraction artifact. Its attached note allows unspecified divergences, which does not define a single number: changing D to 2D doubles the answer. The intended primary approximation-theory convention used here is **forward Kullback–Leibler divergence**, with natural logarithms and three binary visible variables and one binary hidden variable. No claim for arbitrary divergences, reverse KL or a different logarithm base is made.

The original [AIM page](http://aimpl.org/boltzmann/1/) was recovered through its HTTP address after the HTTPS endpoint failed; item1.2 confirms both the question and the underspecified divergence remark. [Montufar's 2018 primary review](https://arxiv.org/abs/1806.07066), Section9 item10, independently records the exact three-visible/one-hidden divergence question and the conjectured constant, crediting discussions with Johannes Rauh. The neighboring RBM(3,2) result is a different model.

A prior full-scope computer-assisted candidate was released on **5 September2026**, before this campaign attempt, as *The Exact KL Radius of Two Bernoulli Products on Three Bits*, Anonymous, version0.1.0-candidate, [Evidence Press](https://evidencepress.org/releases/rbm31-exact-kl-radius/), DOI[10.5281/zenodo.22339153](https://doi.org/10.5281/zenodo.22339153), with [repository and certificate data](https://github.com/ipitchford/rbm31-exact-kl-radius). Its own status is anonymous, AI-assisted and unrefereed. Producer replay and internal editorial reports are not independent-person review. The scholarly creator is not inferred from the repository owner's account name.

The present package independently reconstructs the written analytic argument and all six explicit certificate trees with locally authored code. No upstream software was executed. The upstream prose was read; its checker was read only to resolve certificate serialization, especially the most-significant-bit-first order of the stored mixture coordinates. Its query interface uses a separate least-significant-bit convention. The first local replay caught that distinction as a support mismatch; the corrected local checker uses the certificate convention explicitly. The final source commit, data hashes and local checker hashes are recorded separately.

The strong prior-Alec gate found no earlier attempt: main contained only catalog/assessment/queue records, all-state PR searches by ID and RBM were empty, and no attempt-path history or campaign artifact existed. The polished queue title came from an imported partial report, not an Alec attempt. That earlier partial proves only a parity projection and a bracket; the September5 full candidate adds the global step.

## 2. Model and exact claimed conclusion

Let M be the compact set of mixtures of at most two Bernoulli products on {0,1}³:

$$q(x)=\lambda\prod_{i=1}^3u_i^{x_i}(1-u_i)^{1-x_i}+(1-\lambda)\prod_{i=1}^3v_i^{x_i}(1-v_i)^{1-x_i},$$

with all seven parameters in [0,1]. Factoring the RBM expression exp(b·x)(1+exp(c+w·x))/Z identifies its strictly positive-parameter distributions with the interior-parameter two-product mixtures, and M is their closure. Compactness and lower semicontinuity give a minimizer of D(p||q); the uniform product gives a finite competitor, so every minimizer is positive on supp(p). Approximating its mixture parameters from the interior preserves the finite divergence on supp(p). Thus the closed-model minimum equals the finite-RBM infimum.

The credited candidate theorem, independently reconstructed below, is

$$\max_{p\in\Delta_7}\min_{q\in M}D(p\Vert q)=c=-\frac34\log(2\sqrt3-3).\tag{1}$$

The only maximizing p are the two uniform parity laws. This is an exact value; a decimal approximation is not used in any proof decision. In bits divide by log2.

## 3. Independently checked lower bound

Put s=sqrt3, a=(2-s)/4, b=(2s-3)/4 and

$$q_*=(1/4,a,a,b,a,b,b,3a),\qquad p_E=(1/4,0,0,1/4,0,1/4,1/4,0).$$

All entries of q_* are positive. Direct algebra gives

$$q_*=\frac{3-s}{6}\delta_{000}+\frac{3+s}{6}\operatorname{Ber}((3-s)/2)^{\otimes3}.$$

Consequently q_* belongs to M and D(p_E||q_*)=-(3/4)log(4b)=c.

For each incomparable pair x,y of cube vertices, let L_xy=e_(x meet y)+e_(x join y)-e_x-e_y. There are nine such rows. Every positive interior-parameter two-product mixture can be coordinate-complemented so its component parameters are ordered in every coordinate. Its log probability then equals a modular function plus log(1+exp(d+sum w_i x_i)) with w_i>=0. The nonnegative second derivative of log(1+exp z), integrated over two nonnegative increments, proves L_xy log q>=0. The total coordinate complement leaves the cone unchanged. Thus four even coordinate complements represent all possible orientations and preserve p_E.

For F(z)=log(sum exp z)-p_E·z, convexity and its gradient at log q_* yield a sharp certificate. The three active rows are

L_1=e_001+e_111-e_011-e_101,
L_2=e_010+e_111-e_011-e_110,
L_3=e_100+e_111-e_101-e_110.

Exact algebra gives L_i log q_*=0 because b²=3a², and q_*-p_E=a(L_1+L_2+L_3), with a>0. Therefore for every z in this cone,

$$F(z)-F(\log q_*)\ge a\sum_iL_i(z-\log q_*)\ge0.$$

This proves the lower bound on each cone and hence on every positive-parameter mixture after the appropriate even complement. Approximation of boundary parameters extends the inequality: if the limiting q vanishes on a positive parity entry its divergence is infinite; otherwise divergence converges on the four target entries. The same argument applies to odd parity by one coordinate complement.

The local checker verifies the mixture identity, all nine inequalities and three exact multiplier identities in Q(sqrt3). It does not assume a sufficient characterization of nonnegative tensor rank at boundary points. The lower bound is therefore independent of the imported boundary-MLE classification.

## 4. Why finitely many support simplices suffice

Write rho(p)=min_(q in M) D(p||q). A stochastic channel on one visible bit maps each product to a product, hence maps M into itself. Data processing gives rho(Kp)<=rho(p). Cube symmetries preserve rho in both directions.

For two unnormalized coordinate slices u_y,v_y with nonempty supports and supp(u) subset supp(v), set

$$\tau=\min_{u_y>0}v_y/u_y>0,\quad r_{0,y}=(1+\tau)u_y,\quad r_{1,y}=v_y-\tau u_y.$$

Then r is a probability table with strictly smaller support, and p=Kr where K(0|0)=1/(1+tau), K(1|0)=tau/(1+tau), K(1|1)=1. Thus rho(p)<=rho(r). No approximation of weights occurs. If a bit is deterministic, the remaining arbitrary two-bit table is a mixture of two products by conditioning on another bit, so rho=0. Otherwise repeat until both projected slice supports are incomparable for every coordinate. Support strictly decreases, so termination takes at most seven steps.

Independent enumeration of all255 nonempty subsets finds exactly50 irreducible supports, in six disjoint symmetry orbits represented by

{0,7}, {0,3,5}, {0,1,2,7}, {0,3,5,6}, {0,1,2,4,7}, {0,1,2,5,6,7},

with orbit sizes4,8,24,2,8,4. The checker reconstructs these using bit operations, rather than trusting the supplied support list. The weights on each support remain arbitrary real numbers.

## 5. Independent exact replay of the continuous cover

The six upstream JSON files are mathematical data, copied unchanged with attribution and SHA256 hashes. No supplied Python was run or imported. Each leaf carries either an exact translated q_* or rational mixture parameters. Membership is certified by reconstructing the Bernoulli products, not by testing numerical rank.

Four support types start with their full standard probability simplex. The even-parity simplex uses all24 ordered-weight simplices: for an ordering x_1,...,x_4, its vertices are r_j=(delta_(x_1)+...+delta_(x_j))/j. For ordered weights p_(x_1)>=...>=p_(x_4), putting p_(x_5)=0 gives the exact convex combination

$$p=\sum_{j=1}^4j(p_{x_j}-p_{x_{j+1}})r_j.$$

For the five-point support, cone the analogous ordered odd-parity simplices from delta_0. There are52 roots altogether. Thus these are continuous covers, not meshes of isolated sample targets.

At each tree split, replace an edge endpoint by its midpoint in each of two children. If barycentric weights satisfy lambda_i<=lambda_j, the child replacing vertex i represents the parent point with midpoint weight2lambda_i and remaining j-weightlambda_j-lambda_i. The opposite inequality selects the other child. Hence the two children cover the parent exactly. The local checker reconstructs every rational vertex, traverses both children and rejects missing, duplicate, invalid or unreachable records.

For each leaf and its common witness q, it certifies D(v||q)<=c at every vertex v. For any convex combination p of these vertices,

$$\rho(p)\le D(p\Vert q)\le\sum_j\lambda_jD(v_j\Vert q)\le c,$$

by convexity in the first argument. The same fixed witness is essential. Combining this with the support/channel reduction proves the universal upper bound in (1) for all real probability tables.

### Independent logarithm intervals

The local checker uses integer fixed point S=2^80 and32 series terms, rather than the producer's128 bits and48 terms. For positive rational x, reduce x=2^k u with1<=u<2 and y=(u-1)/(u+1) in[0,1/3). Then

$$\log u=2\sum_{j=0}^{31}\frac{y^{2j+1}}{2j+1}+R,\qquad 0\le R\le\frac{9}{4\cdot65\cdot3^{65}}.$$

The bound follows directly by replacing all tail denominators by65 and summing a geometric series. Each fixed-point product/division is rounded down for lower bounds and up for upper bounds. The same series at y=1/3 encloses log2. Negative k reverses the appropriate interval endpoints. An integer square root bounds sqrt3 strictly between L/S and (L+1)/S; affine evaluation then bounds all star probabilities and c. No floating-point logarithm appears in a certification decision.

Every non-parity vertex is proved strictly below the lower endpoint for c. Exact parity vertices are accepted only with a matching-parity star witness, using the analytic equality already proved. Positive target mass over zero witness mass is rejected. The complete replay has16600 leaves and93792 vertex incidences, including552 exact parity incidences; the maximum depth is20. The smallest strict margin exceeds2e-6 nats. Exact per-file margins and all control counts are in `cover_verification.json`. They are margins only at the finitely many tested vertices, not a uniform gap for all nonmaximizing targets.

## 6. Equality cases and assurance boundary

Within any finite-divergence leaf simplex, D(p||q) is strictly convex in p. Any nonvertex mixture of distinct vertices therefore has strict error below c; every non-parity vertex is already strictly certified. Thus an irreducible maximizing target must be uniform parity.

If a target underwent at least one strict support reduction and the terminal table is parity u, consider the last inverse channel K. Its genuine mixing sends both input bit states to one output state with positive mass from the strictly positive q_*. In each such pair exactly one target parity entry is positive. The likelihood ratios u_x/q_*(x) differ, so equality in the log-sum inequality is impossible. Therefore D(Ku||Kq_*)<D(u||q_*)=c. Earlier channels preserve this strict upper bound. This proves that only the two uniform parity targets maximize the radius.

The present conclusion is a credited reconstruction of the September5 full candidate, not an independently discovered theorem. A separate campaign reviewer must still inspect this analytic-to-data bridge and the locally written checker before any result PR. The source remains an anonymous unrefereed submission; an AI audit does not change its journal-review status. The arbitrary-divergence wording is not solved by a KL calculation. No stronger statement for RBM(3,2), larger RBMs or all mixture component budgets is inferred here.

One substantive route was used: independent analytic reconstruction and certificate replay of the prior full candidate. This is a source-application outcome, with recommended already_solved1/5 only after separate review accepts the intended forward-KL scope and the complete verification; otherwise retain a source hold.
