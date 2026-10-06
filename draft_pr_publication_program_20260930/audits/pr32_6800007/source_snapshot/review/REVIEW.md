# Independent review of the flag-manifold classification, 6800007

**Verdict: PASS for the complete cohomological classification stated in the candidate.** No mathematical correction is required. This is an independent adversarial AI review, not a formal proof certificate or a finding of historical novelty.

Reviewed on 2026-09-30 using GPT-6 Astra at xhigh reasoning. The reviewed artifact is CANDIDATE.md, SHA-256:

501c9a536246ad06b29e16720c613bcb292c863857849f837bb0250c45a58050

The reviewed statement concerns a fixed smooth second-countable real three-manifold without boundary, ordinary homotopies through totally real immersions, and the ordered complex flag variety with its integrable complex structure. It includes nonorientable and noncompact sources and does not require properness. This scope is mathematically supported. No assertion about embeddings, equivalence under source diffeomorphisms, or the neighboring real-form uniformization question follows.

## 1. Exact target and prior results

The original Morgan–Pansu list, Section 6, Question 7, printed page 6, asks for the homotopy classification of totally real immersions of real three-manifolds into the complex full flag manifold. It immediately identifies the h-principle as the relevant reduction. The original TeX and the university-hosted PDF agree; the question does not impose compactness or orientability. The candidate's convention of homotopy through totally real immersions agrees with Falbel–Veloso's later explicit convention. [Original list](https://www.imo.universite-paris-saclay.fr/~pierre.pansu/problems_MTDG.pdf)

Falbel–Veloso's 2020 author manuscript, Section 8.1, Proposition 8.1, already gives an integer family of totally real regular-homotopy classes over each nonzero homotopy class of maps from the three-sphere. I read the proposition and proof in the full author-manuscript text. The arXiv record has only its 2018 version; the later proposition is not attributed to that earlier file. The candidate credits this prior result correctly. Its additional zero underlying class is also justified by the argument: the pulled-back tangent bundle is trivial there as well. [2020 author manuscript](https://www.researchgate.net/publication/340658748_Flag_structures_on_real_3-manifolds), [2018 arXiv record](https://arxiv.org/abs/1804.11096)

Koshkin's Theorem 3 already supplies a primary/secondary quotient classification for maps from arbitrary three-dimensional CW complexes into compact simply connected homogeneous spaces. The candidate does not mistake that general framework for a new theorem. Its calculation also includes the tangent-bundle isomorphism and computes the coupled monodromy action explicitly. [Koshkin, Theorem 3](https://arxiv.org/abs/0808.0024)

The result is an explicit cohomological classification rather than a restatement as a mapping or frame-bundle problem. Its final data are the ordinary integral groups in degrees one, two and three, the orientation Bockstein, cup products, an explicitly specified index condition, and an explicitly specified homomorphism whose cokernel is taken. For a finite triangulation these are finite abelian-group calculations, including Smith reduction. For arbitrary noncompact sources the formula is a structural classification; it is not a claim that the input cohomology has a finite presentation or a uniform effective algorithm.

A bounded additional search did not locate the exact formula. That does not establish novelty, priority, or exhaustive current literature coverage.

## 2. Formal immersion and h-principle audit

At every point, a real-linear derivative from a three-dimensional real space to a three-dimensional complex space is totally real if and only if its complexification is an isomorphism. Consequently the formal datum is precisely a map \(f\), together with
\[
TM\otimes\mathbb C\cong f^*TF.
\]
No orientation, metric, Lagrangian condition or derivative trivialization of \(TM\) may be added to this datum. The candidate adds none.

The relation is open and ample. Fix a principal slice, hence the values of the derivative on a real hyperplane. If those two columns are complex independent, the excluded third columns are their complex span, a real codimension-two linear subspace. Its complement is connected and its convex hull is the entire affine slice. If the fixed columns are complex dependent, the slice contains no allowed derivative. This verifies ampleness in every principal direction.

I checked Forstnerič's scanned printed pages 244–246. Theorem 1.1 gives the Euclidean formal classification. Section 2, page 246, states the weak-homotopy-equivalence theorem for open ample relations in a general smooth bundle, with no open-source or orientability restriction. Applying that theorem to the product bundle \(M\times F\to M\), using the preceding local slice computation, supplies the required target-manifold and parametric version. A weak homotopy equivalence gives exactly the necessary bijection on components. Theorem 1.4 on page 245 does expressly assume a compact orientable three-manifold, and the candidate correctly avoids using it for the broader existence statement. [Forstnerič, 1986](https://users.fmf.uni-lj.si/forstneric/papers/1986Expositiones.pdf)

Borrelli also explicitly separates totally real regular homotopy from isotopy of embeddings. The immersion classification must not inherit the extra embedding conditions in his main results. [Borrelli, Section 2](https://doi.org/10.1155/S1073792802105125)

## 3. Bundle model, determinant and existence

The compact homogeneous-space model \(F=SU(3)/T^2\) is the homotopy fiber of \(BT^2\to BSU(3)\). The three ordered tautological lines have a specified product trivialization. Therefore the first nullhomotopy in the proposed simultaneous fiber is an \(SU(3)\)-trivialization. Replacing it with a free \(U(3)\)-trivialization would change the problem, but the candidate retains the correct determinant constraint.

The holomorphic tangent representation has the three weights
\[
x_2-x_1,\quad x_3-x_1,\quad x_3-x_2.
\]
These are the lower matrix entries in the quotient of the Lie algebra by the upper triangular subalgebra. Its first Chern class is
\[
2(x_3-x_1)=-4x-2y.
\]
The representation is a complex vector-bundle representation of the compact torus; a holomorphic direct-sum splitting over the flag variety is not needed.

On a three-dimensional CW complex, \(BSU(3)\) is 3-connected and a rank-three complex vector bundle is classified by its first Chern class. Thus the first bundle always admits the required \(SU(3)\)-trivialization. The second admits an isomorphism with \(TM\otimes\mathbb C\) exactly when its first Chern class is \(\delta=\beta(w_1(TM))\). The determinant of the complexification is the complexified real orientation line, which gives this Bockstein directly from its sign transition functions.

It follows that every admissible index has a formal representative. The range of \((x,y)\mapsto-4x-2y\) is exactly \(2H^2(M;\mathbb Z)\). Coefficient exactness and \(\rho_2\beta(w_1)=Sq^1w_1=w_1^2\) give precisely the asserted existence criterion. No division by two or torsion cancellation is used.

The distinction between \(\delta=0\) and \(\delta\in2H^2\) is real, not redundant. The example in Section 7 below tests a nonzero divisible determinant class.

## 4. Loop coordinates and potential Postnikov obstructions

This is the most delicate part of the proof, and it passes the audit.

A loop at the classifying map of \(E=TM\otimes\mathbb C\) is a rank-three bundle on \(M\times S^1\) with the fixed identification with \(E\) on \(M\times\{1\}\), up to relative homotopy. Stabilization and translation by \(-E\) identify its class with a relative stable rank-zero class. These operations preserve the group law on fundamental groups: the stable mapping space is group-like, and loop concatenation agrees with addition on its fundamental group.

There is no missed ambiguity from the slice identification. Restriction to \(M\times\{1\}\) is split by projection to \(M\), in both ordinary cohomology and stable K-theory. Hence the relative classes inject into the corresponding absolute groups. In particular, slanting with the circle records all of the relative cohomology classes in degrees two and four:
\[
H^2(M\times S^1,M\times\{1\};\mathbb Z)=H^1(M;\mathbb Z),
\]
\[
H^4(M\times S^1,M\times\{1\};\mathbb Z)=H^3(M;\mathbb Z).
\]

Rank three lies safely in the stable range here. The fibration \(U(n)\to U(n+1)\to S^{2n+1}\), together with unitary periodicity, gives
\(\pi_2BU(3)=\mathbb Z\), \(\pi_4BU(3)=\mathbb Z\), and zero groups in degrees one, three and five. The map \((c_1,c_2)\) to \(K(\mathbb Z,2)\times K(\mathbb Z,4)\) induces isomorphisms in all these degrees. On \(S^4\), the quaternionic Hopf line, regarded as a complex rank-two bundle and stabilized, has second Chern class a generator: its sphere bundle is \(S^7\), so its Euler class is a generator by the Gysin sequence. Thus there is no hidden integer factor in the \(c_2\) coordinate. [Bott, stable unitary homotopy, pp. 314–315](https://doi.org/10.2307/1970106)

Relative bundle classes use a domain of dimension four, and their homotopies use dimension five. The stated homotopy-group range therefore gives both existence and uniqueness for the relative classification. The first higher Postnikov data cannot contribute in this dimension. This is an integral obstruction argument, so it also covers torsion cohomology. It does not infer an integral result from a rational Chern character or merely from an associated graded group.

For relative classes, \(c_1=ht\), where \(t\) comes from the parameter circle. The cross term in the Whitney sum formula vanishes because every product \((ht)(h't)\) is zero. Therefore
\[
\bigl(c_1/[S^1],-c_2/[S^1]\bigr)
\]
is an additive isomorphism to \(A\oplus C\). The corresponding \(BSU(3)\) group is \(C\). In particular, neither a nonabelian loop-group action nor an unresolved abelian extension remains.

For a nontrivial \(E\), the coordinate must use \(V-E\). The exact formula
\[
c_2(V-E)=c_2(V)-c_1(V)c_1(E)+c_1(E)^2-c_2(E)
\]
is correct. A concrete negative control is \(M=\mathbb{RP}^2\times S^1_x\). Let \(L\) have its nonzero order-two class \(b\), let \(E=L\oplus1\oplus1\), and let \(P\) on \(S^1_x\times S^1_t\) have \(c_1(P)=xt\). Clutching the trivial summand gives \(V=L\oplus P\oplus1\). Then \(c_2(V)=bxt\ne0\), while \(V-E=P-1\) has \(c_2=0\). This verifies that the virtual correction has actual torsion content.

## 5. Monodromy and completeness of the quotient

The source loop group is \(H^1(M;\mathbb Z)^2\). A loop has line classes \(x_i+h_it\), with \(\sum x_i=\sum h_i=0\). Calculating the coefficient of the parameter circle in the second Chern class yields
\[
a=\sum_i x_i h_i,\qquad
k=2(h_3-h_1),\qquad
b=\sum_{i<j}(x_j-x_i)(h_j-h_i)=3a.
\]
The determinant correction in the virtual class removes the \(\delta k\) term before taking the second coordinate. The calculation uses only integral addition and multiplication.

The complete image is consequently \((a,k,3a)\), not separate images in the three factors. In particular, quotienting each factor independently would discard real extension information. For a fixed component of the source, the components of the homotopy fiber form a transitive orbit of the target fundamental group, whose stabilizer is exactly the image of the source fundamental group. Higher homotopy groups affect higher homotopy of the fiber, not this component orbit. Since the target group is abelian, the orbit is a torsor for the quotient group.

The displayed change of variables
\[
(u,m,v)\longmapsto(v-3u,m,u)
\]
is integral and unimodular, with an integral inverse. It is valid when \(C\) has torsion. It sends the image to \((0,k,a)\), giving exactly \(C\oplus\operatorname{coker}D_{x,y}\). The proof thus counts homotopies of all line-bundle data; it does not only count framings over one fixed map.

## 6. Noncompact and nonorientable scope

A second-countable smooth manifold admits a countable locally finite triangulation of its actual dimension. The argument can therefore use an actual three-dimensional CW model, and \(M\times S^1\) and the relative homotopy domains have dimensions four and five. Obstruction-theoretic connectivity bounds are cellular dimension bounds, not finite-cell assumptions. Applying them directly to the infinite CW complex avoids any inverse-limit or phantom-map inference.

The relevant bundles are ordinary numerable bundles over a paracompact space. Homotopies are ordinary homotopies, with no control imposed at infinity. Thus ordinary cohomology is the appropriate theory. Compactly supported or end-preserving cohomology would classify a different problem. For example, the candidate correctly gives one class for \(\mathbb R^3\), whereas inserting compactly supported \(H^3\) would create spurious classes.

The coefficients are untwisted integral coefficients even when \(M\) is nonorientable. They arise from the simply connected complex bundle-classifying spaces, not from integration against a chosen orientation of \(M\). For a closed connected nonorientable three-manifold the ordinary top group can be \(\mathbb Z/2\); it must not be deleted by de Rham reasoning.

## 7. Independent examples and exact diagnostics

The independent checker uses explicit cellular cochains, full abelian-group presentations, finite quotient enumeration and an integral graded exterior algebra. It does not import or call the candidate's checker.

- **Three-sphere:** the two loop groups give \(\mathbb Z^2\), with no source-loop action. Projection to the underlying map leaves an integer family, agreeing with the credited Falbel–Veloso result.
- **\(S^2\times S^1\):** the original coupled three-row presentation, before the candidate's splitting, has columns \((0,-4,0)\) and \((-3n,-2,-9n)\). Smith reduction for all \(-15\le n\le15\) reproduces the stated groups, including the exceptional free rank at \(n=0\).
- **Lens spaces:** with \(A=0\), \(B=\mathbb Z/p\), \(C=\mathbb Z\), there are \(p\gcd(p,2)\) admissible labels and a \(\mathbb Z^2\)-torsor at each. All labels were enumerated for \(1\le p\le32\); in particular even-order torsion cannot be divided out.
- **\(\mathbb{RP}^2\times S^1\):** cellular cochains give \(A=\mathbb Z\), \(B=C=\mathbb Z/2\), with \(\delta\) the generator of \(B\). The index set is empty. The same orientation obstruction remains for the noncompact \(\mathbb{RP}^2\times\mathbb R\).
- **Klein bottle \(K\) times \(S^1\):** let \(a\) generate \(H^1(K;\mathbb Z)\), \(t\) be the circle class, and \(b\) generate \(H^2(K;\mathbb Z)=\mathbb Z/2\). Then \(A=\mathbb Z a\oplus\mathbb Z t\), \(B=\mathbb Z(at)\oplus(\mathbb Z/2)b\), \(C=(\mathbb Z/2)bt\), and \(\delta=0\). Here \(a^2=0\) because \(a\) is pulled back from a circle, and the only relevant nonzero torsion product is \(bt\). Write \(x=n(at)+\epsilon b\), \(y=-2n(at)+\eta b\). The fiber groups are \((\mathbb Z/2)^4\) for \((\epsilon,\eta)=(0,0)\), \((\mathbb Z/2)^2\oplus\mathbb Z/4\) for \((1,0)\), and \((\mathbb Z/2)^3\) when \(\eta=1\). Both Smith reduction and direct finite quotient enumeration verify these groups. The order-four case is a useful test that the coupled action preserves extension information.
- **Twisted \(S^2\)-bundle over \(S^1\):** its cellular coboundary in degrees two to three is multiplication by two; hence \((A,B,C)=(\mathbb Z,0,\mathbb Z/2)\) and \(\delta=0\). The formula gives eight classes, with group \((\mathbb Z/2)^3\).
- **Interior of a Möbius band times \(\mathbb R\):** the source retracts to a circle and has trivial complexified tangent bundle. The formula gives two classes. Independently, the unitary frame total space of \(TF\) has fundamental group \(\mathbb Z/2\), from the determinant map \(\mathbb Z^2\to\mathbb Z\), \((p,q)\mapsto-4p-2q\). This gives the same two free homotopy classes of circle maps.
- **A genuine nonzero determinant:** Reid's closed nonorientable hyperbolic manifold \(m313(1,0)\) has \(H_1=\mathbb Z\oplus\mathbb Z/4\) and \(w_1\) has no integral lift. Thus \(B=\mathbb Z/4\) and \(\delta=2\) in this group. It is nonzero but divisible by two. The presentation in Reid's Section 2 independently reproduces the abelianization; its orientation character lifts to \(\mathbb Z/4\). The admissibility equation has exactly eight solutions, namely arbitrary \(x\) and odd \(y\). This tests the existence statement with a genuinely nontrivial \(TM\otimes\mathbb C\), rather than only algebraic torsion rings. I do not infer the remaining cup-product table of this manifold from its homology. [Reid's appendix](https://math.rice.edu/~ar99/immersionsFKKT_2.pdf)
- **Three-torus:** 750 clutching cases in the genuine graded integral ring \(H^*(T^3\times S^1;\mathbb Z)\) verify both Chern-slant coordinates, including the signs from anticommuting degree-one generators and the root-weight factor three.

The Euclidean existence/nonexistence checks for the Klein product and projective-plane product also agree with Ho–Jacobowitz–Landweber's Remark 4.4. That paper does not establish the flag classification; it is an independent consistency check on the nonorientable examples. [New York Journal of Mathematics 18 (2012), pp. 470–471](https://nyjm.albany.edu/j/2012/18-26p.pdf)

There are **1,595 passing independent exact assertions**, including 750 graded-ring cases. The author's existing verification receipt was separately reproduced byte for byte. These computations check the stated algebra and examples; the h-principle and obstruction-theoretic conclusions are justified by the written audit above.

## 8. Final scope and verification boundary

The full theorem stated in CANDIDATE.md passes this review, with no unresolved mathematical gap identified. The target's h-principle, known sphere calculation and general obstruction-theory framework remain prior work. Novelty of the precise integral formula remains unestablished.

The four review deliverables are REVIEW.md, review_summary.json, independent_checks.py and independent_results.json. Reproduce the independent receipt from their directory with:

    python independent_checks.py > independent_results.json

Downloaded reference documents and page images are not part of these deliverables.
