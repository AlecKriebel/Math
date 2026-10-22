# Kirby Problem 4.64 / catalogue 2940

**Unsolved, five substantive approaches.** The result is a credited obstruction-and-reduction packet, not an irreducible example and not an impossibility theorem.

- `PROOF.md`: full scoped arguments, invariant conventions, five approaches, and exact remaining gaps.
- `SOURCE_GATE.md`: primary-source locations, version boundaries, and literature-search limitations.
- `ATTEMPT_LOG.md`: mechanism and outcome for each substantive attempt.
- `verify.py` and `verification.json`: deterministic, standard-library-only finite arithmetic checks.
- `STATUS.json`: machine-readable claim boundary.
- `MANIFEST.json`: SHA-256 bindings for the other seven public files.

The strongest sufficient criterion is credited to Furuta–Kametani–Minami: an irreducible **spin** rational-cohomology K3#K3 would solve the problem. Its ordinary BF nonvanishing is known; all ordinary SW invariants vanish by parity. No irreducible realization is provided. The attractive −2-sphere gluing of two standard K3s is excluded because every ordinary BF class vanishes.

Run from this folder:

```sh
python3 verify.py > replay.json
cmp replay.json verification.json
```

The checks verify finite arithmetic controls and consistency of two published low-dimensional group formulas. They do not prove the cited gauge-theory theorems, compute an invariant of an unknown manifold, or test irreducibility. Full mathematical arguments and external theorem dependencies are in the proof and source gate.

The packet has not yet passed a separate adversarial review at author freeze. No novelty or external human peer-review certification is claimed. Full source PDFs and extracts are not part of this distributable packet.
