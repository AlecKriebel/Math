# Exact source scope: Bandeira's OSNAP part(3)

This packet concerns only the independent sparse-sign coordinate-subspace model in part(3) of Open Problem4.4. It does not concern arbitrary deterministic subspaces or conditioning each column on exactly s nonzeros.

## Primary statement

The [2015 author blog](https://afonsobandeira.wordpress.com/2015/10/25/10l42concentration/) gives the part(3) model explicitly. The full [2016 author notes](https://people.math.ethz.ch/~abandeira/TenLecturesFortyTwoProblems.pdf), pp.76–77 (same PDF page numbers), distinguish all three parts. Both complete pages were read and visually checked. The original MIT lecture-note link is dead; the author's ETH-hosted full notes were retrieved. Direct UnsolvedMath access failed, so the pinned imported entry was checked against these primary sources.

The model has independent rows z_k∈R^d and independent coordinates0,±1/√s with probabilities1−s/m,s/(2m),s/(2m). It asks for universal constants at dimension m≥c_1(d+log(1/δ))/ε² and expected column sparsity s≥c_2log(d/δ)/ε², with s≤d≤m. Its covariance is exactly I_d/m. KNOWN_RESULT.md proves that bound from published Wishart moment lemmas, preserving both logarithmic arguments and the strict probability inequality.

## Range conventions must be visible

The full problem treats s as a sparsity parameter, and part(2) says explicitly that each column has exactly s nonzero entries. That is the ordinary positive-integer sparsity convention. Our corollary is stated for the slightly larger range of **real1≤s≤d**, positive integer d,m, and the standard subspace-distortion/failure ranges **0<ε,δ<1**. The brief blog display does not explicitly print all these ranges. We do not claim an unrestricted theorem for arbitrary positive s or arbitrary ε.

If the isolated display were read as permitting0<s<1, even its d=1 form could fail: take ε=1/2 and s=1/4. The scalar normalized Gram is4N with N integer, so |4N−1|≥1 deterministically. For any proposed positive c_1,c_2, choose δ=exp(−1/(32c_2)); then s≥c_2log(1/δ)/ε², and m can be chosen arbitrarily large to satisfy the dimension bound. Failure probability is1>δ. This demonstrates the need to state the standard lower sparsity convention; it is not presented as a counterexample to the intended OSNAP question. Distortion parameters above1 likewise are outside the standard embedding regime and outside our claim.

The full notes' part(1) display has an apparent extra normalization in the auxiliary δ_{ri}, and part(2)'s displayed condition inherits it; its explanatory sentence says exactly s nonzeros. We use the unambiguous part(3) law itself, which agrees between the blog and the notes, rather than propagating that unrelated auxiliary normalization issue.

## Literature comparison and credit

1. Cai–Han–Zhang, EJP27(2022), paper29, DOI10.1214/22-EJP758, **Lemma5.4 and Lemma2.6**, give the bounded-entry trace comparison and the Gaussian Wishart moment bound needed directly for this special coordinate model. Their published statements and relevant complete proof sections were read. Lemma5.4's proof invokes symmetric entry distributions; our law is symmetric. Its Gaussian comparison uses rounded variance sums, not the much larger general sub-Gaussian parameter of a sparse sign.
2. Chenakkod–Dereziński–Dong, ICALP2025 / arXiv:2411.08773v2, Section9 Definition9.1 and Theorem9.2, treat the iid-entry distribution for arbitrary U. Their displayed sparsity bound includes log²(d/(εδ))/ε, log(d/(εδ))/ε² and log³(d/(εδ)) terms. The arbitrary-U result is broader but is not a verbatim proof of the exact special-case scales. The standard OSNAP construction elsewhere in that paper fixes the number of nonzeros per column and is a different law.
3. Chenakkod–Dereziński–Dong, SODA2026 / arXiv:2508.14234v2, gives nearly optimal general OSNAP tradeoffs up to sub-polylogarithmic factors. Its abstract, main theorem scope and model definitions were inspected. Its stronger algorithmic context does not replace the exact iid-coordinate law here.
4. Dumitriu–Zhu, Bernoulli30(4)(2024),2904–2931 / arXiv:2209.12271, gives sparse rectangular extreme-singular-value bounds with additional aspect-ratio/sparsity restrictions and different error expressions. The main result scopes were inspected; they are not the basis of our exact corollary.

The old imported research note describes the remaining gap as merely unspecified sharp constants while invoking polylogarithmic-factor results and a different embedding model. That is not a valid source match by itself. The present proof uses the exact bounded-Wishart lemmas and supplies conservative constants; no sharpness or first-priority claim is made.

## Prior-attempt gate

All-state PR/commit searches by ID2800404, aliasAMR-027-0404, OSNAP and sparse-embedding terms; both conventional target paths;360 live branch names; and411 locally mirrored refs found no matching attempt. The dataset's random-scattering restricted-isometry record30002097 is distinct. These finite checks are recorded in PRIOR_GATE.json and do not certify inaccessible/deleted history.

Source retrieval, known-lemma specialization and scope verification use **zero substantive author turns**. The proposed disposition is a credited source-qualified known result, subject to independent review. No raw imported records or primary PDFs belong in the public packet.
