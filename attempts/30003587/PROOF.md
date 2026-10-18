# Strong approximate innerness of finite abelian diagonal quasi-free actions

Date: 11 October 2026. Problem 30003587, OWR-15585-006.

**Status:** Accepted after independent AI mathematical audit for the stated theorem. This AI-assisted manuscript relies on the explicitly cited standard operator-algebra results below. No external human peer review or formal proof-assistant certification is claimed. This is a reduction to the published Barlak–Szabó theorem, not a claim that its authors proved the broader statement. No novelty or priority certification is made.

## 1. Statement and the exact property

**Theorem.** Let M be a finite 0–1 matrix with no zero rows or columns and suppose O_M is simple and purely infinite. Every action α of a finite abelian group G by diagonal quasi-free automorphisms, in the sense of OWR2017/42, p.2621, Question 1, is strongly approximately inner.

Here strongly approximately inner means: for each g in G there is a sequence u_{g,n} of unitaries in the **whole action's fixed-point algebra** O_M^α such that Ad(u_{g,n})(a) tends to α_g(a) in norm for every a. No approximate representation relation between different g is asserted or needed.

We prove the more general edge-diagonal statement for a finite strongly connected graph with at least one edge which is not a directed cycle. Write A=C*(E), with vertex projections p_v and edges S_e satisfying S_e* S_e=p_{r(e)}, S_e S_e*≤p_{s(e)}, and p_v=Σ_{s(e)=v}S_e S_e*. Assume

α_g(p_v)=p_v,    α_g(S_e)=χ_e(g)S_e,

where each χ_e is a character of G. For a finite path μ, write χ_μ=∏_{e in μ}χ_e. A vertex, viewed as a length-zero path, has character 1.

## 2. Published inputs, with their scope

1. Barlak–Szabó, arXiv:1708.08258v3, Definition 2.5, p.10, gives the strong approximate innerness definition above. Corollary 2.8, pp.14–15, proves it for an **outer** finite abelian diagonal quasi-free action on a finite **strongly connected aperiodic** graph with at least two edges. We use exactly that restricted theorem. Corollary 2.7 is its 0–1-matrix predecessor.
2. For a finite graph without sinks whose every cycle has an exit, its canonical diagonal D_E is a MASA in C*(E). Conti–Hong–Szymański, arXiv:1101.4210v3, §2.1, p.5, states this in our source/range convention and attributes it to Hopenwasser–Peters–Power, Theorem 5.2. The latter uses the reversed convention, calling the corresponding conditions “no sources” and “every loop has an entrance.”
3. A pointwise outer action of a finite group on a simple unital C*-algebra has simple fixed-point algebra. This follows from Kishimoto's simplicity theorem for the crossed product and the usual identification of the fixed-point algebra with the averaging-projection corner. This does not assume aperiodicity of a presenting graph.
4. We use the standard graph Cuntz–Krieger uniqueness theorem (every cycle has an exit and all vertex images nonzero implies injectivity), and elementary finite strongly connected graph period decomposition. We spell out the relevant corner identification rather than assume an equivariant Morita-invariance theorem.

Public links:
- https://arxiv.org/abs/1708.08258v3
- https://doi.org/10.7146/math.scand.a-114823
- https://arxiv.org/abs/1101.4210v3
- https://nyjm.albany.edu/j/2005/11-18.html
- Kishimoto, “Outer automorphisms and reduced crossed products of simple C*-algebras,” Comm. Math. Phys. 81 (1981), 429–435.

## 3. Inner edge-diagonal automorphisms are vertex coboundaries

**Lemma 1.** If E is finite, strongly connected, has at least one edge, and is not a directed cycle, and an edge-diagonal automorphism σ(S_e)=z_eS_e is inner, there are numbers t_v in the circle such that

z_e=t_{s(e)} conjugate(t_{r(e)}),

and σ=Ad(Σ_v t_v p_v). The coefficients are unique after imposing t_b=1 at one chosen base vertex b.

**Proof.** Every cycle of E has an exit: an exitless cycle in a strongly connected graph would be the whole graph. Thus D_E is a MASA. The automorphism σ fixes each path-range projection and hence D_E pointwise. If σ=Ad(h), this forces h∈D_E.

Identify D_E with C(E^∞), the continuous functions on the compact infinite-path space, taking each path-range projection to the characteristic function of its cylinder. For a path μ and an infinite path x starting at r(μ), the standard diagonal conjugation identity is

(S_μ* h S_μ)(x)=h(μx).

It holds first for cylinder characteristic functions and hence for all h by uniform approximation. From hS_μ=z_μ S_μh we obtain h(μx)=z_μh(x). For a closed path μ, take x=μμμ… . Then μx=x and h(x) has modulus one, so z_μ=1. Thus the product of the edge phases along every closed directed path is 1.

Choose a directed path θ_v from b to v for every v, with θ_b the empty path, and put t_v=z_{θ_v}^{-1}. For an edge e from v to w choose any directed return path η from w to b. Both θ_v e η and θ_w η are closed paths at b. Their phase products equal 1, giving z_{θ_v} z_e=z_{θ_w}, or z_e=t_v conjugate(t_w). Conjugation by Σ_v t_v p_v therefore agrees with σ on all generators. If two normalized vertex potentials have the same edge ratios, their ratio is constant along all directed edges, hence constant by connectivity, and is 1 at b. ∎

**Important simplification.** No extension of characters from a subgroup will be needed. The same fixed paths θ_v define the needed representation on the whole group directly.

## 4. Full-corner lemmas, including exact fixed-point membership

First recall an elementary fact: if p is a full projection in a unital C*-algebra B, there exist finitely many x_i∈Bp with Σ_i x_i x_i*=1. Indeed, fullness gives finite rows Y=(y_i) and Z=(z_i), with entries in Bp, for which YZ* is invertible. The inequality (YZ*)(YZ*)*≤||Z*Z|| YY* shows YY* is positive invertible. Set x_i=(YY*)^{-1/2}y_i.

**Lemma 2 (outerness survives an invariant full corner).** Let σ∈Aut(A), σ(p)=p, with p full. If σ restricted to pAp is inner, then σ is inner on A.

**Proof.** Choose a finite frame x_i∈Ap as above. If σ|_{pAp}=Ad(u), u∈U(pAp), set

U=Σ_i σ(x_i)u x_i*.

For all i,j, u(x_i*x_j)u*=σ(x_i*x_j). Consequently

UU*=Σ_{i,j}σ(x_i)σ(x_i*x_j)σ(x_j*)=1,

and, using u*σ(x_i*x_j)u=x_i*x_j,

U*U=Σ_{i,j}x_i(x_i*x_j)x_j*=1.

For a∈A, each x_i*ax_j lies in pAp, so

UaU*=Σ_{i,j}σ(x_i)σ(x_i*ax_j)σ(x_j*)=σ(a).

Thus σ=Ad(U). ∎

**Lemma 3 (lifting strong approximate innerness).** Let α:G↷A and let p∈A^α be full in A^α. If α restricted to pAp is strongly approximately inner, then α is strongly approximately inner on A.

**Proof.** Choose x_i∈A^αp with Σ_i x_i x_i*=1. Fix g. Let u_n∈U((pAp)^α) implement α_g on pAp in the point-norm limit. Set

V_n=Σ_i x_i u_n x_i* ∈ A^α.

Since x_i*x_j is fixed by α_g,

V_n V_n*=Σ_{i,j}x_i Ad(u_n)(x_i*x_j)x_j* →1.

Likewise V_n*V_n→1 because Ad(u_n*) converges to α_g^{-1} and fixes these same Gram entries. For arbitrary a∈A,

V_n a V_n*=Σ_{i,j}x_i Ad(u_n)(x_i*ax_j)x_j* →α_g(a),

since α_g fixes each x_i. Thus V_n is eventually invertible. Its polar unitary

w_n=V_n(V_n*V_n)^{-1/2}

belongs exactly to A^α, satisfies ||w_n−V_n||→0, and implements α_g asymptotically. Discard finitely many initial n. This is precisely the required strong approximate innerness. ∎

## 5. Removing graph aperiodicity for outer actions

**Lemma 4.** Every outer edge-diagonal finite abelian action on C*(E), for E finite strongly connected with at least one edge and not a directed cycle, is strongly approximately inner, regardless of the graph's period.

**Proof.** Let d be the period of E. Partition E^0 into cyclic classes V_0,…,V_{d−1}, with edges going from V_j to V_{j+1 mod d}. Let p=Σ_{v∈V_0}p_v. This projection is nonzero and α-invariant.

Define the return graph F to have vertices V_0 and one edge for each length-d path in E starting in V_0. Such paths also end in V_0. Keep different paths as different edges: the graph may have multiple edges. Its adjacency matrix is the V_0 block of the dth power of E's adjacency matrix. Standard period decomposition shows this matrix is primitive. In particular F is strongly connected and aperiodic. It is not a directed cycle: E has a branching vertex, and tracing backwards to V_0 by fewer than d steps and then extending to d steps produces at least two return paths from some vertex of V_0. Hence F has at least two edges and every cycle has an exit.

The vertex projections p_v, v∈V_0, and partial isometries S_μ for the length-d paths above form a Cuntz–Krieger F-family. They give a homomorphism C*(F)→pAp. It is injective by graph Cuntz–Krieger uniqueness: the vertex projections are nonzero and F has the exit condition.

For surjectivity, pAp is the closed linear span of S_μS_ν* with s(μ),s(ν)∈V_0 and r(μ)=r(ν). Their lengths are congruent modulo d. Choose k∈{0,…,d−1} so |μ|+k and |ν|+k are both divisible by d. By the graph relations,

S_μS_ν*=Σ_{τ∈E^k, s(τ)=r(μ)} S_{μτ}S_{ντ}*.

Every path on the right decomposes into length-d F-edges, proving surjectivity. This argument covers length-zero μ,ν,τ using the vertex convention. Thus C*(F)≅pAp.

The isomorphism is equivariant for the return-path action α_g(S_μ)=χ_μ(g)S_μ. By simplicity of A, p is full in A. Lemma 2 shows the restricted action is outer: an inner restriction of α_g for g≠1 would make α_g itself inner. The return action satisfies the precise hypotheses of Barlak–Szabó Corollary 2.8, so it is strongly approximately inner.

Finally, outerness and simplicity of A imply A^α is simple. Therefore the nonzero projection p is full in A^α. Lemma 3 lifts strong approximate innerness from pAp to A, with all lifted unitaries still in A^α. ∎

**Optional 0–1 check.** Instead of invoking Corollary 2.8, replace F with its edge matrix L(e,f)=1 exactly when r(e)=s(f). The canonical F-edge generators form an O_L family, giving the canonical equivariant identification. Since F is primitive, for sufficiently large n there is a length-(n−1) path from r(e) to s(f) for every e,f, so L^n(e,f)>0. This verifies both the 0–1 hypothesis and aperiodicity without identifying a multigraph adjacency matrix with a 0–1 matrix.

## 6. Removing outerness

Let K={k∈G: α_k is inner}. This is a subgroup, being the kernel of G→Out(A). Use the fixed directed paths θ_v from Lemma 1 and define, for every g∈G,

D_g=Σ_v χ_{θ_v}(g)^{-1}p_v.

The D_g form a unitary representation of G, and every D_g is fixed by every α_h. By Lemma 1, α_k=Ad(D_k) for k∈K. Define

β_g=Ad(D_g*)∘α_g.

Because α fixes all D_h and the D_g commute and multiply as a representation, β is an action. It is edge-diagonal:

β_g(S_e)=χ_{θ_{s(e)}}(g)χ_e(g)χ_{θ_{r(e)}}(g)^{-1}S_e.

Moreover β_k=id for k∈K, so it factors through H=G/K. The resulting H-action is outer: if β_g is inner, then α_g=Ad(D_g)β_g is inner, hence g∈K. H is finite abelian. If H is nontrivial, Lemma 4 makes β strongly approximately inner. If H is trivial, this conclusion is immediate using the unit 1.

Fix g. Choose v_n∈U(A^β) with Ad(v_n)→β_g. Since β_g fixes every p_v, ||[v_n,p_v]||→0. Pinch onto the vertex-block diagonal:

z_n=Σ_v p_v v_n p_v.

Then z_n∈A^β∩{p_v:v∈E^0}', and

||z_n−v_n||≤Σ_v ||[v_n,p_v]||→0.

Hence z_n is eventually invertible; the polar unitaries

w_n=z_n(z_n*z_n)^{-1/2}

remain in A^β∩{p_v}', are asymptotically equal to v_n, and implement β_g. They commute with all D_h, so for every h∈G,

α_h(w_n)=D_h β_h(w_n)D_h*=w_n.

Thus w_n∈A^α exactly. Each D_g is also α-fixed, so D_g w_n∈U(A^α), and

Ad(D_g w_n)→Ad(D_g)β_g=α_g.

This proves the edge-diagonal theorem with neither extra hypothesis. Pinching and polar decomposition supply the original fixed-algebra membership in this proof. An alternative is available for genuine cocycle perturbations of finite abelian actions: if alpha_g=Ad(d_g) beta_g and d is an honest beta-cocycle, beta-fixed implementers v_n for beta_g give t_n=d_g v_n with ||alpha_h(t_n)-t_n||=||beta_g(d_h)-v_n d_h v_n*|| tending to zero. Finite averaging over alpha, followed by polar decomposition, gives exactly alpha-fixed implementers. This alternative requires the genuine cocycle law; a projective family of pointwise inner implementers does not supply it.

## 7. Returning to the exact queued CK question

In the OWR definition, α preserves span{s_i} and fixes p_i=s_i s_i*. Writing α_g(s_i)=Σ_j c_{ji}(g)s_j, the range condition forces c_{ji}(g)=0 for j≠i: multiplying by p_j gives c_{ji}(g)s_j=0. Thus α_g(s_i)=χ_i(g)s_i, with χ_i a character. Alternatively the slightly broader Barlak–Szabó definition can first be diagonalized by their Proposition 1.8(2); strong approximate innerness is invariant under conjugacy.

Let E be the graph with vertex set {1,…,n} and an edge i→j whenever M(i,j)=1. In O_M put

p_i=s_i s_i*,    T_{ij}=s_i p_j  (M(i,j)=1).

These are a graph Cuntz–Krieger family: T_{ij}*T_{ij}=p_j, their ranges for a fixed source sum to p_i, and distinct edges have orthogonal initial products. Conversely, in C*(E), s_i=Σ_{j:M(i,j)=1}T_{ij} satisfies the O_M relations. These inverse formulas give an isomorphism O_M≅C*(E), with α_g(T_{ij})=χ_i(g)T_{ij}.

The graph has no sinks or sources. Simplicity forces it to be strongly connected. One way to see the last point is to use the standard saturated-hereditary ideal construction: if its component graph has more than one vertex, choose a terminal component T and a distinct source component S. As there are no graph sources, S contains a cycle. The saturated hereditary closure of T cannot contain that cycle and is therefore proper; it gives a nonzero proper ideal, a contradiction. Strong connectivity plus simplicity and pure infiniteness excludes a directed cycle (whose algebra is a matrix algebra over C(T)).

The edge-diagonal theorem now applies and proves the stated affirmative answer to the exact OWR Question 1.

## 8. Scope, provenance, and acceptance cautions

This proof does not infer aperiodicity from simplicity. It constructs an aperiodic return graph and proves the required equivariant corner transfer. It does not infer strong approximate innerness from ordinary approximate innerness. It explicitly constructs approximating unitaries in the fixed algebra of the original action.

The substantive external theorem remains Barlak–Szabó's aperiodic outer-action result. The added reductions are given in full here. The targeted current-source checks located the published theorem with its two original hypotheses, and did not locate a prior explicit statement of the combined reduction. That bounded search is not a novelty certificate. An independent AI audit accepted all lemmas and the graph/CK presentation correspondence without requesting mathematical repair. The acceptance binding records the audited version and the exact editorial changes.

## Verified public source locations

- Original question: Selçuk Barlak, “Diagonal quasi-free automorphisms of Cuntz–Krieger algebras,” Oberwolfach Reports 2017/42, printed p.2621, Question 1. [Report PDF, page 21](https://publications.mfo.de/bitstream/handle/mfo/3607/OWR_2017_42.pdf#page=21).
- Selçuk Barlak and Gábor Szabó, “On diagonal quasi-free automorphisms of simple Cuntz-Krieger algebras,” Math. Scand. 125 (2019), 210–226. [Published article](https://doi.org/10.7146/math.scand.a-114823); [arXiv v3](https://arxiv.org/pdf/1708.08258v3), Definition 2.5, p.10; Corollary 2.7, p.13; Corollary 2.8, pp.14–15. The outer and aperiodic hypotheses belong to the cited theorem and are removed by the reductions above.
- Roberto Conti, Jeong Hee Hong and Wojciech Szymański, “Endomorphisms of graph algebras,” J. Funct. Anal. 263 (2012), 2529–2554. [arXiv v3](https://arxiv.org/pdf/1101.4210v3), §2.1, p.5.
- Alan Hopenwasser, Justin R. Peters and Stephen C. Power, “Subalgebras of graph C*-algebras,” New York J. Math. 11 (2005), 351–386. [Publisher PDF](https://nyjm.albany.edu/j/2005/11-18.pdf), Theorem 5.2, printed p.360/PDF p.10; convention discussion, §2, printed p.354/PDF p.4.
- Alex Kumjian, David Pask and Iain Raeburn, “Cuntz-Krieger algebras of directed graphs,” Pacific J. Math. 184 (1998), 161–174. [DOI](https://doi.org/10.2140/pjm.1998.184.161); [February 1998 author preprint](https://documents.uow.edu.au/~dpask/index_files/papers/ckaodg.pdf), Theorem 3.7, preprint p.12; Theorem 1.2, p.5.
- Akitaka Kishimoto, “Outer automorphisms and reduced crossed products of simple C*-algebras,” Comm. Math. Phys. 81 (1981), 429–435. [Publisher](https://doi.org/10.1007/BF01209077), Theorem 3.1, printed p.434. The source verification records text-level inspection of the author-uploaded original; no original PDF acquisition is claimed.
- Siegfried Echterhoff and Mikael Rørdam, “Inclusions of C*-algebras arising from fixed-point algebras,” Groups Geom. Dyn. 18 (2024), 127–145. [DOI](https://doi.org/10.4171/GGD/743); [final publisher PDF](https://ems.press/content/serial-article-files/42588), printed pp.127,129/PDF pp.1,3.

Source hashes, version distinctions and retrieval limitations are recorded in SOURCE_METADATA.json and SOURCE_VERIFICATION.md. They establish which sources were inspected, not formal verification of the mathematics.

Intermediate graph scope: all graph reductions assume at least one edge. In the finite strongly connected case this guarantees no sinks or sources and excludes the edgeless singleton, whose standard graph algebra is C and whose edge-phase action is trivial. The original essential-matrix target automatically supplies edges, no sinks and no sources; its full theorem is unchanged.

## Current review qualification (17 October 2026 local date)

The complete deduction above is retained. The claim that one specific pinch/polar construction is necessary has been replaced by the explicit alternative for genuine finite abelian cocycles. This changes no theorem, graph reduction, or implementing sequence used in the original proof. Matsumoto's 2000 diagonal-coboundary and periodic-point arguments precede the inner-phase mechanism (Lemma 5.14 and Proposition 6.4), and the return corner is a special case of Crisp–Gow's 2004 preprint Theorem 3.1. These mechanisms are credited prior work. The current audit does not establish firstness of the combined full statement or current worldwide openness. Current verification is supplied separately from the historical 11October acceptance and check summaries.

- K. Matsumoto, On automorphisms of C*-algebras associated with subshifts, J. Operator Theory 44 (2000), 91–112, Lemma 5.14 and Proposition 6.4: https://jot.theta.ro/jot/archive/2000-044-001/2000-044-001-005.pdf .
- T. Crisp and D. Gow, Contractible subgraphs and Morita equivalence of graph C*-algebras, arXiv:math/0404542v1 (29April2004), Theorem 3.1 and canonical path map: https://arxiv.org/abs/math/0404542v1 . The current source inspection uses the preprint; final DOI10.1090/S0002-9939-06-08216-5 is bibliographic metadata, without assuming final-body identity.

### Broader prior-theorem consequence identified in the current audit

The full target is also an explicit consequence of Gabe–Szabó's general equivariant uniqueness theorem: arXiv:2205.04933v1 (10 May 2022), Definition 1.15 p.13, Proposition 3.14 p.29 and Theorem 5.8 pp.45–46 (https://arxiv.org/abs/2205.04933v1). For an outer finite abelian edge-phase action, each automorphism is equivariantly homotopic to the identity by interpolating its edge phases. Equivariant uniqueness gives asymptotically implementing, asymptotically whole-action-fixed unitaries; finite averaging and polar decomposition give exactly fixed unitaries. The normalized all-group vertex representation above removes the inner kernel, giving an outer quotient with no graph-period restriction. The genuine-cocycle averaging argument restores the original action. This complete assembly was written and checked in the current audit; it is not attributed as a printed Cuntz–Krieger theorem in that source. Final publication metadata is Acta Math.232(2024),1–77, DOI10.4310/ACTA.2024.v232.n1.a1; inspected theorem locators refer to the actual preprint, not an unavailable final body.

Christensen–Neagu–Szabó, arXiv:2504.12730v1 (17 April 2025), Definition3.1/Remark3.2 pp.11–12 and Theorem3.7 p.15 (https://arxiv.org/abs/2504.12730v1), supplies a prior duality framework for exactly the weaker strong approximate innerness used here. Genuine-cocycle and ambient-full-corner transfer can also be composed from that framework; these are not claimed as newly discovered invariance mechanisms. The current paper is an attributed exposition and complete verification of prior-theorem consequences. No first solution, new mechanism, earliest consequence date, or present worldwide openness is certified.
