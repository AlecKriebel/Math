# Final n=3 compact-probe clean-room reproduction

All commands run from the repository root. The full replay is intentionally
sequential because simultaneous semantic shard audits are unsafe on the 16 GB
M1 host.

```bash
bash reviews/compact_probe_format/final_n3_cleanroom/verify_quick.sh
bash reviews/compact_probe_format/final_n3_cleanroom/verify_full.sh
```

`verify_quick.sh` replays the localized witness-normalization discrepancy,
all semantic mutations, all merger mutations, the global binding bijection,
and the final certificate using the already generated independent shard
certificates.

`verify_full.sh` first regenerates the four independent shard certificates in
the strict order `s0`, `s1`, `s2`, `s3`; it then runs every quick gate and
rebuilds the manifest. It never launches two shard audits concurrently.

The independent implementation imports no module under `primary`. It reuses
the committed n=4 clean-room graph/Fourier engine from commit `35c0116d`, adds
an independently implemented ordinary-triangle quotient and exact sign proof,
and reads the invariant templates only as frozen mathematical input data.

Expected final totals:

- 144 exact base paths;
- 101,148 exact directed relations;
- 90,008 generic polynomial separations;
- 9,676 labelled isomorphisms;
- 840 ordinary triangle redirections;
- 624 strict open-cube separations;
- 56 relations where compact and verbose select different, independently
  valid strict witnesses.

The final status is `VERIFIED_AFTER_CORRECTION`: lossless equality of selected
witness bodies is false, while relation-level semantic equivalence is verified.
