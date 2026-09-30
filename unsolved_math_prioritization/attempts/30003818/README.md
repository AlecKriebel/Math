# 30003818: Brownian first-visit cell lengths

[JOINT_LAW.md](JOINT_LAW.md) gives a complete independently reviewed analytic joint-law characterization for both starting rules in the original question. Every Laplace-transform coefficient is reduced to a finite sum of deterministic integrals of explicit interval exit kernels. The outer series has a uniform factorial truncation bound.

The formula concerns first physical visits by independent walkers that never stop or coalesce. It preserves dependence between test-point hitting times of each walker. This is a transform answer, without a claimed named density or fast numerical evaluation.

- One substantive family (1/5); separate adversarial AI review passed: [report](review/REVIEW.md), with 46,056 independent exact controls. The frozen artifact’s earlier pending-review header is superseded by this record
- 8,520 exact diagnostic assertions pass, using Python’s standard library
- Run `python verify.py` to reproduce the receipt on stdout
- The exact finite controls support the reasoning, but do not replace the Brownian proof
- Standard kernels and strong Markov methods are credited; historical priority is unestablished
- AI-assisted, not human peer reviewed; the coordinating task owns queue changes
