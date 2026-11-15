# Row 130 / record 23392409 native custody and editorial expectations

The sealed native metadata and source-custody inputs support the expectations below. This is informed metadata/custody support, not a third scientific approach family, scientific revalidation, or an assessment of an editorial draft. The unsealed owner editorial folder was not inspected.

| Item | Exact expectation |
|---|---|
| Current whole source namespace | 121 regular files, no symlinks; exactly 118 manifest payloads plus 3 declared terminal exclusions |
| Native asset array and files-entry array | `five_centers.pdf`, `five_centers.tex`, `verification-package.zip`, in that order; 3 assets |
| Separate native `files.order` field | Present empty list `[]`; it does not contain the asset sequence |
| PDF | 78594 bytes, SHA256 `50000abd0e226e014d5ecc0a04dd7ef948839cb2a6a4919b2f1e1c113e4e2bb3`, 6 pages; archived copy byte-identical |
| Standalone/controlling TeX | 15048 bytes, SHA256 `4d88d47cb2250fa91984e31ef32f58843064df9dcac5e46c7796058594693581`; archived controlling copy byte-identical |
| ZIP | 362975 bytes, SHA256 `c32415716b800aa38687d9882598ab4c8b9ae43a91e4805bc1ebfaa3572a299f`; 64 regular payload occurrences, one container, no nested archive |
| Publication date | Native string `2026-10-15`, displayed as 15 October 2026 |
| Version | **ABSENT** from native record, latest record, and sole version hit, at both top level and metadata. No default `1.0` |
| Custody representation of missing version | `version_field_present:false` with `version:null`; the `null` is a representation of native absence, not a native explicit-null version |
| Native license/access | `{"id":"cc-by-4.0"}`; `access_right:"open"` |
| Authored note and original support/code | Broad CC BY 4.0. The original instrument covers the draft and accompanying original support files; the root clearance's separate code instrument is `null`. Do not invent an MIT exception |
| Third-party works | Retain their own rights |
| Native `swh` | `{}` for record/latest; `null` for the sole versions hit. Preserve this distinction |
| Native files response | `entries` is a list; `default_preview:null`; `order:[]`; each access object is `{"hidden":false}` |

The license conclusion is the scope of the supplied original instrument and sealed root clearance. This metadata-only work does not establish a universal claim that the letters “MIT” appear nowhere or that every payload's authorship was independently proved.

All 118 sealed source-manifest payload hashes match. Every one of the 64 actual ZIP payload occurrences was independently read as opaque bytes and checked against its extracted copy, native name/order, length, SHA256, CRC32, compression fields, external attributes, create system, flags, timestamp, and archive comment. Reading bytes for custody did not entail interpreting manuscript, program, or result content. A separate read-only PDF metadata inspection reports 6 pages.

All four whole native API objects, all source custom JSON objects, original transport bodies, transport receipts, source manifest/seal/closure, original rights files, and the root clearance are preserved as byte-identical originals within ignored `private/`. This includes the root clearance's embedded original custom objects and any original historical flags. No original was reserialized, normalized, or overwritten. The derived native schema has 504 entries and exactly matches the original `NATIVE_SCHEMA_TYPES.json`, including type, order, empty-object, empty-list, null, and absence distinctions. All 8 transport bodies match their receipts; the original 301 body and ordered duplicate response-header arrays remain intact.

The current source and two current scientific verdict/seal pairs were used only for path/byte-count/SHA256 binding checks. Their scientific conclusions were not assessed here:

| Bound object | Bytes | SHA256 |
|---|---:|---|
| Root clearance | 101108 | `0cfd2378fcd36e8813b9f6fb37a9218d91037f1cc20a7ee143e736b8cfe382b6` |
| SOURCE_READY | 33082 | `388fbf673c3f14886f9da3628be04a1f7c019b0d6d1c6c936fb084d8a245d972` |
| Scope VERDICT | 6264 | `e15f9970fbfb5cf6317691fa9c07b94895aa877dd984d3b7822199bf3afc5f7a` |
| Adversarial VERDICT | 43257 | `47781112ab3e91f7bf36a0cfd7ad56b0ab4ffc3d9c817c01b84d22a52705cc4f` |
| Scope SEAL | 1755 | `a2c4d967263c44e4df3c47613cfc7b089bf479691b479a3459eb0d9c135abf49` |
| Adversarial FINAL_SEAL | 690 | `9379b6cbf2f7c01e85e712aa793f622022745f950f0ff236ec3c01937adbcd44` |

The complete absolute paths and all other bindings are in `INPUT_BINDINGS.json` and `WHOLE_SOURCE_BINDINGS.json`. `CUSTOM_OBJECT_TYPES_AND_KEYLISTS.json` records full original JSON key orders and types. The original CLOSED status/history flags, wherever present in the root's embedded objects, remain bound by the whole root byte copy; this support does not replace or promote them.

The self-authored `verify_read_only.py` uses only Python standard-library imports and performs no writes, network calls, subprocesses, project imports, or supplied/project program execution. Before support sealing, both normal and optimized modes passed all 1150 checks. The checker additionally verifies the complete support seal whenever `SEAL.json` exists. Independent literal verification and adversarial review are recorded in `PEER_METADATA_REVIEW.md`.

The research log records two harmless helper limitations: a corrected list/dictionary assumption, and a rights-only search that accidentally displayed a README scientific paragraph due to substring matching. That paragraph was not scientifically assessed or used. There were no source, owner/editorial, Sheet, site, core, Git, deployment, redirect, configuration, or contact changes and no external communication.
