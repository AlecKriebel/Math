# Fresh independent operations03 adversarial review

**Verdict: reject operational clearance. Three material objections remain.** No live write, publication, merge, DOI assignment or ledger success was performed or asserted. The frozen scientific acceptance is unchanged. Review completion is 100% for this fixed operations03 package; overall research estimate remains 79%.

The reviewed operations manifest is `69cb677847d73ffcfe8c3dc710978e62da1bbfc3f69e1b7944d7f5411183cea7`; the separately checked source bootstrap is `6bde66dd5ad378b8c1164fee8013e5b524255f76d1f8b5f0b5f58003802ebde0`. All production helpers, the shared Zenodo implementation, both retained harnesses, bootstrap, source-anchored checker, repair report and operating policies were read before execution. No production or scientific source was changed. All new work resides in this review folder.

## F1 — bare resolver authorities with ports bypass the alias gate (material)

At `operations/collect_live.py:48`, the generic scheme branch runs before recognizing a bare known resolver authority with a port. For `doi.org:443/abc`, it removes `doi.org:` as a scheme, parses `443/abc` as authority/path and then ignores it because host `443` is not a DOI resolver. The same happens to `shortdoi.org:443/abc`, `doi.org.:443/abc`, encoded colons and explicit nested query/fragment references such as `https://ordinary.invalid/?r=shortdoi.org:443/abc`.

These are precisely official-looking unresolved resolver references for which the declared conservative policy requires review; the review does not claim that `/abc` resolves or equate arbitrary strings with a real DOI. The defect is the gate silently certifying absence rather than stopping for reconciliation.

Independent evidence:

- `NESTED_ALIAS_DIAGNOSTIC.json` identifies the precise initially failing case; the initial independent group remains **FAIL**, not rewritten into a pass.
- `PORTED_AUTHORITY_FULL_GATE_RESULTS.json` records 15 accepted complete gates: five variants in each of ledger cells, ordinary unexempt account metadata and local state. All used actual 197-account/181-ledger fixtures with both complete account enumerations and terminal empty pages. Explicit `//doi.org:443/abc` and HTTPS counterparts reject, isolating the no-scheme authority parsing fault.
- `PORT_MODE_0.json`, `PORT_MODE_1.json`, `PORT_MODE_2.json`: all 72 independently chosen no-scheme host/port/nested/encoded forms are accepted in each of ordinary, `-O`, and `-OO`, through the externally pinned loader.
- `NEAR_PUBLICATION_PORTED_ALIAS_RESULTS.json`: inserting the nested unresolved alias into either a ledger cell or unrelated account metadata **after the complete stage** permits the real production lifecycle under the memory service model to issue one publish POST and create `ZENODO_PUBLISH_VERIFIED.json`.

Required repair: recognize known bare resolver authority/port forms before generic scheme handling, including nested and bounded decoded forms; apply the same nonhome, host, port and short-alias policy. Preserve generic homes, canonical long DOI positive controls and ordinary unrelated URI paths. Do not resolve uncertainty by assuming a short name is unrelated.

## F2 — another owned record sharing the exact target concept family is ignored (material)

At `collect_live.py:180`, account leads are selected only by semantic text or exact upload MD5. Once a target exists, lines 183–185 add records whose **own numeric IDs** equal a member of the target family. They never compare the family of every other owned record with the target family, and they do not use canonical record/concept DOI references in account text as identity leads.

The independent full-gate control begins with a correctly staged synthetic target record 777, concept 778. One ordinary, unexempt owned record retains its unrelated metadata/files but has `conceptrecid="778"` and `conceptdoi="10.5281/zenodo.778"`. Its independently calculated family intersects the target family at 778. Both complete account enumerations see this unchanged record. Nevertheless, the full before-publish gate reports only the already cleared distinct WARM lead and the publication lifecycle issues one POST and writes a verified success receipt. This is an explicit same-family ambiguity, regardless of whether target native version metadata would normally make such a provider state unlikely. The policy must reject inconsistent identity evidence rather than certify it as absent.

`KNOWN_TARGET_FAMILY_SUMMARY.json` reports the result with the actual source-account identity omitted. Exact raw result and all synthetic service captures are under `private/`. A second case shows an explicit canonical target DOI in another record's references is also absent from related-account leads. Such a reference could ultimately be distinct, but should be adjudicated as a lead rather than silently omitted. No actual duplicate is claimed to exist in the live account.

Required repair: validate and compare every owned record's declared record/concept/version family against the exact target family; add unresolved intersecting records as leads that cannot be exempted as distinct from the target. Treat explicit target aliases as related evidence requiring root reconciliation. Preserve the distinction between a related lead and a proven duplicate, and test contradictions rather than assuming native/legacy projections cannot disagree.

## F3 — alias and semantic scans operate on a projection, omitting raw account fields (material)

`projection()` at lines 132–134 discards `links` and every other top-level field outside eight selected keys. Both the alias scan (177–178) and semantic lead selection (180) consume that projection. The report's promise to scan original account keys and values is therefore not implemented.

The diagnostic in `INDEPENDENT_RESULTS.json` confirms PR1131 pointers in metadata extras and file extras block, while the same pointer in a top-level extra or `links` extra is ignored. The separate near-publication control places `https://ordinary.invalid/?r=//shortdoi.org/abc` inside a raw account `links` entry. This is an already-covered explicit nested alias when passed directly to the parser; here it is never passed to the parser. Both complete account scans and publication pass, with one model POST and a verified receipt. This mechanism is independent of F1's port parsing.

The claim is bounded: the test injects a new link key; it does not assert that the live provider currently returns it. Unknown supplied account fields containing explicit unresolved identities must be scanned or rejected under the advertised policy. The current minimal record schema accepts the field and then discards it.

Required repair: run bounded string/alias/semantic validation over the original complete record's keys and values, or reject unreviewed fields before discarding them. Ensure any root exemption binds the identity-bearing evidence actually scanned; simply discovering a new raw-field lead while continuing to hash only the old projection can leave exemptions stale.

## What was independently validated

The original source-only checker was run with real network, token and process interfaces blocked **before** project loading. Complete package/proposal and preparation verification passed: frozen six release assets, 44 source payloads, 45 source ZIP members, five flat kit members, eight proposed files, original historical bytes, unchanged scientific/root review bindings, all final executable/dependency pins, three accepted final10 raw runs, 131 unchanged copied inputs per accepted mode and all 37 private custody trees. Original live `operations/runtime/` was empty. `INPUT_VALIDATION.json` records this result.

Independently written streaming code then checked **all 26** retained replay archives without extracting any archive: 337,245 members, exact closed inventories, type, regular/hardlink bodies, modes, exact nanosecond PAX mtimes and gzip CRC. It streamed 834,505,799 regular-file bytes. `ARCHIVE_VALIDATION.json` contains exact compressed archive and canonical inventory hashes. Failed06/07/08/09 evidence was not promoted; the original operations checker verifies only accepted10 as current source evidence. Historical08/09 O/OO copies remain unexecuted. The preparation's 78 full plus 63 nested group counts are retained preparation evidence, not the independent verdict.

The new separate fixture copied 131 exact files, including the complete final public closure, shared dependency, accepted scientific bindings, original account/ledger captures and seven native reference captures, with no credential files. `private/fixture/COPY_RECEIPT.json` pins those bytes. It differs intentionally from preparation input manifest `f88dc518…`: the new review executes the **final** `69cb6778…` manifest. The final executable bytes independently equal preparation's exact tested source pins, including 58,040-byte harness SHA `2188a8a033a6d63f78010899f19e6bf8894eadaf0db4a2070e70eeb0abdf45da`.

The main independent probe has ten groups: nine pass and one deliberately retained alias rejection failure exposes F1. The projection group records diagnostic observations rather than treating acceptance as safety. Additional focused falsifiers establish F2 and F3. Passing controls include exact source DOI attribution versus prefix/suffix/Unicode confusion, immediate original-title guard before description PATCH, existing record/concept/encoded ledger collisions, six final-full-gate native/concept/owner/version/metadata/DOI drifts with zero POSTs, bad-clearance rejection before any provider write, the complete numeric four-cell positive append with blank B and prior-row preservation, inconsistent native append response handling and read-only recovery, formula ambiguity and prior-row drift without blind retry, and stale Git test-parent/live-main/selected-proof conflict rejection.

All service events in these controls were memory events. The sealed preparer's service models were reused after complete source reading; test choices, new fault inputs, assertions, streaming verifier and verdict were independently authored. Network/socket/HTTP/process entry points were blocked before module load; token loading was disabled or replaced by a sentinel. No blocked real path was attempted. Every original copied input remained byte-exact at completion. The review makes no distributed atomicity, crash durability, universal duplicate absence or novelty claim.

The final family-falsifier source was replayed in three fresh namespaces after moving its raw-result destination into `private/`; all three observations reproduced. Its first raw result and initial review checkpoint seal are retained privately. `EXECUTED_REVIEW_SOURCE_PINS.json` binds every final independently authored test source; the final original-package checker runs again before the final review seal.

## Boundary and next step

The earlier operations02 repairs are materially improved and their specific title, concept DOI, numeric tab identity, native append response and readback checks survived the fresh controls. That does not close the newly demonstrated omissions. The zero-material-objection prerequisite is not met. Root should adopt or rebut these exact counterexamples, obtain separate repairs, reseal the full package and commission a new independent review. No operational clearance should be issued from this seal. The scientific freeze and scientific clearance need no reopening on this evidence.

Public review outputs contain summaries and hashes. Raw fixture copies, service bodies, synthetic clearances/intents and the unredacted owned-record test result are private, excluded by `.gitignore`, and must never be included in public Git/publication payloads.
