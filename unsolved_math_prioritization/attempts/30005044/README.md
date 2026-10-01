# 30005044: explosion with infinite-mean offspring

**Unreviewed complete candidate, author turn 1/5.** The original question is existential and concerns the contact process with fitness, not an age-dependent branching process.

The explicit law $\mathbb P(\xi\ge m)=m^{-1/4}$ has finite offspring at every vertex and infinite mean. For every $\lambda>0$, the proposed proof gives

$$
\mathbb P(|X_{1/(2\lambda)}|=\infty)\ge(7/30)e^{-3/(2\lambda)}>0.
$$

A deterministic geometric schedule and summable recovery windows ensure that infinitely many vertices are infected **at the same finite time**. Fitnesses at least 1 preserve the conclusion. Almost every tree has positive quenched probability of finite-time explosion for every infection rate. No classification of all infinite-mean laws or novelty is claimed.

- [Full proof and source-scope statement](PROOF.md)
- [Exact original target](TARGET.md)
- [Source and prior-attempt gate](SOURCE_GATE.md)
- [Primary inputs](source_manifest.json)
- [Exact finite controls](verify.py) and [receipt](verification.json)
- [Research log](RESEARCH_LOG.md), [turn ledger](turns.json), and [adversarial review request](REVIEW_REQUEST.md)

Run `python verify.py` from this folder. The checker uses the Python standard library only. It checks finite algebra and conditioning controls; the infinite probability arguments require mathematical review.
