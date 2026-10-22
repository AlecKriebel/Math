# Independent reconstruction before prior opinions

The exact claim is an existence theorem for a deliberately selected sequence of bounded-degree trees, dense cross-root traffic, capacity prices positive and linear, fixed-topology upgrades, and iid quenched exponential slopes. It does not purport to settle a uniquely specified conjecture or provide Aldous’s preferred canonical model.

## Algebra and optimization

Each physical edge separates a descendant block of k_e leaves all on one side of the root. With unit cross-root commodities its forced initial load is k k_e. Doubling all commodities forces every upgraded capacity independently to be at least 2k k_e. That vector is feasible. Strict positivity of each linear marginal price forces uniqueness of the componentwise minimum. This conclusion would fail for zero prices or topology changes; these cases are expressly excluded.

The full family of tree constraints is equivalent to k row and k column bounds of 2k: every internal edge load is a sum of its descendant terminal loads. The auxiliary directed network has source-to-row and column-to-sink capacities 2k and row-to-column capacities d_ij. For the cut retaining rows A and columns B with the source, its capacity is 2k(k-|A|+|B|)+sum_(A x (R\B))d_ij. Thus the displayed formula follows from max-flow/min-cut. It is a finite minimum of affine nonnegative-slope functions; continuity, concavity and the minimum active slope on the right follow by local strict separation from every inactive cut. Every slope lies between 0 and S_k; normalization is by actual S_k>0, not k².

If offered rows and columns are strictly below 2k, the whole offered matrix is feasible and uniquely attains total offered demand because each entry is upper bounded. Summing strict descendant terminal slack gives strict slack on every physical edge. If F=2k², the sum of k row bounds is attained, so every row is at its bound; similarly every column is at its bound. Every descendant aggregate and both root edges then saturate for every optimizer. No choice of a preferred optimizer is needed for these phases.

## Probability and time quantifiers

For Gamma(n,1), exponential Markov with lambda=1-1/a, using the reversed inequality for negative lambda when a<1, gives exp(-n[a-1-log a]). The derivatives of I((1-delta)^-1) and I((1+delta)^-1) with respect to delta are delta/(1-delta)^2 and delta/(1+delta)^2. Integration yields delta²/2 and delta²/8 for 0<delta<1. No independence between intersecting rows or cuts is used.

Lower endpoint: 2k row/column tests, each n=k, yield 2k exp(-k delta²/2); substituting delta=8 sqrt(log k/k) gives 2k^-31. Failure includes equality, giving strict slack on the good event. Finitely many strict inequalities persist to the right of the endpoint, making the endpoint right derivative equal S_k.

Upper endpoint: only a+d>k need checking. With Z on A x D, failure requires ad+(1+delta)Z<2k(a+d-k)<=2ad, hence Z<ad/(1+delta). The algebraic gap is (k-a)(k-d)>=0. Set q=min(a,d), ell=k-max(a,d): ell<q and ad=q(k-ell). For q<=floor(k/2), count orientations by at most 2 binom(k,q)binom(k,ell); summing ell=0,...,q-1 bounds count by 2q k^(2q). Here ad>=qk/2. For q>k/2, ad>k²/4 and all possible cuts number at most 4^k. For c>=8log k/k the resulting terms are 2q k^-2q and (4/k²)^k. The geometric derivative identity gives sum 2q k^-2q=2k^-2/(1-k^-2)^2. Empty A/D and a<=b cuts are automatic; a=k,d=k lies in the large class; q=1,ell=0 is included. The upper event permits cut equality, which suffices for saturation and a zero right derivative.

All-time statements require only two endpoint events. Every earlier time retains strict lower-phase slack since X>=0; every later time retains a capacity-saturating flow since upper bounds increase. Thus no union bound over uncountably many times is invoked. A measurable optimizing selection exists by enumerating finitely many LP bases, retaining feasible bases with maximal objective and selecting the first; every such vertex depends measurably on the demand matrix. For any measurable selection, the probability of violating the claimed outer phase is at most epsilon_k.

For fixed t<2 or t>2, delta_k eventually places it in its phase and epsilon_k tends to zero. At t=2 monotonicity sandwiches F(2) between k²+(1-delta_k)S_k and 2k² on the good event; S_k/k² converges in probability to 1 by variance k^-2. No derivative limit at 2 follows. On binary k, epsilon_k is summable; first Borel-Cantelli gives eventual good events under every common coupling, with no independence across k needed.

## Attempted falsifiers

Individual row/column feasibility alone does not prove upper saturation; mixed rectangle cuts must remain. Replacing positive costs by nonnegative costs breaks uniqueness. Replacing X>=0 by arbitrary slopes breaks the uniform time extension. Omitting the minimum active slope at ties gives wrong right derivatives. Replacing the realized S_k normalization by k² loses exact r=1 below the transition. Each of these would invalidate a broader claim; the final theorem excludes or explicitly handles them. The analytic proof has no identified gap at this reconstruction checkpoint.
