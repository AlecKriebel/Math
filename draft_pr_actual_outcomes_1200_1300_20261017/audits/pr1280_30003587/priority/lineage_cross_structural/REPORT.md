# PR1280 / 30003587: detached reverse lineage challenge

Report completed in the post-seal phase on 2026-10-18 UTC. The actual completion/seal timestamps and file hashes are recorded in VERDICT.json and OUTPUT_MANIFEST.json. The initial direct_lineage seal is preserved verbatim.

## Finding

**The full original target is a consequence of an inspected 2022 general theorem plus elementary, graph-specific kernel normalization and finite averaging.** The deduction is written out below and was assembled in this audit in October 2026. This does not establish that an older source explicitly printed the full target, recognized this consequence, or resolved the named question at that time. Priority remains uncleared for any claim of first solution, first explicit statement, or new mechanism.

The reverse challenge also confirms the positive structural precedents: the exact periodic return corner is a special case of Crisp–Gow 2004, and Matsumoto 2000 gives the diagonal-coboundary/periodic-orbit mechanism from which the all-period vertex-inner characterization follows. Katayama–Takehana 1997 is a relevant earlier coefficient-inner characterization, with a genuine aperiodicity restriction.

Two proposed general lemmas survive direct proof checking: strong approximate innerness for finite abelian actions is preserved by genuine cocycle perturbations, and it passes from an invariant corner full in the ambient algebra to that algebra. Fullness of the projection in the fixed algebra is unnecessary. Exact fixed algebras can change under cocycle perturbation. These conclusions correct overly broad necessity language in the sealed structural report; no historical sealed file has been edited.

## Exact target and exposure

For an essential finite 0–1 matrix A, with O_A simple and purely infinite, and a finite abelian group acting by the diagonal quasi-free automorphisms in OWR Question 1, the target is: for each g there are unitaries w_(g,n) in the fixed algebra of the entire original action such that Ad(w_(g,n)) converges pointwise in norm to alpha_g. No approximate representation relations between different g are required. Neither matrix primitivity nor pointwise outerness is admitted as an extra hypothesis.

The official [OWR body](https://ems.press/content/serial-article-files/46706), printed p.2621/PDF p.21, was read and visually checked in the initial phase. Its original bibliographic year is 2017; the official publisher page displays publication on 5 July 2018. The result displayed next to Question 1 retains both outerness and aperiodicity. The full question was the original admission target; finding a prior consequence does not retrospectively narrow that admission.

My initial direct-lineage output was sealed at 2026-10-18T02:51:19.726474Z, before reading any other family's report. At approximately 02:52:10Z, in this expressly authorized reverse-challenge phase, I first read the structural report and the assigned corner/cohomology proof sections, then the corresponding alternate-reconstruction material. INPUT_AUTHENTICATION.json verifies the specified manifest hashes and every member, including the initial direct-lineage output. Other-family verdicts and the parent's preliminary PASS were not used as proof. The candidate's original submitted proof and source files were permitted initial inputs; no current-edition or root synthesis report was read or edited here.

## Primary passages and structural mappings

### Matsumoto 2000: periodic graphs really are covered by the mechanism

Kengo Matsumoto, *On automorphisms of C*-algebras associated with subshifts*, J. Operator Theory 44 (2000), 91–112, [official publisher PDF](https://jot.theta.ro/jot/archive/2000-044-001/2000-044-001-005.pdf). Fresh body: 303396 bytes, SHA256 64bfe3cc88b00ac3cb64a7df4ce0fbf728ff548e6be9a8515a9c482da65274ff.

Actually read: the subshift condition (I) definition at printed p.94/PDF p.4; §3 setup and maximal-abelian argument at pp.97–98/PDF pp.7–8 as relevant; Lemma 5.14 and Proposition 5.15 at p.109/PDF p.19; the immediately preceding setup and Proposition 6.4 at pp.110–111/PDF pp.20–21. Pages 109 and 111 were visually checked in this phase. The condition (I) setup, lemma proof, and periodic-point formula are decisive.

The lemma identifies an inner diagonal automorphism lambda(U) with a diagonal coboundary U=v phi(v*); its proof puts the implementer in the diagonal using maximal abelianness. Proposition 6.4 obstructs innerness if the product of U around a periodic orbit is nontrivial. The stronger condition (D) in neighboring Theorem 5.16 belongs to a different exact-sequence statement and is not needed for these two passages.

Here is the precise graph implication. Let E be finite strongly connected and not a directed cycle, with graph generators S_e,p_v. Its edge 0–1 matrix is L(e,f)=1 exactly when r(e)=s(f). The S_e satisfy the CK relations for L because S_e*S_e=p_r(e)=sum_(s(f)=r(e)) S_f S_f*. Conversely the graph vertices are sums of edge-range projections. Thus this is the same algebra and the path diagonal is the same diagonal. Every cycle has an exit, so this finite-type shift satisfies condition (I), irrespective of its period.

For edge phases z_e, put U=sum_e z_e S_e S_e*. Then lambda(U)(S_e)=z_e S_e. If this automorphism is inner, Proposition 6.4 forces z_mu=1 on every closed path mu: repeat mu infinitely and use its periodic orbit. If the least period is shorter than |mu|, the conclusion for the least orbit implies the same conclusion for its repetition.

Choose a base vertex b and directed paths theta_v from b to v, with theta_b empty. For an edge e:v->w, choose a return path eta from w to b. The two closed paths theta_v e eta and theta_w eta yield
z_(theta_v) z_e z_eta = 1 = z_(theta_w) z_eta.
Consequently z_e=z_(theta_w)/z_(theta_v). With d_v=z_(theta_v)^(-1),
z_e=d_v conjugate(d_w), and D=sum_v d_v p_v implements the automorphism exactly. The converse follows by applying Ad(D) to generators.

This last finite-graph path comparison is a deduction here, not a printed statement attributed verbatim to Matsumoto. It establishes that the inner-characterization mechanism covers periodic graphs. Matsumoto does not thereby explicitly state the finite-group strong-approximate-innerness theorem.

### Crisp–Gow 2004: exact corner, map, and all hypotheses

Tyrone Crisp and Daniel Gow, *Contractible subgraphs and Morita equivalence of graph C*-algebras*, [arXiv:math/0404542v1](https://arxiv.org/pdf/math/0404542v1), 29 April 2004. Fresh body: 195004 bytes, SHA256 2aea95a14808c0f4cb646b6db2a85eafbaaba91819736cf0865ab2e50cd74c7c. Actually read: graph conventions and Theorem 3.1 at preprint pp.2–3, and its proof at pp.5–8; theorem pages 2 and 3 visually checked.

Let d>1 be the period and V_0,...,V_(d-1) its cyclic classes. Retain G^0=V_0 and remove T^0=E^0 minus V_0.

- E is finite, hence has no acyclic infinite tail; it has no sinks or infinite emitters, so all singular vertices lie in the retained set vacuously.
- Every edge advances the cyclic class. A path lying wholly in T has at most d-2 edges. Hence T is acyclic and has no infinite paths.
- Theorem 3.1(a) concerns infinite paths from a retained vertex staying forever in T after leaving it. There are none.
- Conditions (b), (c), and (d) quantify over infinite paths in T. All are vacuous here.
- A positive first-return path from V_0 to V_0 with intermediate vertices in T has exactly d edges: an earlier return is impossible by cyclic classes, and a longer first return is impossible because time d already returns.

Thus the theorem's new graph is exactly the length-d return graph F. Its proof specifies the map p_v^(F)->p_v and S_(new mu)->S_mu and identifies its image with p C*(E) p for p=sum_(v in V_0)p_v; the projection is full. This is an exact corner, not merely an unspecified stable isomorphism. An edge-phase action transports to F with phase chi_mu=product_(e in mu)chi_e; generator formulas prove equivariance directly. This equivariance check is an audit deduction rather than a separate assertion in the source.

Strong connectivity of F follows by cutting paths between V_0 vertices into d-blocks. The gcd of F-closed-path lengths is the original gcd d divided by d, hence one; finite irreducibility then makes F primitive. This last period argument is separate from Crisp–Gow. For d=1 use the identity corner.

The later publication is Proc. Amer. Math. Soc. 134 (2006), DOI [10.1090/S0002-9939-06-08216-5](https://doi.org/10.1090/S0002-9939-06-08216-5). Fresh publisher PDF acquisition returned 403. Only the inspected v1 theorem numbering and proof are asserted.

### Katayama–Takehana 1997: useful predecessor with narrower hypotheses

The actual [RIMS report](https://www.kurims.kyoto-u.ac.jp/~kyodo/kokyuroku/contents/pdf/1003-6.pdf), Kokyuroku 1003 (1997), 81–93, was acquired in the initial phase: 993227 bytes, SHA256 78f5420942ad9a48b22ea7405fa77567cc70e6aebb667a610582343bc511fb42. Proposition 1.2 at pp.81–82/PDF pp.1–2 and Proposition 2.6 at p.89/PDF p.9, including relevant proof material p.90/PDF p.10, were checked. Proposition 2.6 was visually inspected initially and re-read as text here.

Proposition 2.6 assumes a full finite-type Hilbert bimodule over a finite-dimensional abelian coefficient algebra B, complex dimension greater than one, and B being X-aperiodic. It characterizes innerness by trivial coefficient automorphism and coefficient-inner form Ux=uxu*. Proposition 1.2 identifies X-aperiodicity with primitivity of the associated finite matrix. Thus it supports the vertex-coefficient mechanism under aperiodicity; it does not itself remove arbitrary graph period. The later 1998 same-title journal body, DOI 10.1142/S0129167X9800021X, was not acquired; journal numbering is not inferred.

## The full target as an audit-composed 2022-theorem consequence

The primary general theorem is Gabe–Szabó, [arXiv:2205.04933v1](https://arxiv.org/pdf/2205.04933v1), dated 10 May 2022 in the actual body. Theorem 5.8 appears at preprint pp.45–46; Definition 1.15 at p.13 and Proposition 3.14 at p.29 were re-read here. The initial source ledger pins 707699 bytes and SHA256 d3dcff5b942e016f46ff4101e01ce39fdcc09c29e7f9fde21677b0019d909120. Version 3 (16 August 2023) also has Theorem 5.8, now p.46, and the relevant outer-action criterion is Proposition 3.15 p.29. Do not cite the two versions' proposition numbers interchangeably.

Theorem 5.8 applies to an exact group, separable unital exact domain, unital Kirchberg codomain, and amenable isometrically shift-absorbing codomain action. For two unital cocycle embeddings it identifies equality of equivariant KK classes with asymptotic unitary equivalence in the sense of Definition 1.15. Proposition 3.14 makes isometric shift absorption equivalent to pointwise outerness for countable discrete groups acting on Kirchberg algebras. The theorem has the equivariance control needed below; ordinary nonequivariant Kirchberg–Phillips uniqueness would not suffice.

### 1. Reduce the original presentation to edge phases without losing the action

In the original OWR definition the span of canonical T_i is invariant and the range projections p_i=T_iT_i* are fixed. Multiplying alpha_g(T_i) by p_j forces all coefficients except the i-th to vanish. Thus alpha_g(T_i)=chi_i(g)T_i, with chi_i a character. In the vertex graph of A put S_(i,j)=T_i p_j when A_ij=1; the CK relations give the graph relations, and T_i=sum_j S_(i,j). Its edge phases are chi_i.

Essentiality gives no graph sources or sinks. Simplicity forces strong connectivity in this finite setting: if there were several strongly connected components, a terminal component would generate a nonempty proper saturated hereditary set. Properness follows because some other source component contains a cycle (there are no sources), and its vertices cannot be swallowed by saturation. The corresponding graph ideal contradicts simplicity. Pure infiniteness excludes the directed-cycle case. Consequently the graph framework above covers the full original target. More general abelian domain-diagonal quasi-free conventions can first use Barlak–Szabó's simultaneous diagonalization (final Proposition 1.8, pp.215–216); the original OWR definition already supplies eigenvectors.

### 2. Normalize the entire inner kernel by an explicit representation

Let K={k in G: alpha_k is inner}. It is a subgroup, as the inverse image of the identity in Out(A). Fix the same base paths theta_v for every group element and define, on all of G,
D_g = sum_v chi_(theta_v)(g)^(-1) p_v.

Because each path phase is a character, D_g D_h=D_(gh). Every D_g is fixed by alpha. By the Matsumoto/path-comparison deduction, alpha_k=Ad(D_k) for k in K. Define
beta_g = Ad(D_g*) alpha_g.

The representation identity and alpha-fixedness of the D's prove that beta is an action. It fixes every p_v and every D_h, and beta_k=id for k in K. Hence it factors through H=G/K. Its H-action is pointwise outer: if beta_g were inner, alpha_g would also be inner, forcing g in K. This handles nonfaithfulness too. If K=G, the original action is already implemented exactly by the original-action-fixed D_g; that case needs no uniqueness theorem.

This is a graph-specific split of the inner kernel. No arbitrary projective family of inner implementers is being substituted for a genuine representation.

### 3. Apply old equivariant uniqueness to the outer quotient, without a period assumption

Assume H is nontrivial. A finite graph Kirchberg algebra is separable, unital, nuclear, and therefore exact. The finite group H is exact and amenable; its action is amenable. Its pointwise outer action beta is isometrically shift-absorbing by the cited proposition. Thus every hypothesis of Theorem 5.8 holds with domain=codomain=A and action=beta.

For fixed h in H, the automorphism beta_h commutes with the whole action, so (id,1) and (beta_h,1) are unital equivariant cocycle embeddings. They have the same KK^H class. Indeed, if beta_h(S_e)=lambda_e S_e, choose real a_e with exp(i a_e)=lambda_e. The maps
delta_t(p_v)=p_v, delta_t(S_e)=exp(i t a_e)S_e, 0<=t<=1,
are automorphisms by the graph relations, commute with every beta_l, and interpolate id to beta_h. A homotopy of equivariant maps gives equality in KK^H. These maps need not themselves be an H-action.

Theorem 5.8 and Definition 1.15 therefore give unitaries u_t in A with Ad(u_t)->beta_h and max_(l in H)||beta_l(u_t)-u_t||->0. Average:
b_t=|H|^(-1) sum_l beta_l(u_t).
Then b_t is exactly beta-fixed and ||b_t-u_t||->0. Eventually b_t is invertible, so its polar unitary
v_t=b_t (b_t*b_t)^(-1/2)
lies exactly in A^beta, stays norm-close to u_t, and implements beta_h asymptotically. Choosing a sequence of times yields strong approximate innerness of beta, inflated to G. No graph period, return corner, or approximate representation property was used.

### 4. Restore the original action and its exact fixed algebra

The D_g are an honest beta-cocycle, since beta_g(D_h)=D_h and D_g D_h=D_(gh); alpha_g=Ad(D_g)beta_g.

More generally, let beta be SAI for finite abelian G and d an honest beta-cocycle. Put alpha_g=Ad(d_g)beta_g. For fixed g choose v_n in U(A^beta) implementing beta_g, and put t_n=d_g v_n. Then Ad(t_n)->alpha_g. The cocycle identity and commutativity of G give
alpha_h(t_n)=d_h beta_h(d_g) v_n d_h*
            =d_g beta_g(d_h) v_n d_h*,
hence
||alpha_h(t_n)-t_n||=||beta_g(d_h)-v_n d_h v_n*|| -> 0.
Because G is finite this convergence is uniform in h. Averaging t_n over the original alpha and taking the eventual polar unitary produces w_n in U(A^alpha), with ||w_n-t_n||->0. Thus Ad(w_n)->alpha_g exactly as required.

The converse follows with the honest alpha-cocycle e_g=d_g*: e_g alpha_g(e_h)=d_(gh)*. So genuine cocycle perturbation preserves this property, although it need not preserve the exact fixed algebra.

Steps 1–4 establish the full original target. They are a checkable October 2026 assembly of inspected old theorems and elementary arguments. I found no primary passage that explicitly prints this full assembly or labels it as a resolution of OWR Question 1. That failure to locate a passage cannot establish firstness.

## Independent check of the ambient-full corner transfer

Let alpha act on unital A, let p be invariant and full in A, and assume its restriction to pAp is SAI. A full finite frame y_j in Ap can be chosen with sum_j y_j y_j*=1. For completeness, fullness gives finitely many a_i,b_i with sum_i a_i p b_i invertible; its row/column factorization implies sum_i a_i p a_i* is invertible, and normalization yields such a frame.

Fourier projections for the finite abelian action give homogeneous x_i in Ap with alpha_h(x_i)=chi_i(h)x_i and sum_i x_i x_i*=1. The frame identity follows by character orthogonality:
sum_(j,chi) P_chi(y_j)P_chi(y_j)* = |G|^(-1) sum_h alpha_h(sum_j y_j y_j*)=1.

Fix g and write sigma=alpha_g. Choose u_n in U((pAp)^alpha) implementing sigma on pAp. Define
V_n=sum_i sigma(x_i)u_n x_i*.
Every summand is exactly alpha-fixed: alpha_h commutes with sigma and its two character factors cancel. Expanding the finite sums gives
V_n V_n* = sum_(i,j) sigma(x_i) Ad(u_n)(x_i*x_j) sigma(x_j*) -> 1,
V_n* V_n = sum_(i,j) x_i u_n* sigma(x_i*x_j)u_n x_j* -> 1.
Here x_i*x_j belongs to pAp. The second convergence follows from the first implementation convergence by applying the inverse unitary on sigma(b). Likewise, for a in A,
V_n a V_n* = sum_(i,j) sigma(x_i) Ad(u_n)(x_i*a x_j) sigma(x_j*) -> sigma(a).
The frame identity collapses all three limiting sums. Both norm defects are needed: a single isometry defect would not imply invertibility. Eventually V_n is invertible, and its polar unitary is exactly alpha-fixed, norm-close to V_n, and implements sigma. This proves ambient SAI without fullness in A^alpha.

Conversely, compress ambient fixed implementing unitaries by p. As alpha_g(p)=p, their commutators with p tend to zero, so their compressions have both unitary defects tending to zero in pAp. Polar decomposition gives the restricted property; fullness is unnecessary for this direction.

The same frame formula with an exact corner implementer gives exact ambient innerness. Therefore pointwise outerness passes to an invariant ambient-full corner. Combining this with Crisp–Gow and Barlak–Szabó gives a second valid assembly: outer arbitrary-period graph actions reduce to the old outer primitive result, then the normalized kernel and honest-cocycle argument restore the full nonouter target. The 2022 uniqueness route bypasses that corner assembly.

## Adversarial boundaries and priority limits

The fixed-algebra change is real. For trivial beta on M_2 and the representation d_1=diag(1,-1) of Z_2, A^beta=M_2 whereas A^alpha is the diagonal algebra. Both actions are SAI. Fixed-algebra equality and invariance of the SAI property are different assertions.

Pointwise-inner projective families give no analogous unrestricted conclusion. For G=Z_2 x Z_2 on M_2 tensor O_2, use conjugations by Pauli X and Z in the first factor. The automorphisms commute but XZ=-ZX, and the entire fixed algebra is 1 tensor O_2. Its unitaries act trivially on M_2, so they cannot approximate either nontrivial Pauli automorphism. This is not a counterexample to honest-cocycle invariance: a cocycle for the trivial action would be an actual representation, which this projective family is not.

For the period-two bipartite graph with 2 vertices in each class and every edge between the two classes, the gauge sign is inner via 2p-1. The return projection p is full in the simple ambient graph algebra but not in the sign-fixed algebra pAp direct-sum (1-p)A(1-p). This disproves any general assertion that fixed-algebra fullness is necessary for transfer; the homogeneous-frame proof explains why transfer still works. Directed cycles remain excluded by the target and cannot be slipped into the Kirchberg uniqueness step.

Kodaka–Teruya 2015 does not supply a direct shortcut with exactly the target's hypotheses. The freshly acquired [publisher body](https://www.impan.pl/shop/publication/transaction/download/product/91245), Definition 6.2 and Theorem 6.3 at printed p.287/PDF p.29, and Corollary 6.4 pp.289–290/PDF pp.31–32, preserve approximate representability under the stated strong Morita equivalence. Their definition includes comultiplication/coherence conditions. Those add group-representation relations beyond independent fixed implementers; Barlak–Szabó SAI alone does not supply that upgrade. This limitation does not defeat the direct frame proof above.

Christensen–Neagu–Szabó [arXiv:2504.12730v2](https://arxiv.org/pdf/2504.12730v2), Definition 3.1 and Remark 3.2 at p.11, were re-read, along with Lemma 3.3 and proof pp.12–13. They explicitly match the finite abelian unital definition with Izumi's property and distinguish it from approximate representability; Lemma 3.3 gives an equivariantly sequentially split characterization. These passages are useful broader infrastructure, not a printed full CK target or a direct printed statement of the exact cocycle/frame lemmas in this report.

The final Barlak–Szabó publisher body is already authenticated in the initial seal: [official migrated endpoint](https://journals.msp.org/mscand/article/download/221/220), final Theorems 1 and 2 at p.212, graph proof pp.223–224; arXiv v3 calls these Corollaries 2.7 and 2.8. Both retain outer/aperiodic hypotheses. Izumi's original Kyoto preprint already supplies the broader finite Cuntz O_n abelian SAI case without outerness; its final 2004 PDF remains unavailable here. These facts must remain separate from the full CK result.

Gabe's [author publication list](https://jamiegabe.com/research/) actually read in this phase records the dynamical theorem as Acta Math. 232(1), 1–77 (2024), DOI 10.4310/ACTA.2024.v232.n1.a1. Both discovered official final-PDF endpoints returned 403 when opened. Thus final publication metadata is authenticated, but final theorem numbering/body identity is not asserted. The 2022 deduction rests on the actually read v1 body.

No located explicit old combined statement is a bounded search result. No firstness, new solution, new mechanism, or earliest consequence date is certified. A defensible framing is an attributed complete proof/exposition of the original full claim, with the alternate deduction from Gabe–Szabó explained and older structural mechanisms credited. The target's truth and its eligibility as a novel contribution are separate questions.

## Record and limitations

QUERY_LOG.json records 24 new literal queries focused on cocycle invariance, full corners, Matsumoto, and the uniqueness consequence, with URLs and authored inspection/access status only. This phase did not rerun the initial 67-query search. Raw source bodies, extracts and visual checks stay in _local and are excluded from the manifest; no provider excerpts or source PDFs are redistributed in the authored output.

The unresolved Zacharias 2000 chapter-body access gap from the initial audit remains a gap. Final bodies for Katayama–Takehana, Crisp–Gow and Gabe–Szabó were not silently substituted from metadata. No outside individual was contacted, and no external input was requested or drafted. No git/index/commit/push/release/publication operation occurred. Only this detached folder was written. All initial sealed public members were rehashed at finalization.

