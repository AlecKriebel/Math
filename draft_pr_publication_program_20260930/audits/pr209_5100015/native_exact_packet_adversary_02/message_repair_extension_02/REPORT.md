# PR209 message-repair source and exact manifest03 review

Decision: **PASS, conditional exact packet only.** No mandatory or optional
findings remain in this repaired source and reviewed packet. This assessment
grants no Root acceptance, reference action or terminal completion.

The prior manifest02 and source review remain preserved as historical evidence.
An independent actual-candidate check then stopped at the same provider
representation mismatch as Root: GitHub's commit metadata displayed 266 message
bytes, omitting exactly the terminal LF from the 267-byte canonical request.
Reconstructing the canonical raw commit from the actual author, committer,
tree, parents and exact manifest message produced the expected native SHA1
`45d77dd0d8780135182dcab3fc6ac518e9ac7564`; reconstructing it with the displayed
message alone produced `b3c02eca3fa3efcf2259f1e015cea7380b862591`. No actual
changed-scope acceptance was issued for that attempt. Its stopped records are
sealed under `candidate_addendum_01`; Root abandoned that candidate and
manifest02 before any reference update.

The repaired pure message validator accepts either the exact canonical text
or omission of exactly its final LF. It records the representation, count and
full canonical/metadata byte pins. The verifier still recomputes the exact
canonical commit identity and checks the candidate against that identity before
accepting native metadata. Exact response SHA, tree and ordered parents remain
mandatory. Explicit fixed author and committer name, email and date checks are
now present as well. No stripping of general whitespace, source adapter,
monkeypatch or weakened native identity rule was introduced.

I ran 45 new independent offline controls directly against the reviewed pure
helper and deterministic constructor. My actual metadata fixture was separately
captured before the repair; it is 1799 bytes with SHA256
`dcedc58bf8a14f436cc5bc7d2d4ce3d209dec6261e349779b9ae438bf5ad1b71`.
The controls cover exact and actual one-LF readback and the returned byte pins;
leading/trailing spaces, CR, CRLF, tabs, extra LFs, omission of multiple LFs,
internal/text changes and invalid types; canonical commit sensitivity to changed
tree, parent order, parent identity, message, author and committer; and fixed
actual identity mismatch rejection. AST comparisons prove that every other
model function is identical to the reviewed pre-repair source, that the original
deterministic-OID prefix remains intact, and that all changed-scope, full-body
and final-MAIN checks remain unchanged. The executor AST is unchanged except
for its new model pin. These complement the prior 58 independent controls;
they are not represented as a fresh rerun of those earlier controls.

The new exact packet is `ROOT_EXACT_MERGE95_MANIFEST_03.json`, 246659 bytes,
SHA256 `153ef02f3eb7a7c701a75b7d68a6fe916fec118f0862680fc2b3da95bcfabaa6`.
Model: 35600 bytes /
`207f30fc102f634dddf843b0f31d9b939a5e4dbc376b8ad8eff83537236c8c14`.
Executor: 28678 bytes /
`f97661a3db96e9c89e141d13e16676adc55fef58b1be074dff0bcc071a99b93e`.
The canonical tree core remains unchanged. The explicit source closure is
59 files / 753543 bytes; its 12686-byte manifest has SHA256
`247a829181e5fcd7d75cf75a25cbf4cc31a405b8f5afd17baffec418437d009d`.

I renewed the complete exact-packet review. All 381 selected files / 4533496
bytes match their full SHA256, byte count, native blob identity, readonly mode
and explicit native preimages. All 59 source-closure files are selected exactly;
operational scaffolds are excluded from that closure. The original 54-file
prepared attempt / 205547 bytes and 23-file original archive remain exact.
The unchanged reuse closure is still 228 files / 5435888 bytes, and every local
body was read and checked again against its SHA256 and native blob identity.
The five actual local preimages remain unchanged; their proposals agree on
case95, 50 completed, 35 published, last207, cursor209 and no advancement. Both
logs preserve their old prefixes and now disclose the stopped attempt and
narrow repair. The dated denominator99 and all prior completed/publication
memberships are preserved. Only the one own QUEUE row changes; the DOI, existing
tracker row, mathematical package and qualified priority treatment are unchanged.

Nine fresh constrained native GETs authenticated six needed immediate trees
(522 inspected entries), the unchanged ready PR title/body and the unchanged
MAIN lease before and after the read-only audit. I reused only immutable
observations already sealed under the identical native parent: the actual
parent commit metadata and the prior authenticated opaque shared-tree tuple.
The fresh request count stayed below Root's cap10. A separate canonical
serializer/rebuild again agreed with the reviewed model on exactly 381 changed
leaves, 53 added directories and zero deletions. The conditional tree is
`a10d2fb1f1657a95e599c99f3b64e8ace0bc4ba9`, with conditional commit
`a4ad2608cb71096514c92a2e6f38daa216565b42` and ordered parents
`a687f7f4b7c374c6f29feb99b5d0e017833244e8` and
`d827ae3c46c01ff68df7fd86f26b230c0ab2ac97`.

This remains a source and conditional packet assessment. It does not establish
the new actual candidate, its 609 native full bodies, a reference update,
genuine PR merge, locked five-view synchronization or completion100. Root's
fresh native candidate/body verification and separate actual CAS/readback/sync
gates remain required. I invoked no production CLI, created no Root gate,
native object or reference, changed no local five view and performed no
publication or tracker action.
