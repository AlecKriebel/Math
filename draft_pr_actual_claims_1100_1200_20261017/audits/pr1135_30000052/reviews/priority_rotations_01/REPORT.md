# Focused adversarial priority review: random rotation orbits

**PR #1135 / problem 30000052 / OWR-723-005**  
**Frozen head:** e809a9c40f4ccdaced6f45f10b1dc8b7725a2119  
**Review completed:** 2026-10-17 UTC  
**Verdict:** No documented preexisting full solution for the exact averaged anchored discrepancy law was located in this focused literature family. A complete additional Fourier proof was independently derived during this audit. That new deduction does not, by its use of classical ingredients alone, establish that the problem was previously solved.

The review concerns historical implications, not a new whole-package review. It neither authorizes nor performs a PR mutation, publication, or tracker write. All frozen input files were hashed before work and rechecked by the independent program.

## 1. Exact target and disqualifying substitutions

Novak's question, reporting joint work with Hinrichs, is printed on p.698 of Oberwolfach Report 13/2004. The definition on p.697 is the normalized anchored Lp discrepancy. It asks whether the expectation of its **p-th power**, for even p, is no larger for

    t_j = {j Z + Delta},  j=0,...,n-1,

than for n independent uniforms. Z and Delta are independent continuous uniforms, and points are counted by index with weight 1/n. The official source was freshly retrieved, read and visually checked.

A previous negative answer for d=1,p=4 and any n suffices. Therefore an earlier exact-law theorem giving a positive-constant/n lower bound for the fourth expected discrepancy moment would already settle the full universal question negatively; the candidate's sharp n=3 value is not necessary for that historical gate. Conversely, a result for a good fixed generator, an almost-everywhere bound, a rational-generator ensemble, an unshifted sequence with no checked shift bridge, a supremum instead of integrated discrepancy, or an expected norm rather than its fourth power is insufficient without a proved implication.

## 2. Strongest verified result of this audit

The full proof is in [FOURIER_IMPLICATION.md](FOURIER_IMPLICATION.md). It is a new audit argument, independent of the candidate's triple-inclusion and empty-tail proofs.

For F(x)=n^{-1}sum_j 1_{t_j<x}-x and e(x)=exp(2 pi i x), ordinary integration of each indicator gives

    integral_0^1 F(x)e(x) dx = -(1/(2 pi i n)) sum_j e(t_j).

This identity handles endpoints directly, with no ambiguous Stieltjes convention. Hölder then gives

    disc_4(t)^4 >= |sum_j e(t_j)|^4 / ((2 pi)^4 n^4).

For the exact sampling law, the sum is e(Delta)D_n(Z), where D_n(Z)=sum_{j=0}^{n-1}e(jZ). Thus the common phase disappears pointwise, and continuous averaging over Z is exactly integration of the fourth Dirichlet-kernel moment. Orthogonality, or equivalently the ordered count a+b=c+d, yields

    integral_0^1 |D_n(z)|^4 dz = (2n^3+n)/3.

Consequently

    E_{Z,Delta} disc_4^4 >= (2n^2+1)/(48 pi^4 n^3).

The iid fourth moment is (3n-1)/(30n^3). The lower bound is strictly larger for every n>=234. The least threshold for **this lower bound** is 234, certified using only the rational bounds 223/71<pi<22/7. The polynomial comparison is positive at234 even with the upper pi bound, negative at233 even with the lower bound, and increasing thereafter. It does not prove the candidate's n=3 counterexample and is not claimed to be a sharp threshold for actual reversal.

The older printed ingredients are precise:

* Su, *A LeVeque-type lower bound for discrepancy*, Springer 2000, Lemma 4 (p.450) and its proof (p.451), gives the nonzero Fourier coefficient identity for cumulative discrepancy. Su adds a centering constant; it vanishes from nonzero coefficients. The displayed identity is applicable after recovering the uncentered anchored discrepancy. His main lower-bound theorem concerns a supremum discrepancy and is not being substituted for the L4 norm.
* Anderson, Ash, Jones, Rider and Saffari, *Exponential sums with coefficients 0 or 1 and concentrated Lp norms*, Annales de l'Institut Fourier 57(2007),1377--1404, definition (1.1) and Lemma 2.1, pp.1383--1385, proves the exact-convention general moment asymptotic integral|D_n|^p=delta_p n^(p-1)+o(n^(p-1)), with delta_p>0 for p>1. The complete proof of that lemma was read and its pages visually checked. It alone gives the order 1/n lower bound after the new discrepancy application; the exact finite count strengthens the corollary.

These source claims are generic identities and kernel estimates. The source texts inspected here do **not** state that the Novak comparator fails, do not state the anchored random-lattice fourth moment lower bound, and do not combine the selected coefficient, phase cancellation, uniform-slope integration and iid comparison. No evidence was found that this combination was previously recorded. It is therefore appropriate to credit the classical ingredients and label the present application a new audit deduction, while withholding an exhaustive novelty assertion. The root reviewer retains the final historical classification decision.

## 3. Independent reproduction and adverse controls

`verify_fourier_bridge.py` is a new standard-library program, importing none of the candidate's verifiers. It checks:

* Ordered additive quadruple counts, the triangular pair-sum formula, and integrality for every n=1,...,256.
* Independent Laurent-polynomial constant-term expansions for n<=48 and explicit four-index slope/shift Fourier modes for n<=17.
* The indicator Fourier primitive as formal coefficients, including endpoint representatives, for multiple finite point configurations.
* The iid formula by integrating the full Binomial(n,x) law with exact beta integrals for n<=96; it does not use a fourth-moment oracle.
* The rational pi threshold, all smaller positive integers, and the derivative bound for every larger real n.
* Seven adverse controls reject treating the lattice phases as iid, omitting slope averaging, using an iid phasor moment, replacing continuous slopes by a discrete rational ensemble, misusing this coarse bound at n=3, extending it to refute p=2 equality, or dropping normalization.

Both normal and optimized Python runs passed **1558 explicit requirements** and **7 adverse controls**, with byte-identical result files. Deliberate failure guards exited unsuccessfully in both modes. These finite checks supplement the universal proof; they do not numerically certify Hölder, replace the literature reading, or prove exhaustive priority.

## 4. Other older rotation literature and precise exclusions

The source-level coverage is detailed in [SOURCE_INSPECTION.md](SOURCE_INSPECTION.md), with actual retrieval receipts and a ledger of 51 searches. Many broad searches returned irrelevant material, which was rejected; the count is not a claim of 51 useful theorems or exhaustive indexing.

Kesten's 1964 primary article studies supremum discrepancy and gives convergence in measure at the logN loglogN/N scale. Its scan was retrieved, OCRed, and the introductory definitions/main Theorem 2 and concluding Theorem 3 were inspected. No source-compatible fourth integrated-moment conclusion follows from those statements alone. No claim is made to recertify every proof in this 31-page article.

Dolgopyat and Fayad's primary arXiv 1211.4323v3 and journal metadata identify Cauchy limit theorems for random toral translations. The slope and shift law is relevant, but a weak limit at the logN scale gives no lower bound of order n^3 for the unnormalized fourth moment. Its higher-dimensional theorem also randomizes box parameters. The original statements and relevant resonance-removal context were inspected; the full long proof was not recertified. The absence of fourth-moment control is a logical limitation of the cited statements, not a claim that an unknown theorem cannot exist elsewhere.

Sugita's 2016 open primary article was read at its sampling definitions, pairwise-independence and variance proofs, and continuous Theorem 7. The latter explicitly allows only 1<=p<2 and establishes degeneration of CLT-scaled averages. Its discrete theorems do not silently become a continuous fourth-moment statement. Their variance equality agrees with the p=2 consistency check and does not refute the target.

Cesaratto--Vallée 2012, Sugita--Takanobu 2000 and Janson 1988 remain bounded-access gaps. Publisher abstracts/metadata were read, but their full bodies were not available in this pass. The first includes continued-fraction-dependent truncation issues; the second concerns the exact continuous random Weyl law and variance robustness; the third proves examples of CLT failure. None may be declared a full-text exclusion or an exact-law fourth-moment solution from titles or abstracts alone. No outreach was prepared or initiated.

The 2013 Koksma--Hlawka working paper inspected supplies broad translated geometric discrepancy inequalities, not an already identified exact-law comparator. Its methods are background rather than evidence of an older resolution.

## 5. Later overlapping preprint and chronology

The EulerSolve primary landing page for Alper Ferudun's note records manuscript and online dates 14October2026, labels it an unrefereed preprint, and states the same n=3,d=1,p=4 values plus broader results. This overlaps the candidate but is later than the frozen source proof's 10October2026 date. It must not be called an older result relative to that source proof merely because it is already public when this audit is performed. Root and another assigned reviewer are checking the full paper and chronology; this focused report independently verifies only the landing-page claims and dating, not its proof or provenance.

## 6. Conclusion and limits

**No older documented full solution was located in this family.** The strongest outcome is a fully verified new Fourier application of classical formulas giving another negative resolution for n>=234, together with explicit primary-source attribution. This is mathematical evidence that the candidate's conclusion is consistent with classical harmonic analysis, not proof that the original question had already been answered. Neither the literature audit nor the finite verification establishes exhaustive novelty, formal proof-assistant certification, journal acceptance, or human peer review.

No candidate inputs, PR, comments, branches, git index/refs, publications, or sheet rows were changed. Third-party bodies remain ignored. Completion estimate for this assigned focused audit: 100%; the root program and any preprint preparation remain separate.
