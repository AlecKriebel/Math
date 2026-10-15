# Primary source and priority mechanism check

This review reconstructed the candidate proof before consulting earlier verdicts. It then retrieved the critical primary bodies afresh. `SOURCE_ACCESS_RECEIPTS.json` and `SOURCE_NEIGHBOR_ACCESS.json` contain URLs, times, response types and byte fingerprints only. Raw PDFs, HTML, extracted text, renders and GitHub API data remain ignored. The complete 21-page September 2026 preprint was inspected, including assumptions, theorem statements, proof and references. The 2025 preprint and published model/main-results passages were independently reconciled. No previous review's PASS is used as a premise.

## Literal source question

The [official OWR report](https://ems.press/content/serial-article-files/51350), DOI [10.4171/owr/2025/7](https://doi.org/10.4171/owr/2025/7), was re-fetched at its declared 407,216 bytes and SHA-256 `7eaef18918195d4911ed399f76caec0bbb1fbc1432eacf838e06f403900b09ba`. Complete printed pp. 364, 365 and 371 were read and visually inspected. Page 365 explicitly assigns norm topology to the dynamical strong-continuity terminology, and separates it from the weaker strong operator topology. Page 371's subsection 2.2 has free kinetic energy on all space and a pair interaction integrated over Lambda×Lambda. It asks for a particular interaction and states without smearing. The adjacent fixed-high-density/Hartree subsection 2.1 is a bosonic model; it does not impose density or energy constraints on the fermionic question. Zero external one-body potential is permitted by the earlier context. The candidate's dimension-three example therefore meets the existential criterion. A fixed-vector discontinuity would not meet the question's topology, and is impossible for the stated self-adjoint dynamics.

## Exact relationship to the 2026 source

[Siebert, arXiv:2609.34402v1](https://arxiv.org/abs/2609.34402v1), submitted 28 September 2026, precedes the original 7 October candidate. Its current unversioned record still lists v1. Its PDF was independently fetched at 448,261 bytes and SHA-256 `5d35ca7805a8e1d8be3227eedcfb3e76111d85ae7df8cdcc3820d7c8fd15473c`.

Theorem 2.4 is literally for a full-space difference potential W(x−y), under dispersion, lower-bound, external-potential and local-propagation hypotheses. Proposition 2.6 explicitly proves maximal norm 2 for a nonzero constant full-space interaction cN(N−1). Neither literally states a spatial-cutoff theorem. In particular q(x)q(y) changes under simultaneous translations and cannot be identified with a difference potential merely by naming its plateau.

The proof-level cutoff adaptation nevertheless closes. Put q=1_B4 and K(x,y)=q(x)q(y). Decompose the candidate as sum_j h_k,j + sum_i≠j K(x_i,x_j), where h_k=−Delta+(1−k)q. The off-diagonal sum is ordered and the distinguished particle sees 2 sum_j K(x,y_j). Bounded symmetric multiplication preserves the sector domains and commutes with the smooth local-number observable. Choose cluster support near 2e1 inside Lambda, an interior probe near zero and an exterior probe near 6e1. The cross-kernel values are exactly 1 and 0. The source's packing, leakage derivative, local antisymmetrization and relative-phase argument use these properties; translation invariance is not needed by these bounded-kernel estimates. The original coarse O(n²t²) leakage gives positive qualitative norm discontinuity at sufficiently small fixed theta/n.

The step one-body potential is not smooth globally, but D(h_k)=H² with equivalent graph norm. A compactly supported smooth probe away from the jump lies in D(h_k²), because h_k sends it to another such function. Functional calculus gives ||(exp(−ith_k)−1)u||H² ≤ C|t|( ||h_ku||+||h_k²u|| ). This verifies the needed local H² propagation without pretending that multiplication by q preserves arbitrary H² functions.

## Independent check of the audit-time bootstrap

Let B0 contain the original packing cube, with closure inside a slightly larger B compactly contained in Lambda and disjoint from the fixed interior probe. Take smooth chi_B zero near B0 and one on B^c. For the interacting cluster, define F(s)=<dGamma(chi_B²)> and E(s)=<T_n>. The sector potential is bounded, the evolution preserves its H² domain, and smooth localization preserves that domain. The differentiated localization expectation has only the kinetic commutator:

    |F'(s)| ≤ C sqrt(F(s)) sqrt(E(s)+n).

Initially all n particles are inside Lambda. Conservation of the exact energy n(n−k)+E(0), with E(0)≤Cn^(5/3), and M=n−L give

    E(s)=E(0)+<M(2n−k−M)> ≤ Cn^(5/3)+2nF(s).

Here M≤N_Bc≤dGamma(chi_B²) as multiplication operators. This is a closed inequality, not an assumed small interacting kinetic energy. For G_delta=sqrt(F+delta),

    |G_delta'| ≤ Cn^(5/6)+C sqrt(n) G_delta.

Gronwall and delta↓0 give F(s)≤Cn^(5/3)s² exp(C sqrt(n)|s|). At s≤a/n the exponential is uniformly bounded.

The source's localized antisymmetrizer J_n has squared norm bounded by 1+N_A on distinguished-coordinate support in A. Decomposing by the number of cluster particles in A proves that estimate directly; the global norm sqrt(n+1) is unnecessary on the localized term. Split the distinguished/cluster vector into the all-cluster-in-B term, its cluster leakage, and the distinguished probe tail. The first residual vanishes exactly. The second squared norm is at most 8n²F(s): both the probability of cluster leakage and its weighted N_A expectation are bounded by F(s). This uses only a first moment of the interacting cluster. The third term is bounded by Cn^(3/2)|s| using the fixed probe's O(s) tail and the global J bound. Integrating gives comparison error C_a(n^(11/6)+n^(3/2))t².

At the original t_n=pi/(2n+1−k), take a=pi/2. The comparison error is O(n^-1/6+n^-1/2), and F(t_n)=O(n^-1/3). The cross phase exp(2int_n) tends to −1; for k=0 it is not exactly −1 by itself. Replacing the fixed probe's one-body evolution costs O(t_n); the cluster's occupation of that probe is bounded by F(t_n). Thus the creation matrix element tends to −1 and the annihilation dual matrix element to −2 for the original fixed mode and vectors. The CAR upper bound 2 gives the same norms and changing-state value 4. No circularity, interacting Slater assumption, or unsupported second moment occurs in this bootstrap.

This validates the current root/mapping/bootstrap discussion. The first priority family's coarse estimate has a genuine quantitative gap for that written estimate, which the later bootstrap closes. These are audit deductions from the earlier mechanism, not theorems literally printed in the prior paper and not evidence of earlier public disclosure of the bootstrap. Neither exact quantitative firstness nor method novelty is established.

## Other sources and remaining coverage limits

[Siebert 2025](https://arxiv.org/abs/2409.10495v2), also [LMP 115, 33](https://doi.org/10.1007/s11005-025-01919-y), extends the CAR algebra and obtains norm continuity after time averaging. Both preprint and published PDF fingerprints match the candidate's source identities. It is not a UV-smearing construction. The current records list v2. GNRS arXiv:1912.12552v2 and HLS arXiv:2310.17736v2 retain smearing in their positive continuity results; the model equations and principal continuity statements were checked. The HLS published body was also re-fetched. Buchholz arXiv:1709.08107v7 and 1807.07885v2 concern Bose/resolvent and extended-algebra dynamics. Their main continuity statements were checked and have different algebras/topologies. The localized-frame arXiv:2406.15670v2 model and Pachon arXiv:2604.26267v2 Corollary 8 are neighboring results, not the candidate's unregularized cutoff discontinuity. Current version histories were refreshed for all eight arXiv references.

The official Bratteli–Robinson preview's complete printed p. 354 was independently read and visually inspected: it gives a high-density physical expectation, not the displayed construction. The freshly served preview has a different PDF byte fingerprint from the older source manifest, so no byte identity is claimed; the current official body supports the same scoped attribution. Radin's author-hosted scan matches the packaged fingerprint; printed pp. 69, 78 and 79 were visually inspected. It explicitly limits the direct model argument to distinguishable particles and discusses the single-species indistinguishability obstruction and absence of a calculation in a specific quasi-local C*-algebra.

The [APS 1990 abstract](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.64.1863) is visible through the web reader and specifies a momentum cutoff; direct retrieval returned 403 and full-body access requires authorization. The 1991 subscription review was not newly authenticated. The thesis landing returned 403 in this review; the older report's empty-body access gap is not treated as resolved. The correct GNRS publisher-PDF route returned HTML, while the arXiv v2 body was accessible. An initial mistyped publisher DOI was corrected and is recorded as a reviewer locator error, not a source absence. A fresh search lead arXiv:2610.12731 was screened at its official abstract and concerns irreversible quantum spin dynamics.

Exact-title, cutoff/local-number and norm-discontinuity searches supplied no basis for firstness. Citation indices are demonstrably incomplete in the saved family evidence and cannot certify absence. The family's 95% coverage figure is an estimate of its bounded audit, not a novelty probability, and this review does not convert it into one. Current paper, README, live PR body and exact descriptor correctly refrain from first-solution, certified-method-novelty and continued-openness claims. No source or priority correction is required.
