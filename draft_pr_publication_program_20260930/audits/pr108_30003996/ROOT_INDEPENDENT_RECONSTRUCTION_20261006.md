# PR108: independent reconstruction, pending final mathematical gate

Exact reviewed head: `3526d46bf143b08e5055ffa7728c6278e9f958ea`.
Target: 30003996 / OWR-16633-013. Original claim `claimed_solved`, original
effort 2/5, authenticated by the incoming QUEUE row and timestamped research
log. There is no incoming machine-readable status or turn ledger. This audit
adds no central proof-search turn and does not fabricate a historical ledger.

## Literal model and success criterion

I read the complete Kaibel contribution in the pinned Oberwolfach Report
50/2018, printed pp3014–3015. Problem 1 selects ONE undirected spanning tree
and sums costs of its induced arborescence over ALL vertex roots. Each root
has its own vector on BOTH directed versions of every undirected edge.
Problem 2 has a different fixed-root path-cost objective and must not be
substituted. The primary source's wording “(Why)” and the dataset's dated
open label do not establish current openness or novelty.

The candidate decision theorem uses explicit nonnegative integer vectors,
a connected simple graph, and an integer threshold. It suffices for the
literal optimization-hardness question on arbitrary real vectors. NP
membership is asserted only for the finite encoded decision problem. If
arborescences in the source point inward, transposing every coefficient
preserves the objective and reduction.

## All-size threshold argument checked independently

After simplifying repeated literals and tautological clauses, relabel actual
occurring variables densely. For a nontrivial 3-CNF instance with n,m>=1,
use hubs t,f, variable vertices v_i and clause vertices q_j. Edges are tf,
both hub attachments for every variable, and literal incidence edges.
Let B=n+1, K=Bm+n, N=n+m+2. At root t give tf cost0, hub-variable
edges cost1, and clause-variable edges costB, symmetrically. At each clause
root give only variable-to-hub directions the 0/1 literal test; every other
coefficient is0.

For ANY spanning tree, not merely proposed witnesses, let h indicate tf,
p count hub-variable edges and q count clause-variable edges. Connectivity
forces q>=m, and p+q+h=N-1. Thus the root-t contribution is exactly

    p+Bq = K+(1-h)+n(q-m).

Other root contributions are nonnegative. An objective at mostK therefore
forces h=1 and q=m. Every clause is a leaf; deleting the clause leaves
leaves the two hubs joined by tf and exactly one hub attachment per variable.
For a clause root, its selected variable's edge points variable-to-hub;
every other variable edge points hub-to-variable. Thus only its selected
literal contributes and contributes0 precisely when true. The objective
on these structured trees is K plus the number of false selected literals.
Both implications of SAT equivalence follow. No assumption about optimal
trees was used in forcing this form at the decision threshold.

The graph has at most1+2n+3m edges; the explicitly encoded dense table has
2N|E| coefficients, each at mostN. K is polynomially bounded. The same
reduction has polynomial unary length. A tree certificate can be checked
by N traversals and N(N-1) additions of finite integers. Adding1 to EVERY
arc coefficient at EVERY root shifts every tree by N(N-1), so the positive
cost variant is also valid.

Trivial preprocessing can be made explicit using the connected two-vertex
single-edge graph with all coefficients0: threshold0 is a fixed yes
instance and threshold-1 a fixed no instance. Alternatively, if a
nonnegative threshold is desired, set both directional coefficients1 at
each root and use threshold0 for the fixed no instance. Unused or sparse
variable names do not control n; count/relabel actual variable symbols.

## Boundaries and unclaimed extensions

The structured-tree identity is NOT a formula for the global optimum over
unstructured trees. No approximation, planarity, degree, fixed-root-count
or adjacent Problem2 claim has been established. Finite computations support
the proof and do not replace it.

After the fresh all-tree family had independently frozen its proof, I asked
it to challenge a direct parameter consequence of the SAME structural
identity: for any integer B>=2,

    p+Bq = K+(1-h)+(B-1)(q-m),   K=Bm+n.

This would permit B=2 and costs0,1,2. It is an audit robustness observation,
not a new central route or a priority-cleared contribution. The family has
reported agreement and a B=1 failure control; its artifacts still require
root readback before any promotion. The original B=n+1 argument remains
the current candidate.

## Evidence and present clearance

Original native bodies and their Git object IDs are bound by
`original_source_authentication_20261006/ORIGINAL_BLOB_MANIFEST.json`.
Raw dataset statement, SQLite import and submitted source agree; absent
joined prior report is authenticated as the importer-normalized empty
object. Review hash:
`9a2816afbdd3750d36f550dc6e91c7201aa024344a7b83fdb420aafe6c86df0d`.
Primary PDF custody reuses identical previously retrieved primary bodies;
it is accurately labeled as custody reuse, not a new network retrieval.

Three materially distinct fresh families are running: arbitrary-tree
threshold and boundary falsification; independent dense-cost reproduction
and checker controls; literal primary-source and encoding audit. Their
initial reports support the argument. The reproduction family identified
assert-based guards that disappear under Python -O; an explicit guard
repair, fresh actual runs and full final report authentication are pending.

Source authentication100%; mathematical workflow30%; priority0%; PR108
workflow10%; program16/99 (16.16%). NO publication, novelty, merge or closure
clearance is granted by this interim note.
