# Third-pass boundary and high-incidence-core partial results

Problem 3251, queue row 1753. Status: unsolved. This edition records the third confirmed substantive pass; at least three passes are confirmed, and the lifetime attempt count is unknown. The parallel structural and boundary investigations and the separate core addendum belong to this one third pass. No fourth-pass material is included.

The target asks whether every finite simple odd-hole-free graph with at least one edge has a two-coloring with no monochromatic maximum clique. A maximum clique means maximum cardinality, not inclusionwise maximal. This is different from perfect divisibility. No full-solution or novelty claim is made.

## Complete mathematical contents

- [Sharp order proof](SHARP_ORDER_PROOFS.md) and [independent audit](SHARP_ORDER_AUDIT.md): if q=chi(H)>r=omega(H), then |H|>=2q-r+1, with equality exactly K_(r-2) joined to C5. If q>=r+2 or H is induced-C5-free, the bound improves by one. Every indivisible graph with clique number k>=3 has at least 3k vertices. In a minimal indivisible graph, each clique-cutset side has at least 3k vertices; |G|>=s+t(3k-s). An edge cutset requires |G|>=6k-2, giving 22 at k=4; an arbitrary clique cutset gives 5k, hence 20 at k=4. These are necessary barriers, with no forcing-side existence or sharpness claim.
- [Complete boundary-extension proof](BOUNDARY_EXTENSION_PROOFS.md): incidence-at-most-two mixed constraints are unsatisfiable exactly when some component is an all-bichromatic size-two odd cycle. Every admissible coloring of any clique boundary extends when all outside vertices lie in at most two maximum cliques. This includes a k-1 versus 1 maximum-clique boundary and needs no odd-hole-free assumption.
- [Complete core addendum](HIGH_INCIDENCE_CORE_PROOFS.md) and [combined independent audit](BOUNDARY_CORE_AUDIT.md): let X be the vertices in at least three distinct maximum cliques of G, counted in G. A prescribed coloring of any P containing X extends if it has no monochromatic (k-1)-clique. An indivisible graph must have omega(G[X])>=k-1, chi(G[X])>=2k-3, |X|>=2k-2 and X noncomplete. Under induced minimality, omega(G[X])=k. These conditions are necessary, not sufficient.

[Exact finite scopes](VERIFICATION_SCOPE.md), [small explicit examples](SMALL_EXAMPLES.md), [sources and credit](SOURCES.md), and [acceptance limits](ACCEPTANCE_AND_SCOPE.md) accompany all five complete proofs and audits.

The intended predecessor is [the initial partial-results edition](../3251_divisibility_partials_20261012/README.md). Sibling links specify the intended repository layout; their inclusion does not assert that either edition has already been published remotely. The known omega<=3 target range is credited to the established coloring result. Hu–Xu–Zhuang's overlapping reductions are credited, without a novelty claim.

This is a prose-only publication candidate. It distributes authored mathematics and audits, public bibliography/source metadata, small explicit examples, and an exact public inventory. It does not distribute third-party manuscript text, original programs, datasets, raw captures, private coordination or operational verification files. The finite checks reported here were audited in their original frozen setting; the prose edition is not a standalone replay package for those exhaustive computations.
