# PR209 independent native source and exact-packet audit 02

Decision: **PASS, conditional exact packet only.** No mandatory or optional
findings remain in the reviewed source and packet. This review grants no Root
acceptance, execution authority, reference update or completion status.

Reviewed packet: `ROOT_EXACT_MERGE95_MANIFEST_02.json`, 239460 bytes,
SHA256 `1b282ab9e11c5e384b8260099bbe6c039ee0a2a079d709822010b80d5c8f97ca`.
The obsolete manifest01 was not cleared or executed. The current model is
34552 bytes / `c22897967151f0ba0defe53020b262334d341686a877ea7d7b7acc58a319ad6a`;
executor 28678 bytes / `21a8faf28fcc2cd18ee24625bd703aee685ff706b39d17b84d0546e11acbe660`;
canonical read-only tree core 4719 bytes /
`c71575a580c43fea8d302c978e0b6c340a16474779ffeb4671e77b967cf6e2ce`.
The explicit source closure is 46 files, 612177 bytes, controlled by the
9977-byte source manifest with SHA256
`0dad47bbd28d997b87f3fea3d280cd9b023ec47318a5d2d9771e739b8c673112`.
Operational packet95 scaffolds are excluded from that source closure.

I independently read the entire model, executor and canonical tree core. The
operations have separate source/manifest acceptance, immutable object creation,
actual Root expected-SHA/force-false CAS, full native readback and locked local
five-view synchronization barriers. There is no reference writer in the
executor. The journal reserves one manifest-bound candidate attempt, records
the exact request and predicted object identity before each POST, stops on
uncertainty and does not retry mutations. Body and immediate-tree hashing and
the final changed-scope check prevent a native tree response from silently
changing foreign files. The narrow successful immutable-SHA GET cache is
memory-only; mutable MAIN, PR and comparison observations remain fresh.

I wrote and ran 58 independent offline controls. They verify source closure
and cross-pins; strict phase facts and type distinctions; the append-only
merge95-to-completion100 research-log sequence; duplicate, reversed, malformed,
inline and nonterminal current markers; exact four-cell changes to the one own
QUEUE row; independent canonical tree serialization; stale native preimages;
leaf/ancestor collisions; malformed immediate trees; opaque foreign executable,
symlink and submodule tuples; independent deterministic commit serialization
and merge-parent order; and immutable-cache response cloning, fresh mutable
routes and independent-instance freshness. These controls import the inert
source in separate module objects. The cache test substitutes an in-memory
fake transport and an in-memory record collector; it performs no provider or
production journal operation and creates no Root gates.

I then audited every selected byte of the final exact packet. The packet has
367 selected files, 4387521 bytes. Every file's full SHA256, byte count, native
blob identity, regular readonly source mode and explicit preimage were checked.
The prepared own attempt contains exactly 54 files / 205547 bytes. Its 23-file
original-submission archive matches the fixed original native identities.
The two naturally carried Root artifacts are the exact permitted PR207
terminal receipt and PR208 status-only skip receipt. All other changed leaves
are confined to the PR209 attempt, its new audit folder, the three program
views and the one own QUEUE row. No full tracker readback, private render cache,
private directory or journal is selected.

The five proposed views agree on case95, completed50, published35, last207,
cursor209, no advancement and an active/incomplete goal. The dated denominator99
and the full existing completion membership remain unchanged; the already
published PR209 is adopted into the publication list once. Both research logs
retain their complete actual local preimage prefixes. The current local five
preimages and their frozen copies match exactly. The prospective text explicitly
states that these facts become current after actual CAS/readback and locked
installation. The existing DOI `10.5281/zenodo.23413614`, tracker row
`'Math Puzzles'!A121:D121`, exact contemporary attribution and absence of a
priority, firstness, simultaneity or causal-independence claim are consistent.
No duplicate upload, version or tracker append is proposed.

The separate shared publication subtree remains opaque at native tree
`d036a7d104ffe002a7a9ac6bfd58f65c583e6526`. Its reference closure is exactly
228 files / 5435888 bytes, selected for reuse rather than overwrite. I read and
checked every one of those 228 local bodies against its fixed full SHA256 and
native blob identity. This local byte check does not replace the later actual
native full-body retrieval and verification required before Root accepts a
candidate or completed checkpoint.

Twelve narrowly scoped fresh native GETs authenticated MAIN, its parent/tree,
the unchanged ready PR title/body and eight required immediate native trees
(973 inspected entries). I did not traverse the full repository. The actual
MAIN lease stayed `a687f7f4b7c374c6f29feb99b5d0e017833244e8` throughout the audit.
A separate independently written tree serializer and overlay reconstruction
agreed with the reviewed model on exactly 367 changed leaves, 52 added
directories and zero deleted directories. Foreign native tuples are retained.
The conditional resulting tree is
`fb2dd942618a707e587737c5592b5b60884e9c9b`, and the deterministic conditional
commit is `45d77dd0d8780135182dcab3fc6ac518e9ac7564`, with ordered parents
`a687f7f4b7c374c6f29feb99b5d0e017833244e8` and
`d827ae3c46c01ff68df7fd86f26b230c0ab2ac97`.

This is a native operations and scope audit, not another mathematical or
priority review. The separately recorded Root scientific, publication and
whole-package clearances retain their own evidence and limits. I invoked no
production CLI, created no native objects or refs, changed no local five views,
performed no publication or tracker action and created no Root gate. Future
candidate creation/readback, actual CAS, genuine PR merge readback, locked
synchronization and completion100 remain separate required steps. This audit
must be re-evaluated if the bound source, packet, native parent or accepted
preimages change.
