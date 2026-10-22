# Independent priority audit A: triangle-specific history

Reviewer: `/root/pr1262_priority_triangle`. Problem 30001248, PR1262, submitted head `fb7b750865f3e220590f128661c487c5984bae75`. Audit performed 17 October 2026 UTC after the mathematical PASS gate. AI-assisted internal review; unrefereed and without external human peer review or formal proof-assistant certification.

## Decision

**PASS_CREDITED_CONSEQUENCE_ONLY.** The sharp conclusion is mathematically a full answer to the historical fixed-density triangle modulus question, but the substantive quantitative local limit input and the underlying mechanisms predate this work. Publication may explain the complete reduction and reproduce the known obstruction with explicit attribution. It must not claim a new local limit theorem, a new counterexample, a new mechanism, first resolution, current openness, or independent discovery lineage.

I did not locate an earlier printed statement of the exact full modulus equivalence in the bounded primary passages inspected. That negative search result does **not** establish novelty. The complete consequence is assembled in this audit from an older quantitative theorem, classical concentration and Gaussian summation, and a CLT obstruction already noted by Scott–Tateno. A theorem's corollaries do not become new in priority merely because a literal wording search does not find them.

This report was sealed before reading any other new priority family or source-question-family result. Root's exact mathematical target and PASS gate, and the submitted historical proof and audit, were read; they are not treated as certificates of bibliographic novelty.

## Exact target and historical question

The target is the ordinary triangle count, counting each unordered vertex triple once, for a fixed real density 0<p<1. The discrepancy is the maximum over **all** residues of the relative error `|q P(T=a mod q)-1|`, for **every** positive integer sequence q(n). The accepted equivalence is convergence to zero exactly when q=o(n²). Fixed q, prime q, an unscaled additive error, a support-only statement, labeled embeddings 6T, and a varying-density theorem are different claims.

Scott's contribution, explicitly joint work with Atsushi Tateno, already states the necessary o(n²) scale, proves an all-integer o(n²/log n) modular result, and states a triangle Gaussian unit-cell LLT. Its two contribution pages were freshly read and visually checked. It contains a proof description rather than a complete technical proof. The final broader subgraph conjecture must remain distinct from the triangle target. [Scott–Tateno, OWR23/2009, printed pp.1279–1280](https://doi.org/10.4171/owr/2009/23).

A Scott talk abstract in the May 2008 Dagstuhl collection already announces the smaller modular range. Oxford's seminar archive records Tateno talks on triangle residues in 2005 and triangle/complete-graph counts in 2006; those titles establish earlier activity, **not** theorem statements or proofs. [Dagstuhl collection, PDF p.8](https://drops.dagstuhl.de/storage/16dagstuhl-seminar-proceedings/dsp-vol08201/DagSemProc.08201.1/DagSemProc.08201.1.pdf), [Oxford archive](https://www.maths.ox.ac.uk/groups/combinatorics/past-events/past-junior-combinatorics-seminars).

## Triangle-specific priority map

| Source | Directly checked scope | Priority classification |
|---|---|---|
| Loebl–Matoušek–Pangrác, 2004 | Author preprint Theorem 1.2: p=1/2; primes between a constant and a function of order log n; relative uniformity. The theorem display was checked visually after local PS conversion. | Earlier modular triangle theorem, weaker range and density scope. |
| Scott–Tateno, 2008 abstract /2009 report | All fixed p; all integer moduli o(n²/log n); necessary o(n²) scale; triangle cell LLT stated. | Direct historical predecessor; sharpness idea already explicit. |
| Gilmer–Kopparty, 2014 preprint /2016 journal | Author PDF Theorem 2: uniform full shifted-integer-lattice Gaussian LLT, normalized error o(1); true standard deviation of order n². | Prior triangle LLT. An unspecified o(1) alone does not justify multiplying a growing tail or this particular logarithmic-window transfer. |
| Berkowitz, 2016 submission /2017 v3 | v1 p. 6 and v3 p. 7 Corollary 1: point error O(n^(-5/2+epsilon)), with correct centered lattice there; v3 p. 7 checked visually. | Prior quantitative triangle input strong enough for the present transfer; no new quantitative LLT here. |
| Berkowitz, 2018 clique preprint | Theorem 1 on PDF p.1: quantitative LLT for fixed cliques, with polynomial normalized error; triangles included. | Further earlier sufficient quantitative premise and explicit edge-projection/Fourier mechanism precedent. |
| Sah–Sawhney, 2020 preprint /2022 journal | v1 Theorem 1.1, p.3, gives normalized uniform error O(n^(-1/2+epsilon)); Section 5 p.28 counts isomorphic subgraphs once and uses the true mean/standard deviation. | Clean substantive imported theorem for this package. Theorem 1.3 already supplies the ordinary 2K2 obstruction. |
| Araújo–Mattos, 2023 v1 /2025 journal metadata | v1 introduction states the constant-p history and addresses sparse triangles; current archive/publisher metadata link later v3 and journal publication. | Later triangle history confirms earlier fixed-p coverage; its sparse theorem is not imported or claimed here. |
| Sah–Sawhney–Zhu, 2024 | PDF pp.1–3 restate the connected-count theorem and explain joint graph factors and the skew lattice. | Later explicit restatement, not a new triangle solution in this package; no product-Gaussian raw-count shortcut. |

The Loebl author preprint's actual Theorem 1.2 is logarithmic, matching Scott's account. Gilmer–Kopparty's introduction describes a smaller logarithmic-power range; I do not silently substitute that secondary account for the checked original theorem. The author-hosted Loebl page itself also has a volume typo, whereas the publisher metadata and Matoušek publication list give volume 289. No historical disagreement affects the present theorem.

The [Loebl paper](https://doi.org/10.1016/j.disc.2004.08.008), [Gilmer–Kopparty author version](https://sites.math.rutgers.edu/~sk1233/triangles.pdf), [Berkowitz v1](https://arxiv.org/abs/1610.01281v1), [Berkowitz v3](https://arxiv.org/abs/1610.01281v3), [2018 clique paper](https://arxiv.org/abs/1811.03527v1), [Sah–Sawhney v1](https://arxiv.org/abs/2006.11369v1), [Araújo–Mattos v1](https://arxiv.org/abs/2307.09446v1), and [joint-count paper](https://arxiv.org/abs/2412.09535v1) are primary references for these distinctions.

## What the older theorem already supplies

For triangles, the Sah–Sawhney pointwise theorem supplies a polynomially vanishing normalized error over **every integer**. The submitted reduction adds bounded-differences tails, a finite central residue sum, and the shifted Gaussian-grid comparison. Their error terms vanish for every q=o(sigma), including an arbitrarily slowly vanishing q/sigma. Since sigma is of order n², this supplies the whole sufficiency range.

The converse removes the mean phase from the first modular Fourier coefficient and uses the ordinary triangle CLT along a subsequence with sigma/q converging. Scott–Tateno already identifies the same normal-modulo-scale obstruction. The explicit varying-frequency and oscillating-sequence details make this reconstruction checkable; they do not justify a new mechanism or first sharpness claim.

The centered-edge projection also has direct precedent: Berkowitz's v1 p.3 and the 2018 clique paper p.2 explain the dominant degree-one edge component and the small higher-order remainder. The Gaussian mesh estimate, Poisson summation alternative, martingale concentration, and binomial CLT are standard tools. This package's credit should reflect a transparent assembly and validation of these ingredients.

No earlier exact printed iff statement was found in the checked theorem statements and modular references. This means the classification is **full consequence composed now from older results**, together with **same-mechanism precedent**; it is not an independently established earliest printed full theorem. The source LLT's deep decoupling and Fourier proof is used as an established import, not independently certified in full by this audit.

## Version and source limits

The archive dates are bibliographic dates, not the internal dates of downloaded PDFs. Berkowitz's freshly retained v1 has the 5October 2016 archive stamp but an internal 17September 2018 date; v3 has the 21March 2017 archive stamp and an internal 27November 2024 date. No cause or new theorem version is inferred from those mismatches. The v3 Corollary 1 used for priority has the correct triangle center. The submitted historical comments about other narrow display defects must not be generalized to every version or used to reject the paper's results.

Berkowitz's journal publication was **not verified**: the current archive page has no journal reference, the inspected later primary bibliographies cite a preprint, and one Crossref title search returned no exact Berkowitz journal item among its first eight results. This is not evidence of nonpublication. Cite the verified versioned preprint rather than inventing a journal reference.

Fresh publisher metadata verifies Gilmer–Kopparty, Random Structures & Algorithms 48(4),732–750(2016), DOI10.1002/rsa.20604; and Sah–Sawhney, Journal of the London Mathematical Society 105(2),950–1011(2022), DOI10.1112/jlms.12523. Direct requests for those publishers' full HTML failed, so their final published bodies were **not** compared line by line. Sah's current author PDF is byte-identical to the inspected arXiv v1. No claim that a journal proof or all versions were fully audited is made.

A 2026 ECCC lead, Shimizu–Yasunaga's *Hardness Amplification Beyond Boolean Functions*, was followed because it discusses triangle counts modulo primes. Its inspected application and reduction passages concern circuit hardness and sums of function values, not the required all-modulus distribution theorem. It supplies no priority clearance for our theorem. [Primary report](https://eccc.weizmann.ac.il/report/2026/038/).

## Search bounds and recommended publication wording

The ledger records **56 literal web queries in 14 batches**, plus **one separate Crossref title query**. This included historical names, exact titles, modulus/relative-uniformity variants, contemporary dates, and forward references through later triangle, connected-count, joint-count, and complexity papers. Repeated or poorly focused searches are retained honestly; unrelated geometry, mesh, graph-packing, and number-theory results were excluded. Search previews and whole-file term scans are not whole-proof reads, and search engines are not exhaustive citation indexes.

Backward references were followed from Scott to Loebl and the CLT history, and from quantitative work to Gilmer–Kopparty and its modular-count discussion. Forward checks include Berkowitz 2018, Kopparty's 2017 report, Sah–Sawhney 2020/2022, Araújo–Mattos 2023/2025, Sah–Sawhney–Zhu 2024, and the 2026 complexity lead. Standalone full Scott–Tateno technical work was not located; old missing research packages were not recovered or rerun. Fixed-q general subgraph theorems are contextual and cannot silently furnish growing-q uniform constants.

Recommended title: **Sharp modular equidistribution for triangle counts: a deduction from quantitative local limit theorems**.

Recommended central description: **For fixed 0<p<1, we give a complete derivation of the sharp q=o(n²) relative modular-uniformity criterion for ordinary triangle counts from the prior quantitative local limit theorem of Sah and Sawhney. The derivation addresses a range question recorded by Scott and Tateno, who already identified the necessary scale and established the smaller o(n²/log n) range. Earlier quantitative triangle work of Berkowitz provides sufficient input as well. We make no claim to a new local limit theorem, mechanism, or bibliographic priority for the corollary.**

Keep that credit in the abstract or first paragraph, proof premise, preprint metadata, README and final acceptance record. If the known 2K2 supplement is retained, credit Sah–Sawhney Theorem 1.3 prominently and identify the adjacent-target overlap without counting a second discovery. Extensive AI assistance and unrefereed status belong in both paper and metadata. Publication as a transparent attributed note is supported; novelty, present-day openness, human peer review, and independent discovery lineage are not certified.
