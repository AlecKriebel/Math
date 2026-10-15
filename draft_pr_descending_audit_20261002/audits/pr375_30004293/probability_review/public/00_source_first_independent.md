# Source-first probability audit (sealed before candidate access)

Scope: independent adversarial audit of the Bernoulli subset-sum model, its literal infinite-set question, and prefix lower bounds. No candidate proof, candidate code, historical review, root verdict, or sibling analysis has been read. Sources were fetched afresh directly from the specified original URLs. This document does not certify the 94/134-page FGK proof as a whole; its stated theorems are external inputs.

## Exact objects and source boundaries

Let independent X_i have P(X_i=1)=1/i, including X_1=1, and A={i:X_i=1}. Representations are finite subsets, without repetitions or order. Set r_A(x)=#{B subset A: sum B=x}, M(D)=max_x r_{A intersect [1,D]}(x), and M_h(D)=max_x #{B subset A intersect [1,D]: |B|=h, sum B=x}. Empty subsets are allowed and represent zero once. For each fixed x>=0, r_A(x) is finite because all participating elements are at most x; negative x has count zero.

Green's OWR 50/2019 contribution, printed pp.3164-3167 (PDF pages 24-27), formulates an untruncated model question and immediately distinguishes an annular, fixed-k threshold problem. FGK v3 and the published paper define beta_k through probability tending to one for k distinct equal-sum subsets of [D^c,D], not through an almost sure eventual assertion. These statements require separate probability modes.

FGK Theorem 2 and Corollary 1 provide the external numerical lower input eta=log(2)/log(2/rho)=0.3533227727..., rho=0.2812113496.... Lemma 2.1 supplies a prefix lower bound in probability and its following remark explicitly identifies prefix growth as of independent interest. Therefore a claim of an unprecedented first prefix lower bound would conflict with the source. Theorem 7 gives only tilde-gamma_k <= beta_k <= gamma_k; equality and general perturbation from weak to strict entropy remain unproved there. Restricted subflag tests cannot be substituted for all subflags without a separate reduction theorem.

Both fetched FGK versions visibly print beta_k <= beta_{k+1} in the Corollary 1 proof. The model definition instead implies beta_{k+1} <= beta_k: k+1 representations imply k. This is a source typo, not a license to reverse the actual monotonicity. Dyadic interpolation still works with the correct direction.

## Proposed mechanisms and exact checks, before candidate exposure

1. Literal infinite supremum: use fixed-k source inputs, monotonic prefix counts, and countable intersection. No rate, tensor power argument, or zero-one law is necessary.
2. Almost sure lower prefix exponent: use fixed deterministic disjoint annuli and a strong law for independent bounded indicators. Explicitly handle an excluded integer endpoint and do not claim probability-to-one alone implies eventual almost sure success.
3. Tail invariance: convolution gives multiplicative 2^{|F|} comparison after removing any fixed finite F. Kolmogorov's law makes liminf and limsup exponents individually deterministic; it does not make them equal.
4. Fixed-cardinality stabilization: cancel common elements from colliding subsets and sum the expectations of all bounded-size disjoint relations. This produces a finite random collision core. Check the distinction between exactly h and at most h.
5. Controls: exhaustive finite subsets, all disjoint tensor products, harmonic composition identities, a monotone sequence with unequal normalized liminf/limsup, and a probability-to-one sequence with infinitely many failures. These are structural controls, not sampled prefix-count simulations.

## Independent deductions

### A. Literal supremum

For every fixed k with beta_k>0, choose 0<c<beta_k. The admissible set is downward closed: a larger annulus contains a smaller one. Hence the definition as a supremum gives the probability-to-one assertion at c, without assuming the endpoint beta_k is admissible. M(D) then tends to infinity in probability. Since M(D) is nondecreasing, P(sup_D M(D)>=k)=1. FGK supplies positive beta_k for all fixed k (their Theorem 2 plus monotonicity, or the explicit remark after Theorem 7). Intersect over k. Thus sup_x r_A(x)=infinity almost surely. Every individual r_A(x) remains finite, so there is no attained infinite maximum. This is a corollary of established threshold results, not a determination of a finite-prefix growth exponent.

### B. Independent annular amplification with an almost sure mode

Fix k>=2 and 0<c<beta_k. Let U_j=exp(c^{-j}) and I_j=[U_j,U_{j+1}) intersect N, j>=0. These deterministic coordinate sets are pairwise disjoint. Since U_j=U_{j+1}^c, the event E_j that I_j contains k distinct equal-sum subsets has probability tending to one. The source uses a closed upper endpoint; deleting that endpoint changes the probability by at most 1/U_{j+1} if it is an integer, and by zero otherwise.

Y_j=1_{E_j} are independent and bounded. If S_n=sum_{j<n}Y_j, Hoeffding gives P(|S_n-E S_n|>epsilon n)<=2 exp(-2 epsilon^2 n), a summable bound. Borel-Cantelli and rational epsilon imply (S_n-E S_n)/n ->0 almost surely; Cesaro and P(E_j)->1 give S_n/n ->1. Select one of k equal-sum subsets independently in each successful annulus. Disjoint supports make all k^{S_n} unions distinct, with identical total sum. They lie below U_n, so M(U_n)>=k^{S_n}. As log log U_n=n log(1/c),

liminf_{D->infinity} log M(D)/log log D >= log k/log(1/c), almost surely.

Interpolation uses M(U_n)<=M(D) for U_n<=D<U_{n+1}; the ratio n/(n+1) tends to one. Countably many k and rational c<beta_k then give the stronger abstract bound

liminf log M(D)/log log D >= sup_{k>=2} [log k/log(1/beta_k)] >= zeta_plus >= eta,

almost surely, where endpoint passage is continuity from below. If only the stated external corollary is used, the advertised numeric consequence is the eta lower bound. This derivation adds a probability mode to the same tensor-power mechanism; no new improvement of eta or matching upper exponent has been obtained.

### C. Tail invariance and deterministic exponents

For finite disjoint F and B, coefficients of product_{a in F union B}(1+z^a) are the convolution of the two nonnegative coefficient arrays. Thus M(B)<=M(F union B)<=2^{|F|}M(B). For finite changes in the Bernoulli coordinates, the values log M(D)/log log D differ by a quantity tending to zero. The liminf and limsup are tail random variables in the extended interval [0,infinity]. Applying Kolmogorov's zero-one law to rational threshold events makes each equal to an almost surely constant value (possibly infinity). This supplies no equality of the two constants and no upper bound. A deterministic monotone staircase can have liminf 1 and limsup 2 after this normalization; finite-change invariance does not prevent that.

### D. Fixed h: finite collision core and eventual constant maximum

For t>=1, let g_t(s) be the sum of product_{a in B}1/a over t-element subsets B of N summing to s. Enlarge to ordered tuples with repetitions to obtain

g_t(s)<=H_{s-1}^{t-1}/((t-1)! s).

Indeed, for each ordered composition a_1+...+a_t=s, replace product 1/a_i by (1/s) sum_i product_{j!=i}1/a_j, and bound the resulting t-1 tuple sum by H_{s-1}^{t-1}. This gives ordered weight <=t H_{s-1}^{t-1}/s, then divide by t!.

For fixed h, consider disjoint nonempty U,V subset A, |U|,|V|<=h, sum U=sum V. Independence on their disjoint supports gives expected relation count at most

sum_{p,q=1}^h sum_{s>=1} g_p(s)g_q(s) <= C_h sum_s (1+log s)^{2h-2}/s^2 < infinity.

Hence only finitely many such relations occur almost surely; C is the finite union of their supports. If two subsets of A of cardinality <=h have equal sum, cancel their intersection. Their nonempty differences form one of these relations, so their parts outside C are identical. For a fixed sum, all the representations therefore share the same outside subset T. For at-most-h counts the representation number is bounded by the maximum at-most-h count within C, and the latter is attained within C. The at-most-h maximum stabilizes once C is in the prefix.

For exactly h, all representations have identical outside subset T, so their parts in C all have cardinality h-|T|. Thus the maximum is bounded by max_{0<=j<=h} M_j(C). Because A is almost surely infinite (independent Borel-Cantelli and sum_i1/i=infinity), each chosen core family of cardinality j can be completed by h-j elements of A outside C. This attains the bound at some finite prefix. Therefore M_h(D) is eventually a finite random constant. Reusing an exact-h bound from at-most-h without this completion step would be a gap.

## Strongest independent result and exact gap

Validated by deductions above: literal unboundedness, an almost sure eta prefix lower exponent conditional on established FGK threshold results, deterministic extended liminf/limsup exponents, and finite eventual exact-h maxima. No matching upper prefix exponent, no proof that the liminf and limsup agree, no new numerical improvement beyond FGK, no divisor transference, and no general weak/strict entropy equality have been proved. Numerical controls cannot fill any of those gaps.

Checkpoint: 2026-10-03 06:54 UTC (exact seal time in JSON). Audit completion estimate 35%. This estimate concerns completion of the assigned audit, not solution of the quantitative open problem. Independent proposal/verdict sealed before any candidate access.
