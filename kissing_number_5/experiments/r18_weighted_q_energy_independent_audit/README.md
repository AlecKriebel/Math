# Independent audit: the \(r=18\) weighted \(q\)-energy argument

This folder independently audits equations (12)--(15) of
`proofs/antipodal_deep_graph_coupling.md` and the immediate deep-edge
corollary.  It does not modify or import the production verifier.

Run:

```bash
python3 experiments/r18_weighted_q_energy_independent_audit/verify_independent.py
python3 -m unittest experiments.r18_weighted_q_energy_independent_audit.test_independent
shasum -a 256 -c experiments/r18_weighted_q_energy_independent_audit/MANIFEST.sha256
shasum -a 256 -c experiments/r18_weighted_q_energy_independent_audit/AUDITED_SOURCES.sha256
```

The audit covers:

- ordered versus unordered pair factors;
- why one representative from each antipodal pair is safe;
- the sign of \(q\) on the entire closed interval
  \([-1/2,1/2]\);
- exact optimization of the common representative weight;
- the arbitrary nonnegative residual-weight identity;
- zero weights and equality-boundary cases;
- the exact threshold forced on at least one residual cycle edge.

The mathematical conclusion is that equations (12)--(15) are correct.
The production verifier's arithmetic checks are correct but do not by
themselves certify the interval-sign argument or derive equation (15);
the independent checker fills those coverage gaps.

`AUDITED_SOURCES.sha256` pins the exact shared proof, certificate,
production verifier, and production test that were audited.  A later
intentional edit to one of those files requires updating the snapshot
only after re-running this audit.
