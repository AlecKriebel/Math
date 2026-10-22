# Distinct-edge correlation for uniform forests: exact reductions and a proved subfamily

## Status and exact target

This is an AI-assisted, unrefereed authored-prose edition with an internal AI mathematical audit. It has no external human peer review or formal proof-assistant certification. It is not a computational reproduction package: the complete mathematical arguments and essential formula witnesses are included, while programs, raw expanded certificates, source documents, and datasets are not distributed. Historical checks and source inspection are described as historical evidence, not as newly executed checks or blanket acceptance of external source proofs.

This is an independently authored partial-results and obstruction report for corpus 3309 / OPG-1757. It does **not** prove or disprove the general conjecture, does not establish a new research result, and must not be described as an accepted full solution.

Let G=(V,E) be a finite **simple** graph. Let F(G) consist of **all acyclic edge subsets**, with the full vertex set retained, including isolated vertices and the empty edge set. Choose F uniformly from F(G). For **distinct** edges e,f, the target is

P(e,f in F) <= P(e in F) P(f in F).

The distinct-edge repair is explicit in Grimmett–Winkler, arXiv:math/0302185v3, pp.1–3. It is not a counterexample discovery. A spanning tree, a rooted forest, or a fixed-component forest has a different law. We prove no assertion about full negative association of arbitrary increasing events.

For the auxiliary statements below we explicitly allow positive edge weights and occasionally loopless multigraphs. These are named extensions used in the proof, not silently substituted hypotheses. A forest in a loopless multigraph cannot include both edges of a parallel pair.

Write

Z_G(w) = sum over F in F(G) of product over g in F of w_g,

and mu_w(F)=w^F/Z_G(w). The empty forest ensures Z_G(w)>0 even when some weights are zero. Subscripts denote derivatives, and

Delta_G(e,f) = (Z_G)_e (Z_G)_f - Z_G (Z_G)_{ef}.

Multiaffinity gives, for positive weights,

Cov_mu(X_e,X_f) = -w_e w_f Delta_G(e,f)/Z_G(w)^2.                 (1)

Indeed the one- and two-edge marginals are respectively w_e Z_e/Z and w_e w_f Z_ef/Z. This elementary identity is our only probabilistic-algebraic interface. At unit weights, if N,N_e,N_f,N_ef count the corresponding forests, the target is N_e N_f - N N_ef>=0.

## 1. Exact restriction to simple bipartite host graphs

**Theorem 1.** The following universal statements are equivalent:

U. Every finite simple graph has pairwise negatively correlated distinct edges in its uniform all-forest measure.

B. The same assertion holds for every finite simple bipartite graph.

W. Every finite loopless multigraph, with arbitrary positive edge weights, has pairwise negatively correlated distinct edges in its product-weighted all-forest measure.

This is a reduction, not a proof that any of the three statements is true. Uniform-to-weighted equivalence is prior work credited to Cocks and Erickson by Erickson (2012), p.76. The proof here keeps the host graph simple and bipartite and tracks individual marked microedges explicitly; no novelty is claimed for this refinement.

**Construction and counting.** Fix a finite loopless multigraph H and for each labeled edge g=uv choose a positive integer n_g. Choose an even integer L>=2. Replace g by n_g length-L u-v paths. All internal vertices are new, disjoint between paths and gadgets. Delete the original edges. The result G is finite and simple, including when H had parallel edges. It is bipartite: assign all original vertices color 0 and alternate colors along every even-length path.

Call a path complete if all its edges are selected. Any forest of G has at most one complete path in a single gadget; two would make a cycle. Project it to a labeled edge subset A of H by retaining g if its gadget has a complete path.

We claim the original edge set is acyclic if and only if A is a forest and every gadget has at most one complete path. Every cycle in G must traverse each visited internal degree-two vertex using both incident edges. It therefore consists of complete paths and projects to a cycle in H, including a two-edge cycle if two distinct parallel macroedges are selected. Conversely a cycle in H, or two complete paths in one gadget, gives a cycle in G. Partial path pieces cannot form additional cycles. This proves the claim and makes the projection exact.

Set d=2^L-1, the number of proper edge subsets of one length-L path. If g is absent from A, its gadget has d^{n_g} choices. If g is present, choose the complete path in n_g ways and all other paths in d^{n_g-1} ways. Consequently the number of forests above A is

C product over g in A of (n_g/d),  where C=product over g of d^{n_g}.

Thus the projected measure is **exactly** mu_w on H with w_g=n_g/d, and

Z_G(1)=C Z_H(w).                                               (2)

Conditional on A, choices in different gadgets are independent, because the preceding acyclicity criterion imposes no remaining condition connecting their partial paths.

**Transfer for individual distinct edges.** In each gadget choose one fixed path and one fixed edge a_g of it. Given g absent, that path is a uniform proper subset; exactly 2^{L-1}-1 such subsets contain a_g. Therefore

p0=(2^{L-1}-1)/d.

Given g present, the distinguished path is the complete one with probability 1/n_g. Otherwise its law is the same proper-subset law. Hence, with Y_g=1_{g in A},

E[X_{a_g} | A] = p0 + delta_g Y_g,

delta_g = (1-p0)/n_g = 2^{L-1}/(n_g d) > 0.                    (3)

For distinct macroedges g,h their gadgets have disjoint edge sets and independent choices conditional on A. Applying the conditional covariance identity gives

Cov_G(X_{a_g},X_{a_h}) = delta_g delta_h Cov_{H,w}(Y_g,Y_h).    (4)

This is an equality about two individual microedges. It does not assume that pairwise correlation extends to general increasing events.

**Density and equivalence.** W implies U, which implies B. Assume B and take any positive vector v on E(H). Along even L tending to infinity choose positive integers n_g(L) with n_g(L)/(2^L-1) tending to v_g, for example the nearest positive integer to v_g(2^L-1). Each constructed G is simple and bipartite. By B and (4), every distinct-edge covariance for H at these weights is nonpositive. For fixed finite H its covariance is a ratio of polynomials with denominator Z_H(w)^2>0, and is continuous at v. Taking the limit proves W. This proves all equivalences.

In contrapositive form, a strict weighted counterexample on a finite loopless multigraph would yield a finite **simple bipartite uniform** counterexample after sufficiently accurate rational approximation. The proof supplies no such counterexample. Nonnegative weights can be included by continuity or by deleting zero-weight edges.

**Exact transfer witness.** For a triangle with labeled macroedges 01,12,02 take L=2 and multiplicities (1,1,2). The resulting seven-vertex simple bipartite graph has edges

03,31,14,42,05,52,06,62.

It has 234 forests. Its macro activity vector is (1/3,1/3,2/3), with partition function 26/9; equation (2) reads 234=3^4*(26/9). For macroedges 01 and 02 their covariance is -2/169. For microedges 03 and 05 it is -4/1521, exactly (2/3)(1/3)(-2/169). The historical exact check independently enumerated all 256 microscopic subsets and all eight macro subsets using two acyclicity criteria. Its verification metadata is summarized in VERIFICATION.json; the program and raw output are not part of this prose edition.

## 2. Exact weighted certificates on K4

Label K4 edges a=01,b=02,c=03,d=12,e=13,f=23, using the same letters for weights. Every forest has at most three edges. Thus Z is one plus the sum of all edge weights plus the sum of all distinct two-edge products plus the sum of all three-edge products except the four triangles abd,ace,bcf,def. This completely specifies Z without any enumeration theorem.

There are two automorphism orbits of distinct edge pairs. Put S=1+c+e+f. Direct expansion yields

Delta(a,b) = (d S + e f)^2 + d S^2 + e f(1+e+f),              (5)

Delta(a,f) = (b e - c d)^2 + b e(1+b+e) + c d(1+c+d).        (6)

For completeness, equations (5) and (6) can be obtained by writing Z=A+aB+bC+abD (or with f replacing b); multiaffinity gives Delta=BC-AD. Substitution from the explicitly specified forest monomials and expansion gives the displayed polynomials. The historical verifier independently constructed that monomial list and checked polynomial equality coefficient by coefficient. These exact finite identities, together with the finite monomial characterization, are mathematical proofs, not numerical sampling of weight values.

Every term on the right is nonnegative for nonnegative weights, and for positive weights the displayed nonsquare terms are strictly positive. K4 therefore has strictly negative correlation for any distinct pair at all positive weights. Relabeling by a vertex permutation covers every pair. This is an independently authored verification of a known result, not a new K4 theorem.

At unit weights N=38 and N_a=14. The incident joint count is 4, so Delta(a,b)=196-152=44 and covariance=-11/361. The disjoint joint count is 5, so Delta(a,f)=196-190=6 and covariance=-3/722.

## 3. Closure operations and a proved infinite family

Call a loopless weighted forest graph Rayleigh if all its Delta polynomials are nonnegative at all positive activities. The following elementary arguments prove closure under the specified operations. Intermediate multigraphs are allowed explicitly; the original target is recovered for the simple final graphs at unit weights.

For an edge x=uv of a graph write Z=A+xB. Here A counts all forests after deleting x, and B counts those forests of the deleted graph in which u and v are disconnected. Adding x gives a bijection from those forests to forests containing x. In particular A>=B>0 at nonnegative activities, with both having the empty monomial.

**Parallel replacement.** Replace x by two parallel edges a,b. A forest can use neither or exactly one, so Z'=A+(a+b)B=Z(a+b). For two old edges, the Rayleigh difference is the old one at x=a+b. For a new edge a and an old i it is Delta_Z(x,i). For the new pair it is B^2. All are nonnegative. Iteration covers more parallel edges.

**Series replacement.** Replace x by a two-edge path with weights a,b and a new internal vertex. If both edges are not chosen, the proper subsets contribute 1+a+b and the old deleted graph may have any forest. If both are chosen, u,v must have been disconnected. Thus

Z'=(1+a+b)A+abB = q Z(t),  q=1+a+b, t=ab/q.

For old i,j, Delta_{Z'}(i,j)=q^2 Delta_Z(i,j) at x=t. For new a and old i, differentiation and cancellation gives

Delta_{Z'}(a,i)=q^2 (partial t/partial a) Delta_Z(x,i)
               =b(1+b) Delta_Z(x,i).

The new pair has Delta_{Z'}(a,b)=A^2-AB=A(A-B)>=0. The argument with a,b exchanged is the same. Thus subdivision preserves the weighted property.

**Disjoint unions and one-vertex unions.** Every cycle stays in one factor, so the partition functions multiply. An internal Rayleigh difference acquires the square of the other factor, and a cross-factor difference is zero. These operations preserve the property.

**Edge two-sums.** Let G1,G2 have distinguished nonloop edges x1=u1v1,x2=u2v2. Start with disjoint copies, remove these two edges, identify u1 with u2 and v1 with v2, and make no other identifications. All other edges retain their labels. Write Z_i=A_i+x_i B_i as above. The deleted-side forest either disconnects the two terminals (weight B_i) or connects them (weight A_i-B_i). The union is cyclic exactly when both sides connect the terminals: each side is a forest with a unique terminal path, and their union then gives a cycle; any cross-side cycle conversely supplies both paths. Therefore

Z = A1 A2 -(A1-B1)(A2-B2)
  = B2 [ A1 + ((A2-B2)/B2) B1 ].                              (7)

For two edges from side 1 its Rayleigh difference is B2^2 times that of G1, evaluated at x1=(A2-B2)/B2>=0. Boundary value zero is handled by continuity. The side-2 case is symmetric.

For a cross pair g on side 1 and h on side 2, put r_i=A_i/B_i. Then r_i>=1 and Z=B1 B2(r1+r2-1). Direct differentiation gives

partial_g r1 = (B1 partial_g A1-A1 partial_g B1)/B1^2
             = Delta_{Z1}(x1,g)/B1^2,

and the analogous formula for side 2. Since log Z=log B1+log B2+log(r1+r2-1),

partial_g partial_h log Z
 = -(partial_g r1)(partial_h r2)/(r1+r2-1)^2.

Multiplying its negative by Z^2 proves the exact polynomial identity

Delta_Z(g,h)=Delta_{Z1}(x1,g) Delta_{Z2}(x2,h)>=0.              (8)

All denominators used are positive. This proves two-sum closure without assuming general negative association.

**Minors.** Edge deletion specializes its activity to zero, so the required differences follow by continuity. For contraction of a nonloop x, the forest polynomial is B=Z_x, allowing loops created by contraction to be discarded because no forest uses them. Divide Delta_Z(g,h) by x^2 and let x tend to infinity to get Delta_B(g,h)>=0. Thus the class is minor-closed as well.

**Corollary.** Every graph obtained from single edges and copies of K4 by finitely many of the preceding operations has pairwise negative correlation for its positive-weighted forest measure, and hence, when simple, satisfies the original unit-weight target. This includes series-parallel graphs and series-parallel extensions of K4. The family and the closure principles are established prior mathematics: Erickson (2012), p.76, credits the K4-extension family to Semple–Welsh and two-sum closure to Cocks/Wagner. Equations (5)–(8) are a self-contained verification here. This is not a claim that the construction covers all graphs.

## 4. Concrete obstructions to tempting general proofs

**Real stability already fails on a triangle.** Its forest polynomial is

P(a,b,c)=1+a+b+c+ab+ac+bc.

Set a=b=c=z=(-3+i sqrt(3))/6. Then Im(z)>0 and P(z,z,z)=1+3z+3z^2=0. Therefore P is not real stable. The strong-Rayleigh theorem cannot be applied by simply asserting that forest polynomials are stable. This does not contradict ordinary Rayleigh inequalities at positive real weights; for example Delta_P(a,b)=c+c^2>=0.

**Coefficientwise Rayleigh positivity already fails on K4.** Expanding (6), the coefficient of bcde is -2. Thus a proof that every forest Rayleigh polynomial has only nonnegative coefficients is false. Nevertheless the exact square in (6) proves its pointwise nonnegativity. The witness is a refutation of this stronger algebraic shortcut, not a counterexample to forest negative correlation.

**A root vertex changes the measure.** Add a new root joined to each vertex v of G with positive edge weight r_v. Take a weighted spanning tree of this augmented graph and remove the root. If the remaining forest has components C, exactly one root edge must meet each component. Summing over choices gives its marginal weight

w^F product over components C of (sum over v in C of r_v).

This generally differs from w^F. Even on K3 no fixed positive root-edge weights make it uniform: equality between the empty forest and each one-edge forest would require 1/r1+1/r2=1, 1/r1+1/r3=1, 1/r2+1/r3=1, hence r1=r2=r3=2. Then the empty forest factor is 8 but each spanning-tree factor is 6, a contradiction. With all r_v=1, K3 has seven unrooted forests but total rooted multiplicity 16, distributed by component sizes. The spanning-tree determinantal law therefore does not establish the target by this unmodified projection.

## 5. Remaining gap, prior work, and dependency boundary

The main gap is unchanged: Delta_G(e,f)>=0 at positive real weights for arbitrary finite graphs, equivalently the original uniform-simple target by Theorem 1. Neither sparse coefficient tests, bipartiteness, rooting, nor the proved family closes it. No graph outside the stated finite checks was searched exhaustively, and no counterexample to the target was found or claimed.

Corpus 30006450 / OWR-14299575-001 has the same first polynomial question at the all-one vector; its further interpolation-class question is broader. The pairwise result must not be double-counted across those records. This overlap supplies no second solved problem: the general pairwise question remains unresolved by this work, and the broader interpolation-class question is not addressed. No novelty is claimed.

External sources establish statement, history, and present-day scope only; the mathematical results proved here depend solely on the explicit finite polynomial identities, counting, elementary differentiation, and continuity. No author code was executed. The historically inspected recent papers remain scope statements rather than audited general proofs. Source text and PDFs are not distributed; the authored exposition is self-contained.

### Public references

- Grimmett and Winkler, *Negative Association in Uniform Forests and Connected Graphs*, arXiv:math/0302185v3, https://arxiv.org/abs/math/0302185 . Primary exact measure and distinct-edge formulation, pp.1–3.
- Erickson, *Sums of squares and negative correlation for spanning forests of series parallel graphs*, Australasian Journal of Combinatorics 52 (2012), 75–87, https://ajc.maths.uq.edu.au/pdf/52/ajc_v52_p075.pdf . Historical attribution on p.76; no proof theorem from this source is needed for the self-contained derivations above.
- Wagner, *Negatively correlated random variables and Mason's conjecture*, arXiv:math/0602648v1, https://arxiv.org/abs/math/0602648 . Weighted formulation and prior closure context.
- Cocks, *Correlated Matroids*, Combinatorics, Probability and Computing 17 (2008), 511–518, https://doi.org/10.1017/S0963548308009152 . Publisher abstract inspected; full proof not retrieved in this investigation.
- Huang, *On Negative Correlation of Arboreal Gas on Some Graphs*, arXiv:2311.00965v1, https://arxiv.org/abs/2311.00965 . Structural reductions, with relevant proof passages on pp.12–13 checked for prior scope, not adopted as proof dependencies.
- Gupta, *Edges of the uniform random forest of K_n are pairwise negatively correlated for every n*, arXiv:2609.26134v1, https://arxiv.org/abs/2609.26134 . Complete-host claim only; retained PDF literally displays August 2026 metadata despite its identifier. No source code or all-n proof audited here.
- Çiçeksiz and Ravichandran, *Negative Correlations for Forests and the q<1 Random-Cluster Model*, arXiv:2610.00549v1, https://arxiv.org/abs/2610.00549 . Relevant abstract and scope statements inspected; does not supply an established general unit-forest result here.
- *Arbeitsgemeinschaft: Combinatorial Hodge Theory*, Oberwolfach Report 47/2025, https://doi.org/10.4171/owr/2025/47 . Overlap source; corpus display year and primary report year must not be silently conflated.
