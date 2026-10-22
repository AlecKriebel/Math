# Reading and reproducing this verification package

The accompanying five-page note proves the full historical OWR2017/42 Question1 by explicitly composing earlier theorems. Read `manuscript/main.tex` with the published PDF. The result includes periodic matrices and nonouter/nonfaithful actions. Its implementing sequences are fixed by the entire original action; no approximate group law is claimed. This is attributed exposition and verification, with no firstness or present-openness claim.

`original_submitted/` preserves all nine captured Git files. `current_edition/` contains the explicitly qualified edition: the sufficient original return-corner proof remains valid, an unnecessary necessity assertion is qualified, and prior mechanisms and historical/current evidence boundaries are made explicit. `provenance/CURRENT_EDITION_CORRECTION.json` binds both editions and the six documentary changes. It does not authenticate missing older proof/program/input bytes.

`provenance/MATH_GATE.json` and `provenance/PRIORITY_ADJUDICATION.json` state the current, limited conclusions. Authored mathematical and priority reports are under `reviews/` and `priority/`. Each explicitly registered family manifest binds only its declared relative authored members. Source inventories, absolute input/deployment paths and search-result receipts are not promises that third-party bodies are redistributed. Those bodies, extracts, page images and raw provider responses are omitted.

## Portable checks

Use Python3 with its standard library. From the extracted archive directory run:

```
python3 -B verify.py --expected-manifest-sha256 MANIFEST_SHA256 --expected-context-sha256 CONTEXT_SHA256 --expected-snapshot-sha256 SNAPSHOT_SHA256
```

Replace the three capitalized values with `verification_anchors.manifest`, `.context` and `.snapshot` from the independently obtained published repository `publication/BUILD_RECEIPT.json`. That receipt also gives the archive and PDF hashes. Compare the downloaded archive against its independently obtained hash before extracting. Computing every expected hash solely from the same untrusted archive is a consistency check, not independent authentication. The public Zenodo record supplies artifact checksums; the reviewed repository receipt supplies SHA256 anchors.

The verifier checks exact archive membership, both nine-file editions, explicitly registered family members, current gate/context/source bindings and six durable finite diagnostic programs. It copies each program into temporary space and runs it in normal, `-O` and `-OO` modes. It leaves the package unchanged. An integrity failure, failed explicit predicate, diagnostic mismatch or process timeout fails the run. Standard-library diagnostics need no network or credentials.

The finite programs check graph/character identities, normalized kernels, explicit finite frames and cocycle boundary examples. They do not prove operator-algebra approximation limits or replace the written proofs and imported theorems. Some preserved historical programs contain assertions, timestamps or original-directory writes; they are not the current automatic replay targets. Detached durable revisions preserve their mathematical checks using explicit validators and isolated stdout results. Historical aggregate counts without their old program/input bytes were not replayed.

The manuscript is reproducible from its LaTeX source with a suitable TeX installation; the build used the compiler/version recorded in `provenance/COMPILE_RECEIPT.json`. Exact PDF bytes also depend on that compiler, cache and environment. The chosen build timestamp is distinct from actual review/publication dates. `provenance/LAYOUT_VERIFICATION.json` records actual inspection of every page.

AI tools were used extensively throughout reasoning, source auditing, diagnostics, writing and internal adversarial review. This work is unrefereed and has no claimed external human peer review or formal proof-assistant certification. Byte hashes and finite tests establish only their stated consistency properties.
