# Counterexample and adversarial catalog

## C-01: zero-parameter mobile criterion is false

For

\[
J=\begin{pmatrix}-10&20&-50\\1&1&0\\1&0&2\end{pmatrix},\qquad M=\{1\},
\]

`J` is Hurwitz and the determinant-at-zero blocks containing the immobile set do not supply the proposed negative witness. Nevertheless

\[
J-\operatorname{diag}(257/2,0,0)
\]

has eigenvalue `3/2`, and at that positive spectral parameter the immobile block determinant is `-1/4`. The repaired theorem must quantify over `lambda > 0`.

## C-02: nonzero modes cannot generally be restricted to S

Take `S = span((1,1))` and `D = diag(1,2)`. Then `D(1,1)=(1,2)` is not in `S`. The zero spatial mean, not pointwise membership in `S`, enforces integrated conservation laws.

## C-03: same signed interaction graph, opposite network answers

The fixed-row realizations of the two all-negative Hurwitz matrices recorded in the manuscript have identical unsigned and signed interaction graphs for every positive realization. One is signed-P0 on every principal set; the other has a negative signed two-species minor and is admissible.

## C-04: same Gamma, opposite network answers

Two exact two-species networks use the ordered columns `[e1,-e1,e2,-e2]`. Different source complexes yield respectively a Hurwitz factor with a positive diagonal entry and the identically zero factor for every positive steady flux.

## Falsifier results

- No matrix with a negative signed principal minor but without a constructive positive diagonal witness was found in the complete bounded census or random rational campaign.
- No false YES/NO appeared in 917 small `PARTITION` instances.
- Numerical optimization on exact NO instances did not find a right-scaled Hurwitz lift.
- All Boolean selectors matched the principal-block determinant identity.
- Both circuit enumerators and every exact cone decomposition agreed.

These failures to find additional counterexamples are corroborative only; the outcome rests on the independent proofs.
