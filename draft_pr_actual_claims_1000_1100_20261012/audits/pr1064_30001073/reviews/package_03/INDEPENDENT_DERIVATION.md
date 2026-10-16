# Independent derivation, frozen before earlier review verdicts

The target is a fixed unnormalized bound on the squared Frobenius norm of a doubly stochastic matrix. The claimed upper estimate is stronger: it needs only nonnegative row sums equal to one. Write P for a random permutation with arbitrary law and B for its marginals. This derivation does not assume B equals the input matrix.

Give the rows independent continuous uniform priorities. For any fixed order, the entropy chain rule and relative entropy to the marginal row restricted to the columns still available give

    H(P) + sum b_ij log b_ij <= sum_i E log Z_i.

Every history used has positive probability. Its conditional distribution is supported on positive marginal entries in the available set, so Z_i is positive. Conditioning instead on the entire supported permutation and a priority t, the conditional expectation of Z_i is b_i,P(i)+(1-t)(1-b_i,P(i)). Jensen and integration therefore give

    E log Z_i <= -1 + sum_j q(b_ij),
    q(b) = -b^2 log b/(1-b), q(0)=0, q(1)=1.

There is no illegal exchange of an entropy conditional law with a full-permutation conditioning: the conditional-law inequality is averaged first, and only its scalar right side is subsequently reconditioned. A finite permutation law bounds every sampled positive b away from zero. The logarithms and integrals are consequently integrable. Deterministic permutations give equality, a useful endpoint check.

For positive permanent, specialize to the Gibbs permutation law with probabilities proportional to products of input entries. Then log per(A)=H(P)+sum b log a. Its marginals B are doubly stochastic, b>0 implies a>0, and both B and a row-stochastic A have total mass n. Thus

    log per(A) <= -n + sum [q(b)-d(b,a)],
    d(b,a)=b log(b/a)-b+a >=0.

At b=0<a, d=a must be retained; only the global sums of linear terms cancel. At a=b=0, d=0. An a=0<b cannot appear under the Gibbs law. Zero permanent is a separate trivial case.

For the scalar inequality, set h(x)=x^2(1-log x), with h(0)=0. The elementary b log(1/b)<=1-b gives q(b)<=b and q(b)<=h(b). If b>=exp(2)a, then d>=b+a>=q(b). Otherwise discard d>=0. On [0,1], h is increasing because h'(x)=x(1-2 log x)>0. For b<=a, h(b)<=h(a); for a<b<exp(2)a, compare the square factors and the logarithms separately to obtain h(b)<=exp(4)h(a). This also covers b=1 by limits and does not use monotonicity beyond one. Consequently q-d<=exp(4)h(a).

Summation gives the entrywise entropy bound. Cauchy--Schwarz in each row gives S=sum a^2>=1. The probability law p=a^2/S has at most n^2 atoms, and exactly

    sum a^2 log(1/a) = S/2 [H(p)-log S] <= S log n.

Hence per(A)<=exp[-n+exp(4)S(1+log n)] for every n>=1. For fixed S<=gamma the all-n prefactor is exp(exp(4)gamma)n^(exp(4)gamma). For n>=2, 1+log n<=3log n; the corresponding pure-power estimate is not asserted at n=1. The doubly stochastic lower bound is prior van der Waerden and is not a lower bound for arbitrary row-stochastic matrices.

Uniform blocks with n=km and S=k give permanent (m!/m^m)^k, asymptotic exp(-n)(2pi/k)^(k/2)n^(k/2). Thus polynomial loss is necessary, with the exponent here deliberately loose. A normalized hypothesis S/n<=gamma would admit permutation matrices and would not answer the source's question.

Before reading earlier verdicts I find no analytic gap in this reconstruction. What remains is source attribution, independent numerical falsification controls, and distribution/compilation verification. The mathematics proves a credited corollary; it does not prove historical novelty.
