# Source scope and literature status

## Source problem

- Afonso S. Bandeira, *Ten Lectures and Forty-Two Open Problems in the Mathematics of Data Science*, Open Problem 9.3, MIT course excerpt pp.1–2: [primary PDF](https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-of-data-science-fall-2015/29dc319cb9f8992c5b4b46b917ecd86d_MIT18_S096F15_Open9.3.pdf).
- Dustin G. Mixon, *Applied Harmonic Analysis and Sparse Approximation*, August 25, 2015, Problem 6, attributing the observation to Rachel Ward: [primary post](https://dustingmixon.wordpress.com/2015/08/25/applied-harmonic-analysis-and-sparse-approximation/).

These sources motivate exact LP tightness for unplanted Euclidean data. The earlier post specifies a uniform Frobenius-sphere law. Neither fixes the relation between dimension, sample size and cluster count. We therefore state every partial result's regime, without inserting a universal worst-case metric conjecture into the question. The source's incidental reference to an integral “k-means” solution immediately after its k-median LP is a naming slip; objective (1) is unsquared data-point k-median.

## Credited correction of the disjoint-ball claim

Alberto Del Pia and Mingchen Ma, *k-median: exact recovery in the extended stochastic ball model*, Mathematical Programming 200 (2023), 357–423; [accepted arXiv v2](https://arxiv.org/abs/2109.02547v2), [publisher](https://doi.org/10.1007/s10107-022-01886-5).

Appendix B, Example 2, contradicts Awasthi et al.'s Theorem 7: dimension 2, seven unit balls, minimum center separation 2.2, radial continuous density, positive mass around each center, and sufficient outer-shell concentration. Its exact conclusion is failure of planted exact recovery with probability tending to one. That conclusion alone does not establish a strict global LP/IP gap.

Theorems 6–7 assume dimension m>=2, unit radii, equal sample counts, equal expected radii, rotational invariance, absolute continuity, and positive mass in every center neighborhood. Sufficient center separation is respectively >3.29 or >2+C sqrt(k log(m)/m), for a positive constant C. Theorem 8 gives >2 under the stochastic-ball model with the same regularity assumptions and a strictly radially decreasing density. High probability refers to sample count per ball tending to infinity. These are planted-recovery statements, not unplanted Gaussian tightness theorems.

The inherited synopsis for record AMR-027-0903 treated the broad separated-model result as settled without this correction; that unqualified treatment should not be retained.

## Other credits and limits

Pranjal Awasthi, Afonso S. Bandeira, Moses Charikar, Ravishankar Krishnaswamy, Soledad Villar, and Rachel Ward, *Relax, no need to round: integrality of clustering formulations*, ITCS 2015, [arXiv v5](https://arxiv.org/abs/1408.4045v5). This is the historical clustering-relaxation source. Its disputed stochastic-ball theorem is not a dependency of the present proofs.

Mohammadtaghi Hajiaghayi, Wei Hu, Jian Li, Shi Li, and Barna Saha, *A Constant Factor Approximation Algorithm for Fault-Tolerant k-Median*, SODA 2014, [author PDF](https://cse.buffalo.edu/~shil/papers/FTKM-SODA2014.pdf), Lemma 3.1, already proves line-metric integrality for a more general LP. Approach 2 is an elementary proof for the ordinary-demand special case, not a new theorem claim.

The search also located Sang Ahn, Colin Cooper, Gérard Cornuéjols, and Alan Frieze, *Probabilistic Analysis of a Relaxation for the k-Median Problem*, Mathematics of Operations Research 13(1) (1988), 1–31, [publisher abstract](https://doi.org/10.1287/moor.13.1.1). Its stated near-optimal-value analysis for a planar model is not used as an exact-tightness theorem here; the full paper was not inspected in this attempt.

Targeted searches inspected source titles, exact problem phrases, Gaussian/unplanted tightness, and subsequent clustering-LP literature through 2026-10-07. No directly applicable resolution of the unspecified joint probability question was established. This is a bounded search result, not a certification that no later result exists. Approximation ratios, k-means SDP recovery, planted exact recovery, and exact LP value equality are kept distinct.
