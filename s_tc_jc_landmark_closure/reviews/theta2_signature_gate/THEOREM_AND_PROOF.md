# Five-port theta-2 signature gate

Status: **VERIFIED**.

## Theorem

Work with the locked standard semi-directed convention and the open
Jukes--Cantor parameter domain.  Let the source be one of the three anchored
minimum strong supports of the `theta-2` core, with four selected outgoing
ports and one incoming tensor port.  Let the target range over every full
standard-strong completion on the same five selected tensor ports, allowing
its rooted incoming boundary either to be selected or to be marginalized.

For each ordered four-port marginal, pull back the complete 84-element orbit
of the seven inert JC invariant templates.  Write `S(H)` for the set of
templates whose pullback on the port tensor of `H` is a nonzero integer
polynomial.  Then:

1. the target grammar is exhaustive;
2. the necessary condition `S(source) subset S(target)` leaves exactly three
   source-target signature pairs;
3. all three pairs have equal signatures, and their three exact signature
   hashes are the hashes bound to the frozen theta-2 hard-cover roots;
4. no strict signature inclusion survives;
5. the 192 raw surviving presentations split intrinsically as

   - 18 direct presentations with no omitted target boundary role;
   - 42 nonretaining selected-incoming presentations; and
   - 132 nonretaining marginalized-incoming presentations;

6. all 18 direct presentations are labelled mixed-graph isomorphisms;
7. the canonical decorated-relation multiset of the 132 independently
   generated marginalized presentations is exactly the canonical multiset of
   the 132 frozen restoration roots;
8. every one of the 42 selected-incoming nonretaining presentations is an
   admissible-root-presentation duplicate of a frozen class, with an explicit
   mixed-graph vertex transport preserving all five selected port matches,
   retained arrowheads, and omitted physical boundary placeholders.

Thus the frozen 132-root theta-2 hard-cover input omits no algebraically
necessary nonretaining decorated relation.  This theorem does not certify the
downstream restoration forest, any other primitive core, arbitrary
subdivisions, or the global identifiability theorem.

## Proof

### 1. Source supports

The theta-2 core has arcs

```text
S->U, S->V, U->X0, V->X0, U->X1, V->X1
```

and minimum repairs

```text
{2,3}, {2,5}, {3,4}, {4,5}.
```

Its two reticulation sinks require two child ports.  The branch automorphism
identifies repairs 1 and 2 while repairs 0 and 3 remain distinct.  Hence the
anchored minimum-support quotient has exactly the three representatives
`0,1,3`.  The verifier constructs them directly from the displayed arcs and
checks the explicit primitive data against the inert core certificate.

### 2. Exhaustive target grammar

For every primitive core, choose:

1. selected or marginalized incoming mode;
2. a subset of selected reticulation-sink children;
3. a minimum repair; and
4. a weak composition of all remaining selected ordinary ports among the
   directed core segments.

Insert one dummy child for every omitted sink and one dummy port on every
empty segment of the chosen repair.  In marginalized mode also retain the
structural incoming leaf as a zero-character dummy.  Conversely, contracting
unselected ordinary subdivisions in any full strong target recovers exactly
these data, so the grammar is onto.

At five selected tensor ports this gives 1,983 selected-incoming and 4,155
marginalized-incoming raw completions.  Grouping only completions with the
same core kind and complete five-marginal descriptor gives 335 bases.  The
verifier independently checks that every grouped variant has the same full
ordered descriptor deck; no ordered port transport is lost.

### 3. Exact JC signatures

Each reticulation switching is enumerated directly.  Descendant masks are
computed on each displayed tree, and each four-port mask is identified with
its complement.  This is exact on the zero-sum Fourier slice because the XOR
on a subset equals the XOR on its complement.

For a descriptor-template pair, three finite-field evaluations are used only
as a fast nonvanishing certificate.  A nonzero residue proves that the
integer pullback is nonzero.  Every modular-zero candidate is then expanded
as an exact sparse integer polynomial; only the zero polynomial receives a
zero signature bit.  Thus every bit is exact.

If a source-open model germ were contained in a target germ and an invariant
vanished identically on the target but not on the source, the common source
set would lie in the proper zero set of a nonzero source polynomial.
Therefore

```text
S(source) subset S(target)
```

is necessary for source-relative containment.  Across all five four-port
marginals and all relative five-port assignments, the exact filter produces
1,950 target signatures and only three necessary source-target pairs.  Every
pair is equality; there is no strict inclusion.

### 4. Why three hashes are not enough

Several raw target completions and port assignments share one signature.
Accordingly, equality of the three survivor hashes is explicitly not treated
as a relation-inventory certificate.  The verifier expands every surviving
base assignment back through every raw completion provenance, producing 192
raw decorated presentations before graph quotienting.

The intrinsic direct predicate is that no omitted real target boundary role
remains.  It gives the exact partition `18 + 42 + 132` stated above.

### 5. Independent decorated mixed-graph quotient

The second verifier reconstructs source and target rooted graphs from the
primitive provenance without importing any project graph code.  It then:

1. marks every arc entering a reticulation;
2. undirects every other arc;
3. suppresses the binary root once;
4. retains all five selected labels `L_0,...,L_4` jointly on both sides;
5. gives every unselected physical boundary one placeholder colour while
   retaining its structural attachment; and
6. canonically labels the directed, side-coloured source-target relation by
   independent individualization/refinement.

Because the relation direction is fixed and the five matched port colours
are unique on both sides, canonically labelling the ordered source and target
components is equivalent to canonically labelling their coloured disjoint
union with five matching edges.  Every quotient is accompanied by an
explicit raw-vertex transport.  For omitted boundaries, the certificate also
records the induced physical-role transport; no omitted port is discarded.

All 18 direct target graphs have exactly the source mixed-graph code, so they
are labelled isomorphisms (ordinary `T` is not needed in this gate).

For the nonretaining strata, the 132 independently generated marginalized
presentations and the 132 frozen roots have equal canonical multisets.  Both
have 57 canonical classes, with multiplicity distribution

```text
30 classes of multiplicity 1,
 3 classes of multiplicity 2,
24 classes of multiplicity 4.
```

The verifier writes all 132 source and target transports.  The additional 42
selected-incoming presentations occupy classes already represented in the
frozen multiset; all 42 receive explicit transports to a frozen
marginalized-incoming representative.  This proves that they are alternative
root presentations, not omitted standard semi-directed relations.

### 6. Mutation sensitivity

The replay rejects omission of an incoming mode, deletion of a completion
class, alteration of a source repair, reversal of containment direction,
deletion of one same-signature provenance, collapse of two distinct
same-signature provenances, deletion of a nonretaining presentation, and
collapse of two distinct port-matched relations sharing an unlabelled target
topology.

Two failed mutation designs are preserved.  A nominal five-bit complement
before quartet projection is semantically vacuous: after restriction it only
exchanges a split side with its four-port complement, which has the same XOR
on zero-sum assignments.  The active wrong-width mutation instead uses a
three-bit complement on a four-port marginal and is rejected.

