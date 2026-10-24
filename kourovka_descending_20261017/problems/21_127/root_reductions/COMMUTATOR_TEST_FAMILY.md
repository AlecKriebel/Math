# Exact commutator test family and a search limitation

Checkpoint 2026-10-24T20:43:09.563159+00:00. Standard derived test family, no novelty or full-resolution claim.

For every group G and product g of k≥1 commutators, scl_G(g)≤k−1/2. An explicit covering construction gives the bound without assuming that surfaces realizing a limiting LP exist.

Represent g by the oriented boundary of a once-punctured genus-k surface. For each odd N≥1, give its first two handle generators the permutations σ(x)=x+1 and τ(x)=2x on Z/N, and give all other handle generators the identity. Since 2 is a unit modulo odd N, these are permutations. Their commutator σ τ σ^−1 τ^−1 is x↦x−1, an N-cycle. The associated surface cover is connected since σ acts transitively; the boundary has a single degree-N lift. Its Euler characteristic is N(1−2k), and its genus is (1+N(2k−1))/2. Compose this cover with the original surface map to K(G,1). The boundary maps to g^N up to orientation/conjugation, so

cl_G(g^N) ≤ N(k−1/2)+1/2.

Dividing by odd N→∞ proves the bound, since the scl limit exists by subadditivity. At k=1 this is the universal bound scl([u,v])≤1/2.

Heuer's sharp RAAG gap, *Gaps in scl for Amalgamated Free Products and RAAGs*, GAFA29(2019),198–237, Theorem7.3 (arXiv1802.01107v3; actual source audited in priority/), says every nonidentity commutator-subgroup element of a RAAG has scl≥1/2. Consequently every nontrivial single commutator in a RAAG has **exactly** scl=1/2. The identity has scl0. By homogeneity, any conjugate of a nonzero mth power of a nontrivial commutator has scl=|m|/2.

Two further elementary consequences give exact controls. First, a nontrivial RAAG commutator cannot be a proper power h^m with |m|>1: its abelianization vanishes, the RAAG abelianization is torsion-free, and therefore h lies in the commutator subgroup. The gap and homogeneity would give 1/2=|m|scl(h)≥|m|/2, a contradiction.

Second, let c be a nontrivial commutator and N≥1. Apply the genus-k bound to an optimal commutator expression for c^N: homogeneity gives N/2=scl(c^N)≤cl(c^N)−1/2. Hence cl(c^N)≥floor(N/2)+1. The odd-degree cover above gives the matching upper bound for odd N. For even N, write c^N=c^(N−1)c and use the odd bound plus one commutator. Thus, for every such c and every N≥1,

cl(c^N)=floor(N/2)+1.

This is an exact universal test family, derived from the credited gap and standard surface covers. No originality is asserted for the no-proper-power or commutator-power consequences.

These exact values hold for commutators of arbitrary group elements, not only generators. They are a useful control for surface constructions and negative searches. Testing many single-commutator words therefore cannot produce irrationality or establish rationality beyond this special class. A hypothetical irrational counterexample is not a conjugate of a power of a single commutator. Products of two or more commutators remain unrestricted by this argument except for the stated upper bound.

The standard group/surface and sharp-gap inputs are fully credited. This note supplies neither a uniform bound on commutator length nor a discrete half-integer spectrum for arbitrary words. Converging rational estimates cannot fill that gap.
