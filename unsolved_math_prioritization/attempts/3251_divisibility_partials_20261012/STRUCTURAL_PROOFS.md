> Edition note: This complete authored text preserves the mathematical arguments and substantive audit findings. Original operational references and identities of material not distributed here have been replaced with descriptive prose. The independent audits are AI mathematical reviews, not human peer review or formal proof verification.

# Odd-hole-free 2-division: structural continuation and a precise gluing obstruction

## Status and scope

**The unrestricted conjecture is not proved or disproved here.** The results below are complete proofs of the stated reductions and extension lemmas, together with an explicitly identified published theorem for clique number three. No novelty is claimed. Finite checks are regression tests, not substitutes for proofs.

All graphs are finite and simple. A graph is **nonedgeless** if it has at least one edge. Put \(\omega(\varnothing)=0\). For a graph \(G\) with \(k=\omega(G)\ge2\), a **division** is a partition \(V(G)=A\mathbin{\dot\cup}B\) with \(\omega(G[A]),\omega(G[B])<k\). Parts may be empty in the definition, although neither is empty in a division of a nonedgeless graph. This is exactly a two-coloring with no monochromatic maximum clique. Hereditary **2-divisibility** asks this for every nonedgeless induced subgraph. It is different from perfect divisibility.

The target is that every odd-hole-free nonedgeless graph has a division. An odd hole is an induced cycle of odd length at least five. The edgeless exception is part of the intended formulation, not a counterexample to be exploited.

## 1. Verified elementary baseline and the clique-number-three case

**Lemma 1 (color grouping).** If \(\omega(G)=k\ge2\) and \(\chi(G)\le2k-2\), then \(G\) has a division.

**Proof.** Take a proper coloring with at most \(2k-2\) colors. Divide its color classes into two groups, each containing at most \(k-1\) classes. Each clique meets each proper color class in at most one vertex, so neither resulting part contains a \(k\)-clique. \(\square\)

This contains the earlier case \(\chi=\omega\): alternatively, isolate one proper color class and put all other classes together.

For \(k=2\), an odd-hole-free graph is bipartite. Otherwise choose a shortest odd cycle. A chord splits it into two shorter cycles, one odd, contradicting minimality. It therefore is induced; triangle-freeness excludes length three, and odd-hole-freeness excludes every other possible odd length. A proper bipartition is a division.

For \(k=3\), Chudnovsky, Robertson, Seymour and Thomas prove that every \(K_4\)-free odd-hole-free graph is four-colorable [CRST, Theorem 1.3, repeated as 3.2]. Lemma 1, grouping four proper colors into two pairs, gives the desired division. This application uses their published theorem as an external mathematical input; it is not a new proof of their decomposition theorem.

Consequently, any counterexample to the target has \(\omega\ge4\). The source statement and the application were checked, but the entire CRST proof was not independently audited here.

For completeness, the basic imperfect examples also have direct divisions. Let \(G=\overline{C_{2q+1}}\), \(q\ge3\). Then \(\omega(G)=q\), because the independence number of the original cycle is \(q\). Split its cyclic order into consecutive blocks of lengths \(q\) and \(q+1\). Each block induces a path in the original cycle, so its clique number in \(G\) is respectively \(\lceil q/2\rceil\) and \(\lceil(q+1)/2\rceil\), both less than \(q\). These antiholes are odd-hole-free: every vertex has only two nonneighbors, so an induced odd hole would have length at most five; an induced five-cycle would force the selected set to contain both original cycle-neighbors of each selected vertex, hence the whole \((2q+1)\)-cycle, a contradiction.

If every nonedgeless induced subgraph of a graph has a division, induction on \(k\) gives \(\chi(G)\le2^{k-1}\). For \(k=1\) use one color; for \(k\ge2\), divide and apply disjoint palettes to the two parts. This is the standard hereditary consequence, not a proof of the missing division.

## 2. The correct minimal-obstruction framework

Call \(G\) **minimal indivisible** if it is nonedgeless, has no division, and every proper nonedgeless induced subgraph has a division. If the target has a counterexample, choose one of minimum order. Since odd-hole-freeness is hereditary, that graph is minimal indivisible in this sense.

The following general reductions do not require odd-hole-freeness.

**Proposition 2.** If \(G\) is minimal indivisible and \(k=\omega(G)\), then:

1. \(\omega(G-v)=k\) for every vertex \(v\).
2. \(\chi(G)\ge2k-1\), and \(|V(G)|\ge3k-2\).
3. For every division \((A,B)\) of \(G-v\), the sets \(A\cap N(v)\) and \(B\cap N(v)\) each contain a \((k-1)\)-clique.
4. Every vertex lies in two maximum cliques whose intersection is exactly that vertex; in particular, \(\deg(v)\ge2k-2\).

**Proof.** If deleting \(v\) reduced the clique number, the partition \(\{v\},V(G)\setminus\{v\}\) would be a division, proving (1). Lemma 1 proves the chromatic inequality in (2). In an optimal proper coloring with \(q\) nonempty classes, the vertices forming singleton classes are pairwise adjacent: otherwise two singleton classes could be merged. There are therefore at most \(k\) singleton classes. Every other class has at least two vertices, so \(|V(G)|\ge2q-k\ge3k-2\).

By (1) and minimality, \(G-v\) has a division at the same threshold \(k\). If \(A\cap N(v)\) contained no \((k-1)\)-clique, adding \(v\) to \(A\) would leave both parts \(K_k\)-free. This would divide \(G\). The same argument applies to \(B\), proving (3). Choose the two cliques from (3). They are disjoint, and adding \(v\) to each proves (4). \(\square\)

The lower degree bound is familiar from vertex-Folkman criticality. Here it is derived directly, and no claim of novelty is made.

**Lemma 3 (paired local obstruction).** For the two \((k-1)\)-cliques \(R,B\subseteq N(v)\) furnished by Proposition 2, there is a bijection \(f:R\to B\) such that every \(x\in R\) is nonadjacent to \(f(x)\).

**Proof.** Form the bipartite graph \(F\) on \(R,B\) whose edges are nonedges of \(G\). For \(X\subseteq R\), every vertex of \(X\) is adjacent in \(G\) to every vertex of \(B\setminus N_F(X)\). Thus \(X\cup(B\setminus N_F(X))\) is a clique in \(G[N(v)]\). Such a clique has size at most \(k-1\), because adjoining \(v\) would otherwise produce a clique larger than \(k\). Hence \(|N_F(X)|\ge|X|\).

Here is the matching argument explicitly. Choose a maximum matching. If it leaves some vertex of \(R\) unmatched, start alternating paths at all unmatched vertices of \(R\). No reached vertex of \(B\) can be unmatched, since that would give an augmenting path. Let \(X\) and \(Y\) be the reached vertices in \(R\) and \(B\). Then \(Y=N_F(X)\), every vertex of \(Y\) has a distinct matched partner in \(X\), and \(X\) additionally contains an unmatched starting vertex. Therefore \(|N_F(X)|=|Y|<|X|\), a contradiction. A perfect matching gives the desired bijection. \(\square\)

An immediate constructive criterion follows: if a graph of clique number \(k\) has an elimination order in which, whenever the remaining graph still has a \(k\)-clique, the next vertex's neighborhood contains no two disjoint \((k-1)\)-cliques, then it has a division. Stop when the remaining clique number is less than \(k\), color those remaining vertices arbitrarily, and reinsert vertices in reverse order. Both choices of color can fail only if the two forbidden disjoint cliques exist. In particular, every \((2k-3)\)-degenerate graph of clique number \(k\) has a division. This is a one-step claim at threshold \(k\).

## 3. Connectedness, the active clique core, and modules

Define the **maximum-clique edge core** \(F\) to have the same vertices as \(G\), with an edge \(xy\) exactly when \(x,y\) lie together in some maximum clique of \(G\). This graph records constraint connectivity; its edges need not include every edge of \(G\).

**Proposition 4.** A minimal indivisible graph \(G\) and its maximum-clique edge core are connected and have no cut vertex. Also \(\overline G\) is connected.

**Proof.** A maximum clique lies in one connected component of the core. If the core were disconnected, independently color the induced subgraphs of \(G\) on its components. Each is proper. If its clique number is \(k\), use minimality; if smaller, color arbitrarily. No maximum clique becomes monochromatic, a contradiction.

If \(v\) is a cut vertex of the core, let \(D_1,\ldots,D_t\), \(t\ge2\), be its components after deletion. Color each proper induced graph \(G[D_i\cup\{v\}]\) without a monochromatic \(k\)-clique, using minimality when necessary. Swap the two colors in a block if necessary so that all blocks give \(v\) the same color. Every maximum clique lies in one block, because otherwise two of its vertices in distinct \(D_i\)'s would form a core edge. The combined coloring is a division, a contradiction.

Since the core is a spanning subgraph of \(G\), its connectedness and absence of cut vertices imply the same properties for \(G\). Finally, if \(\overline G\) is disconnected, partition its components into two nonempty unions \(X,Y\). Then \(X\) is complete to \(Y\) in \(G\), so \(k=\omega(G[X])+\omega(G[Y])\). Both summands are positive and less than \(k\); coloring \(X,Y\) differently is a division. \(\square\)

**Caution.** Deleting graph edges outside maximum cliques preserves the division constraints but can create induced odd holes. The core is not asserted to be odd-hole-free. It cannot simply replace \(G\) in a structural theorem about odd-hole-free graphs.

A **module** is a set \(M\) with \(1<|M|<|V(G)|\) such that every vertex outside \(M\) is either complete or anticomplete to \(M\).

**Proposition 5.** A minimal indivisible graph has no module.

**Proof.** Suppose \(M\) is a module, and put \(L=V(G)\setminus M\).

First assume \(G[M]\) has an edge. Divide \(G[M]\) by minimality. Color \(G[L]\) without a monochromatic \(k\)-clique: use its division if it has an edge, or any coloring otherwise. Combine the two colorings. A maximum clique entirely in one piece is not monochromatic. If a maximum clique \(K\) meets both pieces, its outside part is complete to all of \(M\), by the module property. Consequently \(K\cap M\) must be a maximum clique of \(G[M]\): replacing it with a larger clique of \(G[M]\) would enlarge \(K\). The division of \(G[M]\) makes \(K\cap M\), hence \(K\), bichromatic.

If \(M\) is stable, retain a representative \(m\in M\) and delete the others. The resulting proper induced graph has clique number \(k\), since every clique uses at most one vertex of \(M\), and that vertex can be replaced by \(m\). Divide this graph and assign every vertex of \(M\) the representative's color. Any hypothetical monochromatic maximum clique would replace to one in the smaller graph, a contradiction. \(\square\)

The module-free reduction is already present in the literature, for example Song–Xu, Lemma 2.3 [SX]. The proof above explicitly separates stable modules, which cannot themselves have a division under the nonedgeless convention.

## 4. Clique-precolor extension

The next lemma identifies when a side of a clique separator imposes **no** additional constraint on the separator's two colors.

**Lemma 6.** Let \(k\ge2\), let \(H\) satisfy \(\chi(H)\le2k-2\), and let \(C\) be a clique of \(H\). Any red/blue coloring of \(C\) with at most \(k-1\) vertices of each color extends to a coloring of \(H\) with no monochromatic \(k\)-clique.

**Proof.** Choose a proper coloring of \(H\) with \(q\le2k-2\) classes. Vertices of \(C\) lie in distinct classes. Assign each of those classes its vertex's prescribed red/blue color. If \(a,b\) classes are thus assigned red and blue, respectively, their remaining capacities are \(k-1-a\) and \(k-1-b\), both nonnegative. The number \(q-a-b\) of remaining classes is at most the sum of these capacities. Distribute the remaining classes accordingly. Each final color is a union of at most \(k-1\) stable sets, so it contains no \(k\)-clique. \(\square\)

In particular, a perfect side of clique number at most \(k\) always accepts every admissible precoloring, since \(\chi(H)=\omega(H)\le k\le2k-2\).

## 5. Exact separator compatibility and numerical consequences

Let \(C\) be a nonempty clique cutset of \(G\), let \(s=|C|\), and let \(D_1,\ldots,D_t\), \(t\ge2\), be the components of \(G-C\). Set \(H_i=G[C\cup D_i]\). The threshold throughout is \(k=\omega(G)\), even when a side has smaller clique number.

Let \(\mathcal T\) be the two-colorings of \(C\) with no monochromatic \(k\)-clique. Since \(C\) is a clique, \(s\le k\). If \(s<k\), all colorings are in \(\mathcal T\); if \(s=k\), precisely the two constant colorings are excluded. Let \(\mathcal S_i\subseteq\mathcal T\) consist of the colorings of \(C\) that extend to \(H_i\) without a monochromatic \(k\)-clique.

**Proposition 7 (exact compatibility).** A graph \(G\) has a division if and only if \(\bigcap_{i=1}^t\mathcal S_i\ne\varnothing\).

**Proof.** Restrict a division to each side for one direction. Conversely, extend a common coloring independently to each side and combine the extensions. No clique uses vertices from two distinct \(D_i\)'s, so every maximum clique lies in one side. \(\square\)

**Theorem 8 (minimal separator obstruction).** If \(G\) is minimal indivisible, then every clique cutset as above satisfies:

1. Every \(\mathcal S_i\) is nonempty and invariant under simultaneously swapping both colors, but their total intersection is empty.
2. For each \(i\), there is a boundary coloring \(c_i\) lying in every \(\mathcal S_j\), \(j\ne i\), and not in \(\mathcal S_i\). The color-swap orbits of these \(c_i\)'s are all distinct.
3. \(t\le2^{s-1}\) if \(s<k\), and \(t\le2^{k-1}-1\) if \(s=k\).
4. For every \(i\), \(\chi(H_i)\ge2k-1\) and \(|V(H_i)|\ge3k-2\). Hence
   \[
   |V(G)|\ge s+t(3k-2-s).
   \]
5. Each component \(D_i\) meets a maximum clique of \(G\).

**Proof.** Each side is a proper induced subgraph. Minimality supplies an admissible coloring; if its clique number is below \(k\), any coloring already avoids monochromatic \(k\)-cliques. Thus \(\mathcal S_i\ne\varnothing\). Color-swap invariance is immediate, and Proposition 7 gives the empty total intersection.

Remove all of \(D_i\). The remaining graph is proper, so color it without a monochromatic \(k\)-clique, using minimality or the smaller threshold as appropriate. Its restriction \(c_i\) belongs to all \(\mathcal S_j\) with \(j\ne i\). It cannot belong to \(\mathcal S_i\), or it would extend to all of \(G\). If \(c_i\) and \(c_j\) shared a color-swap orbit for distinct \(i,j\), invariance and \(c_j\in\mathcal S_i\) would contradict \(c_i\notin\mathcal S_i\). There are \(2^{s-1}\) orbits of colorings of a nonempty \(s\)-set, with one orbit removed when \(s=k\). This proves (2)–(3).

If \(\chi(H_i)\le2k-2\), Lemma 6 would imply \(\mathcal S_i=\mathcal T\), contrary to the witness \(c_i\notin\mathcal S_i\). Therefore \(\chi(H_i)\ge2k-1\). The singleton-class argument in Proposition 2 applied to \(H_i\), whose clique number is at most \(k\), yields \(|V(H_i)|\ge2\chi(H_i)-\omega(H_i)\ge3k-2\). Summing \(|D_i|=|V(H_i)|-s\) proves (4).

Finally, if no maximum clique met \(D_i\), an admissible coloring of \(G-D_i\) could be extended arbitrarily over \(D_i\) without making any maximum clique monochromatic. This proves (5). \(\square\)

**Consequences.** A one-vertex clique separator is impossible, recovering the cut-vertex reduction. For a separator \(C=\{x,y\}\) of size two and \(k\ge3\), there are only two boundary orbits: equal colors and different colors. Thus a minimal obstruction would have exactly two components, with one side allowing only equal colors on \(x,y\), and the other allowing only different colors. Both sides must have chromatic number at least \(2k-1\). If \(k=4\), each side has at least ten vertices and the complete graph has at least eighteen. For any clique separator in the \(k=4\) case, the displayed order bound gives at least sixteen vertices.

This is a rigorous reduction, not a proof that such incompatible sides cannot occur in odd-hole-free graphs. In particular, absence of clique cutsets is **not** assumed. Hoàng explicitly poses that absence as Conjecture 4.7 in [H25].

## 6. Two concrete reasons the direct gluing/local-extension approaches stop

**Different valid local divisions need not align by a color swap.** Take two triangles sharing an edge \(xy\), with other vertices \(a,b\). On triangle \(xya\), color \(x,y\) red and \(a\) blue. On triangle \(xyb\), color \(x,b\) red and \(y\) blue. Each local triangle is divided, but one restriction colors \(x,y\) equally and the other differently; no global swap aligns them. The graph itself is easily divisible. Thus the existence of some local divisions does not establish compatibility of arbitrary chosen divisions.

**A good deletion coloring can be blocked in a graph that is itself perfect.** Take two \(k\)-cliques meeting in exactly \(v\), with no other cross edges, for \(k\ge3\). After deleting \(v\), color one \((k-1)\)-clique red and the other blue. This valid coloring does not extend to \(v\). Nevertheless, color \(v\) red and choose one blue vertex in each clique, coloring the others red; this is a division. The graph has no induced cycle of length at least four. Therefore the paired local obstruction alone cannot force an odd hole. One must control which deletion coloring is selected or how different local obstructions interact globally.

## 7. What remains for the original target

Combining the proved reductions with the checked published inputs, a smallest counterexample would have clique number \(k\ge4\), at least \(3k-2\) vertices, chromatic number at least \(2k-1\), minimum degree at least \(2k-2\), no nontrivial module, and a 2-connected maximum-clique edge core. Its complement is connected. Each vertex lies in two maximum cliques intersecting only there, and the corresponding two neighborhood cliques admit a perfect matching of nonedges.

It must also contain an induced \(P_5\), because odd-hole-freeness already excludes \(C_5\), and Chudnovsky–Sivaraman prove the \((P_5,C_5)\)-free subclass is 2-divisible [CS, Theorem 2.1]. It is nonperfect by Lemma 1; the Strong Perfect Graph Theorem would therefore force an odd antihole of length at least seven. This last structural conclusion invokes that classical external theorem, rather than a proof of it here.

The remaining problem is to rule out such a graph while using the absence of induced odd holes. The separator analysis pinpoints one obstruction: incompatible feasible boundary-color sets cannot be dismissed merely because every side has some division. The local analysis pinpoints another: blocked deletion colorings occur even in perfect graphs. Neither obstruction has been eliminated in general here.

## 8. Source dependencies and inspection levels

- **[OPG]** [2-colouring a graph without a monochromatic maximum clique](https://www.openproblemgarden.org/op/2_colouring_a_graph_without_a_monochromatic_maximum_clique). Problem statement inspected. The original Hoàng–McDiarmid publisher abstract, [On the divisibility of graphs](https://www.sciencedirect.com/science/article/pii/S0012365X01000541), explicitly uses induced subgraphs with at least one edge.
- **[CRST]** Chudnovsky–Robertson–Seymour–Thomas, [K4-free graphs with no odd holes](https://thomas.math.gatech.edu/PAP/k4free.pdf). Author PDF dated October 5, 2001, revised August 5, 2009; 24 PDF pages. Theorem 1.3 on printed page 1 (PDF page 3), and its derivation as Theorem 3.2, inspected. The source itself explicitly notes the implication for the K4-free division problem. The complete decomposition proof is an external dependency, not independently audited here.
- **[CS]** Chudnovsky–Sivaraman, [Perfect divisibility and 2-divisibility](https://web.math.princeton.edu/~mchudnov/Perfect2div.pdf), author PDF dated April 20, 2017. Definitions, Lemma 1.2 and Theorem 2.1 inspected. The bull-free perfect-divisibility statements are not used as though they directly established the target.
- **[SX]** Song–Xu, [Divisibility and coloring of some P5-free graphs](https://kam.mff.cuni.cz/~spring/media/papers/4/Divisibility_Coloring_P5_free_JS.pdf), Discrete Applied Mathematics 348 (2024), 144–151. Lemma 2.3 inspected for prior credit for the homogeneous-set reduction. Proposition 5 is proved fully above and does not depend on the source proof's treatment of edgeless modules.
- **[H25]** Hoàng, [On the structure of perfectly divisible graphs](https://arxiv.org/pdf/2506.12660v2), arXiv:2506.12660v2, June 17, 2025. Section 4 and especially Conjectures 4.6–4.7 inspected. Used to delineate the unresolved gluing assertion, not as a theorem proving it.
- **[SPGT]** Chudnovsky–Robertson–Seymour–Thomas, [The strong perfect graph theorem](https://arxiv.org/abs/math/0212070), Annals of Mathematics 164 (2006), 51–229. The standard characterization is used only for the optional odd-antihole consequence; no independent proof audit is claimed.

All other mathematical assertions in Sections 2–6 are proved here. No copied source documents, source text, dataset contents, or private coordination material are part of this authored proof.

## 9. Reproducibility

The original author program, written in Python 3 using only the standard library, enumerated every labeled simple graph on zero through six vertices, computed clique and chromatic numbers exactly, checked the clique-precolor extension and exact separator identity, constructed module colorings, and checked the listed critical-obstruction restrictions whenever minimal indivisibility held. The original result record retained exact counts and the program identity. No external solver, random sampling, or downloaded author program was used. The program and raw result records are not distributed in this prose-only edition; the complete mathematical arguments above and the substantive audit below remain available. The finite counts are reproduced in VERIFICATION_SCOPE.md.

No minimal indivisible graph with a clique cutset occurs in this finite range, so the numerical critical-separator assertions have no nonvacuous small-order test instance. The exact separator identity and clique-precolor extension do have the many nonvacuous instances counted in the output.

The tests cannot resolve larger orders or certify that all odd-hole-free graphs divide. Their role is to catch errors in the finite formulations and constructions; the general reductions rest on their written proofs.
