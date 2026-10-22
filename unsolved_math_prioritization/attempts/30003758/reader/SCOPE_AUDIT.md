# Source-scope audit

30003758 / OWR-15999-007 · 13 October 2026

## Decision and preserved question

**Defer for source-scope clarification.** No uniquely specified outstanding
proposition has been recovered, and no replacement formalization is adopted.
This is neither an impossibility result nor an `already_solved` classification.

Mixon's contribution, joint work with Villar, to *Applied Harmonic Analysis and
Data Processing*, Oberwolfach Reports 15 (2018), printed pp. 785–787, asks on
printed p. 786:

> Can we extrapolate a near-optimal clustering for T from the SDP of S?

The source defines finite Euclidean squared-error k-means and the Peng–Wei SDP,
with S chosen uniformly among subsets of a fixed size. It leaves the quality
bound, confidence, sample budget, data hypotheses, and extrapolation access or
computational restrictions unspecified. It does not forbid reading unsampled
points. The 2018 volume was published in January 2019; these dates identify the
same source. See the [publisher](https://ems.press/journals/owr/articles/15999)
and [report](https://ems.press/content/serial-article-files/46736).

## What later results establish

- **Zhuang–Chen–Yang (2022):** A sampled SDP, estimated centroids, and nearest-center
  assignment yield exact planted-label recovery under specified Gaussian-model,
  separation, dimension, and cluster-count conditions. The theoretical sample
  law is independent Bernoulli; fixed-size sampling is described as a practical
  alternative. Unequal-cluster variants retain hypotheses. Their multi-epoch
  conjecture is a separately identified later target. See Sections 3–4 and
  Theorems 4.1, 4.3–4.4 of [*Sketch-and-lift*](https://proceedings.mlr.press/v151/zhuang22a.html).
- **Clum–Mixon–O'Hare–Villar (2024):** Algorithm 1 and Theorem 2 describe Bernoulli
  subsampling followed by assignment of all points to estimated centroids.
  Optimal-partition recovery is conditional on positive proximity, a geometric
  radius/separation condition, and a sample threshold depending on dataset
  geometry, dimension, cluster count, and balance. Section 4's lower-bound
  certificates serve a different purpose. See the [final journal article](https://academic.oup.com/imaiai/article/13/3/iaae016/7713562).
  The [2022 arXiv v1](https://arxiv.org/abs/2211.15744) has different author naming
  and order; its downloaded PDF is not represented as the final journal PDF.
- **Mixon–Villar (2017):** The sampled-SDP lower bound in Theorem 2.1 is a
  certification result. It is not, by itself, a method to produce the full-data
  partition. The historical extrapolation wording above comes from the OWR
  contribution. See [*Monte Carlo approximation certificates for k-means
  clustering*](https://arxiv.org/abs/1710.00956).

These conditional pipelines answer meaningful versions of the research direction.
Their existence does not select a universal approximation theorem for this entry.
The cited proofs were not independently audited here, and this audit does not
rely on any unexamined boundary case of a published theorem. No published-paper
error is alleged.

## Scope that must be settled before proof work

A separately stated residual would need to fix:

1. The data class and the objective: approximation of k-means cost, recovery of
   specified labels, or another explicit success criterion.
2. A multiplicative or additive quality inequality, its accuracy parameters,
   and a convention when the optimum is zero.
3. The sample law and a nonvacuous size bound, including dependence on dataset
   size, dimension, cluster count, geometry, accuracy, and confidence.
4. The available SDP output, treatment of fractional or nonunique optima,
   rounding and ties, solver accuracy, access to unsampled coordinates, and
   computational budget.
5. The probability space and success probability, repetitions if allowed,
   and whether the guarantee is uniform over datasets or model-dependent.
6. Nonempty-cluster and sample-feasibility conventions.

The source does not choose these values. A fixed-size guarantee cannot simply
be imported from a Bernoulli theorem without a justified transfer and probability
accounting. A rare omitted cluster only obstructs a suitably specified algorithm
or information model; it does not refute every possible extrapolation step.
Likewise, a cost certificate does not automatically construct the desired
partition. Choosing an open question from a later paper would require its own
identity and literature comparison.

## Acceptance boundary

Accepted here: the source-scope hold and the need to compare an explicitly
chosen residual against known conditional results. Not established: a new
mathematical result, a proof correction, global openness, exhaustive current
literature coverage, or a lifetime attempt count. The bounded primary-source
review is dated 13 October 2026. This assessment contributes zero new substantive
proof-attempt passes, and readiness remains uncleared.
