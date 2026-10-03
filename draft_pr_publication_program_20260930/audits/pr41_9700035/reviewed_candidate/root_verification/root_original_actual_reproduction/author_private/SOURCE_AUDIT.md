# Source and prior-art audit

Checked 30 September 2026. This is a bounded current-literature audit, not an exhaustive novelty certificate.

## Original statement and two corrections

The pinned dataset's statement matches **Open Problem 35** in [Aldous's 2012 manuscript](https://www.stat.berkeley.edu/~aldous/206-SNET/Papers/aldous_SIRSN_long.pdf). Its discussion identifies far-away excursions as the obstacle. The [2014 published paper](https://www.maths.tcd.ie/EMIS/journals/EJP-ECP/article/download/2920/2920-16115-1-PB.pdf), EJP 19, article 15, renumbers it **Open Problem 9**, p. 38, and asks what additional assumptions, if any, suffice. The present arXiv record still lists only [1204.0817v1](https://arxiv.org/abs/1204.0817), dated 3 April 2012; that record is not the revised published paper.

The historical imported report is preserved unchanged in `prior_report.json`, but its description of span as a minimal Steiner-type connecting network is wrong. Span is the union of the prescribed pairwise routes. Also, the constant ell is the length intensity of the rate-one Poisson sampled network, not a generic optimization constant. Relevant published definitions and scaling relations are in Sections 2.2–2.3 and 6.1–6.3. The conditional proof keeps the whole route length, including the exterior of the sampling square.

The author's [maintained SIRSN problem page](https://www.stat.berkeley.edu/~aldous/Research/OP/sirsn.html) continues to point to the paper's problems and the Poisson-line literature. It does not provide a resolution of this asymptotic.

## Later primary literature

- **Kahn, 2016:** [Improper Poisson line process as SIRSN in any dimension](https://arxiv.org/abs/1503.03976), current v3, 29 September 2016; Annals of Probability 44(4), 2694–2725, DOI [10.1214/15-AOP1032](https://doi.org/10.1214/15-AOP1032). The full paper was retrieved; Theorem 5.1 and its proof, Remark 5.1, Theorem 6.1, and the main construction statement were inspected. The proof of Theorem 5.1 gives finite route-length moments of order less than gamma−1. Remark 5.1 proposes better moments as a conjecture. It must not be promoted to a theorem. This paper supplies a concrete SIRSN and moment information, not the general spanning-length law claimed by the dataset.
- **Blanc–Curien–Kahn:** [Geodesics in planar Poisson roads random metric](https://arxiv.org/abs/2407.07887), arXiv v1, 10 July 2024, published in PLMS in 2025, DOI [10.1112/plms.70070](https://doi.org/10.1112/plms.70070). The current version history, full preprint, published abstract and principal statements were inspected. The main results concern non-pausing geodesics, the geodesic frame, and local stars/hubs. They do not state the requested general spanning-length asymptotic. This audit is not an independent certification of every proof in that 57-page paper.
- **Kendall:** [From Random Lines to Metric Spaces](https://arxiv.org/abs/1403.1156) and [Rayleigh Random Flights on the Poisson line SIRSN](https://arxiv.org/abs/1908.08481) were checked for context and for the distinction between construction/route regularity and the spanning functional. The historical pre-SIRSN difficulty in the former is addressed by Kahn's later construction result; it is not treated as current proof that no SIRSN exists.

The moment theorem in Kahn suggests concrete cases where the supplied extra assumption can be checked (for example, gamma>5 gives a finite fourth moment by that published result). The binary-hierarchy model also has bounded stretch, as Aldous's Proposition 3.1 and its extension to the continuum explain. These are applicability observations using credited existing estimates; no novelty claim is made for those model properties.

## Scope and stopping decision

`PROOF.md` proves the interior law from stationarity, scaling, finite intensity and finite mean route length. Its full-network theorem additionally assumes t^4 P(D>t) tends to zero. No implication from the original axioms to that tail hypothesis is established. The missing general step is an integrable control of distant excursions, not the in-square approximation or the Poisson-to-binomial conversion.

Searches included the exact problem phrase, SIRSN spanning-length asymptotics, route-length moments, and 2024–2026 geodesic results. No general resolution was located. This is a qualified search finding, not proof of absence.

## Repository and dataset gates

Before any branch push, all-state PR searches for `9700035`, `SIRSN`, and `spanning subnetwork` returned no prior attempt. The remote branch `dot/math-9700035` did not exist. Main had no attempt folder for this ID, and its queue row was rank 61, queued, 0/5. No entry in the related-target groups supplied a duplicate. The pinned problem code has one record; the historical report joins uniquely on AMR-096-0035. The nearby SIRSN records 9700027–9700036 ask distinct questions; none is silently counted as solved by this partial result.

Full source PDFs remain outside the repository. `source_provenance.json` records their hashes and URLs.
