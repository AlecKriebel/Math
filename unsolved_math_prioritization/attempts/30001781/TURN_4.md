# Turn 4: nonflat row coefficients and the remaining column-entropy cost

2026-10-01. Fourth substantive author turn. All rows in this turn are arbitrary independent centered isotropic log-concave vectors; no latent representation, symmetry or coordinate independence is assumed. The original conjecture is still unresolved.

## 1. A complete nonflat one-column result

Put b_k=sqrt(k) log(3n/k). There are universal C,c>0 such that, for every1<=k<=n and t>=0,

    P(A_(k,1)>C[b_k+log(3N)+t])<=2exp(-ct).                  (1.1)

After enlarging the baseline constant, this also has the benchmark form with an additive deviation s and upper tail exp(-c' min(s^2,s)). Thus the corrected sharp scale is valid for m=1, with all row coefficient profiles covered. This is a standard-probability consequence proved below, not a novelty claim or the full m-variable result.

## 2. Independent order-statistic lemma

Let Z_1,...,Z_n be independent real variables, not necessarily identically distributed, with

    P(|Z_i|>u)<=C_0 exp(-c_0 u), u>=0.

Write Z_l^* for the decreasing order of their absolute values and T_k(Z)=(sum_(l=1)^k (Z_l^*)^2)^(1/2). There is a universal constant depending only on C_0,c_0 such that

    P(T_k(Z)>C[sqrt(k) log(3n/k)+v])<=2exp(-v), v>=0.       (2.1)

Here is a direct proof. For t>=0, independence and the union bound over l-element sets give

    P(Z_l^*>t) <= binomial(n,l) [C_0 exp(-c_0 t)]^l.

Choose

    t_l=C_1[log(en/l)+v/l],

where C_1 is large enough that the last expression is at most exp(-2v-2l). The constants C_0 are absorbed because log(en/l)>=1. A union over1<=l<=k is bounded by a constant times exp(-2v), which is at most2exp(-v). Outside that exceptional event every Z_l^* is at most t_l.

Let L=log(en/k)>=1. Since log(en/l)=L+log(k/l),

    sum_(l=1)^k log^2(en/l)
      <=2kL^2+2 sum_(l=1)^k log^2(k/l)
      <=2kL^2+4k <=6kL^2.

The integral comparison in the middle uses the decreasing function log^2(1/x) and integral_0^1 log^2(1/x) dx=2. Also sum_(l>=1) l^(-2)<=2. Squaring the t_l bound and using(a+b)^2<=2a^2+2b^2 therefore gives T_k(Z)<=C[sqrt(k)L+v], proving(2.1). The proof does not require identical laws or symmetry.

Every fixed unit-direction projection Z_i=<X_i,y> meets the hypotheses by the classical one-dimensional log-concave subexponential bound, and those projections are independent across i. Crucially, T_k already optimizes over every k-sparse Euclidean row coefficient vector, including the nonflat profiles excluded from turn3.

For m=1, apply(2.1) to each coordinate column, with v=log N+t (or log(3N)+t to absorb constants), and take a union over N. This proves(1.1). The coordinates within a row need not be independent.

## 3. General column sparsity by an explicit net

Define

    H_m=m log(5eN/m).

The same argument gives, for arbitrary k,m,

    P(A_(k,m)>C[b_k+H_m+t])<=2exp(-t), t>=0.                (3.1)

Indeed, take a1/2-net of the Euclidean sphere on each m-element coordinate support, with at most5^m points. The total number of directions is at most binomial(N,m)5^m<=exp(H_m). For each direction y, apply(2.1) to the independent row projections with v=H_m+t. The union bound gives the stated exceptional probability.

To pass from the net to all directions, for each fixed support regard y->Ay as a linear operator from Euclidean m-space to R^n equipped with the norm T_k. The usual net estimate multiplies its operator norm by at most two. This step is valid for all row coefficients because T_k is a norm; no flat-vector convex-hull approximation is used.

The bound is sharp at the original scale in the row-dominated regime

    H_m <= C_2 b_k

for any fixed numerical C_2, with corresponding constants. Taking t comparable to b_k gives failure at most2exp(-c b_k). It also yields the stated complete m=1 estimate. Outside that regime the column term is larger than the conjectured a_m=sqrt(m)log(3N/m), by as much as order sqrt(m). This limitation is explicit.

A bound C[Lambda+t] with failure2exp(-ct) can be converted to the version exp(-c' min(s^2,s)) above a larger universal baseline by the same small-deviation/Markov adjustment described in turn2. We do not claim concentration around the exact mean or introduce an unstated optimal tail requirement into the original report's 'high probability' wording.

## 4. Why this route still does not close the question

The nonflat coefficient issue from turn3 is now handled exactly inside T_k. The remaining obstacle is the uniform optimization over sparse column directions. Estimate(2.1) offers an additive v cost for a single direction; a direct net with exp(H_m) directions consequently charges H_m. The desired column contribution is only sqrt(m) log(3N/m).

One cannot replace the union-bound cost by its square root using only the individual exponential tail and the number of tests. An abstract family of M independent exponential variables has maximum of order log M. That observation concerns arbitrary tests, not the correlated linear projections of one log-concave vector, and is not a matrix counterexample. It identifies which extra information a successful argument must use: geometric dependence among the column directions and/or stronger multiscale projection estimates, not just their separate tails.

The published2014 full general-row theorem already has a much smaller extra sqrt(loglog) factor than(3.1), so this elementary general estimate is not advertised as an improvement. Its value in the attempt is the complete m=1 boundary and the precise separation of the nonflat row optimization from the unresolved column process. No actual independent isotropic log-concave counterexample to the corrected conjecture was found.

The original remains unresolved after4/5 substantive author turns. One final substantive turn remains, aimed at the genuinely correlated column/multiscale step rather than recycling the invalid arbitrary-norm Chevet comparison.
