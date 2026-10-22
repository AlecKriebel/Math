# Rational VOA automorphism finiteness: audited partial results

Problem 30002842 / OWR-13673-012, queue rank 991.

**Disposition: unsolved in this packet; five substantive approaches completed.**
A June–July 2026 preprint claims the stronger inner-derivation theorem. Its current v5 was inspected, and a specific unverified limit step remains. An explicit descendant sequence satisfies the stated representative conditions, including the displayed tail-lifting operation, but contradicts the limit inference. This is an audit of that argument, not a counterexample to its theorem or to the finiteness conjecture.

Read `REPORT.md` for full proofs, exact hypotheses, the preprint audit, a completely settled tensor-Virasoro subclass, and the remaining normalization/tail-control gap. `LEDGER.json` records the chronological investigation. `SOURCES.json` records public references and source-byte fingerprints without embedding their contents. `GATE.json` describes the inherited-attempt search.

## Reproduce the checks

Use Python 3. No third-party packages or network are required.

```
python verify_packet.py
python -O verify_packet.py
python -OO verify_packet.py
python test_negative_controls.py
```

The last command runs mathematical false-claim fixtures and manifest/inventory mutations under all three optimization modes. Every check uses explicit condition-and-raise, not removable assertion statements. The manifest authenticates bytes against the fixed release fingerprint reported by the author; it is not a digital signature. A self-consistent malicious replacement of both data and manifest is outside its scope.

These checks verify exact finite algebra, descendant normalizations, spectral-filter coefficients, declared scope, and packet integrity. They do not mechanically prove a general VOA theorem, inspect fresh web content, certify novelty, establish peer review, or show the conjecture false.

All files in this packet are authored text, metadata, or reproducible checks. No PDFs, source extracts, corpus contents, queue text, chat links, or private coordination files are included. No repository or queue mutation was performed by this investigation.
