# Independent actual PR209 candidate03 metadata audit

Decision: **PASS actual native metadata and complete changed scope**, conditional
on Root's separate 609 native full-body checks and actual CAS/readback/sync
gates. No mandatory or optional findings remain. This report grants no Root
authority and establishes no reference update or completed PR merge.

The actual candidate is `a4ad2608cb71096514c92a2e6f38daa216565b42`, tree
`a10d2fb1f1657a95e599c99f3b64e8ace0bc4ba9`, with exactly these ordered parents:
`a687f7f4b7c374c6f29feb99b5d0e017833244e8` and
`d827ae3c46c01ff68df7fd86f26b230c0ab2ac97`. The bound manifest03 is 246659
bytes, SHA256
`153ef02f3eb7a7c701a75b7d68a6fe916fec118f0862680fc2b3da95bcfabaa6`.
Model 35600 bytes / `207f30fc102f634dddf843b0f31d9b939a5e4dbc376b8ad8eff83537236c8c14`
and executor 28678 bytes /
`f97661a3db96e9c89e141d13e16676adc55fef58b1be074dff0bcc071a99b93e`
remain unchanged from the exact packet/source review.

Fresh native metadata agrees with the manifest on exact author and committer
name, email and UTC date, ordered parents, tree and message representation.
The API again omits precisely one terminal LF from the canonical message:
267 canonical bytes / SHA256
`a61d0fa1b2a5d31f940cc132fed2ef65b623c78e604dcd3dc6ac0ab14e0f91e3`,
266 displayed bytes / SHA256
`dfd486574e3713d0dc413c2b4bd81a91170878eeb681124ccf2c681f557c3fbb`.
The reviewed pure validator records that sole normalization. I independently
reconstructed the actual canonical commit bytes using the exact bound message
and actual author/committer/tree/parents; their native SHA1 is exactly the actual
candidate. No general whitespace normalization or source adapter was used.

The actual complete native delta has exactly 381 changed leaves, 53 added
directories and zero deleted directories. Every changed leaf is precisely a
manifest-selected leaf, with its expected regular-file mode and blob identity;
every old leaf/preimage tuple agrees. The actual own attempt subtree is exactly
`7bf7c70929c0b14b5851bb33795a7bf76bf6b929`. The shared publication subtree remains
exactly `d036a7d104ffe002a7a9ac6bfd58f65c583e6526`. All foreign native tuples are
preserved by the complete delta equality.

This audit used 60 fresh, constrained metadata GETs, below cap75. It fetched no
native blob bodies. The actual MAIN lease stayed at the reviewed parent and
PR209 stayed open, ready, with the exact prepared head and unchanged reviewed
title/body at both ends of the audit. Only previously sealed immutable parent
commit metadata was reused; no MAIN or PR observation was cached. Fifty-five
complete immediate trees / 1832 entries were captured and authenticated.

For a second cross-check, a separate offline program directly encoded all
55 native trees with an independent binary serializer and used a breadth-first
delta computation instead of the reviewed recursive NativeTrees implementation.
It independently agreed on the entire 381/53/0 scope, all 381 current/preimage
tuples, the own/shared subtrees and the actual canonical commit bytes. This
cross-check made zero additional provider calls.

The obsolete candidate45d and its stopped addendum remain abandoned and
preserved. This addendum changes no prior sealed review. It does not establish
the 609 native blob bodies, actual Root CAS, genuine PR merge readback, local
five-view synchronization or completion100. I invoked no production CLI,
created no Root gate, native object or reference, changed no local five view,
and performed no publication or tracker action. Root must still complete its
separate full-body and actual-effect gates before advancing.
