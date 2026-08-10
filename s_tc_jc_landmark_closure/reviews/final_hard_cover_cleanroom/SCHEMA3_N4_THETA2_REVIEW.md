# Schema-3 n=4 theta-2 base hard-cover review

## Verdict

**VERIFIED — scoped n=4 base gate.**

The active primary summary
`primary/certificates/hard_cover_schema3_theta2_full_summary.json`, with
physical SHA-256
`915bed0a3add001c1a94d6d862a2359e6ad75b3489f8d71b7adf006952b5ce37`,
passes an independent graph-to-algebra replay.  The clean-room implementation
does not import the primary canonicalizer, completion enumerator, switching
engine, descendant-mask code, invariant selector, or sign flags.

This verdict covers the corrected schema-3 **theta-2 minimum-support n=4
base hard cover only**.  It does not certify the superseded p/q probe stream,
the n=3 merged hard cover, other primitive cores, or the global theorem.

## Exact scope and totals

The frozen stream contains:

| object | exact count |
|---|---:|
| fixed full root cases | 132 |
| exact rooted graphs | 606 |
| canonical path-bound states | 2,106 |
| refinement states | 114 |
| generic polynomial separations | 1,860 |
| labelled-isomorphism terminals | 132 |
| ordinary-T terminals | 0 |
| unresolved terminals | 0 |
| primary polynomial bodies | 19 |

Every state identity includes its fixed full root case and exact source and
target rooted graph IDs.  No two states collide under the independently
normalized decorated-relation identity.  For every raw presentation merged
into a state, the clean room regenerates the complete child-state set; there
are zero per-path disagreements and zero first-provenance reuse failures.

## Zero-sum split-complement normalization

**VERIFIED.**  For every displayed switching and every retained edge, the
clean room computes the selected descendant mask directly and replaces it by

\[
  \min(S,S^c)
\]

over the full selected-port universe.  It then zips rows that have the same
complete switching-mask profile.  The resulting JC descriptor is invariant
under the admissible rooted presentations of each standard mixed graph.

There are 474 standard mixed-graph groups, of which 66 contain multiple
rooted presentations.  The active normalization has zero failures on these
66 groups.  Removing normalization breaks all 66 groups; complementing in an
incorrect four-port universe also breaks all 66.  All 606 exact graph
descriptors change under either adversarial rule, so this check is not
vacuous.

## Terminal graph-to-polynomial audit

**VERIFIED.**  The clean room independently enumerates displayed switchings,
derives descendant masks, builds exact JC Fourier coordinates, and derives a
target identity with a nonzero source pullback on the exact quartet bound to
each of the 1,860 separated graph relations.

- All 1,860 witnesses use the same quartet claimed by the corresponding
  primary record; no fallback to a different quartet is accepted.
- A separately generated finite invariant family supplies 1,828 witnesses.
- Exact target-nullspace derivation supplies the remaining 32 degree-five
  witnesses, all with port-arm multidegree `(3,3,3,4)`.
- The target pullback is exactly zero and the source pullback is an explicit
  nonzero integer polynomial in every case.
- All 19 primary polynomial bodies are well formed, referenced, and
  conflict-free across 415 exact descriptor/invariant binding classes.

The mathematical acceptance decision uses the independently regenerated
polynomial, not a primary `PASS` flag or a frozen topology identifier.  The
primary body IDs and exact hashes are checked as stream-integrity bindings;
the clean room is free to derive a different representative of the same
separating ideal.

The other 132 terminals are independently reduced to equal labelled standard
semi-directed mixed-graph codes.  Thus they are labelled isomorphisms.  No
ordinary-T or unresolved terminal occurs in this scoped stream.

## Mutation sensitivity

**VERIFIED.**  Thirteen adversarial mutations are all rejected:

1. delete a relation;
2. duplicate a relation;
3. alter port matching;
4. reverse source and target;
5. alter one path's child set;
6. merge across fixed root cases;
7. merge across source rooted graph IDs;
8. merge across target rooted graph IDs;
9. alter an exact rooted graph ID;
10. replace a polynomial commitment;
11. assign a valid polynomial to the wrong relation;
12. remove split-complement normalization;
13. normalize complements in the wrong selected-port universe.

## Frozen certificate commitments

- Full audit:
  `5cea78208f1ccbce93b22fb7f5c71e73999a9abea51e23d7182b9cfa4f1be1c6`
- Mutation audit:
  `c5cceff673c84ff0f654438adc0ef9aead969101549a4daa645a26911d0ad2e6`

The compressed primary files are additionally checked against their physical
hashes; their decompressed logical streams are checked against the summary.
The exact values are recorded in the full-audit certificate.

## Explicit nonclaims

- **UNRESOLVED:** active p/q probe closure.  Existing probe evidence binds a
  superseded base and remains historical only.
- **UNRESOLVED:** the merged n=3 gate until its distinct clean-room replay is
  completed.
- **UNRESOLVED:** arbitrary-subdivision coherence, remaining primitive cores,
  and the global standard-S_TC JC identifiability/containment theorem.

These limitations do not weaken the n=4 base verdict; they prevent this
local certificate from being promoted beyond its actual scope.
