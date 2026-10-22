# PR1407 / 1200024: independent original-scope, correctness and priority audit

The unrestricted vertex-transitive counterexample survives this audit. For the binary grandparent graph G and its simple graph square H=G²,

E deg_FUSF(G)(o)=(24−sqrt(2))/7>161/50,
E deg_FUSF(H)(o)≤3208526010913748780/10^18<321/100.

Under the explicitly stated standard forest-derived convention b_F(X)=E deg_FUSF(X)(o)/2−1, this proves b_F(G)−b_F(G²)>1/200. No fatal mathematical gap or substantive repair was found. The negative conclusion concerns arbitrary vertex-transitive graphs; it does not refute the already affirmative Cayley/common-unimodular-action case. The original source does not print the normalization formula, so that qualification should remain visible.

Priority is unestablished. No authenticated existing publication/deposit of the full graph-square negative or this exact comparison was found. The grandparent family and the free/wired/electrical machinery are established prior material; no dependency DOI is a publication of this full comparison. No four-cell already_solved publication row is proposed, and this PR or its audit acceptances must not be treated as an existing publication. This is an independent AI mathematical/source audit, not human refereeing or formal proof-assistant verification.

Assigned audit100%; parent sweep80% at closure. All work is confined to this folder, all18 head blobs are privately pinned, and all prior closed audits are preserved. No author program was executed; only newly authored exact controls were run. No external communication, provider/row/publication/PR write, Git index/ref mutation or STATE edit occurred.

## 1. Input binding and fresh duplicate gate

Target head a2a3eaf94ab8605717e6c9a6a5b4972f4495059e,18 paths. INPUT_RECEIPT.json binds path, git blob, SHA256 and length; PRIVATE_INPUT retains exact bytes, including the compressed inert flow certificate and the author's nested manifest. The main canonical PUBLICATION/QUEUE/catalog records were searched read only: the target is queued on main, while the exact pinned PR QUEUE row1893 claims solved. These are distinct observations, not authorization to alter either.

Before substantive mathematics, the2026-10-22T14:23:13.104454Z GWS gate resolved numeric sheet1254632077 and read all43 columns A:AQ,191 rows. Response SHA256446ba179ebbb49bee9cf4cf5619a09b1ea2e41fdb5c8ce2431ec44b5e8d86371. The single broad native hit124 concerned Habert–Pocchiola's double-permutation/fibration problem, and its full native row was read and found distinct. GWS_DUPLICATE_CHECK and LOCAL_PUBLICATION_DUPLICATE_CHECK record the actual account/canonical gate. Related DOI/source leads were treated as claims pending primary-body inspection.

The complete mathematical RESULT, grandparent_proof, grandparent_exact_resistance, SQUARE_BOUND, unimodular_projection_comparison and operator_notes were read, as was the prior ADVERSARIAL_REVIEW. Acceptance reports supplied no mathematical authority. Actual program/certificate execution was limited to this audit's independent code; author scripts were pinned but not executed.

## 2. Actual original and scope adjudication

Primary original: Miklós Abért, Some questions,2November2010, Question24, printed4. The author homepage links https://www.renyi.hu/~abert/questions.pdf . This audit freshly recovered valid PDF bytes102130, SHA256576000d7a042147021311cb8fd944e414d8d49db73642fcaf06dd9c2d90aa4e1; the whole seven-page text was read and printed4 visually inspected. This succeeds beyond the earlier package's web-text-only inspection/failed shell HTML retrieval; those historical source limits are not silently presented as this audit's limits.

The question explicitly describes an arbitrary vertex-transitive graph and asks equality between G and G² for the first L² Betti number obtained from expected degree in a free spanning forest. Section4 is headed Vertex transitive graphs. There is no global unimodularity restriction in the introduction or preceding sections. The immediately preceding Question23 separately says its assertion is known for unimodular vertex-transitive graphs, and Question22 explicitly says unimodular random network. Thus importing an implicit unimodularity hypothesis into Question24 is not supported by the inspected primary text. The adjacent author comment says the Cayley case is true because the number depends only on the group and not the generating set. This also supports the usual simple graph power on the same vertex set, rather than a Cartesian product square, which would change the group.

The source does not specify the normalization or fully define locally finite/connected conventions. The candidate explicitly uses b_F=Edeg/2−1, the standard normalization matching the Cayley identity. The proof establishes unequal expected degrees directly and therefore disproves square invariance for that stated forest-derived invariant. It should not claim the original printed this formula. Its graph is infinite, connected, simple, unweighted and locally finite, satisfying the usual restrictive graph conventions; no pathological failure of those conventions is involved. The term Betti is not replaced by finite graph cycle rank, a clique-complex Betti number, or a different weighted/nonunimodular invariant.

Question25's request for a forest proof of finite-index multiplicativity is separate. The inspected EulerSolve2026 adjacent-question page addresses25, not24. The original's warning that questions may have been solved later is retained as a priority uncertainty, not a request for outreach; no outreach was prepared or initiated.

## 3. Foundation imports, free versus wired, and factors of two

The actual corrected author-hosted BLPS, Uniform Spanning Forests, Ann.Probab.29(2001),1–65, version27January2009, https://rdlyons.pages.iu.edu/pdf/usf.pdf , was freshly retrieved and pinned. The electrical discussion/finite Kirchhoff Theorem4.1, §5 free/wired construction, Theorem6.4, Proposition7.1, the proof of Theorem7.3 and infinite transfer-current Theorem7.8 were read. Those primary bodies establish:

* A finite unit-conductance connected network has P(e in UST)=R(e−,e+), with Thomson's principle for finite unit flows.
* Free finite induced exhaustions converge, independent of exhaustion. The free edge current is projection onto the orthogonal complement of the closed finite-cycle space. Proposition7.1 identifies the limiting free current; Theorem7.8 gives its marginal/determinantal interpretation.
* Wired current is the minimum-energy unit flow among all square-summable infinite-network flows; it can have strictly smaller energy than free current. These notions cannot be interchanged.
* WUSF expected degree is2 on every transitive reversible network, by Theorem6.4; no unimodularity assumption is needed there. This theorem says nothing forcing FUSF expected degree2.

For the negative proof only single-edge marginals and finite Thomson/Rayleigh are needed. No MTP is used to compute the negative gap. The energy of a flow is the sum of its squared currents over each unoriented edge once. There is no extra1/2 in the certificate energy; the sole division by2 appears in the b_F convention. For general conductances the marginal is conductance times resistance; here every conductance is1.

BLPS §5 initially formulates exhaustion with induced subgraphs. The candidate's H_{n,n} need not be so declared. This does not create a gap: its finite connected edge sets increase and eventually contain every fixed finite induced ball, and are contained in a sufficiently large such ball. Rayleigh monotonicity squeezes its limiting resistance to the same free induced-exhaustion limit. Proposition7.1 explicitly covers finite subnetworks. The alternative induced exhaustion below removes even that minor convention issue.

## 4. The graph and its full automorphism group

Fix an end xi of the(q+1)-regular tree T, q≥2, and let p(v) be the unique neighbor toward xi. Define G_q by all unordered pairs {v,p(v)} and {v,p²(v)}. The original tree edges remain, so the graph is connected. There are no loops or multiple simple edges because T is a tree. Its degree is(q+1)+(q²+1), and its end-stabilizer acts transitively, proving vertex transitivity. The square is also simple and transitive under this same action.

The stronger full-group nonunimodularity assertion is valid. For a tree edge x–p(x), its common G-neighbors are p²(x) and the q children of x, exactly q+1 triangles. For the grandparent edge x–p²(x), only p(x) is a common neighbor, giving one triangle. Thus graph automorphisms recover the original T-edge relation. Among x's recovered T-neighbors, the G-induced graph is K_{1,q}, centered at p(x): the other q vertices are x's children and are joined only to p(x). For q≥2 the center is unique. Every automorphism preserves p, hence the end, and conversely all end-preserving tree automorphisms preserve G_q. Thus Aut(G_q) is exactly the closed end-stabilizer.

The stabilizer of x fixes p(x), while the stabilizer of p(x) is transitive on its q children, including x. The paired suborbit sizes are1 andq. The standard locally compact transitive-graph unimodularity criterion therefore fails for the full automorphism group. Tangv2 §2.3 Proposition2.2 and the accompanying modular/MTP statements were inspected as a primary source for this criterion. For q=2 the graph has degree8 and paired sizes1,2. A regular tree alone would have a unimodular full automorphism group despite admitting a nonunimodular transitive subgroup; the recovery argument above specifically prevents that mistake here.

## 5. First exact resistance derivation: free branches and diagonal exhaustion

Use q≥2 until the final substitution. Let B_m(u;a,b) consist of u and its descendants down to m generations, with its parent a and grandparent b as two terminals. Include all G_q edges from these interior vertices within that set and omit the terminal edge a–b. There are no other exits from the untruncated descendant part: every edge moves one or two generations along a comparable ancestor ray. Different child branches share only their terminals, with no cross-branch edge. Free truncation deletes all outside-descendant edges, without identifying any boundary vertices.

Let k_m be its terminal conductance. B_0 is the path a–u–b of two unit edges, so k_0=1/2. For B_{m+1}, each of u's q child branches has terminals u,a and conductance k_m. Hence u–a has conductance1+qk_m, while u–b has conductance1; series reduction gives

k_{m+1}=(1+qk_m)/(2+qk_m).

The increasing map sends the increasing sequence from1/2 into[1/2,1], so it converges. Its positive fixed point k solves qk²+(2−q)k−1=0, with a unique positive root. Let A=1+qk. The fixed-point equation gives k=A/(1+A).

Fix the ancestral ray x_i=p^i(o). H_{m,n}, n≥2, consists of x_0,...,x_n with their parent and skip-one edges, q depth-m branches at x_0 with terminals x_0,x_1, and(q−1) depth-m side branches at each x_i,1≤i<n, with terminals x_i,x_{i+1}. The child x_{i−1} is excluded as it lies on the spine. It is finite connected and increasing in m,n. Every fixed off-spine vertex has a finite ancestor-merger point x_i and finite descendant depth; consequently H_{n,n} exhausts every vertex and edge. Omitting side branches at the current top x_n is temporary and disappears in later diagonal terms. Nothing is wired at the top or leaves.

Reduce the descendant branches. The bottom conductance x_0–x_1 is A_m=1+qk_m. Every higher adjacent conductance is c_m=1+(q−1)k_m; every skip-one conductance is1. In the upper suffix x_1,...,x_n the conductance B_{m,n} from x_1 to x_2 is

B_{m,n}=T_{c_m}^{n−2}(c_m),    T_c(t)=c+t/(1+t).

For n=2 it is c_m; adding an upper triangular cell places c_m in parallel with a unit edge in series with the previous upper conductance, proving the recurrence. This is a two-terminal reduction on a triangular chain, not an assumption that arbitrary branches remain independent in a random spanning tree.

On t≥c_m≥1, T'_c(t)≤1/4. Both its fixed point and all iterates stay in a common bounded interval for fixed q. Therefore the distance from B_{m,n} to its fixed point is at most C_q4^{−(n−2)}, uniformly in m. The positive fixed point is the positive root of B²−c_mB−c_m=0 and depends continuously on c_m. Since c_m→c=1+(q−1)k, the actual diagonal B_{n,n} converges to the root B of B=c+B/(1+B). This root is A, because c=A−k and k=A/(1+A). This justifies the diagonal limit directly, without interchanging two unsupported infinite limits.

The three-terminal reduced triangle has conductances A_m,B_{m,n},1 on x_0x_1,x_1x_2,x_0x_2. Parallel/series formulas give

R_{H_{m,n}}(x_0,x_1)=1/[A_m+B_{m,n}/(1+B_{m,n})],
R_{H_{m,n}}(x_0,x_2)=1/[1+A_mB_{m,n}/(A_m+B_{m,n})].

Passing along H_{n,n} and using the genuine free exhaustion yields

R_F(o,p(o))=1/[1+(q+1)k],
R_F(o,p²(o))=2/[3+qk].

The end-preserving transitive group is transitive on all unoriented tree edges and on all unoriented grandparent edges. At o there are q+1 tree edges and q²+1 grandparent edges. Kirchhoff marginals therefore give the degree expectation by summing those two resistances with those multiplicities. No unimodular edge-intensity counting is invoked.

For q=2, k=1/sqrt(2), A=1+sqrt(2), and elementary rationalization gives

R_F(tree)=(3sqrt(2)−2)/7,
R_F(grandparent)=(6−2sqrt(2))/7,
Edeg_FUSF(G)(o)=3R_F(tree)+5R_F(grandparent)=(24−sqrt(2))/7.

Since(73/50)²>2, sqrt(2)<73/50 and the expectation is strictly greater than(24−73/50)/7=161/50. This is an exact infinite-volume result, not a numerical extrapolation from a finite graph.

## 6. Independent induced-exhaustion derivation and finite guards

Let v_j=p^j(o) and S_n be all descendants of v_n down to depth2n, with G_n=G[S_n]. These finite induced connected sets increase: in S_{n+1} old depths increase by1 while permitted depth increases by2. Every fixed vertex's end ray merges with o's, so the sets exhaust T.

In the binary case let c_0=1 and c_m=1+2c_{m−1}/(1+c_{m−1}). This is the conductance of a depth-m descendant tree part including its direct parent edge but excluding the root's grandparent edge. Each child contributes its reduced edge c_{m−1} in series with a unit edge to the parent's parent. With a_m=1+c_{m−1}/(1+c_{m−1}), eliminating all off-spine descendants in G_n leaves:

v_0v_1 conductance c_n;
v_jv_{j+1} conductance a_{n+j},1≤j<n;
v_jv_{j+2} conductance1,0≤j≤n−2.

At v_0 both children are off-spine; at v_j, j≥1, only one is. The side-child descendant depth there is n+j−1, which explains the index. At the top v_n the remaining off-spine part has a single attachment v_n and has no effect on terminal resistances; it must not be spuriously given a second terminal outside G_n.

For the suffix, u_{n−1,n}=a_{2n−1} and u_{j,n}=a_{n+j}+u_{j+1,n}/(1+u_{j+1,n}) for1≤j≤n−2. Thus the same triangle formulas use c_n,u_{1,n},1. The map c↦1+2c/(1+c) contracts on[1,infinity) by at most1/2, with positive fixed point c=1+sqrt(2). All suffix maps contract by at most1/4 on their relevant domain. Their coefficient indices are at least n+1, so with epsilon_n=sup_{m≥n+1}|a_m−a|,

|u_{1,n}−c|≤(4/3)epsilon_n+C4^{−(n−2)}→0,

using c=a+c/(1+c). This independently recovers both free resistances and the expectation.

New independent_reduction_check.py builds actual finite descendant graphs from ancestor relations and performs global rational Laplacian Schur elimination, without importing either author's recurrence/graph code. Eight two-terminal branch cases(q=2,3;m=0,...,3) and three full induced cases(q,n)=(2,2),(2,3),(3,2) agree exactly. The largest is127 vertices, chosen to check the actual finite interfaces/indexing, not as an expansive toy computation. Examples: the binary n=2 triangle is(7/3,17/10,1), resistances27/80 and121/240; n=3 has triangle(12/5,6236/2669,1). These diagnostics support the finite identities. The proofs above supply all depths and the infinite limit.

## 7. Square graph, complete neighborhood and independent inert certificate check

Use the radius10 ball in the underlying T about o. Its vertices are root(), words with three first choices0,1,2 and two later choices0,1, in breadth-first lexicographic order. Thus it has1+3(2^10−1)=3070 vertices. The distinguished end is the all-zero ray. For an all-zero word the end-parent is its zero extension; otherwise it is the word prefix. This agrees at root and at every vertex: the tree path toward the zero ray first removes the nonzero tail, then proceeds up that ray. A boundary end-parent outside the ball is simply absent.

Let K be the induced G-subgraph on this ball and J=K². Every J edge is an actual H=G² edge because its witnessing K path is a G path. Conversely any H-neighbor of o is reached by at most two G steps, each corresponding to at most two T edges. The whole witnessing tree walk lies in the radius4 ball, already inside K. Hence J contains every H edge at o, even though J need not be the full induced H-subgraph on its vertex set.

The40 root neighbors also admit a complete structural count:4 strict ancestors;2+4+8+16=30 strict descendants at depths1–4;1 sibling;1 uncle;2 children of the sibling;2 children of the uncle. These disjoint cases exhaust one/two G-step possibilities. It is not enough to certify only a selected subset of root edges.

The compressed certificate is exactly165241 bytes with SHA2566573c55f2998f4576a050a0757ca74f1cae9cadfa96ec61c69b181c530f79c4f. It is read as inert gzip/JSON data. New independent_flow_check.py constructs the underlying coordinate tree, its full infinite grandparent-neighbor relation, the endpoint-restricted K, and then its square. It verifies undirected adjacency, reconstructs all19931 edges and their order, and separately computes the infinite root-neighborhood to check completeness and size40. It does not import or execute the candidate's checker, numerical generator or earlier replay.

For every one of40 supplied flows, the checker reads all19931 numerators as actual integers, hence797240 integer entries total. With common denominator D=10^9 it checks every vertex divergence: +D at the specified neighbor v, −D at o, zero at all3068 other vertices. This is122800 exact divergence equations. It recomputes every energy by summing integer squares once per unoriented edge and matches the40 supplied numerators and total:

sum_v Energy(theta_v)=3208526010913748780/10^18<321/100.

No solve residual, numerical tolerance, optimization of the energy, floating-point eigensolver or approximate current is trusted. A feasible flow is sufficient; near-optimality is unnecessary. Reversing all flow directions preserves energy and exchanges source/sink, harmless for symmetric resistance. The checker also independently verifies the root-local triangle counts1,3 and the unique-parent K_{1,2} reconstruction.

Four deliberate mathematical corruptions are detected: changed current violating divergence, wrong terminal, missing edge and changed energy. The independent reduction code additionally checks that the free two-edge leaf branch has resistance2 rather than the wired terminal identification's0. These controls support the verification logic; the closed input SHA is the actual identity binding.

## 8. Why the finite certificate proves an infinite free upper bound

For each actual H-root neighbor v, the rational certificate is a unit flow theta_v in finite J. By finite Thomson, R_J(o,v)≤Energy(theta_v). Take a connected finite induced exhaustion H_n of H. For all sufficiently large n it contains the same J as a subgraph; extend theta_v by0 on added edges. It remains a unit flow with exactly the same energy, and finite Thomson or Rayleigh gives R_{H_n}(o,v)≤R_J(o,v)≤Energy(theta_v). Taking the decreasing free-exhaustion limit proves R_H^F(o,v)≤Energy(theta_v).

Kirchhoff's finite edge identity and the free weak limit give P({o,v} in FUSF_H)=R_H^F(o,v). Summing over the complete40 root neighbors proves the stated upper bound on Edeg_FUSF(H). All40 may use different flows; no joint-flow feasibility is required for marginal summation.

This argument is valid precisely because the flows have finite support. Replacing free resistance by the unconstrained minimum over arbitrary square-summable infinite-network flows would produce wired resistance and invalidate the desired upper bound. That replacement is not made. The boundary vertices of J are never shorted to each other or infinity, and no wired lower bound is passed off as a free upper bound.

Combining the strict original lower bound161/50 with the strict square upper bound321/100 gives

b_F(G)−b_F(H)=(Edeg_FUSF(G)−Edeg_FUSF(H))/2
 >(161/50−321/100)/2=1/200.

There is no need to compute the square's exact infinite expectation. The exact original expression and the verified finite witnesses suffice for a full negative answer under the stated convention.

## 9. The separate affirmative unimodular comparison

The auxiliary positive result also checks out with the usual closed locally compact unimodular transitive action convention. Let Gamma act transitively and unimodularly on G; the same Gamma acts on H=G². For one chosen orientation per unoriented edge, let Z_G and Z_H be the cycle-orthogonal l²-gradient spaces. A cycle-orthogonal field determines a global vertex potential modulo constants by path integration; its gradient has finite energy. Thus the description includes all finite-energy gradients, not merely closure of gradients of finitely supported functions(which would give the wired space).

If G has degree d, each old edge lies in2(d−1) unoriented nonbacktracking length-two paths. Bound the squared endpoint difference on any such path by twice the sum of the two edge differences squared, and overcount all paths if an added edge has several representations. This proves

E_G(f)≤E_H(f)≤[1+4(d−1)]E_G(f)=(4d−3)E_G(f).

Hence T:d_G f↦d_H f is a bounded Gamma-equivariant bijection Z_G→Z_H with bounded inverse by restriction. Its polar part U is an equivariant unitary between those closed spaces. Extend by0 on Z_G-perp. Then U*U=P_G and UU*=P_H.

Define the nonnegative transport

m(x,y)=(1/4)sum_{e incident x}sum_{f incident y}|<U chi_e,chi_f>|².

Automorphisms change orientation signs but preserve these squares. Each edge has two endpoints, so Parseval gives

sum_y m(o,y)=(1/2)sum_{e incident o}<P_G chi_e,chi_e>,
sum_x m(x,o)=(1/2)sum_{f incident o}<P_H chi_f,chi_f>.

Both are finite, bounded by half the corresponding graph degree. Ordinary unimodular mass transport equates them. Transfer-current diagonals are FUSF marginals, so the expected degrees and b_F agree. Tang§2.3's tilted formula reduces to this identity when the modular function is1; Gaboriau's actual§2.4/Proposition2.9/Definition2.10 explicitly assumes transitive unimodular H. The hypothesis is neither absent nor transferable to the counterexample.

Equivariant Hilbert-space isomorphism alone still exists in the nonunimodular case; equality of these rooted diagonal sums does not follow. The operator_notes projection defect is consistent: if Z_H is the graph of the new-edge extension L and A=(I+L*L)^−1, then its difference is tau_new(LAL*)−tau_old(L*LA), with tau half the root incidence sum. Rectangular trace cyclicity is exactly the unavailable step without ordinary MTP. Thus the negative result does not contradict energy equivalence or unitary equivalence.

The zero-invariant statement is also sound: equivalent Dirichlet norms preserve the closure of finitely supported potentials modulo constants, hence the harmonic Dirichlet quotient vanishes for G iff for H. BLPS7.3 identifies this with FUSF=WUSF, and6.4 gives WUSF expected degree2 for all transitive reversible graphs. Positivity and transitivity of the harmonic projection make b_F=0 equivalent to its vanishing. This preserves only zero versus positive values, not equality of positive rooted diagonal sums. Neither auxiliary comparison is needed for the strict counterexample.

## 10. Primary priority evidence and exact limits

Tang, Weights of uniform spanning forests on nonunimodular transitive graphs, arXiv1908.09889v2(3December2020), was freshly retrieved as valid71-page PDF. Its introduction, §2.1/§2.3 and complete§5.2, printed40–48, including all statements/proofs/remarks5.4–5.12, were read. It defines exactly this grandparent model, proves FUSF connectivity and branching number>1, and uses finite ball resistances for path bounds. It does not in that inspected body give the exact root expected degree, the two conductance recurrences above or an expectation comparison with the simple graph square. No literal earlier exact formula was found by text searches. Those established family/structural results are credited; their DOI is not full-target coverage. The DOI10.1214/21-EJP709 redirected to Electronic Journal of Probability volume26(2021), but the publisher response was a1159-byte HTML challenge rather than an accessible scholarly body. The final journal edition was therefore not read; arXivv2 is the actual inspected full-text edition. A secondary2022 metadata date was not adopted as authoritative publication dating.

Pete–Timár, arXiv2006.06387v2(24January2021), published Ann.Probab.50(2022),2218–2243, DOI10.1214/22-AOP1581, is a relevant known noninvariance result. Its actual introduction/Theorems1.1–1.2 were inspected, not merely its title. It varies FUSF component counts even between Cayley graphs of one group and explicitly points out that their expected degree still depends only on the group. It also constructs light FUSF components in another nonunimodular graph. Component count, lightness and expected degree are different quantities. This is not an authenticated earlier answer to Question24; its long construction/proof is not claimed independently audited here.

Gaboriau, Invariant Percolation and Harmonic Dirichlet Functions, arXivmath/0405458v3, actual§2.4 and preceding MTP discussion, supplies the unimodular harmonic-projection invariant. It does not justify extending tracial dimension invariance to this nonunimodular root intensity. BLPS2001/corrected2009 supplies the general free/wired framework and zero-property rough-isometry invariance, not the new positive-value square gap.

A further primary2013 source was read through publisher PDF text: Russell Lyons's complete contribution in OWR42/2013, printed2391–2392, https://ems.press/content/serial-article-files/46473 . It starts with Cayley graphs and states EdegFUSF=2beta_1(group)+2, supporting the normalization and known Cayley restriction. It does not discuss the unrestricted nonunimodular square counterexample. The entire48-page report was not read or locally pinned; only the identified contribution was inspected through web text, so no local full-report hash is claimed.

The actual EulerSolve page https://eulersolve.org/papers/amr-011-0025/ was found for the adjacent AbértQuestion25. Its stated result is a forest proof of finite-index multiplicativity, with DOI10.5281/zenodo.22245583. Only its target/scope/record were inspected; its mathematical proof was not audited and its DOI is not full Question24 coverage. A single analogous inferred0024 URL was inaccessible through the web tool. That is an access failure, not proof that no such paper exists. The inspected related-paper list did not reveal an exact0024 record; it is not an exhaustive deposit search.

Bounded searches used exact1200024/AMR-011-0024, original Question24/Abért/Abert, grandparent plus expected degree/resistance/square, free-uniform/free-spanning-forest plus graph powers/graph square/Betti/nonunimodular, and the exact candidate title/value. No authenticated earlier full-target theorem/deposit was found. Searches returned much irrelevant material, not evidence of absence. The author-hosted whole Lyons–Peres book was not fetched or claimed read: it is a large source, and earlier size/access limits remain a literature-coverage limit. Unindexed papers, other editions, books/exercises, theses, talks or alternative terminology could contain the result. Historical firstness and current worldwide openness are not certified. Outside input could help assess those limits; no outreach was prepared or initiated.

The strongest verified statement is therefore a complete mathematical negative under the explicit forest-derived convention and literal arbitrary-VT scope, with exact witnesses and proof. The remaining gap is priority coverage, not a missing resistance estimate or a restriction to a weaker graph class. Absence of a full-target prior does not turn the proof into a partial result, and it does not establish novelty.

## 11. Check artifacts and closure boundary

independent_flow_check.py and independent_reduction_check.py are new, standard-library-only code. Their full outputs agree normally, with -O and with -OO; runtime guards are explicit exceptions. Flow output SHA256154127a084246165fcda25a9002b319f122bff5d8bdb99fb3a8c68a2e3a16dd7; reduction output SHA2566c2b5555d79a81abc88bc3bef8c450a3cba94fb810574b0e7b274fab697e02c9. Their receipts record all mode executions. No compiler/package/cache installation, numerical generator or author replay is needed.

The exact original formula rests on the written all-depth reductions and contraction/exhaustion proofs; its finite guards do not replace them. The square bound rests on the finite integer certificate plus the all-graph free-exhaustion transfer, not finite numerical evidence alone. Raw scholarly bodies, extracted text and pinned inputs are private; retrieving a whole PDF does not imply every page was read. SOURCE_INDEX records the exact inspection scopes and access failures. RESULT's historical proof map mentions excluded optional generator/log files; PROJECTION explains their exclusion. This audit uses the actual18-path inventory and its own concrete replay artifacts, so those historical names are not missing mathematical assumptions.

verify_seal.py checks closed membership, bytes/SHA256, file/directory modes and nanosecond mtimes, all18 original git-show bindings and private pins, without author execution. It rejects nine mutated manifests in memory. This is an integrity check, not a mathematical proof checker or signature. Only this folder's root MANIFEST is excluded from its own payload hashes; the nested claimant manifest remains included. The separately reported root-manifest SHA anchors the closed artifact. No writes occur after sealing; subsequent verification is read only.
