# Independent secondary smoothing check

UTC: 2026-10-24. Internal subagent `smoothing_secondary` started with no inherited conversation and did not author the proof or edit files. Full21.124 discovery estimate remains **4%**.

The secondary reviewer independently verified the rational-function criterion, denominator-square clearing and all-positive-axis hypothesis. It found no endpoint gap in the smoothing argument. It independently confirmed the explicit integer-m threshold by exact rational arithmetic for m=1,...,100.

The reviewer identified the same literal Laurent/ordinary-polynomial defect as the primary reviewer, and also requested an explicit integer qualifier for m. Both corrections were propagated by the author; the final note hash is in RECEIPT.json.

The reviewer supplied a separate proof of the required uniform estimate. Let M≥d and0≤k≤M. The ratio

    (k)_j (M-k)_(d-j)/(M)_d

is the probability that the first j of d ordered draws from M objects are successes and the remaining d−j are failures, when sampling without replacement from a population with k successes. Sampling with replacement gives probability

    (k/M)^j (1-k/M)^(d-j).

The replacement sample conditioned on all labels being distinct has the without-replacement distribution. The probability of at least one repeated pair of labels is at most binom(d,2)/M. Consequently the absolute difference between the two pattern probabilities is at most that bound, uniformly in k, including k=0,M. After multiplying by |c_j| and summing, this bounds the normalized coefficient error by

    binom(d,2) * sum_j |c_j| / M.

This tends to zero uniformly and is identically zero for d=0,1. The positive minimum of F on the compact simplex therefore yields eventual positive coefficients. This is a self-contained finite sampling argument; no external positivity theorem was assumed.

The reviewer explicitly rejected any inference that a compatible CAT(0) Gram matrix automatically produces such rational weights. The audit concerns the construction once a finite strictly positive rational kernel has been provided.
