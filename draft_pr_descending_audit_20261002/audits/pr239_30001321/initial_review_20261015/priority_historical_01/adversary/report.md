# Independent adversarial audit: early dynamic/time-space sources

Authoring checkpoint: 2026-10-15 04:35 UTC. This report was developed independently of new parent-lane reports. Only parent messages giving scope/source-retrieval status were read. No other new priority report was read. No outreach or Git/provider mutations were performed.

## Claim tested and present verdict

Let the environment consist of iid transition parameters p(t,x) with a fixed law supported on (0,1), and let the transverse walker move by ±1. For a deterministic partition into consecutive intervals of width M_N, write

D_N(M_N,ω) = Σ_I |P_ω(X_N∈I) − P(X_N∈I)|.

The audited target is: for every deterministic M_N→∞, however slowly, and every fixed ε>0, the environment probability P(D_N>ε) is smaller than every inverse power of N. Variants with polynomially many starting points need an additional uniformity quantifier; they do not follow automatically from a single-start statement.

**Verified finding:** the primary full sources inspected below establish full-law invariant-density or weak quenched limit results, and some quantitative smooth-test estimates. I have not authenticated a theorem in these sources that gives this whole target. There is an exact missing implication involving the coarse L1 norm, arbitrary width, and environment tail quantifier. This is a bounded source audit, not a novelty or priority claim. In particular, BMP1999 and Conlon–Song1999 remain full-source gaps.

## Authenticated primary full sources

1. **Bolthausen–Sznitman (2002),** *On the static and dynamic points of view for certain random walks in random environment*, Methods Appl. Anal. 9(3), 345–376, DOI 10.4310/MAA.2002.v9.n3.a4. Publisher PDF: https://www.intlpress.com/api/bgcloud-front/resource/pdf/volume/1806623584179167237-1806623584179167237-6ac853c8711bd0149b0a8c1cef32ba0d.pdf . SHA256 `b45824712f99076e2d1282b2660cc3fca6ac574ad4f82934ba83a1b2a74454ca`, 323691 bytes, 32 pages. A distinct publisher download variant (same article) has SHA256 `b4442384d2e76e123c6ddf885b2d5038bbd08d84ae6cf2797fca852dc542eb92`, 307904 bytes. Author preprint: https://www.math.uzh.ch/d.php/publication/2 , SHA256 `3fae0ed87620129400826f500e8e903ca79fb0a19239b5ee2b854b1b580e5a14`, 341098 bytes, 36 pages. Use published numbering below, not preprint numbering. The preprint has broken text encoding; its OCR is private and is not the controlling transcription.
2. **Boldrighini–Minlos–Pellegrinotti (2004),** *Random walks in quenched i.i.d. space-time random environment are always a.s. diffusive*, PTRF129, 133–156, DOI10.1007/s00440-003-0331-x. https://link.springer.com/content/pdf/10.1007/s00440-003-0331-x.pdf . SHA256 `f8bd982c1965d69d589b1b236363450062a80e6ceb6a9fb60a5f52ec7338ea49`, 222535 bytes, 24 pages.
3. **Boldrighini–Minlos–Pellegrinotti (1997),** *Almost-sure central limit theorem for a Markov model of random walk in dynamical random environment*, PTRF109, 245–273, DOI10.1007/s004400050132. https://link.springer.com/content/pdf/10.1007/s004400050132.pdf . SHA256 `004c21460a56c19aa6ef8c81709c2f4742dd2e62e70a11ee7db0d469615c2415`, 438855 bytes, 29 pages.
4. **Rassoul-Agha–Seppäläinen (2005),** *An almost sure invariance principle for random walks in a space-time random environment*, DOI10.1007/s00440-004-0424-1. Author full PDF https://people.math.wisc.edu/~tseppalainen/papers/qclt-sp-time.pdf , SHA256 `dd98c68b959ee71b05590d2f6bbdc962f83af7d398b95d3517c44f897a432cc8`, 196739 bytes. Used as an independent check on the scope of the older CLT results, not as an all-scale local theorem.

Whole third-party PDFs, their full text/OCR, and rendered pages are private reading material. They are excluded from the public authored manifest. Exact source URLs and hashes are metadata, not uploaded copies.

## BS2002: what genuinely transfers

The paper's “dynamic point of view” is the environment seen from the walker. Its directed section nevertheless contains an iid time-space model. The precise encoding for a nearest-neighbor transverse path S_n is

(u_n,v_n)=((n+S_n)/2,(n−S_n)/2).

A +1 transverse step becomes e_1; a −1 step becomes e_2. Parity is built into this bijection, and iid parameters on the visited parity class extend to iid parameters on all of Z². Thus the relevant BS dimension is d=2, not d=1. The condition 0<p<1 almost surely is exactly positivity of both forward directions, with no deterministic uniform lower bound required.

The exact chain of locators is: directed setup (0.3), p346; reverse density g_N=Σ_x p_N(x,0,ω), (1.34), and its martingale law Proposition1.4, (1.36)–(1.38), p353; positivity (3.1) and Theorem3.1, (3.2)–(3.3), **p363/PDF19**; equivalent invariant law and ergodicity in Remark3.2(2), p365. The theorem gives sup_N E[g_N²]<∞ and Q≪P; martingale convergence gives an L2 limiting density. This is substantial full-law prior structure. It does not state an endpoint local approximation, an interval-width error, or a finite-N environment tail bound.

The neighborhood exposure proof is in Theorem4.2, pp368–371. It concerns bounded fixed Lipschitz path tests and uses (4.18)–(4.20) to enumerate an initial ball first. Its small-disorder, uniformly elliptic, nonnestling static setting has d≥4. The estimates (4.28), (4.31)–(4.35) give a polynomially decaying variance, sufficient for Lemma4.1's summability along geometric scales. Remark4.3 on **p371/PDF27** says the method also applies in the positive directed case when d≥4. It does not assert this proof in directed d=2. Removing the initial neighborhood and counting late intersections would fail without a new estimate when the transverse difference walk is recurrent. Neither its stated test class nor its tail calculation supplies the audited target.

## BMP2004: full-law weak limit, quantitative second moments

On pp134–135, assumptions I–IV require valid transition probabilities, a completely irreducible averaged walk, zero-mean random perturbations, and exponential spatial decay uniform in the environmental state. The additional condition (1.3) is

∫_{T^ν} E|p̃_0(λ)+c̃(λ;ξ)|² dλ/(2π)^ν < 1.

For ±1 steps the integral equals E[p²+(1−p)²]=1−2E[p(1−p)]<1 for every law supported on (0,1). No small-noise condition is present. A bare ±1 averaged walk is periodic; that boundary must be tracked rather than silently applying any aperiodicity convention in “completely irreducible.” The change Y_n=(S_n+n)/2 has 0/1 steps and averaged characteristic function (1−m)+m exp(iλ), whose modulus is strictly below one away from λ=0. This removes the Fourier period obstruction. A completely unambiguous full-law weak theorem with no such terminology issue is Rassoul-Agha–Seppäläinen2005 Theorem1: deterministic unit time coordinate, finite annealed second moment, and positive probability of a genuinely nondeterministic transition suffice; all hold here.

BMP2004's unnumbered theorem on p135/PDF3 is convergence in distribution for the diffusively scaled position, for almost every environment. It does not state a strong local norm. Its quantitative core is Lemma2.1, p136, (2.2a), and the p137 bound (2.3b). Combined with (2.4b)–(2.4c), cancellation of Σ_u c(u;s)=0 gives for a fixed bounded C1 test f

E|μ_N^ω(f)−μ_N^0(f)|² ≤ C||∇f||_∞² × {N^{-1/2} (ν=1), N^{-1}log N (ν=2), N^{-1} (ν≥3)}.

This displayed inequality is a deduction from their formulas, not a separately stated theorem. In ν=1, Chebyshev supplies O(ε^{-2}N^{-1/2}) for this fixed smooth test, rather than every polynomial exponent. Proposition2.2, p138, controls differences between times for C2 tests; AppendixB turns these controls into almost-sure convergence. It does not change the finite-time tail quantifier to superpolynomial.

## BMP1997: moment order changes the allowed noise

Theorem1, p248, assumes transverse ν≥2, finite environmental state space, finite jump range, Fourier aperiodicity (1.2a), nondegenerate covariance, and sufficiently small perturbation ε. Proposition2.2, p251/PDF7, gives for each integer n≥1, when ε is sufficiently small depending on n,

E|μ_T^ω(f)−μ_T^0(f)|^{2n} ≤ C||f||_1^{2n} T^{-n}(log T)^{2n−1}  (ν=2),

and the same without the logarithm when ν≥3. These are stronger-than-L2 estimates, but **∀n ∃ε_n** is not **one arbitrary fixed law ∀n**. They also concern fixed C1 tests and exclude ν=1 in this paper. Thus neither a high-moment tail upgrade for one unrestricted law nor arbitrary-width coarse L1 follows directly from this proposition.

## BMP1999 and Conlon–Song1999: bounded unresolved-source status

BMP1999 is *Central limit theorem for a random walk in dynamical environment: integral and local*, Theory Stoch. Process.5(21)(3–4),16–28. Sapienza's primary institutional record https://iris.uniroma1.it/handle/11573/28307 identifies small stochasticity and a final-point environmental prefactor; it explicitly has no attached source. The official TSP archive at https://tsp.imath.kiev.ua/published/index.html starts at volume11 in the returned listing. RomaTre https://iris.uniroma3.it/handle/11590/116583 returned403. OpenAlex identifies these locations but no PDF. No full BMP1999 was authenticated.

The authors' own2007 survey DOI10.1070/RM2007v062n04ABEH004428, §1.4.3, p680, is indexed at https://www.mathnet.ru/php/getFT.phtml?jrnid=rm&option_lang=eng&paperid=6849&what=fullteng . Its indexed page attributes a local theorem to BMP1999, with Gaussian times a mean-one quasi-local final-point functional Φ. It gives qualitative quasi-locality (1.4.7), not a quantitative environment tail in the inspected excerpt. Full download attempts timed out; IOP returned HTML, not a PDF. The excerpt's first normalized-coordinate range and later unnormalized-coordinate range differ, so no numerical range is promoted here. Dunlap–Gu2022 discusses a restricted range for the1999 theorem, but that secondary-to-this-claim interpretation cannot replace the missing original. Both the original and a visual check of the2007 page remain outstanding.

Conlon–Song1999 is a direct BS2002 citation [5], *Gaussian limit theorems for diffusion processes and an application*, SPA81(1),103–128, DOI10.1016/S0304-4149(98)00095-7. Official abstract: https://www.sciencedirect.com/science/article/pii/S0304414998000957 . ScienceDirect PDF returned403; author Song's publication list contains the citation without a PDF; the checked Conlon historical author root returned404. Thus its exact application hypotheses and probability estimate have not been authenticated. Record this gap; do not infer from it that no stronger theorem exists.

## Checkable implication tests and exact remaining work

1. A weak CLT is logically insufficient even before probability tails are considered. For a concrete continuous example let φ be standard Gaussian density and let f_N(x)=φ(x)[1+a sin(k_Nx)], 0<a<1. The sine integral is zero, so these are probability densities. If k_N→∞, f_N dx converges weakly to φ dx by oscillatory integration. Partition into normalized cells of width h_N=M_N/√N with h_N→0 and choose k_N→∞ with k_Nh_N→0. The coarse L1 discrepancy tends to a∫φ|sin(k_Nx)|dx→2a/π, not zero. The piecewise-sum-to-integral error is bounded by h_N||(φ sin(k_N·))'||_1=O(h_Nk_N). This is an explicit logical counterexample, **not** a counterexample in iid RWRE.
2. Approximating an M_N-sized indicator on diffusion scale uses test derivatives of order √N/M_N. Thus the fixed-test second-moment estimate does not stay uniform for arbitrary slow M_N. Furthermore coarse L1 is the supremum over all sign assignments to cells; a separate bound for each fixed test does not control that supremum without entropy or direct norm estimates.
3. A local formula with a mean-one stationary prefactor still needs spatial averaging over M_N, approximation uniform over the relevant endpoint region, treatment of its remainder in the summed norm, and concentration after aggregation. Qualitative quasi-locality or ergodicity alone supplies no superpolynomial N-tail rate.
4. The route “cite a weak CLT or L2 invariant density, therefore obtain all-scale superpolynomial coarse L1” is **blocked as an argument**: it substitutes the unproved local-norm/tail assertion for its central step. Reopen only with a quantitatively uniform local/smoothing estimate plus an explicit tail derivation. This does not mark the mathematical target false.

Strongest presently verified result for the exact full-law nearest-neighbor model: BS's directed L2 invariant density, plus a.s. weak functional diffusion from Rassoul-Agha–Seppäläinen2005. Strongest authenticated quantitative early estimates: polynomial fixed-smooth-test second moments in BMP2004; high moments only at moment-dependent small noise in BMP1997. Exact remaining priority gap: original BMP1999 and Conlon–Song1999 source authentication, and any actual derivation bridging their claims (if stronger) to the target's three independent quantifiers.

## Post-independence adversarial check of parent coarsening deduction

At **2026-10-15 04:36:08 UTC**, after the initial independent report above was saved, the parent explicitly requested review of its authored `IMPLICATION_AUDIT.md` sectionA. This is the first new parent-lane report read. The following is agreement with that specific check, not a source-result substitution.

If a deterministic fine partition P_m has, for each fixed m, a coarse L1 bound A m^{-a}+A N^{-a} with superpolynomial exceptional probability, where A,a do not grow with m, then it *does* imply every diverging deterministic target width. Let B_N be the union of fine cells split by target boundaries. For a split fine cell J, with A_J=μ(J), B_J=α(J), the discrepancy after splitting is ≤A_J+B_J≤|A_J−B_J|+2B_J. Summing and using the triangle inequality gives exactly

L_target(μ,α) ≤ L_fine(μ,α)+2α(B_N).

For α with maximal mass O(N^{-d/2}) and diffusive tightness, boundary strips have α-mass O_{m,R}(1/M_N+1/√N)+η uniformly in deterministic alignment. Alternatively an L1 approximation to a parity-adjusted Gaussian gives this strip-mass estimate with a deterministic o(1) error. Fix ε first, then m large enough that A m^{-a} is small, then take N large along the specified M_N. Tail constants and thresholds may depend on this fixed m. No union over widths, no m depending on N, and no rate of M_N growth are required.

I find **no hidden partition or uniformity gap in this deduction for regular equal cubes/intervals**. It proves the target-shaped statement in any source model that supplies those premises, including the parent's BBDS percolation-model example if its source hypotheses are as authenticated by the parent. I have not independently read/authenticated BBDS in this subtask and do not certify its source premises here. The missing BS implication is more precise: directed L2 alone does not provide the fixed-m superpolynomial coarse event required to start the deduction. A direct large-m event could close the slow-scale issue without needing a local theorem uniform in m(N).
