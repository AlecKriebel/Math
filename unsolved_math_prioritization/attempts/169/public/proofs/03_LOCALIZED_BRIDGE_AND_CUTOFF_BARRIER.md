# Stage 3: the localized bridge loses budget information at a logarithmic cutoff

Public mathematical edition. The source problem remains UNSOLVED by this five-stage study. Historical statements with residual swap bound 2m and Azuma denominator 8km² remain valid conservative estimates; the final synthesis uses the sharpened m and 2km² bounds. Stage labels record provenance, not additional assumptions. No claim of external peer review or priority is made.


Date: 14 October 2026. Mathematical study stage 3. Let p tend to infinity through primes, k=floor(sqrt(p)), c=floor(100 sqrt(p)), and A be a uniform k-subset of G=Z/pZ. All logarithms are natural.

## Findings

The fixed-R localized noncoverage statement from Stage 2 is not proved or disproved. Two obstacles to closing it by tuning the peeling threshold are proved here.

**A. The enlarged-envelope statement becomes false on a high-probability event once R is about log k.** With high probability there exist X,S such that

|X|<=ceil(log(p/k))+2,
|S|<=k,
H_X(A):=G\(A+(X-A)) subset A+S,
max_y(1_A*1_S)(y)=O(log p).

Thus S is light for the peeling cutoff h of order k/log k. This is a counterexample to the uniform localized lemma with that growing R. It is not a cover with at most c centres: the discarded envelope X-A can have order k log k centres. The original budget of the actual peeled subsets has been lost.

**B. Uniform Poisson moments fail even in the light, exact-cap class.** For every A and a cutoff h of order k/log k, there is an S with |S|=c, max A*S<h, but factorial moments of every fixed order j>=3 diverging. A partial translate of -A creates a spike just below the cutoff; a diffuse padding supplies the remaining centres. On the usual low-autocorrelation event the same obstruction works for correctly normalized moments on every residual H of size at least k.

The present concentration method certifies quantified enlarged residuals for R up to (1/2)log k minus a logarithmic correction. Its resulting cutoff remains much too high to remove the moment counterexamples. Lowering the cutoff sufficiently for a fixed high-order moment argument requires far more blocks; by R about log k the enlarged-envelope localized statement itself is already false. Retaining the actual peeled-block budget is therefore essential.

## 1. Exact typical inputs for A

Write D=A-A and r_A(d)=|A intersect(A+d)|.

### 1.1 Difference-set density with a quantitative error

Fix d!=0. Since p is prime, the edges {x,x+d} form a cycle C_p. The condition d notin D says that A is an independent k-set of that cycle. The exact number of such sets, for k<=p/2, is

(p/(p-k))*binom(p-k,k).

For example, count cyclic gaps of lengths at least two between the k selected points: the count is (p/k)*binom(p-k-1,k-1), equal to the displayed expression. Hence

q_p:=Pr[d notin D]
 =(p/(p-k))*binom(p-k,k)/binom(p,k).                              (1.1)

Expanding the logarithm of the product in (1.1) gives

log q_p=-k^2/p+O(k/p+k^3/p^2)=-1+O(1/k).

Consequently

E|D|=1+(p-1)(1-q_p)=(1-e^-1)p+O(p/k).                           (1.2)

Exchanging one element of A changes A-A in at most 4k positions. The without-replacement exposure/transposition coupling therefore gives

Pr[||D|-E|D||>=t]<=2 exp[-t^2/(32k^3)].                           (1.3)

Take t=p k^-1/4. Since p>=k^2, the failure probability is at most 2exp[-sqrt(k)/32]. The O(p/k) mean error is smaller than t for large p. Thus with probability tending to one,

|D|/p >= 1-e^-1-2k^-1/4.                                       (1.4)

This rate is important: an unspecified o(1) density error would not justify multiplying it by log k below.

### 1.2 Maximum difference multiplicity

Let

m_p=ceil(3log p/log log p),  L_p=3m_p.

If r_A(d)>=3m_p, the occupied-edge subgraph of C_p contains a matching of m_p edges: greedy selection discards at most three edges per selected edge. There are at most binom(p,m_p) possible matchings, and the probability that their 2m_p endpoints all belong to A is at most (k/p)^(2m_p). Therefore

Pr[r_A(d)>=3m_p]
 <=binom(p,m_p)(k/p)^(2m_p)<=(e/m_p)^m_p.

A union bound over d!=0 gives

Pr[max_{d!=0}r_A(d)>L_p] <=p(e/m_p)^m_p=p^(-2+o(1)).              (1.5)

Only the asymptotic regime is used. If 2m_p>k, the matching event is empty. Equations (1.4)-(1.5) define the high-probability event used below, with no independence-of-occupancy approximation.

## 2. A deterministic residual-patching lemma

**Lemma.** Let A be any k-set in a finite abelian group of order p with max_{d!=0}r_A(d)<=L. Let H be any subset of size m<=k. Then there is a translating set S of size at most m such that

H subset A+S,
max_y(1_A*1_S)(y) <= ceil(e(L+1)+2log p).                         (2.1)

**Proof.** Independently for each x in H choose a_x uniformly from A and put t_x=x-a_x. Let S be the set of these centres, removing duplicates. Each x is covered by a_x+t_x, and |S|<=m. For any y, define

Z_y=sum_{x in H}1[y belongs to A+t_x].

The actual representation count f_S(y) is at most Z_y, because duplicate centres are counted repeatedly in Z_y. If x=y, the summand is always one. Otherwise its expectation is r_A(y-x)/k<=L/k. Thus

E Z_y<=1+mL/k<=L+1.

This deliberately loose bound is valid whether or not y belongs to H, and does not require choosing the smallest possible L.

The summands are independent for fixed y. The exponential-moment inequality for Bernoulli sums gives

E exp(Z_y)<=exp[(e-1)(L+1)].

Markov's inequality at e(L+1)+2log p bounds the probability of exceeding that threshold by at most p^-2. A union bound over p values of y has failure probability at most p^-1<1. Some choices therefore satisfy (2.1). If H is empty, take S empty. This proves the lemma. The auxiliary random choices are a proof of existence after A and H are fixed.

## 3. A high-probability counterexample to the growing-R enlarged-residual lemma

Set

R_p=ceil(log(p/k))+2.

Condition on an A satisfying (1.4). Choose R_p independent uniform group elements x_i, allowing repetitions, and let X be their set. For every y, the probability that y is outside D+X is (1-|D|/p)^R_p. Hence

E_X |G\(D+X)|=p(1-|D|/p)^R_p
 <=p(e^-1+2k^-1/4)^R_p.

Using log(e^-1+2k^-1/4)<=-1+2e k^-1/4 and R_p=O(log k),

p(e^-1+2k^-1/4)^R_p
 <=e^-2 k exp[2e R_p k^-1/4]
 =(e^-2+o(1))k<k.                                               (3.1)

There is therefore a set X with |X|<=R_p and |H_X(A)|<=k. Apply Lemma 2 using (1.5) to obtain S with

H_X(A) subset A+S,
|S|<=k<=c,
max_y f_S(y)<=M_p:=ceil(e(L_p+1)+2log p)=O(log p).                (3.2)

This proves Finding A. In particular, for any cutoff h_p with h_p/log p tending to infinity, the set S satisfies max f_S<h_p eventually. The natural peeling cutoff h_p approximately c/R_p, of order k/log k, has this property.

The residual H_X is allowed to be empty; in that case S is empty and the proposed noncoverage statement already fails. No nonemptiness claim is needed for the counterexample to a statement quantified over every X. The argument also patches every nonempty residual of size at most k.

### Why this is not an affirmative construction at the original budget

Equation (3.2) gives a cover by (X-A) union S, with at most R_p k+k centres. This is of order k log k, not bounded by 100k as p tends to infinity. The derivation did not find a subset B of X-A satisfying both

|B|+|S|<=c  and  G\(A+S) subset A+B.                              (3.3)

Nor did it find the disjoint heavy blocks of such a B with their required sizes and peeling order. Replacing those actual blocks by the full envelope X-A is precisely where their budget and geometry were forgotten. Thus (3.2) falsifies an overbroad sufficient lemma under growing R, while (3.3) remains unresolved.

For fixed R the construction in this section does not apply: p(1-|D|/p)^R is a positive proportion of p, far larger than k. No high-probability counterexample to the fixed-R localized noncoverage claim has been established.

## 4. How far the existing affine-hole proof allows the cutoff to move

An explicit extension of the Stage 1 proof makes the quantitative tension visible. Fix an integer R and assume

2R(k-1)/(p-k+1)<=1/2.

For X of size r<=R and y notin X, noncoverage by A+(X-A) means A contains no edge from a graph of maximum degree at most 2r and with no loops. Exposing k points without replacement, after j valid points at most 2rj further points are forbidden. Therefore

Pr[y uncovered] >= product_{j=0}^{k-1}(1-2rj/(p-j)).

Using log(1-z)>=-z-z^2 for 0<=z<=1/2, define

a_p(R)=Rk(k-1)/(p-k+1)
       +[2R^2(k-1)k(2k-1)]/[3(p-k+1)^2].

Then the uncovered mean is at least

B_p(R):=(p-R)exp[-a_p(R)].

The uncovered count is 4rk-swap-Lipschitz. Uniformly over all |X|<=R, the safe Azuma and union bounds give

Pr[there exists X, |X|<=R, |H_X(A)|<B_p(R)/2]
 <=(R+1)p^R exp[-B_p(R)^2/(128R^2k^3)].                          (4.1)

For R=O(log k), a_p(R)=R+O((R+R^2)/k)=R+o(1), and the last negative exponent is

(1+o(1))*k exp(-2R)/(128R^2).

In particular (4.1) tends to zero for

R=floor((1/2)log k-3log log k)                                  (4.2)

and more generally for R<=alpha log k with any fixed alpha<1/2. At (4.2), the negative exponent has order (log k)^4, beating the menu logarithm O((log k)^2). This is a proved range, not a claim that no different method could improve it.

Let h=ceil(c/R) and apply the deterministic peeling at threshold h. At most R blocks are removed. On the event in (4.1), every hypothetical full cover leaves a remainder S satisfying

max f_S<h=O(k/log k),
|S|>=B_p(R)/(2k)=(1+o(1))*(1/2)k exp(-R).

For (4.2) this lower bound is of order sqrt(k)(log k)^3. This valid tuning does not prove that S misses H_X. It only retains a quantitatively controlled nonempty residual.

## 5. Light exact-cap sets that destroy uniform moment matching

Put

Q_p=ceil(4log p/log log p).

For sufficiently large p, let h<=k be an integer with h>=2Q_p+2, and choose any z and any B subset A of size b=floor(h/2). Start with S0=z-B. Pad S0 to exactly c points by choosing c-b points uniformly without replacement from G\S0.

For a fixed y, the padding's contribution to f_S(y) is hypergeometric, with mean at most ck/(p-b)<=101 for all sufficiently large p. The standard union bound over specified successful draws, or the hypergeometric Chernoff estimate, gives

Pr[padding contribution at y>=Q_p] <=(101e/Q_p)^Q_p.

Consequently

Pr[maximum padding contribution>=Q_p]
 <=p(101e/Q_p)^Q_p=p^(-3+o(1))<1.

Choose a padding below this bound. Then

|S|=c,
max_y f_S(y)<=b+Q_p<h,
f_S(z)>=b.                                                       (5.1)

These assertions hold for some S for every A; no exceptional-A construction is used. They yield, for any fixed j>=3,

p^-1 sum_y(f_S(y))_j >=(b)_j/p.                                 (5.2)

At the available peeling cutoff h of order k/log k, (5.2) grows as a positive constant times k^(j-2)/(log k)^j and diverges, whereas the global mean kc/p is at most 100. Thus global Poisson factorial moments cannot be uniformly approximated even over the light sets of exact cap size.

### The correctly normalized localized obstruction

Suppose additionally max_{d!=0}r_A(d)<=L_p, and let H be any set containing z with |H|>=k. For y!=z the S0 contribution is at most r_A(y-z)<=L_p. Thus the mean on H satisfies

lambda_H:=|H|^-1 sum_{y in H}f_S(y)
 <=L_p+Q_p+b/|H|<=L_p+Q_p+1.

But the j-th factorial moment on H is at least (b)_j/|H|>=(b)_j/p. At h of order k/log k, for every fixed j>=3 this lower bound grows faster than lambda_H^j. Therefore the local Poisson-moment approximation also fails, with its own correct local mean. On the event from Section 4, every residual H_X has size at least k, so this warning applies to precisely those canonical residuals.

The constructed S is not claimed to cover H. Hence this is a failure of the uniform moment-approximation route, not a counterexample to fixed-R localized noncoverage itself. A proof conditioned specifically on candidate coverage would need new information beyond the uniform moment approximation disproved here.

## 6. The cutoff scales cannot be reconciled by the present route

Even before local normalization, (5.2) shows that uniformly bounded j-th factorial moments require h=O(p^(1/j)), up to constants, rather than h of order k/log k. This necessary scale alone is far from guaranteeing vanishing approximation errors. For the order-399 Bonferroni zero-mass certificate in Stage 2, this scale is approximately k^(2/399). The improved degree-201 certificate proved in ../proofs/03_MOMENT_CERTIFICATE_BARRIER.md gives the larger but still inadequate scale k^(2/201).

The budget-only bound on the number of peeling blocks is floor(c/h). At the moment scale this permitted number is of order k^(397/399), or k^(199/201) for the improved degree-201 certificate, vastly larger than log k. No theorem reducing that number for every genuine cover has been proved; such a cover-specific improvement would be additional structural information. The present positive-residual estimate only certifies R below about (1/2)log k, and Section 3 shows that the enlarged-envelope localized noncoverage statement itself is false already by R=log k+O(1).

This does not prove that every higher-moment method is impossible. It proves that the specific plan of lowering the heavy-point cutoff, discarding actual block data in favor of X-A, and then applying uniform untrimmed Poisson moment matching cannot be justified by these estimates. Truncated observables, a cover-specific inverse theorem, or an argument retaining the original block budget could behave differently.

## 7. The strongest surviving budget-aware formulation

The exact peeling information is the following data:

- centres x_1,...,x_r with r<=R;
- disjoint blocks B_i subset x_i-A, each of size at least h;
- the remainder S disjoint from all blocks;
- total size sum_i|B_i|+|S|<=c;
- max_y(1_A*1_S)(y)<h.

Write B=union_i B_i and H_B=G\(A+B). A sufficient budget-aware local theorem is

For every such collection, H_B is not contained in A+S.           (7.1)

Every admissible full cover yields such a collection by peeling. Conversely, a violation of (7.1) is a full cover within the original cap. Thus (7.1) is an exact reformulation with structural data, not an easier result already proved. Replacing H_B by the smaller H_X throws away the first four constraints' interaction and can lead to the false growing-R statement in Section 3.

For fixed A and X, a b-element union B has at most binom(rk,b) possibilities, since X-A has at most rk points. This count can be smaller than binom(p,b), but the menu depends on A and S remains unrestricted. The count alone gives no model-correct probability bound. No proof that (7.1) holds on a positive-probability typical-A event, and no realization of the Section 3 patch using a budget-feasible B, has been obtained.

## 8. A budget-preserving way to discard high target multiplicities

There is a simple uniform fact that avoids replacing centre sets by large envelopes. On the event max_{d!=0}r_A(d)<=L, every T of size t satisfies

sum_y f_T(y)^2=kt+sum_{d!=0}r_A(d)r_T(d)
              <=kt+L t(t-1).

For t<=c this is at most 10100Lp, for all sufficiently large p and L>=1. Choose an even integer M>=L^2 with M<L^2+2. Then, simultaneously for all such T,

|{y:f_T(y)>M}|<=10100p/L^3,
sum_{y:f_T(y)>M}f_T(y)<=10100p/L.

At L=L_p from Section 1, both bounds are negligible relative to p. These are global bounds. On a localized set H the corresponding normalized estimates require division by its density |H|/p; no uniform negligible-error assertion for shrinking H is inferred. Clipping the values to min(f_T,M) changes their mean by o(1), preserves their zero set exactly, and keeps the original centre budget unchanged. This lemma does not prove a hole, but it removes the isolated-spike difficulty without introducing an enlarged centre envelope.

Even for this clipped variable, exact universal Poisson-law matching is false. Take T=A. Every non-diagonal ordered representation of y as a+a' comes with its reversed representation. Therefore f_A(y) is even outside the diagonal set {2a:a in A}, which has exactly k elements because p is odd. Since M is even, clipping preserves this parity outside those positions. The clipped distribution puts probability at most k/p on odd values, whereas a Poisson variable of mean k^2/p puts probability (1-exp(-2k^2/p))/2 on odd values, tending to (1-e^-2)/2. Their total variation distance therefore stays bounded away from zero for every A.

### The parity obstruction survives the exact cap

The same failure can be placed at the original cap without special A. Fix 100 distinct shifts u_1,...,u_100, for example 0,...,99 once p>100. Put U=union_i(A+u_i), and let d=100k-|U| be the deficit from repeated centres. On the event max r_A<=L, the elementary union bound on overlaps gives

0<=d<=sum_{i<j}|(A+u_i) intersect (A+u_j)|<=4950L.

Since 100k<=c<=100k+99, pad U to a set T with exactly c centres, adding at most d+99 points. The indexed convolution

g(y)=sum_i (1_A*1_A)(y-u_i)

is even outside a union of at most 100k diagonal positions. Passing from the indexed union to U removes only centres that were repeated, at most d distinct centres. The convolution can change only on the union of their A-translates, of size at most kd. Padding affects at most k(d+99) more positions. Consequently

|{y:f_T(y) is odd}|<=100k+k(2d+99)<=199k+9900kL.

For L=L_p=o(k), the odd fraction is o(1). Clipping at the even M chosen above preserves this conclusion. The exact untrimmed mean is kc/p ->100, and the second-moment estimate shows that the clipped mean also tends to 100. A Poisson law with either mean has odd mass tending to (1-exp(-200))/2. Thus even an exact-cap, budget-preserving, bounded-observable formulation cannot invoke a universal Poisson law. No coverage claim is made for this T.

A possible surviving route is a one-sided estimate for the zero mass of a bounded or clipped convolution observable, allowing compound or other positively clustered laws. Neither the second-moment trimming lemma nor the preceding examples establish such an estimate uniformly over unrestricted T. The joint-dependence issue remains.

## 9. Independent audit and finite identity checks

The independent adversarial audit checked the exact cycle count, quantitative mean and concentration estimates, the patching lemma with duplicate centres, the finite-p exponent a_p(R), the constant 128 in the union bound, the logarithmic cutoff comparison, exact-cap padding, local normalization, and the global clipping and parity arguments. Its requested clarifications are incorporated: the patching group is abelian; its mean bound handles y outside H; shrinking residuals are not described as positive-density; and localized clipping needs a density factor.

## Disposition

Accepted progress: a high-probability counterexample to the growing-R enlarged-residual lemma; exact cycle and patching inputs; a quantitative controlled range for the peeling reduction; a universal full-budget light-moment obstruction; and a budget-preserving truncation with an exact-cap parity obstruction to universal Poisson matching. The fixed-R budget-sensitive bridge, and therefore the original prime/fixed-size/cap problem, remain unresolved.

