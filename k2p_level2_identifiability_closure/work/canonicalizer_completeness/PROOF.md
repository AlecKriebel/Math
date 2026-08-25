# Canonicalizer completeness proof

## The licensed descriptor action

For a rooted factor with \(r\) reticulations, changing the names of the
inheritance coordinates consists of a permutation of the \(r\) reticulations
and an independent exchange of the two incoming parents at each one.  The
complete licensed group is therefore

\[
B_r=S_r\ltimes (\mathbb Z/2\mathbb Z)^r,
\qquad |B_r|=r!2^r.
\]

The slow routine enumerates this group directly: `retic_variants` chooses
every reticulation order and both parent orders, and `descriptor_variant`
constructs the exact pullback.  The fast routine fixes one order and ranges
over every `(p,f)` in the same group.  Its assignment

```text
ob[p[j]] = nb[j] XOR f[j]
```

is the bijection from new switching bits to the slow routine's old switching
bits.  A flip exchanges the factors \(\lambda_j\) and
\(1-\lambda_j\), exactly the physical parent-order complement.

For a fixed group element, two edges are grouped only when their complete
sector signatures agree for every switching and every conservation-supported
character assignment.  Such edges are a serial product class.  Sorting the
signatures removes only the arbitrary class names.  Sorting the resulting
integer sparse pullbacks and taking their lexicographic minimum over all of
\(B_r\) is consequently a complete orbit representative.

A physical port permutation relabels descendant masks and Fourier character
rows by the same bijection.  XOR group sums, the K2P sector map, switching,
and edge-signature grouping commute with this relabelling.  Thus the
slow--fast comparison on each primitive completion archetype covers every
physical port permutation without quotienting any port action.

The audit compares the two implementations on all 10,084 archetypes:

- 6 four-port sources and 2,814 four-port targets;
- 4 five-port \(\theta_2\) sources and 6,138 five-port targets;
- 2 cycle sources and 1,120 three-port targets.

There are zero disagreements.

## The ordinary-triangle quotient

For a semi-directed mixed graph \(M\), let `Ord(M)` contain exactly those
three-cycles having one head on each of two distinct triangle edges, both
heads at the same reticulation, and no head on the third edge.  For
\(E\in\operatorname{Ord}(M)\), form a bipartite incidence expansion
\(I(M,E)\): original vertices and edge-vertices have different colors,
selected boundary labels color the original vertices, incidence edges retain
their head bits outside \(E\), and the three edge-vertices belonging to
\(E\) receive a dedicated `forgotten_triangle_edge` color.

Colored incidence isomorphisms are in bijection with labelled mixed-graph
isomorphisms.  The dedicated color forces the chosen source triangle onto the
chosen target triangle.  Therefore

\[
M\equiv_\triangle M'
\iff
\exists E\in\operatorname{Ord}(M),\ E'\in\operatorname{Ord}(M'):
I(M,E)\cong I(M',E').
\]

Enumerating all vertex triples is exhaustive.  This proves both absence of a
false merge and absence of a false split.

The independent replay reconstructs dummy deletion, suppression, root
suppression, ordinary triangles, marked incidence expansions, and exact graph
isomorphism without calling the atlas implementations.  On every 4,012
rank- and topology-eligible raw presentation it agrees with both the direct
and prepared atlas paths: 3,932 `none`, 26 `isomorphic`, and 54 `triangle`.

Finally, two live attacks demonstrate why both guards are necessary.  A
three-cycle whose two heads land at different vertices is rejected.  A pair
with an ordinary left triangle on one side and an ordinary right triangle on
the other becomes spuriously related if erased edges are unmarked, but is
rejected by the marked construction.  The mutation suite removes each guard
in turn and requires the semantic audit to fail.
