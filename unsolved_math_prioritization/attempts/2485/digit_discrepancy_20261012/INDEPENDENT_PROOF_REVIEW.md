# Independent review: digit-cylinder discrepancy bound for EP1095

Audit date: 12 October 2026. This review is an authored mathematical audit, not external peer review, a novelty determination, or a claim that either successive-ratio conjecture is resolved.

## 1. Verdict and precise accepted scope

**PASS for the complete frozen v2 proof after independent rereading and exact finite diagnostics.**

The mathematical conclusions verified by this review are:

1. With the prime number theorem as standard input, limsup log(g(k))/k <= 6/7 for the actual strict-domain Erdős–Selfridge minimum.
2. Consequently g(k) < exp(0.86k) < L_k for every sufficiently large integer k. No effective onset is supplied.
3. The stated mixed-modulus finite CRT/Bonferroni lower bound, including all endpoint errors and the strict first-survivor choice of T, is correct.
4. The two-digit disjoint-cylinder representation has exact density and the stated minimal unsigned cylinder count in the explicitly defined mod-p/mod-p² cover model.
5. The Taylor remainder sandwich (r/s)e_r(w) <= rho-Q <= e_r(w) is correct for even 2<=r<=s. Its homogeneous one-third comparison has the stated sharp asymptotic threshold kappa.
6. Under the separate omitted-block hypothesis, positivity of the exact odd Bonferroni main coefficient forces the split absolute-error budget to have liminf log(E)/k >=3kappa/20>3/25, and the full budget at least 3kappa/10>6/25.

The barrier is a theorem about the particular unsigned, absolute-error, prime-event Bonferroni certificate. It is not a lower bound on actual discrepancies, first surviving multipliers, g(k), or the performance of arbitrary sieve methods. In particular it does not prove subexponential growth impossible. The main 3/4-cutoff construction does not itself satisfy the barrier's additional omitted-block hypothesis.

Not established: an effective numerical onset, the all-k inequality g(k)<L_k, exp(o(k)) growth, either successive-ratio conjecture, optimality among all methods, or novelty/priority.

## 2. Reviewed mathematical versions and correction history

The complete original mathematical version was independently read. The preceding accepted reduced-lattice theorem was also read. The full accepted corrected proof is distributed here as [DIGIT_DISCREPANCY_THEOREM_v2.md](DIGIT_DISCREPANCY_THEOREM_v2.md); the two authored precision corrections are retained in [CORRECTION_HISTORY.md](CORRECTION_HISTORY.md).

Two prose precision issues were reported after reading v1:

- Its opening described the full forbidden cardinality as approximately p² for every omitted p>k/2. This is not uniformly true: at p=k, the forbidden cardinality is p. The correct statement is that the full representation can require order p² classes. The exact formulas and proof already covered p=k correctly.
- In the threshold proof, the sentence encompassing r>N could grammatically attach Q=rho to that entire case. Exactness Q=rho follows specifically from r>s. The separate case N<r<=s gives the needed r-bound without asserting exactness.

Neither issue changes a displayed theorem or proof calculation. The corrected v2 was independently reread in full. An exact comparison verified that only these two prose passages changed. The complete mathematical correction account is distributed with the accepted proof.

## 3. Local arithmetic and cylinder minimality

For sqrt(k)<p<=k, write k=bp+a, with 1<=b<p and 0<=a<p. As p²>k, only these two digits of k are nonzero. If p does not divide M, t -> Mt-1 is invertible modulo both p and p². Its first two digits fail Lucas precisely when n_0<a or n_1<b.

The disjoint partition is U={n_0<a} and H={n_0>=a,n_1<b}. U consists of a classes modulo p and H of b(p-a) classes modulo p². The latter excludes U, so the densities add without inclusion-exclusion: a/p+b(p-a)/p². Their sum equals 1-(p-a)(p-b)/p² and is strictly between zero and one. Counting the identical union after lifting everything to modulus p² instead gives beta=ap+b(p-a).

The unsigned component class count is h=a+b(p-a)=bp-(b-1)a<=bp+a=k. When p>k/2, b=1 and a=k-p, so h=p exactly. Its density is k/p-1+(2p-k)/p² and beta=p(k-p)+2p-k. The empty units piece at p=k leaves p high-digit-failure classes; no leading digit is discarded.

The minimum-cylinder claim is correctly restricted. A residue class modulo p is an entire units fiber inside Z/p²Z. Exactly a such fibers are wholly bad. All other fibers contain exactly b bad singleton points, with b<p, so no entire such fiber is an eligible cylinder contained in the bad set. Each wholly bad fiber costs at least one cylinder, and each remaining bad point must have its own singleton. This gives a+b(p-a), and the displayed disjoint construction attains it. The affine map permutes fibers and singletons. The proof does not imply a minimum error for signed formulas, Fourier decompositions, or correlated endpoint estimates.

## 4. Mixed CRT accounting and finite initial-interval survival

For a fixed prime subset J, expand its intersection by selecting one of the disjoint components at each prime. Any two distinct selections differ at a prime, where their components are disjoint; therefore the expanded intersections are disjoint as integer sets even though their moduli may differ.

Within each selection, exactly one prime power occurs per prime, so the moduli are pairwise coprime. CRT then produces the product of the local class counts. Each residue class in [1,T] has count differing from T/q by less than one; using at most one is valid. Summing all such errors gives the product of the sums of class counts, namely product h_p. Summing densities gives product w_p instead. The proof does not confuse h_p with a residue count for a single modulus or replace w_p by h_p/p².

For even r, the truncated inclusion-exclusion degree r-1 is odd. Its pointwise value for a point in nu>0 forbidden prime events is -binom(nu-1,r-1)<=0, while a survivor contributes one. This also covers r above the event count under the zero-binomial convention. The empty-intersection count is exactly the integer T, so it contributes no endpoint error. Thus N(T)>=TQ-E with E=sum_{j=1}^{r-1}e_j(h).

Classical consecutive Bonferroni bounds on independent events give 0<=rho-Q<=e_r(w). The coefficient inequality e_r(w)<=z^{-r}product(1+zw_p) holds for every z>0. Consequently N(T)>=T(rho-R)-E. If R<=rho/2, T=floor(2E/rho)+1 yields T rho/2-E>0, including E=0. Since N(T) is an integer, an actual multiplier exists in [1,T]. This is a genuine first-interval upper bound, rather than an inference from positive periodic density.

## 5. Lattice, every prime range, and strict domain

For k>=9, every p>3k/4 exceeds sqrt(k), so deleting it removes exactly its single occurrence in L_k. The extra product over p<=sqrt(k) is disjoint from the deleted product. The valuations of M are therefore exactly those claimed.

For small primes, divisibility of M by p^{a_p+1} makes all relevant digits of tM-1 equal to p-1. For retained sqrt(k)<p<=3k/4, M=pc with p not dividing c. If tc mod p is zero, the next digit after subtracting one is p-1; otherwise it is tc mod p minus one. Failure of the high digit b=floor(k/p) is therefore exactly tc mod p in {1,...,b}, not {0,...,b-1}. This is b distinct multiplier classes modulo p. For omitted primes, the two-digit split from Section 3 applies. There are no missing primes or missing higher relevant digits.

Both 2 and 3 lie in the small-prime range when k>=9. Their respective powers 2^{a_2+1}>k and 3^{a_3+1}>k divide M, and are coprime. Thus M>k² and every t>=1 gives n=tM-1>k+1. The survivor counted by the finite sieve is an admissible competitor for the exact g(k) defined in the theorem.

## 6. Asymptotic calculation and strict margin

The lattice identity is log M=psi(k)-theta(k)+theta(3k/4)+theta(sqrt(k)). The elementary prime-power estimate makes the first difference and final term o(k); PNT supplies log M=(3/4+o(1))k.

For retained primes near sqrt(k), 1-w>=1/p controls the potentially large logarithm. Summing even over all integers in (sqrt(k),2sqrt(k)] costs O(sqrt(k)log k). Above 2sqrt(k), w<=1/4, and log((1+6w)/(1-w))<=(6+4/3)w. The integer inverse-square tail costs O(sqrt(k)). Thus retained events are o(k/log k), including the range where w approaches one.

On the fixed omitted interval, w=u^{-1}-1+O(1/k) uniformly and 0<=u^{-1}-1<=1/3. The logarithmic function has bounded derivative in a fixed neighborhood, so replacing w costs O(1), which is negligible at scale k/log k. A continuous-function approximation by step functions on the fixed compact interval makes the PNT use legitimate without short-interval assumptions.

Independent integration gives

K=integral_{3/4}^1 log((6-5u)/(2u-1)) du
 =(9/20)log(9/4)+(1/4)log(1/2)
 =(9/10)log3-(23/20)log2.

For A=3/28, A log6-K=(176 log2-111 log3)/140. The displayed integer values of 2^176 and 3^111 are exact, and their positive difference is 4483389639004442388280709442303812380810953936563989. No floating-point comparison is required. The even ceiling choice of r differs from A k/log k by less than two. Therefore log(R/rho) has a strictly negative leading coefficient at scale k/log k, and R<=rho/2 eventually.

The separate density estimate -log rho=O(k/log k) follows from the same retained estimates and the bounded omitted logarithms. For h_p<=k and at most k primes, sum h<=k². With m=r-1, e_j(h)<=k^{2j}/j!, and monotonicity through j=m bounds E by m(ek²/m)^m. Its logarithm is (A+o(1))k because log m=log k-log log k+O(1). The factor A, instead of the earlier 2A, is justified by the compressed CRT budget, not by dropping prime-square failures.

Finally T<=2E/rho+1<=2V/rho+1 gives log T<=(A+o(1))k. Combining with the lattice cost proves 3/4+3/28=6/7. Since 6/7<43/50=0.86<1 and log L_k~k, both stated eventual strict inequalities follow. Their use of 'sufficiently large' is essential.

## 7. Exact Taylor remainder and the homogeneous threshold

For F(t)=product(1-w_i t), its rth derivative for even r is r! times the sum over r-subsets of product w_i times the remaining factors. Taylor's integral remainder at 1 therefore has exactly the stated prefactor r, not 1 or r! after division by (r-1)!.

Each remaining factor lies between 1-t and 1 on [0,1]. Integrating the resulting bounds (1-t)^{s-1} and (1-t)^{r-1} gives (r/s)e_r<=rho-Q<=e_r. The lower inequality is valid even with zero weights and at r=s; in the latter case both sides equal e_s. If r>s, the polynomial is exact, and this separate case must not be inserted into the r/s formula.

Let phi(x)=H(x)-x log3+log(3/2). Its derivative is log((1-x)/(3x)); it increases to x=1/4 and then strictly decreases. It is positive at zero and negative at one. The exact signs 5phi(4/5)=log(9375/8192)>0 and 6phi(5/6)=log(2187/3125)<0 isolate the unique root kappa in (4/5,5/6). Rational logarithm intervals independently enclose it between 0.81070 and 0.81072; these decimals are diagnostic, not proof premises.

For N distinguished weights at least one third, rho<=(2/3)^N and e_r>=binom(N,r)3^{-r} whenever r<=N. The ratio r/s is at least 2/k. The entropy lower bound binom(N,r)>=exp(NH(r/N))/(N+1) holds at endpoints as well; at r=N the distribution degenerates harmlessly. Because N/log k tends to infinity, any fixed positive lower bound on phi(r/N) outweighs the polynomial denominator. Positivity Q>0 would instead force (rho-Q)/rho<1. This proves r>=(kappa-o(1))N. For N<r<=s this conclusion is automatic; for r>s it is also automatic and Q=rho exactly.

For the homogeneous case s=N, w_i=1/3, the entropy upper bound and the strict decrease of phi after its root give e_r/rho<=exp(-c_epsilon N) uniformly on kappa+epsilon<=r/N<=1. Thus Q>0 eventually by the upper Taylor bound. At r>N exactness gives positivity directly. This proves an asymptotic threshold, not an exact finite-N threshold and not an optimal threshold for varying Lucas weights.

## 8. Residual budget theorem and limits of its interpretation

The separate family permits omission of arbitrary primes above sqrt(k), using the full general two-digit decomposition. If all but o(k/log k) primes in (3k/5,3k/4] are omitted, PNT gives N=(3/20+o(1))k/log k distinguished events. Each has w>=1/3, h=p>3k/5, and beta>=p(k-p)>=3k²/16. These uniform bounds are all correctly oriented, including the endpoint 3k/4.

For every fixed epsilon>0, positivity Q>0 makes j=floor((kappa-epsilon)N)<=r-1 eventually, by first applying the threshold with a smaller epsilon. Also j<=N, so selecting only distinguished terms gives E_split>=binom(N,j)(3k/5)^j. Even the inequality binom(N,j)>=1 suffices for the leading log(E)/k bound. Since j log k/k tends to (kappa-epsilon)3/20, letting epsilon decrease proves 3kappa/20. The quadratic lower bound for beta similarly doubles this to 3kappa/10. The strict comparisons with 3/25 and 6/25 follow from kappa>4/5.

The conclusion remains valid for r>s, since then the budget includes all degrees through N; it is not an artifact of applying the Taylor formula outside its domain. Any positive certificate TQ-E>0 requires T>E/Q>=E because Q<=rho<=1. This is a statement about the size required by that lower bound, not a statement that the first survivor truly lies that far out.

If log M=o(k), every retained prime in the distinguished interval contributes at least log(3k/5) to log M. Hence at most o(k/log k) such primes are retained and the hypothesis follows. The resulting obstruction to proving an exp(o(k)) witness is expressly conditional on using this particular absolute-error certificate. It leaves open cancellation between endpoint errors, refined sieve weights, multiple lattices or patterns, and direct constructions.

The older generating-function obstruction is also correct: for z<=1 its ratio exceeds one, and for z>1 each distinguished factor is at least (z+3)/2>=sqrt(3z). Thus r<=N/2 cannot produce R<=rho/2. Taking floor(N/2) distinguished full weights gives the weaker stated exponent. The Taylor argument genuinely strengthens this by constraining the exact coefficient Q rather than only its chosen upper remainder estimate.

## 9. Independent finite diagnostics and source checks

Independent finite diagnostics use exact integers and fractions throughout. Checks remain active in normal and both optimized execution modes. The tested families are:

- 281 omitted-prime/k pairs and 281,231 residues against exact binomial coefficients, including k=p and k=2p-1.
- The general two-digit omitted decomposition for 336 pairs and 42,294 exact binomial residues; every unsigned cylinder cover is enumerated in eight small cases, including overlapping covers.
- 17,048 retained-prime residues against exact binomials and 1,360 small-prime digit cases, with all lattice k from 9 through 90 checked for the strict domain and valuations.
- Complete joint periods for k=9,10,11,13, up to 715,715 multipliers. Every nonempty prime subset's density, mixed-component expansion, endpoint inequality at the recorded T values, finite Bonferroni bound, and actual certified survivor is checked.
- 5,460 rational weight vectors through length six, including weights zero and one, giving 14,928 Taylor-remainder checks.
- 7,380 exact entropy-binomial inequalities; exact finite homogeneous positivity examples; the main integer margin; and rational-logarithm enclosures for the homogeneous root.

The independent finite diagnostics pass in normal and both optimized execution modes with identical aggregate results. The author's distinct regression tests were also inspected and repeated in those three modes; their aggregate results agree with each other and with the original author results. The author’s broader regression suite reports 1,943,278 local residues, 280 all-subset and 92 fixed-cutoff lattices, 288,520 joint interval checks, 199,612 full-pair-period prefixes, 1,210 Taylor checks, and eight negative controls. The independent and author test families overlap but are nonidentical.

Finite tests supplement the proof; they cannot establish its asymptotic statements or an effective onset. Author diagnostics remain supplementary to the independent checks.

Fresh bounded public-source checks verified appropriate credit to the original 1974 lcm construction and the classical Brun/Bonferroni sieve. The 2021 arXiv v3 text explicitly identifies itself as an addendum and concerns the hatted approximant in its displayed asymptotic and ratio results; none of that is transferred to actual g(k). The attempted DOI fetch for the original 2020 article failed due to content type, and no fresh inspection of that article is claimed. The accompanying [source scope](SOURCE_SCOPE.md) records the public references and inspection limitations. These checks do not establish novelty or absence of stronger results elsewhere.

No remote repository mutations, publication, or external communication was performed by this audit.
