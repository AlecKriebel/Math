# Proof-repair checkpoint

Timestamp: 2026-09-15T03:47:20.370813+00:00

The runner audit agent subsequently repaired and successfully compiled these five original modules using the pinned toolchain and `lake build`:

- `GeneralSwap`: actual all-dimensional swapped target and nonuniformity.
- `GeneralGuessing`: exact chord identities and quantitative guessing gap.
- `GeneralSecondCoefficients`: literal coefficient phase/sign, exact polar Fourier compression and Parseval normalization.
- `GeneralOperational`: actual partial trace/sandwich, private MUB composition and trivial Eve realization.
- `GeneralOneInput`: dependent-output nonsignalling locality, zero marginals, normalized pure stored-assignment realization, Born behavior reconstruction and perfect Eve guessing.

Their individual build logs are in this directory. No theorem was replaced by an assumption or weakened. Repairs fix keyword identifiers, dimension/coercion inference, sum scope parentheses, complex/real coercions, matrix multiplication associativity for rectangular matrices, dependent equivalence reductions, and proof tactics. `GeneralOperational` now directly imports `GeneralFirstWitness` instead of the unnecessary `GeneralSecondWitness`; all theorems in the file require only the first-family construction. A reusable `matrix_map_star_mul` theorem was added. Original final endpoint names are preserved.

Best estimate: assigned five-module proof repair is 100% complete. Whole-paper formalization and final clean audit remain in progress under the parent agent. These module builds are not a whole-paper certificate.
