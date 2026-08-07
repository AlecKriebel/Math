# Automatic triangle bound and scope-strengthening review

## Verdict: PASS

A separate pre-submission review tested whether the former hypothesis "at most
one triangle per blob" was genuinely needed. The review did not use the
statistical atlas to establish the graph-theoretic reduction.

For a blob `B`, choosing one parent at each reticulation deletes at most
`r(B)` blob edges and leaves a forest. Hence its cycle rank satisfies
`beta(B) <= r(B) <= 2`. After suppressing degree-two path vertices, a
nontrivial rank-two binary biconnected kernel is cubic. The equations
`e-v+1=2` and `2e=3v` give `v=2,e=3`, so the kernel is theta. If two of its
three cycles are triangles, simplicity permits only path lengths `(1,2,2)`,
that is, `K4` minus one edge.

The two reticulations in this core cannot be adjacent: their common edge either
makes one reticulation the child of the other, or, when subdivided by the root,
gives the root two reticulation children. The only nonadjacent pair is the two
length-two path vertices. Their external bridges cannot enter them, because an
incoming reticulation arc cannot be a bridge in a rooted acyclic network. The
root must therefore lie inside the core. On the pole edge both poles have two
reticulation children; on a pole-reticulation edge the opposite pole has two
reticulation children. Thus no tree-child rooting exists.

Two implementations audit the sole finite local case. The primary Python
program and an independently written C++ program enumerate all internal and
external root sites, all reticulation pairs, and all orientations. Both obtain
25 binary acyclic rooted presentations, seven graph-symmetry orbits, and zero
tree-child presentations. The local failures split into 20
reticulation-child violations and five tree vertices whose children are both
reticulations.

The conclusion is stronger than needed for the paper: every binary standard
semi-directed `W_TC` level-2 topology already has at most one triangle per
blob. Therefore the certified statistical theorem previously stated with the
triangle-count condition applies to all binary standard semi-directed `S_TC`
level-2 networks. The hash-locked base statistical release is not modified;
the new release composes it with this independently checked structural lemma.
