# Final release engineering report

Status: **Zenodo version 1.0.0 release candidate prepared for exact-commit reseal; external deposit and journal metadata pending**

This report certifies the immutable snapshots named below.  The current
version 1.0.0 release candidate changes bibliography, nonmathematical
administrative/public-release prose, licenses, citation metadata, and release
engineering only; the mathematical theorem and its active proof evidence are
unchanged.  Exact archive and handoff identities are authoritative in their
manifests so that this ledger does not recursively change the bytes it records.

The deterministic quick/full/regeneration orchestration, canonical TAR.GZ and
ZIP construction, compact verifier packaging, fixed-toolchain PDF source
reproduction, pre-DOI envelope binding, safe archive inspection, and hostile
release mutations are implemented.  Ordinary full replay does not rerun the
hour-scale probe producer; full regeneration does, behind a deliberate
one-shot confirmation.

No K3P DOI, GitHub release, Zenodo record, journal upload, or external
communication is created or claimed by this source ledger.  The direct-deposit
manifest, checksum set, and annotated tag are generated only after the final
source commit and local release gates pass.

## Direct Zenodo version 1.0.0 release policy (30 August 2026)

The first Zenodo/DOI-bearing preprint release uses a dedicated direct-Zenodo layer rather
than the journal-coupled pre-DOI envelope.  The public release changes only
bibliography, declarations, article/supplement release prose, licenses,
citation metadata, and release packaging.  It does not change a theorem,
certificate, mathematical producer, or verifier.  Consequently the reseal
reruns the quick dependency gate, both deterministic PDF source reproductions,
canonical compact/full archive construction, referee-package integrity, and
the independent Zenodo upload-set verifier, but not unchanged hour-scale
mathematical producers.

The annotated tag is `k3p-level2-identifiability-v1.0.0`.  Zenodo assigns the
DOI when the record is published; that DOI is authoritative record metadata
and is deliberately not predicted or embedded in the immutable version 1.0.0
PDF bytes.  The generated manifest and `SHA256SUMS` are the authoritative
file-level bindings.  On 30 August 2026 the author explicitly approved CC BY
4.0 for the article/supplement/documentation/certificate data, MIT for original
verifier/build code, the no-specific-funding statement, and the
no-competing-interests declaration.  Older uses below of “current,” “no release,” or
“remaining gates” are checkpoint-local historical statements about the named
commits, not descriptions of this direct-deposit policy.

## Fourth-referee localized release repair (29 August 2026)

The fresh fourth-revision report found no theorem-level defect.  Its three
release findings were accepted and repaired in their minimal dependency cone.
The integrated classification verifier's previously omitted fourth atomic
JSON writer now applies canonical mode `0644` before replacement.  The focused
control exercises all four writers on existing and new paths and rejects the
unsafe `0644`-to-`0600` fixture.

The reviewer launcher now runs package integrity before creating any excluded
runtime path.  Both the integrity checker and runner reject symlink and
wrong-type objects at `review_runs`, `runner_control`, `home`, and `tmp`.
Runtime directories are opened and created relative to held directory
descriptors with required `O_NOFOLLOW`, device/inode identity checks, and mode
`0700`; the runner lock is likewise created and removed relative to the held
real `review_runs` descriptor.  An end-to-end negative control proves that a
failed integrity preflight cannot write through a pre-existing excluded-path
symlink.  The package builder executes these focused controls on the copied
candidate and rejects any candidate containing `.venv` or `review_runs`.

The report's ledger complaint concerned the older package sealed at
`10bd695c...`, not the live ledger: the latter had already been corrected at
`14eda70d...`.  This addendum makes the replacement package self-describing.
Only the integrated verifier's 27-case mutation report, claim lock,
86-binding artifact report, active manifest, and root checksum were rebound.
All 27 attacks are rejected and the artifact-only theorem and release-input
gates pass.  No mathematical producer, twenty-child fresh replay, probe,
four-port enumeration, restoration computation, sharpness computation, or
full regeneration was rerun, because none consumes the changed report writer
or referee-runtime code.

The package builder constructs every replacement referee handoff from scratch
and rejects a candidate containing either a virtual environment or
pre-existing `review_runs`.  Historical runtime evidence is not copied back
into the manifest-excluded runtime root.  The outer package manifest records
the exact repair commit, payload bytes and modes, canonical proof-archive
hash, and source-reproduction evidence.

### Manifest-bound clean handoff

The exact repair/package snapshot is
`c0894b85a1a6faf08d13bc17f7586de0223081f6`.  Its compact ZIP has SHA-256
`2b540975bbc9136a90ffb46c5f4c8cf442a87804e914fff6745084f928d21a9a`
(385 members; 383 selected files), and its full TAR.GZ has SHA-256
`7501c52166e7ddcddf5c1a5e60105ba308e84e31f23432c36b5c3328b419b2c5`
(598 members; 594 selected files).  Both unchanged PDFs reproduce
byte-for-byte twice under the declared cached-only build contract; the article
and supplement report SHA-256 values are
`9795b16a2ed562839ae160f11b3c4ce713233aa6f57c5443e9afff5805a948a6`
and `5cf36cbbef4d29b2dcc45be3161cec603045d5ab83c231cbebccdb3ca369bbed`.

The clean referee handoff is
`~/Documents/Math/k3p_level2_fifth_revision_referee_2026-08-29`.  It seals 635
payload files totaling 161,143,650 bytes.  Its package-manifest SHA-256 is
`97cdf689b27d443179ab03dd4b18022cd8ded9f4a38c5514f69eab35e797d10b`,
and its outer-checksum SHA-256 is
`820380cf7ab9d476723240c6b86df3e27d5e2bcb30042833d7ee69ac802c1aae`.
Independent integrity replay passes 597 core rows plus the bound source
reports, transcripts, source ZIPs, byte counts, and modes.  The delivered
folder contains no symlinks, virtual environment, or pre-existing
`review_runs` directory.

This paragraph is a post-build record of the manifest-bound handoff.  It does
not recursively alter that already sealed package; the outer manifest and
checksum file inside the handoff are the authoritative package identities.
No unchanged long producer was rerun.

## Historical third-referee repair and exact-once acceptance run (29 August 2026)

All four third-referee findings were repaired without changing a theorem
statement.  Atomic JSON replacement now preserves canonical file modes and is
covered by a focused unsafe-mode rejection test.  The directed-cut evidence
binds an exact typed nine-row implication object in independent direct and
adversarial verifiers, binds custom evidence to the theorem certificate, and
is freshly executed by the outer release gate.  Stale counts and version
language were corrected.  PDF source reproduction now uses a pinned Tectonic
0.16.9 executable, an exact 725-file cache manifest, `--only-cached`, a
minimal non-inherited environment, and sealed final reports and transcripts.

The repaired proof and referee-package snapshot is
`10bd695cc7b7e0fd98a187026059b043589244f0`.  Its release selection contains
594 full files and 383 compact files, with selection SHA-256 values
`4d0686fc43bc53bb76d61d056f78f72f9da585e743ae386016fc7d64ba12e67a`
and
`835971a4858334085b4a1d352190038306909751075e518333e9acd0bade77a0`.
The release-engineering suite rejects all 37 mutations and passes all 12
controls; its payload is
`e8d8fa6769c57d27fb636a1e8fef6038b1c01a6167b935e9f6ebfdd1452cca35`.

The current 38-page article and 14-page supplement have SHA-256 values
`3d08a722ba1fa53f6e336ab285c1cd32d1307bac08e1d4dd2460da71df1816d6`
and
`96508f4b4eddb89de99881172abee307b3fe86d236f48e17508bdd1ca9c30efa`.
Every page was visually inspected, all fonts are embedded, and the source
ZIPs reproduce the delivered PDFs twice under the closed build contract.  The
article and supplement source ZIP SHA-256 values are
`25a5730c31cdeffba4158203307a1be2d583e56e9cac5b0cc9922f8899ff3dba`
and
`34441c556277f152c96b88f2165afa450f905e1d7563aeeeb2115bd70148d5be`;
their logical reproduction payloads are
`d404ad7b99cd4b75386c97aa4fd6d700eba53f1eee8c4039b1b843afa539cd4f`
and
`9431b8d933ec9a236c30dd288f5bbbdbe21f6710e1746bd313192d1fe77c423e`.

The canonical full TAR.GZ and compact ZIP have SHA-256 values
`fecb2eda22bcb0558c02e14fdb7767b4229bde33471a4de2a764191f42d8d293`
and
`51e54e2d4eed0d7e980fccbd0319d79e83633a4fad9308c4ed79198112edc014`.
The neutral referee package seals 635 payload files totaling 161,122,700
bytes; its manifest SHA-256 is
`c67c1c524ef59217a2327e7dd4016cd82a9b8be1e8f188e6cc61a4fe1fd6c725`.

After sealing, the portable runner's `all` mode was launched exactly once
inside an externally imposed, credential-free macOS sandbox.  It passed 4/4
verification commands in 3,016.565 seconds and 55/55 regeneration commands in
8,584.394 seconds, for 11,608.930 seconds total.  The hour-scale probe producer
ran exactly once, in 2,886.752 seconds.  Package and virtual-environment
inventories were unchanged; both phases reported zero undeclared workspace
drift.  The runner summary SHA-256 is
`8aca186fe28786e61d7c25798fecf255b43dcaf9cfd0dc0035802757bc5f0db8`,
and the external supervisor summary SHA-256 is
`afafe7d2504a0937028ec021030ad01dea059fcc932d5f6aa8db7941366c18be`.
The successful run and its transcripts are copied outside the seal into
`~/Documents/Math/k3p_level2_fourth_revision_referee_final_2026-08-29/review_runs/`.
The final copied folder passes its Git-independent integrity checker, and its
sealed payload is byte-for-byte identical to the canonical package.

During the long run, the shared monorepository advanced to
`b49913ad5fc3404933fcedecbf36f1040f1c7f2d` through an unrelated sibling K2P
commit.  No K3P file changed.  The K3P artifacts intentionally remain bound to
the exact `10bd695c...` snapshot; rebuilding them against an unrelated later
monorepo commit would add no K3P evidence and would destroy that clean
execution boundary.

## Historical targeted second-referee repair (29 August 2026)

The current mathematical repair is the direct K3P cut-transfer certificate at
exact pushed proof snapshot
`3710f2a24851bac2a4aee124fc2c5debb5b7c1c5`.  It replaces the stale
load-bearing JC/global-logic premise with the displayed-tree minor argument,
the 808,642-word balanced reduction, and the 379,742-presentation
zero-survivor switching replay.  The active dependency graph now has 15 nodes;
the direct and adversarial K3P cut-transfer suites reject all 39 and 35
declared mutations, respectively, and the active claim-boundary suite rejects
all 16 mutations.  The downstream artifact-only theorem gate passes with 86
bindings, and its integrated mutation suite rejects all 27 attacks.

The referee runner and distribution layer were then hardened through exact
pushed implementation/source snapshot
`825fd0bc4c6e9ba183c54e0800d76be2e93b892d`.  The runner now uses a fixed
clean child environment, an atomic single-run lock, process-group cleanup,
complete workspace and virtual-environment inventories, mode-aware sealing,
and an explicit external-sandbox attestation.  It does not claim to enforce
host or network isolation itself.  The release-engineering suite rejects all
32 mutations.  Safe ZIP and TAR extraction applies the already verified file
modes, closing the discrepancy discovered during the final package replay.

At that pre-ledger snapshot, the current article and reader supplement have 38
and 14 pages and SHA-256 values
`5fd4fb902ee72c619c75846e2e5f561b018b4096a659b895063c0758dfc5d9df`
and
`e82d1afb01f937872ec06ee1b1529fe736362c3496721b99813d8849ff7327e6`.
Both were rendered and inspected, have embedded fonts, and reproduce
byte-for-byte from their packaged sources.  The current full and compact
archive selections contain 592 and 383 tracked files, respectively.  The
dated third-revision referee handoff contains 624 sealed payload files and
passes independent byte, mode, inventory, and extracted-artifact checks.

In accordance with the user's runtime constraint, the unchanged multi-hour
producer graph was not rerun after the cut-transfer repair.  Only the changed
cut-transfer dependency cone, its downstream theorem and mutation gates, and
the affected source/distribution checks were rerun.  The last complete
multi-hour execution remains the successful 55-command regeneration at
`203e114ace0ead3852f109a3713acda37bf74e65`; the present package includes that
historical transcript and separately discloses this execution boundary.  This
is a limitation of the post-repair execution record, not a claim that the
unchanged long producers were freshly executed.

The canonical archive manifests and the outer referee-package manifest, rather
than this self-referential ledger, bind the exact Git commit containing this
report and the final archive hashes.  The older sections below are retained as
dated historical execution records; their former package paths and hashes must
not be used as identifiers for the current handoff.

## Historical self-contained referee-repair distribution (27 August 2026)

The corrected 38-page article and 14-page reader supplement are pushed at
exact source snapshot `5a6d64cb2a76e890d7baaef3ba5ac9861c1d029f`.  Their SHA-256
values are, respectively,
`2a5c71feaadb0056cd738f6344eca2eb5ee09784ba542070238cc476b141b8db`
and
`a1b349bf2ffbdbd290ca2254159dc1304ef299bdbbf8792e7340526d60e985e8`.
Every page was rendered and inspected, all fonts are embedded, and neither PDF
contains the retired internal outcome wording.

Both source packages rebuilt twice and matched those PDFs byte-for-byte.  The
article and supplement logical reproduction payloads are
`655417765a511a80024794e99ebdceaf682321f06c76c4cb0cbdf9d4435fb7bb`
and
`40ec5ba42ce2b5f01598fd79e936bfc39f47504a95892affa1cea8d9fa5c5614`;
their source ZIP SHA-256 values are
`98a23fac8fee67510ad53f435ed17ecaae983a122bb0d8baa2b6b48c236d81f5`
and
`0e26f9b3ae11fad49643776509db9e254c8cbfb16f1714d5c575d48711badec5`.

Canonical and independent second builds of the compact and full proof archives
are byte-identical, structurally valid, and pass extracted artifact-only
binding/integrity replay.  Their SHA-256 values are
`3cdf9abb59dfdc86e1e95593e7d8aac02802c277b414c931229b57fc22957d0d`
and
`6fe6ed56e6c5252fdb269655ec508913c4bd5076448e598fd6141d1b913bc101`.
The latter contains 594 archive members and identifies the exact source
snapshot above.

The rebuilt neutral referee handoff contains 622 sealed payload files totaling
160,506,893 bytes.  Its outer manifest has SHA-256
`090741f2cf6aa05ee5d9d65528e66980bb6eefd32c7cd25d49c8906fda83c1d0`,
binds the same source snapshot and full-archive hash, passes independent
integrity checking, and reconstructs the intended 54-command portable
mathematical regeneration plan without execution.  A convenient copied folder
is at `~/Documents/Math/k3p_level2_independent_referee_2026-08-27`; the
canonical build remains under `release/dist/`.

All 35 tracked TeX/Bib source paths were copied, not moved, to the requested
Google Drive `Papers/K3P Level-2 Identifiability` folder.  The destination has
exactly those 35 files, zero missing/extra/mismatched paths, and logical source
set SHA-256
`cfb41635857a578bbea8c43c4726eccf4fe647f2db382364f5b843f5270e7e4e`.
This operational copy is not theorem evidence.

The post-typesetting quick suite at the same source snapshot passed with
payload
`0f6f9537884e8265ba80ae816acb2fe33118b1d8a3c984dc1a0c9fab4df85bd8`.
The full proof and one-shot regeneration evidence remains the exact execution
at proof snapshot `203e114ace0ead3852f109a3713acda37bf74e65` recorded immediately
below; no long producer was rerun merely for typesetting or packaging.
Submission validation remains deliberately `NOT_READY`, with zero structural
errors and 26 human/administrative or upload blockers.

## Strengthened referee-repair proof fixed point

At exact pushed proof snapshot
`203e114ace0ead3852f109a3713acda37bf74e65`, the graph-only non-four anchor
derivation, the exhaustive raw four-port descendant crosswalk, and the
self-contained balanced noncut/displayed-tree cut argument are active and
fully bound.  The portable non-four mutation report excludes runtime,
traceback, path, and temporary compressed-byte data from its logical payload;
all 16 attacks pass their declared rejection checks.

The clean quick suite passed with payload
`0a2394d3cc9529c29c9e21a7b602f1793c9b13da0a437939639ece7ebb411cf0`.
The clean full suite passed in 2,991.443 seconds with payload
`afdceb98352ff9d7446e8787b8508c07b0bf10e9cd497d74f282120b4b49736d`,
including the 20-child fresh integrated replay, 27/27 classification
mutations, and 32/32 release-engineering mutations.

The explicitly confirmed 55-command regeneration ran exactly once and passed
in 8,920.970 seconds with payload
`74ab3e8830f4e0a8e8e1805c9aca591a4ec09d78a160126c183d496db3d6f019`.
The hour-scale probe producer was invoked once and passed in 2,971.512 seconds.
The run regenerated all canonical artifacts, reported zero tracked drift, and
ended with fresh integrated replay plus both mutation gates.

The corrected fixed-epoch article and reader supplement now have 38 and 14
pages, respectively.  Every page has been rendered and inspected, all fonts
are embedded, and the article availability statement points to the exact proof
snapshot above.  Their later commit-bound source reproduction and distribution
hashes are recorded in the final distribution section above.

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

1. Complete the exact-commit direct-Zenodo reseal, push the annotated tag, and
   verify the generated public manifest and upload checksums.
2. Alec must create and publish the external Zenodo record, then download and
   compare every deposited asset before recording the issued DOI.
3. Keep journal packages fail-closed until the separate journal-specific
   metadata and upload artifacts are supplied.  A public preprint release does
   not by itself claim journal submission or human peer review.
