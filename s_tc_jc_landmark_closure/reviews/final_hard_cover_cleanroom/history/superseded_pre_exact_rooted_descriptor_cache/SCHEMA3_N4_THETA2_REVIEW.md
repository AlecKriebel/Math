# Schema-3 n=4 theta-2 clean-room review

## Verdict

**VERIFIED** for the exact primary streams committed by
`primary/certificates/hard_cover_schema3_theta2_full_summary.json` and
`primary/certificates/probe_extension_theta2_schema3_summary.json`.

This verdict is intentionally narrower than the global local-containment
theorem.  It covers the complete corrected theta-2 equal-signature root
stream, its sequential restorations, and its path-bound p/q extensions.

## Independence boundary

The implementation under this directory does not import primary graph
canonicalization, completion enumeration, switching, descendant-mask,
invariant selection, polynomial pullback, sign, or transport code.  Primary
JSONL files are read only as claims to compare against.

The reviewer independently implements:

1. rooted and standard semi-directed validation;
2. exact mixed-graph and decorated-relation canonicalization;
3. active-blob arc recovery;
4. exact p/q arc subdivision and deletion;
5. displayed-tree switching enumeration;
6. descendant-mask construction;
7. JC Fourier coordinate polynomials;
8. two independently derived invariant families;
9. exact integer-polynomial pullbacks; and
10. semantic validation of every topology and transport record.

## Base hard cover

The corrected stream contains:

| Record class | Count |
|---|---:|
| Fixed root cases | 132 |
| Path-bound states | 2,106 |
| Refinement states | 114 |
| Generic polynomial separations | 1,860 |
| Labelled isomorphism terminals | 132 |
| Ordinary T terminals | 0 |
| Unresolved terminals | 0 |

Every one of the 2,106 raw paths regenerates the complete child-state set
declared for its exact fixed root and exact source/target rooted graph IDs.
The 1,860 separated terminals are certified by exact target-zero,
source-nonzero pullbacks.  The 132 remaining terminals are independently
labelled-isomorphic.

Certificate hash:
`245321c8e17c6b27fc2c5230b4074459d106a3c37454c90e1ff84f902954a1a4`.

Independent terminal-record commitment:
`ac39974a85aea561987be75f16f11897c0c583f122d34ab8cb826ec8bb594d89`.

## Probe extension

The probe stream's summary hashes are hashes of decompressed JSONL bytes, not
of gzip containers.  All four logical-stream commitments match exactly.

The independent structural replay establishes:

| Object | Count |
|---|---:|
| Graph records | 23,400 |
| State records | 168,582 |
| Path-binding records | 168,582 |
| Primary polynomial bodies cross-referenced | 29 |
| Base terminal paths extended by p | 132 |
| p children | 12,906 |
| Allowed isomorphic p parents extended by q | 1,302 |
| q children | 155,676 |

For each base path, the p records equal the full Cartesian product of the
independently recovered source and target blob arcs.  For each allowed p
path, the q records equal the corresponding full Cartesian product after the
p insertion.  No nonisomorphic p path advances to q.  Every exact parent and
child graph ID, insertion, deletion, base restoration, parent transport, and
sequential label is checked.

Structural certificate hash:
`e586e17213a37d075cca714d597b0d03a9fa0aa5fb8ed91a5567da3095c8425c`.

Normalized binding commitment:
`7403efa6d1b79ea1602a33a81c0907025894380de82606a517152071616a0b55`.

## Exact terminal algebra

The algebra replay classifies every probe state as follows:

| Stage and class | Count |
|---|---:|
| A+p, exact polynomial separation | 11,604 |
| A+p, labelled isomorphism | 1,302 |
| A+p+q, exact polynomial separation | 141,468 |
| A+p+q, labelled isomorphism | 14,208 |

All 153,072 separations use an independently selected invariant.  Of these,
150,468 are separated by the reviewer's complete arm-multihomogeneous
quadratic family and 2,604 by its independently derived degree-at-most-three
family.  Every target pullback expands to the zero polynomial and every
source pullback expands to a nonzero integer polynomial.  No sign certificate
is used and no all-quartet fallback was required.

The 15,510 isomorphism states pass both mixed-graph transport checks and a
canonical switching-mask comparison quotienting split complements,
reticulation order, and parent-choice flips.

All 132 accepted base terminals are triangle-free on both sides.  Consequently
this actual probe stream does not test a probe inserted on an edge whose
arrowheads change under ordinary triangle redirection.  It must not be used
as the missing T-edge probe-coherence certificate.

Algebra certificate hash:
`d954013945e74c99dc28c2ab55541531cf491e413473ada8931c45e74758f3a8`.

Exact evidence logical-stream hash:
`3c7c8b257f11c57ed35b214f4bb345d72563b74f32d40bb09059eef0314e55cd`.

## Mutation sensitivity

The actual-stream mutation suite rejects all ten tested corruptions:

- missing and duplicate states;
- missing and duplicate path bindings;
- altered port matching;
- reversed source/target direction;
- inconsistent p/q path binding;
- altered exact rooted graph identity;
- altered polynomial hash; and
- a valid exact polynomial reassigned to the wrong decorated relation.

Mutation certificate hash:
`93ed47297ec22b3ac8c50921c05ef6bfdc1f125992e1ca0508970d857bed4e18`.

## Post hoc independent-review comparison

After this clean-room run completed, the separately committed implementation
under `reviews/final_hard_cover_adversary/` was opened for comparison.  It
independently reports the same 23,400 graphs, 168,582 states and bindings,
12,906 p relations, 155,676 q relations, and four terminal-class counts.  It
also identifies the same remaining 110 + 776 unequal-direction gap and the
same triangle-free-terminal limitation.  Its independent agreement is a
cross-check, not an input to any certificate in this directory.

## Preserved reviewer failures

The review preserves three implementation failures rather than deleting their
traces:

1. interpreting logical-stream hashes as gzip-container hashes;
2. comparing presentation-sensitive raw arcs after replacing an exact rooted
   graph by an isomorphic representative; and
3. comparing rooted descendant masks without quotienting split complements.

They are documented under `history/implementation_failures/`.  None is a
failure of the corrected primary stream.

## Remaining scope

This result does not classify the reported unequal-but-necessary signature
directions, does not replace a merged corrected n=3 replay, and does not prove
exhaustiveness of the complete primitive root universe or T-edge probe
coherence.  The global landmark claim therefore remains fail-closed and
unresolved.
