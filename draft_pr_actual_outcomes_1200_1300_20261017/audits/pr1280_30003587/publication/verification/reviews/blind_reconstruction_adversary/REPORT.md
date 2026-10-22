# Initial sealed adversarial audit of the source-only reconstruction

Audit object: `../blind_source_reconstruction/REPORT.md`, SHA-256 `265af80eab06273a7093066b58b11cf965885dc133317f541432eab517a4115c`. This audit remains blind to the original candidate, submitted/current editions, other review families, and root reports. It tests the reconstructed argument, not any candidate's correctness or novelty.

## Verdict

**No mathematical gap found.** The reconstructed proof establishes the full workshop Question 1, given the explicitly imported Barlak-Szabo outer/primitive theorem and the standard graph-diagonal MASA theorem. Its new reductions cover graph period, nontrivial inner elements, nonfaithful actions, and invariance under the whole acting group. In particular, the conclusion is not restricted to pointwise outer actions or primitive original matrices.

This is an affirmative independent adversarial verification of the reduction argument, rather than an independent proof of the deep imported theorem. The strongest verified claim is: for a finite essential 0-1 matrix with simple purely infinite Cuntz-Krieger algebra, every action of a finite abelian group satisfying the workshop's diagonal quasi-free condition has, for each group element, a sequence of implementing unitaries in the fixed algebra of the entire action. No approximate group law for those final sequences is asserted or needed.

No repair to a mathematical step is required. Some details compressed in the reconstruction are expanded below to make the finite frame, its coefficient signs, and the original-action invariance directly checkable. Finite computations are supplemental falsification checks and do not establish any operator limit.

## Source authentication and exact imported input

I independently downloaded the publisher PDF at [the workshop body](https://ems.press/content/serial-article-files/46706), extracted it, rendered PDF page 21, and inspected the complete printed page 2621. Question 1 asks for finite abelian actions on simple purely infinite Cuntz-Krieger algebras and specifies implementers in the fixed algebra of the full action. Theorem 2 adds the outer-action and primitive-matrix hypotheses. These additions cannot be discarded merely by citing that theorem.

I independently downloaded [arXiv 1708.08258v3](https://arxiv.org/pdf/1708.08258v3). Definition 2.5, on printed page 10, confirms the per-element, whole-action-fixed implementing sequence. Corollary 2.7, on printed page 13, supplies exactly the outer, primitive matrix theorem. Corollary 2.8, on printed page 14, states the equivalent finite graph version with at least two edges. I visually inspected those complete pages. The matrix theorem suffices; the graph version gives a second direct check of its application to a one-vertex graph with multiple loops.

The action definition in the v3 paper fixes generator domain projections, while the workshop definition fixes their range projections. This difference does not weaken the imported input here: an edge-phase action fixes both. The original question is audited using the workshop definition.

For the standard structural input I independently fetched [Renault's Cartan paper](https://www.maths.tcd.ie/pub/ims/bull61/S6101.pdf), extracted it, and inspected printed pages 58-59, section 6.3. The exit condition gives maximal abelianness of the canonical graph diagonal. The rest of this report derives the needed reductions explicitly. Primary source bodies, extracts, renderings, and direct-fetch records are only in `_local/`; public query statuses are in `QUERY_LEDGER.md`.

## 1. Original action and essentiality boundary

Let `p_i=T_i T_i*`. The fixed, orthogonal range projections imply that an action preserving the linear span of the `T_i` must satisfy

\[
\alpha_g(T_i)=\chi_i(g)T_i,\qquad \chi_i\in\widehat G.
\]

Indeed, multiplying the expansion by `p_j` kills every coefficient except the `j`th; the preserved range of `T_i` leaves only the `i`th term, of modulus one. The action law gives the character law. Nonzero generators follow from the essential finite graph presentation.

With an edge `e=(i,j)` for each `A(i,j)=1`, put `s_e=T_i p_j`. Then

\[
s_e^*s_e=p_j,\quad
\sum_{s(e)=i}s_es_e^*=p_i,\quad
T_i=\sum_{j:A(i,j)=1}s_{(i,j)}.
\]

These mutually inverse generator constructions identify the two universal algebras and transport the action to an edge-phase action. It is legitimate to prove the stronger intermediate assertion allowing arbitrary edge characters, since both vertex-cocycle correction and passage to return paths preserve this class.

The strong-connectivity deduction uses **both** essentiality conditions. In a finite graph without sinks or sources, suppose `K` is a terminal strongly connected component that is not the entire graph. Every predecessor of a vertex outside `K` lies outside `K`, since there is no edge out of `K`. Following predecessors therefore finds an outside cycle. Infinite paths avoiding `K` form a nonempty set closed under the shift and every allowed prefix. The usual prefix operators on its Hilbert-space basis satisfy every graph relation, annihilate `p_v` for `v` in `K`, and leave some outside vertex projection nonzero. Thus the ideal generated by the nonzero vertices in `K` is proper, contrary to simplicity. This validates the reconstruction's reducible boundary argument.

A source-free assumption cannot simply be omitted from that argument: a source attached to a simple purely infinite strongly connected graph can still yield a simple graph algebra without a strongly connected full graph. That boundary is outside the actual finite essential-matrix target.

A strongly connected graph that is not a directed cycle has an exit on every cycle. A cycle without exits cannot reach any vertex or edge outside that cycle. A directed-cycle algebra is a matrix algebra over `C(T)` and is not simple. Consequently the graph here has exits, and its diagonal is the MASA `D=C(E^infinity)`.

## 2. Inner-phase classification, including periodic graphs

For an edge-phase automorphism `theta(s_e)=lambda_e s_e`, pointwise fixedness of `D` and innerness `theta=Ad(v)` imply `v in D' intersect A=D`. Write `v` as a continuous circle-valued function on infinite paths. The equality `v s_e=lambda_e s_e v` gives

\[
v(ex)=\lambda_e v(x).
\]

For every closed path `mu`, its infinite repetition `x=mu mu ...` is an actual point of the diagonal spectrum. Iteration yields

\[
v(x)=\lambda_\mu v(x),\qquad
\lambda_\mu=\prod_{e\in\mu}\lambda_e,
\]

so `lambda_mu=1`. This is valid on periodic paths even when the original graph period is greater than one. No measure-almost-everywhere argument or absence of periodic paths is being used.

Conversely, choose a path `P_v` from a base vertex `o` to each vertex `v`. Put `L_v=lambda_{P_v}` and `f(v)=L_v^{-1}`, with `f(o)=1`. If two choices end at `v`, append one return path from `v` to `o`; the two resulting closed-path products are one, so their initial products agree. Applying this to `P_{s(e)}e` and `P_{r(e)}` gives

\[
\lambda_e=L_{r(e)}/L_{s(e)}
=f(s(e))\overline{f(r(e))}.
\]

Thus `z=sum_v f(v)p_v` implements `theta`. Two such potentials differ by a constant on every edge, and hence everywhere by strong connectivity. The normalization makes the potential unique. In particular, innerness is equivalent to a finite **vertex** potential, not merely to existence of some function in the infinite-path diagonal.

This proves the precise classification required for the inner-subgroup correction. It uses only the established MASA fact and the stated graph hypotheses.

## 3. Character extension without a group complement

Let `H={h: alpha_h is inner}`. It is a subgroup and contains the action kernel. Uniqueness of normalized vertex potentials gives

\[
f_{h+k}(v)=f_h(v)f_k(v),
\]

so `h -> f_h(v)` is a character of `H` for every vertex.

Here is the extension argument with its consistency check. Given a character `c` on a subgroup `K` and `x` outside `K`, let `r` be the least positive integer with `rx in K`. Choose `z in T` satisfying `z^r=c(rx)`. Set

\[
c'(k+mx)=c(k)z^m.
\]

If `k+mx=k'+m'x`, then `m-m'=lr` for an integer `l` and `k-k'=-lrx`. The ratio of the two proposed values is `c(-lrx)z^{lr}=1`. The formula is therefore well-defined and is a character. Repeating it finitely many times extends to the whole finite abelian group. The construction assumes no splitting of `G` over `H`.

Extend every vertex character to `c_v in G-hat`, with `c_o=1`, and put

\[
u_g=\sum_v c_v(g)p_v,\qquad
\beta_g=\operatorname{Ad}(u_g^*)\alpha_g.
\]

Since `u_g` is an exact representation and all its values are fixed by the original action, `beta` is an action. Its edge character is

\[
\eta_e(g)=\chi_e(g)\overline{c_{s(e)}(g)}c_{r(e)}(g).
\]

On `H` this is one, so `beta` factors through `Q=G/H`. If `beta_g` were inner, the formula for `alpha_g` would make it inner, forcing `g in H`. The quotient action is therefore pointwise outer. This includes a nonfaithful original action without any additional assumption.

An explicit essential 0-1 nonsplit check uses the four-vertex complete bipartite directed graph with classes `{0,1}` and `{2,3}` and all arrows in both directions. Let `G=Z/4` scale every edge by `i^g`. The graph period is two, `H={0,2}`, and the normalized implementer of `alpha_2` is `p_0+p_1-p_2-p_3`. Extend the second class's character by `i^g` and the first class's by one. The corrected phases are `(-1)^g` from the first class to the second and one in the reverse direction. They factor through `Z/2` and are outer on its nonidentity element. There is no complementary subgroup to `H` in `Z/4`, and no complement was used. The return graph has two vertices and two parallel edges for each ordered pair; its primitive vertex matrix has every entry two.

## 4. Return corner, primitive edge matrix, and one-vertex boundary

Let `gamma` now be a pointwise outer edge-phase action on the strongly connected graph `E`, whose period is `d`. Write its cyclic vertex classes `V_0,...,V_{d-1}` so every edge advances one class. Put `p=sum_{v in V_0}p_v`. The return graph `F` has vertices `V_0` and length-`d` paths of `E` as edges. The standard irreducible-period decomposition gives a primitive return adjacency matrix; equivalently, all sufficiently large return lengths divided by `d` connect every specified pair in `V_0`.

The length-`d` partial isometries satisfy the graph relations by finite iteration of the Cuntz-Krieger sums. They generate the whole corner `pAp`: in a corner monomial `s_mu s_nu*`, both initial vertices are in `V_0`, both final vertices agree, and both lengths have the same residue `r mod d`. Append all tails of length `ell` with `r+ell=0 mod d`, `0<=ell<d`. The resulting finite Cuntz-Krieger expansion has both path lengths divisible by `d`, so each term is a product of return edges and their adjoints. Length-zero paths cause no exception.

Branching survives in `F`. Take a branching vertex in class `V_r`; by following predecessors, it is reached from `V_0` in exactly `r<d` steps. Each of its two distinct outgoing edges extends to a length-`d` path, since there are no sinks. These give distinct return edges. Thus `F` has at least two edges, including when `V_0` has just one vertex. The edge matrix

\[
N(e,f)=1_{\{r(e)=s(f)\}}
\]

is a finite 0-1 primitive matrix: if the vertex matrix has positive `m`th power, then `N^{m+1}(e,f)` is the positive number of length-`m` paths from `r(e)` to `s(f)`. Its size is at least two. The graph algebra is the Cuntz-Krieger algebra for this edge matrix, with the same generating partial isometries. Primitive simplicity therefore makes the nonzero surjection onto the return corner injective. There is no use of the inadmissible one-generator primitive matrix `[1]`.

In particular, a one-vertex return graph with `k>=2` loops yields the `k` by `k` all-ones edge matrix, precisely a permitted instance of the imported theorem. Multiple graph edges do not create non-0-1 entries in this edge matrix.

## 5. Exact finite homogeneous frame and phase-correct lifting

Set `t_0=p`. For each nonzero cyclic class `V_r`, take **all** paths beginning in that class of length `d-r`, and let their path partial isometries be the other `t_i`. This family is finite. Put `e_i=t_i* t_i`. Each `e_i` is a vertex projection in `V_0`, except `e_0=p`. For distinct positive frame paths, their lengths agree whenever their initial classes agree, so distinct paths are orthogonal by the graph relations. Different initial classes have orthogonal range support. The support of `p` is disjoint from all positive frame ranges. Therefore

\[
t_i^*t_j=\delta_{ij}e_i,
\qquad e_i\le p,
\qquad \sum_i t_it_i^*=1.
\tag{A}
\]

The sum identity is the iterated Cuntz-Krieger relation separately at every vertex. The frame is homogeneous: `gamma_h(t_i)=rho_i(h)t_i`, with characters `rho_i`, and `rho_0=1`.

If `gamma_g` restricted to `B=pAp` were implemented by `v in U(B)`, the fixed vertex projections imply `[v,e_i]=0`. Define

\[
V=\sum_i\rho_i(g)t_i v t_i^*.
\]

Using (A),

\[
V^*V=\sum_i t_i v^*e_i v t_i^*
=\sum_i t_it_i^*=1,
\]

and likewise `VV*=1`. For every `a in A`, expand

\[
a=\sum_{i,j}t_i b_{ij}t_j^*,\qquad
b_{ij}=t_i^*at_j\in e_iBe_j.
\tag{B}
\]

Then `Ad(V)(a)` has coefficients `rho_i(g) conjugate(rho_j(g))` and corner entries `v b_ij v*`, which are exactly the coefficients and entries of `gamma_g(a)`. Thus an inner corner restriction would make the global automorphism inner. Pointwise outerness passes to this particular corner by this explicit calculation.

Apply the imported primitive outer theorem to the action on `B`. For fixed `g`, obtain `w_k in U(B^gamma)` implementing `gamma_g|B`. Vertex compression, justified in the next section, makes these unitaries commute exactly with every vertex in `V_0` and hence every `e_i`. Put

\[
W_k=\sum_i\rho_i(g)t_i w_k t_i^*.
\tag{C}
\]

The same unitary calculation applies. The coefficient is `rho_i(g)`, not its conjugate and not a scalar omitted from the formula. For every `h` in the entire acting quotient,

\[
\gamma_h(W_k)=
\sum_i\rho_i(g)\rho_i(h)\overline{\rho_i(h)}t_i w_k t_i^*
=W_k.
\]

Using (B), the implementation error is the finite sum

\[
\sum_{i,j}\rho_i(g)\overline{\rho_j(g)}\,
t_i\bigl(w_k b_{ij}w_k^*-\gamma_g(b_{ij})\bigr)t_j^*.
\tag{D}
\]

Every entry tends to zero in norm by the corner implementing property; the frame has finitely many entries, so the norm of (D) tends to zero. This is a genuine point-norm deduction. It uses no numerical evidence about C*-algebra limits.

## 6. Polar compression and original whole-group invariance

For finitely many fixed orthogonal projections `q_j` summing to the unit, if `Ad(w_k)(q_j)->q_j`, then

\[
\|[w_k,q_j]\|\to0,\qquad
x_k=\sum_jq_jw_kq_j,
\qquad \|x_k-w_k\|\to0.
\]

Write `delta_k=||x_k-w_k||`. Then `||x_k* x_k-1||<=2 delta_k+delta_k^2`. Eventually `x_k` is invertible; its polar unitary `z_k=x_k(x_k*x_k)^{-1/2}` belongs to the same fixed commutant by functional calculus. The inverse square root tends uniformly to one on the shrinking spectral interval, so `||z_k-x_k||->0`, hence `||z_k-w_k||->0`. Its implementing limit is unchanged. This is not an assertion that averaging unitaries preserves unitarity.

For the original action, first use section 5 for the quotient action `beta`. Compress its implementing unitaries by **all original graph vertex projections**, obtaining `z_{g,k}` in `A^beta` commuting with every `p_v`. They therefore commute with every `u_h` from section 3. For all `h in G`,

\[
\alpha_h(z_{g,k})
=u_h\beta_h(z_{g,k})u_h^*
=z_{g,k}.
\]

The vertex unitary `u_g` is itself fixed by every `alpha_h`. Consequently

\[
U_{g,k}=u_g z_{g,k}\in U(A^\alpha),\qquad
\operatorname{Ad}(U_{g,k})\to
\operatorname{Ad}(u_g)\beta_g=\alpha_g.
\]

This addresses the main potential fixed-algebra obstruction. Merely knowing that an implementer is fixed by the corrected action would be insufficient; exact vertex commutation supplies the missing implication. If the quotient is trivial, the vertex unitary itself already implements the original action, so the all-inner case is included.

## Falsification record and limitations

The independent `check_boundary_cases.py` did not import the reconstruction's checking code. It directly compares closed-walk phase constraints with an exhaustive search for normalized vertex potentials; independently constructs cyclic classes and return paths; checks preservation of the inner subgroup; and tests that distinct frame cylinders are prefix-incomparable. It passed:

- 11,248 edge-labelled strongly connected noncycle 0-1 graphs on two or three vertices over `Z/2`, including 48 periodic cases;
- 64 one-vertex three-loop phase assignments over `Z/4`;
- two essential 0-1 complete bipartite `Z/4` cases, before and after the nonsplit character correction.

The total is 11,314 exact finite cases. The initial local checker used a single short reachability horizon that need not yet be positive in a primitive graph. That checker defect was corrected to enumerate short paths of all relevant lengths; it did not identify a failure of the reconstruction. The successful final code and result are included for reproducibility.

These finite checks cannot establish maximal abelianness, the imported BS theorem, or operator convergence. Those enter respectively through the authenticated structural input, the authenticated deep theorem, and the explicit norm argument (D). No unsupported substitute for these inputs is being inferred from computation.

The audit attempted the named failure mechanisms: hidden splitting, wrong cocycle sign, failure on kernels, unequal frame lengths or invalid supports, missing homogeneous coefficients, nonunitary compression, incorrect whole-group fixedness, an inner return restriction, one-vertex multiloop returns, and misuse of source-free/essential assumptions. None gives a counterexample under the exact target hypotheses. No additional mathematical gap remains identified in this audit. Novelty and the status of any submitted proof remain unaudited here.

The actual initial completion timestamp, exposure state, and exact public membership hashes are recorded in `SEAL.json` and `MANIFEST.json`. This report was completed and sealed before any cross-family feedback was received.
