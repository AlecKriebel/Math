# Adversarial review: final n=3 compact probe family

## Verdict

**VERIFIED AFTER CORRECTION — evidence-format gate only.**

The four locked compact summaries and the locked verbose summary encode the
same 101,148 directed graph relations, with an exact global bijection of
verbose binding IDs. Every parent/child graph, insertion and deletion,
source-to-target direction, class, and unique isomorphism or ordinary-`T`
transport was independently reconstructed. Every compact and verbose selected
separator was independently regenerated through displayed switchings,
descendant masks, complement-normalized Fourier descriptors, and exact
polynomial pullback. Strict signs were proved independently by exact
factorization and affine endpoint signs on the open unit cube.

The exact class totals are:

| Classification | Count |
|---|---:|
| Generic polynomial separation | 90,008 |
| Labelled isomorphism | 9,676 |
| Ordinary triangle redirection `T` | 840 |
| Strict open-cube separation | 624 |
| **Total** | **101,148** |

Unlike the n=4 triangle-free gate, this n=3 family exercises all four compact
format branches, including both `T` and strict separation.

## Correction discovered by the audit

The stronger claim that compact and verbose always choose the identical
witness body is **FALSE**. The first sequential failure occurs at path 59,
`A+p+q`, `(p,q)=(45,47)`, verbose binding
`ff90b28e38f7be890d3c207e08e6ff1c4a51afbcf89a40ea28bdf2960e47cf6b`.
Compact chooses quartet chunk 3 and verbose chooses chunk 32. Both use
invariant 49; both independently have source pullback zero and target
pullback strictly positive, but their exact target polynomials differ.

Across the complete family, 56 strict relations have this form. No generic,
isomorphism, or `T` relation has a nonidentical evidence body. The corrected
contract is semantic:

1. path, graph relation, insertion, direction, class, and unique transport
   must agree exactly;
2. each package's selected witness must independently prove its claim on that
   same exact graph relation;
3. witness identity need not agree when several valid separators exist.

The failed lossless claim, its first counterexample, the original partial
streams, and the review-harness failures are retained under `history/`.

## Completeness and mutation sensitivity

The compact row indexing was independently shown to be a bijection onto every
raw `A+p` arc pair and every conditional `A+p+q` arc pair. The four shard
ranges are gapless `[0,144)`, and the union of normalized relations equals the
full set of 101,148 verbose binding IDs.

All 18 semantic mutations were rejected, including deletion, duplication,
truncation, arc reordering, path/root/parent corruption, source-target
reversal, class changes, port and transport corruption, wrong polynomial or
sign, and moving a valid generic or strict separator onto a relation where its
regenerated pullback is wrong. Nine merger mutations were also rejected while
the unmodified baseline passed.

## Schema observations

- No content-address collision was observed; every graph, state, witness,
  transport, and polynomial body was rehashed and checked. As usual, SHA-256
  content addressing is an engineering commitment rather than a mathematical
  proof of collision impossibility.
- Unique transports and parent-to-child transport coherence are verified for
  all 10,516 allowed cells (`9,676` isomorphisms plus `840` ordinary `T`).
- `primary/COMPACT_PROBE_SCHEMA.md` should explicitly distinguish semantic
  witness equivalence from lossless selected-witness identity before this
  format is described in a release document.
- The hardened merger is verified as an aggregator bound to exact primary and
  independent shard certificates. It does not replace the relation-level
  semantic replays.

## Scope

This result certifies the final n=3 evidence format and exact package. It does
not, by itself, prove the global level-2 identifiability theorem. No file under
`primary` or another review directory was edited.
