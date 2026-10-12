# Exceptional surfaces: thin generic chains and limits of the circular-cover method

**30006161 / OWR-14299082-003. Partial result; the original two questions remain unresolved.**

For both $S^2$ and $\mathbb{RP}^2$, we prove the following scoped consequence of classical chain-density results: comeagrely many maximal connected chains have **empty interior in every proper member**. Consequently, the orbit of any chain containing a proper set with nonempty interior is meagre, although every orbit is dense. In particular, the elementary chains of concentric disks cannot be the sought generic chains.

We also give an elementary fundamental-group obstruction to a circular covering. It verifies precisely why one branch of the published negative theorem cannot cover the two exceptional surfaces. Neither statement settles whether some orbit inside the residual set of thin chains is comeagre. All imported results are credited; no novelty or human peer review is claimed. Separate adversarial review is pending.

## 1. The exact problem and topology

The original is Andrea Vaccaro's report, jointly with Gianluca Basso and Alessandro Codenotti, in [Oberwolfach Report 2/2025](https://ems.press/content/serial-article-files/51347), printed pp.89–92. Question 3 on p.90 asks whether there is a generic chain on the sphere, and whether there is one on the real projective plane.

Here $C(X)$ is the space of **nonempty** compact connected subsets of a compact metric space $X$, with the Vietoris topology, equivalently its Hausdorff metric $d_H$. A maximal connected chain is a family $\mathcal C\subset C(X)$ linearly ordered by inclusion and maximal for that property. The space

$$\Phi(X)\subset C(C(X))$$

of such chains has the second Vietoris topology, equivalently the Hausdorff metric induced by $d_H$. It is compact and metrizable. Each chain is an order arc from a singleton to $X$; it has a unique root, the point in its intersection.

The acting group is the **full** group $G=\operatorname{Homeo}(X)$ with the compact-open topology. Its action is

$$g\mathcal C=\{g[K]:K\in\mathcal C\}.$$

A chain is generic exactly when its orbit is comeagre in $\Phi(X)$, meaning that the complement is a countable union of nowhere dense sets. Density of one orbit, or even density of every orbit, is a weaker assertion.

The full accepted version of [Basso–Codenotti–Vaccaro, arXiv:2403.08667v3](https://arxiv.org/abs/2403.08667v3), abbreviated BCV, defines these objects in Section 2.1. Its Question 1.4 retains both exceptional surfaces. The paper is published in Duke Mathematical Journal **174** (2025), 3135–3196, [DOI](https://doi.org/10.1215/00127094-2025-0010). The complete accepted manuscript was retrieved; the final journal PDF was not compared line by line.

## 2. Credited density and minimality inputs

We use two published facts of Yonatan Gutman, [*Minimal actions of homeomorphism groups*, Fundamenta Mathematicae **198** (2008), 191–215](https://doi.org/10.4064/fm198-3-1). The complete [published PDF](https://www.impan.pl/shop/en/publication/transaction/download/product/88680) was retrieved and the relevant hypotheses and proofs were inspected.

- **Ray density:** Theorem 5.3, pp.198–199, says that ray-induced chains are dense for a strongly arcwise-inseparable Peano continuum. Lemma A.1, p.211, verifies this hypothesis for every closed topological surface.
- **Minimality:** Theorem 6.5, pp.201–202, gives minimality of the chain action for a locally transitive group under the same continuum hypothesis. The full homeomorphism group of a closed surface is locally transitive. Thus every orbit in $\Phi(X)$ is dense. BCV Theorem 7.7 independently includes this case and explicitly credits Gutman's earlier theorem.

A ray-induced chain means

$$\mathcal C_\gamma=\{\gamma([0,t]):0\le t<\infty\}\cup\{X\},\tag{1}$$

where $\gamma:[0,\infty)\to X$ is continuous, injective and has dense image. Every finite restriction of $\gamma$ is an embedding by compactness. Hence every proper member in (1) is an arc or a singleton, and has empty interior in a surface. One way to see the latter is that an open disk contained in an arc would embed a circle in an interval, which is impossible.

The published ray-density proof is an actual approximation theorem in the **double Hausdorff topology**, not just density of finite arcs in $C(X)$. That distinction is essential for the following argument. Gutman's notation $M(X)$ for the connected-chain space agrees with the present $\Phi(X)$; his $\Phi(X)$ without the connectedness restriction is a larger space and is not being substituted here.

## 3. A residual thinness theorem

### Proposition 1

Let $X$ be a closed connected topological surface. Then

$$\mathcal T(X)=\{\mathcal C\in\Phi(X):
\operatorname{Int}_X K=\varnothing\text{ for every }K\in\mathcal C\setminus\{X\}\}\tag{2}$$

is a dense $G_\delta$ subset of $\Phi(X)$. Its complement is meagre. Moreover, if a chain contains a proper member with nonempty interior, its whole homeomorphism orbit is meagre.

### Proof

Choose a countable collection of nonempty closed disks $B_i\subset X$ whose interiors refine every nonempty open set, and a countable basis of nonempty open sets $U_j$. Such disks can be chosen in a countable atlas using rational closed coordinate disks.

For each $i,j$, put

$$F_{ij}=\{\mathcal C\in\Phi(X):
\exists K\in\mathcal C\text{ with }B_i\subset K\subset X\setminus U_j\}.\tag{3}$$

The incidence relation

$$\{(\mathcal C,K)\in\Phi(X)\times C(X):K\in\mathcal C\}$$

is closed: if $\mathcal C_n\to\mathcal C$ and $K_n\to K$ with $K_n\in\mathcal C_n$, the second Hausdorff metric implies $K\in\mathcal C$. The conditions $B_i\subset K$ and $K\subset X\setminus U_j$ are also closed for Hausdorff convergence. Therefore the set of pairs satisfying all three conditions is compact. Its projection $F_{ij}$ is compact, hence closed.

No ray-induced chain belongs to $F_{ij}$. Its proper members have empty interior and cannot contain $B_i$, while its last member $X$ cannot avoid the nonempty set $U_j$. Since ray-induced chains are dense by Gutman's Theorem 5.3, every closed set $F_{ij}$ has empty interior. Thus every $F_{ij}$ is nowhere dense.

A chain fails (2) precisely when it lies in some $F_{ij}$. Indeed, given a proper member $K$ with nonempty interior, choose $B_i\subset\operatorname{Int}K$ and $U_j\subset X\setminus K$. Conversely, the member witnessing (3) is proper and contains a nonempty open disk. Consequently

$$\Phi(X)\setminus\mathcal T(X)=\bigcup_{i,j}F_{ij}.\tag{4}$$

This is a countable union of closed nowhere dense sets, proving that $\mathcal T(X)$ is comeagre and $G_\delta$; compact metrizability and the Baire theorem give its density. The property of having a proper member with nonempty interior is invariant under ambient homeomorphisms. An orbit of such a chain is contained in the meagre set (4), hence is itself meagre. $\square$

### Corollary 2: the natural disk chains do not answer the source question

The conclusion applies in particular to $S^2$ and $\mathbb{RP}^2$. A nested family of round closed metric balls, from radius zero up to the diameter in the usual round metric, is a maximal connected chain on either space. Before the last radius, each positive-radius member is a proper disk with nonempty interior. Therefore its orbit is meagre.

These ball families really are maximal chains: their members vary continuously in the Hausdorff metric, strictly increase from a point to $X$, and any compact set comparable to every member equals the member at the supremum of the parameters below it. The spherical radii run from $0$ to $\pi$; the projective radii run from $0$ to $\pi/2$ when the covering sphere has radius one.

By the credited minimality theorem, these same meagre orbits are dense. Thus approximating every chain by images of a round-disk chain would not establish genericity. If a comeagre orbit exists, Proposition 1 forces it to lie entirely inside $\mathcal T(X)$: it must meet that invariant comeagre set by the Baire theorem.

## 4. Why circular covers cannot supply the missing negative answer

BCV Theorem 1.2 excludes generic chains under any of three hypotheses: a locally non-planar open subset; a planar open set containing a simple closed curve that is not locally separating; or a circular covering. The first two fail for a closed surface, since local charts are planar and a local arc of any embedded circle separates a sufficiently small coordinate disk.

Their circular-cover definition requires connected open sets $O_0,\ldots,O_{\ell-1}$, $\ell\ge4$, covering $X$, such that

$$\overline O_i\cap\overline O_j\ne\varnothing
\quad\Longleftrightarrow\quad i=j\text{ or }i-j\equiv\pm1\pmod\ell,$$

and each $O_i\setminus\bigcup_{j\ne i}O_j$ is connected. The next necessary condition does not even need that last requirement.

### Lemma 3: a cycle cover gives an infinite cyclic quotient

Suppose a compact metrizable, locally path-connected space $X$ has a finite cover by connected open sets satisfying the displayed closure-intersection pattern. Then there is a continuous map

$$f:X\longrightarrow S^1$$

whose induced homomorphism on fundamental groups is surjective onto $\mathbb Z$.

### Proof

All nonadjacent pairs of cover sets are disjoint and no three cover sets meet. Adjacent sets actually overlap, rather than merely having intersecting closures. For if $p\in\overline O_i\cap\overline O_{i+1}$, choose $O_k$ containing $p$. If $k=i$ or $k=i+1$, openness supplies points in $O_i\cap O_{i+1}$. Otherwise $\overline O_k$ meets both adjacent closures, impossible for a cycle of length at least four.

Choose a partition of unity subordinate to this finite cover, for example by normalizing the functions $d(x,X\setminus O_i)$ in any compatible metric. Their positive coordinates at any point belong to one vertex or an adjacent pair. They therefore define a continuous map $f$ to the geometric cycle $C_\ell\cong S^1$. Moreover $f(O_i)$ lies in the open star of the vertex $v_i$.

Pick $p_i\in O_i\cap O_{i+1}$, with indices modulo $\ell$, and choose a path $\gamma_i$ in $O_i$ from $p_{i-1}$ to $p_i$. Such paths exist because the sets are connected, open and locally path-connected. The loop $\gamma_0*\cdots*\gamma_{\ell-1}$ maps to a loop in the geometric cycle. Its $i$th part lies in the star of $v_i$, joining interior points of the two incident edges. Within that contractible star it is homotopic, relative to its endpoints, to the path through $v_i$. The concatenated paths traverse the cycle exactly once. Their winding number is one, so $f_*$ contains a generator of $\mathbb Z$. $\square$

Since $\pi_1(S^2)=0$ and $\pi_1(\mathbb{RP}^2)\cong\mathbb Z/2$, neither group surjects onto $\mathbb Z$. Thus neither surface admits a circular cover. This agrees with, and gives an elementary group-theoretic explanation of, BCV Proposition 6.13, whose proof instead uses their unicoherence. The argument is a standard nerve/partition-of-unity construction; no novelty is asserted.

Importantly, the lemma is an obstruction to applying **that sufficient hypothesis**. It is not a proof that a generic chain exists. A cycle occurring in one finite graph approximation is also not a circular cover of the entire surface: additional vertices or intersections can destroy the winding-number quotient.

## 5. The remaining quantifier gap

BCV Theorem 5.6 records Rosendal's criterion. In the present Polish action, a comeagre orbit exists exactly when the action is topologically transitive and

$$\begin{gathered}
\text{for every identity neighborhood }H\subset G\text{ and nonempty open }U\subset\Phi(X),\\
\text{there is a nonempty open }V\subset U\text{ such that, for all nonempty open }W_0,W_1\subset V,\\
H W_0\cap W_1\ne\varnothing.\tag{5}
\end{gathered}$$

Topological transitivity already holds by minimality. What remains is to prove (5), or to find one fixed $H,U$ such that **every** nonempty open refinement $V\subset U$ contains two smaller open sets that cannot be reconciled by an element of $H$. Excluding the disk-chain orbit, or establishing the failure for only one chosen refinement, does not meet that quantifier.

The off-by-one graph-amalgamation condition in BCV Theorem 5.9 is a necessary consequence of (5), not a stated sufficient criterion. Passing a finite collection of graph tests cannot settle the original question either way.

There is another tempting but invalid shortcut. BCV Theorem 7.7 establishes minimality and comeagrely many turbulent **points** even for these exceptional surfaces. In their Definition 7.3, a turbulent point is defined through interiors of closures of local orbits; generic turbulence additionally requires absence of a comeagre orbit. That missing condition cannot be omitted. For a simple diagnostic, the circle group acting on itself by translation is transitive and every point has a local orbit containing a neighborhood of itself, so every point is turbulent under that local definition. Yet its single orbit is the whole space.

## 6. Outcome and verification

Two approaches were investigated: extending the published circular-cover obstruction, and testing the disk-exhaustion model for a generic chain. The first is blocked by Lemma 3 and the exact source exclusions. The second is ruled out by Proposition 1, but does not control the remaining thin-chain orbits.

The complete original target remains **unsolved**, with two substantive approaches used. The partial conclusions above are self-contained Baire-category and nerve arguments with explicitly credited ray-density/minimality inputs. The checker supplies small exact finite diagnostics for the incidence and winding mechanisms and for the fundamental-group distinction. It does not claim that a finite graph or a numerical test proves an infinite-dimensional Baire-category theorem.
