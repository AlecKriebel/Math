# Catalog-seed stratified pilot: independent replay

Evidence category: **independently replayed computational observation**.

The preregistered 22-line pilot has exact plan, record, and output coverage.
All 22 graph artifacts were replayed with the exhaustive Python five-subset
counter and the independent C++ bitset verifier.  Every replay agrees with its
stored search record at objective `E = 2`; none is a construction.

## Results

- Exact Python replays: 22/22.
- Independent C++ bitset replays: 22/22.
- Objective split: 11 graphs have `(C5,I5) = (0,2)` and 11 have
  `(C5,I5) = (2,0)`.
- Edge-count range: 448 through 454.
- Raw graph6 uniqueness: 22/22; graph SHA-256 uniqueness: 22/22.
- Across all 231 pairs of labeled 903-edge vectors, Hamming distance has
  minimum 115, median 439, mean 435.4761904761905, and maximum 488.

Raw graph6 uniqueness and these distances are label-sensitive.  They do not
assert pairwise nonisomorphism.

## Binding hashes

- Plan:
  `f84455483c8bf00fa4c075db1554ab0eb4742084f6de135397c14dd2a79e74de`
- Production summary:
  `83e550395f8c6ba28c8ceb16114cb029dc495327c08fa3fce0215b374506b9da`
- Independent replay checker:
  `318d4100e15c5965ee1acfa373a86b753e6a08e2717ad6bdb3533ff2d745cf79`
- Exhaustive Python verifier:
  `fb8f5bee76f98a37a080970cd0548b88825f6f0f49f1144db20a3524ce5878b5`
- C++ bitset verifier:
  `2ba9e189bc56b4d7c439b26317ade8eec60589c58e294bd26d7f35f4bd631f89`
- Search binary:
  `4141c3a52e309ff5a3aff7c3022638e9f9bc902926d3939fddf9d81720662491`
- Runner:
  `69247a3a4bda68626f4fa10bc9a4432066291a94b9ee9a7a009e356e4dead10d`
- Compact verifier manifest:
  `fd9373ea9382a9c332ba0d74e45ae0cce00562215b92aa4e8af38c08c9e4757b`
- Independent replay JSON:
  `b59d0afa958f370715bbfa5379d7edac81b92cbb62e6332383f64458a887f7d9`

The compact JSON stores, for every selected line, the graph hash, stored-record
hash, and hashes of the freshly replayed Python and C++ verifier outputs.
Failure to find `E = 0` in this heuristic schedule is not nonexistence
evidence.
