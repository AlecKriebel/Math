# Acceptance of bounded density degree results

## Verdict

Accept the bounded results in PROOF.md for problem 20000357, AIM Problem 1.18. The complete mathematical audit supports both finite-cover transfer directions, the Galois divisor restriction, sharp minimum bounds, the non-Galois residue example, and the stated curve-component transfers. This is a mathematical review of the written argument, not journal acceptance, formal proof-assistant certification, a novelty claim, or a solution of the full original problem.

## Accepted claims and hypotheses

For a finite dominant degree-\(n\) morphism of geometrically integral varieties over a number field, density at degree \(d\) upstairs forces density at some degree \(d/m\) downstairs with \(m\mid d\) and \(1\le m\le n\); density at degree \(e\) downstairs forces density at some degree \(em\) upstairs. For a Galois function-field extension, the multipliers divide \(n\). When the minima exist, \(b\le a\le nb\), and the proof supplies both endpoints for each \(n\).

For finite degree-\(n\) maps of smooth projective geometrically integral curves, the accepted component claims are

\[
n\delta_{\mathbb P^1}(D/k)\subseteq\delta_{\mathbb P^1}(C/k)
\]

and, for every integer \(r\ge2\),

\[
rn\delta_{\mathrm{AV}}(D/k)\subseteq\delta_{\mathrm{AV}}(C/k)\cap\delta_{\mathbb P^1}(C/k).
\]

Acceptance depends on the actual closed-point construction: the multiplication theorem supplies a point in the required divisor class on \(D\), its pencil composes with the cover, and Hilbert irreducibility produces an integral fiber on \(C\). Pulling back an effective divisor alone is insufficient.

## Residual and verification boundary

No undilated AV inclusion or complete classification of possible spectra is established. The cubic example proves dense nondivisor residue behavior, not the failure of every conceivable set-level strengthening. No comprehensive literature-closure claim is made.

The source hypotheses were checked as recorded in SOURCE_HYPOTHESES.md and SOURCE_PINS.json. The public proof preserves all mathematical sections of the accepted 17,481-byte proof after two notation-only backslash restorations and removal of an internal row identifier. The audit preserves all ten mathematical checks, the source review, and the exact residual; editorial changes concern provenance wording and distribution administration.

Input hashes, closed manifests and controlled mutations establish preservation and distribution boundaries. They do not prove generic étaleness, Hilbert irreducibility, Riemann–Roch, the index-existence theorem, Picard-variety facts, or any other algebraic-geometric assertion. Those are justified in the mathematical argument or identified as established theorem dependencies.
