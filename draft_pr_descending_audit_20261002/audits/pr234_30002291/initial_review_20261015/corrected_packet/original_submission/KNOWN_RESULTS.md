# Known results and what the candidate does not claim

The 2013 OWR question is open-ended about sufficient hypotheses. Its displayed result is at each fixed t, with 0<alpha<1/2 and quadratic increments. It does not ask for arbitrary semimartingales without conditions, or assert a particular functional topology.

The complete primary texts checked here include:

- Basse-O'Connor–Lachièze-Rey–Podolskij, Annals of Probability45(6B),4477–4528 (2017), arXiv1506.06679
- Basse-O'Connor–Heinrich–Podolskij, Bernoulli24(4A),3117–3146 (2018), DOI10.3150/17-BEJ956, arXiv1604.02307v2

The second paper's Theorem1.2(i) is already a nontrivial semimartingale-driver extension. Its driver is dY=sigma_-dL, with L symmetric pure-jump Lévy relative to the filtration and sigma adapted càdlàg; independence is not required. Under its (A),(B1), beta<2, p>beta and alpha<k-1/p, it proves functional stable M1 convergence. At p=2,k=1, its sum over l>=0 of h1(l+U)^2 matches the OWR sum over l>=1 of h1(l-U)^2 after replacing U by1-U. Its factor |Delta L_T sigma_(T-)|² is exactly the squared jump of the semimartingale driver. The paper explicitly says J1 and J2 convergence fail in this regime. The candidate does not rediscover that result or claim a new truncation method.

The candidate's explicit driver class instead permits any predictable compensator kernel nu_s(dz)ds with a uniformly bounded quadratic rate, and bounded predictable drift, on the real-line prehistory. The jump kernel need not be a scalar dilation of one fixed Lévy measure, and symmetry or stationarity is not required. The proof relies only on the martingale isometry, bounded truncated intensity, absolute continuity of finite jump-time vectors, and deterministic kernel bounds.

Examples include sums of independent pure-jump Lévy noises with bounded predictable coefficients whose Lévy measures differ. Their compensator is a random mixture of push-forward measures and need not fit a single scalar volatility representation. The bounded-rate class also includes a symmetric Lévy measure with density 1/(|z|³ log²(1/|z|)) on 0<|z|<exp(-1): its quadratic rate is finite, while its Blumenthal–Getoor index is2. No new theorem is claimed for the full class of all pure-jump semimartingales.

A deterministic jump-time example shows that a missing time-density hypothesis cannot simply be ignored. It is a limitation outside the candidate's assumptions, not a refutation of the original request for sufficient conditions.

Publication should present the result as an explicit sufficient-conditions theorem, with its class stated in full and known results credited. Independent review must decide whether that is a complete answer to the source's open-ended target or should be catalogued as a scoped partial. No novelty determination follows from the limited current-source search.
