# Homeomorphism groups and the ANR problem

Problem 3011 / KP-5.4. Research date: 2026-10-08.

## Verdict and scope

**Partial analysis; the compact-manifold problem is unresolved here.** Five mathematical routes were investigated. The results below are proved reductions, elementary constructions, and explicit failures of proposed shortcuts. They are not a proof or refutation of the compact-manifold ANR conjecture, and no novelty is claimed for them.

The current K3 question asks whether the homeomorphism group of a manifold is an absolute neighborhood retract. Its remarks identify the earlier question as Kirby 1997, Problem 5.27; record the two-dimensional results; and state that dimensions greater than two are unknown. The actual April 2026 preliminary K3 PDF, printed p. 304, was retrieved and checked [K3]. It does not specify compactness, group topology, or a relative boundary condition in the short statement.

That omission matters mathematically. The intended classical **compact** problem must be distinguished from an unrestricted noncompact reading. Edwards–Kirby explicitly give a noncompact counterexample on printed p. 77 [EK]. A fully written escaping-twist argument is included in §7; it is an explanation of a known scope obstruction, not a new solution of KP-5.4. Yagasaki's positive theorem for noncompact surfaces concerns the **identity component**, not an assertion that the full group is an ANR [Y].

For the central analysis, a manifold is a second-countable Hausdorff topological manifold of finite dimension. We use the compact-open topology on the **full** homeomorphism group. For compact M this is the uniform topology for any compatible metric. We concentrate on compact manifolds and, when using interior-ball fragmentation, on closed manifolds. A boundary-fixed group is denoted explicitly. Neither the discrete group topology, a smooth topology on Diff(M), the Whitney topology on a noncompact group, nor the identity component of a noncompact group is silently substituted.

The normalized local test object is

\[
G_n=\operatorname{Homeo}(D^n\,\mathrm{rel}\,\partial D^n).
\]

Ferry's geometric-topology notes, Question 13.10, printed p. 90, explicitly state the compact-manifold ANR problem and its reduction to this relative disk group [F-notes]. This is an older exposition, not a current-status source. Our independent conditional fragmentation proof below spells out what such a reduction uses, rather than treating a deformation or an isotopy factorization as an ANR theorem. For manifolds with boundary, half-ball factors or a separate boundary-extension argument must also be supplied.

## 1. Definitions, topology, and what would finish the problem

We use ANR for metrizable spaces: every closed embedding into a metric space has a retraction from some open neighborhood. Equivalently, every continuous map from a closed subset A of a metrizable parameter space Z into the target extends to a neighborhood of A. The latter is the absolute neighborhood extensor (ANE) formulation. AR/AE means extension over all of Z. These standard equivalences and the equivalence `contractible ANR = AR` are used as retract-theory facts; see [Y, §2] and its reference to Hu.

For compact metric M, put

\[
 d_\infty(f,g)=\sup_{x\in M}d(f(x),g(x)),\qquad
 D(f,g)=\max\{d_\infty(f,g),d_\infty(f^{-1},g^{-1})\}.
\]

These give the same topology on Homeo(M). Indeed, if f_i converges uniformly to the homeomorphism f and y=f_i(x), then
`d(f^{-1}(y),x) = d(f^{-1}(f_i(x)), f^{-1}(f(x)))`,
which tends to zero uniformly by uniform continuity of f^{-1}. The metric D is complete when d is complete: uniformly Cauchy forward and inverse maps converge to maps f,g, and uniform continuity in compositions gives fg=gf=id. The forward-only metric need not be complete. It is important not to invoke completeness of that metric in a limiting construction.

Local contractibility is necessary for ANR. It is not sufficient for general metrizable spaces, even metrizable groups: Cauty's non-AR metric linear space is contractible and locally contractible, hence cannot be an ANR [C94; C05]. The ANR assertion therefore needs more than contracting every sufficiently small family of homeomorphisms. The missing statement in this report is extension for **arbitrary metrizable parameter spaces**, or an equivalent genuine neighborhood-retraction construction.

For compact positive-dimensional manifolds the familiar Hilbert-manifold recognition theorem applies only **after** ANR has been established. It cannot be used to manufacture the ANR hypothesis. Ferry's Hilbert-cube-manifold theorem has an infinite-dimensional manifold as its input, a different class from finite-dimensional M [F77].

## 2. Route A: construct an ambient retraction by interpolation

### 2.1 A correct closed ambient model

For the disk, embed G_n into `C(D^n,D^n)^2` by

\[
 h\longmapsto(h,h^{-1}).
\]

The image is closed: a limit (f,g) satisfies fg=gf=id by uniform convergence and uniform continuity. Boundary-fixing is closed as well. In contrast, G_n need not be closed in the forward-map space alone. The ambient pair space with boundary values fixed is a convex metrizable subset of a locally convex function space, hence an AR by the usual convex extension theorem. A neighborhood retraction onto the pair graph would prove G_n is ANR. This is a precise target for a retraction construction, not such a construction.

### 2.2 The one-dimensional interpolation works

Let G_1 be increasing homeomorphisms of [-1,1] fixing its endpoints. A finite convex combination of elements of G_1 remains continuous, endpoint-fixing and strictly increasing, and thus remains in G_1. This gives a direct extension proof, with no completeness assumption on the forward metric.

Let A be a nonempty closed subset of a metric space Z and f:A→G_1 be continuous. Take a locally finite Whitney-type cover (U_i) of Z\A, a subordinate partition of unity (λ_i), and points a_i∈A chosen so that if z∈U_i then d_Z(z,a_i)≤C d_Z(z,A), for a uniform constant C. Such a cover is obtained by refining balls of radius d_Z(z,A)/4 and choosing an approximate nearest point in A. Define

\[
 F(z)=\sum_i\lambda_i(z) f(a_i)\quad(z\notin A),\qquad F(a)=f(a).
\]

The sum is locally finite and convex, so it lies in G_1. As z→a∈A, every a_i with λ_i(z)>0 tends to a. Hence

\[
 \|F(z)-f(a)\|_\infty\le
 \max_{\lambda_i(z)>0}\|f(a_i)-f(a)\|_\infty\longrightarrow0.
\]

Thus F is continuous. If A is empty use the constant identity map. This proves the AE, hence AR, property of G_1. This is an elementary recovery of a known low-dimensional fact, included to test the mechanism.

### 2.3 Arbitrarily small rotations destroy that mechanism in every n≥2

Take a ball of radius r in the interior of D^n, centered at the origin in local coordinates. Let R_θ rotate the first two coordinates and fix the remaining coordinates. Choose a continuous function θ(s) equal to π for s≤r/3 and zero for s≥2r/3. Define

\[
 h(x)=R_{\theta(\|x\|)}x
\]

on the ball and use the identity outside. Rotation preserves the radius, so its inverse is `x↦R_{-θ(∥x∥)}x`. Thus h∈G_n, and both h and h^{-1} have displacement at most 2r. For x=(s,0,…,0) with |s|<r/3,

\[
 \frac{x+h(x)}2=0.
\]

The affine midpoint of id and h collapses an entire interval. By making r arbitrarily small, this occurs in every uniform identity neighborhood. Therefore no proof can obtain a convex neighborhood in the ambient forward-map space by simply choosing the neighborhood smaller. The same midpoint operation on map–inverse pairs fails to stay in the pair graph.

**Exact remaining gap:** a nonlinear, continuously chosen correction that produces inverse pairs on an ambient neighborhood and fixes every genuine homeomorphism. The counterexample rules out affine averaging, not nonlinear retractions or the ANR property.

## 3. Route B: Alexander shrinking and parametrized extensions

For the Euclidean unit disk define, for 0<t≤1,

\[
 A_t(h)(x)=\begin{cases}t h(x/t),&\|x\|\le t,\\x,&\|x\|\ge t,\end{cases}
 \qquad A_0(h)=\mathrm{id}.
\]

The definitions agree on the gluing sphere because h fixes ∂D^n. Each A_t(h) is a boundary-fixed homeomorphism; its inverse is A_t(h^{-1}). Moreover

\[
 \|A_t(h)-A_t(g)\|_\infty=t\|h-g\|_\infty,
 \qquad \|A_t(h)-\mathrm{id}\|_\infty=t\|h-\mathrm{id}\|_\infty.
\]

At t=0 the displacement is at most 2t, uniformly in h. At a positive t, continuity follows from the gluing formula and uniform continuity of h. Thus this is a continuous contraction of G_n to the identity. Every forward-metric ball about the identity is contracted **inside itself**. Right translation transports these contractions to a neighborhood basis at every group element.

These conclusions are stronger than merely vanishing homotopy groups, but they still do not prove ANR. In particular, `G_n is ANR` is equivalent to `G_n is AR` because G_n is already contractible.

A fully detailed independent extension analysis is in `PARAMETRIC_EXTENSION.md`. Its finite-simplex construction has face compatibility, an explicit cardinality-dependent control estimate, an extension theorem for bounded-multiplicity parameter covers, and an explicit radial-twist counterexample to dimension-independent control of that particular interpolation. It states a sufficient replacement property for a different family of operations. Finite-dimensional disks or a fixed finite simplicial parameter complex do not test that missing quantifier.

**Exact remaining gap:** a uniformly small, face-compatible interpolation or another extension construction with control independent of the number of active partition-of-unity coordinates. For the specific canonical Alexander interpolation, the accompanying note proves that dimension-independent control is false: vertices whose forward-and-inverse distances to the identity are at most π/(2N) have an interpolated point at distance at least 1/2. Worst-case amplification lies between m/π and 2m+1 for an m-simplex. A different interpolation or extension scheme remains possible; this is not a non-ANR theorem.

## 4. Route C: fragmentation and a local section of multiplication

This route tries to use finitely many local homeomorphism groups as ANR building blocks.

**Conditional lemma.** Let G be a separable metrizable topological group, let H_1,…,H_r be metrizable ANE spaces that are subgroups of G with their subspace topologies, and let U be an open identity neighborhood. Suppose continuous maps σ_i:U→H_i satisfy

\[
 g=\sigma_1(g)\cdots\sigma_r(g)\quad(g\in U).
\]

Then U is an ANE. Consequently G is locally ANR, hence ANR by the local-to-global theorem for metric ANRs.

**Proof.** Given f:A→U from a closed subset of a metrizable Z, extend each σ_i f to a map F_i:V_i→H_i on an open neighborhood V_i of A. On V=∩V_i define F=F_1⋯F_r. It is continuous and equals f on A. The open subset F^{-1}(U) of V contains A, and F restricted there is the required extension into U. Every translate of U is an ANE. Apply the standard local-to-global ANR theorem. ∎

This proof does not assume that a continuous image of an ANR is ANR, which would be false. The continuous local section and the finite intersection of extension neighborhoods are the relevant mechanisms.

For a closed n-manifold, suitable finite-chart fragmentation has factors supported in embedded closed balls. A homeomorphism supported in such a ball and fixed on its boundary is identified, by coordinates and extension by the identity, with G_n. Edwards–Kirby supplies canonical local deformations; the standard disk reduction recorded by Ferry packages the fragmentation argument. Our lemma explains why **ANE of the factor groups**, rather than their mere contractibility, is needed.

An isotopy factorization for an individual isotopy is weaker than the continuous local section in this lemma. One must not replace one by the other without justification. The proof above is conditional and does not independently reconstruct every localization step of Edwards–Kirby. In the boundary case one must also control half-balls or first extend the boundary motion; the interior-ball statement alone does not cover that case.

**Exact remaining gap:** establish the ANR/ANE property of the relative disk factors in n>2 (plus the specified boundary localization when relevant). This route reduces the difficulty; it does not remove it. Repeating the fragmentation argument with contractible factors is circular.

## 5. Route D: stabilize by the Hilbert cube and descend

Set Q=[0,1]^N and use the cube model I^n for the disk. The compact space I^n×Q is homeomorphic to Q by reindexing coordinates. Thus its full homeomorphism group is an ANR by the Hilbert-cube result [F77]. There is a natural closed embedding

\[
 j:G_n\hookrightarrow\operatorname{Homeo}(I^n\times Q),\qquad j(h)=h\times\mathrm{id}_Q.
\]

It is closed because a limit and its inverse preserve the Q-coordinate, are independent of that coordinate in the I^n-coordinate, and fix the relevant base boundary. If there were a neighborhood retraction onto j(G_n), ANR would descend to G_n.

The obvious proposed retraction fixes q_0=(1/2,1/2,…) and sets

\[
 R(F)(x)=\pi_{I^n}(F(x,q_0)).
\]

**This formula fails on every identity neighborhood.** In the first n+1 coordinates, take a small Euclidean ball around (1/2,…,1/2), of radius r<1/4. Rotate the x_1-coordinate against the first Q-coordinate by angle π/2 in the inner ball, tapering the angle continuously to zero before the boundary, and leave all remaining coordinates fixed. As in §2, preservation of distance to the center gives a homeomorphism with inverse obtained by reversing the angle. Extend it by the identity, including all Q-tail coordinates.

For x=(1/2+s,1/2,…,1/2), with |s| sufficiently small and q=q_0, the inner rotation sends the x_1 displacement to the Q-coordinate. All first n output coordinates are (1/2,…,1/2). Thus R(F) collapses a nontrivial interval. Both F and F^{-1} converge uniformly to the identity as r→0 in any compatible product metric, so merely restricting to a smaller neighborhood does not fix the problem.

**Exact remaining gap:** a continuous normalization that separates the base and Hilbert-cube coordinates and is the identity on all product homeomorphisms. No such neighborhood retraction was constructed. Being a closed subgroup of an ANR topological group does not supply one automatically. This stabilization argument fails even in dimensions where G_n is already known to be an AR, so the failure is a method obstruction, not evidence against the conjecture.

## 6. Route E: finite-dimensional exhaustion and ANR recognition

Another possible route is to combine local contractibility with a countable union of finite-dimensional compacta, as in Haver's sufficient criterion [H]. That hypothesis is impossible for any identity neighborhood of the disk group. Here is a direct proof.

### 6.1 A Hilbert cube in every identity neighborhood

First construct an interval's worth of boundary-fixed homeomorphisms of C=[-1,1]^n. Write x=(x_1,x') and put

\[
 b(x')=\prod_{i=2}^n(1-x_i^2),\qquad
 \psi_t(x)=\bigl(x_1+\tfrac t4 b(x')(1-x_1^2),x'\bigr),\quad0\le t\le1,
\]

where the empty product for n=1 is one. In each x_1-fiber the derivative is at least 1/2, and its endpoints are fixed. Other boundary faces have b=0. Thus ψ_t is a homeomorphism of the cube fixed on its boundary. It is injectively parametrized since ψ_t(0) has first coordinate t/4; ψ_0=id.

In an arbitrarily small interior chart of D^n choose pairwise disjoint closed cubes C_j, with diameters tending to zero, accumulating only at a point outside their interiors. Rescale ψ_{t_j} into C_j and use the identity outside their union. The resulting piecewise map Ψ(t_1,t_2,…) is a homeomorphism: each cube is preserved; the formulas agree on boundaries; and both the map and its inverse are continuous at the accumulation point because the cubes' diameters tend to zero.

The map Ψ:Q→G_n is continuous in the uniform topology. A finite initial set of cubes gives ordinary finite-parameter continuity, and the remaining tail moves points by at most the largest tail diameter. It is injective by evaluating the centers. Since Q is compact and G_n Hausdorff, Ψ is a topological embedding. Making all cubes small enough places its image in any prescribed identity neighborhood. The same construction works in an interior chart of any positive-dimensional compact manifold.

### 6.2 Why a finite-dimensional compact exhaustion cannot exist

Suppose such a neighborhood U were covered by compact finite-dimensional subsets K_1,K_2,…. Intersect them with an embedded Q⊂U. Each Q∩K_i is closed and finite-dimensional. It has empty interior in Q: any nonempty open subset of Q contains cubes [0,1]^m for every m, whereas covering dimension of a closed subspace cannot exceed that of a finite-dimensional metric space. Thus Q would be a countable union of closed nowhere dense subsets, contradicting the Baire theorem.

This proves more than the failure of a proposed particular exhaustion: **no** such exhaustion exists. The conclusion also applies to the dimension-one and dimension-two groups already known to be ARs. Therefore it is strictly an obstruction to this sufficient criterion. Finite-dimensional parameter extension, a CW-type model for the whole group, or local contractibility cannot be promoted to ANR by pretending the homeomorphism group has the dimension of the underlying manifold.

**Exact remaining gap:** an infinite-dimensional ANR criterion with its additional hypotheses actually proved for G_n. The failed exhaustion cannot be repaired by choosing more finite-dimensional compact pieces.

## 7. Known noncompact scope obstruction, with proof

There is a connected orientable boundaryless surface S obtained by starting with a cylinder and inserting a locally finite sequence of one-holed tori along disks tending to an end. Choose handles T_j escaping every compact subset of S, and curves a_j,b_j in T_j with oriented intersection one. Let τ_j be a Dehn twist about a_j, supported in a small annulus in T_j.

For each compact K⊂S, τ_j and τ_j^{-1} restrict to the identity on K for all sufficiently large j. Hence τ_j→id in the compact-open topology. On homology, with the sign fixed by orienting the twist,

\[
 (\tau_j)_*[b_j]=[b_j]+[a_j],\qquad (\tau_j)_*[a_j]=[a_j].
\]

The class [a_j] is nonzero: its algebraic intersection with the compact curve b_j is one. The twist formula follows by cutting b_j at its single crossing of the twist annulus; after the twist the crossing arc winds once around its core. All remaining parts of b_j are unchanged. Thus τ_j is not homotopic to the identity.

A continuous path in Homeo(S) with compact-open topology gives a continuous homotopy S×I→S because S is locally compact. Homotopic maps induce the same map on H_1. Consequently no τ_j belongs to the identity path component. If Homeo(S) were locally path connected at id, some open path-connected identity neighborhood would exist and would contain τ_j for large j, a contradiction. Therefore Homeo(S) is not locally path connected and is not an ANR.

For any n≥3 the same argument applies to the connected n-manifold S×S^{n-2}: use τ_j×id. The supports escape compact sets by projection to S. Nontriviality on H_1 is preserved because the inclusion S→S×S^{n-2} at a fixed point admits the projection back to S as a left inverse. Thus the unrestricted noncompact reading has counterexamples in every n≥2.

This argument is consistent with [Y]: an identity component may itself be a Hilbert manifold without being open in the full group. It is also consistent with [EK, Corollary 6.1], which covers manifolds homeomorphic to interiors of compact manifolds, a smaller class than all noncompact manifolds. Edwards–Kirby's own p. 77 counterexample already uses a locally finite collection of torus pieces escaping to infinity. No new counterexample claim is made.

## 8. Attempt ledger and stopping point

The five counted mathematical approaches are:

1. Ambient inverse-pair retraction and convex interpolation: proves the one-dimensional extension lemma; disproves the higher-dimensional affine shortcut.
2. Alexander/parametric extension: gives controlled contractions and finite-dimensional parameter extension; arbitrary parameter multiplicity remains uncontrolled.
3. Fragmentation: proves a local-section-to-ANE lemma; leaves the disk-factor ANE hypothesis unproved.
4. Hilbert-cube stabilization: proves a closed embedding and refutes raw projection as a neighborhood retraction; continuous desuspension remains unconstructed.
5. Finite-dimensional-exhaustion recognition: embeds Q in every identity neighborhood and rules out the needed exhaustion by a Baire argument.

Source recovery, literature searches, computational checks, and audits count as zero mathematical approaches. The additional noncompact example in §7 is a scope check and is not counted among the five compact-target routes.

No construction here meets the arbitrary-metric-parameter extension condition for G_n when n>2, and no compact-manifold counterexample is produced. The current primary problem list still states the higher-dimensional problem as open. The literature search found no verified later general resolution, but that is a bounded negative search result, not proof that no unpublished or unindexed result exists.

**Remaining target:** prove or disprove the ANR property for the compact-manifold homeomorphism group in dimensions greater than two, with the stated topology. In the disk reduction, the exact unresolved assertion is that G_n is an AE/AR. Boundary, noncompact, and identity-component statements must retain their own hypotheses.

## References and inspection limits

[K3] R. İ. Baykur, R. C. Kirby, D. Ruberman, *K3 – A New Problem List in Low-Dimensional Topology*, author's preliminary AMS version, April 2026, Problem 5.4, printed p. 304. https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf . Problem and remarks inspected; no source text is included in this packet.

[EK] R. D. Edwards, R. C. Kirby, *Deformations of spaces of imbeddings*, Ann. of Math. 93 (1971), 63–88. https://doi.org/10.2307/1970753 . Public author-hosted version: https://www.maths.gla.ac.uk/~mpowell/Edwards%20Kirby.pdf . Printed pp. 63–65, 75–78 and relevant relative-case statements inspected. In particular Corollary 1.1 has a compactness hypothesis; p. 77 explains its noncompact limitation. A second public scan omits p. 63 from its early page order and was not used alone to verify that corollary.

[M71] W. K. Mason, *The space of all self-homeomorphisms of a two-cell which fix the cell's boundary is an absolute retract*, Trans. Amer. Math. Soc. 161 (1971), 185–205. https://doi.org/10.2307/1995936 . The theorem is recorded in [K3], [D], and [Y]; the original full proof was not inspected in this pass.

[LM72] R. Luke, W. K. Mason, *The space of homeomorphisms on a compact two-manifold is an absolute neighborhood retract*, Trans. Amer. Math. Soc. 164 (1972), 275–285. https://doi.org/10.2307/1995974 . Correct AMS identifier: https://doi.org/10.1090/S0002-9947-1972-0301693-7 . The original AMS PDF request returned HTTP 403, so the full proof is not claimed inspected. The theorem and compactness hypothesis are independently recorded by [K3] and [Y, Fact 2.1].

[F-notes] S. Ferry, *Geometric topology notes*, Chapter 13, Question 13.10, printed p. 90. https://webhomes.maths.ed.ac.uk/~v1ranick/papers/ferrygt.pdf . Compact formulation and disk reduction inspected. An undated older exposition; web retrieval dates are not publication dates.

[D] J. J. Dijkstra, *On Homeomorphism Groups and the Compact-Open Topology*, Amer. Math. Monthly 112 (2005), 910–912. https://www.cs.vu.nl/~dijkstra/research/papers/2005compactopen.pdf . Full three-page text inspected; particularly p. 912 on relative cube groups and the ANR/AR gap.

[Y] T. Yagasaki, *Homotopy types of homeomorphism groups of noncompact 2-manifolds*, arXiv:math/0010223, version 1 (2000). https://arxiv.org/abs/math/0010223 . Theorem 1.1, Corollary 1.1, §2 and the ANR argument in §4 inspected. The cited theorem concerns identity components.

[F77] S. Ferry, *The homeomorphism group of a compact Hilbert cube manifold is an ANR*, Ann. of Math. 106 (1977), 101–119. https://annals.math.princeton.edu/1977/106-1/p07 ; https://doi.org/10.2307/1971161 . Publisher's theorem-bearing abstract inspected; its entire proof is not reconstructed here.

[C94] R. Cauty, *Un espace métrique linéaire qui n'est pas un rétracte absolu*, Fund. Math. 146 (1994), 85–99. https://doi.org/10.4064/fm-146-1-85-99 ; https://eudml.org/doc/212053 . Bibliographic abstract checked; supporting context read in [C05]. This is an external counterexample dependency, not a construction supplied by the present report.

[C05] R. Cauty, *Rétractes absolus de voisinage algébriques*, Serdica Math. J. 31 (2005), 309–354. https://www.math.bas.bg/serdica/2005/2005-309-354.pdf . Abstract and introductory comparison between topological ANRs, algebraic ANRs, and locally equiconnected spaces inspected. Algebraic ANR is not substituted for ANR.

[H] W. E. Haver, *Locally contractible spaces that are absolute neighborhood retracts*, Proc. Amer. Math. Soc. 40 (1973), 280–284. https://doi.org/10.1090/S0002-9939-1973-0331311-X . Used only to motivate the explicitly disproved exhaustion hypothesis, not to prove an ANR conclusion. Original full text was not obtained in this pass; [C94] cites the paper. No positive conclusion depends on invoking its theorem. The Baire obstruction in §6 is proved directly and does not depend on Haver's theorem.
