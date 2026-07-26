# Independent v3 aggregate-verifier author validation

Status: **INCOMPLETE_1_OF_16_VERIFIED_NONCLAIM**.

The independent verifier accepted the frozen v3 run structure, rebuilt the
3,992,947-byte parent CNF without importing the production generator, derived
the four cube variables, reconstructed all 16 leaf hashes, and established the
16-assignment coverage table and all 120 pairwise cube conflicts.

It then validated the sole committed terminal leaf (`1111`) through the full
retained chain: exact v3 schemas, frozen historical source and tool bindings,
raw binary-DRAT scan, canonical additions-only normalization, normalized
binary-RUP scan, six resource reports, six child records, exact success output,
artifact inventory, certificate, outcome, and checkpoint links.

After 18 hostile fixture tests passed, one fresh `lrat-check` process was
started under the campaign-wide heavy-child lock. The verifier independently
reconstructed the leaf CNF and copied the pinned checker and bound LRAT into a
private temporary directory. It used an empty environment, observed a clean
exit, enforced the live memory/disk/load gates, and bound stdout and stderr in
the external append-only replay record.

A hostile wording review then found that the incomplete report inherited a
terminal-only claim-boundary sentence. The final verifier repairs that sentence
to state explicitly that there is no aggregate claim and exactly one of 16
leaves is validated. After the repair, one final authorized checker-only replay
created a new empty ledger bound directly to the final verifier source set
(`9ea439…`). A subsequent resume check started no child and recovered the
unchanged final record.

No CaDiCaL process was launched. Two earlier invocations stopped before child
creation: one because the requested ledger parent did not yet exist, and one
because the conservative default 6 GiB memory gate was unavailable. The
successful bounded replay used a 512 MiB child cap plus a 512 MiB reserve and
observed a 45.28125 MiB peak polled resident set in the final replay.

The result is deliberately not promoted. Fifteen partition leaves remain
pending. Even after all 16 leaves are verified and independently replayed, a
separate mathematical audit must still establish that the frozen SAT encoding
and search scope cover the intended `n=12, k=4` theorem.

Decisive hashes:

- final verifier source set: `9ea4397d1526302ca499d9c56af8a0c70ad86234b5e8eb4b9da0a9bcbfa76c46`
- final replay producer source set: `9ea4397d1526302ca499d9c56af8a0c70ad86234b5e8eb4b9da0a9bcbfa76c46`
- final replay manifest: `9039e2b6c29e972b247bfaf09c9796c048b60bb088ab3cb68d2e1541b15db644`
- final case `1111` replay record: `5ec39210e0265644432ba8ab10e7bcf7b1dc96473dd08ff9d75a7ad5e6d19120`
- reconstructed parent: `adbe0c01614bae6cd3aed4ccdcd45a757ca56e7ef9c4f2f280f2d8ef200e40ac`
- reconstructed leaf `1111`: `aafc85341993ed030fe72ba222a4efaa5a02f6ea6fa95519a9dd2ed755b94d1f`
- converted LRAT: `90787a09742237e3c38c8b4f36916b2d0ccbd37be3920feb16ddb3306ec228d0`
