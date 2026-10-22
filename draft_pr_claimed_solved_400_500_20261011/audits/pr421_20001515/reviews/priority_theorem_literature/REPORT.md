# Independent theorem/literature priority audit: PR421 / 20001515

Audit date: 2026-10-12 UTC. Exact target:
```
G = <a,b,c,t | tat^-1=a, tbt^-1=ab, tct^-1=bcb>.
```
The last b is positive. The required conclusion is a proper, cocompact action by cubical isometries on a CAT(0) cube complex. This audit accepts the separately validated finite model with cells (1,7,8,2), dimension 3, at frozen source head d5bf8b5a25cabb177433338fae60af52ebfecf1c; it examines priority, not that model's proof.

**Finding.** A complete existence deduction can be assembled from earlier WPD, Morse, finite-completion, and convex-gluing results, using this group's specific HNN presentation and a cubical involution. No earlier primary source recording that application to this exact G was found. No inspected theorem on a recognized broad class of polynomial or quadratic mapping tori directly settles G by checking monodromy hypotheses alone. Therefore this is evidence that the existence claim is accessible using older tools; it is not evidence assigning an earlier target-specific resolution date. Neither first-resolution priority nor novelty of the exact small cell count is certified.

The initial independence seal used a stricter “earlier theorem implication” priority test. The subsequent root instruction distinguishes that test from the user's historical meaning of “already_solved.” This final report preserves the distinction: a deduction assembled during this audit does not by itself show that the problem had already been recorded as resolved.

## Checkable older-tools deduction

Set H=<x,y,b | [x,y]=1, bxb^-1=y>. Let K have one vertex, three unit edges, and squares xyx^-1y^-1 and bxb^-1y^-1. Its link is a simple bipartite graph, hence flag. Thus K is finite NPC. Its cubical involution λ swaps x,y and reverses b. On the second square it takes the boundary to a cyclic permutation of its inverse, so this is an actual cubical automorphism.

In the HNN Bass–Serre tree with vertex group A=<x,y>≅Z², put g=bx. The vertices g^n A form a geodesic axis: its words are cyclically reduced with stable letters all of the same sign. At A the adjacent axis edges have stabilizers <y> (toward bA) and x^-1<x>x=<x> (toward x^-1b^-1 A). Their intersection is trivial. A tree isometry fixing the two endpoints fixes the intervening segment pointwise.

[Minasyan–Osin, corrected v6](https://arxiv.org/pdf/1310.6289v6), Corollary 4.3, PDF p.13, therefore makes g WPD. This is an element-specific check; the whole tree action is not assumed acylindrical. Their [2018 erratum](https://arxiv.org/pdf/1711.09486v2) concerns an invalid finite-extension argument and affected manifold/commensurability claims, not Corollary 4.3 or its elementary tree proof.

[Dahmani–Guirardel–Osin](https://arxiv.org/pdf/1111.7048v5), Corollary 2.9, PDF p.8 (full theorem 6.8), gives a virtually cyclic hyperbolically embedded subgroup E(g) containing g. [Sisto](https://arxiv.org/pdf/1310.7753v1), Theorem 1, PDF p.1, makes g Morse in finitely generated H. In particular <g> is quasiconvex for the generating set x,y,b; Morse control of geodesics between orbit points is the needed hypothesis, not merely undistortion.

[Ben–Zvi–Kropholler–Lyman](https://arxiv.org/pdf/2011.05374v1), Theorems 1.1 and 5.1, produce a finite NPC completion j:Q→K of the two-edge circle spelling bx, with j a local isometry and j_*(π1Q)=<bx>. The [published version](https://wrap.warwick.ac.uk/id/eprint/160721/1/WRAP-folding-like-techniques-CAT%280%29-cube-complexes-Kropholler-2021.pdf) retains these statements: Theorem 1.1, typeset p.2/PDF p.3; Theorem 5.1, typeset p.8/PDF p.9, proof on the following page. K has one vertex, so the edge generating set required by Theorem 5.1 is precisely x,y,b. This application uses the finite-completion theorem without the supplied explicit Q.

Use j and λj as the two attachments of Q×[0,1] to K. The same domain Q provides identical cubical edge geometry; λ sends bx to b^-1y. Lifts of both local isometries are convex cubical embeddings. [Hagen–Wise v3](https://arxiv.org/pdf/1605.07879v3), Definition 3.1 and Remark 3.7, PDF pp.13–17, explicitly gives cocompact cubulation for compatible convex edge spaces and cocompact vertex spaces. Its auxiliary collection can be empty, so its auxiliary acylindricity conditions impose nothing here. Equivalently, the finite double mapping cylinder is NPC by the local-isometry link argument stated there. Its universal cover is CAT(0); the finite quotient makes its deck action proper and cocompact. Q has dimension at most 2 as a local isometry to K, so this also supplies a dimension-at-most-3 model, without a small-cell bound.

Van Kampen gives J=<H,z | z^-1(bx)z=b^-1y>. Since y=bxb^-1, the last relation is z^-1 bxz=xb^-1. Put t=x, a=xy^-1 and c=x^-1z^-1. Then [x,y]=1 becomes [t,a]=1, bxb^-1=y becomes tbt^-1=ab, and the last relation becomes tct^-1=bcb. Conversely y=a^-1t and z=c^-1t^-1 recover the original presentation. This proves exact isomorphism, rather than resemblance to a workshop variant.

The target-specific ingredients are the presentation change, the finite NPC base, the two-edge stabilizer calculation, and the involution-compatible attachment. The general theorems alone do not identify these ingredients for this mapping torus. No publication date is assigned to this combination.

## Other primary candidates and exact limits

| Source, inspected current version / locator | What it proves or leaves open for this target |
|---|---|
| [Hagen–Wise 1605.07879v3](https://arxiv.org/pdf/1605.07879v3), 13 Aug 2025; Cor.7.2 p.43, Questions1.2–1.3 p.5, Remark6.10 p.41 | The revised fast-automorphism theorem supplies free cube actions; its strategy for cocompactness is not a blanket geometric-cubulation theorem. Current v3 explicitly repairs only some cases of an older gap. The compatible convex gluing statement above is usable separately. |
| [Wu–Ye 2504.14192v1](https://arxiv.org/pdf/2504.14192v1), 19 Apr 2025; Thms1.4–1.5 pp.2–3 | Linear tubular families, virtual specialness, and particular tubular cocompactness criteria. The target's quadratic attachment is not established to lie in those tubular families; assuming such a transfer would move the central difficulty. |
| [Bongiovanni–Ghosh–Gültepe–Hagen 2508.15738v3](https://arxiv.org/pdf/2508.15738v3), 15 May 2026; ThmA p.2, Example9.4 pp.36–37 | Unbranched/coarse-median/HHG/quasi-isometry characterization. No geometric action follows from that equivalence; Example9.4 separates HHG from virtual cocompact cubulation. |
| [Munro–Petyt 2407.09275v3](https://arxiv.org/pdf/2407.09275v3), 11 Jun 2025; ThmsC–F pp.3–4 | Coarse obstructions and a tubular classification. ThmD excludes quadratic strata; ThmE requires a tubular group. Neither gives the target action without additional work. ThmF also prevents conflating noncompact virtual specialness with virtual cocompact cubulation. |
| [Lyman 1909.03097v3](https://arxiv.org/pdf/1909.03097v3), 4 Oct 2020; ThmA/CorB p.1, Question1 p.2, worked example p.4 | CAT(0) metric models, with cocompact cubulation explicitly asked separately. The palindromic b→aba example is the distinct workshop variant. |
| [Woodhouse, published](https://ems.press/content/serial-article-files/29874), 2018; Thm1.1 p.679/PDF1; [finite-dimensional paper](https://arxiv.org/pdf/1502.02619), Thm1.1 | Tubular virtual specialness/free finite-dimensional or locally finite actions do not supply cocompactness for the present iterated HNN extension. |
| [Button, accepted manuscript](https://api.repository.cam.ac.uk/server/api/core/bitstreams/8a19b850-deb4-4cd8-afcd-ffefcc239426/content), Theorem1; published2017 | Equitable-set free cubulation of tubular free-by-cyclic groups does not upgrade to the required geometric action. |
| [Brady–Soroko, author version](https://sites.math.unt.edu/~soroko/Dehn-functions-RAAGs.pdf), published2019; §5 pp.15–19, Props5.1/5.3 | Explicit NPC LOG models of polynomial mapping tori. Their displayed LOG presentations have torsionfree abelianization, unlike this G; no exact identification follows. RAAG subgroup embeddings also do not give a cocompact action of the subgroup. |
| [Leary–Niblo–Wise](https://eprints.soton.ac.uk/29827/1/Leary_Niblo_Wise.pdf), published1999; Props1–3 pp.1–4 of author copy | Different ascending-HNN examples. The rank3 example has torsionfree H1; it is not the target. Bestvina–Brady Morse functions there are not the Morse-element result used above. |
| [Dahmani–Krishna 2212.09869v2](https://arxiv.org/pdf/2212.09869v2), 29 Jan 2024; Thm1.1 p.2 | Relative cubulation under relative irreducibility/atoroidality hypotheses; infinite peripheral cell stabilizers are not proper action. No applicable relative decomposition settling G was found. |
| [Dahmani–Krishna–Mutanguha 2306.15054v2](https://arxiv.org/pdf/2306.15054v2), 29 Jan 2024; main theorem | Requires a hyperbolic mapping torus. Exact G contains <a,t>≅Z². |
| [Hsu–Wise, primary author manuscript](https://www.imo.universite-paris-saclay.fr/~frederic.haglund/MalnormalCubulation.pdf), 1 Mar 2012; ThmA/CorC p.1 | Requires relative hyperbolicity with abelian peripherals or hyperbolicity; no such applicable hypothesis was verified for this polynomial group. |
| [Haglund–Wise, published2012](https://annals.math.princeton.edu/wp-content/uploads/annals-v176-n3-p02-p.pdf), Thm1.2 p.1428/PDF2 | Hyperbolic virtually special vertex groups required by the stated main combination theorem; H contains Z². It does not replace the elementary convex gluing used above. |
| [Merladet Urigüen–Minasyan 2505.18054v3](https://arxiv.org/pdf/2505.18054v3), 29 Oct 2025; introduction and AppendixA | Virtual-retraction/CAT(0)/tubular virtual-special results; these are not an exact cocompact cubulation theorem for G. |
| [Leary 1009.1540v3](https://arxiv.org/pdf/1009.1540v3), 15 Oct 2012; AppendixC, ThmC.9 p.33 | General NPC link criterion, a construction tool; no target-specific resolution. |

Finite-index upward inheritance is not automatic. [Hagen](https://arxiv.org/pdf/1202.4462v4), Theorem B, p.2, classifies geometric cubulation of crystallographic groups by the hyperoctahedral condition. [Fioravanti, published2024](https://msp.org/gt/2024/28-1/gt-v28-n1-p03-p.pdf), Corollary G, p.170/PDF10 and proof PDF53–54, requires an invariant induced coarse median for the finite-index extension; it discusses the (3,3,3) triangle counterexample. No exact G-invariance argument can be omitted from a proposed virtual-special transfer.

Abelianization gives H1(G)=Z²⊕Z/2: the b relation kills a and the c relation imposes 2b=0. The workshop b→aba variant has Z²⊕(Z/2)². Its candidate 3-cube discussion in the [official workshop report](https://aimath.org/pastworkshops/freebycyclicrep.pdf), p.2, therefore does not transfer by a cosmetic relabeling.

## Search limits and recommendation

The search followed the initial papers' citations into primary classification, WPD/Morse, folding, and combination results, checked version changes and the relevant theorem/example portions, and searched literal words/presentations and standard-family names. SEARCH_LOG.json records the bounded queries; SOURCE_RECEIPTS.json records source hashes, dates, versions and failures. Full foreign source files stay private.

No absolute absence-of-prior-work assertion follows. The remaining historical gap is an earlier recorded exact application, or a broader stated theorem demonstrably covering this G without the presently made target-specific combination. The accepted explicit (1,7,8,2) construction's novelty is also unproved: the older-tools route produces a finite completion, not that cell count. A defensible statement is “an explicit small NPC model, with a separate existence deduction from older general results”; “first resolution of an open problem” needs the historical gap closed. This audit alone does not justify relabeling the problem already_solved under the historical definition.

Original budget remains 1/5; zero new proof-search turns. No outreach or Git/PR/publication operations were performed.

