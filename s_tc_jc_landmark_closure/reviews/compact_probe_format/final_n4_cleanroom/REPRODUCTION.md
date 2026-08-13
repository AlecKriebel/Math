# Deterministic reproduction

Run from a checkout containing the exact primary inputs named in the review:

```bash
bash reviews/compact_probe_format/final_n4_cleanroom/verify_quick.sh
bash reviews/compact_probe_format/final_n4_cleanroom/verify_full.sh
```

`verify_quick.sh` validates the frozen artifacts, their hashes, global path
coverage, and the 168,582-record compact/verbose binding bijection.

`verify_full.sh` regenerates all four independent shard certificates and
normalized relation streams, reruns the semantic mutation suite, invokes the
primary merger only as a black box, reruns its aggregation mutations, and
then rebuilds the final gate certificate.  The clean-room code imports no
module from `primary`.

The expected final line is a JSON object with `"status":"VERIFIED"`,
`"relations":168582`, and counts 153,072 generic polynomial separations plus
15,510 labelled isomorphisms.

The full replay is intentionally much slower than the quick validation.
