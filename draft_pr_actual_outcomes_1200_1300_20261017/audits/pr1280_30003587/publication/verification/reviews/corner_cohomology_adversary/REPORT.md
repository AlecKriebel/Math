# Corner/cohomology adversarial audit of PR1280 / problem 30003587

Initial seal: see `VERDICT.json` for the actual UTC timestamp. This is a candidate-informed structural audit, not a blind rediscovery or formal verification. No other family’s or root’s mathematical report was read before this seal.

## Result and exact claim

**No counterexample or blocking gap was found.** An independent transfer mechanism proves a stronger corner statement than the submitted proof uses. Together with the authenticated Barlak–Szabó outer aperiodic theorem and the graph-diagonal MASA fact, it gives a complete alternative route to the full target. The underlying published theorem remains a substantive external input. No novelty claim is made for the reductions below.

The target is: if M is a finite 0–1 matrix without zero rows or columns and O_M is simple and purely infinite, then every finite abelian diagonal quasi-free action α is strongly approximately inner. Precisely, for each g there must be unitaries u_(g,n) in **A^α**, fixed by every h in G, whose conjugations converge in norm on each a to α_g(a). There is no required relation among the different g-sequences. All proof statements below use this exact property.

The graph statement established here is broader: a finite strongly connected directed graph E that is not a directed cycle, including parallel edges, admits this conclusion for every finite abelian edge-diagonal action. Parallel-edge-mixing quasi-free actions can also be reduced by simultaneous finite-dimensional diagonalization. The essential 0–1 CK problem follows by the explicit generator correspondence in §7; no primitive-matrix hypothesis is inferred from simplicity.

## 1. Original question and imported input authenticated

The original [EMS report](https://ems.press/content/serial-article-files/46706), printed p.2621 / PDF page 21, was freshly downloaded, text-inspected, rendered, and visually inspected. Its setup excludes zero rows and columns; its quasi-free condition preserves the generator span and fixes the individual range projections. Question 1 asks the full finite abelian, simple, purely infinite question and specifies implementers in the whole fixed algebra. The nearby Theorem 2 has the additional outer and aperiodic assumptions. These are distinct scopes.

The exact imported result is [Barlak–Szabó, arXiv:1708.08258v3](https://arxiv.org/pdf/1708.08258v3), Corollary 2.8, pp.14–15: finite graph, at least two edges, strongly connected and aperiodic; finite abelian group; diagonal quasi-free action; pointwise outerness. Its conclusion is the property of Definition 2.5, p.10, with whole-action-fixed implementers separately for each g. Corollary 2.7, p.13, is the 0–1 primitive-matrix form. The graph definition allows edge-span preservation and fixes vertices. The v3 PDF was freshly acquired and the relevant text inspected; its p.14 was also rendered and visually inspected.

The only other specialized external fact needed by this alternate route is the graph diagonal MASA statement in [Conti–Hong–Szymański, arXiv:1101.4210v3](https://arxiv.org/pdf/1101.4210v3), §2.1, p.5: with no sinks and exits for every loop, the canonical path diagonal is maximal abelian. This text was freshly inspected in its source/range convention. The proof also uses the standard graph Cuntz–Krieger uniqueness theorem for Condition (L) and nonzero vertex images, and the saturated hereditary set construction of graph ideals. The finite return-graph construction below makes uniqueness’s hypotheses explicit. Fixed-point simplicity and Kishimoto’s theorem are **not needed by this alternate route**.

Byte sizes, hashes, retrieval status and inspection distinctions are in `SOURCE_PROVENANCE.json`. Third-party source bodies, extracts, and images are confined to `_local/`.

## 2. Strong approximate innerness transfers across an ambient-full corner

**Theorem A.** Let α be an action of a finite abelian group G on a unital C*-algebra A. Suppose p∈A^α is full in A. If α restricted to pAp is strongly approximately inner, then α is strongly approximately inner on A. Fullness in A^α is unnecessary. Conversely, restriction to any invariant corner preserves strong approximate innerness.

**Proof of the forward direction.** First choose a finite frame y_j∈Ap with Σ_j y_j y_j*=1. Here is an elementary justification of this standard fullness consequence. Approximate 1 sufficiently well by a finite sum a_j p b_j so that T=Σ a_j p b_j is invertible. Write T=YZ*, with rows Y=(a_jp), Z=(b_j*p). Since TT*≤||Z*Z||YY* and TT* is positive invertible, YY* is positive invertible. Then y_j=(YY*)^(-1/2)a_jp have the required property.

For each character χ of G, put

    y_(j,χ) = |G|^(-1) Σ_h conjugate(χ(h)) α_h(y_j).

These belong to Ap because p is invariant. Character orthogonality gives

    Σ_(j,χ) y_(j,χ) y_(j,χ)*
      = |G|^(-1) Σ_h α_h(Σ_j y_j y_j*) = 1.

Thus there is a finite **homogeneous** frame x_i∈Ap with α_h(x_i)=χ_i(h)x_i and Σ_i x_i x_i*=1. Fix g and choose u_n∈U((pAp)^α) implementing α_g on the corner. Define

    V_n = Σ_i α_g(x_i) u_n x_i*
        = Σ_i χ_i(g) x_i u_n x_i*.

Every summand is fixed by each α_h, since its two frame factors have inverse h-phases and u_n is fixed. Therefore V_n∈A^α **exactly**. For b∈pAp, Ad(u_n)(b)→α_g(b), and consequently u_n*α_g(b)u_n→b. The finite Gram-entry calculations are

    V_n V_n*
      = Σ_(i,j) α_g(x_i) Ad(u_n)(x_i*x_j) α_g(x_j*) → 1,

    V_n* V_n
      = Σ_(i,j) x_i u_n* α_g(x_i*x_j) u_n x_j* → 1,

    V_n a V_n*
      = Σ_(i,j) α_g(x_i) Ad(u_n)(x_i*a x_j) α_g(x_j*)
        → α_g(a).

Both unitary-defect limits imply eventual invertibility. The polar unitaries

    W_n = V_n (V_n*V_n)^(-1/2)

lie exactly in A^α, tend in norm to V_n, and implement α_g. This proves the conclusion without fixed-algebra simplicity.

Equivalently one can use the orbit frame x_(h,j)=|G|^(-1/2)α_h(y_j). The action permutes this frame, and α_k(V_n)=V_n follows by reindexing and α_kα_g=α_gα_k. This avoids Fourier decomposition and identifies exactly where abelianness enters.

**Reverse direction.** If v_n∈U(A^α) implements α_g, then ||[v_n,p]||→0 because α_g(p)=p. Hence z_n=pv_np has z_n*z_n→p and z_nz_n*→p. Its polar unitaries inside the unital corner pAp are whole-action-fixed and implement the restricted α_g. No fullness is needed for this direction. ∎

**Exact inner version, used below.** If σ(p)=p, p is full in A, and σ|_(pAp)=Ad(u), the same frame argument without any averaging gives the exact unitary

    U = Σ_i σ(y_i) u y_i*,

with UU*=U*U=1 and UaU*=σ(a). Thus an outer automorphism cannot become inner on an invariant full corner. The identity follows by replacing all three limits above by equalities. This exact statement does not require G or abelianness.

## 3. Honest finite abelian cocycle perturbations preserve the property

**Theorem B.** Let β:G↷A be strongly approximately inner, G finite abelian. Let d_g be a genuine β-cocycle:

    d_(gh)=d_g β_g(d_h),   d_1=1.

Then α_g=Ad(d_g)β_g is strongly approximately inner.

**Proof.** Fix g and choose v_n∈U(A^β) implementing β_g. Set t_n=d_gv_n. These unitaries implement α_g asymptotically. For every h, the cocycle identity and gh=hg give

    α_h(t_n)=d_h β_h(d_g)v_n d_h*
            =d_g β_g(d_h)v_n d_h*.

Since v_nd_hv_n*→β_g(d_h), this implies ||α_h(t_n)−t_n||→0. The finite average z_n=|G|^(-1)Σ_h α_h(t_n) lies in A^α and ||z_n−t_n||→0. Its polar unitary is eventually defined, lies in A^α, and implements α_g. ∎

This proves, within the exact finite abelian setting, the invariance needed to replace the submitted pinch argument. It is not an unsupported appeal to exterior equivalence. A projective family with a nontrivial scalar multiplier is **not** a genuine cocycle for the trivial action; §5 explains why this distinction matters. The submitted pinch/polar construction is valid, but its description as “necessary” is stronger than needed: finite averaging/polar is an alternative.

## 4. Diagonal inner kernels have no projective obstruction

Use graph conventions S_e*S_e=p_(r(e)) and S_eS_e*≤p_(s(e)). Write σ_z(S_e)=z_eS_e and z_μ for the product along a path. For a strongly connected finite non-cycle graph every cycle has an exit, so its canonical diagonal D=C(E^∞) is a MASA.

**Cycle criterion.** σ_z is inner if and only if z_μ=1 for every closed directed path μ. In that case it has normalized vertex implementer D_z=Σ_v t_vp_v, unique after t_b=1.

For the nontrivial direction, if σ_z=Ad(u), it fixes D pointwise, so u∈D by maximal abelianness. For a path μ, the cylinder-function identity S_μ*uS_μ(x)=u(μx), initially verified on cylinder projections, gives u(μx)=z_μu(x). When μ is closed take x=μμμ…; since u(x) is nonzero, z_μ=1. Choose directed paths θ_v:b→v, θ_b empty, and put t_v=z_(θ_v)^(-1). For e:v→w, choose a return path η:w→b. The two closed paths θ_veη and θ_wη show z_(θ_v)z_e=z_(θ_w), hence z_e=t_v conjugate(t_w). This is exactly conjugation by Σ t_vp_v. The converse is immediate by cancellation around closed paths. Connectivity proves uniqueness.

For the action α_g(S_e)=χ_e(g)S_e, define on **all of G**, not just its inner subgroup,

    d_g = Σ_v χ_(θ_v)(g)^(-1) p_v.

Each vertex coefficient is a character. Consequently d_gd_h=d_(gh), and α fixes every d_h. Let K={g:α_g is inner}. The cycle criterion gives α_k=Ad(d_k) for every k∈K. Thus

    β_g = Ad(d_g*)α_g

is an edge-diagonal action, trivial on K. It descends to G/K, and its quotient action is outer: inner β_g would make α_g inner, forcing g∈K. The construction has an actual representation, so there is neither a projective multiplier nor a character-extension assumption. Also d_g is a genuine β-cocycle, since β fixes the vertex algebra. Theorem B can therefore restore α from β once β is strongly approximately inner.

This simultaneously handles a nonfaithful action. Its ordinary action kernel ker(α) can be strictly smaller than K. The quotient used here is the **inner** kernel, and the construction remains valid when K=G or when G/K is trivial.

## 5. Attempted obstructions and explicit boundary cases

**Pauli obstruction outside the diagonal class.** Let X=[[0,1],[1,0]] and Z=diag(1,−1). Their conjugations give an action of G=Z₂×Z₂ on M₂, since XZ=−ZX. The fixed algebra is C1, so all fixed unitaries implement the identity, whereas Ad(X) is nontrivial. The action is not strongly approximately inner. The same obstruction persists on M₂⊗O₂ with trivial action on the second factor: fixed unitaries lie in 1⊗O₂ and fix M₂⊗1 pointwise. This is a simple purely infinite example, so pure infiniteness and abelianness alone do not eliminate the obstruction.

More generally, if an inner action on a simple unital A has projective implementers U_g, every whole-action-fixed approximating unitary commutes with U_h. Hence strong approximate innerness forces α_g(U_h)=U_h. The scalar commutator U_gU_hU_g*U_h* must be 1. Conversely, if all implementers commute, they themselves are whole-action-fixed and implement exactly. Thus the Pauli alternating multiplier is a genuine obstruction. It cannot occur for an edge-diagonal graph action here: its inner implementers lie in D, α fixes D pointwise, and the preceding normalized vertex construction splits the kernel explicitly.

**Period two, fixed-algebra fullness fails.** Take the bidirected complete bipartite graph with V₀={0,1}, V₁={2,3}; every cross-part directed edge appears once. Its 0–1 adjacency matrix is [[0,J],[J,0]], J the 2×2 all-ones matrix. It is irreducible of period 2 and has exits. Let p=p₀+p₁ and let α be the order-two gauge action S_e↦−S_e. Then α=Ad(2p−1), so α is strongly inner. But

    A^α = pAp ⊕ (1−p)A(1−p),

and p is not full there. It is full in the simple ambient A. A homogeneous frame for Ap is p together with the edges from V₁ into V₀. Taking the corner implementer u=p in Theorem A yields exactly

    V = p − Σ_(s(e)∈V₁) S_eS_e* = 2p−1.

This directly falsifies the proposed *necessity* of fixed-algebra fullness, while supporting the target conclusion. It is not a counterexample to the submitted sufficient hypothesis.

For the order-four gauge subgroup, S_e↦iS_e, the inner subgroup is {0,2}⊂Z₄: a closed path of length 2 forces ζ²=1, and those phases are vertex coboundaries. The return graph has adjacency [[2,2],[2,2]], so the restricted action factors through the outer order-two gauge action on that primitive graph. Theorem A lifts its fixed implementers and recovers the full order-four action directly.

**Noncyclic mixed kernel.** On the same exact 0–1 graph take G=Z₂×Z₂ and source labels χ_v(a,b)=(−1)^a on V₀ and (−1)^b on V₁. The action is faithful, while its inner kernel is K={(0,0),(1,1)}. The nonidentity kernel element is the period-two gauge action; the quotient action after the normalized vertex twist is outer of order two. This tests that faithfulness and outerness are different and that a noncyclic original group causes no hidden projective problem. A nonfaithful case is obtained from any action by precomposing with a noninjective finite abelian quotient; fixed algebras and the per-element implementers are preserved under that pullback.

**Excluded directed cycle.** For a directed d-cycle, A≅M_d(C(T)). Gauge phase ζ acts on the central cycle coordinate by ζ^d. If ζ^d≠1 it cannot even be approximately inner, because inner automorphisms fix the center. Thus removing the non-cycle / simple purely infinite assumptions really can fail; this is not a limiting case silently handled by the imported theorem.

## 6. Alternative full graph proof using the direct transfer mechanisms

First suppose the finite abelian edge-diagonal action is outer. Let d be the graph period, let V₀ be one cyclic class, and put p=Σ_(v∈V₀)p_v. This is invariant and full in the ambient graph algebra: if an ideal contains p, it contains every p_v, since a path μ from V₀ to v gives S_μ*pS_μ=p_v. Strong connectivity supplies such paths and Σ_v p_v=1. The return graph F has vertices V₀ and an individual edge for each E-path of length d beginning in V₀. Distinct paths stay distinct, so multiple edges are allowed.

The standard finite irreducible-matrix period decomposition says F is primitive. One elementary justification is that based closed walks have lengths with gcd d. A finite subset already has gcd d; after division by d its nonnegative semigroup contains all sufficiently large integers (choose representatives for each residue modulo one generator). Inserting these based loops between fixed connecting paths produces all sufficiently large lengths divisible by d between any two vertices of V₀. F is therefore strongly connected and aperiodic. A branching vertex in E produces at least two length-d paths from some vertex in V₀: walk backwards fewer than d steps to V₀, choose either branch, and extend to length d. Thus F is not a single directed cycle, has at least two edges, and satisfies Condition (L).

The families p_v, v∈V₀, and S_μ, |μ|=d, form a graph CK family for F, with nonzero vertex images; graph uniqueness gives injectivity. For surjectivity, pAp is spanned by S_μS_ν* starting in V₀ with common terminal vertex. Their lengths are congruent mod d. Append all paths τ of the one common length k∈{0,…,d−1} that makes both lengths divisible by d:

    S_μS_ν* = Σ_(|τ|=k, s(τ)=r(μ)) S_(μτ)S_(ντ)*.

Each right-hand path decomposes into return edges. The empty-path case uses vertex projections and causes no exception. This proves the equivariant isomorphism C*(F)≅pAp; return edges have character χ_μ.

By the exact inner extension after Theorem A, the restricted action remains outer. All hypotheses of authenticated Corollary 2.8 now hold. It gives strong approximate innerness in pAp, and **Theorem A** lifts it using fullness in A alone. This proves the outer graph statement without a fixed-point simplicity input.

For a general action, perform the normalized vertex twist of §4. The quotient β of G/K is outer unless the quotient is trivial. The outer graph statement proves β strongly approximately inner; when the quotient is trivial its implementer is simply 1. The **honest cocycle perturbation Theorem B** then proves α strongly approximately inner. This closes the nonouter case without a new cohomology-vanishing assumption. No central difficulty has been transferred to an unsupported lemma.

For the broader edge-span-preserving graph definition, fixed vertices force edge mixing to stay within the finite-dimensional spaces of parallel edges from v to w. On each such space the action is a unitary representation, because S_e*S_f=δ_(e,f)p_w. A finite abelian family of unitary matrices simultaneously diagonalizes. The resulting blockwise unitary change of edge generators preserves the graph CK relations and defines an automorphism with inverse the inverse block matrices. Conjugacy reduces to the proved edge-diagonal statement, and carries whole-action-fixed implementers back. This broadening is not needed for the original CK definition, whose individual generators are already eigenvectors.

## 7. Exact matrix claim, independently checked translation

For the original definition, α_g(s_i)=Σ_j c_(ji)(g)s_j and α_g(p_i)=p_i, with p_i=s_is_i*. Since p_jα_g(s_i)=0 for j≠i, while p_js_j=s_j≠0, all off-diagonal coefficients vanish. Thus α_g(s_i)=χ_i(g)s_i with χ_i a character.

Let E have edge i→j exactly when M(i,j)=1. Inside O_M set T_(ij)=s_ip_j. Then

    T_(ij)*T_(ij)=p_j,
    Σ_(j:M(i,j)=1) T_(ij)T_(ij)*=p_i,

and the edge orthogonality relations follow from the orthogonality of the p_j and of the s_i ranges. Conversely s_i=Σ_j T_(ij) satisfies s_i*s_i=Σ_j M(i,j)p_j and s_is_i*=p_i; the cross terms vanish using the orthogonal terminal projections. These formulas are inverse, so O_M≅C*(E) equivariantly, and α_g(T_(ij))=χ_i(g)T_(ij).

No zero rows or columns mean no graph sinks or sources. For a finite graph with those properties, simplicity forces strong connectivity. Otherwise choose a terminal strongly connected component T in the condensation graph and a distinct source component S. Since the original graph has no sources, S contains a directed cycle. The saturated hereditary closure of T cannot absorb that cycle: each cycle vertex retains an edge inside the omitted cycle. It is therefore a nonempty proper saturated hereditary set, giving a nonzero proper graph ideal, a contradiction. A directed cycle algebra is M_d(C(T)), so it is excluded by the assumed simplicity and pure infiniteness. The graph theorem therefore gives precisely the original matrix conclusion.

## 8. Checkable computations and limits of evidence

`CHECKS.py` is standalone authored code, with no third-party source code or dependencies. It checks the orbit-frame formula on a nonhomogeneous 16-element frame in M₄ for Z₂×Z₂ using exact Gaussian dyadic arithmetic, including all 64 matrix-unit implementation comparisons. Its rank-one corner is ambient-full and is not full in the diagonal fixed algebra.

On the exact bidirected K₂,₂ period-two graph it exhausts all 4⁸=65,536 edge-character assignments into the dual of Z₂×Z₂ and the 4⁴=256 source-only assignments arising from the exact CK subclass. It verifies the closed-simple-cycle / normalized vertex-coboundary equivalence, that the normalized coefficients form representations, that the twisted edge characters vanish on the computed cycle kernel, and that the twisted action has exactly that ordinary kernel. Closed directed walks decompose into simple cycles, so checking those cycles is the correct finite combinatorial criterion. The edge-label kernel-order histogram is {4:64, 2:5952, 1:59520}; the source-only histogram is {4:4, 2:84, 1:168}. These are combinatorial confirmations of the proved criterion, not numerical tests of innerness in an infinite C*-algebra.

The code also verifies the Pauli sign obstruction and one-dimensional fixed subspace. `CHECK_RESULTS.json` records the actual run and scope. The infinite-dimensional statements are supported by the written proofs and explicitly identified published inputs, not by these finite tests alone.

## Exposure, status and remaining gap

Permitted candidate exposure: `submitted/PROOF.md` and `submitted/SOURCE_METADATA.json`. I also opened `submitted/SOURCE_VERIFICATION.md` as source-verification material; it contains authored corner/period supplements, so this is disclosed as a limitation of early independence. No other review or root mathematical report was read. The direct homogeneous/orbit-frame theorem, finite averaging proof of cocycle invariance, and obstruction tests were developed in this family after that exposure.

This family’s audit is complete at initial seal, best-guess **100% toward the assigned structural audit**, with **no blocking mathematical gap found for the full target**, conditional on the named standard graph results and the authenticated Barlak–Szabó theorem. It is not a claim of formal proof-assistant certification, a new human peer review, or verified novelty. No git, candidate, index, publication, or remote mutation was performed. No individual was contacted.
