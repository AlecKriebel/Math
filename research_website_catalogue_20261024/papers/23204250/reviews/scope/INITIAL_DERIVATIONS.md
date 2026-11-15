# Paper-first independent analytic reconstruction — record23204250

Private while root139 comparison gate is CLOSED. Entire actual published PDF6pages, controlling TeX189lines and6 fresh own individual rasters have been personally read. No supplied scientific programme/result, archived review/triage, current peer/root opinion, or new foreign scientific body has been read. This is an independent scope/analytic lane. Its mechanism is a uniform exact convex-analytic and constructive proof, not the opposite lane's finite gadget enumeration or native replay. No scientific conclusion or novelty is assumed.

## Exact target, model and success criteria

P_TSP(N) is the convex hull of ordinary undirected Hamiltonian-cycle incidence vectors in K_N, N≥3, one coordinate per unordered edge. P_PM(n) is the perfect-matching polytope in K_n for even n≥2. The size xc_psd,R(P) is the least positive matrix order r with P=π(L∩S_+^r), L affine and π affine. Affine equations are free. Multiple PSD blocks are charged by their sum of orders via a block-diagonal embedding, not by the maximum block order. The theorem states constants c>0,N0 such that for every integer N≥N0,

2^(cN) ≤ xc_psd,R(P_TSP(N)) ≤ 2(N−1)+(N−1)(N−2)2^(N−3).

This is a statement about exact real semidefinite lifts, not approximate relaxations, a particular hierarchy, bit complexity, arbitrary TSP algorithms, P versus NP, complex cones or stable-set polytopes. Success requires the entire original theorem, including every sufficiently large city count and the stated explicit upper bound, rather than a subsequence or a narrowed surrogate. A substantive defect in a central imported theorem or bridge must be documented and deferred, not silently repaired by replacing the target.

The central external premise is the exponential real PSD-rank theorem for shifted matching matrices from the pinned OpenAI126 manuscript. It is not proved in the six-page target. The initial can verify all local implications uniformly while retaining that exact central gap; actual primary proof/hypotheses/edition interfaces must be read after this initial and own proof/control results are frozen. The target's assertions that earlier audits examined it are author assertions, not independent evidence here.

## Family1 — affine exact-lift convention, unrestricted auxiliary variables

Suppose an LMI is T(z)⪰0 with arbitrary auxiliary real coordinates z and affine output U(z), and its image is the bounded nonempty polytope P. Parameterize any auxiliary affine equalities first. Choose one feasible z0. If k lies in the kernel of T's linear part, z0+λk is feasible for all real λ, since its matrix is unchanged. Boundedness of P forces U_lin(k)=0. Thus U_lin factors through T_lin, and U factors affinely on the affine image of T. Extend the resulting affine map from that affine subspace to all real symmetric matrices using a linear complement. The section L is precisely im_aff T, so its exact PSD image is P. No Slater point or boundedness of the lifted section is needed.

Nonemptiness matters to choose z0; boundedness matters to kill output along kernel directions. An unbounded output z from the constant1×1 PSD matrix T(z)=1 is an immediate counterexample to the factoring conclusion without boundedness. Counting only the maximum PSD block would make an arbitrary linear extension's scalar nonnegativity blocks size1, so it cannot be the convention used in an exponential order lower bound. A block-diagonal section of total order Σr_i gives exactly the sum convention without adding unconstrained off-diagonal entries.

Falsifiers: a hidden non-affine output, a lift with no chosen vertex preimages, finite-width restrictions on allegedly unrestricted kernel variables, omitted affine equations, or substituting complex Hermitian matrices. The main theorem is only under its exact real convention.

## Family2 — shifted matching matrix and quantifier boundary

For odd U⊂[n] and a perfect matching M, A_n(ρ)_(U,M)=|M∩δ(U)|−1+ρ. Crossing parity is odd: summing matching degrees in U gives |U|=2|M∩E(U)|+|M∩δ(U)|. Thus the crossing count is at least1, A_n(0) is nonnegative, and each odd-cut slack is tight by choosing exactly one crossing edge and pairing the even remainders internally. U and its complement are nonempty because n is even and |U| odd. For n=2 some/all slacks are0; the asymptotic input's threshold is not omitted.

The target states the imported quantifiers as ∃γ>0 such that for every fixedρ∈(0,1), ∃n0(ρ), ∀even n≥n0(ρ), rank_psd,R A_n(ρ)≥2^(γn). The constantγ is written uniformly inρ, while the threshold may depend onρ. Actual imported Theorem1.1 must be checked for this exact quantifier order rather than casually replacing γ by γ(ρ). The target ultimately needsρ=1/2, but a stronger inaccurately stated imported claim must not be silently narrowed away. Exponential versus merely superpolynomial is another central interface: no Lean statement claiming only growth beyond every polynomial certifies 2^(γn).

Endpointρ=1 has an explicit small factorization: index diagonal entries by edges e of K_n, take F_U=diag(1[e∈δ(U)]) and G_M=diag(1[e∈M]). Their trace product is the crossing count=A_n(1). Forρ>1, adding one scalar constant block gives order binom(n,2)+1. Forρ<0 a tight row has a negative entry and is outside the nonnegative PSD-factorization framework. Thus0<ρ<1 is a real boundary, not a dispensable word. No uniform conclusion atρ=1 follows from thresholds that may diverge asρ→1.

Falsifiers: a theorem for a different matrix/row range, different cone/normalization, odd n, or onlyρ depending on n; a missing −1 shift; or confusing a PSD factorization order with its squared parameter count. Actual foreign body remains unread at this initial.

## Family3 — one-block shift and exact asymptotic loss

If A_n(0) has real PSD factors F_U,G_M of order r, block matrices diag(F_U,ρ),diag(G_M,1) are PSD forρ≥0 and have trace product A_n(0)+ρ. Hence rank_psd A_n(ρ)≤rank_psd A_n(0)+1, equivalently rank_psd A_n(0)≥rank_psd A_n(ρ)−1. This is an upper construction for the shifted matrix and a lower transfer to the unshifted one. It does not transfer a shifted lower bound to a slack matrix without paying the additive1.

Atρ=1/2 and after the external premise, r0≥2^(γn)−1. Forγn≥2, write x=2^(γn/2)≥2; then x²−1≥x. Thus after increasing the even threshold one may choose a=γ/2>0 and obtain rank_psd A_n(0)≥2^(an). Constants remain unspecified existential constants. No floating estimate or explicitγ is supplied by the target. A finer threshold is unnecessary and is not a new research direction.

Falsifiers: inequality reversal, an uncharged scalar PSD block, moving −1 into the exponent incorrectly, claiming the bound at all small n, or using theρ=1 polynomial factorization as an exponential premise. A direct exact block-trace control can check signs and dimensions but cannot establish the external asymptotic rank theorem.

## Family4 — common support and a genuinely closed evaluation cone

For any exact affine lift of a finite polytope choose one PSD preimage B_v for each vertex. Let J=Σ_v B_v and W=range J. For PSD summands, ker J=∩ker B_v: if x^T Jx=0, each nonnegative x^T B_vx=0, and PSD implies B_vx=0. Thus every B_v is supported in W. Orthogonal compression A↦P_W A P_W preserves PSD and all values tr(AB_v). On W, J is positive definite, with minimum eigenvalueλ>0.

The evaluation cone C={(tr(AB_v))_v:A⪰0 on W} is closed. If its evaluation vectors converge, each coordinate is nonnegative and their sum tr(AJ) is bounded. Since J⪰λI_W, tr A≤λ^-1 tr(AJ). A PSD matrix has Frobenius norm≤tr A, so the representing A's form a bounded set in a finite-dimensional closed cone. A subsequence converges to A⪰0 giving the limiting evaluations. A choice of representatives for each vector is enough; no uniqueness or canonical factor is required. If W=0, all B_v=0, so all vertices have the same affine image and every tight slack is0, represented by A=0.

This is not the false general assertion that every linear image of the PSD cone is closed. A separate negative control is the image of [[x,y],[y,z]]⪰0 under(x,y): matrices [[1/k,1],[1,k]] are PSD, their outputs tend to(0,1), but PSD with x=0 forces y=0. The unbounded trace k+1/k is exactly what the finite PSD evaluation/coercivity condition excludes. The second functional here is not a PSD B_v, so it is not a counterexample to the lemma. A support-kernel negative control can also add arbitrarily large PSD mass on W⊥ without changing evaluations; compression is essential before asserting bounded representatives.

Falsifiers: using uncompressed trace bounds when J is singular, assuming arbitrary cone projections closed, requiring lifted-section boundedness, or applying compactness in an infinite-dimensional cone. This family is the principal uniform analytic route and is independent of enumerating any tour or matching.

## Family5 — tight slack certificate without strict feasibility

For a valid nonnegative affine slack f on P tight at vertex v0, set y_v=f(v). The dual of C consists exactly of c=(c_v) with Z=Σ c_v B_v⪰0, by PSD self-duality on W. For arbitrary such c let s=Σc_v, t=|s|+1 and q=s+t>0. The matrix X=(Z+tB_v0)/q is PSD. It lies in the original affine L because it is the affine combination Σ(c_v+t1[v=v0])B_v/q whose coefficients sum to1; individual coefficients need not be nonnegative. Thus exactness of the lift gives π(X)∈P and f(π(X))≥0. Affineness and f(v0)=0 give q f(πX)=Σ c_v f(v). So every c∈C* pairs nonnegatively with y. Closed-cone separation and Family4 give y∈C**=C. Extend the representing matrix by0 on W⊥, preserving order r.

There is no assumption that all feasible matrices lie on W or that compressing an arbitrary feasible X preserves L. Compression is only for representing the evaluation cone; the affine-combination witness X uses the actual original B_v and lies in L directly. This distinction avoids an unsupported facial-reduction/Slater claim. The zero-dimensional support and one-vertex polytope are covered separately. Tightness is used at exactly the tB_v0 correction: a non-tight f would contribute a constant, so the present argument must not just discard it.

Applying this separately to every odd U with common vertex factors B_M constructs F_U⪰0 satisfying tr(F_U B_M)=A_n(0)_(U,M). Different row certificates are allowed, while the chosen vertex lifts remain shared. Hence every order-r exact lift of the matching polytope gives an order≤r factorization of the entire odd-cut matrix. A full irredundant facet description is unnecessary. Together with the shift, this proves the uniform local reduction xc_psd,R P_PM(n)≥2^(an) conditional on the exact external premise.

Falsifiers: pairwise certificates with different column lifts, using weak conic duality as if it guaranteed attainment, an unsupported Slater point, a correction matrix not in the affine slice, or loss of a constant term in f. The direct finite-evaluation separation proof should be compared with actual upstream affine-certificate and cone-factorization bodies after own results freeze.

## Family6 — nonempty faces and affine images preserve the order

If F={x∈P:h(x)=b} is an exposed nonempty face, add the affine equality h(πX)=b to L. The resulting image is exactly F: an image point satisfies the supporting equality, and every F point had a lift already. Composing π with any affine T gives exactly T(F). No new PSD coordinate is added, so xc(T(F))≤xc(F)≤xc(P). Finite intersections of supporting equalities can be exposed by summing their nonnegative slacks. None of this needs a strictly feasible lift or a bounded feasible section. Empty faces would be outside the stated nonempty-polytope convention.

Falsifiers: arbitrary subsets called faces, composing a non-affine projection, dimension charging for free affine equations, or using the reverse inequality. This local deduction does not depend on classical LP extension-complexity theorems as an unverified black box, although their historical reduction credit must be checked in actual sources later.

## Family7 — uniform3n gadget and surjectivity

In three n-vertex layers L,D,R, restrict TSP(3n) to the graph containing cliques on L and R and forced two-edge paths l_i−d_i−r_i. Zeroing all excluded nonnegative coordinates exposes a face. Each d_i has degree2 in any face tour, forcing both incident path edges. Each l_i and r_i consequently has one residual same-layer edge; these are perfect matchings A,B. Contracting the n forced paths gives an n-vertex degree2 multigraph A∪B, with the two colors retained even when the underlying edge repeats. A Hamiltonian face tour is equivalent to connectedness of that colored union.

For any given A, order its k=n/2 disjoint pairs(a_j,b_j) and set B={(b_j,a_(j+1))}, cyclic j. Each vertex occurs once in B and the alternating traversal a1,b1,…,ak,bk,a1 covers every index. Expanding the paths yields one genuine Hamiltonian cycle on3n distinct cities. At n=2, A and B are parallel colored edges after contraction but expand to a six-city cycle. Treating this as a forbidden simple two-cycle would incorrectly discard the boundary case. Thus projection onto the L matching coordinates maps the whole face onto P_PM(n); injectivity is neither needed nor generally true.

For disconnected A∪B, expanding gives disjoint subtours, not a Hamiltonian cycle. For example A=B at n=4 has two connected components. The construction uses a chosen B completing each A, not a claim that every ordered pair of matchings is a tour. Falsifiers include disconnectedness, omitted colors, forbidden extra cross edges or projection to an arbitrary2-regular graph instead of a matching.

## Family8 — uniform2n contraction and missing-ones negative family

Use two n-layers L,R, force every diagonal l_i r_i to1 and every non-diagonal cross edge to0. The functional Σ_diag x_e−Σ_nondiagcross x_e≤n is valid on TSP(2n). Since every x_e∈[0,1], its deficit is Σ_diag(1−x_e)+Σ_nondiagcross x_e, a sum of nonnegative terms. Equality therefore forces each displayed condition. The previous completion gives a nonempty face. Degree2 then forces a same-layer perfect matching at every vertex, and contracting diagonals gives the same connected colored A∪B. Hence xc(TSP(2n))≥xc(PM(n)). At n=2 the expanded cycle is l1,l2,r2,r1,l1, so no three-city degeneracy occurs.

Forcing only cross zeros is inadequate. At n=4 the cycle l1,l2,l3,l4,r4,r3,r2,r1,l1 has no non-diagonal cross edge but its L projection is a length3 path, whose two internal vertices have degree2. The missing diagonal-one constraints are the precise failed hypothesis. This is a uniform constructive counterexample to an invalid shortcut, not a finite exhaustive replay.

No priority is assumed for this elementary contraction. It improves only the constant lost in the exponent, not the external central rank mechanism. Falsifiers: a non-exposed subset, claiming n bound forces each diagonal without coordinate upper bounds, or forgetting that a tour's global connectedness is essential after contraction.

## Family9 — padding at every N≥m≥3

For N=m the identity suffices. Otherwise expand old city v through the forced path v,z1,…,zt with t=N−m≥1, imposed by equality in Σ_path x_e≤t. Each path coordinate is≤1, so equality forces all. Expanding any edge vw of any old tour proves nonemptiness. In any face tour, internal path vertices have degree2 already; only v and zt have one free neighbour in W=old\{v}. Those two neighbours are distinct: if both were w, the path plus w would close a cycle excluding at least one other old vertex because m≥3. This would contradict the single Hamiltonian cycle. Contracting the path yields an ordinary old Hamiltonian cycle rather than a doubled edge.

The linear map is y_ij=x_ij for i,j∈W and y_vj=x_vj+x_zt,j. On integral tours the distinct-neighbour argument makes the latter coordinates0/1; it is not assumed that sums of two arbitrary0/1 coordinates are automatically0/1. Each old tour has an expansion and each face tour contracts to an old tour; convexity and linearity give equality of polytopes. The m=3 boundary is valid; m=2 is intentionally excluded. No injectivity of this projection is claimed.

Falsifiers: a disconnected subtour after contraction, an endpoint using the same old neighbour, omitting the sum in the projection, or proving only monotonicity along a restricted parity sequence. The theorem's quantifier every sufficiently large N relies on this family.

## Family10 — integer rounding and uniform exponential rate

Let n1 be an even matching threshold and a>0 the matching exponent. For arbitrary large integer N take n=2 floor(N/4), even, with2n≤N. The2n construction plus padding gives xc(TSP(N))≥2^[2a floor(N/4)] whenever n≥n1. Since n>N/2−2, every fixed c<a/2 works eventually. A concrete safe choice is c=a/3 and N≥max(12,2n1+4): N≥12 gives n≥N/3, and the second threshold ensures n≥n1. Using the3n construction instead, n=2 floor(N/6) gives any eventual c<a/3. The strict and eventual qualifiers are not removed at small city counts.

This is a uniform all-residue-class argument, not an empirical fit to a few N. The rateγ remains an unspecified imported positive constant; neither source proof nor local rounding supplies a numerical lower constant without its hypotheses. Falsifiers: choosing odd n, n too large to embed, neglecting N≡1,2,3 mod4, replacing a limit exponent by a minimum valid at all N, or accidentally multiplying city count by the number of tour variables binom(N,2).

## Family11 — exact flow upper bound and diagonal SDP embedding

Fix rootcity1 and Q of size q=N−1≥2. The subset-state DAG has states(S,i) with∅≠S⊂Q,i∈S. Every middle arc increases |S| by1, so it is acyclic. Source arcs start at singletons, middle arcs append a new city, and sink arcs leave full sets. A source-to-sink path visits each Q city exactly once. Its edge-label sum is a Hamiltonian cycle, and every undirected Hamiltonian cycle has exactly its two root-based orientations as paths, including N=3.

Every nonnegative unit flow decomposes into such paths: start on a positive source arc and follow positive outgoing arcs by conservation until sink; no repeated vertex can trap it in a DAG. Subtract the minimum positive arc flow on that path. At least one arc leaves the positive support. Repeat at most finitely many times. A residual positive flow with zero source supply would contain a minimal positive vertex in the DAG with no incoming positive flow, contradicting conservation. Thus no residual circulation survives, and extracted coefficients sum to1. This is an exact convex-hull description, not a relaxation containing disconnected tours.

There are Σ_nonempty S |S|=q2^(q−1) states plus source/sink. Middle arcs are counted by ordered i≠j and arbitrary subsets of the other q−2 cities: q(q−1)2^(q−2). Add q source and q sink arcs to obtain m_N=2q+q(q−1)2^(q−2). Diagonal X⪰0 of order m_N is exactly a nonnegative arc vector after imposing zero off-diagonal entries; conservation and unit-supply equations are affine. The label projection gives exactly TSP(N). Thus xc≤m_N=2(N−1)+(N−1)(N−2)2^(N−3), with log2(m_N)=N+O(log N)=O(N). Together with the conditional lower it gives the original2^Θ(N).

No minimality of this explicit upper lift is claimed, e.g. TSP(3) is a point while this construction still uses six arcs. No P versus NP assertion follows because the formulation itself is exponentially large. The controls for this lane should focus on analytic cone/trace/order and symbolic counting identities, not repeat native finite tour enumeration. Falsifiers: cycles in the state graph, unbounded circulations, counting undirected states instead of directed arcs, identifying PSD with entrywise nonnegativity without imposing diagonal structure, or changing block-order convention.

## Family12 — exact dependency and formalization/credit interfaces

After this initial and own proof/control freeze, the designated sole raw acquisition owner should provide only actual raw bodies and full transport custody for the exact pinned matching manuscript and its mathematical affine-certificate definitions. Its full proof's local contraction, multiplicity, orthogonal splitting, Fourier smoothing, parity functional, normalization and truncation bridges require personal inspection. No archived reviewer assertions or finite matrix experiments can substitute for the central universal lower-bound argument. Actual Lean source bodies/docs are necessary to distinguish superpolynomial statements from the claimed exponential estimate; no Lean build or supplied code execution belongs to this lane.

Actual primary passages of Yannakakis Theorem2 at printed454 and Rothvoss's matching-to-TSP discussion are needed for classical reduction credit, not as black boxes replacing the explicit gadgets above. The actual cone-factorization definition/hypotheses and LRS versus LPDWY correction bodies should be checked for precise lower-bound exponent/category/edition. Held–Karp credit is bounded to the classical dynamic-programming idea; our full constructive upper proof does not rely on an unavailable original theorem. No current worldwide firstness or exhaustive absence claim is assumed from the author's literature search. The original text's historical audit and priority narrative is not a current scientific opinion supplied to this lane.

Falsifiers: only superpolynomial instead of exponential input, approximation instead of exact lift, complex instead of real factors, theorem normalization changed by a row rescaling, insufficient dimension-independent constants, or a correction contradicting a claimed historical bound. A central gap triggers deferred disposition with exact evidence, not an extended repair or an unannounced narrower paper.

## Family13 — source/edition/rights and exposure honesty

Native version is ABSENT. The actual printed paper says October6,2026 and has no version line; no default1.0 is created. Source acquisition's false/null UNREAD flags remain historical facts and are never rewritten after this review. The complete immutable source is104 files=101payloads+3 exact terminals,13directories;3 native assets include2 ZIP containers with35 total regular occurrences. There is one six-page native PDF and one controlling189-line TeX, with no additional distinct controlling manuscript or embedded PDF. The published text claims CC BY4.0 for newly authored prose/documentation and MIT for verification code; actual license files/asset scopes remain to be inspected later, rather than assuming identical terms across assets or borrowing another record's broad-code license.

Prior related background consists of general mathematical knowledge of PSD cones, finite-dimensional linear algebra, graph polytopes and exact asymptotic notation. This lane previously performed unrelated source/editorial/integration work and row137 group/cost review; those packets remain immutable and row137 findings remain withheld. The old unrelated excluded-row134 opinion exposure is disclosed. No record139 peer/root opinion, native scientific result or archived reviewer body was read before this initial. The actual target manuscript necessarily contains author assertions about audits and finite check counts; these were read as manuscript content and are not proof or independent results here. No scientific programme has yet been executed in this row139 lane; the only executed new helper authenticated whole bytes and made ordinary Poppler derivatives.

The core/source/prior-final namespaces are read-only; generated caches are opaque custody assets, not scientific evidence. No website, Git, Sheet, deployment, redirect, dependency installation, child agent or external-human communication/prepared outreach occurs. The root139 comparison gate remains CLOSED, so only neutral custody/initial/results/final locators may be sent.

## Family14 — intended independent controls and strongest current result

The strongest paper-first result at this freeze is a full uniform derivation of the original theorem from the stated external exponential matching premise, including the non-Slater tight-slack bridge, exact shift loss, both uniform reductions, every-city padding and explicit exponential upper construction. The external premise and claimed historical/source interfaces remain unverified by actual primary-body reading at this phase. No final disposition is fixed.

Own bounded controls can use exact rational matrices to test common-support compression, trace coercivity and noncommutative trace identities; a nonclosed arbitrary PSD image and a support-kernel mass family challenge the false compactness shortcuts. Signed affine coefficient witnesses with negative total sum test the t=|s|+1 normalization. Exact symbolic/counting and exponent-threshold inequalities can check quantifier directions without enumerating native matching/tour cases. These controls must be fully authored/read and their actual first results frozen before foreign/supplied body exposure. Their finite evidence does not establish an asymptotic rank lower bound or a theorem for all PSD matrices.

Follow-up defaults null. An improved constant-factor city gadget, a restatement of a cone-factorization bridge, or a finite checker is not automatically a substantial potentially publishable new contribution. Full proof/interface inspection, exact residual gaps and attribution determine the final decision. Agreement with the opposite lane will never be a proof.
