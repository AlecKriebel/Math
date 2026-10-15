# Independent adversarial audit of the supplied prior-theorem route

Audit verdict: the chain yields a proper cocompact cubulation of the exact group, without using the new explicit completion Q. No fatal hypothesis gap was found. The conclusion below is a deduction made in this audit from older general theorems. The inspected papers do not document this particular group as an application, so the chain alone does not establish that its positive answer was previously recorded or regarded as routine.

The criteria were sealed before primary-source review. No peer report/verdict, explicit Q, its links, or its proof was read. The full canonical catalog record was read for the exact target and treated as context rather than a priority conclusion.

## Exact deduction

Let A=⟨x,y | [x,y]⟩≅Z² and

\[
H=\langle A,b\mid bxb^{-1}=y\rangle,
\qquad g=bx.
\]

Let K be the one-vertex cubical complex with three unit loops x,y,b and two squares with boundaries xyXY and bxBY; capitals denote inverse orientations.

### 1. The base is finite NPC

The torus square contributes the complete bipartite graph on {x,X} and {y,Y} to the vertex link. The other square adds the edges B–x, B–X, b–y, b–Y. This six-vertex, eight-edge graph is simple and bipartite (parts {x,X,b} and {y,Y,B}), so has no triangle and is flag. Therefore K is finite nonpositively curved, and its universal cover is a proper two-dimensional CAT(0) cube complex. Its fundamental group is H; the HNN normal-form theorem embeds A.

The accompanying finite script checks this link and the symmetry below. It only uses K and contains no construction of Q.

### 2. The actual element bx is WPD

Fix the following Bass–Serre convention. Vertices are left cosets hA. The oriented base edge e runs from A to bA and has stabilizer ⟨y⟩, using b⟨x⟩b⁻¹=⟨y⟩. Its translates have endpoints hA,hbA.

The homomorphism ε_b:H→Z sending b↦1 and x,y↦0 defines an integer height on vertices. The edge e increases height by one, and g increases every height by one. Since gA=bA, the edges gⁿe concatenate without backtracking; their union is an axis for g. Thus g is loxodromic, rather than merely an element of a group that has some loxodromic element.

At A the outgoing axis edge e has stabilizer ⟨y⟩. The incoming edge g⁻¹e has stabilizer

\[
g^{-1}\langle y\rangle g
=x^{-1}b^{-1}\langle y\rangle bx
=\langle x\rangle.
\]

Their intersection is trivial in A. The pointwise stabilizer of the two axis vertices g⁻¹A and gA fixes the intervening segment and is therefore trivial. The finite segment stabilizer criterion in [Minasyan–Osin, Corollary 4.3, corrected v6](https://arxiv.org/abs/1310.6289v6) consequently gives WPD for this g on this simplicial tree. No global acylindricity, local finiteness of the tree, or finite-index extension argument is needed.

### 3. The metric and finite-completion hypotheses hold exactly

[Dahmani–Guirardel–Osin, Theorem 6.8 and Corollary 2.9, v5](https://arxiv.org/abs/1111.7048v5), applied to the single loxodromic WPD element, supply a hyperbolically embedded virtually cyclic E(g) containing g. Pairwise noncommensurability imposes no condition on a singleton. H is finitely generated and ε_b(g)=1, so [Sisto, Theorem 1](https://arxiv.org/abs/1310.7753v1) applies and makes g Morse. The cited Sisto identifier and title are confirmed.

There is no hidden CAT(0)-metric conversion here: K has one vertex, so the 1-skeleton of its universal cover is exactly Cay(H,{x,y,b}), with the same edge metric. Taking geodesics in the Morse condition makes C=⟨g⟩ quasiconvex for this precise generating set. The two-edge circle Γ mapping by bx represents an injection Z→H, again by ε_b(g)=1. Its lift is within distance one of C and contains C. If desired, geodesics between lift vertices are handled by joining each endpoint to a C-vertex by one edge, obtaining uniform quasi-geodesics with endpoints in C. Thus the lifted graph has the required combinatorial quasiconvexity as well.

[BZ/K/L, Theorems 1.1 and 5.1](https://arxiv.org/abs/2011.05374v1) now give a finite NPC cube complex Q and a based cubical local isometry j:Q→K, through which Γ→K factors, with j_*(π₁Q)=C. The maximal tree in K is a single vertex, so their prescribed generating set is exactly {x,y,b}. Local-isometry injectivity identifies π₁Q with C, retaining the generator bx. Neither specialness nor a finite cover is required. The published version has the same needed statements: [WRAP published PDF](https://wrap.warwick.ac.uk/160721/1/WRAP-folding-like-techniques-CAT%280%29-cube-complexes-Kropholler-2021.pdf), pp. 2, 8–9.

It is unnecessary to prove E(g)=C, to eliminate a finite kernel of E(g), or to pass to a power of g. The completion is applied to C itself. Also, the initial bx circle is not a local isometry: its intermediate corner has germs B,x, which span an edge in the link of K. The completion theorem genuinely supplies the required replacement; attaching the uncompleted circle would be invalid.

### 4. One symmetry supplies the matched domain

Define λ on K by x↦y, y↦x, b↦b⁻¹. On xyXY it gives yxYX, a dihedral reparametrization of the same square. On bxBY it gives BybX, again a dihedral reparametrization of the same square. Hence λ extends to a cubical isometric involution of K. It fixes the unique vertex and sends bx to b⁻¹y.

The two maps j and λj use the identical finite cubical domain Q and are both based local isometries. This is stronger than equality of translation lengths and avoids an assumption that two independently constructed convex hulls happen to be isomorphic.

### 5. The finite cylinder gives properness and cocompactness

Form

\[
M=K\cup_{j,\lambda j}(Q\times[0,1]).
\]

This is a finite cube complex. The following general link argument does not inspect any link of the explicit new Q. At a vertex of K, each cylinder endpoint germ adds the cone on the corresponding image of Lk_Q(q) in Lk_K. This image is injective and full because the attaching map is a local isometry. There is no link edge between two distinct interval germs. A clique therefore either lies in the flag base link, or contains exactly one interval germ and lies in its cone on a full flag subcomplex. In either case it spans a simplex. All links are flag, so M is NPC. Its dimension is at most three, since local isometry into K forces dim Q≤2.

This also verifies the standard compact local-isometry gluing invoked in [Hagen–Wise v3, Remark 3.7](https://arxiv.org/abs/1605.07879v3). It does not use their free-cubulation theorem or its unresolved cocompactness strategy.

Van Kampen gives, with the interval direction chosen accordingly,

\[
\pi_1M=\langle H,z\mid z^{-1}(bx)z=b^{-1}y\rangle.
\]

The universal cover of a finite NPC cube complex is locally finite and finite dimensional, hence a proper CAT(0) cube complex. Its deck action by π₁M is proper and cocompact. In particular this is an action of the full displayed group, with no virtual qualifier and no inference from a mere free action.

### 6. The presentation is exactly the canonical target

Set

\[
t=x,\qquad a=xy^{-1},\qquad c=(zx)^{-1}=x^{-1}z^{-1}.
\]

These substitutions are invertible: x=t, y=a⁻¹t and z=c⁻¹t⁻¹. The relation [x,y]=1 becomes [a,t]=1. The relation bxb⁻¹=y becomes btb⁻¹=a⁻¹t, equivalently tbt⁻¹=ab.

Using b⁻¹y=xb⁻¹, the top relation is z⁻¹bxz=xb⁻¹. Substituting z=c⁻¹t⁻¹ and cancelling yields cbt c⁻¹=b⁻¹t, or

\[
c^{-1}(b^{-1}t)c=bt.
\]

Multiplication gives tc=bcbt and therefore tct⁻¹=bcb. The final b is positive. Thus π₁M is precisely the target G, and the route proves its geometric cubulation.

## Source chronology and erratum boundary

The relevant WPD criterion is already Corollary 4.2 in [Minasyan–Osin v1, 23 October 2013](https://arxiv.org/abs/1310.6289v1); it is Corollary 4.3 in v6 (20 December 2017). The [erratum, v1 26 November 2017; v2 9 March 2018](https://arxiv.org/abs/1711.09486v2) concerns the claimed invariance of acylindrical hyperbolicity under finite extensions/commensurability. This audit never uses that claim. In particular, E(g) being virtually cyclic is the hypothesis of Sisto's theorem, rather than an invocation of the erroneous finite-extension inference.

The required DGO statement is present as Theorem 6.8 in [v1, 30 November 2011](https://arxiv.org/abs/1111.7048v1), and in v5 (2 December 2014). Sisto has one arXiv version, dated 29 October 2013. Both needed completion statements are present in BZ/K/L v1, dated 10 November 2020. Its publication was [available online 28 October 2021](https://www.cambridge.org/core/journals/mathematical-proceedings-of-the-cambridge-philosophical-society/article/abs/foldinglike-techniques-for-cat0-cube-complexes/B81A93F5F50E9A49789D9194828FDE02), with journal issue July 2022. The literal cited Hagen–Wise Remark 3.7 is in v3 of 13 August 2025; the elementary link proof above establishes the needed gluing independently of that version.

Accordingly, the named non-gluing tools in this route were available by 10 November 2020. This is a bound on the availability of a sufficient theorem toolkit, not a proven date of discovery, publication, or recognition of this exact consequence. The inspected sources give general criteria; none of their checked relevant passages asserts the target G or this particular bx/λ(bx) cylinder application. That narrow observation is not a claim of exhaustive literature coverage. A previously documented direct application would require a separate exact-source witness.

## Adversarial disposition

| Suspected failure | Result |
|---|---|
| Wrong tree orientation or unrelated WPD element | Resolved by explicit axis and its adjacent stabilizers. |
| 2017 finite-extension gap | Not used; corrected current WPD statement applies directly. |
| CAT(0) quasiconvexity substituted for combinatorial quasiconvexity | Avoided by exact Cayley-graph identification. |
| Completion requires a finite cover or changes the subgroup | No: image is exactly ⟨bx⟩ and domain is finite. |
| Two cyclic models have unmatched shapes | Same Q works by postcomposition with λ. |
| Only a free/noncocompact/virtual action obtained | Finite NPC M gives full-group proper cocompact deck action. |
| Wrong sign in canonical c relation | Exact invertible substitutions produce bcb. |
| Proof circularly assumes the new explicit Q | No: Q is obtained existentially from the prior completion theorem. |
| Older toolkit mistaken for documented older solution | Remains a distinction; no direct older witness is supplied by this chain. |

Strongest checked mathematical result: the supplied theorem mechanism is sufficient for a geometric cubulation of the exact G, indeed in dimension at most three. Remaining gap in this audit is historical documentation of whether and when this exact deduction was previously made; there is no remaining mathematical hypothesis gap in the audited chain. No editorial classification is prescribed.

All downloaded papers, extracted text, HTML, detailed receipts and checksums remain under private_sources/priority_route_adversary. Public outputs are limited by the final positive allowlist.
