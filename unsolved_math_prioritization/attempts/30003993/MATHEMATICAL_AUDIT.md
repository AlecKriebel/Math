# Independent mathematical audit: directed linear k-cut limit-3 partial

Problem 30003993 / OWR-16633-010. Audit date: 10 October 2026.

Public proof-only edition. This AI-assisted audit is unrefereed; acceptance is not external human peer review, journal acceptance or formal proof-assistant certification.

## Verdict and exact scope

**ACCEPT the stated partial theorem. The original problem remains OPEN.**

The reviewed construction gives, for every integer k >= 2, a finite simple directed graph with k distinct ordered terminals and unit edge costs, with

- C_k = sum from l=1 to k of (k-l+1) floor(k/l);
- integer optimum C_k-k^2;
- a feasible vector for the original edge path-distance LP of objective C_k/3.

Consequently its actual integrality gap is at least 3(1-k^2/C_k), and these lower bounds tend to 3. This establishes a lower limit of at least 3 for the actual gaps; it does not establish that the actual gaps converge to 3. The proof does not establish an unbounded gap, a universal upper bound, or the exact fractional optimum. No priority or novelty claim is accepted.

This edition binds the distributed [PROOF.md](PROOF.md): 9,897 bytes, SHA-256 `e23c1b69c878f943bcfd381f9d1025b0a3a512bc2eb8014a3d46106987e84d73`. The complete accepted mathematical arguments and substantive audit findings are preserved. Edition changes are editorial, with no new mathematical correction. A packaging checker issue identified during the independent audit was corrected by that audit before final acceptance; it did not affect the proof, source records or mathematical certificates.

## 1. Same originating problem and source credit

Chandra Chekuri's contribution, [Open Problem: Approximation and Integrality Gap for Linear k-Cut](https://ems.press/content/serial-article-files/46772), Oberwolfach Report 50/2018, printed p. 3013 (PDF p. 45), specifies deleting edges of a directed graph to block every lower-to-higher ordered-terminal path. Its unresolved question is whether the natural LP gap is bounded uniformly in k or is unbounded. The candidate uses this edge-cardinality model and all its forbidden terminal pairs, not a fixed-k, undirected, or arbitrary-demand substitute.

The author-hosted journal version of Kristóf Bérczi, Karthekeyan Chandrasekaran, Tamás Király and Vivek Madan, [A tight sqrt(2)-approximation for linear 3-cut](https://karthik.ise.illinois.edu/pubs/linear-3-cut.pdf), Mathematical Programming 184 (2020), 411–443, [DOI](https://doi.org/10.1007/s10107-019-01417-9), was independently inspected at PDF pp. 2, 4, 5, 7 and 30. It distinguishes node and edge models, describes the distance relaxation, and reports general-k bounds ceil(log2 k) above and 2(1-1/k) below; its tight sqrt(2) result is for k=3. The ceiling in the logarithmic bound must be retained when quoting this source. The source still treats general k as open.

The related [cluster-vertex-deletion paper](https://researchmgt.monash.edu/ws/portalfiles/portal/367152543/341613069_oa.pdf) by Manuel Aprile, Matthew Drescher, Samuel Fiorini and Tony Huynh discusses a gap of 3 for the general induced-P3 covering LP. The [interval-graph deletion paper](https://arxiv.org/abs/2210.07699) by Dibyayan Chakraborty, L. Sunil Chandran, Sajith Padinhatteeri and Raji R. Pillai concerns related algorithmic problems. Neither supplies a premise needed in the audited proof, nor is either taken as establishing this particular interval-weight construction's priority. Bounded current searches found no resolution or matching theorem, which is not evidence of exhaustive novelty clearance.

[SOURCE_METADATA.json](SOURCE_METADATA.json) contains public URLs, source hashes where historically verified, and recorded inspection scope. No third-party source PDF, extracted source text or private coordination material is distributed.

## 2. Auxiliary paths and the fractional witness

Write I=[a_I,b_I] for a nonempty integer interval in {0,...,k-1}. The auxiliary graph has an interval vertex of weight floor(k/|I|), arcs I->J for distinct intervals with b_I>=a_J, entries s_i->I when i>=b_I, and exits I->s_j when a_I>=j.

There are no terminal-to-terminal arcs. A terminal-free segment with one interval satisfies i>=b_I>=a_I>=j. A segment with two intervals satisfies i>=b_I>=a_J>=j. Neither can increase terminal index. Thus a terminal-free forward segment uses at least three interval traversals. This argument is valid for walks too; repeated vertices cannot create a one- or two-traversal exception.

For any walk from s_i to s_j with i<j, list all terminal visits in order. If every consecutive pair were nonincreasing, its last terminal index would be at most its first. At least one consecutive pair increases, so the corresponding terminal-free segment has at least three interval traversals. Assigning each interval length 1/3 is therefore feasible, including for paths that visit other terminals internally. This avoids silently treating terminals as sources or sinks, which the original model does not require.

## 3. Every retained family is covered

Two interval vertices have arcs in both directions exactly when the intervals intersect. Therefore every connected component of their undirected intersection graph is strongly connected. Each component's interval union is an interval: along an intersection chain, successive unions remain intervals. Different components have disjoint unions and are totally ordered from left to right. All intercomponent arcs point left. Consequently no directed cycle joins components, and these are precisely the strongly connected components of the retained interval graph.

For a component A, let alpha=max a_I and beta=min b_I. If beta<alpha, take I attaining beta and J attaining alpha. A directed interval path I->...->J exists within the component. Prepend s_beta->I and append J->s_alpha. This is a forbidden forward path, so every feasible family must have alpha<=beta in each component.

Conversely, assume alpha<=beta for every component. If a terminal-free path enters A through I from s_i, then i>=b_I>=alpha. If it exits A to s_j through J, j<=a_J<=alpha<=i. If it crosses components, it moves strictly left. Every endpoint in a later component is then below the minimum endpoint of the initial component and hence below alpha<=i. It cannot exit at j>i in that case either. Finally, splitting at internal terminal visits excludes all forward paths, as in Section 2.

Thus feasibility is equivalent to each intersection component having a common point. This is a characterization of arbitrary interval-vertex deletion sets; it assumes no terminal labels, canonical cut form, or restricted choice of retained intervals.

## 4. Exact auxiliary integer optimum

The total interval weight is C_k. For a feasible component with union [L,R], put n=R-L+1 and choose an integer p in its common intersection; integer endpoints ensure such a p exists. A length-l interval containing p has its starting point among p-l+1,...,p, so there are at most l such intervals. All intervals in this component have length at most n. Hence its retained weight is at most

sum from l=1 to n of l floor(k/l) <= kn.

Different component unions are disjoint subsets of the k integer points. Their n values sum to at most k, so total retained weight is at most k^2. Retaining precisely all k singleton intervals is feasible, has retained weight k^2, and attains the bound. Thus the minimum deleted interval weight is exactly C_k-k^2.

This also proves C_k>k^2 for every k>=2: the singleton terms already sum to k^2, and a nonsingleton interval has positive weight.

## 5. Finite simple unweighted conversion and arbitrary edge cuts

Split every interval I into I^- and I^+ with central edge I^- -> I^+ of integer cost c_I. Every other auxiliary arc becomes an edge of cost M=C_k+1. Replace a cost-w edge u->v by w length-two routes u->z->v, each with its own private internal vertex. All final edges cost one.

All routes and bundles have distinct edges. Their private vertices preclude parallel edges, loops, and connections between unrelated route interiors. Terminals are unchanged and distinct. The construction therefore is a finite simple directed graph in the original model; neither infinite protection nor weighted final edges remain.

Breaking one leg of every nonsingleton central route leaves exactly the singleton auxiliary structure and gives a feasible cut of size C_k-k^2. Let D be any optimum final edge cut. Its size is at most C_k-k^2<C_k+1=M. Thus D cannot break every route in any protected bundle: that would require at least M distinct deletions. Define an interval to be retained when its central bundle has at least one complete surviving route. If the resulting retained auxiliary family admitted a forbidden path, every needed protected and central connection could be lifted through a surviving route. This would give a forbidden walk, and hence a forbidden path, in the graph after D, a contradiction.

The fully broken central bundles therefore define a feasible auxiliary deletion set. A fully broken bundle for I costs at least c_I distinct deleted edges, regardless of which route legs are cut. Distinct bundles have disjoint edges, so |D| is at least the sum of these c_I values, which Section 4 bounds below by C_k-k^2. Together with the exhibited cut this proves equality.

The lower bound is about genuinely arbitrary final edge cuts, including partial protection damage, mixed first/second legs, and deletions in different kinds of bundles. Such cuts are not assumed canonical; the bound itself shows why inexpensive cuts must preserve all protected connections.

## 6. Fractional objective and projection in the final graph

Give each first edge of a central route length 1/3 and every other final edge length zero. There are exactly sum_I c_I=C_k central routes, so the unit-edge LP objective is C_k/3, not 2C_k/3 and not an unweighted count of auxiliary interval vertices.

A path between terminals cannot start or end inside a route. Each private route vertex has exactly its designated incoming and outgoing edge, so every visit to such a vertex traverses the whole route. Contracting those visits projects the path to a walk in the split graph. The only exits from I^- are central routes and the only entries to I^+ are central routes. Hence every interval traversal contributes one charged central route. Splitting the projected walk at terminal visits and applying Section 2 gives at least three central traversals somewhere on any forward path, for total length at least one. Therefore the vector is feasible for all original path constraints.

There is a forward path for k>=2, using [0,0], [0,1], [1,1] from s_0 to s_1 and any corresponding routes. Thus the nonnegative unit-edge LP has positive optimum (indeed at least 1), so division by it is legitimate. Since LP<=C_k/3, the ratio inequality has the claimed direction.

## 7. Asymptotic bound and size

The elementary inequality floor(k/l)>=k/l-1 gives

C_k >= k((k+1)H_k-k) - k(k+1)/2,

where H_k=sum from l=1 to k of 1/l. Dividing by k^2 gives a lower bound (1+1/k)H_k-3/2-1/(2k), which tends to infinity. Consequently k^2/C_k tends to zero and 3(1-k^2/C_k) tends to 3. The proof uses the known divergence of the harmonic series, not numerical extrapolation.

There are O(k^2) interval vertices, O(k^4) nonsplitting connections, and C_k<=k^2 H_k=O(k^2 log k). Replacing each protected connection by C_k+1 private routes therefore produces O(k^6 log k) vertices and edges. This is a polynomial-size construction, although full expansion becomes impractically large quickly. Symbolic formulas alone do not falsely claim those large graphs were materialized.

## 8. Independent exact computations and controls

The independent mathematical checker imported no candidate code. It indexed intervals by length, used bitset transitive closure for full terminal reachability, union-find for intersection components, and heap-based shortest paths in independently generated expanded graphs. All decisions used integers or exact fractions. Normal and Python -O executions produced identical certificate bytes. The following are historical supplementary checks recorded by the audit; this edition does not distribute the programs, generated certificates or raw outputs.

- Exhausted all 33,864 retained families for k=2,3,4,5. Direct reachability agrees with the common-point characterization. Maximum retained weights are 4,9,16,25.
- Independently expanded graphs for k=2 through 6. Every graph is simple and loopless. The stated cut is feasible with the correct cardinality, and every forward terminal shortest distance is exactly 3 in units of 1/3.
- The k=6 graph has 30,605 vertices and 61,114 edges; its witnessed optimal cut size is 29. Optimality at this size rests on the universal argument, not exhaustive arbitrary-edge enumeration.
- For k=2 and k=3, a complete path-branching decision procedure searches every possible arbitrary edge cut within budgets 0 and 2, respectively. It finds none, independently confirming optima 1 and 3. The k=3 search visits 135 distinct deletion sets; branching on every edge of a currently surviving forbidden path is complete even though it need not enumerate all edge subsets.
- Checked harmonic bounds exactly for every k=2 through 300. Independently interchanged the two finite sums defining C_k at specified values through k=1,000,000.
- Negative controls: zeroing the [0,1] central charge yields distance 2/3; adding an illegal terminal-entry shortcut yields distance 1/3; reducing protected multiplicities to 1 at k=3 permits a two-edge cut, below the claimed protected-model optimum 3. Each is detected.
- Rejected the non-Helly overlap chain [0,0],[0,1],[1,1]. Accepted a valid optimal cut mixing first and second route legs, and an explicit forward walk through an internal terminal with a repeated interval traversal.

The candidate's own mathematical checker was additionally rerun during the audit in normal and optimized modes and reproduced its stored certificate. This cross-check is supplemental. The complete universal arguments above support the mathematical acceptance; independent code supplied further finite error checks, and no theorem claim requires the omitted code or certificate.

## 9. Integrity findings and limits

An early candidate inventory checker skipped files with a manifest or sidecar basename even when they were unlisted nested files. A copied-packet mutation demonstrated the issue. The independent audit authored a packaging-only correction to that checker, excluding only the two exact root-relative sidecars and rejecting symbolic links, including directory links. The original proof author did not make this correction. The audit then regenerated the candidate inventory metadata and external seal. Every other candidate payload file, including the mathematical proof, source records and mathematical certificates, remained byte-for-byte unchanged. This is an explicit exception to preservation of the original candidate package, not a mathematical correction or a claim that the entire original package was untouched. Exact correction records and post-correction adversarial checks were retained in the non-distributed audit evidence. The independent inventory checker verified every included file's byte count and SHA-256 against an external manifest digest.

Hash integrity does not prove mathematics. Finite tests do not prove the theorem for all k. This audit supplies complete universal arguments for that purpose and uses tests to probe likely implementation and modeling errors. It has not established priority, exhaustive current literature coverage, or a solution to the original absolute-constant-versus-unbounded question. No mathematical blocker remains for the precisely stated partial theorem.

Edition preparation rechecked the frozen accepted byte identities and publication integrity. It did not rerun the original mathematical programs or perform new scholarly retrieval, source-text inspection or literature search. All recorded mathematical computations and scholarly inspections above are historical. The complete proof and universal audit arguments stand independently of omitted programs, raw outputs, generated certificates or datasets.
