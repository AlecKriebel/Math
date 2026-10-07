# Independent scoped review: positive Bernoulli cost

Reviewer: fresh package-review-02 positive-cost subagent. Written 2026-10-07 UTC.

## Verdict and exact scope

**Clean scoped verdict: no substantive mathematical failure found.** I independently reconstructed the entire positive-cost chain from the pinned upstream source, before consulting any archived review. The reconstructed chain proves

\[
\operatorname{Cost}(\mathcal R_{\Gamma\curvearrowright X})\geq 1+\alpha/100
\]

for the displayed rank-100 amalgam and free Bernoulli action, when

\[
0<\alpha<1/200,\qquad
K\alpha^3<1/2,\qquad K=e^{96}96^{99}/95^{95}.
\]

The frozen candidate's choice \(\alpha=2^{-61}\) therefore gives the stated gap \(1/(100\cdot2^{61})\). No extra unproved algebraic assumption was inserted into this reconstruction: notably, the coefficient group is the actual subgroup of the presented group, and its embedding follows from the relative-presentation isomorphism.

This is a manual mathematical source audit by an AI agent, not a formal proof certificate or human refereeing. I did not review the candidate's direct cellular Betti computation, the full priority audit, or publication metadata as part of this assigned scope. I did read the candidate's complete main.tex to establish the actual positive-cost claim and its attribution. No archived reviewers' conclusions were read. A nested independent review was attempted but the concurrency limit prevented it; the parent is itself independently reviewing the planar/rank route.

## Sources and identity

Upstream checkout: `/Users/alec/Desktop/math`, read-only. Its HEAD was checked as
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`, with no working-tree changes shown. Source directory:
`preprints/A-group-without-fixed-price-October-5-2026/build`.

Frozen candidate: `/Users/alec/Documents/Math/openai_followon_cost_betti/verification/frozen-v2/publication/main.tex`.

SHA-256 hashes of the material actually read:

| Source | SHA-256 |
|---|---|
| compression.tex | e50593230e86100c675a8021a1ca3d4f0a1993882815595ba3baaa20c8b70572 |
| deployment.tex | cfcc17cbdc07eae6198351f9ef331c59411e081b6ac91b270f515ef68a800dce |
| finite-models.tex | 84ad9737399e3c4b1ddc0101e18922dcc8dd3cf5b8543cf7391e4993715c21f8 |
| planar.tex | 9c92939226f0264571b2e17bc352e8cec5746d1ae89b77ef86cdee821774c06f |
| rank-surgery.tex | 03f5dedd2fd062a69f6965fa558c5382016c0dad6a308dc834a5d59e537eaf7d |
| conclusion.tex | 9290635fcd579e99e1db4331caf318abcbb210410afa3f6035dd29c3ea3b5fa5 |
| group-actions.tex | 7d24f27417d52e5944c8d28bc80cb1b60d3c8fbe1696c58de4c678c605e672b3 |
| introduction.tex | 6cbfa027e1ddc3efc5dd435347c76c0003f67551749931cf21763e3282cfa1bc |
| paper.tex | d978244ac944e7a58b15fc228ff10fab0d9ac23713b1165ee8d3b7471176c8dd |
| frozen-v2/publication/main.tex | 7475979d063f5ad6e9e85f09fca5eca6f1beb83a83f654bc9011854dc8c4182a |

I also read the upstream README, manuscript-specific README and INPUTS.md, the original REQUEST.txt and the applicable AGENTS.md. The INPUTS.md provenance caveat does not certify the argument; the verdict above rests on the proof reconstruction below.

## Exact objects and hypotheses

\(A=F(a,b_1,\ldots,b_{99})\), \(u_0=1\), \(u_i=u_{i-1}ab_i\), \(w=u_{99}a\), and \(J=\langle b_1,\ldots,b_{99},w\rangle\). The no-cancellation argument in group-actions.tex proves that these generators freely generate \(J\); thus \(J\) is infinite. The elementary normal-form construction proves that \(A\) and \(B=J\times\langle t\rangle\) embed in \(\Gamma=A*_J B\), have intersection \(J\), and alternating words outside \(J\) of length at least two lie in neither factor. These are precisely the normal-form facts used later.

The source's coordinate action \((xg)(h)=x(gh)\) is a right action and preserves product probability. For every \(g\ne1\), a fixed point forces \(x(g)=x(1)\), a null event for independent continuous coordinates. Countability supplies a Borel invariant conull free set \(X\). All deployment displacements are therefore unique, and all cylinder approximations may be made on the full product without changing costs.

The relative quantity is
\[
\delta_X=\inf\{C(\mathcal E):\mathcal E\subseteq\mathcal R_A,
\quad\mathcal R_J\vee\mathcal E=\mathcal R_A\}.
\]
It is finite because the full a-map, costing one, suffices together with \(\mathcal R_J\). The action is p.m.p. on a standard probability space; no ergodicity assumption is needed anywhere in the lower-bound chain.

## 1. Compression and deployment

The compression lemma has the correct saved-cost term on a finite measure space, without renormalization:
\[
C(\mathcal F)\le C(\mathcal E)-\kappa(\mathcal S)+\kappa(\mathcal T)+\varepsilon.
\]

The small complete-set construction is valid without a smoothness assumption on infinite classes: mark finitely many separating partition atoms, then add the unsaturated complement. Each class is hit pointwise. The expected added measure tends to zero by dominated convergence because the number of atoms hit by every infinite class tends to infinity. Finite classes use a Borel transversal and the p.m.p. finite-class counting identity.

For the compression itself, every finite \(\mathcal S\)-class outside the retained set chooses one labelled edge toward a smaller distance. The selected origins are a transversal of precisely those classes. The same labelled edge cannot be chosen in both directions because distance strictly decreases; this yields the exact deleted cost \(\kappa(\mathcal S;Z\setminus Y)\), even when several original indices describe the same geometric edge. The retraction is constant on removed classes and fixes the retained set. Its many-to-one character is dealt with by splitting both source and target according to the ambient partial isomorphisms. Each split is genuinely injective and measure preserving, and indexed-family cost remains the original residual cost even when pushed domains overlap. Thus the recovery of \(\mathcal Q|Y\), and then \(\mathcal Q=\mathcal T\vee\mathcal F\), is valid.

The deployment proof first turns a near-optimal graphing into a finite graphing of group restrictions. Missing edges of a finite group-generating set have measures tending to zero, so this finite approximation does not assume that optimal graphings are finite. Subdivision then introduces finitely many sheets with measure \(\lambda\), projection P injective and measure preserving on each sheet, and
\[
C(\mathcal E_A^0)+C(\mathcal E_B^0)=c+\lambda(Z)-1.
\]

At alternating stages, \(S_{n+1}=Q_i^n\cap\overline{\mathcal R}_J\). The processed factor relation remains unchanged, the other grows, and the joint relation remains the full pullback relation. Summing the compression inequalities telescopes \(\kappa(S_0)=\lambda(Z)\), yielding
\[
C(\mathcal E_A^n)+C(\mathcal E_B^n)\le c-1+\kappa(S_n)+\varepsilon.
\]

The exhaustion of the supplied relation does not require convergence of the graphings themselves. Both factor relations increase; their intersections with the J-relation have common union \(S_\infty\). A shortest alternating chain between J-related endpoints cannot have length at least two: any J-step can be absorbed into a neighbor, and the remaining displacement word is reduced outside J but has product in J. Amalgam normal form excludes it. Hence \(S_\infty=\overline{\mathcal R}_J\). Every such class contains an infinite free J-orbit in the base sheet, so \(\kappa(S_n)\to0\) by dominated convergence.

At each finite stage, projecting graphings using sheet pairs preserves their cost. Giving all J-steps for free recovers \(\mathcal R_A\) by the analogous shortest-chain normal-form argument. Therefore
\[
\delta_X\le C(\mathcal E_A^n)+C(\mathcal E_B^n)
\le c-1+\kappa(S_n)+\varepsilon.
\]
The order of limits (finite stage, then errors, then near-optimal cost) proves
\(\operatorname{Cost}(\mathcal R_\Gamma)\ge1+\delta_X\).

Falsification checks: repeated edge instances, multiple projection sheets, zero-measure exceptional sets, finite and infinite intermediate classes, and noninjectivity of the whole projection do not invalidate this argument.

## 2. Cocycle transfer and exact finite models

For an exact finite right A-set V, define \(\theta(v,a)=x_v\), \(\theta(v,b_i)=1\), and the source-correct inverse rule. Free reduction makes this a well-defined word cocycle:
\[
\theta(v,gh)=\theta(v,g)\theta(vg,h).
\]
Its w-value is exactly the displayed defining row of \(D_V\), so every J-value is one. Importantly, this is a cocycle on labelled group steps, not a purported cocycle on finite-model endpoint pairs. Equal endpoints for different labels do not force equal cocycle values.

The restriction of the Gamma Bernoulli action to A is the Bernoulli shift \(\Omega^A\), with \(\Omega=[0,1]^{A\backslash\Gamma}\), by the actual disjoint coset-coordinate rearrangement. Freeness is used to choose path types whose label is exactly a. Finitely many such types cover measure \(1-\epsilon\); finite-coordinate approximations of their paid domains preserve coverage to \(1-2\epsilon\) and total cost to \(C(\mathcal E)+\epsilon\). Inverse-domain tests use the shifted source \(hg_\ell^{-1}\), as required.

Independent base labels on V give \(\xi_{vq}=\xi_vq\) exactly. Every finite-coordinate cylinder has its original law at sources without coordinate collisions. The exceptional fraction is bounded by the fixed-point fractions of the finitely many nonidentity labels \(gh^{-1}\). No independence between different sources is required. For each labelling, paid cocycle values plus one \(x_v\) for every uncovered source generate \(D_V\). Taking expectations therefore proves
\[
\limsup_k \operatorname{rk}(D_{V_k})/|V_k|
\le C(\mathcal E)+3\epsilon,
\]
and then \(\delta_X\ge\limsup_k\operatorname{rk}(D_{V_k})/|V_k|\).

The random-model construction uses the actual free basis \(a,u_1,\ldots,u_{99}\), justified by inverse substitutions. For a set T of size s, the identity column forces T to lie in its candidate containing set C of size 96s. The union bound is
\[
\binom ns\binom n{95s}(96s/n)^{99s}
\le [K(s/n)^3]^s.
\]
The exponent is exactly \(99-1-95=3\); the exponential factor is \(e^{96}\). Splitting the sum at a fixed R and using \(K\alpha^3<1/2\) proves expansion with probability tending to one.

For a fixed reduced word of length L, exposure of random permutation entries has a fresh request until the first visited-vertex collision; immediate inverse requests are excluded by reduction. The resulting fixed-point expectation is at most \(L(L+1)/(2(n-L+1))\). A diagonal choice of increasingly large n simultaneously enforces expansion and the first k fixed-point bounds. It needs no uniform estimate for growing word length.

Repeated row columns give fixed points of \(u_i u_j^{-1}\). Two distinct shared columns between different rows give fixed points of \(u_i u_k^{-1}u_lu_j^{-1}\). The stated adjacent-index inequalities make these words nonidentity, including cases containing the identity symbol \(u_0\). Thus the finite union of these fixed-point sets contains all bad rows, giving \(b(V_k)=o(|V_k|)\) on the same sequence used by transfer.

Falsification checks: finite models may have stabilizers and need not be transitive; cylinder labels may overlap between sources; the diagonal sequence and o(n) exceptions are compatible; none invalidates the estimate.

## 3. Relative planar shortening

The key source statement is planar.tex, lines 31–53. Its hypotheses count exterior occurrences, not lengths of coefficient spellings. The argument correctly retains coefficient values in H.

The finite filling uses only finitely many true H-relations, but minimality is taken in the actual free product \(L=H*F(U)\). The temporary presentation complex need not embed in L, and the proof never assumes it does. Generic points in the U-circle interiors give finite disjoint cooriented arc/circle tracks; every exterior occurrence is paired by one arc endpoint.

Connectedness of the disk-and-arc graph follows from the embedding \(H\hookrightarrow D\): a regular-neighborhood boundary around a component separated from the outer disk avoids all track points, hence is an H-element. Capping its inner relator holes makes it trivial in D; injectivity makes it trivial in H. Replacing that disk side with an L-filling reduces the relator count. Closed tracks are retained and do not obstruct this argument.

At an inner disk all exterior signs agree, so there is no inner loop. If an arc joins two copies of the same relator, they have opposite orientation and use the same unique exterior occurrence. At its constant target point their based boundary words are literal inverse words, even with noncommuting coefficients. A disk neighborhood of the pair and joining arc therefore has boundary trivial in L and removes both disks, contradicting minimality. Other tracks crossing this neighborhood do not prevent changing its filling. Distinct relators have at most one joining arc. Thus there are no parallel edges between inner vertices.

Every complementary face of the connected sphere graph is a disk. Collapsing the U-circles sends each track to the basepoint and records each sector's coefficient value. Its face equation is genuinely in H. For an inner–outer bigon it is \(h_{\rm inner}h_{\rm outer}^{-1}=1\), so it gives equality, not conjugacy, of the coefficient gaps. An outer monogon would contradict cyclic H-reduction; inner monogons are already excluded. A bigon through an inner vertex must connect it twice to the outer vertex; the doubled-bridge alternative would require inner degree one.

The weights 1/3, 1/2, 1 for nonbigon inner corners have total at most \(\ell-2\) on every face of length \(\ell\), including repeated face walks and outer loops. Euler therefore gives total inner contribution at least two. A positive inner vertex either is the sole inner disk with all bigons, giving the full cyclic match, or has exactly one nonbigon gap containing at most three inner edges. This supplies a consecutive bigon string with at least \(m-3\) exterior occurrences and contribution at most one. Consequently the second case supplies two distinct positive inner vertices and two exterior-disjoint matching intervals.

Falsification checks: torsion in H, infinitely many defining H-relations, closed tracks, cut vertices, outer loops, repeated face walks, and relator copies of opposite orientation are all covered. The source does not replace coefficient equality by equality of formal spellings.

## 4. Saturation, seam, and surgery

Assume for contradiction \(\beta\le\alpha n/100\) for a minimal-edge connected labelled graph surjecting to D. Pruning degree-one vertices and allowing a basepoint on an otherwise degree-two circle justify the bound of \(3\beta\) arcs, including the point and circle cases.

Initial bad-row columns and every possible arc addition together contribute at most
\[
100b+30(3\beta)\le1.9\alpha n<2\alpha n.
\]
A nontrivial row addition contributes at most 90 columns because every such row is good and already has ten distinct S-columns. If \(s=\lfloor\alpha n\rfloor\ge1\) rows were added, their union would have at most \(2\alpha n+90s<96s\) columns, contradicting expansion. The strict inequality remains valid at s=1; indeed \(\alpha n<s+1\le2s\) gives the stronger bound \(<94s\). Thus
\[
|S|\le2\alpha n+90(s-1)\le92\alpha n<n.
\]
Every arc now has zero or more than 30 U-occurrences. Every mixed row has at least 91 distinct positive U-letters, and distinct mixed rows share at most one.

Let H be the actual subgroup generated by the S-letters. The relative presentation is valid by inverse maps on all original generators: the quotient with the true relations of H maps to D; conversely, D maps to it because omitted S-only rows are true H-relations and all other original rows remain. These are inverse maps. This supplies the exact embedding needed by the planar lemma without requiring finite presentability or an independent proof that H is free.

For j outside S, a shortest based loop P representing \(x_j\) traverses complete arcs and has zero or more than 30 exterior occurrences. Its label is linearly H-reduced. An inverse-letter pair across a trivial H-gap either deletes a closed trivial detour when it is the same graph edge, or permits sliding the second incidence along the S-path and folding two equally labelled outgoing edges. The slide preserves connectedness, counts and all loop values because that S-path has value one. Folding reduces edges and does not increase rank, contradicting minimality. Thus P cannot already equal \(x_j\) in \(H*F(U)\).

Cyclically reducing \(\operatorname{lab}(P)x_j^{-1}\) leaves an exterior letter: otherwise embedding H would imply the original word was already trivial in the free product. Linear reduction of P shows that the first cancellation must involve the appended letter. Subsequent cancellations remove only the two ends of P's exterior list. Therefore the surviving block retains every internal coefficient gap, with just one seam letter or seam gap potentially disruptive.

Two exterior-disjoint planar intervals cannot both contain that seam letter or cross that seam gap; one intact interval in P has at least \(91-3=88\) exterior occurrences. A full cyclic match leaves at least 90 after cutting the seam. Consequently Q in P matches an actual consecutive row segment, with distinct exterior indices, using at least 88 of the original 100 positions. Matching coefficient values gives equality in D to the inverse complementary row segment, a word z of length at most 12. If this word is empty, the stipulated two-letter identity word provides a nonempty inserted path.

At least one arc traversal in Q contains more than 30 exterior occurrences: otherwise complete traversals contribute zero and its two partial ends contribute at most 60. Choose I from the first through last exterior edge of that traversal. It has at least 31 edges, with distinct degree-two interior vertices and no interior basepoint. Its first and last edges are exterior. Distinct exterior indices of Q prevent Q's endpoints from lying inside I, any later entry through those boundary edges, or any second traversal of I. Hence Q1 and Q2 avoid its edges and interior vertices.

Attach z between Q's endpoints and delete I. The bypass \(Q_1^{-1}ZQ_2^{-1}\) avoids the deleted segment and has exactly its value in D. It reconnects I's endpoints and replaces every use of I in an old reduced based loop. Surjectivity therefore persists. If I or Z has coincident endpoints the interior-vertex counts are still \(\ell-1\) and \(k-1\); both edge and vertex counts change by \(k-\ell\), leaving graph rank unchanged. The number of edges drops by at least \(31-12=19\), the required contradiction.

Falsification checks: the trivial group/point graph, rank-one circle, floor boundary s=1, S-only loops, cyclic cancellations, inverse relators, long coefficient spellings, self-returning arcs, coincident surgery endpoints, and the empty complementary word do not break the argument.

## 5. Constants and conclusion

On the constructed sequence, eventually \(\alpha n_k\ge1\) and \(100b(V_k)\le\alpha n_k\), so the deterministic result gives \(\operatorname{rk}(D_{V_k})>\alpha n_k/100\). Hence
\[
\delta_X\ge\limsup_k\operatorname{rk}(D_{V_k})/n_k\ge\alpha/100,
\quad\operatorname{Cost}(\mathcal R_X)\ge1+\alpha/100.
\]
The strict finite-model inequalities only yield a nonstrict lower bound after a limit; both source and candidate use the correct nonstrict result.

The candidate's exact parameter certificate was independently recomputed with Python arbitrary-precision integers:

```
2 * 3^97 * 96^4 = 3242474995074537080717329593630696549869310581938323456
2^183           = 12259964326927110866866776217202473468949912977468817408
2^61            = 2305843009213693952
100 * 2^61      = 230584300921369395200
```

The first integer is strictly smaller than the second. Since
\(K=e^{96}96^4(1+1/95)^{95}<e^{97}96^4<3^{97}96^4\), this proves \(K2^{-183}<1/2\), and \(2^{61}>200\) proves the other admissibility condition. No floating-point rounding is used.

## Additional attempted contradiction: conjugate intersections

The parent suggested testing a fixed-price-one criterion requiring \(B\cap a^{-1}Ba\) infinite. I independently derived the intersection boundary without reading the parent's receipt. Normal form first reduces it to \(J\cap a^{-1}Ja\).

The already-folded labelled core graph for J consists of the 99 b_i-loops at vertex 0 and the w-cycle with vertices 0 through 198, whose positive edges are
\(2i\xrightarrow{a}2i+1\) (0 through 98),
\(2i-1\xrightarrow{b_i}2i\) (1 through 99), and
\(198\xrightarrow{a}0\).
It has 199 vertices and 298 edges. The intersection is represented by loops in its fibre product based at (0,1). Directly checking the common signed outgoing labels gives exactly the path

```
(1,3) -- (0,2) -- (0,1) -- (198,0) -- (197,0) -- (196,198).
```

The end vertices have no additional common labels; each interior pair has exactly the two displayed incidences. This six-vertex, five-edge component is a tree, so its reduced loop language is trivial. Therefore \(J\cap a^{-1}Ja=\{1\}\), and the proposed infinite-intersection hypothesis fails. This check does not assert a general malnormality theorem for J.

The standalone `verify_boundary_checks.py` independently reconstructs this folded graph and its fibre component and repeats the exact integer comparison. It uses only Python's standard library, writes nothing, and can be run with `python3 verify_boundary_checks.py` from this review directory. Its output is retained in `boundary_checks.json`.

## Exact remaining gap and promotion scope

No remaining mathematical gap was identified in the assigned positive-cost chain. The strongest verified statement of this review is the source's Bernoulli lower bound with the candidate's exact parameter. The reconstruction is independent of archived audits; the parent has separately reconstructed the critical planar/rank part. This clean verdict supplies scoped proof-audit evidence only. It does not by itself certify the other candidate arguments, priority, licensing, package fidelity, publication, or tracker operations.

No upstream mutation, Git mutation, deposit/tracker action, or communication with external individuals occurred. All writes were restricted to this assigned review directory.
