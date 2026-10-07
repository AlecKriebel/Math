# Replay and trust boundary

Run `python verify.py` from any directory. The script resolves all files relative to itself. It verifies the manifest before importing the mathematical implementations, pins the explicit witness coefficients, reconstructs both arrangements twice, and compares full certificates. Run `python -O verify.py` as well; validation uses explicit exceptions rather than assertions.

`verify_inputs.py CATALOG PROBLEMS REPORTS [SOURCE_DIRECTORY]` separately checks the byte identities of the three supplied corpus snapshots, the complete exact-ID problem/report pair, and optionally all locally retained scholarly-source bytes. These input files are deliberately absent from this publication packet. Omitting this check is not evidence that the corpus was verified. No copied source text or PDF is distributed.

## Why the two finite enumerations are complete

For arrangement.py, every vertex of a simple d-arrangement is the intersection of a d-element basis. At such a vertex, every choice of signs on its d incident hyperplanes labels one adjacent open chamber. Each chamber is a nonempty pointed full-dimensional polyhedron, and hence has a vertex. Thus collecting these local signs enumerates every chamber.

Intersecting d-1 hyperplanes gives a line. Its finite arrangement edges are exactly the segments between consecutive intersection vertices; its two unbounded edges are the extreme rays. The signs on the remaining hyperplanes are constant on the relative interior of each edge or ray. Extending signs on the d-1 supporting hyperplanes enumerates their incident chambers. Every unbounded pointed polyhedron has an unbounded edge, so a chamber is unbounded exactly when it appears beside one of these rays. The resulting vertex-edge graphs of bounded chambers are therefore exact. Breadth-first search computes their graph diameters. Exact chamber counts, facet counts, regularity, connectivity, and the defect identities are additionally checked.

For verify_planar.py, let M exceed the absolute value of every coordinate of every line intersection. The square [-M,M]^2 contains all arrangement vertices strictly in its interior. For each of the 2^n sign vectors, repeated clipping computes exactly the intersection of the corresponding closed halfplanes with the square. Empty and zero-area intersections are discarded. Every feasible chamber has a vertex, and local sectors at its vertices are contained in the square, so no full-dimensional chamber is missed.

A bounded chamber is the convex hull of its vertices, all strictly inside the square, so its clipped polygon misses the square boundary and is unchanged by clipping. An unbounded chamber has a vertex inside the square and an unbounded ray, which must cross the square boundary. Therefore its clipped polygon meets that boundary. This establishes the boundedness classification without a floating-point test. Consecutive duplicate and collinear points are removed, yielding the true side count of each bounded polygon. Its graph diameter is floor(k/2).

The verifier compares complete sign sets and side counts between these algorithms, as well as exact certificate objects. The finite witness is a computer-assisted exhaustive proof for these explicit coefficients. It does not exhaust the space of arrangements with eight lines or establish any higher-dimensional conjecture.

## Integrity limitations

SHA-256 manifests detect accidental changes relative to the frozen packet; they do not make an untrusted verifier trustworthy. The external archive manifest pins the package. The algorithms and the elementary proofs remain open to independent mathematical review. No pass is treated as an independent audit: the author ran these checks, and a separately assigned reviewer must review them.
