# Source gate: quadratic-length universal random permutations

Date: 2026-10-21 UTC. Queue row 1841; problem ID 30003131; source key OWR-14604-008.

## Verdict

**Exact target recovered. A new, precisely matching preprint claims a stronger affirmative result. Independent proof acceptance is recorded separately; the independent auditor has returned PASS for the fully written 32k² theorem.** The queue target is the weaker 1000k² question, not the sharp-constant conjecture. The August 2026 dataset literature assessment predates the October manuscript and is stale for this question.

## Original question and model

Noga Alon, “When are random permutations k-universal?”, in *Combinatorics and Probability*, Oberwolfach Report 22/2016, printed p.1218 (PDF page 30), DOI 10.4171/OWR/2016/22. [Official report landing page](https://ems.press/journals/owr/articles/14604); [official PDF](https://ems.press/content/serial-article-files/46627?nt=1).

Alon's host has n independent Uniform[0,1] values; their ranks form a uniform element of S_n. A k-pattern occurs on increasing, not necessarily consecutive, indices, with exactly the target relative order. Universality means all k! patterns occur in the same host. Probability tends to one as k tends to infinity. His threshold shorthand f(k) asks, operationally, whether n=1000k² suffices. It does not demand certainty, every finite k, consecutive occurrences, or simultaneous independent hosts for different patterns.

The same passage records the stronger conjecture f(k)=(1/4+o(1))k², an increasing-subsequence obstruction, and O(k² log k) sufficiency. No arbitrary permuton or biased random-permutation model appears. The iid continuous-uniform sequence description and uniform finite permutation description agree through ranks.

The original page was text-extracted and visually inspected; the official publisher PDF's extracted passage was checked against the independently retrieved TIB copy.

## Exact later results and boundaries

1. Xiaoyu He and Matthew Kwan, *Universality of random permutations*, Bulletin of the London Mathematical Society 52 (2020), 515–529, DOI 10.1112/blms.12345. [Author PDF](https://mkwn.github.io/URP.pdf). Theorem 1.2 gives full k-universality with high probability at length 2000k² log log k. Theorem 1.3 gives length 20k² for every pattern in a particular deterministic family Q_k of size (1-o(1))k!, not all k! patterns. That theorem therefore does not settle the queue target. Their Conjecture 1.1 formulates the stronger threshold as (1+ε)k²/4 for each fixed ε>0. Lemma 2.2 is the Bernoulli-matrix interval-minor coupling used by the newer proof.

2. Yu Chen and Yiting Wang, *Quadratic-size Random Permutations are Universal*, [arXiv:2610.13530v1](https://arxiv.org/abs/2610.13530v1), submitted 9 October 2026. Theorem 1.1 states that absolute c>0 and n₀ exist such that, for every integer n≥n₀, a uniform permutation of length 32n² fails n-universality with probability at most exp(-cn/log n). Here their n is Alon's k. Section 4.1 sketches improvement to every fixed constant greater than 1. The manuscript explicitly leaves the sharp 1/4 constant open. Its arXiv record shows one version, no journal acceptance, and author responsibility for an AI-found proof. Treat this as a recent preprint, not a peer-reviewed publication. The full main proof and Section 4.1 were inspected; an independent audit subsequently returned PASS for the fully written 32n² theorem, including the coupling.

## Implication checked independently

For a uniform host of length 1000k², the relative order of its first 32k² entries is uniform on S_(32k²). Every pattern appearing there also appears in the full host. Consequently the newer theorem, if accepted, bounds failure at the exact queue length by exp(-ck/log k), which tends to zero. This is a direct monotonicity reduction, not a similarity-of-titles inference. It settles the stated weaker question while leaving the stronger leading-constant problem distinct.

## Dataset identity and verification evidence

The existing local problems corpus was freshly hashed, not freshly downloaded: 68,931,837 bytes, SHA-256 04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf. Exactly one problem matches both ID and source key, and its target agrees with the original 1000k² conjecture.

The existing local research-results corpus was freshly hashed: 80,334,822 bytes, SHA-256 8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b. It has no entry keyed by OWR-14604-008. This is not a claim of a fresh upstream dataset retrieval.

SOURCE_METADATA.json contains public URLs, retrieval timestamps, PDF/HTML byte counts and SHA-256 hashes. DATASET_METADATA.json contains local corpus hashes and match results. Copied source files, page rendering, and extracted dataset records are excluded from this package.

## Recommendation

The independently accepted 32k² theorem supports closing this exact weaker question as resolved by prior literature, with attribution and manuscript-status caveat. Do not spend a new research pass attacking an allegedly still-open quadratic-existence question before auditing that matching result. Do not report the sharp 1/4 conjecture as solved. No queue or GitHub changes were performed in this gate.
