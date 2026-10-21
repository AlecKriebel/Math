# Packaging validation record

This is a reproducibility/integrity check, not a new mathematical proof or an independent package acceptance.

The numerical script is derived from the mathematically accepted script by replacing all four Python Assert AST nodes with explicit `if not TEST: raise AssertionError()` guards, leaving their complete tests and the rest of the AST unchanged. The generated file was parsed again and its entire AST compared with that exact transformation of the accepted original. This avoids optimizing the guards away under `python -O`; it does not strengthen numerical examples into proof.

The complete numerical output is replayed against sanity_results.json. Five mathematical mutations deliberately corrupt EP reconstruction, the Frobenius tail inequality, candidate diameter, convection skew symmetry, and the PDE bound. Each is rejected by an explicit guard. Each of the four guard conditions is also independently forced to failure. Both ordinary and optimized Python are exercised.

Fourteen integrity controls alter, omit, or add files; add nested files and a nested manifest; add file/directory/manifest symlinks; insert traversal, absolute, backslash, and dot paths; duplicate an inventory entry; and attempt to list the root manifest itself. Every control is rejected in both Python modes. Full machine-readable control outcomes are in mutation_results.json (48 passing controls, including two full numerical-output replays).

The recursive manifest does not authenticate itself. Its hash must be anchored outside this package. No script here validates a mathematical theorem merely by finding its wording or by matching a hash. Mathematical justification is in the authored proofs and the separate stopping-time and structural reviews.

Editorial changes to accepted prose remove checkpoint/coordination language, update one local relative link, and state UNSOLVED status. No mathematical statements, proof steps, hypotheses, or constants were changed. mathematical_acceptance.md explicitly distinguishes its original manuscript binding from this editorial derivative. An independent audit of this complete package is a separate required step before treating it as publication-accepted.
