# Final release engineering report

Status: **preceding commit-bound proof-release ledger; strengthened C1/C2 revision awaiting its 55-command reseal; submission metadata pending**

This report certifies the immutable snapshots named below.  It does not yet
certify the later self-contained C1/C2 strengthening in the current worktree.
That revision must complete one clean 55-command regeneration and a downstream
PDF/source/archive/referee-package reseal before a new final ledger replaces
this historical record.

The deterministic quick/full/regeneration orchestration, canonical TAR.GZ and
ZIP construction, compact verifier packaging, fixed-toolchain PDF source
reproduction, pre-DOI envelope binding, safe archive inspection, and hostile
release mutations are implemented.  Ordinary full replay does not rerun the
hour-scale probe producer; full regeneration does, behind a deliberate
one-shot confirmation.

No K3P DOI, license selection, Git tag, GitHub release, Zenodo record, journal
upload, or external communication has been created or claimed.

## Immutable-link final source reseal

The article's Data and code availability statement now resolves the exact
certificate/replay snapshot through the immutable Git tree at
`e5b0a9fc6cca79d6ab1d6cd96ceb5c4e8be5a2d5`, rather than only through the
moving repository root.  No tag or external release was required.  The final
source bytes containing that link are at exact pushed commit
`0ddf4a76f1c4cc37ac05dcb0915edcfdce65e057`.

At that commit:

- the 33-page article has SHA-256
  `e0df9b22a7db548308736a4728fd32776d5380a5b687d2620d71e3b817a199b1`;
- the unchanged 12-page reader supplement has SHA-256
  `1cd22bc542201cf60ce8eacfd3dfc8cde3e722c57046f2903a9863d2747501c2`;
- the revised availability page was rendered and visually inspected, all
  fonts remain embedded, and the TeX log has no unresolved reference or layout
  warning;
- the clean quick suite passed with payload
  `7c5f960aee698b9d027b64ae72ebe266e5a79890bf75f63af3a183091fe82a34`;
- the clean full suite passed in 205.782 seconds with payload
  `d65da00e795c4515cc390f337d83fe775c17c9a47cef68921c7b50780de827e3`,
  including fresh independent theorem replay, 18/18 integrated mutations, and
  32/32 release-engineering mutations; and
- submission validation remained `NOT_READY`, with zero structural errors,
  26 declared human/release blockers, and 12/12 validator mutations rejected.

Both packaged sources rebuilt twice and matched the committed PDFs
byte-for-byte.  Their logical reproduction payloads are
`65256d4466cd527090b1a970550aac69c0a0957a3e007b62647805f55054a541`
and
`cf9110926d5219275960418d7e9b29093a9708dbc6b784e91481e90745a28523`;
their source ZIP SHA-256 values are
`84a2c4d447782c19bd59d99962f16ba7b71dfde15ef7d3ca2386c97a6fbd1b1d`
and
`aa364e0bda4edf4a8b6ad5d662c6076ab38792b02f93bd5314bbc8c7fd8797ef`.

Canonical and independent second builds of the compact and full proof archives
were byte-identical, structurally valid, and passed extracted artifact replay.
Their SHA-256 values are
`0b6a60c8e2f7ad065f019e10a4d255b3a6cf6af4a42b1e63cdb2533233990033`
and
`101ac4f72748013542cfa66587d3edfe3a6f49fb0e9f684f3ca7f68d13f8c8d4`.

The unchanged hour-scale producer graph remains bound to its successful
one-shot execution at
`7b4cdd3197e6d650abafc263cbc8a568d09ddf9f`; it was not rerun for the
availability-link typesetting change.  As with the preceding fixed point, the
canonical archives bind the exact pre-ledger source commit above, while this
post-run report records the completed execution without recursively changing
that binding.

## Pre-link conditional-PASS minor-revision exact-commit record

The four required minor corrections were checked against the active sources
and applied: the integrated mutation count is 18; the Brits et al. comparison
now names the formal positive-definite stochastic parameter space and cites
arXiv v3; marked/unmarked bridge components are defined; and the exceptional
set \(E_N\) explicitly includes the source rank-drop closure.  The
Cummings--Hollering multigraded implicitization citation and the accepted
hand-checkability/wording polish are also present.  No mathematical producer,
verifier, active certificate, claim lock, manifest, or fileset policy changed.

At exact pushed commit
`e5b0a9fc6cca79d6ab1d6cd96ceb5c4e8be5a2d5`:

- the 33-page article has SHA-256
  `768a35bed573f10f0e989d4d6c39e27ed280871370c06da50e1ace68afb08041`;
- the 12-page reader supplement has SHA-256
  `1cd22bc542201cf60ce8eacfd3dfc8cde3e722c57046f2903a9863d2747501c2`;
- every page was rendered and visually inspected, all fonts are embedded,
  and the TeX logs have no unresolved references or layout warnings;
- the clean quick suite passed with payload
  `b684ca1a018e965271cfecd485cf3679b4d1e17bc93028b1e2328135a838d639`;
- the clean full suite passed in 212.370 seconds with payload
  `166912a36fb672f3f5ce93aef86f2f0f63fb90a9b7dd77f0fdf061a67cdfa217`,
  including fresh independent theorem replay, all 18 integrated mutations,
  and all 32 release-engineering mutations; and
- submission validation remained fail-closed at `NOT_READY`, with zero
  structural errors, 26 declared human/release blockers, and all 12 validator
  mutations rejected.

Each packaged source rebuilt the committed PDF twice and matched it
byte-for-byte.  The article and supplement logical reproduction payloads are
`01a9d8d732c5b8ce16684acbd554fc860fb1604332a46507115926fdcb3e4af5`
and
`c224972b4885d47a6899878845283e85f6f3a639604fc0d41b2afc46f444571a`;
the source ZIP SHA-256 values are
`26e5269503055d65cfb86c5517d52cd863be5878eef8f1fe3dacb2b02f0b0394`
and
`f98be392f84a40abe37f2526cf2f6a8901a4b9fcee2c01a689ad0a9ed1e66911`.

Canonical and independent second builds of the compact and full proof archives
were byte-identical, passed structural inspection, and passed extracted
artifact replay.  Their SHA-256 values are
`42fc5e9e9d4d2797c6b196683a3e7b517ee8f7c8352b7182a07d143b0f8596cf`
and
`e9a6f9f44260df8001364325ac711fceac68a2ef35c9ee141d84cc5688a9f8f9`.

The hour-scale 45-command regeneration was deliberately not rerun: its
producer/verifier/certificate graph is byte-identical to the successful
one-shot execution at
`7b4cdd3197e6d650abafc263cbc8a568d09ddf9f`.  Rerunning it for prose,
bibliography, and PDF bytes would provide no new theorem evidence.  No tag or
formal release envelope was created because submission metadata and the
human-controlled release decision remain open.

## Prior targeted mathematical-revision exact-commit execution record

The bridge-gluing and literal sunlet interfaces have been repaired and rebound
through the integrated theorem gate.  The balanced noncut-compression and
genericity arguments are now explicit.  Independent mathematical and evidence
audits report PASS, and the 32-case release-engineering mutation suite binds an
ordered 45-command regeneration fixed point.

The fixed-epoch candidate PDFs have been rebuilt and visually inspected on
every page:

- article: 33 pages, SHA-256
  `2c7dc0081edf61ec29b38cd48bb9634aa73ceac25efbef38ae62616cd1d0c14b`;
- reader supplement: 12 pages, SHA-256
  `9193b7ed726f41434f313d02d02cb106ab486bb8b2182d922b01c3a78624de20`.

At exact pushed commit
`7b4cdd3197e6d650abafc263cbc8a568d09ddf9f`, the clean quick suite passed
with payload
`63195e8437a90d7dc2a3a5c6b8d1b73d421609d97565a1f9184e0907c304a978`,
and the clean full suite passed in 200.011 seconds with payload
`508843309677738fa04f05701f7e64d53db21b63518976bb49d44bb58c5a6277`.
The single unified 45-command regeneration suite passed in 4,301.285 seconds
with payload
`a73fe870142f8c56589ce1a2efd5fdd748d1b51a178b8043244a8c991fe009d7`.
Its hour-scale probe producer was invoked once, ran for 2,937.148 seconds, and
passed; the suite reports that tracked project bytes were unchanged.

The article and supplement source archives reproduced the committed PDFs in
two independent fixed-toolchain builds each.  Their logical reproduction
payloads are
`b6344bc345d7507663b84cd571702cecdaf1a279da185a9c8196e7469049d6c6`
and
`68a657ae62d3f60fa5b6fb68e0428846d00a193ced328d2be9ed24db42683b0e`.
The source ZIP SHA-256 values are
`2d601b46cd9ef98f0b4a02d9e380dfec016624db0b904d873e8a8caf8109c69c`
and
`67c4241a2688bef99c2ed151fb6c2d3aa4100d2017a0812cf9b74e27787dbf36`.

Canonical compact and full proof archives each rebuilt byte-identically and
passed structural inspection plus an extracted artifact replay.  Their
SHA-256 values are
`1e2be0e6d1657b763ba91ad3d20dedc7a3e8df58702df33896fb225ec6f08315`
and
`28916b14083d305fece3c71cdef1be4af3f6f68708fde3fa363ed03fc834635f`.
These are exact local proof-release assets, not a GitHub/Zenodo release or a
journal submission.

`FINAL_CLAIM_LOCK.*`, `ACTIVE_MANIFEST.json`, and the sealed integrated theorem
report describe the exact pre-execution candidate snapshot and therefore still
list the machine replay/archive steps as nonmathematical gates.  They are not
rewritten after execution because doing so would change the source commit they
bind.  This report and the research/release work logs are the post-run ledger
showing that those machine gates passed at the cited candidate commit.

## Superseded pre-revision exact-commit execution record

At exact commit `6dc41043a977aeb9ea97f33576bc40aa4b63cb4c`:

- The clean quick suite passed in 0.235 seconds with payload
  `fb13f30337558a9914bedf5174e2928c0c68d6270f66ed8bd50f2dc4454226b3`.
- The clean full suite passed in 194.83 seconds with payload
  `4f8cdd082e91f841416f8b356b6fc4043bf79730c085e0ce0aa7ace64a768182`.
- Article and supplement source archives reproduced the committed PDFs twice
  under the pinned arm64 Tectonic 0.16.9 executable.  Their archive SHA-256
  values were
  `095c956b12557fdc445e6b7c9b34ae1c67d7881b26338baec92955630bc2bb13`
  and
  `e9a1a20cc130e8c79d5a6c1720c666e318b4adad2834eecc90b4b01af7b93cfb`;
  their logical reproduction payloads were
  `b13c86e8a403d2b85a8c37cd09cefe50bc80b89f1ca9ec24aa3b5c5da177b417`
  and
  `01e0c17ea7e26ce7ddad1ad691a4a1d1ff4df85be8ea82ace64982da24084725`.
- Compact and full archives each rebuilt byte-identically.  Their SHA-256
  values were
  `2b91c56823772dc45b3633a034cd349e1aa39687c734a0e1528910d1a4e5e588`
  and
  `97e8b3b3c299991a08905858c2ab80c0ee8a06540c7c24befe5bda68446f6cff`.
- The canonical 29-page article and 10-page supplement PDFs remained unchanged
  at SHA-256
  `a50cfeedaeb0c38b484f4ac01e8cca861a87a746ad20d1e43766db3bc752efae`
  and
  `4e20fe62ad4261b2ece54b87a4770a3edf30fe8807851ad48973eaec6db1110c`.

## First all-producer attempt and repair

The first 42-command attempt at that commit did **not** pass as a suite.
Commands 1--27 completed, including the fresh 204-direction cut producer, the
restoration producer/replay/mutations, and the 2,789.020802-second hour-scale
probe producer.  The probe payload was
`b6d836f1a85a11749d49fb714acef955ae0393c80d32186d957c7149a3695565`.
Command 28 then failed because the ignored parent for its independent report,
`release/work/regeneration_ephemeral/`, had not been created.  No regeneration
JSON report was emitted, and tracked project bytes were unchanged.

The suite environment now creates that parent before command execution, and a
regression control binds the invariant.  A separate diagnostic passed suffix
commands 28--37, while a static 42-command audit found no other missing output
parent.  The suffix diagnostic is not represented as a substitute for a single
unified clean run.

During report rebinding, one mutation diagnostic was also found to contain a
random temporary-directory nonce.  The stored diagnostic is now canonical,
its normalization has a regression control, and two complete 31-mutation
reports were byte-identical.  All 31 hostile cases were rejected; the repaired
pre-commit logical payload is
`631ce4b3a4152621466504950e7bf73d44142c2622b064af8cbcc38b049c24f4`.

Submission validation remains intentionally **NOT_READY** with zero structural
errors and 26 explicit blockers: 17 unresolved human/repository token classes,
six absent upload artifacts, and three draft manifest states.  Twelve targeted
submission mutations pass.  The validator rejects external, traversing,
symlinked, and wrong-type source-map inputs; journal archives must equal their
exact committed source expansion plus every manifest-bound upload byte.

## 2026-08-27 independent-referee repair closure

The complete repaired producer graph passed once from clean pushed proof
snapshot `e4b13c571eb462d7ba02e39ffd0a7b368fa5fc9f`.  Its 54 commands ran for
7,686.229 seconds, including fresh derivation of all 405,216 four-port
presentations and semantic replay of all 574,535 probe rows.  Every focused,
independent, and mutation boundary passed.

At exact pushed packaging checkpoint
`9cea20a5636dfcb4a42081afd22efbf5a27e8d99`, the final clean 14-check full
suite passed in 2,411.838 seconds with payload
`b4a8351f5b456d800f7364bc3bbbc818e343b1b24214a8804ef85172f31a2f0e`.
The integrated fresh replay, 24 classification mutations, and 32
release-engineering mutations all passed.  Peak memory was 1,918,763,008
bytes.

At that checkpoint the independently doubled compact and full archives had
SHA-256 values
`0015cd4cb3b18ffa1a1a3336548beefe087015e41a4cf62ed5cf56d23f6ef449`
and
`32abe91329b0f561b23279a46899c48d62e0d283f95b918d0f21f72fabb7a269`.
Both were byte-identical across builds, structurally valid, and passed an
extracted artifact-only binding and integrity replay; that check performs no
fresh theorem computation.  The source ZIPs reproduced the
committed PDFs twice byte-for-byte.  Both PDFs also passed independent
page-by-page visual inspection with all fonts embedded.

The neutral independent-referee handoff sealed 600 payload files and passed
two independent integrity audits.  It contains no symlink, VCS state, virtual
environment, review output, or Python cache.  Its portable plan reconstructs
the documented 53-command mathematical replay.  As a separate operational
handoff, all 35 intended TeX/Bib files were copied to the requested Google
Drive paper folder and verified byte-for-byte; this copy is not a theorem or
release-validity gate.  A stale similarly named legacy archive was moved to an ignored
quarantine so that the distribution directory presents one unambiguous
canonical full archive.

The final post-ledger export is deterministic and identifies its exact source
commit in each archive/package manifest and sidecar.  No tag, DOI, license,
GitHub/Zenodo release, external upload, or journal submission is asserted.

## Remaining gates

1. Keep the submission state fail-closed until the human author declarations,
   repository facts, journal metadata, and upload artifacts are supplied.
2. Create a human-approved exact-HEAD tag and pre-DOI envelope only after those
   blockers close.  License selection, DOI minting, and external uploads remain
   Alec's actions.
