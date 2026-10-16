# Source contract frozen before candidate reading

Timestamp: 2026-10-15 13:54 UTC. Auditor role: independent source-first analytic adversary. Target: PR885 / PID9700042 only. No candidate proof, audit, disposition, or prior verdict has been read at this freeze.

Primary source: David Aldous, “A discrete Hammersley process as an extreme case of oriented percolation flows,” https://www.stat.berkeley.edu/~aldous/Research/OP/hammersley_flow.html . Independently retrieved through the web tool and read in full; the parent's raw HTML was also read in full. Raw-receipt authentication is recorded separately.

## Exact mathematical contract

For integer n >= 2, the vertices are {0,...,n-1}^2. Directed nearest-neighbor edges point right or up, are independent, and have capacity 1 with probability p and capacity 0 with probability 1-p. The source set is the bottom and left boundary excluding (n-1,0) and (0,n-1). Its union includes (0,0) once. The sink set is the full top and right boundary. Thus the two sets are disjoint and zero-length source-to-sink paths cannot contribute. Corners do not carry extra unit capacities; only physical lattice edges do. Shared vertices are allowed, shared edges are not. No bound on the number of paths using a source or sink vertex appears beyond incident edge capacities.

V(n,p) is the maximum count of such open directed source-to-sink paths. The source states L1 convergence V(n,p)/(2n) -> v(p), with deterministic v(p). This existence is part of the source's setup, not the target new conclusion. At p=1 the natural finite comparison is V(n,1)=2(n-1); hence O(1) boundary corrections disappear after division by 2n.

The target is exactly

    lim_{q downarrow 0} (1-v(1-q))/sqrt(2q) = 1.

The order is n -> infinity at fixed q first, followed by q -> 0. A finite-size dilute scaling, an unproved interchange of limits, or a non-sharp bound does not establish this. Any replacement lattice must be coupled with a proved o(n sqrt(q)) error in the relevant ordered limits, or with uniform inequalities strong enough to pass those limits. The leading constant and the factor 2 in the normalization are essential.

The source defines U(n,p) as the minimum number of edge-disjoint directed source-to-sink paths covering every closed edge, and informally states the complement relation up to negligible terms. A candidate using this relation must derive a precise finite identity or adequate error bound. Ordinary vertex-poset chain cover is not automatically an edge-disjoint path cover. Source/sink boundary conventions and corner exclusions must survive any complementation or planar-dual argument.

## Source statements versus heuristics

The page explicitly announces heuristics before its Poisson approximation. Its Poisson scaling display uses delta^(-1/2)n, although dimensionally scaling rate delta to rate 1 uses sqrt(delta)n. Its displayed U*(m,1)~m also requires independent checking: a minimum northeast chain cover of Poisson points equals a maximum southeast antichain and the standard square longest-chain constant is 2. These apparent heuristic normalization errors cannot be accepted as axioms. They do not change the exact written conjecture above.

## Independently chosen falsification mechanisms

1. All-open and very small n boundary tests: check baseline 2(n-1), source/sink disjointness, corner connectors, and possible unintended zero-length paths.
2. Complementation obstruction: find a configuration for which minimizing edge-disjoint closed-edge cover differs from the open-flow deficit by more than the candidate's explicit allowance; scrutinize mandatory side edges and balanced-flow conservation.
3. Dilute-limit obstruction: a local Poisson approximation alone is insufficient on arbitrarily large squares. Test whether blocking, conditioning, or concatenation costs remain o(sqrt(q)) after taking n -> infinity first.
4. Sharp constant obstruction: both lattice edge orientations contribute, so dropping one orientation or counting a two-channel block as one can alter sqrt(2q). Check Poisson scaling and any antichain conversion independently.
5. Multiplicity and degeneracy obstruction: coincident sites, horizontal/vertical ties, defect marks, repeated microcells, and boundary records may defeat an asserted strict-poset or disjoint-occurrence comparison.
6. Imported theorem obstruction: verify exact independence, monotonicity, measurable witness/disjointness, tail speed, area normalization, and applicable dimension/asymptotic regime in the primary source. Finite computation cannot establish these universal claims.

## Acceptance standard

Reconstruct a deterministic finite reduction, both sharp asymptotic inequalities, and the ordered limits. Label imported results and their hypotheses. Any unsupported step carrying the central dilute-limit difficulty leaves the target unverified even when finite checks pass. Only the two named current claim bodies will be read next; independent analysis will be frozen before any older audit/disposition.
