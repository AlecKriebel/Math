# Kirby Problem 4.38: five attempts and the surviving obstruction

**Problem:** 2914 / KP-4.38. **Outcome:** unresolved after five substantive approaches. No proof or counterexample to the general question is claimed. The lemmas below are elementary partial results and method checks; no novelty claim is made.

## 1. Exact question and scope

For a ribbon disk \(\Delta\subset B^4\), is \(B^4\setminus\Delta\) aspherical, meaning that \(\pi_i(B^4\setminus\Delta)=0\) for every \(i>1\)? This is Problem 4.38 on printed page 221 of the 2026 K3 list [K3], corresponding to Kirby's 1997 Problem 1.103.

We use the usual smooth/PL ribbon-disk setting. Replacing the complement by the exterior obtained by removing an open tubular neighborhood does not change its homotopy type: radially push each nonzero normal vector out to the boundary of a smaller tubular neighborhood. The locally flat homotopy-ribbon variant mentioned in [K3] is not silently substituted for this question. In particular, its possible lack of a 2-dimensional homotopy model is a separate issue.

The K3 remarks explicitly flag an incorrect earlier general proof. The primary 2026 article [HR26, introduction and §4] also describes asphericity of arbitrary LOT complexes as unresolved. Neither statement proves that no later solution exists, but both prevent treating an old blanket assertion as an established theorem.

## 2. The LOT model and the exact target

A labeled oriented tree \(T\) consists of a finite tree with vertex set \(V\), an orientation on each edge, and a label \(\lambda(e)\in V\) on each edge. Write an edge as \((s,t;\ell)\), where \(s\) is its source, \(t\) its target, and \(\ell\) its label. Its presentation complex is

\[
K(T)=K\langle x_v\ (v\in V)\mid x_sx_\ell x_t^{-1}x_\ell^{-1}\ (e\in E)\rangle.
\]

There is one 0-cell, \(n=|V|\) 1-cells and \(n-1\) 2-cells. Ribbon-disk complements have this homotopy type; conversely LOT complexes arise from ribbon disks. The geometric description and its conversion into this presentation are explained in [B11, §§1–2 and Appendices A–B], and the same model is used in [HR17, §1] and [HR26, §4]. The relator here is a cyclic conjugate of the convention in [B11], so the presentation complexes agree up to changing the starting point of a cell boundary.

Let \(G=\pi_1K(T)\). Since its universal cover \(\widetilde K\) is simply connected and 2-dimensional,

\[
K(T)\text{ is aspherical}\quad\Longleftrightarrow\quad
H_2(\widetilde K;\mathbb Z)=0.
\tag{1}
\]

Indeed Hurewicz identifies \(\pi_2\widetilde K\) with \(H_2\widetilde K\). If the latter vanishes, all reduced homology vanishes; a first nonzero higher homotopy group would contradict Hurewicz. Whitehead's theorem then makes the universal cover contractible.

## 3. Attempt 1: ordinary homology and the tree incidence matrix

The ordinary cellular boundary of the cell for \((s,t;\ell)\) is \(e_s-e_t\), including when the label equals an endpoint. Thus the degree-two cellular boundary is precisely an oriented incidence matrix of the underlying tree.

Delete the column of one fixed root vertex. The resulting \((n-1)\times(n-1)\) incidence matrix has determinant \(\pm1\). A proof is induction by deleting a leaf other than the root and expanding along its column; the one-vertex case has empty determinant 1. Consequently the boundary is injective and its cokernel is \(\mathbb Z\). Hence

\[
H_1(K(T);\mathbb Z)=\mathbb Z,\qquad H_i(K(T);\mathbb Z)=0\quad(i\ge2).
\tag{2}
\]

**Outcome and gap.** This establishes homology of a circle for every LOT complex. It does not compute the homology of its universal cover. Applying the simply connected Hurewicz theorem directly to \(K(T)\) would be invalid, since its fundamental group is not trivial. The next attempt seeks a stronger topological embedding rather than repeating that inference.

## 4. Attempt 2: add a meridian and try to inherit contractibility

Attach one extra 2-cell to \(K(T)\) along the generator at the chosen root. Call the result \(L\). Its fundamental group is trivial: killing one vertex generator kills each adjacent generator by the conjugacy relation, and connectedness of the tree propagates this to every vertex. The ordinary boundary of \(L\) is the incidence matrix together with the root vector. It is unimodular by the same leaf induction. Thus \(L\) is simply connected and acyclic, so it is contractible by Hurewicz and Whitehead.

This gives a direct proof that each \(K(T)\) is a subcomplex of a finite contractible 2-complex.

**Outcome and gap.** The remaining inference that this subcomplex is aspherical is an instance of Whitehead's asphericity conjecture, not an available theorem. The inclusion into \(L\) kills \(\pi_1K(T)\), so it cannot identify the universal cover of \(K(T)\) with a subspace merely by lifting an injective fundamental-group map. The construction explains the relation to Whitehead's question without settling it.

## 5. Attempt 3: an exact infinite-cyclic-cover calculation

Send every generator to \(t\) to obtain the abelianization \(G\twoheadrightarrow\mathbb Z\). Let \(K_\infty\) be the associated connected cover and put \(R=\mathbb Z[t,t^{-1}]\). Use row vectors for cellular 2-chains. The Fox boundary matrix \(A(t)\) has one row for each edge:

\[
A_{e,v}(t)=\mathbf1_{v=s}+(t-1)\mathbf1_{v=\ell}-t\mathbf1_{v=t(e)}.
\tag{3}
\]

Here \(t(e)\) denotes the target vertex, to distinguish it from the Laurent variable. If indices coincide their contributions are added. Formula (3) follows from the Fox derivatives of \(x_sx_\ell x_t^{-1}x_\ell^{-1}\): the two label contributions become \(t\) and \(-1\), and the inverse-target contribution becomes \(-t\).

Delete the root column to form \(M(t)\). Specializing at \(t=1\) gives the root-deleted incidence matrix, so

\[
\det M(1)=\pm1.
\]

In particular \(\det M(t)\ne0\). Since \(R\) is an integral domain, \(M(t)\) is injective as a map between finite free \(R\)-modules (multiply by its adjugate, or pass to its fraction field). Therefore \(A(t)\) is injective. There are no 3-cells, and we obtain the unconditional result

\[
H_2(K_\infty;\mathbb Z)=0.
\tag{4}
\]

If \(G\cong\mathbb Z\), this is the universal cover, proving asphericity in that special case by (1). This also includes the one-vertex LOT.

**Outcome and gap.** In general \(\pi_1(K_\infty)=[G,G]\), not the trivial group. Its vanishing second homology does not supply (1). No injectivity of the group-ring boundary follows merely from injectivity after the quotient of coefficients \(\mathbb ZG\to R\). In particular a nonzero 2-cycle over \(\mathbb ZG\) could have all its coefficients map to zero in \(R\).

## 6. Attempt 4: reduction, injectivity and a concrete forest-test obstruction

The established theorem [HR17, Theorems 1.1 and 5.1] covers injective LOTs: each vertex is used at most once as an edge label. Its proof uses reductions, relative vertex asphericity, and an induction through proper sub-LOTs with the necessary fundamental-group injections. None of those hypotheses can be removed by just calling the underlying unlabeled graph a tree.

To test a direct extension, consider the path with vertices \(a,b,c,d,e\), all edges initially oriented to the right, and labels

\[
(a,b;c),\quad (b,c;e),\quad(c,d;a),\quad(d,e;c).
\tag{5}
\]

This is compressed: no edge has its endpoint as a label. It is boundary reduced: both leaves \(a,e\) occur as labels. It is interior reduced: adjacent edges have different labels. It is not injective, since \(c\) labels two edges. There is no proper nontrivial sub-LOT: any connected proper subtree is an interval in the path, and each such interval has an edge whose label lies outside it. These claims can be checked on its nine proper intervals containing an edge: four of length one, three of length two, and two of length three.

The positive and negative link graphs of a compressed LOT presentation have, respectively, the pairs \(\{s,\ell\}\) and \(\{t,\ell\}\) as their edges, counted with multiplicity. The direct Stallings criterion requires both graphs to be forests [HR17, Definition 3.4]. Initially the positive graph has two \(ac\) edges and the negative graph has two \(ce\) edges.

A stronger simple tactic is to invert any subset of the five generators, a homeomorphism of the presentation complex. For the link graphs this has the same effect as reversing all LOT edges with labels in that subset [HR17, Lemma 4.7]. Edges carrying the repeated label \(c\) must therefore be reversed together. Let \((A,E,C)\in\{0,1\}^3\) record inversion of generators \(a,e,c\). Inversions of \(b,d\) do not change these link graphs. For all eight possibilities a cycle survives:

| \(A,E,C\) | A surviving link cycle |
|---|---|
| 0,0,0 | positive double edge \(ac\) |
| 0,0,1 | positive triangle \(bce\) |
| 0,1,0 | positive double edge \(ac\) |
| 0,1,1 | positive double edge \(ce\) |
| 1,0,0 | negative double edge \(ce\) |
| 1,0,1 | negative double edge \(ac\) |
| 1,1,0 | positive triangle \(acd\) |
| 1,1,1 | positive double edge \(ce\) |

The accompanying script independently constructs links from the actual signed relator words and checks all 32 generator-inversion subsets. It also checks all 16 independent edge reorientations: precisely the reversal patterns \((0,0,1,1)\) and \((1,1,0,0)\) make both links forests. Neither is compatible with reversing the two \(c\)-labeled edges together.

**Outcome and gap.** Standard reductions followed by this generator-inversion forest test do not prove asphericity for (5). This is a counterexample only to that proposed universal tactic. It is not a counterexample to asphericity, nor a claim that this particular small LOT is unresolved by other methods. More general changes of presentation, weight tests and geometric criteria are not excluded. For comparison, the root-deleted cyclic determinant in (5) is \(\pm t(t^2-t+1)\), so (4) still holds.

## 7. Attempt 5: the universal group ring and why completion is insufficient

Let \(S=\mathbb ZG\). With coefficients on the left of chosen cells, a cellular 2-chain is a row \(u\in S^{n-1}\), and its boundary is \(uA_G\). The Fox matrix in the actual group is

\[
(A_G)_{e,v}=\mathbf1_{v=s}+(x_s-1)\mathbf1_{v=\ell}-x_\ell\mathbf1_{v=t(e)}.
\tag{6}
\]

The simplifications use the relation \(x_sx_\ell=x_\ell x_t\); endpoint coincidences are again handled by adding contributions. The boundary identity follows directly:

\[
(x_s-1)+(x_s-1)(x_\ell-1)-x_\ell(x_t-1)
=x_sx_\ell-x_\ell x_t=0.
\]

There are no 3-cells, hence

\[
\pi_2K(T)\cong\ker\big(S^{n-1}\xrightarrow{u\mapsto uA_G}S^n\big).
\tag{7}
\]

Equation (7) is an exact algebraic formulation of the missing universal assertion.

Let \(I=\ker(S\xrightarrow{\epsilon}\mathbb Z)\) be the augmentation ideal. Delete the root column of \(A_G\), obtaining \(M\). The integral matrix \(U=\epsilon(M)\) is unimodular. Thus

\[
MU^{-1}=1+C,\qquad C\in\operatorname{Mat}_{n-1}(I).
\]

If \(uA_G=0\), then \(uM=0\), so \(u=-uC\). Iterating gives \(u=(-1)^kuC^k\), and therefore every coordinate of \(u\) belongs to \(I^k\) for every \(k\). We have proved

\[
\ker A_G\subseteq\big(\bigcap_{k\ge1}I^k\big)^{n-1}.
\tag{8}
\]

It is tempting to make the right-hand side zero by assuming augmentation-adic separation. But this assumption cannot hold for a nonabelian LOT group, as follows.

**Lemma.** If a group has cyclic abelianization, then \(\gamma_2G=\gamma_3G=\gamma_4G=\cdots\), where \(\gamma_i\) is its lower central series. If the group is nonabelian, then \(\bigcap I^k\ne0\) in its integral group ring.

**Proof.** In \(G/\gamma_3G\), the commutator subgroup is central. Fix a lift \(x\) of a generator of the cyclic abelianization. Every element of this quotient is \(x^m c\) with \(c\) central in the commutator subgroup. All pairs of such elements commute, so the quotient is abelian. This shows \(\gamma_2G\subseteq\gamma_3G\), hence equality; the rest follows by induction from the definition of the lower central series.

For the group ring, the elementary inclusion \(g\in\gamma_kG\Rightarrow g-1\in I^k\) follows by induction from
\[
[u,v]-1=(uv-vu)u^{-1}v^{-1},\quad
uv-vu=(u-1)(v-1)-(v-1)(u-1),
\]
using the convention \([u,v]=uvu^{-1}v^{-1}\), and closure under products and inverses. If \(G\) is nonabelian, choose \(1\ne g\in\gamma_2G\). It lies in every \(\gamma_kG\), and \(g-1\ne0\) because distinct group elements form an integral basis of \(\mathbb ZG\). Thus \(g-1\in\bigcap I^k\) is nonzero. ∎

Since (2) makes the abelianization of every LOT group infinite cyclic, this lemma applies here. The formal inverse \((1+C)^{-1}=1-C+C^2-\cdots\) in a completion cannot be pulled back through an injective completion map in the nonabelian case: that map already has a nonzero kernel.

**Outcome and gap.** We have localized every possible universal 2-cycle in the augmentation-adic intersection, but that intersection is provably nonzero for any nonabelian LOT group. Its nonzero elements need not form a cycle in (7); hence they do not produce a counterexample either. The exact unresolved step is to establish injectivity in (7) for all LOTs, or exhibit a specific LOT and a nonzero group-ring vector in its kernel.

## 8. Final verdict and verification limits

All five approaches stop short of the general question. The results retained are (2), the contractible extension, (4) and its cyclic-group corollary, the finite obstruction to one forest-test tactic, and (8) with its nonseparation warning. These do not justify a solved status.

Run `python3 verify.py` in this directory to reproduce the exact checks. The script uses only the Python standard library. It checks the Fox formula in the finite test set stated in its output, the five determinant certificates for (5), reducedness and the nine proper intervals, all generator inversions and all edge reorientations, and the displayed free-group commutator identity. The general arguments are the proofs above, not extrapolations from these finite checks. No numerical test certifies the vanishing of (7).

## References

- [K3] R. İ. Baykur, R. C. Kirby and D. Ruberman (eds.), *K3: A New Problem List in Low-Dimensional Topology* (2026), Problem 4.38, printed p. 221. [Author-hosted text](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf).
- [B11] T. Bedenikovic, *Asphericity results for ribbon disk complements via alternate descriptions*, Osaka J. Math. 48 (2011), 99–125. [Publisher repository](https://ir.library.osaka-u.ac.jp/repo/ouka/all/4901/ojm48_01_099.pdf), [DOI](https://doi.org/10.18910/4901).
- [HR17] J. Harlander and S. Rosebrock, *Injective labeled oriented trees are aspherical*, Math. Z. 287 (2017), 199–214. [Full author manuscript, v6](https://arxiv.org/pdf/1212.1943v6), [DOI](https://doi.org/10.1007/s00209-016-1823-6). Numbering in this note follows the 24-page v6 manuscript.
- [HR26] J. Harlander and S. Rosebrock, *Local indicability in the presence of diagrammatic reducibility*, Canad. Math. Bull. (published online May 26, 2026). [DOI and primary publication](https://doi.org/10.4153/S0008439526102069). This supplies a recent primary status check; its conditional local-indicability results are not used to assert the general result.

The historical Howie local-indicability theorem is reported in [K3] and [HR26]. Its AMS full-text retrieval was blocked during this investigation, so no claim of a fresh audit of that proof is made. The elementary results in this note do not invoke it.
