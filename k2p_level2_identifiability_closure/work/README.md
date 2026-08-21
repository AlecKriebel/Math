# Direct-closure research workspace

This directory preserves the proof-discovery scripts, intermediate
certificates, and adversarial audits produced during the 36-class direct K2P
closure.  It is research provenance, not the referee entry point.

The authoritative portable replay is under

```text
../package/referee/k2p_offline_sweep_portable/
```

In particular, that package binds the final current-lock `v4` run.  Some
certificates under `work/` intentionally retain hashes from the earlier
36-unresolved `v2` run used during discovery and should not be substituted for
the release goldens.  The exact mathematical obstructions are unchanged; the
record hashes differ because the fail-closed input lock was strengthened.

The `audit_unified_closure/` subdirectory records the independent replay and
mutation campaign that found the optimized-mode and incomplete-census harness
issues.  Both issues are closed in the referee verifier.
