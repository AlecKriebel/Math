# V2 hostile review of the compact DoubleLex LRAT publication package

## Verdict

**ACCEPT THE V2 PUBLICATION PACKAGE FOR THE EXACT-CNF UNSAT CLAIM ONLY.**

No defect was found in the frozen V2 package within its declared scope.  The
V1 metadata-integrity limitation is closed: the exact publication manifest
and README bytes are now hard-bound by the externally reviewed verifier, and
isolated mutations of either are rejected fail-closed.

The package faithfully carries the already accepted LRAT certificate for:

```text
instances/order12_k4_connected_doublelex/instance.cnf
SHA-256 14284db1f0b9cfb37b91d834fbabac1d0ca06d36e0d2782683e35cbd04a976e7
4,030,657 bytes
18,381 variables
115,507 clauses
1,190,774 literal occurrences
```

The exact formula is unsatisfiable.

This verdict is deliberately narrow.  It does not establish the
graph-to-CNF transfer, does not by itself exclude the connected
`(n,k)=(12,4)` graph slice, does not establish an order-12 frontier, and does
not resolve the universal γ–θ conjecture.  Those statements require their
separate mathematical and coverage audits.

## Frozen V2 target

The reviewed target remained unchanged from its opening snapshot through
finalization:

```text
certificates/order12_k4_doublelex_seed0_lrat_publication/
4 regular single-link files
64,302,187 total bytes
canonical inventory SHA-256
31640d4d7557e852798fd763becc1e2ba78fdb630a7439d4e796bdf043666f2e
```

The individual bindings are:

```text
README.md
2,720 bytes
07f73c23dd194b7c3b06c9d4743ef3f637a1ff299a1a0d9d28bdb535da6f848f

proof.converted.lrat.zst
64,288,636 bytes
edc0f6b76bc96b2b26677f399566ae437cc47a6fc0cc921eaff81d77b72a50da

publication-manifest.json
2,766 bytes
409214887b0bae931af7cc1d03d0d1eaaf8de667f4adfa3d2e03d6b291c6f77b

verify_publication.py
8,065 bytes
5bceb1c04756c4dcdfedcfd6609270e54b76ad9949de0b7dcee9be4c258c1c05
```

The reviewer-written evidence is:

```text
hostile_publication_audit_v2.py
40,709 bytes
2791d8ef8fb8876f388a76f53dc9d80af6e30c9213568240dad59ae6e6db2103

hostile-evidence.json
18,220 bytes
6cd5a32ed23d38f24243cf2e63ec27cb3669a8d42300e97dcf87d12b64958189
```

The frozen V1 review was not edited.  Its four files remained byte-identical,
with 65,838 total bytes and reviewer-defined inventory SHA-256
`5dac746f1b514732f711bb3e82260202ed4f3b3cec7a49a024e7b4fbd1543817`.

## Exact schema and trust-root audit

The manifest was parsed with duplicate-key and non-finite-number rejection.
Its exact root schema, nested key sets, value types, timestamps, V2
pending-review status, claim boundary, paths, sizes, hashes, compression
record, proof census, checker binding, author-package binding, hostile-review
binding, and verification record all match the frozen bytes.

The package schema identifier remains
`gamma-theta-doublelex-lrat-publication-package-v1`, version 1; V2 denotes
this revised package/review cycle.  The verification output separately uses
`gamma-theta-doublelex-publication-verifier-v2`.

The manifest deliberately does not attempt a circular self-binding of
`verify_publication.py`.  It labels that executable source as the hardcoded
trust root whose integrity is supplied by the external hostile-review
inventory.  This review supplies that binding:

```text
verify_publication.py
5bceb1c04756c4dcdfedcfd6609270e54b76ad9949de0b7dcee9be4c258c1c05
8,065 bytes
```

The exact reviewed verifier hardcodes the full size and SHA-256 of every
other package file and every decisive external artifact.  Its emitted claim
boundary is:

> This verifies UNSAT only for the exact DoubleLex CNF. Transfer to graphs
> uses the separately reviewed C-037/C-045 implication.

The README and manifest use the same narrow boundary.  Neither presents the
package as an independent graph-slice proof or a universal resolution.

No extra package file, symlink, or multiply linked file was present.

## Formula and accepted-certificate bindings

An independent strict DIMACS parser reproduced:

```text
18,381 variables
115,507 declared and parsed clauses
1,190,774 literal occurrences
maximum variable 18,381
```

The external inputs hard-bound by the verifier were rehashed against the live
files:

```text
exact formula
14284db1f0b9cfb37b91d834fbabac1d0ca06d36e0d2782683e35cbd04a976e7

lrat-check
5d7d77a57457db82e57f2505ea9d0267ff0bceff197235b6edfc8fda1f26c7a2

author certificate
a21bd3db71fb271965859237d7665c5d0c38d32d061fdf3eda285c014e366991

author artifact manifest
846a646ba951569f50a76b562fdc8ec005dcf0f06ff57e48b4e3d4d330fbd607

accepted hostile review
fb95934b5d5acd75c9f6deb9142be3b903900f5abd02a5cc21d9884788f38395

accepted hostile evidence
2651f9d286582c068fb872acf862b82c4d4ab8e5fc07f6b99825b9335dd40b63
```

The complete 35-file author package was resnapshotted and remains
entry-identical to its accepted hostile-review snapshot:

```text
260,029,326 bytes
0814a4f435f9a50784eb12dcd99116f5b4529587a78723bff328dcec86ec7113
```

The accepted hostile evidence retains verdict
`ACCEPT_EXACT_DOUBLELEX_CNF_UNSAT_ONLY` and binds both its fresh and retained
LRATs to the recovered-proof identity below.

## Compression and exact recovery

Zstandard CLI 1.5.7 reported one frame, no dictionary, decompressed size
228,381,671 bytes, and an XXH64 frame checksum.  Its independent integrity
test passed.

Private decompression produced:

```text
proof.recovered.lrat
228,381,671 bytes
0e04eb639a3f7f7d335126d56040abb4ef11e8548770262c316a608390659263
```

The recovered file was compared block-for-block with the retained author
LRAT and was byte-identical.  Recompression using the exact manifested
parameters, `zstd -9 -T1 --check`, reproduced the V2 package stream
byte-for-byte, including its size and SHA-256.

Thus compression has not substituted, truncated, or logically changed the
accepted LRAT artifact.

## Fresh private one-command replay

The reviewer created a private campaign mirror containing only the ten files
needed by the V2 verifier.  Every formula, proof, checker, manifest, README,
certificate, and review input used by the child was a private copy.

From that private campaign root, the documented command was run:

```text
python3 certificates/order12_k4_doublelex_seed0_lrat_publication/verify_publication.py
```

The child exited 0 after 3.961 seconds, wrote empty stderr, recovered the exact
LRAT identity above, and invoked the hash-pinned `lrat-check`.  The checker
produced exactly one verification marker and the required proof census:

```text
c parsed a formula with 18381 variables and 115507 clauses
c VERIFIED
c Added clauses = 471552.  Deleted clauses = 471427.  Max live clauses = 115507
```

The exact one-line JSON result used schema
`gamma-theta-doublelex-publication-verifier-v2` and verdict:

```text
VERIFIED_EXACT_DOUBLELEX_CNF_UNSAT_ONLY
```

No SAT solver was invoked during this audit.

## Fail-closed mutation probes

All thirteen isolated mutation probes were rejected with exit code 1, empty
stdout, and a `REJECTED:` diagnostic.

The eleven probes retained from V1 were:

1. one-byte formula mutation;
2. one-byte compressed-LRAT mutation;
3. one-byte checker mutation;
4. one-byte author-certificate mutation;
5. one-byte author-manifest mutation;
6. one-byte accepted-review mutation;
7. one-byte accepted-review-evidence mutation;
8. formula symlink substitution;
9. formula multiple-hard-link substitution;
10. one-byte compressed-LRAT truncation; and
11. absence of `zstd` from the executable path.

The two V1 gap regressions were:

12. changing the publication manifest's schema version from 1 to 2; and
13. a one-byte README mutation.

The V2 verifier rejected probe 12 against the exact
`409214887b0bae931af7cc1d03d0d1eaaf8de667f4adfa3d2e03d6b291c6f77b`
manifest binding and probe 13 against the exact
`07f73c23dd194b7c3b06c9d4743ef3f637a1ff299a1a0d9d28bdb535da6f848f`
README binding.  The V1 metadata-integrity limitation is therefore closed.

## Final accepted scope

This review accepts exactly:

> The V2 four-file zstd package faithfully represents the already accepted
> LRAT certificate proving that the DoubleLex DIMACS formula with SHA-256
> `14284db1f0b9cfb37b91d834fbabac1d0ca06d36e0d2782683e35cbd04a976e7`
> is unsatisfiable.

No broader graph-theoretic or universal claim follows from this package
review alone.
