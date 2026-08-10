# Adversarial referee report: schema-3 n=3 local base gate

Verdict: **VERIFIED**, with the exact scope and reliance boundary stated
below.

The frozen summary under review has SHA-256
`791844a802af61f64cba937a5adbe9d1d381d3fd7e55165914d4e4c885908e65`.
The reviewed checkpoints are:

- `be8a30870550efba2115cf2eb87e1d3611dd8c3b` — normalized schema-3 n=3
  hard cover;
- `f3cc9493b1e677378e3c0b4f8e965cb9199a436f` — zero-sum descriptor and
  bounded-root convention;
- `1018701d04d8656fe9ac92bb201413e043b802a1` — Euclid's independent
  hard-cover checkpoint, used here only for its completed path audit;
- `663336f839c29d91024220ed3777d0c124e975f5` — the independent ordinary
  JC triangle-redirection certificate.

The verdict applies only to the frozen schema-3 **n=3 fixed-root hard-cover
base relation stream**, with three outgoing roles and four selected ports.
It does not cover probe-extension promotion, arbitrary subdivisions, other
local cores or root widths, cut preservation, bridge peeling,
local-to-global synthesis, or the global identifiability theorem.

## What survived adversarial review

### 1. Frozen streams and directed-relation bindings

The referee independently checked the compressed bytes and decompressed
logical streams for:

- 68,584 directed relations;
- 14,482 rooted graphs;
- 5,344 fixed root cases;
- 225 sparse integer-polynomial bodies.

Every graph, root, polynomial, state, relation binding, and raw path binding
has the correct content address. There are no duplicate state identifiers,
dangling references, or unused polynomial bodies. The independently rebuilt
root-case commitment is
`5604092a360a47f75e003fa2db9bc5886575e1aef106c6657c17546c6c027509`,
exactly the commitment in the frozen summary.

The terminal census is exactly:

```text
56,055  generic polynomial separations
 8,349  relations refined by the next restoration
 4,036  strict open-cube separations
   120  labelled-isomorphism terminals
    24  ordinary-T terminals
```

### 2. Standard-class membership

The verifier did not read a primary validity flag. For each of the 14,482
rooted graphs it independently checked:

- finite simple binary rooted-DAG degrees and absence of parallel arcs;
- acyclicity and reachability from the root;
- the lowest-stable-ancestor condition by enumerating root-to-leaf paths;
- tree-childness of the displayed rooting;
- the locked one-step reticulation-preserving `sd0` reduction;
- simplicity and binary degrees of the resulting labelled mixed graph;
- retained-arrowhead counts;
- absence of an omnian, the locked exact criterion for `S_TC`;
- biconnected-component level at most two;
- at most one triangle.

The resulting inventory contains 1,296 one-reticulation level-1
presentations and 13,186 two-reticulation level-2 presentations. Of the
14,482 mixed presentations, 13,732 are triangle-free and 750 contain exactly
one triangle. No class-membership failure was found.

This statement uses precisely `docs/DEFINITIONS_LOCK.md`: already-simple,
binary, LSA-rootable `sd0` mixed graphs with no omnians. It does not transfer
membership to a broader cleanup or weak tree-child convention.

### 3. Standard mixed quotient and the zero-sum complement

A new individualization/refinement mixed-graph canonizer, written locally in
this package, finds 9,721 labelled standard mixed classes and 2,492 classes
with multiple rooted presentations. It preserves leaf labels, undirected
edges, and the direction of each retained arrowhead.

For every multi-root class, the referee regenerated displayed switchings and
descendant masks. On the zero-sum Fourier slice it replaced a selected side
by the minimum of that side and its **full selected complement**, then
quotiented reticulation-choice permutations and flips. All 2,492 classes
agree after this normalization.

The two intended attacks are mutation-sensitive:

- omitting complement normalization splits 958 rooted-presentation classes;
- complementing in a fixed four-bit universe rather than the actual selected
  universe also splits 958 classes.

Independently exhausting the 64 zero-sum four-character assignments and all
16 masks gives exactly eight split/complement classes. Algebraically,
`xor(S)=xor(S^c)` on the zero-sum slice. Suppressed path rows are zipped by
the positive product map

```text
(x1,...,xk) -> x1...xk,
```

which is onto `(0,1)` and has nonzero differential everywhere in that open
cube.

### 4. Fixed-root restoration paths

Starting from the hash-locked 5,344 root inventory, the referee rebuilt every
restoration insertion from the source segment words, target dummy-role order,
parent binding, and next physical label. It finds:

- 22,000 entry presentations;
- 46,584 child presentations;
- 68,584 presentations in total.

Every possible insertion position of the next label occurs exactly once.
Every child has the correct parent path binding, restoration word, graph
references, transport, and child-state reference. No missing, duplicate, or
mis-parented path was found. Euclid's separately written path implementation
agrees on the same content-addressed streams.

This is fixed-root/path exhaustiveness **after the frozen 5,344-root
inventory**. This referee verifies that inventory's content commitment and
all of its members' standard-class status; it does not re-enumerate the
primitive source/target generator universe from scratch. No conclusion here
promotes this base stream to arbitrary probes or subdivisions.

### 5. Graph-to-polynomial and invariant binding

The referee imports no primary or Euclid code. It independently derives:

```text
rooted graph
  -> displayed reticulation switchings
  -> descendant masks
  -> full-selected zero-sum quotient
  -> JC Fourier-coordinate polynomials
  -> the indexed invariant pullback.
```

It reconstructs the 84-element invariant orbit from seven mathematical
templates and independently verifies every invariant hash and every
port-arm multidegree in the frozen multihomogeneity table.

All 60,091 directed separated relations were attacked at four deterministic
points over the exact prime field of order 2,147,483,647. Every active
pullback was nonzero at least once, every graph-derived value agreed with the
assigned body, and all 240,364 attempted opposite-side falsifications
evaluated to zero.

The final certificate does not stop at these attacks. Sparse integer
expansion independently proves:

- all 246 active descriptor/invariant binding classes equal their assigned
  polynomial bodies;
- all 280 distinct claimed zero-side classes are identically zero;
- all 40 strict-active classes equal their assigned bodies;
- all 225 stored polynomial bodies are regenerated from a graph witness.

Thus a valid polynomial cannot be reassigned merely because it came from a
similar target hash: the source/target graph, selected quartet, invariant,
direction, and body are bound together.

### 6. All strict open-cube signs

The 4,036 strict relations use 27 distinct integer polynomials. An optional
regenerator factored those 27 bodies; the committed stdlib verifier then
independently:

- multiplies all 309 committed factors back to the exact original bodies;
- recalculates every factor's rational Bernstein coefficients;
- proves each factor has one strict sign on `(0,1)^d`;
- combines content, signs, and multiplicities;
- checks the resulting sign against every one of the 4,036 relation claims.

All 27 strict bodies and every reference pass. The Bernstein argument is
strict on the open cube because every Bernstein basis function is positive
there and each certified factor has coefficients of one weak sign with at
least one coefficient of strict sign.

### 7. Source-relative genericity

For each generic-polynomial terminal, the target pullback is the zero
polynomial while the source pullback is a nonzero integer polynomial. Its
source exceptional locus is therefore proper algebraic. For each strict
terminal, the source pullback is zero while the target pullback has a strict
opposite-side sign throughout its open parameter cube. Neither relation can
support the directed full-dimensional source containment under test.

The zero-sum complement is an exact Fourier identity and each suppressed
path product is a positive submersion. Therefore these conclusions hold on
the scoped projective source model, rather than only on an accidental rooted
boundary chart. Here “generic” means outside a proper algebraic subset of
the scoped source model.

### 8. The 144 equal-signature terminals

The 120 isomorphism terminals pass two independent checks:

1. equality under the new exact labelled mixed-graph canonizer;
2. a separate label-, arrow-, incidence-, and distance-preserving
   backtracking isomorphism search.

The 24 ordinary-`T` terminals are pairwise nonisomorphic before quotienting.
Each endpoint has exactly one triangle, and independently forgetting only the
retained arrowheads on that triangle's three edges gives an intersecting
canonical quotient. Thus these are ordinary triangle redirections, not
hidden labelled isomorphisms.

Their model-theoretic promotion is deliberately narrow. The separately
committed clean-room triangle certificate verifies a common
full-dimensional regular **projective port-tensor germ** for the three
orientations. It does not prove or claim equality of their complete open
stochastic images. Consequently, within this frozen n=3 terminal universe,
the only equal-signature outcomes are labelled isomorphism or ordinary `T`.

## Mutation metaaudit

Sixteen independent mutations were required to fail and did fail:

1. delete a relation;
2. duplicate a relation;
3. alter a port correspondence;
4. reverse source and target;
5. reverse a strict source-relative direction;
6. remove a child;
7. merge two root provenances;
8. alter a rooted arc;
9. assign a valid separator and its valid hash to the wrong relation;
10. alter a raw-to-canonical vertex transport;
11. remove complement normalization;
12. use the wrong complement width;
13. forge a nonisomorphic relation as an isomorphism terminal;
14. forge an ordinary-`T` terminal as an isomorphism;
15. alter a restoration word;
16. forge a strict-factor hash.

All mutations are recorded in `mutation_results.json`. Of particular
importance, swapping a syntactically valid polynomial together with its hash
is rejected only because the verifier regenerates the pullback from the
decorated graph relation.

## Preserved upstream limitation

Euclid's completed path audit is independently useful and agrees with this
package. Its frozen terminal routine, however, does not recognize the active
labels `strict_open_cube_separation` and `support_prefix_ordinary_T`. The
aborted attempt and exact dispatch mismatch are preserved under
`history/implementation_failures/`; no result from the aborted run is used.
This package independently replaces that unsupported terminal layer rather
than treating Euclid as an oracle.

## Final scope statement

**VERIFIED:** conditional on the frozen, content-addressed 5,344-root
inventory, the complete schema-3 n=3 fixed-root hard-cover base stream is
class-valid, path-exhaustive, zero-sum normalized, graph-to-polynomial bound,
strict-sign certified, and source-relative generic. Its 144 equal-signature
terminals consist exactly of 120 labelled isomorphisms and 24 ordinary
triangle redirections.

**UNRESOLVED BY THIS REVIEW:** primitive-generator re-enumeration, probe
coherence, arbitrary-subdivision promotion, other base gates, cut and bridge
arguments, and the global standard-strong JC theorem.
