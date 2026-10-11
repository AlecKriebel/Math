# Equality in the three-manifold lower bound: established-theorem reconstruction

Problem 30001703 / OWR-4798-030. Public authored edition dated 11 October 2026 UTC.

AI-assisted, unrefereed authored reconstruction and editorial acceptance. This edition is based on one source/proof reconstruction plus an internal AI review of that report; it does not claim a second independent mathematical audit, external human peer review, or formal proof-assistant certification. It is not a computational reproduction package.

## 1. Verdict and exact scope

For a **connected closed topological 3-manifold** M, let

\[
\Gamma(M)=\min_{|K|\cong M}\{f_1(K)-4f_0(K)+10\},\qquad
\beta_1(M;F)=\dim_F H_1(M;F),
\]

where K ranges over finite simplicial triangulations and F is any field. Then

\[
\Gamma(M)=10\beta_1(M;F)
\quad\Longleftrightarrow\quad
M\cong S^3\ \text{or a finite connected sum of }S^2\text{-bundles over }S^1.
\]

The two bundles are the orientable product S²×S¹ and the nonorientable twisted bundle S²~×S¹. The empty connected sum is S³. There are no additional connected topological types. A sum with k bundle summands has integral first homology Z^k and Gamma=10k. Consequently, equality for **one** field implies equality for **every** field. In particular, odd characteristic does not exclude the nonorientable bundle sums. No tightness, neighborliness, or vertex-minimality assumption belongs in this statement.

This is an established-result coverage conclusion, credited primarily to **Bhaskar Bagchi** and **Basudeb Datta–Satoshi Murai**, using the work of Walkup, Burton–Datta–Singh–Spreer, Bagchi–Datta, Murai–Nevo, and the cited topological foundations. It is not a new equality-classification theorem.

**Audit disposition:** the original connected-manifold question is covered by the established theorems. Their hypotheses, field conventions, invariant shift, minimum attainment, zero-handle case, and converse existence have been checked and reconstructed below. This is more than an abstract-level search, but it is **not a blanket full-paper acceptance or a fully foundational audit of every transitive theorem**. A literal error in the final Datta–Murai cutting definition is documented with a valid counterexample to that definition and an explicit local repair. The theorem-import conclusion and the repaired proof reconstruction are separate claims. No error in the classification statement was found.

This edition distributes authored mathematics and bounded verification metadata. It contains no source documents, source images, expanded gluing data, or executable code. No source-author code was executed in the underlying reconstruction.

## 2. Original question and notation reconciliation

The authenticated source is Ed Swartz, “f-vectors and three-manifold complexity,” in *Topological and Geometric Combinatorics*, Oberwolfach Report 08/2011, DOI 10.4171/OWR/2011/8, printed pp. 409–412. The relevant definition is on printed p. 409 / PDF p. 61; Theorem 3 and the question are on printed p. 410 / PDF p. 62. The retained official PDF is https://ems.press/content/serial-article-files/46323.

Swartz defines gamma(K)=f1−4f0+10 and Gamma(M)=min gamma(K). His Theorem 3 states the lower bound with “any coefficient field.” The following sentence asks exactly which manifolds other than multiple connected sums of S²×S¹ and S²∝S¹ satisfy equality. Here ∝ denotes the nonorientable S²-bundle over S¹. Thus the question concerns the minimum over all simplicial triangulations of a topological manifold, rather than the classification of a single triangulation, all f-vectors, or a neighborly minimizer.

The source question was checked at the exact PDF and printed-page locators above. The supplied problem formulation has the same mathematical target, but leaves connectedness and the zero-summand sphere implicit. Swartz already records Gamma(S³)=0 on p. 409. The mathematically correct closing statement must therefore include S³ explicitly or declare the empty-sum convention. Calling S³ an unexpected additional type would misread the question's context.

Bagchi uses a different gamma: gamma_B(M)=inf_K(f1(K)−4f0(K)). Hence

\[
\Gamma(M)=\gamma_B(M)+10.
\]

His Corollary 1.15 is gamma_B(M)≥10(beta1(M;F)−1), with equality exactly when M admits a 1-stacked triangulation. This is precisely the displayed Gamma bound after the shift; there is no off-by-ten issue.

### Connectedness is indispensable

For c connected components M_i, the same literal formula gives

\[
\Gamma(\bigsqcup_{i=1}^c M_i)
=\sum_i\Gamma(M_i)-10(c-1).
\]

This follows by splitting a finite triangulation into components and choosing componentwise minimizers. Two disjoint 3-spheres give Gamma=−10 while beta1=0. Therefore the unadjusted lower bound does not extend to arbitrary disconnected closed manifolds. The present conclusion is exactly the connected convention made explicit, not an attempted classification of disconnected equality accidents.

### Why the minimum exists

Every compact topological 3-manifold admits a finite simplicial triangulation (the standard 3-dimensional triangulation theorem, traditionally associated with Moise). If “closed triangulated” is part of the hypothesis, nonemptiness is already assumed. For any such K, Bagchi gives g2(K)≥10 beta1(M;F). Thus the set of values g2(K) is a nonempty set of integers bounded below. It has a least element, attained by an actual triangulation. No compactness of a space of triangulations, fixed vertex count, or limiting triangulation is needed. This also explains why Bagchi's finite infimum is attained.

## 3. Authenticated inputs and version control

The underlying source-inventory manifest has SHA-256

`0e957fba97c69c3deb8878d74caf56f722066e2f346c32019bdd1c02f977f3bb`.

All **105 listed members**, totaling **6,003,433 bytes**, were independently read, size-checked, and SHA-256-checked against that manifest during the underlying reconstruction. There were no mismatches. This is a scoped listed-member authentication, not a closed-inventory claim for the larger source collection. The public metadata records the inventory digest and match result without distributing its source contents.

The three controlling PDFs are:

- Swartz OWR 08/2011: 674,651 bytes; SHA-256 `5141477045060d0c901d6961a61379d8db0b4b594da0c9bb81f251f127aa48da`.
- Bagchi, arXiv:1405.5675 **v1**, 22 May 2014, 20 pages: 176,070 bytes; SHA-256 `5dec813c70675e11326f38400d2133354359d13e01c32563aa52b1f9612a8154`. The numbering used here is Theorem 1.14 and Corollary 1.15 in this retained version. https://arxiv.org/abs/1405.5675v1. The eventual journal paper is *European Journal of Combinatorics* 51 (2016), 69–83; its published text was not substituted silently for v1.
- Datta–Murai, **final published** *Electronic Journal of Combinatorics* 24(4) (2017), #P4.12, published 6 October 2017, 14 pages: 307,919 bytes; SHA-256 `f806646eebe640aa5b456c908edc8e8d38cb523c9431617ed1061d1b0d432abf`. https://doi.org/10.37236/6181. The controlling statements are Corollaries 4.6 and 4.9, Proposition 4.8, and Remark 4.10, pp. 10–11.

Supplementary PDFs were independently retrieved from the journal or arXiv: Burton–Datta–Singh–Spreer arXiv:1403.5862v3; Bagchi–Datta arXiv:1208.1389v2 and arXiv:1207.5599v2; Murai–Nevo arXiv:1209.0868v1; and the final Lutz–Sulanke–Swartz 2009 article. Their exact bytes, hashes, URLs, successful retrievals and one failed author-site request are retained. SOURCES.json records historical passage-reading, full retrieval, rendered pages, and actual visual inspection separately. None of these whole PDFs is represented as fully proof-audited.

## 4. Bagchi's equality argument, expanded in dimension three

Fix one arbitrary field F throughout. All first homology groups below use F. A triangulation of an actual closed 3-manifold satisfies the local homology-manifold hypotheses for every F. Bagchi's Theorem 1.14 imposes connectedness and closedness but **no orientability hypothesis**. The explicit sentence immediately after the theorem confirms this.

### 4.1 The separation estimate on vertex links

For a graph G on m vertices put

\[
s(G)=\sum_{A\subseteq V(G)}\frac{c(G[A])-1}{\binom m{|A|}},
\]

where c(empty)=0. This includes the empty-set contribution −1. For a complex, this is its sigma_0 in the conventions used here. It is a graph-connectivity statistic and is field independent.

Burton–Datta–Singh–Spreer, Theorem 1.1, prove that a triangulated 2-sphere L on m vertices satisfies

\[
s(L)\le\frac{(m-8)(m+1)}{20},
\]

with equality exactly for stacked 2-spheres. Bagchi v1 Theorem 1.4 is the same estimate because g0(L)=1 and g1(L)=m−4. The printed parenthetical “Butler et al” in Bagchi v1 is a naming typo: his reference [3] and the actual arXiv paper identify **Burton, Datta, Singh and Spreer**. The credit here follows the actual authors.

The required source proof was read through its degree-3, degree-4 and degree-5 induction (Lemma 2.8, Lemma 3.2, Corollary 3.3 and the proof of Theorem 1.1, PDF pp. 6–11). Its mechanism is as follows. Planarity supplies a vertex of degree at most five. Removing degree three reverses a starring move. Removing degree four fills a quadrilateral using a missing diagonal, then reconstructs the original sphere by starring and one edge flip. In minimum degree five, the planar six-vertex induced graph supplies two missing diagonals from one neighbor; filling the pentagon allows starring and two flips. The exact starring recurrence is s(new)=(m+2)s(old)/(m+1)+(m+2)/20. In the degree-four and degree-five cases, size-preserving injections from vertex subsets whose component count increases under the flips into those whose component count decreases prove nonincrease of s; strictness follows from an unmatched subset or from the smaller sphere being nonstacked. These are specific finite combinatorial arguments, not an orientability or Lefschetz assumption. The theorem is a named dependency, and the present report does not claim an independent exhaustive re-verification of every subset-injection subcase.

For K a closed triangulated 3-manifold, write m_v=f0(lk_K(v)). Bagchi's new definitions give

\[
\mu_0(K)=\sum_v\frac1{1+m_v},\qquad
\mu_1(K)=\sum_v\frac{1+s(\operatorname{lk}_K(v))}{1+m_v}.
\]

Therefore

\[
\mu_1-\mu_0
=\sum_v\frac{s(\operatorname{lk}_K(v))}{1+m_v}
\le\sum_v\frac{m_v-8}{20}
=\frac{f_1-4f_0}{10}
=-1+\frac{g_2(K)}{10}.
\]

The last computation uses sum_v m_v=2f1. Every summand has positive denominator. Hence equality holds precisely when **each vertex link** is a stacked 2-sphere. This is Bagchi Theorem 1.10 specialized without the general g-vector summation notation.

### 4.2 The Morse inequality and its equality condition

The other inequality is

\[
\beta_1(K)-1\le\mu_1(K)-\mu_0(K).
\]

Here is an explicit verification of the part of Bagchi Theorem 1.7 actually needed. For a uniformly random ordering of the vertices, let K_j be the induced complex on its first j vertices. Bagchi Lemma 2.6 says that mu_i is the average of sum_j beta_i(K_j,K_{j−1}). To check this, fix the added vertex v. The relative pair depends, by excision, only on the earlier neighbors of v in its link. A fixed subset A of those m_v neighbors precedes v with probability 1/((m_v+1) binom(m_v,|A|)), because the relative ordering of v and its neighbors is uniform. Empty earlier-neighbor sets contribute relative beta0=1 and relative beta1=0. Nonempty sets contribute relative beta0=0 and relative beta1=c(lk(v)[A])−1. Summing these formulas is exactly the new mu definition above, including its empty-set convention.

For A⊂B two induced complexes in a one-vertex step, exactness of the pair sequence gives

\[
\beta_1(B,A)-\beta_0(B,A)
=\beta_1(B)-\beta_1(A)-\beta_0(B)+\beta_0(A)
+\dim\ker[H_1(A)\to H_1(B)].
\]

Summing along the ordering telescopes the ordinary Betti numbers. Averaging yields the inequality, and equality means that every step has zero kernel for every ordering. Every induced subcomplex can appear in an ordering, so equality is equivalent to injectivity H1(Y)→H1(K) for every induced subcomplex Y. Conversely, injectivity into K implies injectivity at every step by composition. No field-orientability or neighborliness enters this argument. This is precisely the generalization of Bagchi–Datta Theorem 2.6 made possible by the new mu definition; using the old neighborly-only formula would be an incorrect import.

### 4.3 Equality produces an actual stacked filling

Combining the two bounds proves g2(K)≥10 beta1(K). If equality holds, then:

1. each link L_v is a stacked 2-sphere;
2. H1(Y)→H1(K) is injective for every induced subcomplex Y.

Local stackedness alone is insufficient in dimension three. Bagchi's pp. 18–19 supply the missing global argument. Define

\[
W=\{A\subseteq V(K):\text{every subset of }A\text{ of size at most }3\text{ is a face of }K\}.
\]

Then W and K have the same 2-skeleton. For each v, define B_v to be the clique complex of the graph of L_v. Bagchi–Datta Theorem 2.12 (d=2, k=1) says B_v is the stacked 3-ball with boundary L_v. In this special case this is also immediate by induction on starring moves: start with the tetrahedron; starring a boundary triangle adds one new vertex adjacent exactly to its three vertices, so its clique complex adds one tetrahedron along that triangle. This confirms both the ball property and the filling formula used here.

We claim lk_W(v)=B_v. Inclusion from left to right follows because every edge of a link face belongs to L_v. Conversely, take a face A of B_v. All its edges are in L_v. If a 3-element subset T⊂A were not a triangle of K, then K[T]=∂T is an induced 1-sphere. But v*∂T is a subcomplex of K because its three triangles correspond to edges of L_v. Thus H1(K[T])→H1(K) factors through a cone and is zero, contradicting its required injectivity, since H1(∂T;F)=F. All such triangles T must therefore lie in K, and all triangles of A∪{v} containing v lie in K as well. Hence A∪{v} is a face of W. The claim follows.

Every vertex link of W is consequently a homology 3-ball (indeed a stacked PL ball), so W is a homology 4-manifold with boundary. The identity lk_(∂W)(v)=∂B_v=L_v proves ∂W=K. Its 2-skeleton equals K's, so all its interior faces have dimension at least three. This is exactly 1-stackedness. The missing-triangle contradiction is why equality does more than impose stacked vertex links.

For the reverse implication, Bagchi explicitly invokes Murai–Nevo through his Theorem 1.13. In the retrieved Murai–Nevo v1, Theorem 3.1 gives h''_2(W)=0 for a stacked 4-manifold with boundary and Proposition 5.2 gives g-tilde_2(∂W)=h''_2(W). For a connected 3-dimensional boundary, g-tilde_2=g2−10 beta1, yielding equality. The proof uses nonnegativity of h'' and generalized Dehn–Sommerville relations; those algebraic foundations are not independently audited here. Their infinite-field convention can be met by extension to F(t), which preserves ranks of all finite simplicial boundary matrices. Alternatively, Section 5 below proves the reverse implication using the handle characterization and elementary face counts, avoiding that algebraic import in the assembled classification argument.

## 5. Datta–Murai: stacked fillings, handles and topology

### 5.1 What the final statements actually say

In Datta–Murai's convention H^4 consists of stacked triangulated 3-spheres followed by finitely many admissible combinatorial handle additions. Their bar-H^4 is the analogous class of 4-manifolds with boundary, starting with stacked 4-balls and using simplicial handle additions. The bar is essential: interior tetrahedra are retained in a simplicial handle addition, whereas the corresponding two boundary facets are removed in the closed-manifold operation.

Corollary 4.6 says that a connected closed homology d-manifold, d≥2, is stacked exactly when it belongs to H^(d+1). Proposition 4.8 restates Bagchi's equality theorem with his authorship explicit. Corollary 4.9 combines them in dimension three:

\[
K\in H^4\quad\Longleftrightarrow\quad K\text{ is stacked}
\quad\Longleftrightarrow\quad g_2(K)=10\beta_1(K;F).
\]

No orientability assumption appears in these three statements. Proposition 4.7 immediately above them does have an orientability assumption; it is the earlier Novik–Swartz theorem, and must not be substituted for Proposition 4.8.

### 5.2 Their proof chain, including its imports

Lemma 3.1 glues two homology balls along a boundary facet. Mayer–Vietoris gives acyclicity; vertex links are treated inductively; an orientable acyclic homology manifold with boundary is a homology ball by Poincare–Lefschetz duality (Lemma 2.1).

Lemma 3.2 proves that admissible facet identification preserves the homology-manifold and stacked properties. Its low-dimensional exact sequence says that the identification either joins two components, leaving beta1 unchanged, or leaves the manifold connected and increases beta1 by one. The admissibility condition lk(v)∩lk(psi(v))={empty face} is equivalent to there being no edge and no length-two path between each identified pair of vertices. This prevents unwanted face identifications.

Theorem 3.3 cuts along an interior codimension-one face σ whose proper faces are all in the boundary. Lemma 3.4 first shows that cutting a homology ball along such a face has two sides: cap its boundary by a cone to obtain a homology sphere, and apply simplicial Alexander duality to the complementary induced complexes. The complement has reduced H0 of dimension one. Facet-path connectedness shows that the two facets incident to σ lie on different sides. The two sides in every vertex link determine coherent labels for the incident faces; Lemma 3.5 supplies this compatibility. Duplicate the vertices of σ on one side, retaining separate σ and σ+ faces. Induction on dimension identifies the new links as either old links or one of the two ball pieces. Thus the cut complex is a homology manifold. It is either connected or has two components; gluing its two cut facets recovers the original. Stackedness is preserved, and the number of interior codimension-one faces decreases.

Theorem 4.5 now inducts on that number. The terminal connected case is a simplex. A separating cut is recombined using Lemma 4.3, which states closure of bar-H under simplicial connected union; a nonseparating cut is reversed by one handle addition. Lemma 4.2 identifies boundaries of bar-H members with H members, because stacked fillings and their boundaries have the same edges and hence the same admissibility test. These give Corollary 4.6, including dimension three. The proof deliberately works with homology manifolds during cutting; the caution on p. 6 about arbitrary PL cuts must not be erased. The resulting H members are nevertheless actual combinatorial manifolds, since the starting balls/spheres and the permitted operations are combinatorial.

Alexander duality, Poincare–Lefschetz duality, relative exact sequences, and facet-path connectivity of connected homology manifolds are the foundational imports in this reconstruction. No independent audit of Spanier's book or every proof cited for those foundations was done.

### 5.3 A literal defect in the published cutting definition and its local repair

This concerns the **final 2017 PDF, p. 7**, not an abstract or an earlier preprint. The rendered page was inspected. The authors define

R={a∈D: a∩σ≠empty, a is not a subset of σ}.

Their printed definition then forms R_x(k) from a∪{z_k}, subject to **a∈R** and a lying in the x-side of lk_D(z_k). This is incompatible with the subsequent claim R=X∪Y. Removing z_k from a face that meets σ only at z_k leaves a face disjoint from σ, excluded from R.

An explicit valid example uses σ={z1,z2,z3,z4} and the stacked 4-ball D generated by the two 4-simplices σ∪{x} and σ∪{y}. Their common tetrahedron σ is interior and every proper face of σ is on the boundary. The edge e={z1,x} belongs to R. To obtain e in printed R_x(1), the precursor would have to be {x}, since link faces cannot contain z1. But {x} is not in R. No R_x(k) or R_y(k) with k≠1 can contain e because those output faces contain z_k. Also it is not in R_y(1). Thus e is omitted. On this example the literal Definition 3.6 can even retain a facet without all its required relabeled subfaces, so the error is not resolved by the empty-face convention.

The local repair consistent with Lemma 3.5 and the intended construction is

R_x(k)={a∈R: z_k∈a and a\{z_k} belongs to the x-side of lk_D(z_k)}.

Define R_y(k) similarly. Equivalently, keep the authors' a∪{z_k} output but require **a∪{z_k}∈R**, rather than a∈R. The double-link argument in Lemma 3.5 now makes labels independent of which z_k in a∩σ is used. Faces not contained in σ inherit a common side from any incident σ vertex; taking subfaces preserves that side whenever the subface still meets σ outside σ itself. Duplicating σ on the x-side therefore yields a simplicial complex. The proof's three link cases then apply: vertices away from σ have isomorphic old links, z_k+ has the x-side ball as link, and z_k has the y-side ball. The two copies have no common neighbor under the gluing correspondence, so the inverse gluing is admissible. This restores the stated cutting argument.

The underlying authored finite witness check verifies the omitted edge, failure of closure under subfaces for the literal cut, and correct partition and cut for the repaired definition on this valid two-simplex example. It is evidence for the textual defect, not a computational proof of the general theorem. There is no claim that this typo or repair is first noticed here. No source author was contacted.

A second citation-location issue is harmless: Remark 4.10 points to Lutz–Sulanke–Swartz “[13, Section 3]”; the relevant topological-type paragraph and handle face-count formulas in the retrieved final 2009 PDF are in **Section 2, pp. 3–4**. Section 3 discusses lower bounds and tight-neighborly triangulations. The correct passage was read and visually checked, so the topology import does not rest on following the incorrect section number blindly.

### 5.4 From handles to the claimed topological types

A stacked 3-sphere is S³. A combinatorial handle addition removes interiors of two disjoint tetrahedra and identifies their boundary 2-spheres by the prescribed PL map. This is the usual 3-dimensional 1-handle surgery on the boundary of a 4-dimensional ball/handlebody. Topologically it introduces one S²-bundle-over-S¹ summand; the two possibilities are distinguished by orientation. Repetition gives only finite connected sums of these bundles. This is the standard handle-topology fact used by Datta–Murai Remark 4.10 and explicitly recorded by Lutz–Sulanke–Swartz pp. 3–4, not a conclusion from a free fundamental group alone.

In conventional normal form, the orientable possibilities are #(k)(S²×S¹), while the nonorientable ones may be written #(k)(S²~×S¹), k≥1. Allowing mixed summands is equivalent; an existing twisted summand permits the usual handle-orientation change. The classification needed for the question can simply use arbitrary finite sums of the two bundles and does not depend on proving uniqueness of that normal form.

For an H^4 member obtained with k handles, each handle changes f0 by −4 and f1 by −6, hence changes g2 by +10. The starting stacked sphere has g2=0: the boundary of a 4-simplex has (f0,f1)=(5,10), and starring a tetrahedron adds one vertex and four edges, preserving g2. Topological handle addition increases H1 by a free Z summand in this setting. Hence H1=Z^k and g2=10k over every field. This proves the reverse stacked⇒equality implication through Corollary 4.6 without using Murai–Nevo's commutative-algebra proof.

## 6. Converse existence, not just a restriction on types

The preceding implication says equality permits no other types. To establish the full “if and only if” for topological manifolds, one must also realize every allowed type by an equality triangulation.

Here is a direct standard stacked construction. Build a stacked 4-ball with facets

\[
F_i=\{i,i+1,i+2,i+3,i+4\},\quad i=0,\ldots,11.
\]

Each successive 4-simplex attaches along the current boundary tetrahedron {i,i+1,i+2,i+3}. Its boundary K is a stacked 3-sphere. Its graph has an edge exactly between vertices whose labels differ by at most four. The tetrahedra σ={0,1,2,3} and τ={12,13,14,15} are boundary facets. Every vertex of σ is at graph distance at least three from every vertex of τ, so **every** bijection σ→τ is admissible. Bijections of opposite parity give the two orientation types of a single handle. The resulting triangulations represent S²×S¹ and S²~×S¹, respectively. Before gluing, f0=16 and f1=54; afterwards f0=12 and f1=48, so g2=10.

Take simplicial connected sums of any desired k of these building blocks. Gluing along tetrahedra changes the combined f0 by −4 and f1 by −6. Therefore

\[
g_2(K_1\#K_2)=g_2(K_1)+g_2(K_2).
\]

Mayer–Vietoris (or van Kampen followed by abelianization) gives H1(K1#K2;Z)=H1(K1;Z)⊕H1(K2;Z), since the gluing sphere is S². Thus every chosen k-fold sum has a triangulation with g2=10k, and Bagchi's lower bound makes its minimum exactly 10k. For k=0, use the boundary of the 4-simplex, giving Gamma(S³)=0.

The underlying authored finite example checker exhaustively checks the 24 endpoint bijections of this one fixed 16-vertex stacked sphere: admissibility, resulting face counts, closed surface vertex links with Euler characteristic two, orientability, and first Betti numbers over F2 and F3. These finite checks are supplementary controls on the explicitly supplied construction, not a substitute for its topological argument or a census of all triangulations.

## 7. Coefficients, orientability, and excluded overclaims

- F is an arbitrary field, fixed while applying a theorem. First Betti numbers of general 3-manifolds can vary with characteristic because H1 may have torsion. No claim of field independence is made for arbitrary manifolds.
- Equality for a single F forces membership in H^4 and hence integral H1=Z^k. Field independence follows **after** classification. There is no room for a torsion-only counterexample whose equality appears in just one characteristic.
- Every actual closed 3-manifold is F2-orientable. In odd characteristic or characteristic zero, nonorientable manifolds are not F-orientable, but Bagchi Theorem 1.14 does not require that property. Nonorientable bundle sums remain valid equality cases for those fields.
- “Stacked” and “locally stacked” are different in dimension three. The induced-H1-injectivity and canonical-filling step must not be omitted.
- Equality is not the same as tight-neighborliness. A triangulation with g2=10 beta1 need not have a complete graph or the fewest possible vertices. Subdividing a facet of an equality triangulation preserves g2 and the manifold, and generally destroys neighborliness.
- Datta–Murai Section 5 addresses tightness and extra orientability/neighborliness conditions. It is not required for this question. No acceptance of all Section 5 statements is implied here.
- No higher-dimensional classification, full f-vector classification, Gamma additivity for arbitrary connected sums, or computation of Gamma outside this equality class is asserted.

## 8. Acceptance levels, remaining imports, and stopping condition

### Established-theorem coverage audit: passes for the connected question

The exact hypothesis and conclusion match is complete: actual triangulation ⇒ homology-manifold hypotheses; arbitrary fixed field; equality iff stacked (Bagchi); stacked iff H^4 (Datta–Murai); H^4 topology; attainment of the discrete minimum; and existence of equality triangulations for every listed type. The 2011 open question is covered by these later established results; this is a credited source-status conclusion, not a new theorem.

### Reconstructed argument: complete relative to identified standard imports

Sections 4–6 explain the actual proof chain rather than copying abstracts. They include the dimension-three Morse equality calculation, global filling argument, handle induction, exact invariant passage, and converse construction. The printed cutting-definition defect is repaired explicitly, and the theorem's use is not disguised as a literal defect-free reproduction.

### Full foundational or full-paper audit: not claimed

The residual imported foundations and unevaluated transitive proofs are explicitly:

1. The separation-index theorem of Burton–Datta–Singh–Spreer. Its statement, conventions, dependencies and case structure were inspected; every subset injection was not independently formalized or exhaustively audited for arbitrary spheres.
2. Simplicial Alexander duality and Poincare–Lefschetz duality for homology manifolds, as used in Datta–Murai Lemmas 2.1 and 3.4; connected facet-path facts and elementary PL ball gluing/handle topology. Their standard precise forms are used, but Spanier and the complete foundational literature were not read.
3. The triangulability of compact topological 3-manifolds if triangulability is not taken as part of the problem hypothesis.
4. In Bagchi's **original reverse proof**, Murai–Nevo's h'' nonnegativity and generalized Dehn–Sommerville imports. Their theorem-level match and relevant proof passages were checked, but Schenzel/Novik–Swartz/Grabe proofs were not fully audited. The assembled converse in this report instead uses the independently explained handle counts, so this item does not remain a necessary import for that route.

None of these is presented as a newly discovered unresolved mathematical gap. The actual local printed-definition error is separately evidenced in Section 5.3. If the required acceptance criterion is a literal, independently verified, foundational proof of every cited result, the present packet does not meet it and must not be labeled a full proof audit. If the criterion is a source-faithful established-theorem coverage audit of the exact connected question, it does meet it. No worldwide novelty or exhaustive-literature completeness claim follows.

## 9. Integrity and reproducibility

During the underlying reconstruction, only the authored example checker, inventory verifier, and standard PDF-text/rendering tools were executed. No code from a source author or downloaded paper was run. Examples are finite consistency checks; integrity controls authenticate bytes, not the truth of mathematics.

The retained reconstruction inventory contains 65 payload files, with an externally pinned manifest. Its historical integrity verifier checked exact file and directory membership, byte sizes and SHA-256 digests; positive runs and deliberate negative controls were performed under normal Python, -O and -OO without relying on assert. VERIFICATION.json distinguishes those historical checks from this public editorial preparation. Original source bodies and the expanded example records are not distributed here.

The public MANIFEST.json lists exactly the eight edition members and hashes the seven other files, excluding itself to avoid self-reference. An external preparation seal pins the complete local preparation, and the proposed publication metadata separately pins the public manifest. Strict additions-only patch replay and Git-native blob/tree checks establish the proposed repository boundary. These controls are not immutable-storage guarantees, cryptographic authorship, human review, or proof verification.

## References

1. Ed Swartz, “f-vectors and three-manifold complexity,” OWR 08/2011, printed pp. 409–412; definition/question pp. 409–410. https://ems.press/content/serial-article-files/46323.
2. Bhaskar Bagchi, *The mu vector, Morse inequalities and a generalized lower bound theorem for locally tame combinatorial manifolds*, arXiv:1405.5675v1 (2014), especially Theorems 1.4, 1.7, 1.10, 1.13, 1.14, Corollary 1.15 and pp. 16–19. https://arxiv.org/abs/1405.5675v1.
3. Basudeb Datta and Satoshi Murai, *On Stacked Triangulated Manifolds*, EJC 24(4) (2017), #P4.12, Sections 2–4. https://doi.org/10.37236/6181.
4. Benjamin A. Burton, Basudeb Datta, Nitin Singh and Jonathan Spreer, *Separation index of graphs and stacked 2-spheres*, arXiv:1403.5862v3; JCTA 136 (2015), 184–197. https://arxiv.org/abs/1403.5862v3.
5. Bhaskar Bagchi and Basudeb Datta, *On k-stellated and k-stacked spheres*, arXiv:1208.1389v2; Discrete Math. 313 (2013), 2318–2329, Lemma 2.11 and Theorem 2.12. https://arxiv.org/abs/1208.1389v2.
6. Bhaskar Bagchi and Basudeb Datta, *On stellated spheres and a tightness criterion for combinatorial manifolds*, arXiv:1207.5599v2; EJC 36 (2014), 294–313, Lemma 2.5 and Theorem 2.6. https://arxiv.org/abs/1207.5599v2.
7. Satoshi Murai and Eran Nevo, *On r-stacked triangulated manifolds*, arXiv:1209.0868v1; J. Algebraic Combin. 39 (2014), 373–388, Theorem 3.1 and Proposition 5.2. https://arxiv.org/abs/1209.0868v1.
8. Frank H. Lutz, Thom Sulanke and Ed Swartz, *f-Vectors of 3-Manifolds*, EJC 16(2) (2009), #R13, especially Section 2, pp. 3–4. https://www.combinatorics.org/ojs/index.php/eljc/article/download/v16i2r13/pdf/.
9. David W. Walkup, *The lower bound conjecture for 3- and 4-manifolds*, Acta Math. 125 (1970), 75–107. Credited through the inspected sources; full original not retrieved or audited here.
