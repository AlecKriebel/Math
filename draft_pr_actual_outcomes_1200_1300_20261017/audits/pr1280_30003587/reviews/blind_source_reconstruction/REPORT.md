# Independent source reconstruction: problem30003587

This is the initial, candidate-blind report. Its scope is the mathematical question authenticated below. No candidate submission, pull request, current edition, sibling review, or prior reviewer conclusion was inspected. The exposure declaration and manifest are separate files in this directory.

## Verdict and scope

**Affirmative, as a deduction from the authenticated outer/aperiodic theorem and the explicit reductions proved here.** The reductions address periodic irreducible graphs, inner elements, nonfaithful actions, invariance under the entire action, and the absence of any splitting assumption on the acting group. No unresolved mathematical gap was identified in this reconstruction's self-check. Independent adversarial verification of these new reductions remains appropriate before treating this report as a promoted research result.

This verdict concerns the original question. It does not authenticate any candidate proof and does not claim that the reductions are new in the literature. The search was for primary dependencies and was not an exhaustive novelty search.

## 1. Source authentication and exact target

Primary source: Selcuk Barlak's contribution, joint work with Gabor Szabo, printed page 2621, in *Mini-Workshop: MASAs and Automorphisms of C*-Algebras*, Oberwolfach Reports 14 (2017), no. 3, 2601-2629, DOI [10.4171/OWR/2017/42](https://doi.org/10.4171/OWR/2017/42). The publisher's [landing page](https://ems.press/journals/owr/articles/15585) and [PDF body](https://ems.press/content/serial-article-files/46706) were fetched. PDF page 21, printed 2621, was rendered and visually checked against the extracted text.

The workshop ran 2017-09-17 through 2017-09-23. Publisher metadata gives submission 2017-09-17 and publication 2018-07-05. Thus the volume year and actual report publication date differ.

The source setup is a finite matrix \(A\in M_n(\{0,1\})\), with no zero rows or columns, and canonical generators \(T_i\) of \(\mathcal O_A\). Its diagonal quasi-free condition is

\[
\alpha_g(\operatorname{span}\{T_i\})=\operatorname{span}\{T_i\},
\qquad \alpha_g(T_iT_i^*)=T_iT_i^*.
\]

Question 1 assumes that \(G\) is finite abelian and \(\mathcal O_A\) simple purely infinite. The requested conclusion, spelled out there, is exactly

\[
\forall g\in G\quad\exists u_{g,k}\in\mathcal U(\mathcal O_A^\alpha):
\quad \|u_{g,k}a u_{g,k}^*-\alpha_g(a)\|\longrightarrow0
\quad(a\in\mathcal O_A).
\tag{SAI}
\]

The question imposes neither outerness nor aperiodicity. The following Theorem 2 imposes both: \(A\) primitive, meaning some \(A^m\) has every entry positive, and \(\alpha_g\) outer for every \(g\ne1\).

The report's Theorem 2 is the imported deep input **(BS)** in this reconstruction. Its proof is not reconstructed here. The primary [arXiv v1](https://arxiv.org/abs/1708.08258v1), dated 2017-08-28, and [v3](https://arxiv.org/abs/1708.08258v3), dated 2018-10-03, corroborate the restricted theorem and definition. The v3 definition of diagonal quasi-free fixes domain projections and is broader than the workshop's range-projection condition; that broader definition is unnecessary below. No theorem for aperiodic outer actions is silently applied to a periodic or nonouter action.

Two distinctions are essential:

1. In (SAI), \(u_{g,k}\) is fixed by **all** \(\alpha_h\), not just by \(\alpha_g\).
2. Approximate representability additionally asks for compatible approximate group laws among implementing unitaries. Nothing below establishes or uses that additional requirement.

## 2. Convert the original action to an edge-phase action

Write \(p_i=T_iT_i^*\). Since the \(p_i\) are orthogonal and fixed, applying \(p_i\) to an expansion of \(\alpha_g(T_i)\) in the generator span gives

\[
\alpha_g(T_i)=\chi_i(g)T_i,\qquad \chi_i\in\widehat G.
\tag{2.1}
\]

The coefficients have modulus one because the nonzero range projection is preserved. The group law gives the character identity.

Let \(E\) have vertices \(1,\ldots,n\) and an edge \(e=(i,j)\) exactly when \(A(i,j)=1\). In \(\mathcal O_A\), set

\[
s_{(i,j)}=T_i p_j.
\]

Then \(s_e^*s_e=p_{r(e)}\) and \(p_v=\sum_{s(e)=v}s_es_e^*\). Conversely \(T_i=\sum_{j:A(i,j)=1}s_{(i,j)}\), so this identifies \(\mathcal O_A\) with \(C^*(E)\). In this presentation

\[
\alpha_g(p_v)=p_v,\qquad
\alpha_g(s_e)=\chi_e(g)s_e.
\tag{2.2}
\]

Below we prove the result for arbitrary edge characters \(\chi_e\in\widehat G\); thus the intermediate changes in edge phases remain within the class being treated.

### Why the graph is irreducible, including the reducible boundary case

The no-zero-row/column conditions mean that \(E\) has no sinks or sources. If it were not strongly connected, take a terminal strongly connected component \(K\) in its condensation graph. There is an outside cycle: following predecessors of any vertex outside \(K\) never enters terminal \(K\), and a repeated predecessor gives a cycle outside \(K\).

The ideal generated by the nonzero \(p_v\), \(v\in K\), is proper. One direct verification uses the prefix representation on the Hilbert space with basis the infinite paths which never enter \(K\). This set is nonempty because of the outside cycle, is closed under the shift and allowed prefixes, and supports a Cuntz-Krieger representation killing every \(p_v\) in \(K\) but not every vertex projection. Thus the ideal is nonzero proper, contradicting simplicity.

Consequently \(E\) is strongly connected. It is not a directed cycle, since a directed-cycle algebra is a matrix algebra over \(C(\mathbb T)\), which is not simple. Every cycle has an exit: a cycle without exits in a strongly connected graph forces the entire graph to be that cycle. The canonical path diagonal

\[
D_E=C^*(s_\mu s_\mu^*: \mu\text{ a finite path})\cong C(E^\infty)
\]

is therefore a MASA. This is the standard graph-diagonal fact documented in Renault's primary [*Cartan Subalgebras in C*-Algebras*, section 6.3, printed 58-59](https://www.maths.tcd.ie/pub/ims/bull61/S6101.pdf). The action (2.2) fixes \(D_E\) pointwise.

## 3. Classify the inner edge-phase automorphisms

Fix edge scalars \(\lambda_e\in\mathbb T\) defining \(\theta(s_e)=\lambda_es_e\), \(\theta(p_v)=p_v\). For a strongly connected finite graph with exits, the following are equivalent:

\[
\begin{array}{ll}
\mathrm{(i)}&\theta\text{ is inner};\\
\mathrm{(ii)}&\prod_{e\in\mu}\lambda_e=1\text{ for every closed path }\mu;\\
\mathrm{(iii)}&\lambda_e=f(s(e))\overline{f(r(e))}\text{ for some }f:E^0\to\mathbb T.
\end{array}
\tag{3.1}
\]

**Proof.** If \(\theta=\operatorname{Ad}u\), its pointwise fixing of the MASA implies \(u\in D_E\). Regard \(u\) as a circle-valued continuous function on infinite paths. For every edge and infinite tail \(x\) starting at its range,

\[
u(ex)=\lambda_eu(x).
\]

For a closed path \(\mu\), evaluate the iterated equation at \(x=\mu\mu\mu\cdots\). Since \(\mu x=x\), its scalar product must be one. This proves (i) implies (ii).

Choose a base vertex \(v_0\) and paths \(P_v\) from \(v_0\) to \(v\), with \(P_{v_0}\) empty. Put

\[
f(v)=\Big(\prod_{e\in P_v}\lambda_e\Big)^{-1}.
\]

Appending a return path from \(v\) to \(v_0\) shows this is independent of the path choice: the products around both resulting closed paths are one. Comparing \(P_{s(e)}e\) with \(P_{r(e)}\) gives (iii). Finally

\[
z=\sum_v f(v)p_v\quad\text{satisfies}\quad
\operatorname{Ad}z(s_e)=f(s(e))\overline{f(r(e))}s_e.
\]

Thus (iii) implies (i). Normalization \(f(v_0)=1\) makes the vertex potential unique. \(\square\)

This does more than show that the implementer is diagonal: the implementer can be chosen in the **finite vertex diagonal**. That finite-level conclusion is what makes the next reduction stay within edge-phase actions.

## 4. Remove the inner subgroup without assuming a group splitting

Define

\[
H=\{h\in G:\alpha_h\text{ is inner}\}.
\]

It is a subgroup, and contains the entire kernel of the action. For \(h\in H\), let \(f_h(v)\) be the unique normalized potential from (3.1). Products of potentials implement products of automorphisms; uniqueness gives

\[
f_{hk}(v)=f_h(v)f_k(v).
\]

For every vertex \(v\), the map \(h\mapsto f_h(v)\) is therefore a character of \(H\). Every character of a subgroup of a finite abelian group extends to the full group. One elementary proof adjoins one group element \(x\) at a time: if the least positive \(r\) with \(rx\in H\) is given, choose an \(r\)-th root in \(\mathbb T\) of the already assigned value at \(rx\), and use it to extend the character to \(H+\langle x\rangle\). Induction finishes. No complement to \(H\) is needed.

Choose extensions \(\widetilde f_v\in\widehat G\), taking the base vertex extension to be trivial, and define the genuine representation

\[
u_g=\sum_v\widetilde f_v(g)p_v\in\mathcal U(D_E),
\qquad
\beta_g=\operatorname{Ad}(u_g^*)\circ\alpha_g.
\tag{4.1}
\]

Because all \(u_g\) commute and are fixed by \(\alpha\), \(\beta\) is a group action. Its edge phases are

\[
\eta_e(g)=\chi_e(g)\overline{\widetilde f_{s(e)}(g)}\widetilde f_{r(e)}(g).
\tag{4.2}
\]

For \(h\in H\), \(\beta_h=\mathrm{id}\). Hence \(\beta\) descends to \(Q=G/H\). The resulting \(Q\)-action is pointwise outer: if \(\beta_g\) were inner, (4.1) would make \(\alpha_g\) inner and therefore \(g\in H\).

This separates the nonouter and kernel cases explicitly. It does **not** form a quotient action from \(\alpha\) itself unless its inner elements are trivial. It first removes their vertex implementers by (4.1).

## 5. A unitary compression lemma

Let a finite family of orthogonal fixed projections \(q_j\) sum to the unit of a unital algebra \(B\). Suppose \(w_k\in\mathcal U(B^\gamma)\) and \(\operatorname{Ad}w_k\to\theta\), where \(\theta(q_j)=q_j\). Then \([w_k,q_j]\to0\). Therefore

\[
x_k=\sum_jq_jw_kq_j,
\qquad \|x_k-w_k\|\to0.
\]

For sufficiently large \(k\), \(x_k\) is invertible. Its polar unitary

\[
z_k=x_k(x_k^*x_k)^{-1/2}
\tag{5.1}
\]

lies in \(B^\gamma\cap\{q_j\}'\), satisfies \(\|z_k-w_k\|\to0\), and implements the same point-norm limit. This uses exact fixed projections and functional calculus inside their fixed commutant. It does not average arbitrary unitaries and assume the average is unitary.

## 6. Eliminate the graph period by a return corner

For now let \(\gamma:Q\curvearrowright C^*(E)\) be a pointwise outer edge-phase action, with \(E\) finite strongly connected and not a directed cycle. Let \(d\ge1\) be the graph period. Write its cyclic classes as

\[
E^0=V_0\sqcup\cdots\sqcup V_{d-1},
\qquad e:V_r\longrightarrow V_{r+1\pmod d}.
\]

Set \(p=\sum_{v\in V_0}p_v\). Define \(F\) with vertex set \(V_0\) and one edge for every path in \(E\) of length \(d\) starting in \(V_0\). Such paths end in \(V_0\). The adjacency matrix of \(F\) is the \(V_0\) block of \(M_E^d\), and is primitive. This is the elementary period decomposition of an irreducible nonnegative matrix: within a cyclic class the gcd of the return lengths, divided by \(d\), is one, and all sufficiently large such lengths connect any prescribed pair of vertices.

There is a canonical isomorphism

\[
C^*(F)\cong B:=pC^*(E)p,
\qquad s_{\text{edge }\mu}\longmapsto s_\mu.
\tag{6.1}
\]

Here are the needed checks. The length-\(d\) path family satisfies the graph relations by iterating the Cuntz-Krieger relation. It generates the whole corner: a spanning monomial \(s_\mu s_\nu^*\) in the corner starts in \(V_0\), and the two paths end at the same vertex in some \(V_r\). Append every path of length \(\ell\equiv-r\pmod d\), \(0\le\ell<d\), and expand

\[
s_\mu s_\nu^*
=\sum_{\substack{s(\tau)=r(\mu)\\|\tau|=\ell}}
s_{\mu\tau}s_{\nu\tau}^*.
\]

Both new lengths are multiples of \(d\), so every term is in the algebra generated by length-\(d\) paths. The graph \(F\) is strongly connected aperiodic. It has branching, because a branching vertex of \(E\), preceded by the appropriate fewer-than-\(d\) edges from \(V_0\), yields two distinct length-\(d\) paths. Thus \(F\) has at least two edges. Its edge matrix is primitive, so its graph algebra is simple by the standard primitive Cuntz-Krieger result. The nonzero surjection in (6.1) is injective.

For completeness, a finite graph with no sinks is canonically the Cuntz-Krieger algebra of its edge matrix

\[
N(e,f)=\mathbf1_{\{r(e)=s(f)\}}.
\]

The edge generators form the required Cuntz-Krieger family, and conversely the vertex projection is the sum of the ranges of generators with that source. These two universal constructions are inverse. If the vertex adjacency matrix has a strictly positive \(m\)-th power, \(N^{m+1}\) is strictly positive. This explains precisely why the imported matrix theorem (BS) applies to \(F\).

The action on \(B\) fixes its vertices and multiplies its generating length-\(d\) paths by characters. It remains to check outerness on this corner and lift (SAI). Both checks use an explicit finite frame, rather than an unproved assertion that the properties pass through Morita equivalence.

### The homogeneous frame

Take \(t_0=p\). For each \(r\ne0\), include all paths starting in \(V_r\) of length \(d-r\), and let \(t_i\) be their partial isometries. Then

\[
e_i:=t_i^*t_i\le p,
\quad e_0=p,
\quad e_i=p_{r(t_i)}\ (i>0),
\quad t_i^*t_j=0\ (i\ne j),
\quad\sum_i t_it_i^*=1.
\tag{6.2}
\]

All these statements follow from the fixed path lengths within each starting class and the Cuntz-Krieger relation. Each \(t_i\) is homogeneous:

\[
\gamma_h(t_i)=\rho_i(h)t_i,
\qquad \rho_i\in\widehat Q,
\qquad \rho_0=1.
\tag{6.3}
\]

### Corner outerness

Suppose \(\gamma_g|_B=\operatorname{Ad}v\), \(v\in\mathcal U(B)\). Since the vertex projections in \(B\) are fixed, \(v\) commutes with every \(e_i\). Define

\[
V=\sum_i\rho_i(g)t_i v t_i^*.
\tag{6.4}
\]

Equations (6.2) imply \(V^*V=VV^*=1\). Expanding any \(a\) as

\[
a=\sum_{i,j}t_i(t_i^*a t_j)t_j^*
\tag{6.5}
\]

shows \(\operatorname{Ad}V(a)=\gamma_g(a)\). Thus an inner restriction would give an inner automorphism on the full graph algebra. Since the original \(Q\)-action is pointwise outer, the corner action is pointwise outer.

### Apply (BS), then lift with invariance under all of \(Q\)

By (BS) on the primitive edge matrix of \(F\), for each \(g\in Q\) there are \(w_k\in\mathcal U(B^{\gamma|_B})\) with \(\operatorname{Ad}w_k\to\gamma_g|_B\). Apply the compression lemma to the vertex projections of \(B\); henceforth assume \(w_k\) commutes exactly with them and therefore with every \(e_i\). Put

\[
W_k=\sum_i\rho_i(g)t_i w_k t_i^*.
\tag{6.6}
\]

The same calculation as in (6.4) makes \(W_k\) a unitary. For **every** \(h\in Q\),

\[
\gamma_h(W_k)
=\sum_i\rho_i(g)\rho_i(h)\overline{\rho_i(h)}t_i w_k t_i^*
=W_k.
\tag{6.7}
\]

This is whole-action invariance. Using (6.5), the difference between \(\operatorname{Ad}W_k(a)\) and \(\gamma_g(a)\) is the finite sum of terms

\[
\rho_i(g)\overline{\rho_j(g)}\,
t_i\big[w_k(t_i^*at_j)w_k^*-\gamma_g(t_i^*at_j)\big]t_j^*,
\]

each converging to zero. Thus the entire pointwise outer action \(\gamma\) is strongly approximately inner, including when \(E\) has period greater than one.

## 7. Recover the original nonouter action with the correct fixed algebra

Apply section 6 to the outer \(Q=G/H\)-action \(\beta\) from section 4. If \(Q\) is trivial, every \(\alpha_g\) is already implemented by its invariant vertex unitary and nothing remains. Otherwise, for each \(g\in G\), choose

\[
w_{g,k}\in\mathcal U(C^*(E)^\beta),
\qquad \operatorname{Ad}w_{g,k}\longrightarrow\beta_g.
\]

Compress these unitaries by **all original vertex projections**, using section 5, to obtain \(z_{g,k}\) with the same implementing limit, still in \(C^*(E)^\beta\), and commuting exactly with every \(p_v\). Consequently they commute with every \(u_h\) from (4.1). For every \(h\in G\),

\[
\alpha_h(z_{g,k})
=u_h\beta_h(z_{g,k})u_h^*
=z_{g,k}.
\]

Also \(u_g\) is fixed by all of \(\alpha\). Therefore

\[
U_{g,k}=u_gz_{g,k}\in\mathcal U(C^*(E)^\alpha),
\qquad
\operatorname{Ad}U_{g,k}\longrightarrow
\operatorname{Ad}u_g\circ\beta_g=\alpha_g.
\tag{7.1}
\]

Equation (7.1) is exactly (SAI) for the original action. This last compression step is essential: arbitrary implementing unitaries fixed by a cocycle-modified action need not be fixed by the original action.

## 8. Falsification checks and boundary cases

The proof is analytic and algebraic. `check_reductions.py` adds finite exact falsification checks for the graph period, closed-path criterion, vertex-potential criterion, subgroup character extensions, removal of the inner subgroup, and preservation of the inner subgroup under the return graph. These computations do not prove MASA facts, the imported (BS) theorem, or convergence in a C*-algebra.

The recorded run checked 52 deterministic examples and passed. It includes an explicit nonsplit case: \(G=\mathbb Z/4\), two vertices, two parallel edges in each direction, with every edge phase \(i^g\). The graph has period two; \(H=\{0,2\}\); \(\alpha_2\) is implemented by \(p_0-p_1\). Choose \(u_g=p_0+i^gp_1\). Then \(\beta_g\) has edge phases \((-1)^g\) from vertex zero to one and one in the reverse direction. It factors through the outer \(\mathbb Z/2\)-action, without a complement to \(H\). The return corner has one vertex and four loops, each with phase \((-1)^g\). This checks the signs in (4.2) and the periodic/nonsplit interaction concretely.

Additional checks addressed the following failure modes:

- **Primitive versus merely irreducible.** Only the return graph is passed to (BS); its edge matrix is explicitly primitive.
- **Nonouter actions.** Only the modified quotient action is passed to (BS); its pointwise outerness is proved.
- **Action kernels.** Kernels lie in \(H\). A kernel element has trivial normalized vertex potential. The quotient construction does not require original faithfulness.
- **Whole-action invariance.** Equations (6.7) and (7.1) establish invariance under every group element, for each unitary in each sequence.
- **Unitary averaging.** Averaging/compressing a unitary alone is insufficient; the argument uses eventual invertibility and polar correction.
- **Full-corner lifting.** The frame coefficients \(\rho_i(g)\) in (6.6) account for the automorphism on the frame. Omitting them would generally fail on cross-corner terms.
- **Inner corner restrictions.** Equation (6.4) proves precisely the needed outerness implication.
- **One-edge/cycle exceptions.** Simplicity excludes the original directed-cycle algebra, and branching survives in the return graph, so the primitive theorem's size restriction is met.
- **Group laws.** The auxiliary vertex unitaries \(u_g\) form an exact representation because characters were extended. The final \(U_{g,k}\) are not asserted to satisfy any group law; the conclusion remains strong approximate innerness.

## 9. Approach-family record and strongest established result

| Mechanism | Evidence | Status | Exact gap |
| --- | --- | --- | --- |
| Read the workshop's theorem as already answering the whole question | Source body has extra outer and primitive hypotheses | Insufficient alone | Those hypotheses cannot be dropped by citation |
| Primitive return graph plus explicit homogeneous frame | Sections 5-6, equations (6.2)-(6.7) | Complete deduction given (BS) | No remaining gap identified in self-check |
| Remove inner subgroup by finite vertex potentials | Sections 3-4 and 7; nonsplit example and exact checks | Complete deduction | Uses standard diagonal-MASA theorem under exits |
| Simply quotient the original action by its inner subgroup | Inner elements can be nontrivial automorphisms | Blocked | Not an action of the quotient without correction |
| Assert cocycle invariance of strong approximate innerness | Fixed algebras can change | Blocked as a general shortcut | Replaced here by exact vertex commutation |
| Demand approximate representability | Additional compatibility among implementing sequences | Not pursued | Not required by the original question |

The strongest result established in this report is the original affirmative statement, conditional only on accepting the explicitly identified known theorem (BS) and standard graph-diagonal structural facts. It is not merely the restricted outer/primitive statement. The report supplies all additional reductions used to cover the original scope.

The main remaining audit task is independent adversarial verification of the extension proof, especially the inner-phase characterization and the full-corner construction. This is a validation step, not an unproved mathematical lemma being silently assumed. There has been no candidate comparison and no conclusion about the correctness, novelty, or publication readiness of any candidate text.

## 10. Reproducibility and completion

Run `python3 check_reductions.py` in this directory to repeat the finite checks. Primary bodies, extracts, images, fetch headers, and provider outputs are confined to `_local/` and are excluded from the public authored-output membership. `QUERY_LEDGER.md` gives literal requests, URLs, and authored statuses without reproducing source excerpts. `MANIFEST.json` enumerates public authored membership with exact bytes and SHA-256; `_local/PRIVATE_SOURCE_MANIFEST.json` separately enumerates the primary evidence cache.

The actual initial sealing completion UTC is recorded in `SEAL.json` after all content, finite checks, and manifests have been completed. The manifest intentionally does not hash itself or the seal, avoiding a circular hash dependency.
