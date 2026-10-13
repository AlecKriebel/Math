# PR411 administration append receipt serialization repair (V4)

This offline successor preserves the accepted V3 package and fixes only its append receipt guard. The actual publication producer hashes pretty JSON (`sort_keys=True`, `indent=2`, `ensure_ascii=False`) with one trailing newline. V3 used compact JSON for this expected hash and safely stopped the actual integration plan before mutations. V4 uses the producer representation only at this guard. The global compact plan/approval encoder remains unchanged. Payload equality now compares typed canonical JSON to the exact four pinned cells.

The original actual append intent, raw GWS stdout, parsed response, returned range, exact target, integer counts, native header/row GETs, publication joins and freshness deadline remain required. The action, science pin, main descendant, known acknowledgment recovery, exclusive journal, no retry and separate phase approval mechanisms are unchanged. GitHub ref update lacks an expected-old-SHA CAS; the existing helper states this limitation and requires the surrounding gates. This repair grants no live phase approval.

`TEST_RESULTS.json` replays authentic archived administration JSON with explicit virtual asset SHA256/MD5/length objects and an archived-window clock. It executes no asset byte verification, fresh native GET, science reading, integration plan or mutation. The positive result certifies only that receipt joins accept the archived actual shape under those test doubles. Every later live plan must receive genuinely fresh receipts and root-approved inputs.

Narrow replay, using a new nonexistent output directory:

```sh
python3 -B append_receipt_replay.py --case /absolute/path/to/pr411_6800014 --private-dir /absolute/path/to/new-private-replay
python3 -B -O append_receipt_replay.py --case /absolute/path/to/pr411_6800014 --private-dir /absolute/path/to/another-new-private-replay
```

The replay requires the privately held pinned original administration receipts. The sealed public component contains no raw receipts, scientific package, assets, fixture trees or credentials. Obtain the final seal SHA256 independently, then run:

```sh
python3 -B verify_custody.py --expected-seal-sha256 ACTUAL_EXTERNAL_SHA256
```

The positive whitelist excludes itself and the seal to avoid a hash cycle. The seal binds the whitelist; an external actual seal digest anchors custody. The unchanged native phase CLI is documented by the preserved V3 package and is reserved to root after explicit phase approval.
