# The known counterexample to component group surjectivity

## Conclusion and attribution

There is a finite degree-two map of smooth, proper, geometrically connected curves

\[
f:X'\longrightarrow X
\]

over \(K_0=\mathbf C((t))\) such that:

1. \(X\) is a Mumford curve of genus two;
2. the special fiber of the minimal regular model of \(X'\) is the union of two copies of \(\mathbf P^1_{\mathbf C}\), meeting transversely at four distinct nodes;
3. on the component groups of the Néron models of the Jacobians, the covariant map has the form
   \[
   f_*:\mathbf Z/4\mathbf Z\longrightarrow\mathbf Z/8\mathbf Z,
   \qquad j\longmapsto 2j.
   \]

In particular, its kernel is zero and its cokernel is \(\mathbf Z/2\mathbf Z\). This disproves the universal surjectivity assertion in Question 21 of Rabinoff's contribution to Oberwolfach Report 53/2012.

The construction and its negative conclusion are already in that report, pp. 3247–3248, and in Amini–Baker–Brugallé–Rabinoff (ABBR), Example 8.6. This is an authored verification and expanded proof of that prior example, with no claim of novelty. The finite calculations below are proved directly. The algebraic existence argument explicitly imports the published lifting and comparison results listed below.

## 1 The metric graph map

Write \(\Gamma'=B(1,1,1,1)\). Its two vertices are \(u',v'\), joined by edges \(e'_1,e'_2,e'_3,e'_4\), each of length one. Write \(\Gamma=B(1,2,2)\). Its vertices \(u,v\) are joined by edges \(e_1,e_2,e_3\) of lengths one, two, two, respectively. An edge of length two here is a metric interval; the unit-edge subdivision will be introduced only for computing the finite group.

Define \(\varphi(u')=u\), \(\varphi(v')=v\), and map oriented edges from the primed initial vertex to the unprimed initial vertex as follows:

\[
e'_1\mapsto e_1,\quad e'_2\mapsto e_1,\quad
 e'_3\mapsto e_2,\quad e'_4\mapsto e_3,
\]

with expansion factors \(1,1,2,2\). The image length is the source length times the expansion factor, so these edge maps have exactly the required lengths.

At \(u'\), the sum of expansion factors over each of the three target tangent directions is, respectively, \(1+1,2,2\). All are two. The same computation holds at \(v'\). At an interior point of any source edge, the two outgoing slopes are equal. Thus \(\varphi\) is harmonic at every point. It is finite because no edge is contracted, and it is surjective. Above the interior of \(e_1\) are two degree-one points; above either other edge is one degree-two point. Consequently \(\deg\varphi=2\).

Since the graphs are connected, their first Betti numbers are

\[
b_1(\Gamma')=4-2+1=3,\qquad b_1(\Gamma)=3-2+1=2.
\]

All vertex genera in the metrized complexes below are zero.

## 2 The finite graph groups and the actual map

For a finite connected unit-edge graph \(H\), its critical group is \(\operatorname{Div}^0(H)/\operatorname{Prin}(H)\), equivalently the cokernel of a reduced integer Laplacian. For an integer-length metric graph, use its unit-edge subdivision. This finite group is ABBR's regularized Jacobian, not the full real torus Jacobian of the metric graph.

### Source

The source full Laplacian is

\[
\begin{pmatrix}4&-4\\-4&4\end{pmatrix}.
\]

Deleting \(v'\) gives \([4]\), so

\[
K(\Gamma')=\mathbf Z/4\mathbf Z,
\]

with generator \(S=[u'-v']\).

### Target

Subdivide \(e_2\) and \(e_3\) once, at \(a\) and \(b\). The unit edges are \(uv,ua,av,ub,bv\). Deleting \(v\), with remaining vertices in the order \(u,a,b\), gives

\[
L=\begin{pmatrix}
3&-1&-1\\
-1&2&0\\
-1&0&2
\end{pmatrix}.
\]

Its determinant is \(8\). Its entries have gcd one. The minor on rows \(u,a\) and columns \(u,b\) is

\[
\det\begin{pmatrix}3&-1\\-1&0\end{pmatrix}=-1,
\]

so the gcd of the two-by-two minors is also one. The Smith invariants are therefore \(1,1,8\), and

\[
K(\Gamma)=\mathbf Z/8\mathbf Z.
\]

For an explicit presentation, put \(U=[u-v]\), \(A=[a-v]\), and \(B=[b-v]\). The Laplacian columns impose

\[
3U-A-B=0,\qquad -U+2A=0,\qquad -U+2B=0.
\]

Hence \(U=2A\), \(B=5A\), and \(8A=0\). Conversely, these substitutions satisfy every relation, so this presentation identifies \(A\) with a generator of \(\mathbf Z/8\mathbf Z\). In particular, \(U\) has exact order four. An independent rational calculation gives

\[
L^{-1}(1,0,0)^T=(1/2,1/4,1/4)^T;
\]

the smallest positive multiplier making this vector integral is four, confirming the order of \(U\).

### Covariant map

The pushforward of a graph divisor sends a vertex to its image, without multiplying it by the local degree. ABBR Lemma 8.3 identifies this with the covariant map on the regularized Jacobians. Therefore

\[
\varphi_*(S)=[u-v]=U=2A.
\]

There is no ambiguity about descent to the quotient in this example: the source relation \(4S=0\) maps to \(4U=8A=0\). Thus

\[
\varphi_*:j\pmod4\longmapsto 2j\pmod8,
\]

with image \(\{0,2,4,6\}\), trivial kernel, and cokernel \(\mathbf Z/2\mathbf Z\). The group orders alone already rule out surjectivity, while this presentation determines the map and cokernel.

One must not demand that this metric graph map become an ordinary harmonic map between both unit-edge subdivisions: the inverse images of \(a,b\) lie at half-integral positions on source edges. The lifting uses the original metric graphs, and the comparison uses regularized Jacobians. No simultaneous morphism of regular models is being assumed.

## 3 The metrized complex and all local cover conditions

Let \(R_0=\mathbf C[[t]]\), with \(\operatorname{val}(t)=1\). Its fraction field \(K_0\) is complete and discretely valued, its value group is \(\mathbf Z\), and its residue field \(k=\mathbf C\) is algebraically closed. It is important that \(K_0\) itself is not asserted to be algebraically closed. When applying the algebraically closed-field formulation of ABBR, use the complete algebraically closed valued extension \(\Omega=\widehat{\overline{K_0}}\), and then use the fixed-ground-field lifting statement in Remark 7.13.

At each of \(u,v,u',v'\), attach \(\mathbf P^1_k\). On each target component mark \(1,0,\infty\), corresponding to \(e_1,e_2,e_3\). On each source component mark \(1,-1,0,\infty\), corresponding to \(e'_1,e'_2,e'_3,e'_4\). At both source vertices use the residue map

\[
\rho:\mathbf P^1_k\longrightarrow\mathbf P^1_k,\qquad z\longmapsto z^2.
\]

The checks for ABBR Definition 2.19 are explicit:

- The points \(1,-1\) map to \(1\), both with ramification index one.
- The points \(0,\infty\) map to \(0,\infty\), respectively, both with ramification index two.
- Each complete fiber over a marked target point is among the marked source points; no preimage is omitted.
- The degree of each residue map is two, equal to the local harmonic degree.

All markings are distinct in characteristic zero. The only ramification of \(z^2\) is at \(0,\infty\), and both points are marked. Each residue map is separable and tame.

To check the additional condition for a **tame covering**, not just a tame harmonic morphism, compute the graph ramification coefficient at either source vertex:

\[
R_{u'}=2(2-0)-(2-0)-\bigl((1-1)+(1-1)+(2-1)+(2-1)\bigr)=0.
\]

The same holds at \(v'\). At interior points of an edge of expansion factor \(d\), the coefficient is \(2d-2-2(d-1)=0\). Thus the graph ramification divisor is zero. There are no infinite edges or punctures, so take \(D=D'=\varnothing\). The result is a tame covering in ABBR Definition 2.21; the no-loop hypothesis of Theorem 7.4 is also satisfied.

## 4 A split target over the original discrete field

The target must exist over \(K_0\) with a split model; existence over \(\Omega\) alone would not verify Remark 7.13's hypotheses.

Start with the stable nodal curve \(C_0/k\) formed from two projective lines by identifying their marked points \(1\) with \(1\), \(0\) with \(0\), and \(\infty\) with \(\infty\). Its three nodes and all their branches are \(k\)-rational. Each component has three special points, so the curve is stable.

Use the standard stable-curve deformation and algebraization facts stated in the proof of Conrad's Theorem B.2, in Baker (2008), pp. 648–649: node-smoothing parameters are part of a system of independent formal coordinates, and the stable formal family algebraizes. Choose the three node parameters to be

\[
q_1=t,\qquad q_2=t^2,\qquad q_3=t^2.
\]

Any remaining deformation coordinates can be set to zero. The pulled-back proper stable family \(\mathcal X/R_0\) has completed local node equations

\[
xy=t,\qquad xy=t^2,\qquad xy=t^2.
\]

All three parameters are nonzero in \(K_0\), so its generic fiber \(X\) is smooth. The family has geometrically connected fibers. Its skeleton is the split integer-metrized complex \(\Gamma=B(1,2,2)\) with the specified marked rational components. The identification of node thickness with edge length is ABBR Section 5.9.

This is a concrete application of the deformation argument, rather than a claim that the conclusion of Theorem B.2, which supplies a regular model, by itself prescribes arbitrary thicknesses. Here the target model intentionally has thickness two at two nodes and is not regular there.

The normalization exact sequence on \(C_0\) gives arithmetic genus \(3-2+1=2\), hence \(g(X)=2\) by flatness. Its stable special fiber is split and totally degenerate. Mumford's uniformization theorem, Theorem 4.20 of Mumford (1972), therefore makes \(X\) a Mumford curve.

## 5 Lifting over the discrete field and verifying the source model

Apply ABBR Theorem 7.4(1), or Theorem 7.7, to the tame covering of metrized complexes over the target just constructed. This imports the existence of a finite lift with the prescribed source skeleton and residue curves. Its degree is two, and its source is smooth, proper, and geometrically connected.

To obtain the lift over \(K_0\) itself, apply ABBR Remark 7.13. Every hypothesis is now accounted for:

1. \(K_0\) is complete, with algebraically closed residue field;
2. the target skeleton comes from the split semistable formal completion of \(\mathcal X/R_0\);
3. every source edge length is one, in \(\operatorname{val}(K_0^\times)=\mathbf Z\);
4. the metrized-complex map is a tame covering and \(D=\varnothing\).

Thus a lift can be constructed directly over \(K_0\), without a ramified base extension or a rescaling of normalized edge lengths. This last point matters: merely descending to some finite ramified extension and renormalizing would not, on its own, preserve the claimed unit lengths and two-component regular source model.

The local node parameters are compatible in an especially transparent way. Above the two thickness-two target nodes, the source parameter can be \(t\) and the node map has the form

\[
R_0[[x,y]]/(xy-t^2)\longrightarrow R_0[[s,r]]/(sr-t),
\qquad x\longmapsto s^2,\ y\longmapsto r^2.
\]

Above the thickness-one node there are two degree-one node maps. This illustrates compatibility of the lengths and indices; global existence and gluing are supplied by the cited lifting theorem, not inferred solely from these local formulas.

The lifted source model \(\mathcal X'/R_0\) has exactly two rational irreducible components and four nodes, all of thickness one. At a node its completed local ring is \(R_0[[s,r]]/(sr-ut)\) for a unit \(u\), a regular local ring. Away from the nodes the model is smooth over \(R_0\). Thus \(\mathcal X'\) is regular and its four intersections are transverse.

For minimality, denote its two reduced components by \(C_1,C_2\). The special fiber is the principal divisor \(F=C_1+C_2\), so \(F\cdot C_i=0\). Since \(C_1\cdot C_2=4\), it follows that

\[
C_1^2=C_2^2=-4.
\]

There are no other vertical irreducible curves and no exceptional rational component of self-intersection \(-1\). By the minimal-model criterion and uniqueness in the Stacks Project, Definition 55.8.4 and Lemma 55.10.1, this is the minimal regular model. Equivalently, the source stable model is already regular. Its genus is \(4-2+1=3\).

Because \(D=\varnothing\), the lifted curve map is even étale. The genus relation \(2g(X')-2=2(2g(X)-2)=4\) is a consistency check, not the existence proof.

## 6 Passing from graph groups to Néron component groups

The source and target semistable models need not both be regular. The lifted triangulations satisfy \(f^{-1}(V)=V'\). ABBR Theorem 5.13 gives the compatible finite map of semistable formal models; in this proper algebraic setting it is the corresponding map of semistable models. Thus the comparison hypotheses in ABBR Theorem 8.4 are met.

ABBR Theorem 8.2, Raynaud's component-group description, identifies the component groups of the two Jacobians with the regularized graph Jacobians. ABBR Theorem 8.4 identifies the covariant map on component groups with \(\varphi_*\). Section 2 therefore gives

\[
\Phi_{X'}\simeq\mathbf Z/4\mathbf Z,\qquad
\Phi_X\simeq\mathbf Z/8\mathbf Z,\qquad
\operatorname{coker}(f_*)\simeq\mathbf Z/2\mathbf Z.
\]

This has all the geometric conditions in the question. The term “two rational components” describes the **special fiber** of the minimal regular model, not the two-dimensional total space.

## 7 The narrow source correction

Example 8.6 in arXiv v3, p. 50, and in the publisher PDF, p. 65, assigns the two group orders to the opposite graph symbols. The correct values are

\[
|\operatorname{Jac}_{\rm reg}(\Gamma')|=4,
\qquad
|\operatorname{Jac}_{\rm reg}(\Gamma)|=8.
\]

The printed order comparison, as written, would not establish non-surjectivity. Reversing those two numerical assignments repairs that sentence; the actual graph map and the example's negative conclusion are valid. This finding does not invalidate the lifting theorem, the component-group comparison, or the entire published result.

The Oberwolfach report has a separate local symbol slip: in the pair of graph definitions on p. 3248, the second graph is again labeled \(\Sigma'\), although its role and the subsequent map make clear that it is the target \(\Sigma\).

No example in residue characteristic two is asserted here. One verified characteristic-zero example suffices to disprove the universal claim.

## References and imported results

- Joseph Rabinoff, joint with Omid Amini, Matthew Baker, and Erwan Brugallé, “Covers of curves and covers of skeleta,” in *Non-Archimedean Analytic Geometry*, Oberwolfach Report 53/2012, contribution pp. 3245–3248; Question 21 and negative answer pp. 3247–3248. [Report PDF](https://ems.press/content/serial-article-files/46424), [DOI](https://doi.org/10.4171/OWR/2012/53).
- Omid Amini, Matthew Baker, Erwan Brugallé, and Joseph Rabinoff, *Lifting harmonic morphisms I: metrized complexes and Berkovich skeleta*, [arXiv:1303.4812v3](https://arxiv.org/abs/1303.4812v3), dated 15 April 2014; published in *Research in the Mathematical Sciences* 2, article 7 (2015), [publisher record](https://link.springer.com/article/10.1186/s40687-014-0019-0), [publisher PDF](https://link.springer.com/content/pdf/10.1186/s40687-014-0019-0.pdf). Exact dependencies: Definitions 2.19 and 2.21; Section 5.9; Theorem 5.13; Theorem 7.4(1) or 7.7 together with Remark 7.13; Theorem 8.2, Lemma 8.3, and Theorem 8.4. Example 8.6 supplies prior-result attribution, rather than substituting for the arithmetic checks.
- Matthew Baker, with Appendix B by Brian Conrad, *Specialization of linear systems from curves to graphs*, *Algebra & Number Theory* 2 (2008), 613–653, [publisher PDF](https://msp.org/ant/2008/2-6/ant-v2-n6-p01-s.pdf). The proof of Theorem B.2, especially pp. 648–649, supplies the independent node-smoothing parameters and algebraization used for the split target. Its regularity discussion also records the thickness-one criterion.
- David Mumford, *An analytic construction of degenerating curves over complete local rings*, *Compositio Mathematica* 24 (1972), 129–174, Theorem 4.20 on p. 174. [Publisher archive PDF](https://www.numdam.org/article/CM_1972__24_2_129_0.pdf). This supplies the split-degenerate stable-reduction criterion for Schottky uniformization.

- The Stacks Project, [Definition 55.8.4 and Lemma 55.8.5](https://stacks.math.columbia.edu/tag/0C2R), and [Lemma 55.10.1](https://stacks.math.columbia.edu/tag/0C9Y), consulted 11 October 2026: absence of exceptional curves characterizes minimal regular models, and the positive-genus minimal model is unique.

Constancy of arithmetic genus in a proper flat family is a standard fact used above; it is not a new claim or a computer-verified lifting result. The exact finite computations are written out above; the independent verification outcomes and their limits are recorded in [CHECK_RESULTS.json](CHECK_RESULTS.json).
