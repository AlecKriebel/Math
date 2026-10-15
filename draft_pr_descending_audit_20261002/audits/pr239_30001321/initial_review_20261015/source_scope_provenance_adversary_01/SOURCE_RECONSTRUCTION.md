# Independent source reconstruction (sealed before old review verdicts)

Authenticated source: Noam Berger, “Quenched Local Limit Theorem for Space-time Random Walk in Random Environment,” Oberwolfach Report 38/2009, printed pp. 2151–2152; DOI 10.4171/OWR/2009/38. The EMS PDF fetched directly on 2026-10-15 has SHA256 `4642f579215a28b58adb465e3eb3f1512b6dde596505df5a64b3eaae69b86847` and 591192 bytes. Rendered PDF pages 37–38 (one based) were visually inspected. No submission source-audit prose or old independent mathematical verdict had been opened when this note was made.

## Reconstructed statement

The model is a spatial random walk with an environment refreshed independently after each time step, equivalently an oriented walk whose distinguished coordinate increases by one. Its averaged law is described as a possibly biased simple random walk. The stated theorem assumes iid, nearest-neighbor, elliptic space-time RWRE in dimension 1+d, with d≥2. Thus d counts the transverse spatial dimensions and does not count directed time. The first coordinate is deterministic time.

For every deterministic sequence M_N→∞ and epsilon>0, take at each N a partition into cubes of side M_N. Sum the absolute differences of quenched and annealed probabilities of those cells at time N. The environment probability that this sum exceeds epsilon decays faster than every inverse power of N. The printed conjecture says that the same assertion fails at d=1.

The page literally typesets the partition space as Z (no superscript d). This is a dimensional typography issue for d≥2, and disappears at d=1. No rate restriction on M_N appears in Theorem 1. The subsequent remark adds rate restrictions for a different extension to ordinary RWRE satisfying (T'); those restrictions must not be imported into this space-time theorem. Page 2152 describes a proof mechanism and gives a martingale inequality; it adds no hypotheses to the theorem.

## Scope tests to apply

- The iid assumption has both spatial and temporal content. Temporally refreshed but spatially perfectly correlated layers do not satisfy it.
- Elliptic is printed; uniformly elliptic is not printed. A d=1 scalar probability p in (0,1) a.s. fits the ordinary transverse nearest-neighbor model. No inverse-moment condition or common deterministic lower bound is stated.
- One fixed environment law is chosen before taking N→∞. A triangular array of laws depending on N is outside the printed asymptotic assertion.
- In d=1, an equal-length partition into consecutive lattice intervals is a translate of one grid; all deterministic translates should be included. Arbitrary unequal intervals are a stronger assertion and are not demanded by the printed equal-cube statement. Environment-dependent partitions are not explicitly covered.
- The source does not state arbitrary finite-range jumps, holding probabilities, or nonnearest-neighbor kernels. A d=1 proof for two jumps ±1 need not cover those wider models to address the printed conjecture.
- A nearest-neighbor transverse walk is periodic. Any source comparison must retain that parity and must not treat the endpoint law as an aperiodic lattice kernel.
- The strongest success criterion is the universal positive d=1 analogue at each fixed iid merely elliptic law, each deterministic diverging sequence and each epsilon>0, with superpolynomial environment tails. A single positive special law refutes an indiscriminate universal negative only under one reading; it does not settle whether a nondegenerate counterexample to the asserted extension exists. The claimed submission advertises the stronger universal positive analogue, which should be checked directly.

This source reconstruction authenticates the target; it does not verify the submission's proof or establish novelty.
