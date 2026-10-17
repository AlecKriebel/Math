# Root check of the older Gaussian implication

This is a new candidate-aware deduction, not a statement located verbatim in the older paper and not a historical first-disproof date. No external communication was made. Root read the exact version-specific primary Theorem 1 (PDF pp.2–3) and the complex-Gaussian specialization (p.10), plus repository version metadata and publisher bibliographic metadata. Root did not independently audit all of Nikula's proof. Independent source families separately record their wider proof inspection.

## Authenticated theorem and date boundary

Miika Nikula, *Frequent hypercyclicity of random entire functions for the differentiation operator*, arXiv:1209.6209v1. Theorem1 assumes IID complex jets X_n with full support in C and a logarithmic tail bound: for some beta>0, limsup_(r→infinity) (log r)^(1+beta) P(|X|≥r)<infinity. It concludes that sum X_n z^n/n! is almost surely entire and frequently hypercyclic for differentiation in H(C). The standard circular complex Gaussian qualifies (real/imaginary parts independent with variance1/2). The repository lists v1 submitted2012-09-27 12:45:47 UTC; publisher metadata gives online2013-10-08, Complex Analysis and Operator Theory8 (2014),1455–1474, DOI10.1007/s11785-013-0328-0. The retrieved v1 PDF has an internal 'Date: August2,2018'; its cause is not authenticated. The repository version date is reported as repository metadata, without redating the exact multiplier conclusion or assuming journal theorem numbering/content identity from an inaccessible journal body.

## One probability-one coefficient event

For circular complex Gaussian X of density pi^-1 exp(-|z|^2), P(|X|<r)=1-exp(-r^2)≤r^2 and P(|X|>R)=exp(-R^2). Consequently

sum_(n≥1) P(|X_n|<(n+1)^(-3/4))<infinity,
sum_(n≥1) P(|X_n|>log(n+e))<infinity.

For the second inequality, the summands are eventually ≤n^-2. First Borel–Cantelli, intersected with the theorem's probability-one event, gives one entire FHC f with eventual two-sided bounds (n+1)^(-3/4)≤|a_n|≤log(n+e), a_n=f^(n)(0). No polynomial is involved in choosing this event.

For any p(z)=sum_(j=0)^d c_j z^j, d≥1, c_d≠0, and sufficiently large n,

(pf)^(n)(0)=sum_(j=0)^d c_j (n)_j a_(n-j),
|(pf)^(n)(0)|≥|c_d|(n)_d (n-d+1)^(-3/4) - C_p n^(d-1) log(n+e).

The first term has order n^(d-3/4); the second divided by it tends to zero, since log(n)/n^(1/4)→0. The lower bound therefore tends to infinity, even d=1. This is deterministic on the one coefficient event and holds for every polynomial chosen afterward. There is no uncountable intersection of probability-one events and no threshold uniform in p. The scalar derivative sequence cannot be dense: its tail escapes and its finite prefix misses some small disk. Hence every nonconstant pf fails HC(D).

Pick one such f. For any polynomial P, f+P is still FHC (all sufficiently high derivatives agree with those of f), and all sufficiently high jets agree too. Thus all p(f+P) have the same escape property. The set {f+P:P polynomial} is dense in H(C), by density of polynomials. This gives a dense family of simultaneous counterexamples without any Gaussian full-support argument beyond that used in the older theorem.

## Exact square-root annuli also follow after clipping

Let ell_n=(n+1)^(-1/2), u_n=log(n+e). Fix M≥0 and leave n<M Gaussian jets unchanged; for n≥M radially project X_n to the closed annulus ell_n≤|b_n|≤u_n (assign the positive boundary point at zero). Only finitely many upper violations occur almost surely. Every lower correction has size≤ell_n, so c_n=b_n-X_n→0 and is bounded. The series h=sum c_n z^n/n! is entire and

||D^n h||_R≤e^R sup_(k≥n)|c_k|→0.

Adding such a null-orbit perturbation preserves FHC: visit an inner compact-open ball of half the target radius with positive lower density, then remove the finite prefix before the perturbation is smaller than half the radius. Thus the clipped series lies in X_M and remains FHC almost surely.

The clipped law has full support in X_M: each unaltered low coordinate has full C support, each clipped high coordinate has full support in its closed annulus, and independence gives positive mass to each finite-coordinate relative neighborhood. Uniform deterministic factorial tails after M make the product topology equivalent to compact-open topology on X_M. Hence the probability-one FHC set is dense in each X_M. This checks that exact annular HC existence/density also follows from the older theorem plus elementary clipping, rather than claiming the radial change supplies a novel existence theorem.

Unclipped Gaussian jets do NOT eventually satisfy the ell_n lower bound: the independent probabilities 1-exp(-1/(n+1)) have divergent sum; second Borel–Cantelli gives infinitely many failures. This is why clipping is explicit. Finite-prefix upper clipping is harmless for null-orbit preservation.

## Attribution consequence

The older theorem supplies a stronger frequent-hypercyclic version of the simultaneous-counterexample conclusion by a short checked corollary. The current elementary relative-Baire proof is a self-contained alternative mechanism. Neither the basic negative answer, simultaneous existence/density, nor exact-annular existence should be advertised as a new open-problem resolution or first existence theorem. No read source was shown explicitly to state the multiplier corollary; first explicit recognition and earliest possible prior underpinning remain unestablished. The finer original fixed-p null-orbit construction near each prescribed HC starting f is a different mechanism, not supplied solely by random existence; its novelty is also not claimed.
