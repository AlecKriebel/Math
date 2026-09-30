# 30005451: affine preferential-attachment local comparison

[CANDIDATE.md](CANDIDATE.md) gives a complete candidate coupling theorem for the source's indegree-based Bernoulli model and two Poisson-outdegree adaptations, with frozen or sequentially updated weights. It identifies the common affine limit and proves empirical local convergence in probability.

- One substantive approach; separate adversarial review pending
- Exact parameter range: f(k)=ak+b, 0<=a<1 and 0<b<=1, Poisson mean b/(1-a)
- The dataset's fixed-outdegree equality is a source-extraction error
- General nonlinear concave rules and sampling without replacement are outside the theorem
- The Bernoulli neighborhood-tree limit is credited to Dereich–Mörters
- Priority unestablished; no novelty or human-peer-review claim
- Run `python verify.py` with SymPy for 35,349 exact finite/symbolic diagnostics
- [SOURCE_AUDIT.md](SOURCE_AUDIT.md) fixes all model, topology and source-version distinctions
- CHECKPOINT.md preserves the earlier unreviewed checkpoint and is superseded by CANDIDATE.md
