# A bounded-cutset consequence of the Häggström–Mester construction

Status at writing: independently reconstructed antecedent implication, awaiting separate adversarial review. This is not asserted to be a theorem stated in the cited paper, a historical priority certificate, or an edit to the frozen author proof. It analyzes what the published construction implies. No author proof-search budget is consumed or reset.

## 1. Source facts and notation

Häggström–Mester (HM), *Some two-dimensional finite energy percolation processes*, ECP 14 (2009), printed pp44–45, builds two interlaced, subdivided, one-ended trees from the planar UST and its complementary dual tree. In its site configuration \(\widehat X\), the open induced graph is the subdivided primal tree and the closed induced graph is the subdivided dual tree. HM flips each site independently, conditional on these trees, with probability \(2^{-b(x)-1}\), where \(b(x)\) counts the finite vertices separated from its monochrome infinity by removing \(x\). It proves finite energy and survival for both colors. Printed p46 explicitly discusses threshold one for the *pre-flip* configuration. The post-flip threshold is the deduction below, not a quoted source result.

Source identity: published EMIS final PDF, 165957 bytes, SHA-256 `ddbf7afb7874e41839426dc0158d473ae369ae593334f77021dbdef26f2c0c1d`. Primary URL: <https://www.maths.tcd.ie/EMIS/journals/EJP-ECP/article/download/1446/1446-4872-1-PB.pdf>. Printed pp44–46 were read as full pages, extracted and visually checked. The arXiv v1 and final agree on these ingredients; no general identity of their full texts is asserted.

## 2. A finite-path summation fact

Let \(R\) be a locally finite one-ended tree. Orient each edge toward its unique end. For a vertex \(x\), its finite past, including \(x\), has cardinality \(b(x)+1\), where \(b(x)\) is the number of finite vertices separated by removing \(x\).

Along an oriented path toward the end, \(b\) increases strictly: the next past contains the previous past and also the next vertex. A finite simple path is the union of two such increasing arms meeting at their common ancestor; either arm may be empty. Consequently every nonnegative integer occurs as \(b\) at most twice along that path. Thus for every finite simple vertex path \(P\subset R\),

\[
 \sum_{x\in P}2^{-b(x)-1}\le 2\sum_{m\ge0}2^{-m-1}=2. \tag{A}
\]

For edges, write \(s_R(e)\ge1\) for the finite-side cardinality of \(R-e\). The same two-arm argument gives

\[
 \sum_{e\in P}2^{-s_R(e)}\le2\sum_{m\ge1}2^{-m}=2 \tag{B}
\]

for every finite simple edge path. No distributional or geometric assumption on \(R\) is involved.

## 3. The primal finite-side boundaries are fundamental dual cycles

Fix a one-ended primal spanning tree \(T\) on the square lattice whose complementary dual edges form a one-ended spanning tree \(T^*\). Fix a primal vertex \(v\), enumerate its ray edges toward infinity by \(t_n\), and let \(S_n\) be the finite component of \(T-t_n\).

The \(S_n\) are strictly increasing finite sets and exhaust the primal lattice. Indeed any other vertex has a ray that coalesces with the ray from \(v\), and eventually lies on the finite side of \(t_n\). Their boundary edges escape every finite edge set. Every primal boundary edge other than \(t_n\) is outside \(T\), so its dual belongs to \(T^*\).

The dual edge set of \(\partial S_n\) is the fundamental cycle obtained by adding \(t_n^*\) to \(T^*\). Here is a direct verification of the point that must not be silently assumed. A finite primal cut has even dual degree and is a union of dual cycles. It contains only one edge outside the acyclic graph \(T^*\), namely \(t_n^*\). Therefore it cannot contain a second cycle or a separate even-degree component. It is exactly the unique simple cycle consisting of \(t_n^*\) and the finite \(T^*\)-path \(P_n^*\) between its endpoints. Equivalently, \(S_n\) and its complement are connected through their respective components of \(T-t_n\), so the cut is a bond and its planar dual is a cycle.

Under HM's scale-two site representation, this becomes a simple fine-lattice Jordan cycle \(C_n\). Every site of the subdivided path \(P_n^*\) is initially closed, while the missing dual edge contributes precisely one initially open midpoint, representing \(t_n\). The two dual endpoint sites are included in the closed path. Any nearest-neighbor site path from an interior vertex to infinity meets \(C_n\); grid edges cannot cross a grid polygon except at its vertices. The cycles escape every finite set: eventually every coarse primal vertex around each fixed fine site is in \(S_n\). Thus each fine-lattice vertex is eventually enclosed.

## 4. Uniformly bounded mean implies infinitely many bounded open cutsets

Condition on the two initial trees and on HM's parity shift. Let \(K_n\) be the number of finally open sites on \(C_n\). The sole initially open bridge midpoint contributes at most one. Every other cycle site is on the finite closed-tree path and becomes open with its HM flip probability. By (A),

\[
 \mathbb E[K_n\mid T,T^*,\text{shift}]\le1+2=3. \tag{C}
\]

Independence between different cycles is neither true nor needed. Conditional Fatou gives

\[
 \mathbb E[\liminf_n K_n\mid T,T^*,\text{shift}]\le
 \liminf_n\mathbb E[K_n\mid T,T^*,\text{shift}]\le3.
\]

Hence \(\liminf_n K_n<\infty\) almost surely. For almost every output there is a finite integer \(L\), depending on the output and root, such that infinitely many cycles have at most \(L\) finally open sites. Because the cycles escape finite sets, these may be selected recursively to be vertex-disjoint. Their finally open sites separate any finally open path from the root to infinity. This proves a structural output property, not an annealed estimate at a chosen thinning parameter.

Fix such a realized output. For independent site thinning with any \(p<1\), each selected cutset of size at most \(L\) has probability at least \((1-p)^L\) to be deleted completely. Disjointness makes those events independent. The probability to cross the first \(k\) cutsets is at most

\[
 [1-(1-p)^L]^k\longrightarrow0.
\]

An empty cutset already prevents an infinite path. Countability of roots gives no infinite site-thinned component. The same structural property works for every \(p<1\) after the output is fixed. HM's survival proves that the unthinned graph percolates. Therefore the *actual post-flip HM open graph* has quenched internal site critical probability one. By interchanging colors, the closed graph does too. HM Lemma 3.1 (printed p45) transfers the threshold-one statement to internal Bernoulli bond percolation on these bounded-degree graphs.

## 5. What the internal site/bond equivalence does not prove

The graph-theoretic equivalence of internal thresholds does not convert the *external site law* into a finite-energy bond law on the original lattice. Declaring a bond open iff both endpoint sites are open can fail deletion tolerance. Even for iid sites, seeing another open incident bond at each endpoint forces the bond between those endpoints to be open. This positive-probability conditioning event makes its conditional deletion probability zero. A priority argument must not identify that induced bond law with the BHS target.

## 6. An exact midpoint projection to a bond law

The stronger reduction uses the published HM probabilities exactly. First fix the parity phase, for example the unshifted encoding with primal vertices at \(2\mathbb Z^2\). Observe only the final states of the edge-midpoint sites. Reinterpret the midpoint of \(2u\) and \(2v\) as the nearest-neighbor coarse bond \(\{u,v\}\). This is a coordinate marginal of the fixed-phase HM site construction. It is not the induced graph on the finally open sites: the final states of the coarse vertex sites are ignored.

If \(x\) is the midpoint of a primal tree edge whose coarse finite side has \(s\) vertices, removing \(x\) from the subdivided primal tree separates \(s\) vertex-sites and \(s-1\) internal edge-midpoint sites. Hence

\[
 b(x)=2s-1,\qquad 2^{-b(x)-1}=4^{-s}. \tag{D0}
\]

The same identity applies to a non-primal midpoint viewed as an edge of the subdivided dual tree. Thus the exact conditional coarse bond law of the projected midpoint coordinates is

\[
 \mathbb P(e\in X\mid T)=
 \begin{cases}
 1-4^{-s_T(e)},&e\in T,\\
 4^{-s_{T^*}(e^*)},&e\notin T.
 \end{cases} \tag{D}
\]

No rate modification or new random field has been introduced. Conditional independence is inherited from HM's independent site flips by taking their midpoint coordinates. All parameters lie strictly between zero and one. Along each primal ray the sum of deletion probabilities is at most \(\sum_{m\ge1}4^{-m}=1/3\), so eventually retained ray tails exist almost surely and the projected bond output percolates.

For each primal finite side \(S_n\), the non-tree boundary edges have duals along the single path \(P_n^*\). The two-arm counting argument, with \(4^{-s}\) in place of \(2^{-s}\), gives

\[
 \mathbb E[|\partial_X S_n|\mid T]\le1+2\sum_{s\ge1}4^{-s}=5/3. \tag{E}
\]

The same Fatou and escaping-boundary argument yields infinitely many disjoint edge cutsets of bounded size, and hence quenched internal bond critical probability one for every fixed good output. Internal site threshold one follows directly by deleting the endpoints of selected separated edge cutsets (or by the bounded-degree threshold equivalence).

Marginal finite energy follows from conditioning first on the tree: if \(r_T(e)\in(0,1)\) is the parameter in (D) and \(\mathcal F_e\) records all other output bonds, then

\[
 \mathbb P(X_e=1\mid\mathcal F_e)=\mathbb E[r_T(e)\mid\mathcal F_e]\in(0,1)\quad\text{a.s.}
\]

The fixed phase is not an obstacle to coarse-bond symmetry. Coarse translations correspond to even fine-lattice translations, and coarse signed coordinate permutations act on the same primal/dual encoding. The UST input and the primal/dual past-size rule are equivariant under every coarse square-lattice automorphism. The output therefore has full automorphism invariance as a bond law on the coarse lattice, which is isomorphic to \(\mathbb Z^2\).

Pemantle's input law is mixing (arXiv v1 p21 explicitly notes mixing of all orders from tail triviality). The product with independent midpoint marks is mixing, and equivariant factors inherit it. There is no random parity phase in this fixed-phase projected bond law. No mixing assertion is made here for HM's original randomly shifted site process, whose global phase requires separate consideration. Translation-invariant finite energy plus percolation gives a unique infinite component by the classical uniqueness result cited in HM p43. This last uniqueness assertion is not needed to answer the bare existence question.

Thus the exact BHS existence target in dimension two follows from an exact coordinate projection of a fixed phase of HM's published construction, together with the bounded-cutset argument above. This is a source-consequence deduction, not a theorem statement located in HM and not a historical priority certificate. The alternative rates \(2^{-s}\) also obey the same proof, but are only a changed-rate adaptation and are unnecessary to establish this stronger antecedent relation.

## 7. Boundary of this antecedent implication

The planar argument depends on a one-ended complementary dual tree. It does not provide the frozen author's construction on all \(\mathbb Z^d\), \(d\ge2\), or the dimension-free maximum-of-primal-past insertion rule. It gives bounded cutsets along a subsequence, not the author's eventually singleton cut boundaries along every ray. Timár's theorem supplies general one-ended inputs, but supplies no planar dual object in higher dimensions. No all-dimensional antecedent is established here. No new result is claimed for uniform finite energy.
