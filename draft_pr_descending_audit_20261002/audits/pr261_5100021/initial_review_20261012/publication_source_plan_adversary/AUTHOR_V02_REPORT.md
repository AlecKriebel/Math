# Exact AUTHOR v02 source and plan audit

The repaired source and concrete AUTHOR v02 graph passed independent verification.
An exact GO decision is recorded in `AUTHOR_V02_GO.json`. This report
does not approve TITLE_BODY, MAIN, replay, recovery, or a source-only operation.

The original AUTHOR v01 operation is HOLD. Its explicit file deletions emptied
the current `independent_review` directory, but the original publisher would
create/read an empty provider tree. The fresh repaired source omits that selected
empty directory from its parent and records the omission explicitly. It forbids
an empty repository root and skips empty-tree POST/GET. All other selected bytes
are identical. [GitHub's tree documentation](https://docs.github.com/en/rest/git/trees)
does not promise creation of an empty tree; the [primary WaterButler provider
implementation](https://github.com/CenterForOpenScience/waterbutler/blob/develop/waterbutler/providers/github/provider.py)
records the concrete 422 empty-tree failure. The repair avoids depending on that
unsupported operation.

Reviewed source is 36,358 bytes, SHA256
`ec8caa65269272d1f965779b7fe8f214a241e5291a9023a2778fdae387591788`.
Exact PLAN is 109,287 bytes, SHA256
`f1a4347056d3df1be687db91cb70e3b249094cb74ac0bf8624344054b1e2d801`;
INPUT is 26,422 bytes, SHA256
`b7427c2997834c8c47642bf54b2e0564e31e3c2b4103eab7079ece79caad944e`.

Independent reconstruction used only captured provider data and local frozen
bytes. Nine clean GET requests yield 36 complete capture files. Provider ref,
PR261 identity, open/draft/unmerged state, exact author head/title/body and both
repository identities match the plan. The baseline commit's full native object
hash is independently verified, accounting for its original `-0700` timezone.
Every captured direct tree also reconstructs to its native object ID.

All 53 operations equal the finalized packet change map: 52 target-attempt
operations plus the generated QUEUE replacement. All 41 after-packet native blob
IDs equal the finalized candidate, and all 25 historical originals are preserved
byte-for-byte. The complete historical attempt tree is precisely the old native
attempt tree. Every unselected direct entry and foreign subtree is retained.
The complete original author QUEUE is authenticated and differs only at one row's
status and assessment; the original `1/5` and PR261 link remain unchanged.

The full new canonical commit is 282 bytes with no terminal LF. Its parent is
`7b7fcd63d5ea83df3a4c29853c4ba34b93d16f07`, tree is
`1c03470f74bab2855867eb3453faf57571618bf4`, and commit is
`5758b55f8b5ddfd224517ccf7f92ac7f982e6417`. Six nonempty trees require creation;
the seventh tree record is an explicit omission of the selected-empty current
review directory.

Source guards require exact independent and Root source/input/plan pins,
reconstruct the graph before writes and before CAS, create `actual/` exclusively
before the first request, and do not retry on failure. There is exactly one
expected-old, nonforce `updateRefs` operation, bound to
`refs/heads/dot/math-5100021`. Every created blob/tree and full canonical commit is
read back; fresh ref and complete PR guards precede CAS, and ref/PR/root/full
commit postreads precede completion. No local Git/index/ref, native merge/close/
ready, paper, DOI, tracker, or individual-communication operation exists in this
AUTHOR call path. Fixed provider binary availability has been observed in the
successful GET preparation; outer exit/error capture must still be retained for
exceptional launch failures.

Root supplied the concrete AUTHOR-only window and then the authorized original
peer's fresh acknowledgement: read-only Main observation at
2026-10-12T10:54:34Z, no shared/local/Main writes since its earlier window return,
and continued read-only work while Root holds this bounded PR261 window. This
asserts exclusivity between the two coordinated chats and no control of unrelated
writers. Expected-old CAS and immediate complete PR guards still apply. The GO
approves only the exact AUTHOR plan for one Root-approved execution; it confers no
TITLE_BODY or MAIN authority. Root must independently accept actual captures
before claiming publication, and any consumed stage cannot be replayed.

Evidence: `AUTHOR_V02_GRAPH_CHECKS.json`, `check_author_plan.py`,
`SOURCE_CONTROLS.json`, `SOURCE_REPAIR_CONTROLS.json`, and
`ORIGINAL_AUTHOR_RECONSTRUCTED.raw`. This reviewer made no real provider request,
network write, or local Git action. Scientific proof/priority adjudication is
Root's separately reviewed packet decision; this review binds those exact packet
bytes to the bounded publication operation.
