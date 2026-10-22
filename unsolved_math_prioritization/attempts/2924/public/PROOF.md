# Kirby Problem 4.48: five approaches and the parametric gap

**Problem:** 2924 / KP-4.48. **Outcome:** unresolved after five substantive attempts. No general proof or counterexample is claimed. The established special case and the reductions below are not claimed as novel results.

## 1. Target and conventions

Let Δ be a compact contractible topological 4-manifold, let Σ = ∂Δ, and put

\[
G=\operatorname{Homeo}_{\partial}(\Delta)
 =\{f:\Delta\cong\Delta\mid f|_\Sigma=\mathrm{id}\},
\]

with the compact-open topology. The question is whether **G is contractible**. This is K3 Problem 4.48, printed pp. 228–229 [K3]. Its precise category is topological, not smooth. In particular, nontrivial smooth mapping classes are not automatically counterexamples.

Throughout, “weakly contractible” means nonempty and path-connected, with every positive homotopy group zero. “Contractible” means that the identity map of the entire space is homotopic to a constant. We do not silently identify these notions for this homeomorphism group. GRW's actual Theorem A says **weakly contractible**, even though its abstract and the K3 remark use “contractible.” The extension in [KK26, Theorem 6.18] covers dimension 5, not dimension 4. None of the arguments here even establishes weak contractibility for arbitrary Δ.

A compact manifold is metrizable, so compact-open convergence of self-maps is uniform convergence for any compatible metric. The homeomorphism group is a topological group. All families below use this topology; a continuous family of homeomorphisms has a continuous inverse family.

### Preliminary algebraic topology

Δ is orientable because it is simply connected. Poincaré–Lefschetz duality gives

\[
H_i(\Delta,\Sigma;\mathbb Z)=H^{4-i}(\Delta;\mathbb Z)
 =\begin{cases}\mathbb Z&i=4,\\0&i\ne4.\end{cases}
\]

The long exact sequence of the pair therefore identifies Σ as a connected integral homology 3-sphere. It also shows that the boundary map
\(H_4(\Delta,\Sigma)\to H_3(\Sigma)\) is an isomorphism. A boundary-fixing homeomorphism acts identically on its target and hence preserves the relative orientation class. Thus G already consists of orientation-preserving homeomorphisms. Finally,

\[
H_2(\Delta)=H_2(\Delta,\Sigma)=0,
\qquad H^1(\Delta,\Sigma;\mathbb Z/2)=H_3(\Delta;\mathbb Z/2)=0.
\tag{1}
\]

These elementary vanishings explain both the known connectedness result and the failure of purely homological tests below.

## 2. Attempt 1: construct a contraction by shrinking supports

### 2.1 The disk case, including joint continuity

Write D⁴ as the closed unit ball. For \(0<t\le1\), define

\[
A_t(f)(x)=
\begin{cases}
tf(x/t),&\|x\|\le t,\\
x,&\|x\|\ge t,
\end{cases}
\qquad A_0(f)=\mathrm{id}.
\tag{2}
\]

The formulas agree on \(\|x\|=t\), since f fixes the unit sphere. The map is a homeomorphism: on tD⁴ it is conjugate to f by a dilation, it is the identity outside, and its inverse is \(A_t(f^{-1})\). It fixes the boundary.

For \(t>0\), the adjoint evaluation map \((f,t,x)\mapsto A_t(f)(x)\) is continuous on the two closed regions in (2), and the formulas agree on their overlap. At t = 0 there is the uniform estimate

\[
\sup_x\|A_t(f)(x)-x\|\le 2t,
\tag{3}
\]

independent of f: only points of tD⁴ move, and both their initial and final positions lie there. This proves joint continuity at t = 0 as well. By the compact-open exponential law, (2) is a continuous map of \(\operatorname{Homeo}_\partial(D^4)\times I\) into the homeomorphism group. Since \(A_1(f)=f\) and \(A_t(\mathrm{id})=\mathrm{id}\), reversing t gives a strong contraction. This supplies the continuity verification omitted in the usual brief Alexander-trick account [FNOP25, Lemma 4.4].

### 2.2 Every fixed-disk-supported family contracts

Let \(b:D^4\hookrightarrow\operatorname{int}\Delta\) be a fixed locally flat embedded disk. Extend \(bA_t(f)b^{-1}\) by the identity outside b(D⁴). Pasting on the boundary and uniform continuity of b show that this is a continuous contraction of the subgroup supported in b(D⁴).

More generally, suppose a based map \(\alpha:S^k\to G\) admits a continuous factorization

\[
\alpha(z)=f_1(z)\cdots f_r(z)
\tag{4}
\]

in which each \(f_i(z)\) is supported in one fixed disk \(B_i\subset\operatorname{int}\Delta\). Contract each factor with (2) and multiply. This gives a free nullhomotopy H of α. If the individual factors are not based, replace H(z,t) by \(H(z,t)H(z_0,t)^{-1}\). The endpoints remain α and the constant identity, and the new homotopy is based. Thus (4) kills the homotopy class for every k.

This is a genuine sufficient mechanism, but we have not proved that arbitrary spherical families admit (4), even after a suitable relative collar adjustment. Pointwise decompositions or isotopies do not produce a globally continuous factorization over a sphere.

### 2.3 Why contractibility of Δ does not provide radial coordinates

A contraction of Δ is a family of continuous maps; it is not a family of invertible dilations. Consequently the conjugation in (2) cannot be defined from an arbitrary contraction.

There is also a concrete obstruction to using Δ = cone(Σ). If \(\pi_1\Sigma\ne1\), the cone is not a 4-manifold at its vertex v. Indeed its nested punctured conical neighborhoods have fundamental group \(\pi_1\Sigma\), with all bonding maps isomorphisms. If v had a manifold chart, there would be a punctured 4-ball V and nested conical neighborhoods \(U_\delta\subset V\subset U_\epsilon\). The isomorphism \(\pi_1(U_\delta\setminus\{v\})\to\pi_1(U_\epsilon\setminus\{v\})\) would factor through the zero group \(\pi_1(V\setminus\{v\})\), a contradiction.

**Attempt outcome:** a full, explicit disk-supported contraction, but no uniform shrinking/factorization construction for general G. No counterexample to the target is obtained.

## 3. Attempt 2: kill the algebraic and ordinary homotopy obstructions

### 3.1 The mapping-class calculation really gives π₀G = 0

Δ is spin: its obstruction class in \(H^2(\Delta;\mathbb Z/2)\) vanishes. Orson–Powell's Theorem A [OP25] identifies the spin topological mapping-class group with

\[
H^1(\Delta,\Sigma;\mathbb Z/2)\times
\mathcal V(H_2(\Delta),\lambda_\Delta).
\tag{5}
\]

The first group vanishes by (1). The Poincaré-variation group in the second factor consists of maps \(H_2(\Delta,\Sigma)\to H_2(\Delta)\) satisfying the variation identity. Here both groups are zero, so there is exactly one variation. The orientation observation in §1 allows Theorem A to apply to all of G. Hence G is path-connected.

This invocation is sensitive to the pseudo-isotopy input. [OP25, Theorem 3.1 and §6.2] proves the algebraic classification up to pseudo-isotopy; [GGHKP26, Theorem 1.5] supplies the corrected topological pseudo-isotopy-to-isotopy theorem for all compact simply connected 4-manifolds, including nonempty boundary. Its §5 explains the necessary extension of Perron's original boundary hypotheses, and its §6 repairs Quinn's proof without the disputed replacement criterion. Nothing in these theorem statements gives a continuous choice of isotopy over arbitrary parameter spaces.

### 3.2 The entire relative mapping space is already weakly contractible

Let
\(\mathcal M=\{u:\Delta\to\Delta\text{ continuous}:u|_\Sigma=\mathrm{id}\}\).
The boundary inclusion is a cofibration, using a collar. Consequently restriction

\[
\operatorname{Map}(\Delta,\Delta)\longrightarrow
\operatorname{Map}(\Sigma,\Delta)
\tag{6}
\]

is a homotopy-lifting fibration, whose fiber over the inclusion Σ → Δ is \(\mathcal M\). Both total and base spaces are contractible: postcompose any map with a fixed contraction of Δ. The long exact homotopy sequence, including its component terms, therefore shows that \(\mathcal M\) is weakly contractible.

Every map Δ → Δ is an absolute homotopy equivalence, because Δ is contractible. Thus even restricting (6)'s fiber to maps which are absolute homotopy equivalences imposes no new condition. For any \(\alpha:S^k\to G\), its image in \(\mathcal M\) extends over \(D^{k+1}\). What is missing is an extension through **homeomorphisms**. An ordinary homotopy can introduce noninjectivity and cannot be inverted or used for conjugation.

**Attempt outcome:** the known path-connectedness is rigorously recovered, and every obstruction visible to ordinary relative mapping spaces vanishes. Neither fact controls \(\pi_kG\) for k ≥ 1.

## 4. Attempt 3: puncture Δ and apply embedding calculus

Choose a locally flat disk \(B\subset\operatorname{int}\Delta\), and set
\(C=\Delta\setminus\operatorname{int}B\). Its boundary is \(\Sigma\sqcup S^3\).
Van Kampen applied after inserting collars gives \(\pi_1C=0\), since
\(\Delta=C\cup B\) and \(C\cap B\simeq S^3\). The Mayer–Vietoris sequence shows that the inclusion

\[
S^3=\partial B\longrightarrow C
\tag{7}
\]

is an integral homology equivalence. Both spaces are simply connected and have CW homotopy type, so the homology version of Whitehead's theorem makes (7) a homotopy equivalence. The same sequence, or duality for the cobordism, shows that Σ → C is a homology equivalence. Thus C is a topological one-sided h-cobordism, with the S³ end the homotopy-equivalent end.

Consider the space of locally flat embeddings C → Δ which agree with the original inclusion on Σ, in the relative codimension-zero embedding convention. On the component reached by ambient isotopy, parametrized isotopy extension gives the restriction fibration

\[
\operatorname{Homeo}_\partial(B)\longrightarrow G
\longrightarrow\mathcal E_0.
\tag{8}
\]

Here \(\mathcal E_0\) is the isotopy component of the inclusion; G is connected by §3. The fiber is exactly the boundary-fixing homeomorphism group of the missing disk, extended by the identity on C. It contracts by §2. Therefore (8) identifies the positive homotopy groups of G and \(\mathcal E_0\). We use only this component and do not assume that every arbitrary embedding extends to a homeomorphism. The parametrized extension input is [EK71], also specified in [KK26, §5.4.2].

This is the correct location for the GRW mechanism. In the smooth one-sided h-cobordism setting, [GRW24, §2] proves that the embedding-calculus tower limit is weakly contractible: the first stage is a section-space calculation, the higher layers are section spaces over configuration spaces, and the relevant relative cohomology groups vanish by acyclicity. The final step is convergence from actual embeddings to that limit. It is not a consequence of acyclicity alone.

There is a particularly sharp obstruction to naively applying the original convergence bound in dimension 4. That bound requires relative handle dimension at most d − 3 = 1. If C were obtained from a collar of Σ using only 0- and 1-handles, then \(\pi_1\Sigma\to\pi_1C\) would be injective: attaching a 1-handle adds graph edges/free generators or joins components and introduces no relations in the original component group. Since \(\pi_1C=0\), this is impossible whenever \(\pi_1\Sigma\ne1\). Hence the classical low-handle-dimension convergence hypothesis cannot just be inferred from contractibility of Δ.

[KK26] overcomes part of this issue in dimension 5, but has two explicit boundaries against the desired dimension-4 application:

1. Its Theorems 6.1 and 6.3 assume dimension at least 5. The handle-trading Lemma 6.10 used in their proof has \(k<\min(m-2,m/2)\). With k = 2 this holds for m ≥ 5 and fails for m = 4.
2. The smoothing comparison used in the topological proof, §6.2.2, invokes a pullback statement for m ≠ 4. Formal triviality of Δ's tangent data does not remove this dimensional restriction.

For a nonsmoothable Δ one must also not import smooth embedding calculations without a justified topological comparison. Theorem 6.18 carefully deals with this issue for d = 5; it does not do so for d = 4.

**Attempt outcome:** the exact family-level problem is reduced to a punctured-manifold embedding space; the high-dimensional proof cannot cross its stated convergence and smoothing hypotheses. No convergence theorem in dimension 4 is established here.

## 5. Attempt 4: stabilize to dimension 5 through pseudo-isotopies

Let

\[
P(\Delta)=\{F\in\operatorname{Homeo}(\Delta\times I):
F|_{\Delta\times\{0\}\,\cup\,\Sigma\times I}=\mathrm{id}\}.
\]

Write \(e:P(\Delta)\to G\) for restriction to the top face. The remaining face is preserved by such a homeomorphism, and its boundary is fixed, so e is well-defined. Its fiber over the identity is
\(H=\operatorname{Homeo}_\partial(\Delta\times I)\).

### 5.1 An explicit homotopy-lifting formula

Given a homotopy \(h:Z\times I\to G\) and initial lift \(F_z\in P(\Delta)\) with \(e(F_z)=h(z,0)\), put

\[
\delta(z,s)=h(z,s)h(z,0)^{-1},\qquad
R_{z,s}(x,t)=(\delta(z,st)(x),t),\qquad
\widetilde h(z,s)=R_{z,s}\circ F_z.
\tag{9}
\]

For each (z,s), \(R_{z,s}\) is a homeomorphism with inverse
\((x,t)\mapsto(\delta(z,st)^{-1}(x),t)\). It fixes the bottom and side faces. Formula (9) is continuous, equals F at s = 0, and restricts to h(z,s) on the top face. Thus e has the homotopy-lifting property. Since G is path-connected, every element is the endpoint of a path from the identity and e is surjective.

The product Δ × I is a compact contractible topological 5-manifold; corners cause no problem in the topological category. [KK26, Theorem 6.18] together with [GRW24, Theorem A] makes H **weakly contractible**. The long exact sequence for e then gives

\[
\pi_kP(\Delta)\cong\pi_kG\quad(k\ge1),
\qquad \pi_0P(\Delta)\cong\pi_0G.
\tag{10}
\]

The 2026 pseudo-isotopy theorem says P(Δ) is path-connected. Equation (10) shows exactly why this does not settle the higher groups of G: they are the corresponding higher groups of P(Δ).

### 5.2 Why the tempting five-dimensional contraction loses the needed information

A loop \(\alpha:I\to G\), \(\alpha(0)=\alpha(1)=\mathrm{id}\), gives a level-preserving homeomorphism
\(T_\alpha(x,t)=(\alpha(t)(x),t)\) in H. The five-dimensional result removes homotopy obstructions in H. It does not keep the deformation level-preserving. At an intermediate stage a homeomorphism of Δ × I may send a horizontal slice across many levels; projection back to Δ need not be a homeomorphism.

The level-preserving subspace of P(Δ) is the based path space of G and is contractible via \(\gamma(t)\mapsto\gamma(st)\). Proving that its inclusion into P(Δ) is a weak equivalence would settle weak contractibility, but that is an additional fully parametric assertion, not the pointwise pseudo-isotopy theorem.

Also, the simpler assignment \(f\mapsto f\times\mathrm{id}_I\) does **not** land in H unless f is the identity: it moves the two end faces, which are part of the boundary of Δ × I.

**Attempt outcome:** stabilization produces the exact weak equivalence (10), not vanishing of its two sides. The missing result is a higher-parameter straightening/trivialization theorem.

## 6. Attempt 5: use boundary extensions, bundles, and potential cork obstructions

Let \(K=\operatorname{Homeo}_0(\Sigma)\), the identity path component, and let E be the inverse image of K under restriction \(\operatorname{Homeo}(\Delta)\to\operatorname{Homeo}(\Sigma)\). A collar gives a fibration

\[
G\longrightarrow E\xrightarrow{r}K.
\tag{11}
\]

For completeness, the homotopy lifting can be made explicit. Given \(h(z,s)\in K\), set \(\delta(z,s)=h(z,s)h(z,0)^{-1}\). In a collar \(\Sigma\times[0,\epsilon]\), choose a continuous function β with β(0) = 1 and β = 0 near ε. Define
\((y,u)\mapsto(\delta(z,s\beta(u))(y),u)\), and extend by the identity beyond the collar. Composing an initial lift with this homeomorphism lifts h. Surjectivity follows by lifting a path from the identity to any element of K.

Path-connectedness of G only kills the bottom connecting map
\(\pi_1K\to\pi_0G\). The remaining long exact sequence reads, for example,

\[
\pi_2E\longrightarrow\pi_2K\longrightarrow\pi_1G
\longrightarrow\pi_1E\longrightarrow\pi_1K\longrightarrow0.
\tag{12}
\]

Knowing the boundary groups alone does not determine \(\pi_1G\), because the interior restriction maps in (12) are unknown. In all degrees, weak contractibility of G would make r a weak equivalence; no such assertion is supplied by extending individual boundary maps.

There is a concrete bundle formulation of the obstruction. For any based \(\alpha:S^k\to G\), glue two trivial Δ-bundles over the hemispheres of \(S^{k+1}\) using α on the equator. The resulting bundle \(V_\alpha\to S^{k+1}\) comes with the fixed boundary trivialization
\(\partial V_\alpha=\Sigma\times S^{k+1}\).
Then

\[
V_\alpha\text{ is trivial as a bundle relative to that boundary trivialization}
\quad\Longleftrightarrow\quad[\alpha]=0\in\pi_kG.
\tag{13}
\]

To prove this, a nullhomotopy extends α over one hemisphere, and changing its trivialization by that extension makes the transition map the identity. Conversely, a relative bundle trivialization determines maps from each hemisphere to G. Their boundary restrictions differ by α. Each restriction is nullhomotopic, so their product/inverse is nullhomotopic. A free nullhomotopy can be based by the normalization used in §2.2. This proves (13).

Although every fiber of \(V_\alpha\) is the same contractible manifold, it does not follow that the bundle is relatively trivial. Uniqueness of an individual filling is a statement about objects, while (13) asks for a continuous family of identifications. This is the same coherence issue exposed by the other four attempts.

Two proposed counterexample sources fail at an even earlier stage:

- A nontrivial cork **boundary** diffeomorphism is not an element of G, since G fixes Σ pointwise.
- A boundary-fixing diffeomorphism which is smoothly non-isotopic to the identity still maps to the zero element of \(\pi_0G\), by §3.1. Its smooth nontriviality is not a topological obstruction. A family of such maps would require a separate invariant surviving passage to homeomorphisms.

**Attempt outcome:** (13) gives an exact, geometric description of a possible higher-homotopy counterexample, but no nontrivial boundary-trivialized Δ-bundle, and no invariant proving one nontrivial, has been constructed.

## 7. Final verdict and verification scope

The general question is **unresolved in this work**. The strongest established facts are the explicit Alexander contraction for fixed-disk-supported families, the known \(\pi_0G=0\) with corrected sources, and the mapping-space, embedding-space, pseudo-isotopy, and bundle reductions above.

The first missing level is already \(\pi_1G\): this work neither proves that every loop contracts nor constructs a nontrivial loop. More generally, the necessary family-extension statement is that every continuous \(S^k\to G\) extends over \(D^{k+1}\) for all k ≥ 1. Even a proof of all those extensions would establish weak contractibility; a solution to the literal full-space contraction question must also justify the passage to actual contractibility or construct a contraction directly. No unproved CW-type/ANR assertion about G is used here.

The accompanying exact-arithmetic program uses the cube Q = [−1,1]⁴ and the nontrivial family

\[
f_a(x)=\left(x_1+a\prod_{j=1}^4(1-|x_j|),x_2,x_3,x_4\right),\qquad |a|<1.
\tag{14}
\]

This is a homeomorphism for every such a, not merely at the sampled points. Fixing the last three coordinates and writing \(c=a\prod_{j=2}^4(1-|x_j|)\), its first coordinate is \(x_1+c(1-|x_1|)\). The two slopes are 1 + c and 1 − c, both positive; the endpoints −1 and 1 are fixed, and the breakpoint 0 maps to c. The inverse is \((y_1-c)/(1+c)\) for y₁ ≤ c and \((y_1-c)/(1-c)\) for y₁ ≥ c. The formulas agree at the breakpoint and depend continuously on the tail coordinates. Every boundary face is fixed because one factor in the product vanishes.

Using the sup norm, formula (2) applies verbatim to Q. For this family the displacement is at most |a|t. For arbitrary boundary-fixing cube homeomorphisms it is at most 2t. The identity \(A_s(A_t(f))=A_{st}(f)\) follows by using double dilation on stQ, and observing that both sides are the identity outside stQ, including the limiting cases s = 0 or t = 0.

The program checks these inverses, boundary conditions, support bounds, and the composition identity on a fixed rational grid. It also checks the numerical dimension inequalities in the cited convergence argument. These are reproducible consistency checks, not a computation of homotopy groups or a formal verification of the topological theorems.

## References

- **[K3]** R. İ. Baykur, R. C. Kirby, D. Ruberman, *K3: A New Problem List in Low-Dimensional Topology* (2026), Problem 4.48, pp. 228–229. [Author-hosted preliminary book](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf).
- **[GRW24]** S. Galatius, O. Randal-Williams, *The Alexander trick for homology spheres*, IMRN 2024(24), 14689–14703. [DOI](https://doi.org/10.1093/imrn/rnae255). [Author-accepted manuscript](https://api.repository.cam.ac.uk/server/api/core/bitstreams/f3e65116-e119-4947-b4fe-ae433c519841/content).
- **[KK26]** M. Krannich, A. Kupers, *Infinity-operadic foundations for embedding calculus*, Journal of Topology (2026). [DOI](https://doi.org/10.1112/topo.70071). [Institutional full text](https://publikationen.bibliothek.kit.edu/1000192734/180055557), especially §§5.4.2, 6.1–6.3, Theorem 6.18.
- **[OP25]** P. Orson, M. Powell, *Mapping class groups of simply connected 4-manifolds with boundary*, JDG 131(1) (2025), 199–275. [DOI](https://doi.org/10.4310/jdg/1755544135). [Author preprint, v3, 14 August 2024](https://arxiv.org/pdf/2207.05986v3), Theorem A, Theorem 3.1, Proposition 6.2 and §6.2.
- **[GGHKP26]** D. Gabai, D. Gay, D. Hartman, V. Krushkal, M. Powell, *Pseudo-isotopies of simply connected 4-manifolds*, Forum of Mathematics, Pi 14 (2026), e9. [DOI](https://doi.org/10.1017/fmp.2026.10026). [Full text](https://www.cambridge.org/core/journals/forum-of-mathematics-pi/article/pseudoisotopies-of-simply-connected-4manifolds/76BC09B6D1CF91456A4189800D2B0494), Theorem 1.5 and §§5–6.
- **[FNOP25]** S. Friedl, M. Nagel, P. Orson, M. Powell, *The foundations of 4-manifold theory in the topological category*, New York J. Math. Monographs 6 (2025). [Full text](https://nyjm.albany.edu/m/2025/6p.pdf), Lemma 4.4.
- **[EK71]** R. D. Edwards, R. C. Kirby, *Deformations of spaces of imbeddings*, Ann. of Math. 93 (1971), 63–88. [DOI](https://doi.org/10.2307/1970753).
