# Problem 6600013: complexity and rational tiling cohomology

**Reviewed disposition: unsolved, 5/5. Full independent scoped source/proof audit: PASS, with an additive topological clarification.**

Julien's original question asks whether O(n^d) translational patch complexity forces finite total rational Čech cohomology rank for an aperiodic repetitive d-dimensional tiling. The general implication remains unresolved.

- [Exact source and conventions](SOURCE_NORMALIZATION.md)
- [All five scoped outcomes and remaining gap](RESULT.md)
- [Full independent review](final_review/ADVERSARIAL_REVIEW.md)
- [Required unit/Perron–Frobenius roof clarification](final_review/TOPOLOGICAL_CLARIFICATION.md)
- [Original question, Problem 2.5.1](https://arxiv.org/abs/1604.06280)

## Scoped progress

1. A sharp cohomology bound for Cartesian products of one-dimensional systems, with Sturmian equality cases.
2. A source-admissible sheared Thue–Morse/Sturmian example whose raw approximant Betti numbers grow while its limiting cohomology stays finite.
3. A stable-image criterion and exact cochain calculations which identify transient classes that disappear.
4. A finite-stage local covering theorem and minimal cyclic covers with Betti numbers (1,4,q+3), each having its own finite complexity coefficient.
5. An infinite-rank 2-adic suspension whose specified transversal action is nonexpansive and has no continuous finite-alphabet generator. It does not furnish an admissible FLC counterexample.

All finite-cover hypotheses, rational coefficients, no-nonzero-period convention and the single O(n^d) constant required by the original are retained. Arbitrary finite-to-one factors are not assumed to be covers. Integral non-finite-generation and unbounded approximant ranks do not settle rational limiting rank.

## Additive metric clarification

Turn4's variable-length substitution a→aab,b→ab uses the stationary graph model with Perron–Frobenius edge lengths ((1+sqrt5)/2,1), and expansion (3+sqrt5)/2. The tilewise roof-change homeomorphism identifies its topology with the unit-roof symbolic suspension. This is an orbit reparameterization, not a translation-time-preserving conjugacy. It preserves symbolic edge-crossing cocycles and lifts compatibly to the finite decorated covers. Unit-box complexity counts remain in their original normalization. See the linked full clarification.

All 44 frozen author files and all nine review files remain byte-identical. Historical pending-review wording is retained; this wrapper records the completed scoped verdict. Classical Rauzy, Čech, substitution, covering and linear-algebra ingredients are credited, with no novelty certification. The audit is AI-assisted, not external peer review.

## Replay

Python3.10+ standard library only:

    python REPLAY_ALL.py
    python verify_review.py

The author replay reproduces 5,367 assertions and 173 manifest bindings. The portable review entry point also verifies all frozen review hashes, the 44 original Git blob bindings and 22,728 independent controls. It reruns the author controls. Exact rational image computations take longer than the other checks; allow them to finish.

Raw source PDFs are excluded. Optional `--sources PATH` on either command checks the four primary PDF hashes when supplied independently. Without that option the reported source count is zero. Finite controls support the written all-scale proofs and do not replace source admissibility, persistence or topological arguments.
