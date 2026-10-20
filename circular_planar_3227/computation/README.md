# Circular-coloring benchmark certificates

## Scope and result

This directory validates a finite-domain search and independently checks explicit
homomorphisms to the circular complete graph K_{20/7}. It does **not** prove a
universal upper bound for triangle-free planar subcubic graphs, nor establish any
new mathematical result. The supplementary exact_dodecahedron_value.md supplies
a self-contained tight-cycle/numerator-bound and rounding argument connecting
the finite certificates to the known exact value chi_c(D)=20/7.

Seven JSON certificates give complete graph edge lists and complete color maps:

| Graph | Vertices | Edges |
|---|---:|---:|
| 5-cycle | 5 | 5 |
| 7-cycle | 7 | 7 |
| cube | 8 | 12 |
| pentagonal prism | 10 | 15 |
| heptagonal prism | 14 | 21 |
| 3-by-3 hexagonal lattice patch | 30 | 38 |
| dodecahedron | 20 | 30 |

All 128 listed edges pass the separate standard-library verifier. NetworkX 3.7
constructs these benchmark graphs and checks planarity, maximum degree at most
three, and zero triangles. The certificate verifier is independent of NetworkX
and independent of the search routine: it checks the stated edge-list graph, not
the correctness of a named graph's library constructor or its planar embedding.

## Definition and exact arithmetic

For integers p >= 2q > 0, the vertices of K_{p/q} are residues 0,...,p-1. Two
residues a,b are adjacent exactly when q <= (a-b mod p) <= p-q. This is equivalent
to minimum cyclic distance at least q. All tests use integer arithmetic. The JSON
color map therefore certifies a homomorphism from its explicit graph to K_{20/7},
and thus an upper bound 20/7 for that graph's circular chromatic number.

## Justification of symmetry reductions

Only the following two target symmetries are used. There is no quotient by
arbitrary color permutations or graph automorphisms.

1. Rotation: Given any solution c and distinguished vertex r=0, replace every
   color c(v) by c(v)-c(r) modulo p. Differences are unchanged, so this is a
   solution with c(r)=0. Consequently fixing the root color to zero does not
   discard all representatives of any solution class.
2. Reflection: Fix one particular neighbor s of r, chosen before search. Since
   rs is an edge and c(r)=0, c(s) is in [q,p-q]. The map a -> -a modulo p
   fixes zero, replaces each edge difference d by p-d, and preserves the
   adjacency condition. At least one of c(s) and p-c(s) is in
   [q,floor(p/2)]. Thus restricting this one neighbor to that interval preserves
   a representative of every solution up to rotation and reflection. The
   neighbor is not required to have color q. If r is isolated, this second
   reduction is simply omitted.

## Search semantics and limitations

Each vertex starts with a finite bit-mask domain. An arc revision removes a
color at u only if no currently allowed color at adjacent v supports it. Any
full solution extending the current domains is therefore preserved. Revisions
are repeated until no domains change or one becomes empty. Branching chooses a
non-singleton domain and tries each remaining color separately. These branches
are disjoint and exhaustive. A singleton leaf is a candidate assignment and is
checked independently before any SAT certificate is written.

For dodecahedron K_{17/6}, the search returned
EXHAUSTED_SEARCH_NOT_FORMAL_CERTIFICATE after 172 recursive nodes and 13,808 arc
revisions (approximately 0.012 seconds in the initial run). The run had a
30-second budget; a timeout would instead return UNKNOWN_TIMEOUT. The initial status alone is not a noncolorability certificate. The subsequently
generated exhaustive branching certificate described below independently
certifies this finite noncolorability assertion. Neither the search nor the
verifier is formally verified in a proof assistant. One failed rational target
alone does not establish exact circular chromatic number 20/7 without further
mathematical arguments (for example, an applicable numerator bound and the
necessary arithmetic). These additional arguments are now supplied in
exact_dodecahedron_value.md; check_exact_benchmark.py verifies that both
certificates use exactly the same graph and checks the requisite rational gap.

## Reproduction

Run from this directory with ordinary Python (do not use -O, because the verifier
uses assertions):

    python verify_certificate.py *_20_7.json
    python test_verifier.py

Optional producer run_search.py in this directory needs NetworkX (tested with version 3.7),
importable in the active Python environment. The certificate verifier and its tests use only the standard
library. Search timings can vary. results.json records original aggregate
results; certificate file hashes are in SHA256SUMS. Both producer scripts
(run_search.py and make_unsat_certificate.py) overwrite output artifacts; run
them only in a disposable copy. They are not required for verification.

## Independently checked finite UNSAT certificate

The file dodecahedron_17_6_unsat.json contains the explicit 20-vertex, 30-edge
graph, the justified root/neighbor symmetry choice, and the complete branching
tree: 172 nodes, including 108 contradiction leaves. make_unsat_certificate.py
produces it with bitsets and a queue of directed arc revisions.

verify_unsat_certificate.py imports no producer code and requires only Python's
standard library. It independently recomputes propagation with sets and full
edge sweeps. At every internal node it checks that the specified branch colors
are distinct and exactly equal to the independently computed remaining domain.
At every leaf it independently establishes a contradiction from the graph,
symmetry restrictions, and the path's assignments. Leaf domain snapshots are
diagnostic only, checked for syntax and the indicated empty domain; their
contents are never trusted as evidence of contradiction. The producer and
checker may reach different first empty domains because their revision orders
differ, which has no bearing on the validity of the independently recomputed
contradiction.

By induction over this finite tree, no assignment satisfying the initial
root/neighbor restrictions exists. The rotation/reflection argument above then
proves that the stated graph has no K_{17/6} homomorphism. This is an exact,
independently checkable finite computational certificate, not a proof-assistant
formalization or a universal graph-class theorem. Reproduction:

    python verify_unsat_certificate.py dodecahedron_17_6_unsat.json
    python test_unsat_verifier.py

Six negative controls remove a branch, duplicate a branch, change the recorded
domain, substitute a false root contradiction, invalidate the symmetry edge,
and change the target to K_{20/7}. All are rejected.

To check the combined finite benchmark, run python check_exact_benchmark.py and
review the mathematical lemmas in exact_dodecahedron_value.md.

## Exact benchmark value

The separate `exact_dodecahedron_value.md` supplies the self-contained tight-cycle numerator bound and rounding argument. Together with these certificates, it proves the known exact benchmark value 20/7; run `check_exact_benchmark.py`. This does not resolve the universal planar-subcubic conjecture or claim novelty. The finite certificates and theoretical bridge together establish only this benchmark value.
