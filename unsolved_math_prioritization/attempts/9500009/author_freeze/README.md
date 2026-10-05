# Random-labeling peaks on the square: exact reductions and finite checks

**Problem:** 9500009 / AMR-094-0009, queue rank 777.

**Status:** partial investigation; the requested asymptotic question is unresolved.
This is an authored verification packet, not a claimed solution or a novelty claim.

The governing graph is the Cartesian product of two n-vertex paths, with its
ordinary boundary. A uniformly random bijection to {1,...,n²} is conditioned on
having exactly two local maxima. The question is whether their graph distance,
divided by n, tends to zero in distribution. The torus is a different graph.

## What is established here

- An exact subset recurrence for every prescribed pair of peaks, proved in
  `MATHEMATICS.md` and implemented without random sampling.
- Exact pair counts and distance distributions for n=2,3,4. The total numbers of
  two-peak labelings are respectively 8, 143,808, and 779,299,174,080.
- Exhaustive permutation checks for n=2,3; agreement of allowed-root subtraction,
  direct exact-root counting, and a separate total peak-count recurrence for all
  three sizes. The n=4 result is dynamic programming, not enumeration of 16!
  permutations.
- Explicit labelings and spanning-forest lower bounds for all 122 admissible
  unordered peak pairs across these three grids.
- A proved exponential upper bound on the unconditioned probability of exactly
  two peaks, and exact counterexamples to three tempting simplifications.

None of these establishes an asymptotic distance bound. Decreasing values at three
small sizes cannot settle the limit. No prior resolution was found in the sources
checked on 2026-10-05, which is a bounded search finding rather than a proof of
universal absence.

## Replay

Requires Python 3 and a C++17 compiler named g++ already installed.

    python3 code/verify.py

The verifier compiles into a temporary directory, reruns the exact counts, compares
against the saved output, checks the constructions, and prints PASS. Its default
mode does not rewrite packet files. `--write` deliberately regenerates derived
certificate files. Assertions must remain enabled when compiling the C++ source.
All values fit in unsigned 64-bit integers because every stored count is at most
16!; sizes above n=4 are not implemented.

## Packet map

- `MATHEMATICS.md`: definitions, proofs, exact results, and remaining gap
- `RESEARCH_LOG.md`: five bounded approach families and their stopping points
- `SOURCE_VERIFICATION.json`: public source and dataset verification metadata
- `code/count_peaks.cpp`, `code/verify.py`: authored reproducible code
- `results/`: authored exact counts and certificates
- `MANIFEST.json`: hashes and byte counts of the frozen payload

No source PDFs, extracts, screenshots, source records, raw datasets, private
correspondence, or coordination records are included.
