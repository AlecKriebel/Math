# Common basin boundaries: 30001370 / OWR-4132-003

**Reviewed complete answer; claimed_solved, 3/5 substantive author turns.**

For Keller's exact two-branch Möbius transfer system with feedback
G(m)=A tanh(Bm/A), 0<A≤0.4 and 6<B≤16, the basin of the constant density
is the common boundary of the two other basins in the relative L1 topology
on all probability densities. The result requires no boundedness, strict
positivity, BV regularity or prescribed convergence rate of a density.

## Read the proof

- [Exact source and prior work](SOURCE_SCOPE.md)
- [Full result and dependency summary](FINAL_RESULT.md)
- [Turn 1: open-map factorization and boundary pullback](TURN_1.md)
- [Turn 3: self-consistent backward transport and L1 approximation](TURN_3.md)
- [Independent source/proof audit](review/ADVERSARIAL_REVIEW.md)
- [Current disposition and preserved historical state](REVIEWED_STATUS.md)

Turn 2 is a separate linearized stable-subspace calculation and is not needed
for the final nonlinear proof. All three frozen author turns are retained.

The global convergence, basin openness, analytic-core boundary seed and
inverse-expansion mechanism are credited to Bardet–Keller–Zweimüller (2009).
The additional full-density argument is presented in turn 3. Historical
novelty has not been established. The independent audit is AI-assisted;
it is not journal peer review.

## Reproduce

With Python and SymPy installed, run `python verify_packet.py`. This checks
the bound public-file hashes and replays the three author programs plus
the independent standard-library verifier. To also check the locally
obtained primary PDF bytes, pass `--source-dir PATH` containing the three
files listed in SOURCE_MANIFEST.json. Sources are not redistributed here.
The report explicitly distinguishes a public-only check from a source-hash
check. Finite assertions complement the analytic proofs.
