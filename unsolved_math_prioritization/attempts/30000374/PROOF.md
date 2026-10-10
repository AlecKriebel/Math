# Analytic complexity of ordinal colored dense order preorders

## Result and scope

Write \(R_\alpha\) for the preorder in Camerlo's Problem 5 in the Oberwolfach report *Universal analytic preorders*, for a countable ordinal \(\alpha<\omega_1\). The colors have their usual ordinal order. On \(X_\alpha=\alpha^{\mathbb Q}\),
\[
 \varphi R_\alpha\psi\quad\Longleftrightarrow\quad
 \exists g:\mathbb Q\longrightarrow\mathbb Q\;
 [g\text{ is strictly increasing and dense in its convex hull}
 \ \&\ \forall q\;\varphi(q)\leq\psi(g(q))].
\]
We use the product of the discrete topology on the countable set \(\alpha\). This presents the stipulated standard Borel structure.

**Theorem 1.** The following statements hold.

1. \(R_0\) is the empty preorder on the empty space. \(R_1\) is the one point reflexive preorder. These are different Borel degrees.
2. For every \(2\leq\alpha<\omega_1\), \(R_\alpha\), viewed as a subset of \(X_\alpha^2\), is \(\boldsymbol\Sigma^1_1\)-complete and is not Borel. More strongly, there is a fixed binary valued \(\varphi_*\) such that
   \[
   \{\psi\in X_\alpha:\varphi_*R_\alpha\psi\}
   \]
   is \(\boldsymbol\Sigma^1_1\)-complete. A single continuous reduction from ill founded trees works for every such \(\alpha\).
3. If \(\alpha\leq\beta<\omega_1\), inclusion of colors continuously reduces \(R_\alpha\) to \(R_\beta\). In particular,
   \[
   R_0<_B R_1<_B R_2\leq_B R_\alpha\qquad(2\leq\alpha<\omega_1).
   \]
4. For every nonzero \(\alpha\), there is a least element and a greatest equivalence class. The least equivalence class consists just of the constant zero coloring. A coloring \(\psi\) is greatest exactly when some nonempty real open interval \(I\) satisfies
   \[
   \forall\gamma<\alpha\quad
   \{q\in I\cap\mathbb Q:\psi(q)\geq\gamma\}\text{ is dense in }I.
   \tag{1}
   \]
   Consequently the greatest class is \(\boldsymbol\Sigma^0_3\) (an upper bound, not a completeness assertion). For \(\alpha=\delta+1\), condition (1) says simply that the points of color \(\delta\) are dense in some nonempty interval.

Part 2 is completeness for **sets under continuous many one reduction**. It is not a claim that \(R_\alpha\) is a universal analytic **preorder** under Borel reductions of binary relations. This proof does not decide the exact preorder degrees for \(\alpha\geq2\), their possible strict increases or collapses, or analytic preorder universality. Thus it gives an all parameter pointclass theorem and some degree comparisons, not a full solution of the source's classification problem.

## Dense maps and rational preserving extensions

A strictly increasing \(g:\mathbb Q\to\mathbb Q\) is dense in its convex hull precisely when
\[
 \forall a,b,r,s\in\mathbb Q\quad
 [g(a)<r<s<g(b)\ \Longrightarrow\ \exists t\in\mathbb Q\;(r<g(t)<s)].
 \tag{2}
\]
By Marcone and Rosendal, Definition 4.1 and Proposition 4.2, this is equivalent to being the restriction of a continuous strictly increasing embedding \(h:\mathbb R\to\mathbb R\) with \(h(\mathbb Q)\subseteq\mathbb Q\). Its real image is an open interval, possibly proper or unbounded. The extension is obtained by taking suprema of rational initial segments. Strict increase follows by placing two rationals between any two real arguments; (2) excludes jumps. Conversely a continuous strictly increasing real map sends rational arguments densely into its open real image.

Neither this equivalence nor the definition requires \(g\) to be onto \(\mathbb Q\). For example an increasing order isomorphism \(\mathbb Q\to(0,1)\cap\mathbb Q\) is a valid witness. Merely requiring continuity on \(\mathbb Q\) is insufficient: the map
\[
 g(q)=\begin{cases}q,&q<\sqrt2,\\q+1,&q>\sqrt2\end{cases}
\]
is a continuous increasing embedding of \(\mathbb Q\) into itself but has a gap in its range between \(\sqrt2\) and \(\sqrt2+1\), inside its convex hull.

We will need the following precise extension lemma.

**Lemma 2.** Suppose \(K,L\subset\mathbb R\) are nonempty compact nowhere dense sets, and \(e:K\to L\) is an increasing order homeomorphism such that
\[
 e(K\cap\mathbb Q)\subseteq\mathbb Q.
 \tag{3}
\]
Then there is an increasing homeomorphism \(h:\mathbb R\to\mathbb R\) extending \(e\) with \(h(\mathbb Q)\subseteq\mathbb Q\).

**Proof.** An order isomorphism of the compact sets matches consecutive endpoint pairs, and hence matches the components of \(\mathbb R\setminus K\) with the components of \(\mathbb R\setminus L\), including the two exterior rays. In each matched pair \(J,J'\), the orders \(J\cap\mathbb Q\) and \(J'\cap\mathbb Q\) are countable dense linear orders without endpoints. Choose an increasing bijection between them by back and forth. It extends by Dedekind completion to an increasing homeomorphism \(J\to J'\) with the prescribed endpoint limits. Combine these maps with \(e\). The resulting map is strictly increasing and onto \(\mathbb R\), so it is a homeomorphism. Rational points in complementary intervals have rational images by construction; rational points of \(K\) have rational images by (3). Notice that equality \(e(K\cap\mathbb Q)=L\cap\mathbb Q\) is not needed. Some irrational points of \(K\) may map to rational points of \(L\). \(\square\)

## A fixed compact source

Fix an enumeration \((q_i)_{i\in\mathbb N}\) of \(\mathbb Q\). Recursively choose, for every finite binary string \(u\), a closed nondegenerate rational endpoint interval \(I_u\) and a rational marker \(a_u\in\operatorname{int}I_u\), as follows. Start with \(I_\varnothing=[0,1]\). Having chosen \(I_u,a_u\) at depth \(n=|u|\), choose \(I_{u0}\) strictly to the left of \(a_u\) and \(I_{u1}\) strictly to its right, both inside \(\operatorname{int}I_u\). Require both child intervals to have diameter at most \(2^{-(n+1)}\) and to avoid \(q_0,\ldots,q_n\). This is possible since each side contains an open interval and only finitely many points are forbidden. Choose the next markers in the child interiors.

Let
\[
 A=\{a_u:u\in2^{<\omega}\},\qquad
 p_b=\bigcap_n I_{b\upharpoonright n}\quad(b\in2^\omega),\qquad
 P=\{p_b:b\in2^\omega\}.
\]
Intersections denote their unique points. The interval diameters tend to zero, and siblings are separated, so \(b\mapsto p_b\) is a continuous injection of Cantor space. Every \(p_b\) is irrational, because \(q_i\) is excluded at every depth exceeding \(i\). All markers are distinct rational points. Put \(K=A\cup P\).

The set \(K\) is compact and equals \(\overline A\). Indeed an accumulation of markers of unbounded depth has, by successive binary subsequence selection, a branch limit; conversely the markers along each branch converge to its limit. Bounded depth gives only finitely many markers. Each \(a_u\) is isolated in \(K\), since its two child intervals are positively separated from it, and the other subtrees are separated from \(I_u\). It follows that
\[
 K\cap\mathbb Q=A,
 \tag{4}
\]
and \(K\) is uncountable. It is nowhere dense: if it contained a nonempty interval, the density of \(A\) in \(K\) would give an isolated point of \(K\) inside that interval, a contradiction. Define \(\varphi_*:\mathbb Q\to2\) to be the characteristic function of \(A\).

## Coding arbitrary trees by rational markers

Let \(\mathrm{Tr}\) be the closed subspace of \(2^{\mathbb N^{<\omega}}\) consisting of prefix closed trees, with the empty tree allowed. Let \(\mathrm{IF}\) be its set of trees with an infinite branch. This is a complete analytic set. For completeness, if an analytic \(E\subseteq\mathbb N^\mathbb N\) is represented as the projection of the body of a tree \(S\) on pairs of finite sequences of equal length, then
\[
 x\longmapsto T_x=\{s:(x\upharpoonright |s|,s)\in S\}
\]
is continuous and \(x\in E\) exactly when \(T_x\) has a branch. This is the standard tree representation of analytic sets; see also Foreman, Rudolph and Weiss, Theorem 4.

Independently of \(T\), define rational intervals \(J_{s,u}\) and rational markers \(r_{s,u}\) for pairs \((s,u)\in\mathbb N^n\times2^n\). Start with \(J_{\varnothing,\varnothing}=[0,1]\). If \(J_{s,u}=[l,r]\), set
\[
 c=r_{s,u}=(l+r)/2,\qquad d=(r-l)/2.
\]
For every \(k\in\mathbb N\), set
\[
 \begin{aligned}
 J_{s^\frown k,u^\frown0}
   &=[c-d2^{-(2k+1)},\ c-d2^{-(2k+2)}],\\
 J_{s^\frown k,u^\frown1}
   &=[c+d2^{-(2k+2)},\ c+d2^{-(2k+1)}].
 \end{aligned}
 \tag{5}
\]
All these child intervals lie strictly inside the parent and are pairwise disjoint. The zero child is left of the parent marker, the one child is right of it. Each child diameter is at most one eighth of the parent diameter. As \(k\to\infty\), both children converge to the parent marker. The family of all child intervals has no other external accumulation point. Markers at distinct nodes are distinct, because a parent marker lies outside all its child intervals and incomparable nodes have disjoint intervals.

For \(T\in\mathrm{Tr}\), let
\[
 B_T=\{r_{s,u}:s\in T,\ u\in2^{|s|}\},\qquad
 \psi_T=\mathbf1_{B_T}:\mathbb Q\to2.
 \tag{6}
\]
The map \(T\mapsto\psi_T\) is continuous. A rational coordinate which is not one of the fixed markers is constantly zero. A coordinate equal to the unique marker \(r_{s,u}\) has value one exactly when \(s\in T\), a clopen coordinate test.

**Lemma 3.** If \(T\) is well founded, then \(\overline{B_T}\) is countable. In fact \(B_T\) itself is compact.

**Proof.** The empty case is immediate. Otherwise consider \(x\in\overline{B_T}\), starting in the root interval. If \(x\) is the root marker there is nothing to prove. If it is not, (5) shows that \(x\) lies in one child interval and belongs to the closure of the markers in that child's subtree. To justify this last assertion, near a point other than the parent marker only finitely many child intervals are relevant, and each such interval is separated from all the others and from the parent marker. A child with no markers cannot contribute a closure point. Prefix closure of \(T\) ensures the selected child node belongs to \(T\).

Repeat inside that child. Either the process ends at a marker \(r_{s,u}\in B_T\), or it determines nested nodes \((s_n,u_n)\) of every length with \(s_n\in T\) and \(s_n\subset s_{n+1}\). The second alternative is an infinite branch of \(T\) and is impossible. Thus every closure point belongs to \(B_T\). This set is closed in \([0,1]\) and countable. \(\square\)

**Lemma 4.** If \(T\) has a branch \(a\in\mathbb N^\mathbb N\), there is a compact nowhere dense \(K_a\subseteq\overline{B_T}\) and an increasing order homeomorphism \(e_a:K\to K_a\) such that
\[
 e_a(a_u)=r_{a\upharpoonright |u|,u}\in B_T.
 \tag{7}
\]

**Proof.** Select the binary subtree with intervals
\(J^a_u=J_{a\upharpoonright |u|,u}\). Its two children at depth \(n\) use the common natural number \(a(n)\), so they lie respectively left and right of its marker, are separated, and have diameters tending uniformly to zero. Let \(D_a\) be its markers and let \(K_a=\overline{D_a}\). Exactly as for \(K\), this consists of its finite node markers and its binary branch limits. The markers are isolated in \(K_a\), the branch limits form a Cantor set, and \(K_a\) is compact and nowhere dense.

Match markers by (7) and binary branch limits by the same binary branch. Distinct branches have distinct limits and no limit equals a marker. The two constructions have the same order: a zero descendant precedes its node marker and a one descendant follows it. This gives an increasing bijection. It is continuous at isolated markers. At a branch limit, the nested branch cylinders are neighborhoods in the respective compact sets, and the target diameters tend to zero; hence the bijection is continuous there too. Alternatively an increasing bijection between compact subsets of \(\mathbb R\) is an order homeomorphism. Every selected marker is in \(B_T\), because each \(a\upharpoonright n\) belongs to \(T\). \(\square\)

## Complete analytic upward sections

**Proposition 5.** For every \(T\in\mathrm{Tr}\),
\[
 T\in\mathrm{IF}\quad\Longleftrightarrow\quad
 \varphi_*R_2\psi_T.
 \tag{8}
\]

**Proof.** Suppose first that \(T\) has a branch. Lemma 4 and (4) show that \(e_a\) satisfies the rational preservation hypothesis of Lemma 2: the only rational points of \(K\) are its markers, which (7) sends to rational markers. Extend \(e_a\) to an increasing real homeomorphism \(h\) with \(h(\mathbb Q)\subseteq\mathbb Q\). Its restriction \(g\) is dense order preserving. For \(q\in A\), \(\psi_T(g(q))=1=\varphi_*(q)\). For every other rational \(q\), \(\varphi_*(q)=0\leq\psi_T(g(q))\). This witnesses the right hand side.

Conversely suppose \(\varphi_*R_2\psi_T\). Extend a witnessing \(g\) to the continuous strictly increasing real embedding \(h\). The color condition gives \(h(A)\subseteq B_T\). By continuity on the compact set \(K=\overline A\),
\[
 h(K)=\overline{h(A)}\subseteq\overline{B_T}.
\]
The first equality holds because \(h(K)\) is compact and \(A\) is dense in \(K\). Since \(h\) is injective, \(h(K)\) is uncountable. Lemma 3 therefore rules out well founded \(T\). \(\square\)

For every \(\alpha\geq2\), view the same functions \(\varphi_*\) and \(\psi_T\) as \(\alpha\)-valued. On their range \(\{0,1\}\), usual ordinal comparison is exactly binary comparison. Thus (8) holds with \(R_\alpha\) in place of \(R_2\). This proves continuous analytic hardness of a fixed upward section simultaneously for every nontrivial parameter.

For the upper bound, \(\mathbb Q^\mathbb Q\), with discrete coordinate factors, is Polish. Strict increase is a countable collection of clopen coordinate conditions. Formula (2) is a countable intersection of open conditions. For each fixed \(q\), the condition
\(\varphi(q)\leq\psi(g(q))\) is clopen in \((\varphi,\psi,g)\): variable evaluation is continuous because the index \(g(q)\) is discrete. Therefore the set of witnessing triples is Borel. Its projection is analytic, as is each fixed section. This proves Theorem 1(2), including non Borelness.

There is no restriction to Borel colorings as individual objects. Every function from the countable Borel space \(\mathbb Q\) to a countable discrete ordinal is already Borel, and all functions are allowed in the product coding.

## The small parameters and comparison maps

There is no function from nonempty \(\mathbb Q\) to the empty ordinal, so \(X_0=\varnothing\). There is exactly one function to the ordinal 1, namely the constant zero function. The empty function reduces \(R_0\) to every relation, while no map from a nonempty space to the empty space exists. This proves \(R_0<_B R_1\).

For \(\alpha\leq\beta\), the coordinatewise inclusion \(\alpha^\mathbb Q\to\beta^\mathbb Q\) is continuous. The two color comparisons on its image agree exactly, and the collection of admissible maps \(g\) is unchanged, so it is a reduction in both directions of the defining equivalence. For nonzero \(\alpha\), \(R_1\leq_B R_\alpha\) by a constant map to any element. If \(\alpha\geq2\), \(R_\alpha\not\leq_B R_1\), since the inverse image of a Borel relation by a Borel map is Borel, whereas Theorem 1(2) shows that \(R_\alpha\) is not Borel. These arguments prove Theorem 1(1) and (3).

## Greatest elements and simple sections

For \(\alpha>0\), constant zero lies below every coloring using the identity witness. If \(\varphi R_\alpha0\), its values must all be zero. This proves the assertion about the least class.

Call \(\psi\) locally cofinal on \(I\) if it satisfies (1). If \(\psi\) is locally cofinal, every \(\varphi\in X_\alpha\) embeds below it with image dense in \(I\). Here are details of the required construction. Enumerate the source rationals and the rational endpoint basic intervals whose closures lie in \(I\). Construct a finite increasing partial map at each stage, preserving \(\varphi(q)\leq\psi(g(q))\). At a source stage, place the next unmapped rational in the nonempty target interval determined by its already mapped neighbors, using density of the tail at its own color. At an interval stage, do nothing if the designated target basic interval already contains an image point. Otherwise choose a smaller subinterval avoiding the current finite image. It lies between two consecutive current image points, or in an exterior gap. Choose a fresh source rational in the corresponding source gap. The tail at its color is dense in the smaller target subinterval, so assign it a suitable target point there. This keeps the partial map increasing. The union is total on \(\mathbb Q\) and dense in \(I\), as required.

There exists a coloring \(U_\alpha\) locally cofinal on all of \(\mathbb R\). If \(\alpha\) is a successor take its constant maximum. If \(\alpha\) is a nonzero limit, choose an increasing cofinal sequence \((\gamma_n)\) and partition \(\mathbb Q\) into countably many dense sets \((D_n)\); put \(U_\alpha(q)=\gamma_n\) on \(D_n\). Such a dense partition follows by recursively reserving a fresh rational for every pair consisting of a label and a rational basic interval, and then assigning leftover rationals arbitrarily. Thus \(U_\alpha\) is a greatest element by the preceding paragraph.

If \(\psi\) is greatest, then \(U_\alpha R_\alpha\psi\). For a witnessing real extension \(h\), each tail of \(U_\alpha\) is dense in \(\mathbb R\). Continuity and strict increase imply that its image is dense in the nonempty open interval \(h(\mathbb R)\). It lies inside the corresponding tail of \(\psi\). Thus (1) holds on that interval. Conversely (1) makes \(\psi\) greatest by the construction above.

Finally (1) is equivalent to
\[
 \exists a<b\in\mathbb Q\ \forall\gamma<\alpha\
 \forall u,v\in\mathbb Q\;(a<u<v<b\Rightarrow
 \exists q\in(u,v)\cap\mathbb Q\;\psi(q)\geq\gamma).
\]
For fixed \(a,b,\gamma,u,v\), the existential coordinate condition is open. The displayed condition is a countable union of countable intersections of open sets, hence \(\boldsymbol\Sigma^0_3\). This proves Theorem 1(4).

For an additional exact elementary comparison, if \(c_\delta\) denotes constant color \(\delta<\alpha\), then
\[
 \varphi R_\alpha c_\delta\iff\forall q\;\varphi(q)\leq\delta,
 \qquad
 c_\delta R_\alpha\psi\iff
 \{q:\psi(q)\geq\delta\}\text{ is dense in some nonempty interval}.
\]

These are a closed condition on the left and a \(\boldsymbol\Sigma^0_3\) condition on the right. A coloring with finite nonzero support \(q_1<\cdots<q_n\) lies below \(\psi\) exactly when there are \(r_1<\cdots<r_n\) with \(\varphi(q_i)\leq\psi(r_i)\); sufficiency follows by extending the finite increasing rational map to an increasing real homeomorphism preserving rationals. These observations are consistent with the non Borel upward section in Proposition 5, whose support is infinite.

## What is not proved

The source uses Borel reducibility of preorders: one Borel map must preserve and reflect every ordered pair. The map in (8) reduces a set to an upward section; it is not a reduction of arbitrary analytic preorders to \(R_2\). Set completeness cannot be used as a substitute for that missing conclusion.

Camerlo, Marcone and Motto Ros, Theorems 5.13 and 5.14, treat equality colors, reverse natural number colors, and color orders with two incomparable elements. A usual ordinal has neither an infinite descending chain nor two incomparable elements. Their stated hypotheses do not cover \(R_\alpha\). Reversing the underlying rational order does not reverse the order of the colors. The continuous linear order embedding theorems also do not directly apply: continuity merely on \(\mathbb Q\) permits jumps at irrational cuts, as shown above.

The remaining classification task is to determine the Borel preorder degrees of \(R_\alpha\) for all \(\alpha\geq2\), including which of the inclusion reductions are reversible and whether any of these preorders is universal analytic. No answer to those questions, no global openness certification, and no novelty claim is made here.

## References

1. Riccardo Camerlo, *Universal analytic preorders*, Oberwolfach Report 55/2005, pp. 3127–3129, Problem 5 on p. 3128. https://ems.press/content/serial-article-files/46028
2. Alberto Marcone and Christian Rosendal, *The complexity of continuous embeddability between dendrites*, Journal of Symbolic Logic 69 (2004), 663–673, Section 4, Definition 4.1 and Proposition 4.2. https://users.dimi.uniud.it/~alberto.marcone/CED.pdf
3. Riccardo Camerlo, Alberto Marcone and Luca Motto Ros, *Invariantly universal analytic quasi-orders*, Section 5.3, Theorems 5.13–5.14. https://arxiv.org/abs/1003.4932
4. Matthew Foreman, Daniel J. Rudolph and Benjamin Weiss, *The conjugacy problem in ergodic theory*, Annals of Mathematics 173 (2011), 1529–1586, Theorem 4 on p. 1538. https://annals.math.princeton.edu/wp-content/uploads/annals-v173-n3-p07-p.pdf
5. Raphaël Carroy, Yann Pequignot and Zoltán Vidnyánszky, *Embeddability on functions: order and chaos*, Transactions of the American Mathematical Society 371 (2019), 6711–6738, Section 5.1. https://arxiv.org/abs/1802.08341
