# Exact failure diagnosis

The failed build compares BODY spans that differ by one trailing LF byte. Accepted article/model/HEAD/MAIN/abstract content remains exact. The whole-BODY preservation requirement is valid; this particular comparison uses incompatible representation extents.

The accepted binding descriptor covers from `<body>` through `</body>`, excluding the following LF. Saved producer line513 captures through `</body>\n`, including that LF, then line514 compares the resulting length/hash against the shorter descriptor.

| Accepted page | Binding byte span | Binding bytes | Producer byte span | Producer bytes |
| --- | --- | ---: | --- | ---: |
| Hafnian23205294 | [6890,23731) | 16841 | [6890,23732) | 16842 |
| Complex retract23203270 | [6452,23193) | 16741 | [6452,23194) | 16742 |

In both independently measured cases the producer buffer equals the binding buffer followed by exactly `0a`. Full exact SHA256 values and suffix hex are in DIAGNOSIS.json. The first actual failing iteration was hafnian. Its first length comparison is false, so Python short-circuits before the original hash and abstract comparisons. Evaluating those data comparisons independently gives hash-equality false because the extents differ, and abstract-equality true. The retract row is a passive counterfactual under the same saved comparison, not a second producer invocation or observed failure.

Both full accepted article pins, standalone wrapped heads, complete MAINs, model pins and Bib descriptors match the immutable bindings. Each model abstract equals the accepted binding abstract, ScholarlyArticle.abstract, DC.description and visible original abstract. Actual native head shapes remain one wrapped ScholarlyArticle each; hafnian encoding order ZIP→README→PDF and retract ZIP→PDF are intact. No scientific words, copy, descriptor or source object was changed. Original contract C04 and all28 criteria remain unchanged. The complete article pin also binds the LF outside the BODY descriptor; its exclusion from that narrower descriptor is not loss of article custody.

All653 actual saved producer lines and complete actual PLAN.md were personally read before diagnosis. The literal original build remains one exit1, stdout0bytes, stderr954bytes, error `Accepted whole BODY/abstract`. Both original300799-byte guards are exact SHA256bec295cc87b3d65f0bbd65c741b8893528db093771d2790a181fa07c84871982. There is no producer FINAL/OWNED_MANIFEST. The diagnostic does not convert that failed build into a successful stage.

One independently saved/full-read197-line passive data reader ran once, exit0/stderr0. The complete fresh diagnostic guard files are each771145bytes, byte-identical, SHA2562ce2b86a9408e446c7639162e945608b9a7457c8e7a2cf4d51f7b9b3eda22f8f. They protect the full source153/22, private204/13, oldINITIAL14/0, binding13/0, root controls, native M/W HEAD/index/config/local loose+packed heads, public781/377 and complete stopped producer1579files/756childdirs. The current protected dictionary also equals the frozen producer guard. Ordinary Math remote-tracking/FETCH/nonlocal packed metadata stays outside native-local claims.

Both retained baseline-public and candidate-public clones are still781files/377childdirs and whole-byte/mode/topology equal to Wpublic. All nine intended new leaves and four directories remain absent; HEAD activation, new candidate payloads, aggregate changes and terminal stage controls were not reached. Native Math maina4ce/index91b10… and Wmaster7d5/index592a… remain protected. The guessed documentation-path read error is preserved in READ_FAILURE.json; root explicitly identified PLAN.md and resumed routine local reads without any producer retry.

Diagnostic completion100%. The strongest result is the exact one-byte extent mismatch and unchanged accepted content/protected state. No producer or source/helper execution/import/AST/compiler/test, repair/retry, proposed code edit, Git/network/W/Sheet/action/outreach or other-packet mutation occurred. Future producer GO and stage/production/live/scientific/copy approval remain false. Root disposition of this evidence and any separately authorized fresh producer continuation/full later implementation audit remain distinct work.
