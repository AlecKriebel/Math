# Integral Skyline Bases: partial theorem and verification

Problem: 30001525 / OWR-4413-009.

Status: **partial progress; unrestricted conjecture unresolved**. Five mathematical approaches were pursued. No claim of novelty is made.

## Results

- A proof of the requested additive cyclic-basis property for S_n for every n<=7, in every cohomological degree.
- For S8, an explicit single-skyline source family whose third integral Bocksteins have exact order 8 in every positive degree divisible by 8.
- An artificial free-complex counterexample to the generic preferred-basis shortcut, explaining why abstract Smith normal form alone does not solve the actual conjecture. This is not a symmetric-group counterexample.

Read `PROOF.md` for full hypotheses, constructions, proofs, citations and remaining obstruction. `TURN_LEDGER.json` records the actual sequence of mathematical approaches, including failed generalizations and the replaced S8 candidate. Source lookup, literature review, checking and packaging are not counted as approaches.

## Verification

Run `python3 verify.py`. It uses only the standard library and reproduces `TEST_RESULTS.json`. The checks include exact S4 algebra through degree 80 and all C8 Mackey cosets. The script does not claim to compute integral Fox-Neuwirth cochains or test arbitrary symmetric groups.

`SOURCE_METADATA.json` records public titles, source URLs, byte hashes, inspection scope and dated literature limitations. No downloaded papers, source text, datasets, private source-gate material or private coordination records are in this packet. `MANIFEST.json` freezes the listed public-packet files and excludes itself from the per-file list to avoid self-reference.
