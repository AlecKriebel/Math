# Independent first mathematical assessment

Timestamp: 2026-10-12T15:03:05.680987+00:00. Checkpoint completion estimate: 85% of the requested scientific implication audit, not a probability of correctness or a project approval estimate.

## Claim under test and first finding

The exact candidate is the growing-threshold/growing-seed theorem in `../repaired_candidate_v2/CANDIDATE.md` (SHA-256 `abe51c0360499d3dbd3da392bad37650b10e29a843654dd7e76260ab69c06c7e`). The proposed implication is from the 3 May 2022 v1 of Ganguly--Ramanan, arXiv:2205.01587, Theorem 4.6, Corollaries 4.7 and 5.16, plus elementary limit-tree infection and a deterministic slow diagonal. The candidate's conclusion is treated as a hypothesis throughout.

First independent finding: the implication appears complete. A naive direct encoding of multiedge multiplicities as edge marks FAILS the source's all-graph Assumption 1. The finite configuration multigraph is instead sandwiched between two simple-skeleton comparison processes. This elementary repair eliminates that obstruction and supplies the complete candidate conclusion. The deduction below does not use the candidate's two-root time-ball branching approximation. It requires no quantitative convergence rate, no finite simulation, and no uniform-in-growing-parameters invocation of the hydrodynamic theorem.

This is an implication/priority-relevance assessment, not an operational acceptance, claim of historical exhaustive novelty, or evaluation of any other manuscript. A transparent corollary of a prior general theorem need not have been explicitly stated by that prior author. The first finding is that no new configuration-model stochastic limit theorem is needed for this existence conclusion.

## Exact primary-source coverage

I read the candidate body in full. For the actual 53-page v1 source I read the title/version and abstract, section 2.1 (simple locally finite graph convention), section 2.2 (trajectory topology), section 2.4 (marked local convergence), section 3.1 (local rates/Standing Assumption), section 4.1--4.3 theorem hypotheses and statements, Corollary 4.7 and its proof, Example 4.8, Definition 5.11 and Remarks 5.12--5.13, Definition 5.14, Proposition 5.15 with its proof, and Corollary 5.16 with its proof. Tool extraction coverage is recorded separately. Some initial bundled output was truncated; I re-read the exact theorem hypotheses in a smaller output. I visually inspected complete PDF pages 5, 11, 12, 14, 15, 22 and 24. The PDF was independently extracted with Poppler 26.08.0: its bytes reproduce the supplied .txt exactly. I do not claim to have read every proof in all 53 pages, nor to independently reprove Ganguly--Ramanan's theorem.

No other audit body, parent reduction, verdict or report has been read before this assessment. An initial overbroad `rg --files` exposed other candidate/audit PATH NAMES and a truncated filename listing, not any mathematical contents. This is disclosed rather than hidden under a declaration of blindness. The only mathematical bodies consumed were the exact candidate and the exact primary source. Root instructions and the PDF skill were also read. No Git/index/ref/checkouts/local branch manipulation, remote mutation, publication or outreach was performed.

## 1. Exact finite law and an order-preserving graphical construction

Write states as `2 < 0 < 1`, where 0 is susceptible and 1 and 2 are irreversible infection colors. On a finite multigraph, each physical nonloop edge e has independent type-a exponential traversal cost of rate lambda_a. Only a traversal from a type-a endpoint to a susceptible endpoint can produce a new type-a vertex. Memorylessness gives the generator

`q_v(0 -> a | x) = lambda_a sum_{u != v} m_uv 1{x_u=a}`.

Unactivated weights are independent of the history which determines their first activation. An active exponential residual remains exponential conditional on the observed infection history. Once the other endpoint is infected the edge cannot recolor it. Loops make no transition. All rates are finite because the finite degree list is finite. Uniqueness of the finite-state continuous-time chain therefore identifies the candidate's independent exponential-edge law with this generator.

Equivalently, put independent Poisson arrows of rate lambda_a on both orientations of each physical edge for each type. An arrow u->v of type a sets v to a only if u=a and v=0. At a susceptible--infected edge only the arrow pointing into the susceptible endpoint can act, so this convention does not double the transmission rate. This is a law equivalence; it is not a claim that independent directed clocks equal a fixed undirected weight realization on every cyclic graph.

Every arrow update is monotone for the order `2 < 0 < 1`. For example a type-1 arrow can only raise a susceptible target to 1, and if its source is 1 in a lower configuration it is also 1 in an upper one. A type-2 arrow can only lower a susceptible target to 2; if its source is 2 in an upper configuration it is also 2 in a lower one. The other target cases are checked directly by the three possible states. Common arrows thus preserve initial coordinatewise order at all times. In particular more initial type-2 vertices and fewer initial type-1 vertices cannot increase the type-1 set.

## 2. Multigraph repair, avoiding the unbounded-multiplicity trap

Let B_n contain every vertex incident to a loop or to a pair of parallel nonloop edges. Let H_n be the simple skeleton: remove loops and retain one edge per distinct neighboring pair. Keep each original vertex with its repaired degree d_v as a discrete static mark, even when that is not its skeleton degree. Original initial states are 1 on {d_v>=k}, 2 at W_n, and 0 otherwise (take fixed k>d_0).

Define lower and upper initial states by assigning every vertex in B_n state 2 or state 1, respectively, and leaving the others' initial states unchanged. These bracket the original initial states in `2 < 0 < 1` even when B_n intersects the seed set or contains W_n.

Run both modified processes on the ORIGINAL multigraph with the common arrows. Each vertex in B_n remains permanently in its prescribed color. Every parallel edge has both endpoints in B_n, so none of its arrows can ever change any endpoint in either modified process. A loop never changes any endpoint. Every edge joining B_n to its complement has multiplicity one, since the complement contains no endpoint of any parallel edge. Therefore deleting loops and retaining one representative per parallel group does not change either modified process. Their finite laws are exactly the ordinary two-color Markov infection processes on the SIMPLE skeleton H_n. This is an exact coupling for every finite multigraph, not a probabilistic approximation at a sampled graph.

Thus, with F_n^-(k,t), F_n(k,t), F_n^+(k,t) the fractions of vertices in state 1,

`F_n^-(k,t) <= F_n(k,t) <= F_n^+(k,t)`

pathwise under this coupling. Both bounding simple processes are within the source's actual graph convention.

Why the tempting alternative fails: on a simple edge having multiplicity mark m, the rate lambda_a m has no bound depending only on |cl_v(H)| when m is arbitrary. Even a two-vertex graph violates Assumption 1 uniformly over marks. Our comparison construction has rates independent of the degree/defect marks, and never uses this invalid encoding.

## 3. Marked empirical local convergence in probability

Let mu=E[D], and D* have law P(D*=d)=d P(D=d)/mu. The root of the limit tree has degree D; other vertices have offspring D*-1. The parity repair changes one degree by one. The empirical degree probabilities and empirical mean converge in probability to their iid limits; the empirical second moment also converges. Indeed the repair changes its normalized value by at most `(2 max_i D_i+1)/n = o_P(1)`. Finite second moment implies `max_i D_i=o_P(sqrt(n))` by a union bound and `x^2 P(D>x)->0`. The empirical size-biased law converges in total variation to D* (pointwise convergence on a countable space and normalization suffice).

For any fixed radius r, expose all incident half-edges of all vertices reached through radius r, and the degrees of new partners, enough to detect any loop or parallel edge incident to those vertices. In the limiting tree this exposure has finitely many vertices and a finite sum of their finite degrees almost surely. Choose a deterministic stub-budget M making its tail probability less than epsilon. While the total exposed incident degree is at most M, sampling a partner without replacement differs from a fresh size-biased partner only by vanishing depletion and collision error of order `M^2/(2n-M)` (the total degree is at least 2n). Include every already revealed vertex/frontier target in this budget. The single parity repair is already included in the converging empirical law; it does not require conditioning the sampled iid degrees on an even total.

The stopped exploration consequently converges to the prescribed tree and sees B_n nowhere in radius r with probability tending to one. Then let M grow. For two independent uniform roots the same construction gives two independent limiting trees: expose both bounded neighborhoods jointly, with the same vanishing cross-collision estimate and the same empirical size-biased law. The roots themselves have empirical degree law tending to D. The possible root coincidence has probability 1/n. For every bounded fixed-radius marked observable f, this gives convergence of its empirical expectation and a second moment converging to the square of its limiting expectation. Hence its empirical average converges in probability. This extends to every bounded continuous local observable by fixed-radius approximation on high-probability finite neighborhoods; alternatively use the countable cylinder convergence-determining class for these discrete marks, and tightness supplied by the one-root local convergence. This is the source's Definition 4.4, not merely annealed one-root convergence.

For the singleton W_n, let A_n be the number of repaired degree-d_0 vertices. Then `A_n/n -> P(D=d_0)>0`. Conditional on the degree list and the matching, W_n is uniform among that class. An exposed set of at most M vertices contains W_n with probability at most M/A_n. This tends to zero in probability, and the event A_n=0 is negligible. This remains true though the class selection is degree-conditioned. It does not assume W_n is an unconditioned uniform root. In the limit both bounding processes have initial state

`xi_v = 1{deg_T(v)>=k}`

with 0 elsewhere and no type-2 seed. If full repaired degrees are retained as static marks, those marks equal tree degrees on the limiting tree. Upper/lower defect choices disappear locally. Seed selection still used only the pre-matching degree list in the original candidate; the defect-dependent choices are proof comparisons, not proposed seed selection.

## 4. Verify every needed Ganguly--Ramanan hypothesis

Use discrete state space X={0,1,2}, jumps J={1,2}, and any strictly positive finite driving measure on J with the corresponding intensity normalization. The local rates on every simple marked graph, for all histories and all marks, are

`r_a(G,v,t,x)=lambda_a 1{x_v(t-)=0} sum_{u in N_v(G)}1{x_u(t-)=a}`.

They are Borel measurable, invariant under rooted marked isomorphisms, predictable, and local to the closed one-neighborhood, verifying the Standing Assumption. They obey `r_a <= lambda_max (|cl_v|-1)` for ALL graphs, histories and static marks. One may choose the positive nondecreasing constants `C_l,T=1+lambda_max*l`, independent of T. They ignore environmental marks, so Assumption 2 holds identically. The vertices of H_n lie in the deterministic countable set N and |H_n|=n. All finite graphs meet the finite dissociability requirement. The limit is UGW(D); finite E[D^2] gives E[D*-1]<infinity and Corollary 5.16 supplies almost sure finite dissociability. Marks do not change that property. No third moment is required.

Theorem 4.6 and Corollary 4.7 now give, for each FIXED k>d_0 and FIXED deterministic finite t, convergence in probability of both bounding empirical trajectory measures to the law of the same root trajectory on this marked limit tree.

At time t>0, evaluation on J1 paths is continuous whenever the root does not jump at t. There is no such deterministic-time jump: conditional on its finite root degree D, the root's total rate is bounded by `(lambda_1+lambda_2)D`, and the driving Poisson measures have diffuse time coordinates. For example the expected number of root jumps in an interval of length h is at most `(lambda_1+lambda_2)mu*h`, which rules out an atom at t. Therefore the empirical fraction in state 1 converges to

`p_k(t)=P(X_root^k(t)=1)`.

Sandwiching proves `F_n(k,t)->p_k(t)` in probability for the original exponential-edge multigraph model, with its one conditioned degree-d_0 competitor. Boundedness also gives convergence in L1/expectation. For the candidate conclusion only the lower bound would suffice.

## 5. Elementary tree infection and explicit slow diagonal

Since D>=2 a.s., every non-root vertex has at least one child. Choose a ray from the root by an auxiliary ordering independent of degrees. Its first R non-root total degrees are iid D*. For fixed k, let a_k=P(D*>=k)>0. The chance that none of those R vertices is initially type 1 is `(1-a_k)^R`. A high-degree seed within that segment sends infection back to the root along at most R edges. There is no limiting type 2. Its travel time is at most a sum G_R of R iid rate-lambda_1 exponentials, so `P(G_R>T)<=R/(lambda_1 T)`. Other type-1 arrivals only help. Thus

`1-p_k(T) <= (1-a_k)^R + R/(lambda_1 T)`.

This argument uses a finite path, not a limit of an unjustified infinite shortest-path construction. Well-posedness on the limit tree is supplied by the source. It shows p_k(T)->1 as T->infinity for each fixed k.

Take K_j=d_0+j for j>=2, a_j=P(D*>=K_j)>0, q_j=P(D>=K_j)>0, R_j=ceil(j^2/a_j), and finite strictly increasing T_j with `T_j>=j^2 R_j/lambda_1` and `T_j>=j`. Then the right side is <=2/j^2. By the just-proved fixed-parameter expectation convergence there are deterministic strictly increasing N_j such that for EVERY n>=N_j,

`E[1-F_n(K_j,T_j)] <= 3/j^2`.

Increase N_j also to satisfy `N_j>=4j^2/q_j`, `log N_j>=j T_j`, and `N_j>=j`. Define J(n)=max{j:N_j<=n}, k_n=K_J(n), t_n=T_J(n), with arbitrary early conventions. Then J(n), k_n, t_n tend to infinity and `t_n/log n<=1/J(n)->0`. The expectation bound and Markov inequality give `F_n(k_n,t_n)->1` in probability. Monotonicity of irreversible infection gives the ultimate conclusion. Every sequence is deterministic and depends only on the law and fixed rates, never on the sampled graph or weights.

Before repair the seed count is Binomial(n,q_J), with mean at least 4J^2 and variance at most its mean. Chebyshev gives count >=half the mean with probability >=1-1/J^2; repair only increases it, so |S_n|->infinity. Also `E[|S_n|/n]<=q_J+1/n->0`.

The original seed stub sum has normalized expectation `E[D 1{D>=k_n}]->0` by integrability. If the independent uniform repair vertex crosses the threshold, the additional counted mass is at most D_repair+1; its normalized expectation is at most `(mu+1)/n`. The total stub sum is at least 2n, so the initial stub fraction tends to zero in probability. All type-1 seeds have actual degree >=k_n, while W_n has fixed degree d_0 off a negligible missing-class event.

This proves every stated conclusion, including sublogarithmic time, diverging seed count, vanishing seed density and stub mass, degree-only selection, arbitrary fixed rate disadvantage, and the actual parity-repaired configuration multigraph.

## Remaining falsification work after this seal

Recheck the monotone update argument by exhaustive finite-state checks (diagnostics only), recheck what all-graph boundedness rules out, and compare the v1 statements to a safely acquired actual published/current primary version if useful. Verify source identity and final inventory. No mathematical gap is presently identified; the remaining uncertainty is whether a hidden incompatibility in source hypotheses or the exact finite-law/comparison construction invalidates the reduction. No novelty census beyond this implication is claimed.
