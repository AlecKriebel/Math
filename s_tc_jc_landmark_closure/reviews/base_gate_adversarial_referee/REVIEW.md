# Adversarial referee report: corrected n=4 local base gate

Verdict: **VERIFIED**, with the exact scope and reliance boundary below.

Reviewed commits:

- `d7fb159e038630b449bd87dc835432c5897788b6` — corrected schema-3 n=4
  theta-2 base gate;
- `f3cc9493b1e677378e3c0b4f8e965cb9199a436f` — zero-sum descriptor and
  bounded-root convention.

The verdict applies only to the frozen schema-3 **n=4 theta-2
minimum-support base hard cover**. It does not cover the n=3 gate, p/q probe
extensions, other primitive cores, arbitrary subdivisions, or a global
identifiability theorem.

## What survived adversarial review

### 1. Frozen artifacts and content associations

The active primary summary has SHA-256
`915bed0a3add001c1a94d6d862a2359e6ad75b3489f8d71b7adf006952b5ce37`.
Its four compressed streams and their decompressed logical streams match the
frozen commitments exactly.

The independent referee checked every content address:

- 606 rooted graph identifiers;
- 132 fixed root-case identifiers;
- 19 sparse-polynomial identifiers;
- 2,106 directed state identifiers and binding commitments;
- every raw path-binding commitment;
- every graph, root, and polynomial reference from every state.

There are no duplicate or dangling identifiers and no association failure.

### 2. Locked class membership

All 606 rooted graphs were checked without reading a primary validity flag.
Each is:

- a finite simple binary rooted DAG;
- root-reachable and LSA-rooted;
- tree-child in the displayed rooted presentation;
- reduced by the locked one-step reticulation-preserving `sd0` operation to a
  simple binary mixed graph;
- omnian-free and therefore standard-strong under the locked criterion;
- level exactly two, with exactly two reticulations in its largest blob.

Every one of the 606 mixed graphs is triangle-free. Consequently, an ordinary
triangle-redirection terminal cannot occur inside this particular frozen
base stream.

This membership conclusion uses the exact class in `docs/DEFINITIONS_LOCK.md`:
simple binary LSA-rootable `sd0` mixed graphs with no omnian. It is not a
claim about a broader cleanup convention.

### 3. Root/complement quotient

A new individualization/refinement canonizer, unrelated to either the
primary or the previous clean-room canonizer, finds exactly:

- 474 labelled standard mixed-graph classes;
- 66 classes containing multiple rooted presentations.

For each of those 66 classes, the referee regenerated displayed switchings
and descendant masks from the rooted graph. On the zero-sum Fourier slice it
normalized each selected side by its full selected complement and zipped
identical switching rows. The normalized descriptors agree in all 66
classes.

Both adversarial alternatives fail in all 66 classes:

- omitting complement normalization splits every class;
- complementing in a fixed four-bit universe before taking the full selected
  quotient also splits every class.

The underlying algebra is exact. For a zero-sum character assignment,
`xor(S)=xor(S^c)`. Exhaustion of all 64 zero-sum quartet assignments and all
16 masks gives exactly eight split/complement equivalence classes and no
additional collapse. Zipping repeated rows is the positive product map

```text
(x1,...,xk) -> x1...xk,
```

which is onto `(0,1)` and has nonzero differential throughout the open cube.

### 4. Path exhaustiveness after the frozen root inventory

The restoration forest was reconstructed directly from the source segment
words and target dummy-role order. It contains:

- 1,056 first-restoration presentations: eight for each of 132 roots;
- 1,050 child presentations from the 114 refined states;
- exactly 2,106 presentations in total.

Every possible insertion position of the next physical label occurs once.
Every child has the correct parent binding, restoration-path extension,
source word, target role, graph identifiers, and child-state reference. No
state has multiple raw provenances in this stream, so no hidden canonical
merge is used to make the count work.

This proves path exhaustiveness **conditional on the frozen 132-root
inventory**. This referee did not duplicate the prior primitive-generator
enumeration that established those 132 roots; it instead checked its frozen
commitment and every downstream path. That deliberate reliance boundary is
why this review is independent rather than a copy of the previous full
replay.

### 5. Graph-to-polynomial binding and source genericity

The referee independently regenerated the 84-element invariant orbit from
the seven mathematical templates. Every invariant index and SHA-256 agrees
with the frozen multihomogeneity table, and every invariant has the claimed
port-arm multidegree.

For each of the 1,860 separated directed relations, it then regenerated:

```text
rooted graph
  -> displayed switchings
  -> quartet descendant masks
  -> zero-sum complement quotient
  -> JC Fourier coordinates
  -> the indexed invariant value.
```

Exact arithmetic modulo the prime `2147483647` produced a nonzero source
value for every relation. A nonzero modular value is an exact certificate
that the integer source pullback is not the zero polynomial. Four independent
deterministic target evaluations per relation—7,440 attempted
falsifications—were all zero.

In addition, 44 graph-derived pullbacks were expanded symbolically over the
integers. The sample covers:

- all 19 frozen primary polynomial bodies;
- all 12 invariant indices used by the stream;
- all three selected port counts, 6, 7, and 8;
- all 16 occurring `(port count, quartet chunk)` strata.

Every sampled target pullback is identically zero and every sampled source
pullback is nonzero. The full target-identity statement for the remaining
records is bound to the prior exact full-audit commitment
`5cea78208f1ccbce93b22fb7f5c71e73999a9abea51e23d7182b9cfa4f1be1c6`.
Thus this referee attacks and samples that proof rather than silently
claiming to have repeated all 1,860 symbolic expansions.

For every relation, a target identity and a nonzero source pullback imply
that the indistinguishable source parameters lie in a proper algebraic zero
set. Complement normalization is an identity on the zero-sum slice, while
root splitting and row zipping are positive submersive product maps.
Therefore the separation is source-relative generic on the locked standard
semidirected model, not merely on a rooted boundary chart.

### 6. The terminal claim

All 132 equal-signature terminals were checked twice:

1. by the new exact individualization/refinement canonical form;
2. by a separate label-, arrow-, and distance-preserving backtracking
   isomorphism search.

Both checks find labelled mixed-graph isomorphism in every case. There are:

```text
132  labelled-isomorphism terminals
  0  ordinary-T terminals
  0  unresolved terminals
```

This statement is confined to the scoped frozen n=4 terminal universe. It is
not the claim that every n=4 level-2 relation in the larger project has been
classified.

## Mutation metaaudit

The earlier 13-mutation certificate is hash-locked, reports all mutations
rejected, and is internally consistent. The present referee also implemented
12 independent attacks:

1. delete a relation;
2. duplicate a relation;
3. alter a port matching;
4. reverse source and target;
5. delete a child;
6. merge root provenance;
7. alter a rooted arc;
8. assign a valid polynomial body to the wrong relation;
9. remove complement normalization;
10. use the wrong complement width;
11. forge a nonisomorphic pair as an isomorphism terminal;
12. alter one restoration word.

All are rejected. The first implementation syntax failure was preserved under
`history/implementation_failures/` before repair.

## Final scope statement

**VERIFIED:** the frozen corrected schema-3 n=4 theta-2 minimum-support base
gate contains only generic polynomial separations, required refinements, and
labelled-isomorphism terminals. Its class membership, quotient convention,
path closure, source-relative genericity, and terminal classification survive
the attacks above.

**UNRESOLVED BY THIS REVIEW:** n=3, p/q probe closure, arbitrary-subdivision
promotion, other cores, and the global standard-strong JC theorem.
