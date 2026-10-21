# Independent AI mathematical audit: diagonal quasi-free finite abelian actions

Date of historical audit: 11 October 2026. Current editorial qualification: 17 October 2026 local date.

Editorial provenance: the original submitted report remains verbatim in the verification package. This current edition qualifies the former absolute pinching-necessity sentence. Its historical first-person source and execution statements are retained as historical claims, not as newly authenticated events. The intermediate graph statements are now explicitly restricted to graphs with at least one edge, excluding the edgeless singleton before the Kirchberg and infinite-path arguments; essentiality already guarantees this for the original target. The older frozen proof, audit and supplement named below are unavailable in the submitted nine-file packet; current independent mathematical review does not certify those missing bytes or the old execution history.

This is an AI-assisted audit. Independence refers to a separately authored mathematical review and separately authored finite checks. It does not mean external human peer review or formal proof-assistant certification. First-person inspection statements below describe that AI audit. The frozen audited proof and this public editorial edition are bound in ACCEPTANCE.json.

Problem: 30003587; OWR2017/42, printed p.2621, Question 1.

## Verdict

**ACCEPT the mathematical argument in the frozen proof identified below for its stated theorem.** No mathematical repair is required. The reductions correctly remove the outerness and aperiodicity restrictions from the published Barlak–Szabó result for the precise original finite Cuntz–Krieger presentation. This acceptance relies on the identified published operator-algebra inputs, as ordinary mathematical proofs do; it is not an independent reproof of those inputs, a novelty certification, a publication authorization, or acceptance of any stronger approximate-representability claim.

Audited candidate: 14,337 bytes, SHA-256
`00ec1535e8dea4958ba73c5afd37758a678c4f7430746318d1761d4056e04e5f`.

I read the entire frozen candidate, independently recomputed the corner/frame and action identities, checked the source statements described below, and ran separately authored finite combinatorial stress checks. I did not modify the candidate or execute its author's code.

## 1. Exact source scope and definition

The opening paragraph on OWR printed p.2621 explicitly assumes a finite 0–1 matrix with **no zero rows or columns**. Its diagonal quasi-free definition preserves the linear span of the canonical generators and fixes their individual range projections. Question 1 includes nonouter actions and does not assume an aperiodic matrix. The theorem printed below the question imposes both additional restrictions. I inspected this page visually.

Barlak–Szabó's Definition 2.5, arXiv v3 p.10, requires, separately for each group element, a sequence of unitaries in the fixed algebra of the **entire** action implementing that automorphism in point norm. It does not impose a group law on the approximating unitaries. Their Corollary 2.7, p.13, retains outer action and aperiodic 0–1 matrix; their graph version, Corollary 2.8, pp.14–15, retains outer action and strongly connected aperiodic finite graph with at least two edges. The proof uses precisely this graph version and does not misattribute the broader result to that paper.

Sources: [OWR2017/42](https://publications.mfo.de/bitstream/handle/mfo/3607/OWR_2017_42.pdf#page=21); [Barlak–Szabó v3](https://arxiv.org/pdf/1708.08258v3).

## 2. Matrix and graph conventions

The correspondence in the candidate is correct:

- vertices are the matrix indices;
- there is one edge i→j when M(i,j)=1;
- p_i=s_i s_i* and T_ij=s_i p_j;
- conversely s_i is the sum of outgoing T_ij.

For distinct edges, T_ij* T_kl=0, while T_ij* T_ij=p_j and the outgoing range projections sum to p_i. Conversely, the cross terms T_ij T_ik* vanish for j≠k because their right-support projections p_j,p_k are orthogonal. Thus both directions satisfy the respective universal relations and are inverse. These are identities on the actual presented algebras, not only stable equivalences.

The original range-fixing definition forces eigenvector generators: p_j α_g(s_i)=0 for j≠i, and hence a span-preserving image of s_i has only its s_i coefficient. The coefficient is unimodular, and the action law makes it a character. Therefore the transferred action is edge-diagonal in exactly the convention used in the reduction.

### Why strong connectivity is legitimate here

Simplicity of an arbitrary finite graph algebra does not force strong connectivity if source vertices are allowed. The candidate avoids that false assertion: no zero columns rules out graph sources, and no zero rows rules out sinks.

If the finite component graph has more than one component, choose a terminal component T and a distinct source component S. Every vertex of S has an incoming edge in S, so S contains a cycle. Starting with T and repeatedly saturating cannot absorb the vertices of that cycle: every cycle vertex still emits an edge to the next cycle vertex outside the current set. The saturated hereditary closure of T is consequently nonempty and proper. Its graph ideal contradicts simplicity. This verifies the candidate's argument. Once strong connectivity is established, the directed-cycle case is excluded because its algebra is a matrix algebra over C(T).

## 3. Inner-kernel reduction

The MASA step is valid. In a strongly connected graph that is not a directed cycle, every cycle has an exit. An edge-diagonal automorphism fixes every finite-path range projection, thus the whole canonical diagonal pointwise. An inner implementer therefore lies in that diagonal's commutant, which is the diagonal itself.

The required MASA input is explicitly stated in Conti–Hong–Szymański, §2.1, p.5. I also inspected the primary Hopenwasser–Peters–Power Theorem 5.2, printed p.360. That paper reads graph paths in the opposite convention: its no-sources/entrance wording translates to the no-sinks/exit wording here. Its §2, printed p.354, explicitly explains this reversal. No unjustified AF-core MASA assertion is used.

For a diagonal unitary h and path μ, S_μ* h S_μ evaluates at an infinite path x as h(μx). Applying this to the intertwining equation yields h(μx)=z_μ h(x). For a closed μ, the periodic path μμμ… is an allowed infinite path, and h never vanishes, so z_μ=1. This checks all closed directed paths, not only a selected collection of cycles.

With fixed paths θ_v:b→v and a return path from r(e) to b, compare θ_s(e)eη and θ_r(e)η. Their unit cycle products imply

z_e=z_θ_s(e)^(-1) z_θ_r(e).

Thus the normalized vertex potential t_v=z_θ_v^(-1) has the correct sign and implements the automorphism by conjugation. Connectivity gives uniqueness after t_b=1.

Most importantly, the frozen candidate does **not** need the originally proposed character-extension argument. It defines

D_g=Σ_v χ_θ_v(g)^(-1)p_v

on all of G directly. This is an exact representation, is fixed by α, and implements α_k for every element k of the inner kernel K. Hence β_g=Ad(D_g*)α_g is an honest action with β_k=id. On an edge its character is χ_θ_s(e) χ_e χ_θ_r(e)^(-1), as written. Innerness is unchanged by multiplication with an inner automorphism, so the induced action of G/K is pointwise outer. There is no hidden projective-representation or cocycle obstruction.

Sources: [Conti–Hong–Szymański](https://arxiv.org/abs/1101.4210v3); [Hopenwasser–Peters–Power](https://nyjm.albany.edu/j/2005/11-18.pdf#page=10).

## 4. Return graph and invariant corner

Let d be the graph period and V_0 one cyclic class. The return graph uses every length-d path starting in V_0 as a distinct edge. Its adjacency matrix is the V_0 block of M^d, and the standard irreducible-matrix cyclic decomposition makes that block primitive. Retaining path multiplicity is essential and the candidate does so.

The return graph has at least two edges. A branching vertex can be preceded by a path from V_0 of length less than d; choose either branch edge and extend to length d. There are no sinks, so both extensions exist and remain distinct. Thus the primitive return graph is not the single-loop exception and has the required exit condition.

The corner surjectivity argument is sound and resolves a potentially serious omission in a mere informal return-graph claim. A spanning element S_μS_ν* of pAp has both initial vertices in V_0 and the same terminal vertex. Therefore |μ| and |ν| agree modulo d. Appending the **same** path τ of the complementary length and summing over all such τ gives exactly S_μS_ν*. Both extended paths then split into length-d return edges. Zero-length paths cause no exception.

Injectivity follows from graph Cuntz–Krieger uniqueness. I inspected Kumjian–Pask–Raeburn Theorem 3.7 in its February 1998 author preprint, p.12: local finiteness, no sinks and condition (L) apply; all return-edge images are nonzero because S_μ* S_μ is their nonzero terminal vertex projection. Thus the candidate's stronger nonzero-vertex formulation supplies the theorem's nonzero-edge hypothesis.

This corner identification is equivariant because products of eigenvector edges are eigenvectors. The candidate correctly does not call the multigraph's possibly integer-valued adjacency matrix a 0–1 matrix. Corollary 2.8 applies directly; alternatively its explicitly given edge matrix is a primitive 0–1 matrix of the required size.

## 5. Full-corner outerness and strong approximate innerness

Both analytic corner lemmas were recomputed independently.

### Finite frame

For a full p in unital B, fullness supplies a finite sum Σ y_i z_i* invertible, with y_i,z_i∈Bp. The displayed row inequality makes Σ y_i y_i* positive invertible. Normalization therefore yields x_i∈Bp with Σ x_i x_i*=1. No Murray–von Neumann equivalence of p and 1 is being assumed.

### Outerness

If σ fixes p and is implemented on pAp by u, then

U=Σ_i σ(x_i)u x_i*

is unitary. Its two norm-square products simplify using u(x_i*x_j)u*=σ(x_i*x_j), and inserting the same frame twice gives UaU*=σ(a). Consequently an outer automorphism remains outer on an invariant full corner. For this lemma the frame need only lie in Ap, not in the fixed algebra.

### Lifting implementing sequences

For strong approximate innerness the different, stronger fullness condition is correctly used: p is full in A^α. A frame inside A^αp then gives

V_n=Σ_i x_i u_n x_i* ∈ A^α.

The Gram entries x_i*x_j are fixed, so both V_n V_n* and V_n*V_n tend to 1. The inverse-conjugation convergence used here is valid: if Ad(u_n)→σ in point norm for an automorphism σ, then Ad(u_n*)→σ^(-1). Inserting x_i* a x_j gives V_n a V_n*→α_g(a). Two-sided near-unitarity makes V_n eventually invertible; functional calculus within A^α gives its polar unitary, which is norm-close and still implements α_g asymptotically. There is no coherence requirement left unproved.

### Fixed-point fullness

Pointwise outer finite-group actions on simple unital A do have simple fixed algebras without any graph-period condition. In the crossed product, e=|G|^(-1)Σ_g λ_g is a nonzero projection and a↦ae identifies A^α with e(A⋊G)e. Indeed, eae=E_α(a)e; injectivity also follows from the coefficient expectation. Kishimoto's Theorem 3.1 makes the crossed product simple. Its nonzero corner is simple, so the nonzero cyclic-class projection is full in A^α.

I verified Theorem 3.1 in the author-uploaded original article's full-text OCR, including its explicit simple-A/pointwise-outer specialization. I additionally inspected Echterhoff–Rørdam's published p.127, which states the same finite-group fixed-point consequence. Neither source has the graph-aperiodicity restriction.

Sources: [Kishimoto original article, author-uploaded full text](https://www.researchgate.net/publication/225983054_Outer_automorphisms_and_reduced_crossed_products_of_simpleC-algebras); [Echterhoff–Rørdam](https://ems.press/content/serial-article-files/42588).

## 6. Restoring the original fixed algebra

The final pinching step correctly supplies fixed-point membership in this argument. A genuine finite abelian cocycle perturbation also admits an averaging/polar alternative, so pinching is not a necessary form of the argument. Exact fixed-algebra membership must still be proved.

For β-fixed implementing unitaries v_n and each vertex p_v, β_g(p_v)=p_v implies ||[v_n,p_v]||→0. Therefore z_n=Σ_v p_v v_n p_v is norm-close to v_n, lies exactly in A^β, and commutes with all vertex projections. Its polar unitary w_n has those same exact memberships and still implements β_g. Every D_h is a vertex-diagonal unitary, so

α_h(w_n)=D_h β_h(w_n)D_h*=w_n.

Since D_g itself is α-fixed, D_g w_n lies exactly in A^α and implements α_g in the limit. This checks the full group's fixed algebra, not merely the fixed algebra of g or of K. The trivial quotient case is harmless: β is trivial and 1 is an implementer.

## 7. Independent finite stress checks

The separately authored finite-check program runs without importing any source-author code. It checks every 0–1 matrix of sizes 1 through 4, including the no-zero-row/column condition. For each essential reducible matrix it verifies a terminal component has proper saturated hereditary closure. For each strongly connected noncycle it computes the period, constructs the return block, tests primitivity within the standard finite exponent bound, and verifies the return graph has at least two edges.

It also exhausts all cyclic phase labelings modulo 2 through 6 on three four-edge graphs, including a periodic branching graph. It compares closed-cycle phase conditions with fixed-base-path potentials, checks the inner-kernel subgroup and checks that the untwisted action has no nontrivial inner elements in its quotient.

Result: PASS; 66,066 matrices considered; 41,776 essential; 25,835 strongly connected noncycles, including 118 periodic examples; 15,931 reducible ideal checks; 6,822 phase labelings and 36,600 group-element checks. These are adversarial regression checks, not a substitute for the all-size mathematical argument or the operator-algebra proof.

## 8. Remaining limitations and disposition

No proof gap, contradictory hypothesis, wrong convention, or missing group implementation has been found in the frozen candidate. No mathematical correction is requested. A polished presentation should retain the precise no-zero-columns assumption, the distinction between fullness in A and in A^α, the multigraph/edge-matrix distinction, and the pinching step. It should cite the primary source locations verified above, and it should continue to distinguish this deduction from the literal statement of Barlak–Szabó's published theorem.

This AI audit accepts the stated deduction only; it is not formal certification. It makes no assertion about first discovery, current community acceptance, bibliographic completeness, or a stronger approximately representable action. No source documents, dataset contents, repository changes, external communications, or publication were produced by this audit.
