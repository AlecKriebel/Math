# Independent proof audit: Nicolau's first 2010 question

This is a checkable audit derivation, not a new research publication. The target is the first question on printed p.2872/PDF p.60 of EMS46308, DOI10.4171/OWR/2010/49. It asks whether, for every real locally integrable function F, the limsup of |F_In(x)-F(x)| divided by sqrt(Q_n(x) |log|log Q_n(x)||) is finite almost everywhere on R, with Q_n=sum over k>=n of (F_I(k+1)-F_Ik)^2. It does not assume a within-atom regularity bound for Q_n. A failure on any positive-measure subset disproves it. The second question, about arbitrary lacunary dilates of a smooth periodic function, is separate.

## Parameters and deterministic budgets

For fixed integer k>=1 and 0<a<exp(-e), write ell=log log(1/a^2), m=ceil(64 k^2 ell), L=ceil(2^m (k+2)log 2), and b=L a^2. Put t=log(1/a^2). Since 2^m<=2 t^(64 k^2 log 2),

    b <= exp(-t) [2(k+2)log 2 t^(64 k^2 log 2)+1] -> 0.

The limit holds for each fixed k; uniformity in k is unnecessary. Thus one can inductively select strictly positive a_k so that b_k<=2^-k min(1,a_1^2,...,a_(k-1)^2). Each minimum is positive. It follows that sum b_k<=1, a_k^2<=2^-k, and

    B_k := sum_(j>k) b_j <= a_k^2 sum_(j>k)2^-j = 2^-k a_k^2.

The deterministic stage endpoint M_k=sum_(i<=k)m_i L_i tends to infinity. The deterministic coefficient-square sequence, taking every potential increment as active, has finite sum sum b_k; therefore its tail tends to zero even when the index falls inside a stage. No size bound on the astronomically large finite block lengths is required for an existence proof.

## Predictability and stopping

On [0,1), use independent fair binary signs r_j and their dyadic filtration F_n. Take the usual half-open intervals; dyadic endpoint expansion conventions affect a null set. Stage k has L_k potential blocks of length m_k. For a block starting at s, let H be the event all its m_k signs are positive. Activate block h exactly when all earlier potential blocks in the same stage failed. Its activation A is measurable in F_s, because those whole blocks have already finished. Use every increment of an active whole block,

    d_(s+v) = a_k A r_(s+v) / sqrt(m_k),  1<=v<=m_k.

A negative sign inside a block does not deactivate its later increments. An all-positive whole block deactivates subsequent blocks in that stage. The next stage always starts active. Consequently E[d_j | F_(j-1)]=0, all d_j are bounded, and f_n=sum_(j<=n)d_j is a dyadic martingale. Only the signs and disjoint potential-block success events are independent; the stopped increments need not be independent.

Every active whole block contributes precisely a_k^2 to the realized square function. All inactive increments are zero. Hence sum_j d_j^2 <= sum_k L_k a_k^2 <=1 on every binary path. This verifies both the active and inactive cases without replacing realized variation by predictable variation.

## Terminal function and exact dyadic averages

Martingale orthogonality gives E[d_i d_j]=0 for i<j. Tonelli and the pathwise bound give sum E d_j^2<=1. Thus f_n is Cauchy in L2 and has an L2 limit f with ||f||_2<=1. This step also rules out a non-uniformly-integrable abstract martingale unrelated to an integrable terminal function.

Here is a direct almost-sure argument, avoiding an unverified imported tail theorem. Fix deterministic N and m>N. For X_i=f_i-f_N let E_i be the disjoint event that i is the first crossing of |X_i|>lambda, N<i<=m. Since E_i is F_i-measurable and E[X_m-X_i | F_i]=0,

    E[X_m^2 1_Ei] = E[X_i^2 1_Ei] + E[(X_m-X_i)^2 1_Ei]
                  >= lambda^2 P(E_i).

Summing and then letting m increase yields

    P(sup_(i>=N)|f_i-f_N|>lambda) <= lambda^-2 sum_(j>N) E d_j^2.

Choose increasing deterministic N_l so that the last sum is <=2^-4l and take lambda=2^-l. The probabilities are summable. Borel-Cantelli I implies that for all sufficiently large l all i>=N_l satisfy |f_i-f_Nl|<=2^-l, so the sequence is Cauchy almost surely. Its a.s. limit agrees with the L2 limit by convergence in probability.

For fixed n, E[f_m | F_n]=f_n for all m>=n. L2 continuity of conditional expectation gives E[f | F_n]=f_n. Conditional expectation on a positive-measure dyadic atom is the interval mean of f. Taking the common full-measure set for these countably many statements identifies one terminal f with all its actual dyadic averages. The values of f on the exceptional null set may be assigned arbitrarily. Since f_n is constant on each atom, its atomwise mean identities are also exact.

## Eventual success and errors at deterministic times

Within stage k the disjoint potential-block events H_(k,h) have probability p_k=2^-m_k and are independent. Stage failure occurs exactly when none succeeds, regardless of whether later blocks would have been inactive following a success. Therefore

    P(stage failure)=(1-p_k)^L_k <=exp(-p_k L_k)<=2^-(k+2).

Borel-Cantelli I gives success at every sufficiently large stage a.s.; it requires no independence between stages. At the deterministic stage endpoint set R_k=f-f_Mk. Orthogonality and the deterministic future budget imply E R_k^2<=B_k<=2^-k a_k^2, and Chebyshev gives P(|R_k|>a_k)<=2^-k. Another application of Borel-Cantelli I gives |R_k|<=a_k eventually on a common full-measure set.

The successful block's starting index is generally NOT a stopping time. There is no optional-sampling or conditional estimate at that random index. All probability estimates above concern potential blocks or deterministic M_k. The finite diagnostic exhibits two paths with the same empty prefix but different values of the event that the first successful start is zero.

## Divergence using only pathwise identities

At the first successful block of a successful stage k, let n_k be its start. All its signs are positive and every later same-stage increment vanishes. Thus, pathwise,

    f-f_nk = a_k sqrt(m_k)+R_k,
    a_k^2 <= Q_nk = a_k^2 + sum_(j>M_k)d_j^2 <= a_k^2+B_k <=2a_k^2.

The n_k tend strictly increasingly to infinity across successful stages. For 0<q<exp(-e), the derivative of q log log(1/q) is log log(1/q)-1/log(1/q)>0. Also 2a_k^2<exp(-e) and ell_k>log(2e)>1. Hence

    Q_nk log log(1/Q_nk) <=2a_k^2 ell_k,
    |f-f_nk| >=a_k(sqrt(m_k)-1)>=a_k(8k sqrt(ell_k)-1).

The quotient is at least (8k-1)/sqrt(2), and therefore tends to infinity along those stages. These assertions hold on the intersection of the convergence, eventual-success, and eventual-small-error full-measure sets. For every finite n, some later stage has an always-active first block, so Q_n>0 on every path. Finite total square sum gives Q_n->0 for all paths. This includes indices in inactive runs and inside stages. The denominator is eventually positive on the full-measure set where f is identified.

## Matching the original real-line statement

Extend f by zero to F on R. Since [0,1) has measure one, ||f||_1<=||f||_2, so F is globally integrable and in particular locally integrable. For x in [0,1) and n>=0, its standard dyadic interval of length 2^-n lies entirely in [0,1); hence its F-mean is f_n. The original square sum over k>=n equals sum_(j>n)d_j^2 after j=k+1. For 0<Q_n<exp(-e), |log|log Q_n||=log log(1/Q_n). Thus the original quotient diverges on a set of measure one inside the unit interval. Its possible zero-over-zero values elsewhere are immaterial to the counterexample; no assertion about them is used.

## Why conditional and selected-time bounds do not remove the counterexample

At deterministic stage start M_(k-1), inside any atom I, the event that the first block succeeds and the event that every block fails both have strictly positive relative probability. On the first, Q<=a_k^2+B_k; on the second Q>=L_k a_k^2. The corresponding square-root tail ratios can be at least sqrt(L_k/(1+2^-k)), which tends to infinity. Both events retain positive measure after deleting any null set. Thus no uniform finite constant bounds S'_n(x)/S'_n(y) inside all generation-n atoms, even essentially. This is the explicit hypothesis of the positive Theorem29 in the dissertation (printed34/PDF43), the talk's PDF50, and Acharya-Ghimire2016 Theorem1. The latter's Theorem2 is stated only along specially chosen times. A subsequence upper bound does not bound a full limsup. This audit does not certify either external positive proof and imports neither.

## Priority and proof limits

Ghimire's 2011 talk PDF51-69 and 2012 dissertation Section3.3, printed50-59/PDF59-68, already use repeated blocks, stop after a positive large block, control future square tails, and obtain divergence with gamma_k->infinity. In the dissertation gamma_k=log k and alpha_k=exp(-e^k) occur on printed55, so the final conclusion on printed59 is for a single construction with unbounded gamma_k, not merely a family of examples violating different fixed constants. The final normalization uses S'_n sqrt(log log(1/(S'_n)^2)), with (S'_n)^2=Q_n.

The dissertation contains informal integer/initial-parameter notation (including log1) and an estimate displayed with a random successful endpoint. The latter equals the deterministic stage endpoint after the successful block by stopping. Its error bound can be justified using that deterministic endpoint. One may also replace its imported exponential bound by Chebyshev: once the future square budget is <=alpha_k^2/2, the probability of error exceeding .1 alpha_k log k sqrt(k) is <=50/[k(log k)^2], summable for k>=2. The finitely many initial parameters can be omitted or separately defined and trial counts rounded up, with slightly enlarged harmless budget constants or inductively smaller amplitudes. Also, the source passes from comparable square tails to an unchanged displayed constant .9; comparability alone loses a fixed factor. With Q<=1.5 alpha_k^2 the normalized lower bound is instead at least (.9/sqrt(1.5)+o(1)) gamma_k, still tending to infinity. This does not certify its literal .9 constant. These observations explain rather than silently adopt the source's compressed steps. The complete independent proof above uses the PR's simpler all-positive events and stronger inductive budgets; it needs no CLT tail constants, integer choices, or source exponential inequalities.

The finite exact diagnostics verify stopping, predictability, dyadic-average identities, squares, orthogonality, and failure probabilities in small models and reject deliberately invalid mechanisms. They do not execute infinite stages or the enormous analytic parameters. The written proof establishes those infinite assertions. No independent human peer review is asserted, and this AI-assisted audit is not an immutable mathematical publication.
