# Turn 4: a strictly positive corruption comparator at the bounded-prior regret rate

**Scoped partial; the adaptive selection/refit question remains unresolved at 4/5.** For the exact source family, this turn proves that the deterministic positive schedule h_n=n^(-4) attains the known bounded-prior empirical-Bayes regret order. The argument explicitly passes through the discontinuous gap-filled h=0+ limit. It does not claim that cross-validation chooses a comparably good h.

## 1. Scope and classical inputs

Let Lambda_i be iid from G supported on [0,M], with fixed M<infinity, and Y_i|Lambda_i independent Poisson(Lambda_i). For an estimator A(Y), define average regret

 Reg_G(A)=E||A(Y)-Lambda||^2/n-mmse(G)
         =E||A(Y)-f_G(Y)||^2/n,

where f_G(y)=E[Lambda|Y=y]. The second identity uses the iid-prior model, since conditioning on the entire sample still gives E[Lambda_i|Y]=f_G(Y_i). It is not an assertion for arbitrary deterministic means relative to an unspecified Bayes oracle.

We use the classical fixed-sample Robbins bound of Polyanskiy--Wu, *Sharp regret bounds for empirical Bayes and compound decision problems*, arXiv:2109.03943v2, Theorem 2 and Appendix C, equation (115). Their estimator (5) is exactly the in-sample rule R(Y_i)=(Y_i+1)N(Y_i+1)/N(Y_i). It has total regret O_M((log n/log log n)^2), hence average regret O_M(r_n), r_n=(log n/log log n)^2/n. Their matching lower bound makes this order minimax. The Robbins rate and isotonic projection principle are credited prior theory.

Brown--Greenshtein--Ritov (2013), Section 2.4, already identifies the gap-filled limit of the unprojected source smoother as h decreases to zero. That limit is not a new discovery here. The present deductions are an explicit uniform convergence bound for the full source family, a missing-bin comparison at the regret scale, and the resulting strictly positive comparator. No historical-priority claim is made.

## 2. The known gap-filled limit, with quantitative uniform control

Fix a sample y of n nonnegative integers. Let its distinct values be x_1<...<x_J, empirical weights pi_{x_j}=N(x_j)/n, and m=x_J. For the unprojected source function b_h from Turn 1, define

 b_+(x_j)=x_{j+1} pi_{x_{j+1}}/pi_{x_j}, j<J;
 b_+(x_J)=0.

Let P_pi be weighted least-squares isotonic projection on these observed values, so Delta_h=P_pi b_h, Delta_+=P_pi b_+, and Delta_0 is the separately defined projected Robbins endpoint.

**Lemma 1.** For every sample and 0<h<=1,

 max_{y observed}|b_h(y)-b_+(y)| <= m n(n+3)h,
 max_{y observed}|Delta_h(y)-Delta_+(y)| <= m n(n+3)h.             (1)

The all-zero sample has all these values zero. In particular, the claim does not identify Delta_+ with Delta_0.

### Proof

For z=y+j>=y observed, write s=max{t observed:t<=z}. The shifted convolution identity from Turn 1 writes the first-stage smoother as

 a_h(z)= [sum_t t pi_t k_h(z+1-t)]/q_h(z),

with q_h(z)=sum_t pi_t k_h(z-t). For terms t<=s, use the denominator contribution pi_s k_h(z-s). Their sum is bounded by

 sum_{t<=s}(t pi_t/pi_s) h^(s+1-t)(z-s)!/(z+1-t)!
   <= h sum_{t<=s}t pi_t/pi_s <= m n h.                          (2)

Here pi_s>=1/n, h<=1, and the factorial ratio is at most one. Averaging over j with Poisson(h) probabilities keeps the bound mn h.

The only other possible numerator term has t=z+1 observed. Such terms are indexed by t>y, with s the preceding observed value before t. Their contributions after the j=t-y-1 Poisson averaging are exactly

 J_t=e^(-h)(t pi_t/pi_s)h^(s-y)(t-s-1)!/(t-y-1)! /(1+R_s),

 R_s=sum_{r<s}(pi_r/pi_s)h^(s-r)(t-s-1)!/(t-r-1)!.              (3)

For the first observed t>y, s=y, 0<=R_y<=nh, and J_t=b_+(y)e^(-h)/(1+R_y). Consequently

 0<=b_+(y)-J_t<=b_+(y)(h+R_y)<=mn(n+1)h.                        (4)

For every later observed t, s>y; thus the sum of those J_t is at most

 h n sum_t t pi_t <= hnm.                                      (5)

If no t>y exists, all jump terms are absent and b_+(y)=0. Combining (2), (4), and (5) proves the first inequality in (1). Isotonic projection is order-preserving and translation-equivariant; its max-min formula in weighted interval averages proves both facts directly. If ||u-v||_infinity<=epsilon, then v-epsilon<=u<=v+epsilon, and these facts imply ||P_pi u-P_pi v||_infinity<=epsilon. This proves the second inequality.

## 3. Exact comparison with the Robbins endpoint

Pointwise on the observed domain b_+>=b_0, because b_0(y)=(y+1)pi_{y+1}/pi_y is either exactly b_+(y) or zero. Therefore

 0<=Delta_0<=Delta_+<=m.                                        (6)

The upper bound follows either by (1) and Turn 1, or by the suffix-mean formula: every suffix sum of pi_y b_+(y) is a sum of t pi_t over a smaller suffix and is at most m times the original suffix mass.

Weighted isotonic projection preserves the weighted mean. If l is the sample minimum, then the exact mean difference is

 sum_y pi_y[Delta_+(y)-Delta_0(y)]
   =sum_{t>l, N(t-1)=0} tN(t)/n.                               (7)

Indeed the b_+ weighted mean includes each t pi_t except the minimum support point, whereas b_0 includes precisely those t with t-1 observed. Using (6), the empirical squared difference D(y) satisfies

 D(y):=sum_y pi_y[Delta_+(y)-Delta_0(y)]^2
   <=m sum_{t>l,N(t-1)=0}tN(t)/n.                              (8)

For a mixture supported on [0,M], its count probabilities p_t obey t p_t<=M p_{t-1}. Also, for iid count observations,

 E[N(t) 1{N(t-1)=0}]=n p_t(1-p_{t-1})^(n-1).                  (9)

To check (9), sum the n indicators that a specified observation equals t and all other observations differ from t-1. This is a direct multinomial calculation; no independence between adjacent empirical counts is assumed.

Fix an integer cutoff L>=1. On the event m<=L use (8), drop the sample-minimum restriction for an upper bound, and then use (9). Since x(1-x)^(n-1)<=1/n for 0<=x<=1 and n>=1,

 E[D(Y)1{m<=L}]
   <=L sum_{t=1}^L t p_t(1-p_{t-1})^(n-1)
   <=M L sum_{t=1}^L p_{t-1}(1-p_{t-1})^(n-1)
   <=M L^2/n.                                                 (10)

On m>L, (6) gives D(Y)<=m^2 and

 E[m^2 1{m>L}]<=sum_i E[Y_i^2 1{Y_i>L}]
              <=n E[Z^2 1{Z>L}], Z~Poisson(M).                 (11)

The last inequality follows by stochastic domination of each mixture count by Poisson(M), since z^2 1{z>L} is nondecreasing. For fixed M>0, choose L_n=ceil(A log n/log log n) with any fixed A>3, for sufficiently large n. The Poisson bound P(Z>=k)<=(eM/k)^k and the exact identity

 E[Z^2 1{Z>L}]=M^2 P(Z>=L-1)+M P(Z>=L)

show that the right side of (11) is n^(1-A+o(1)), hence O_M(n^(-2)) after increasing A slightly, for example A=5. Small n can be absorbed into a constant depending on M. If M=0 all estimators vanish. Thus

 sup_{G supported on [0,M]} E D(Y)=O_M(r_n),
 sup_G E m^2=O_M((log n/log log n)^2).                          (12)

## 4. A positive-h minimax-order comparator

The posterior mean vector f_G(Y) is monotone as a function of the observed count. Projection onto the weighted isotonic cone therefore cannot increase its squared distance from the Robbins vector, sample by sample. The credited Robbins bound consequently gives Reg_G(Delta_0)<=O_M(r_n). By the regret identity and (12),

 Reg_G(Delta_+)<=2 Reg_G(Delta_0)+2E D(Y)=O_M(r_n).               (13)

Now choose the strictly positive h_n=n^(-4). Lemma 1 gives, for n>=1,

 ||Delta_{h_n}(Y)-Delta_+(Y)||^2/n
   <=[n(n+3)h_n]^2 m^2 <=16m^2/n^4.                            (14)

Another squared-triangle inequality and (12)-(14) imply

 sup_{G supported on [0,M]} Reg_G(Delta_{n^(-4)})=O_M(r_n).       (15)

This uses the exact original smoother and empirical-multiplicity isotonic projection, without clipping, changing the family to ERM, or treating h=0+ as h=0. The exponent 4 is a convenient sufficient choice, not asserted optimal. The known minimax lower bound supplies matching order in n; no new minimax lower bound is claimed.

## 5. Consequences and what remains

Any deterministic positive grid H_n that contains n^(-4) now has a proved O_M(r_n) comparator for the iid bounded-prior model. This removes the comparator hypothesis from the conditional full-refit oracle reductions in Turns 2 and 3, within that model. The adaptive correction Omega remains unbounded for their selectors. Consequently, (15) is a result about a fixed positive schedule, not a theorem that the original cross-validation/refit rule attains this rate. No heavy-tail or arbitrary deterministic-mean compound-regret extension is asserted.

The h=0+ gap-filled formula and the Robbins minimax rate are known inputs. The explicit comparison above is retained as a scoped deduction, with no historical novelty certification. This completes substantive author turn 4; one author turn remains unless a separate full-source review finds a complete target resolution. All claims await independent audit.
