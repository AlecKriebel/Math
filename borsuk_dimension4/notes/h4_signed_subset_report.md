# Exact elimination of the signed 60-line golden configuration

**Checkpoint:** 2026-08-01T16:33:25-07:00  
**Discovery discipline:** first-principles exact computation only; no web or
literature search was used.

## Result

The proposed signed-subset route cannot produce a counterexample.  In fact a
stronger statement holds:

> Let \(V\) be the 120 oriented golden vectors (scaled by four), and let
> \(U\subseteq V\) be arbitrary.  The graph on \(U\) whose edges are the pairs
> with dot product exactly \(-8\) is five-colorable.

Consequently:

1. no switching of all 60 antipodal lines has a non-five-colorable negative-8
   graph;
2. deleting vertices to remove the forbidden negative
   \(4+4\sqrt5\)-magnitude pairs cannot help;
3. more generally, there is no subset of these oriented vectors with all pair
   products at least \(-8\) and a non-five-colorable \(-8\) graph.

This eliminates this configuration, not the four-dimensional Borsuk problem.

The exact certificate and its dependency-free checker are in
`borsuk_dimension4/search/h4_signed_subset_search.py`.

## 1. Exact configuration and relations

Coordinates are stored in the basis \(1,\sqrt5\) and multiplied by four.  The
120 vectors are

\[
 \{\pm4e_i\}_{i=1}^4,
 \qquad
 \{(\pm2,\pm2,\pm2,\pm2)\},
\]

together with the even coordinate permutations and independent signs on the
three nonzero entries of

\[
 (0,2,1+\sqrt5,-1+\sqrt5).
\]

Every vector has squared norm 16.  Direct arithmetic in
\(\mathbb Z[\sqrt5]\) gives the complete unordered-pair dot-product table:

| dot product | number of oriented pairs |
|---:|---:|
| \(-16\) | 60 |
| \(-4-4\sqrt5\) | 720 |
| \(-8\) | 1,200 |
| \(4-4\sqrt5\) | 720 |
| \(0\) | 1,800 |
| \(-4+4\sqrt5\) | 720 |
| \(8\) | 1,200 |
| \(4+4\sqrt5\) | 720 |

The checker also certifies the needed strict orderings by integer square
comparisons.  In particular

\[
 -4-4\sqrt5<-8<4-4\sqrt5.
\]

After quotienting by antipodes, the unsigned
\(|\langle x,y\rangle|=8\) graph has 60 vertices, 600 edges, and constant
degree 20.  The longer
\(|\langle x,y\rangle|=4+4\sqrt5\) relation has 360 edges and constant degree
12.

## 2. The antipodal two-cover certificate

Define one graph \(\widetilde G\) on all 120 **oriented** vectors by

\[
 xy\in E(\widetilde G) \quad\Longleftrightarrow\quad \langle x,y\rangle=-8.
\]

This graph is 20-regular with 1,200 edges.  The script contains an explicit
map

\[
 c:V\longrightarrow\{0,1,2,3,4\}
\]

and checks all 1,200 edges directly in exact arithmetic.  Each color class has
24 vertices.  As additional checks on ordering and transcription:

- antipodes always receive different colors;
- each of the ten unordered pairs of distinct colors occurs on exactly six
  antipodal lines.

Now choose any orientation of each of the 60 lines.  The resulting negative-8
graph is exactly the induced subgraph of \(\widetilde G\) on the 60 chosen
oriented vertices.  Restricting \(c\) gives a five-coloring.  This handles all
\(2^{60}\) switchings simultaneously; no switching enumeration or QBF claim is
needed.

If vertices are then deleted to eliminate every longer negative pair, the
remaining negative-8 graph is another induced subgraph of \(\widetilde G\), so the
same restricted coloring works.  The long-edge constraints can only shrink
the graph and therefore cannot evade the certificate.

Equivalently, for an arbitrary \(U\subseteq V\) satisfying
\(\langle x,y\rangle\ge-8\) for all pairs, its \(-8\) graph is
\(\widetilde G[U]\), hence is five-colorable.  This proves the requested
nonexistence exactly.

## 3. Exact checks on the unsigned lead

The attractiveness of the lead is real: the unsigned 60-line graph is
exactly six-chromatic and has no \(K_5\).  Let \(A\) be its adjacency matrix.
The checker verifies, entry by entry,

\[
 A(A+4I)(A-5I)(A-20I)=0.
\]

The graph is connected and 20-regular.  Thus the 20-eigenspace is
one-dimensional.  Combining the annihilating polynomial with
\(\operatorname{tr}A=0\) and
\(\operatorname{tr}(A^2)=60\cdot20=1200\) gives the exact spectrum

\[
 \{20^1,5^{16},0^{18},(-4)^{25}\}.
\]

Hoffman's bound gives

\[
 \alpha\le \frac{60\cdot4}{20+4}=10,
 \qquad
 \chi\ge\frac{60}{10}=6.
\]

An explicit six-coloring with six classes of size ten proves equality.  Exact
bit-set clique search finds a \(K_4\) and proves that no \(K_5\) occurs.

For a deterministic representative of each line, let \(S\) have entry
\(0\) off the absolute-8 relation and entry
\(\operatorname{sign}\langle x_i,x_j\rangle\) on that relation.  The checker
also verifies

\[
 S(S+5I)(S-10I)=0.
\]

Together with its first two traces, this gives

\[
 \operatorname{spec}(S)=\{10^8,0^{36},(-5)^{16}\}.
\]

These identities are independent structural cross-checks that the intended
60-line relation, its signs, and its deterministic ordering were reconstructed
correctly.

## 4. Reproduction

From `/Users/alec/Documents/Math-borsuk4` run

```text
python3 borsuk_dimension4/search/h4_signed_subset_search.py --verify
```

Expected output begins

```text
exact signed golden-line audit passed
oriented_vectors=120 negative_8_edges=1200 degree=20
oriented_negative_8_color_class_sizes=[24,24,24,24,24]
all_2^60_switchings_five_colorable=true
all_vertex_deleted_long_edge_compatible_subsets_five_colorable=true
```

The verifier rebuilds all coordinates, dot products, line relations, matrix
identities, clique checks, and color checks from scratch.  It does not import
the earlier route-A script and uses no floating-point arithmetic or optional
package.
