# Five approaches to even-dimensional stress reconstruction

## 0. Exact question and source scope

Let \(d=2k\ge4\), let \(P\subset\mathbb R^d\) be a full-dimensional simplicial polytope, and put \(\Delta=\partial P\). A missing face is a nonface all of whose proper subsets are faces; its dimension is its cardinality minus one. Assume every missing face has dimension at most \(k\). The question asks whether the affine \(k\)-stress space determines \(P\) up to affine equivalence. Variables are indexed by vertices: the given object is an embedded vector space of polynomials, not merely an abstract vector-space dimension.

The official OWR report, DOI [10.4171/OWR/2023/58](https://doi.org/10.4171/OWR/2023/58), prints this as the \(d=2k\) case of Conjecture 2 on page 3303. Its meeting occurred December 10–15, 2023. The nearby \(k=1\) and \(k=\lfloor d/2\rfloor+1\) discussion concerns Conjecture 1, asking for combinatorial reconstruction with a skeleton supplied, rather than boundary cases of the present affine question.

Primary results:

1. Murai–Novik–Zheng, [arXiv:2306.09816v2](https://arxiv.org/abs/2306.09816v2), Theorem 3.1, give derivative recovery of lower stresses for \(d>2k\). Proposition 3.2 gives a socle formula; Remark 3.6 warns that full lower-degree generation fails at the even endpoint in dimensions at least six. Their Theorem 1.5 proves edge participation in prime simplicial polytopes, including dimension four.
2. Novik–Zheng, [arXiv:2208.06693v2](https://arxiv.org/abs/2208.06693v2), Theorem 6.3, cover natural polytopes having only missing faces of dimension at most \(d-2k+1\). At our endpoint this is the flag case, leaving missing faces of dimensions two through \(k\) untreated.
3. Novik–Zheng, [arXiv:2604.16905](https://arxiv.org/abs/2604.16905), and the April 23, 2026 [author PDF](https://sites.math.washington.edu/~novik/publications/lower%20bound%20on%20g.pdf), Example 6.8 and Corollaries 6.9 and 6.11, give counterexamples to all-lower-degree generation and universal top-stress face participation. Their discussion after Conjecture 6.7 explicitly leaves the natural four-dimensional case open. These auxiliary counterexamples do not refute affine reconstruction.

The 2026 paper on [spheres with \(g_k=1\)](https://arxiv.org/abs/2601.10072) was checked too. Its classification results do not determine all natural embeddings from top stresses. Current primary searches did not locate a solution of the full target; this is a bounded finding, not exhaustive literature coverage.

## 1. Attempt one: isolate the exact linear information needed

Translate the origin into the interior when forming the Artinian face ring; this does not change the affine ideal because the all-ones form is included. Put \(R=\mathbb R[x_1,\ldots,x_n]\), let \(I_\Delta\) be the Stanley–Reisner ideal, set \(\theta_j=\sum_v p(v)_j x_v\), \(\ell=\sum_v x_v\), and
\[
J=I_\Delta+(\theta_1,\ldots,\theta_d,\ell),\qquad B=R/J.
\]
For a polynomial \(a\), write \(a(\partial)\) for its constant-coefficient differential operator. In the standard inverse-system description,
\[
S_i(P)=\{f\in R_i:a(\partial)f=0\ \text{for every }a\in J\}.
\]
The degree-\(i\) differential pairing is nondegenerate, giving \(S_i(P)\cong B_i^*\). The space \(S_1(P)\) is the kernel of the augmented coordinate matrix \(C(P)\) with columns \((p(v),1)\).

From \(V=S_k(P)\), compute
\[
W(V)=\operatorname{span}\{\partial^\alpha f:f\in V,\ |\alpha|=k-1\},\qquad
L(V)=\{a\in R_1:a(\partial)V=0\}.
\]

### Proposition 1: necessary and sufficient criterion

For a fixed natural simplicial \(d\)-polytope \(P\), and \(1\le k\le d/2\), its stress space determines its affine type among natural simplicial \(d\)-polytopes if and only if
\[
W(S_k(P))=S_1(P),\qquad\text{equivalently}\qquad L(S_k(P))=J_1.
\tag{1}
\]
If the missing-face restriction holds for \(P\), failure of (1) supplies counterexamples with the same face lattice and restriction.

**Proof.** Differentiation preserves all stress equations, so \(W\subseteq S_1\). A linear \(a\) annihilates \(W\) exactly when all degree-\((k-1)\) derivatives of \(a(\partial)f\) vanish for every \(f\in V\). In characteristic zero this is equivalent to \(a(\partial)f=0\). Thus \(W^\perp=L\), whereas \(S_1^\perp=J_1=\operatorname{rowspan}C(P)\), proving the equivalence.

If equality holds and \(Q\) has the same stress space on the same \(n\) labels, then \(W\subseteq S_1(Q)\). Both affine-dependence spaces have dimension \(n-d-1\), hence are equal. Their orthogonal row spaces determine the same point configuration up to an invertible affine map.

Conversely choose \(a\in L\setminus J_1\), and replace just the first coordinate row by \(p_1+t a\). For sufficiently small real \(t\), the new convex hull \(P_t\) remains full-dimensional, simplicial, and combinatorially identical to \(P\). Indeed each original facet contains \(d\) affinely independent vertices and has every other vertex strictly on its inner side. All these finitely many strict inequalities persist. The surviving facets have both incident facets at every ridge, so form a union of components of the facet-adjacency graph of the new convex hull. That graph is connected, so they exhaust its boundary.

Every old \(k\)-stress still satisfies the support and coordinate equations, since \(a(\partial)V=0\), so \(S_k(P)\subseteq S_k(P_t)\). The standard natural-polytope stress-dimension theorem gives \(\dim S_k(P_t)=g_k(\Delta)=\dim S_k(P)\). Hence equality holds.

Let \(U\) span the other coordinate rows and the all-ones row. The classes of \(p_1,a\) modulo \(U\) are independent. Thus \(U+\mathbb R(p_1+t a)\) differs for every distinct \(t\), excluding label-preserving affine equivalence to \(P\) for \(t\ne0\). There are finitely many vertex permutations, and each permuted row space of \(P\) equals at most one row space in this family. Avoiding those finitely many parameters excludes unlabeled affine equivalence too. ∎

This reduction is a consequence of the established inverse-system/Gale framework, with the standard identity \(\dim S_k=g_k\) as an external input; no historical novelty is claimed.

The criterion is equivalently
\[
\{b\in B_1:bB_{k-1}=0\}=0.
\tag{2}
\]
Indeed \(a(\partial)V=0\) exactly when \(aR_{k-1}\subseteq J_k\), by the perfect differential pairing.

**Direct special case.** If \(P\) is \(k\)-neighborly, \(I_\Delta\) has no terms of degree at most \(k\). Writing \(Z=S_1(P)\), an invertible linear change of variables shows \(S_k(P)=\operatorname{Sym}^kZ\). For \(0\ne z\in Z\), select a constant direction \(v\) with \(D_vz\ne0\). Then \(D_v^{k-1}(z^k)=k!(D_vz)^{k-1}z\), proving \(W=Z\) and reconstruction. This elementary special case does not handle non-neighborly polytopes.

**Outcome:** exact necessary-and-sufficient target (2), but no universal proof.

## 2. Attempt two: extend the socle argument to the middle degree

The tempting stronger claim is that every lower stress is generated from top stresses by derivatives. The cited socle theorem gives
\[
\dim\operatorname{Soc}(B)_j=m_{d-j}(\Delta)\quad(j<k-1),\qquad
\dim\operatorname{Soc}(B)_{k-1}\ge m_{k+1}(\Delta).
\]
Our hypothesis makes the right sides zero, but the endpoint inequality does not force equality. The stronger claim is already false. The following explicit calculation reproduces the smallest member of the credited 2026 family.

Place three copies of \(T=\operatorname{conv}((1,0),(0,1),(-1,-1))\) in complementary coordinate planes of \(\mathbb R^6\), and take \(P=T\oplus T\oplus T\). Its boundary joins three triangle boundaries, and its only missing faces are the three vertex triples. It satisfies the target with \(k=3\).

The six coordinate relations identify all three variables within each block. Before the affine relation the face ring is \(\mathbb R[a,b,c]/(a^3,b^3,c^3)\). The affine form is \(3(a+b+c)\); therefore
\[
B\cong\mathbb R[u,v]/(u^3,v^3,(u+v)^3)
 =\mathbb R[u,v]/(u^3,v^3,u^2v+uv^2).
\tag{3}
\]
Its Hilbert function is \((1,2,3,1)\). The nonzero quadratic \(q=u^2+uv+v^2\) satisfies \(uq=vq=0\). Multiplying a general quadratic by \(u,v\) shows this socle component is exactly one-dimensional.

In dual coordinates a top inverse polynomial is \(F=X^2Y-XY^2\). Its first derivatives span
\[
\operatorname{span}\{2XY-Y^2,\ X^2-2XY\},
\]
of dimension two, whereas \(\dim S_2=3\). But \(F_{XX}=2Y\) and \(F_{YY}=-2X\), so the second derivatives span all of \(S_1\).

**Outcome:** full lower-degree generation fails for a genuine target polytope; affine reconstruction still succeeds for this realization. Failure of \(S_k\to S_{k-1}\) must not be confused with failure of \(S_k\to S_1\). Condition (2) is weaker than levelness.

## 3. Attempt three: recover the skeleton from stress supports

Another shortcut would read the \((k-1)\)-skeleton from the union of squarefree supports. The same credited example disproves that first step.

Let \(s_j\) sum the original variables in block \(j\). The unique cubic stress up to scalar is
\[
F=(s_1-s_3)(s_2-s_3)(s_1-s_2).
\tag{4}
\]
Every triple containing one vertex from each block is a face. The coefficient of \(s_1s_2s_3\) in (4) is zero, so all \(3^3=27\) such triangles have zero weight in every top stress. The exact program verifies that these are exactly the inactive triangular faces, out of 81 triangular faces of the actual convex hull. Nonetheless, second derivatives recover \(S_1\).

In dimension four write quadratic stresses as \(\tfrac12x^T\Omega x\), with \(\Omega\) symmetric. Then
\[
W(S_2)=\sum_{\Omega\in S_2}\operatorname{im}\Omega,\qquad
L(S_2)=\bigcap_{\Omega\in S_2}\ker\Omega.
\]
The exact target is therefore \(\dim\bigcap\ker\Omega=5\). The credited edge-participation result says each edge appears in some stress. Individual nonzero entries do not establish this simultaneous common-kernel rank condition. Generic-embedding results likewise do not prove it for every natural embedding.

**Outcome:** the support-union shortcut is false already for \(k=3\). For \(k=2\), the common-kernel equality remains the missing natural-embedding assertion.

## 4. Attempt four: suspend into the proved odd-dimensional range

Translate \(P\) to contain zero in its interior, and form the symmetric bipyramid \(Q=\operatorname{conv}((P,0),\pm e_{2k+1})\). It has boundary \(\Delta*S^0\); its missing faces are those of \(\Delta\) and the pair of apices. It thus meets the known odd-dimensional theorem's hypotheses at stress degree \(k\).

But the input \(S_k(P)\) does not directly give \(S_k(Q)\). Put \(A=R/(I_\Delta+\Theta_P)\) and introduce apex variables \(a,b\). The new coordinate equation is \(a-b=0\) and the new nonface equation is \(ab=0\). Hence
\[
A_Q\cong A[t]/(t^2),\qquad
B_Q\cong A[t]/(t^2,\ell_P+2t)\cong A/(\ell_P^2),
\]
whereas \(B_P=A/(\ell_P)\). The natural map \(B_Q\to B_P\) forgets the layer \((\ell_P)/(\ell_P^2)\). The Lefschetz property makes \(\ell_P^2:A_{k-2}\to A_k\) injective, since both successive degree-one maps are injective. Thus
\[
\dim S_k(Q)=h_k(P)-h_{k-2}(P)=g_k(P)+g_{k-1}(P).
\tag{5}
\]
For the 4-cross-polytope, \(h=(1,4,6,4,1)\), so \(\dim S_2(P)=2\). Its bipyramid is the 5-cross-polytope, with \(h=(1,5,10,10,5,1)\) and \(\dim S_2(Q)=5\). The extra three dimensions equal \(g_1(P)\).

**Outcome:** suspension introduces extra stress information. This exhibits the gap in the direct lifting proposal, not an impossibility theorem for all more sophisticated lifts.

## 5. Attempt five: exact natural-realization search and controls

The program enumerates facets by exact rational supporting-hyperplane tests, builds all faces and minimal nonfaces, and computes \(h\). It takes a rational Gale basis \(z_1,\ldots,z_m\), \(m=n-d-1\). The homogeneous solutions to the coordinate equations are \(\operatorname{Sym}^k\langle z_1,\ldots,z_m\rangle\). Expansion into original vertex variables and zero-coefficient constraints for every nonface-supported monomial give the entire affine stress space.

Every resulting basis polynomial is independently rechecked for support and all \(d+1\) differential equations. The program compares its dimension to \(g_k\), computes both derivative ranks, and verifies the missing-face bound. Gale-coordinate and original-coordinate derivative-span ranks agree because the Gale-coordinate map has full row rank.

The ten target cases, recorded as \((d,n,k;\dim S_k,\dim W)\), are:

- Standard 4-cross-polytope: \((4,8,2;2,3)\).
- Specified rational perturbation: \((4,8,2;2,3)\).
- Cyclic polytopes: \((4,6,2;1,1)\), \((4,8,2;6,3)\), \((6,8,3;1,1)\), \((6,9,3;4,2)\).
- Triangle–square and triangle–pentagon free sums: \((4,7,2;1,2)\), \((4,8,2;1,3)\).
- Three-triangle free sum: \((6,9,3;1,2)\), with the one-dimensional degree-two socle defect.
- Standard 6-cross-polytope: \((6,12,3;5,5)\).

All have \(\dim W=n-d-1\), certifying the criterion for these realizations. These are not an exhaustive search of types or realization spaces.

Two controls are separate:
- The 5-cross-polytope is the odd-dimensional suspension control, with degree-two stress dimension five.
- The stacked 4-polytope formed by adjoining \((3/10,3/10,3/10,3/10)\) to \(\operatorname{conv}(0,e_1,e_2,e_3,e_4)\) has \(\dim S_2=0\), \(\dim S_1=1\). It has a missing tetrahedron and is excluded by the target hypothesis. It verifies detection of a genuine deficit without falsely counting it as a target counterexample.

The toy quotient \(\mathbb Q[u,v]/(u^2,uv,v^3)\) is another negative control: its top inverse polynomial \(Y^2\) has derivatives missing \(X\). No polytope realization is asserted for that algebra.

## 6. Remaining gap and disposition

What remains is proving (2), nondegeneracy on the first factor of \(B_1\times B_{k-1}\to B_k\), for every natural simplicial \(2k\)-polytope satisfying the missing-face hypothesis. None of these five approaches establishes this universally. The credited auxiliary counterexamples obstruct stronger shortcuts while retaining the required linear information in the checked realization.

**Unsolved, 5/5 substantive approaches.** The packet gives rigorous reductions, attributed auxiliary obstructions, special cases, and exact checks. It is unrefereed AI-assisted work, without formal proof-assistant certification or a historical novelty claim.
