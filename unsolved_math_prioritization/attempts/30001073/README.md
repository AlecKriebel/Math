# Permanent bounds under a bounded Frobenius norm

Problem 30001073 / OWR-2090-026, rank 1230. Approach 1 of 5.

**Complete mathematical solution, accepted after independent analytic audit.** For every nonnegative row-stochastic n by n matrix A, writing S = sum a_ij²,

    per(A) ≤ exp(−n + e⁴ sum a_ij² log(e/a_ij))
           ≤ exp(−n + e⁴ S(1+log n)).

Zero summands are defined by continuity. Under the source's fixed-γ hypothesis S≤γ, the all-n estimate is exp(e⁴γ) n^(e⁴γ) exp(−n). For n≥2 it implies per(A)≤n^(3e⁴γ) exp(−n). The literal pure-power form is false at n=1 and is not asserted there.

For doubly stochastic matrices, the source's already-known van der Waerden lower bound supplies the other direction, answering the original asymptotic question. The upper-bound proof needs only row stochasticity and does not substitute a stronger entrywise O(1/n) hypothesis. Equal uniform blocks show that some polynomial loss is necessary; the displayed exponent is not claimed sharp.

## Reading order

- [PROOF.md](PROOF.md): complete self-contained analytic proof, endpoints, block example and prior-work boundary.
- [AUDIT.md](AUDIT.md): full substantive independent mathematical audit.
- [ACCEPTANCE.md](ACCEPTANCE.md): precise accepted scope and attribution requirements.
- [SOURCE_LEDGER.md](SOURCE_LEDGER.md): public bibliographic metadata, PDF identities and bounded retrieval/inspection history.
- [PROVENANCE.md](PROVENANCE.md): edition identities and exact editorial boundary.
- [audit_manifest.json](audit_manifest.json), [STATUS.json](STATUS.json) and [MANIFEST.json](MANIFEST.json): edition-bound verdict, scoped status and complete publication inventory.

The Gibbs-marginal/random-order method is explicitly credited to Anari–Rezaei, arXiv:1811.02933v2, §4, equation (6), with classical entropy-method attribution to Radhakrishnan. No novelty, priority or sharp-constant claim is made. This work is AI-assisted and unrefereed; independent analytic audit is not external human peer review or proof-assistant certification.

This edition adds no proof-search turn and makes no change to the queue or historical accounting.
