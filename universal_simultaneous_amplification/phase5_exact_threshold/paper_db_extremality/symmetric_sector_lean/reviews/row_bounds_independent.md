# Independent review of concrete row bounds

Reviewer: phase-linear-algebra agent (not the author of RowBounds.lean).
Reviewed source: SymmetricSector/RowBounds.lean, 2026-09-14T04:53Z.

The theorem `coefficient_system_isUnit N hN` has exactly the mathematical domain
N ≥ 3. Its input is the concrete `coefficientK` defined from Appendix A, rather
than a surrogate numerical matrix. Good rows and bad rows split sums over the
actual channel type, so no nonexistent boundary state contributes.

The good-row bound (N+1)/(2N) is strict below one for N≥3. The bad-row proof uses
a valid majorization of the actual upper offdiagonal numerator N-k-2 by N-k-1;
the proof requires nonnegativity of the actual entry only when its successor
exists. The resulting defect (N+3k-1)/(2kN) is positive. The omitted predecessor
and successor states can only reduce absolute row sums. The dimensions are
N−1 and N−2, matching ranks 1..N−1 and 2..N−1.

The final theorem invokes a proved finite maximum principle and finite-dimensional
injectivity/surjectivity to establish invertibility; it assumes no determinant,
computed positivity, unique solver output, feature-map injectivity, or active-chain
identification. I found no mathematical gap in this translation. Invertibility of
the coefficient system does not prove its scalar is positive or identify its
inverse with the labeled active-chain Green operator.

The module's author reported a clean direct compilation; my dependency module
Phase.lean separately built successfully. The principal phase infrastructure
printed only propext, Classical.choice, and Quot.sound. The project's dedicated
trust reviewer is independently checking the final compiled dependency audit.
