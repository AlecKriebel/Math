# Adversarial review: final n=4 compact probe shards

## Verdict

**VERIFIED — for the evidence-format gate only.**

The four supplied final complement-normalized n=4 compact shards are a
lossless encoding of the complete final verbose package tagged
`theta2_schema3_final`.  The clean-room replay found no mathematical or
serialization discrepancy in the 168,582 directed relations.

This verdict does **not** certify the global identifiability theorem, an
arbitrary-port promotion, or either compact branch that is absent from this
triangle-free dataset.

## Locked inputs

| shard | path range | supplied summary SHA-256 | relations | status |
|---|---:|---|---:|---|
| s0 | [0,33) | `9649b08315dbd5d9dca8b8e4e1892deefe4cecacd81ea6f1880d994e56bd0863` | 42,968 | VERIFIED |
| s1 | [33,66) | `ea0c7181389d4bb73a7a1332ec396f0223cf0e9746efde9f39bc79d3d3029de1` | 40,204 | VERIFIED |
| s2 | [66,99) | `ab678bcbd268ffd704fa79c45ac8a1eb89e2907132eb5e12a99a625cc606ebbd` | 43,034 | VERIFIED |
| s3 | [99,132) | `ffa5658edfaac800da9614fcaf32a576a09d26d6d1449fc89a2ac66efff551d6` | 42,376 | VERIFIED |

The final verbose summary is
`7e1c06223a683b888c365b4fa0fbe0568896a3c4e466be9b382f8d0fd7066c7a`.
Its binding and state streams each declare 168,582 records.

## What was independently reconstructed

The implementation under this directory imports no module from `primary` and
does not reuse another graph, canonicalization, descriptor, invariant, or
separator engine.  It independently performs the following operations.

1. Rebuilds the ordered 132-path inventory from the base hard-cover state and
   graph streams.  The regenerated commitment is
   `21193cac2d8a977e785d9aeb980f57a2c10994d5893fa58c3038792d9c32c5c6`.
2. Checks both historical parent graph content IDs and normalized exact rooted
   graph IDs.
3. Validates every distinct rooted graph as binary, acyclic, LSA-rooted,
   strongly tree-child, and level at most 2; all audited graphs are
   triangle-free and have two reticulations.
4. Recovers admissible internal blob arcs and decodes every p cell and every
   conditional q block by the documented row-major indexing.  The resulting
   arc-pair sets are bijective to the corresponding verbose records.
5. Reconstructs each child by deterministic insertion and proves exact
   deletion back to its parent.
6. Enumerates displayed switchings, computes descendant masks, restricts to
   quartet zero-sum characters, and normalizes each split side by the smaller
   of the side and its four-bit complement.
7. Regenerates every used generic separator pullback exactly.  Each source
   pullback is nonzero, each target pullback is zero, and every exact SHA-256,
   polynomial content ID, and sparse polynomial body agrees.
8. Independently finds the unique labelled mixed-graph isomorphism for every
   allowed cell and checks vertex, edge, reticulation, port, and canonical
   transports.  Every q transport restricts coherently to its parent p
   transport.
9. Compares each compact classification and evidence body to the exact final
   verbose state, graph, insertion, direction, binding, witness, and transport.

The aggregate counts are:

| stage | generic polynomial separation | labelled isomorphism | total |
|---|---:|---:|---:|
| A+p | 11,604 | 1,302 | 12,906 |
| A+p+q | 141,468 | 14,208 | 155,676 |
| total | 153,072 | 15,510 | 168,582 |

The four normalized clean-room relation streams contain 168,582 distinct
verbose binding IDs.  Their union equals the complete set of verbose binding
IDs exactly; there are no missing, duplicate, or cross-shard records.

## Mutation sensitivity

The semantic verifier was tested after deliberately bypassing outer file
hashes.  It rejected all 14 mutations:

- relation deletion and duplication;
- conditional-q truncation;
- wrong relation/witness index;
- wrong polynomial body;
- altered arc order;
- altered port correspondence;
- corrupted vertex transport;
- source/target reversal;
- wrong parent and wrong root;
- cross-path merge;
- incomplete shard coverage;
- duplicate path row.

The hardened primary merger was exercised only as a black box.  It accepted
the genuine four-shard package after receiving all four exact primary and
independent replay certificates.  It rejected incomplete coverage, a
duplicate shard, a missing independent replay, a misbound replay, a wrong
path range, wrong replay counts, and schema-specification tampering.

## Schema review

No collision, transport, or completeness defect was found for these exact
shards.

- Path identity is bound simultaneously to inventory index, exact parent
  bodies, base state/path/root provenance, and a content-addressed path row.
- Relation identity is not inferred from a target hash: source and target
  arcs are explicit and row-major indexing is independently regenerated.
- Evidence is not accepted by hash lookup alone.  The graph-derived
  polynomial or graph isomorphism is regenerated before the stored body is
  compared.
- The 15,510 isomorphism transports are unique and parent-coherent in this
  dataset.
- The four half-open shard ranges are disjoint, gapless, and exhaustive.

SHA-256 is used as an engineering commitment, not as a mathematical theorem
that collisions cannot exist.  Exact normalized bodies are compared wherever
the content ID is load-bearing.

## Mandatory scope limitation

The n=4 base is triangle-free.  Consequently:

- ordinary triangle-redirection `T` cells observed: **0**;
- strict open-cube separation cells observed: **0**.

The compact class-code and transport schema for those two branches therefore
remain unexercised by this gate.  They require a separate dataset containing
actual T and strict cases before receiving the same format verdict.

## Exact certificate anchors

- Final gate certificate:
  `b6efd20d3c7b5da7194821e3bdcaf6228121cb1cbd210d8886d9d08499c5f894`
- Independent shard certificates:
  - s0 `d82c8d7ff455a90586c2dc2dc6a1228a1382de014e3296f03f06d81e978dda1c`
  - s1 `536ace57ad10904bba2b0a83dc570df1c442f576af3f20250966af5489475528`
  - s2 `6d918fb1312295e6aa008ca3b502dcca60f934702e9d11cc65270dabe80fbb4c`
  - s3 `a1373a7fc854ec5121b349ef009f13fcf4bfc5e9817cd7b430a798bbea0e8463`
- Semantic mutation certificate:
  `50b88a881055f3b7859b3f42f79963f49fd07b14b83a8ce0f662c60060781375`
- Merger mutation certificate:
  `6be012f157ff4da37a6a5e1d4773fd672307dbad0730db66b9a20de03b44dc4c`
- Hardened merger manifest:
  `53b6523b7412c266495b5ff05123fe0f8ae15aca98ce9c6ad0246f4673578461`

All first full shard attempts passed.  Their exact one-line outputs are
preserved under `history/`; no semantic failure was repaired or discarded.
The full deterministic rerun did expose a review-harness-only randomized
temporary-path field.  Its successive differing hashes, cause, and correction
are preserved in `history/DETERMINISM_FAILURE.json`.  Two post-correction
runs produced the same merger-mutation certificate hash shown above.
