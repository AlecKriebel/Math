# Independent analytic reconstruction

This argument was reconstructed from the current five-page manuscript, necessary original proof, and primary theorem bodies before inspecting submitted helpers. The fresh controls were also completed before helper inspection. The group is the countable discrete restricted wreath product \(W=(\bigoplus_{\mathbb Z}\mathbb Z)\rtimes\mathbb Z\), with \(t a_i t^{-1}=a_{i+1}\), \(a=a_0\), and shift character \(\chi\).

## 1. The topology and relative lifting argument

The action space consists of homomorphisms from \(W\) into the Polish group of Cantor homeomorphisms. The group equations define a closed subset of the countable product. Neighborhoods may prescribe finitely many group elements, not merely the two generators. Including their inverses gives the uniform control of maps and inverses needed for the homeomorphism topology.

For each continuous finite-valued function \(c:C\to\mathbb Z/m\), the two generator equations defining \(D(c,m)\) imply equivariance under every group word. Their truth is locally constant as a function of the action: a finite clopen partition into the fibers of \(c\) has a positive separation scale, so sufficiently small uniform perturbations of the two generator maps preserve every output label simultaneously. Thus \(D(c,m)\) is both open and closed. There are countably many such functions because clopen subsets of a compact second-countable zero-dimensional space form a countable family.

For \(m\mid n\), consider the obligation that either the old residue map is not equivariant or it has an equivariant compatible lift modulo \(n\). It is open by the preceding observation. To check density near an action \(\alpha\) where the old map is equivariant, form

\[
Y=\{(x,j):c(x)=j\bmod m\},\qquad
\gamma(g)(x,j)=(\alpha(g)x,j+\chi(g)).
\]

This is an exact action: the defining equality is preserved because \(c\) is equivariant. Choose a finite symmetric control set \(F\) and a small clopen partition \(Q\). Refine \(Q\), all \(\alpha(g)^{-1}Q\) for \(g\in F\), and the old fibers to a partition \(P\). For each nonempty atom \(A\), the inverse image \(Y_A\) is \(n/m\) disjoint copies of the Cantor space \(A\), hence is homeomorphic to \(A\). Combining these maps gives a homeomorphism \(h:C\to Y\) which preserves first-coordinate \(P\)-atoms.

Set \(\beta=h^{-1}\gamma h\). If \(h(x)=(u,j)\), the points \(u,x\) lie in one \(P\)-atom, so \(\alpha(g)u,\alpha(g)x\) lie in one \(Q\)-atom. Meanwhile \(\beta(g)x\) lies in the same \(P\)-atom as \(\alpha(g)u\). Thus \(\beta(g)x,\alpha(g)x\) are uniformly \(Q\)-close for every prescribed \(g\), including inverse maps. The second coordinate of \(h\) is the required lift, and reduction modulo \(m\) recovers \(c\).

The countable intersection of these open dense obligations is a dense \(G_\delta\). For any action in it, start with the unique residue modulo one and successively choose compatible maps modulo \(n!\). All maps which might be chosen were already included among the countably many obligations; the recursion introduces no uncountable intersection. The resulting map into \(\widehat{\mathbb Z}\) is continuous and equivariant. Its nonempty compact image is invariant under \(\pm1\), whose translations are dense, hence it is surjective. No uniform measurable selection of this factor across the action space is required.

The argument does not assert that a generic action has finite order, a comeager conjugacy class, minimality, or a continuous integer-valued shift height.

## 2. Slab coordinates, including nonfree actions

For any Borel \(W\)-action with a Borel equivariant profinite height \(p\), fix \(m\ge1\). Let \(r_m(x)\) be the unique representative in \(\{0,\ldots,m-1\}\) of \(p(x)\bmod m\), and \(B_m=r_m^{-1}(0)\). The map

\[
x\longmapsto(t^{-r_m(x)}x,r_m(x))
\]

is a Borel bijection \(X\to B_m\times\{0,\ldots,m-1\}\). The inverse is \((z,r)\mapsto t^r z\): the residue of this point is \(r\), regardless of lamp stabilizers. There is no need to identify group elements with distinct orbit points.

The cut graph contains lamp edges and forward shift edges except at residue \(m-1\). In these coordinates, each lamp edge changes \(z\) by \(a_{-r}\); each permitted shift edge changes only \(r\). This follows from the exact conjugation \(t^{-r}at^r=a_{-r}\). At the forbidden wrap, the normalized base would change, so that edge is correctly excluded.

The graph has degree at most four. Each bounded-length path condition is a finite union of graphs of partial Borel word maps, hence the extended path metric is Borel. Every finite-radius ball is finite. This is the precise notion of “proper” used in the imported theorem, not topological compactness of balls.

## 3. Finite Borel asymptotic dimension with the right uniformities

The subgroup \(K_m=\langle a_0,\ldots,a_{-(m-1)}\rangle\cong\mathbb Z^m\) acts on \(B_m\). CJMST Corollary 5.5 applies to any Borel action of this group, including actions with stabilizers. Each particular \(m\) has a uniform local polynomial growth degree; the direct sum of all lamps does not have a single such bound.

CJMST Lemmas 2.2 and 3.1, and the paragraph following Definition 3.2, give a finite number of Borel colors, fixed for this \(m\), so that for each finite move set the monochromatic components have a uniform finite cardinality bound. A Borel cover can be made a partition by assigning a point to its first containing set; removing points cannot enlarge a monochromatic component. Uniform cardinality bounds follow from uniform metric diameter bounds in the action word metric because its balls are uniformly bounded by finite group word balls.

For radius \(R\ge1\), use all \(K_m\)-words of length at most \(\lceil R\rceil\). Give \((z,r)\) the color of \(z\). A slab path of length at most \(R\) changes its normalized base by at most \(\lceil R\rceil\) lamp moves. A chain whose successive endpoints are within \(R\) and have one color therefore projects into one monochromatic base component. The paths joining those endpoints need not be monochromatic; this does not affect the argument. If a base component has at most \(C_R\) points, the lifted chain component has at most \(mC_R\). Its diameter is at most \(R(mC_R-1)\), using a simple chain in the threshold graph. For \(0<R<1\), the components are singletons.

Thus the Borel asymptotic dimension of each slab metric is finite. The dimension bound may depend on \(m\); the cardinality and diameter bounds may also depend on \(R\). No uniform bound across all widths is needed or established.

## 4. The regular part and the compatible-metric theorem

If \(m\mid M\), a cut at residue \(M-1\) is also a cut modulo \(m\). Hence every old edge survives, \(G_m\subseteq G_M\), and \(\rho_M\le\rho_m\) on pairs of finite old distance. In particular

\[
\sup\{\rho_{(n+1)!}(x,y):\rho_{n!}(x,y)<R\}\le R.
\]

This verifies the exact compatibility required by CJMST Theorem 7.3. That theorem allows the finite Borel dimensions to vary with \(n\).

The embedded integers are a countable Borel subset of the profinite integers, but their preimage need not be countable. Remove the full invariant preimage for the present step. For a point in the remaining invariant set, a forward shift edge cannot be cut at every factorial level: that would give \(p(x)\equiv-1\pmod{n!}\) for every \(n\), hence \(p(x)=-1\). Every forward edge thus eventually appears, and every lamp edge is already present. Inverse edges appear with their corresponding forward edges. A finite word uses finitely many edges, all of which occur at one late enough level. Restricting to the invariant set loses no intermediate vertices.

Consequently the full orbit relation there is the union of the factorial slab finite-distance relations. Apply the compatible-metric theorem. This is not an application of an unrestricted increasing-union theorem for hyperfinite relations.

## 5. The entire exceptional preimage

On \(X_{\rm exc}=p^{-1}(\mathbb Z)\), the integer \(h(x)\) represented by \(p(x)\) is Borel: its countably many singleton fibers are Borel. Put \(q(x)=t^{-h(x)}x\in B=p^{-1}(0)\). The countable piecewise definition makes \(q\) Borel.

For \(y=gx\), the element \(t^{-h(y)}gt^{h(x)}\) has shift character zero and lies in the lamp group \(N\). Conversely an \(N\)-move between normalized points conjugates back to a \(W\)-move. Thus

\[
xE_Wy\quad\Longleftrightarrow\quad q(x)E_Nq(y).
\]

Every finitely generated subgroup of \(N=\bigoplus_{\mathbb Z}\mathbb Z\) is finitely generated abelian and has polynomial growth. CJMST Corollary 7.5 therefore applies to its Borel action on the standard Borel set \(B\), with no freeness condition. Choose finite increasing Borel relations \(F_j\) exhausting that relation. Define

\[
xH_jy\iff x=y\;\text{ or }\;
 (|h(x)|,|h(y)|\le j\text{ and }q(x)F_jq(y)).
\]

Inside the band this is an equivalence relation pulled back from \(F_j\); outside it the classes are singletons. A fiber with specified \(q(x)=z\) and \(h(x)=k\) contains exactly \(t^kz\). Distinct heights cannot describe the same point because their \(p\)-values differ. Hence each band class has at most \((2j+1)|[z]_{F_j}|\) elements. These relations are Borel and increasing. Any orbit pair eventually lies in the height band and has normalized points related by \(F_j\), proving exhaustion. The height cutoff is essential: the unrestricted pullback of even the diagonal relation could have infinitely many points.

Take the stagewise disjoint union of the finite exhaustions on the two invariant pieces. This proves hyperfiniteness on all of \(X\). No invariant probability measure, null exceptional set, or comeager subset of the phase space is used.

## 6. Scope, prior baseline and fresh controls

The main conclusion concerns a comeager subset of the full action space; it does not say every Borel \(W\)-action is hyperfinite. The auxiliary theorem requires the specified Borel height factor and does not require its surjectivity. Empty invariant pieces cause no difficulty. The main continuous factor is surjective by compactness.

The previous locally finite-asymptotic-dimension result does not directly include \(W\). The group is generated by \(a,t\), and for lamps supported in \(\{0,\ldots,d-1\}\),

\[
\|f\|_1\le |(f,0)|_{\{a,t\}}\le\|f\|_1+2(d-1).
\]

The lower bound counts necessary lamp changes; for the upper bound, walk from zero to \(d-1\), make the prescribed changes, then return. These subgroups are undistorted copies of \(\mathbb Z^d\). Thus \(W\) has infinite standard asymptotic dimension and, being finitely generated, is not locally of finite asymptotic dimension. This establishes the advertised limitation of the prior theorem without making a priority claim.

Fresh controls in fresh_height_controls.py use an explicit prefix-code homeomorphism \(C\cong C\times\{0,\ldots,d-1\}\), preserving prescribed initial bits, to test exact compatible lifts. A separate infinite-integer-height action with a finite cyclic lamp quotient tests nonfree slab coordinates, threshold-endpoint projection and exact bounded-height classes. Compatible factorial residues of a genuine noninteger profinite element test eventual edge admission on translated regular heights. Negative controls detect a reversed conjugation index, a retained wrap edge, and a false nondivisor monotonicity assertion. The saved run includes 36 lift parameter cases, 80 slab parameter cases and 26 assertion families. Its 372,046 repeated local assertions are not separate proofs of the infinite theorem.

These computations were completed before submitted executable inspection. They corroborate formulas and boundary behavior; Baire category, the primary Borel dimension results and the universal hyperfiniteness conclusion rest on the argument above and the exact imported theorem interfaces.
