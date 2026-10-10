# Acceptance of the Frobenius permanent proof

**Result: PASS.** Independent adversarial audit found no mathematical defect in the frozen candidate for corpus 30001073 / OWR-2090-026, the Barvinok-Samorodnitsky bounded-Frobenius permanent question in OWR 44/2008, problem 9, printed pages 2549-2550.

Distributed proof edition: `PROOF.md`, 8,060 bytes, SHA-256 `fe83f40d5c6d96a526457eaae290e8b3f0a725b43a91286f818c4fb248db7205`. The complete mathematical and prior-work text of the accepted frozen proof is unchanged; only its opening status sentence is updated. This identity binds the publication edition.

The candidate proves, for every nonnegative row-stochastic n by n matrix with S = sum(a_ij^2),

    per(A) <= exp(-n + e^4 S(1 + log n)).

For the source's fixed gamma hypothesis S <= gamma and n >= 2, this yields

    per(A) <= n^(3e^4 gamma) exp(-n).

Together with the source's known van der Waerden lower bound in the doubly stochastic case, this answers the original asymptotic question affirmatively. The candidate's explicit n = 1 qualification is necessary and correct.

The audit checked the random-order entropy conditioning and support, Gibbs identity, total-mass KL decomposition, scalar absorption, Frobenius entropy estimate, row-stochastic strengthening, zero and unit entries, and block-diagonal polynomial-loss example. It visually checked both original problem pages and the directly relevant prior entropy equation in Anari-Rezaei arXiv:1811.02933v2, section 4, equation (6), page 12.

Acceptance is mathematical and hash-specific. It does not certify novelty or priority. Preserve the current attribution to established entropy methods and the distinction between the source's Frobenius hypothesis and its stronger entrywise special case.

Detailed reasoning and public source hashes are recorded in `AUDIT.md`; the edition-specific mathematical verdict and report identities are in `audit_manifest.json`.
