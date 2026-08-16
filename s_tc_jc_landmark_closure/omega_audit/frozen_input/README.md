# Frozen historical Omega input

This directory is the immutable input to the bounded final Omega audit. It
contains only the exact historical pair and the prior audit artifacts; no
Omega-chain, variant gadget, alternate labelling, or richer-model file is
included.

The operative machine-readable encoding is `historical/jc_omega_move.json`
(SHA-256 `c0b8f907d557d23169a2e132d7a85b789d6fa3fe03d4d90bab286eec206e960f`).
It records:

- rooted arc lists for census entries 16 and 26;
- source labels `(1,2,3,4)` and target labels `(2,1,4,3)`;
- the exact nine-variable rational correspondence;
- four strict rational common parameter points;
- all four nonzero rank-nine minors;
- the historical graph classification and root-relocation map.

The historical primary and standard-library verifiers are copied unchanged.
The prior audit's graph and algebra implementations are also frozen unchanged
for comparison. New audit code must live outside this directory.
