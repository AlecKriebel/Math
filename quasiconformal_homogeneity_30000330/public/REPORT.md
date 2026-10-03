# Quasiconformal homogeneity gaps for hyperbolic surfaces

## Conclusion and exact question

**Unresolved after five substantive attempts.** The work below proves neither the existence nor the nonexistence of the universal gap. The literature search, checked 3 October 2026, located affirmative results under additional hypotheses but no resolution of the full question. This is a bounded search conclusion, not a certification that no later or unpublished solution exists.

For a connected complete hyperbolic surface without boundary, put

\[
K(S)=\inf\{K\geq1:\ \forall x,y\in S\ \exists f:S\to S,
\ f(x)=y,\ K(f)\leq K\}.
\]

The maps are quasiconformal homeomorphisms. We use the standard orientable Riemann-surface convention of the cited papers, with orientation-preserving quasiconformal maps. The problem is already unresolved in this class; no assertion about a separately enlarged nonorientable convention is needed or proved here.

The target asks whether there is **one** constant \(K_2>1\) valid for every such uniformly quasiconformally homogeneous \(S\ne\mathbb H^2\). It does not assume compactness, fixed genus, a conformal symmetry, or a prescribed mapping class. The hyperbolic plane must be excluded because its conformal automorphisms act transitively. A different lower bound for each individual surface, or for each fixed genus, is insufficient.

The primary question occurs after Theorem 3 in Canary's contribution to [OWR], printed p. 2534. The workshop/report year is 2005; the publisher gives publication in 2006.

## Established inputs and their scope

We distinguish ordinary homogeneity from strong homogeneity, which only allows maps homotopic to conformal automorphisms, and extreme homogeneity, which only allows maps homotopic to the identity. Their constants obey

\[
K(S)\leq K_{\rm aut}(S)\leq K_0(S).
\tag{1}
\]

The following inputs are used with their original restrictions.

1. [B05, Theorem 1.1 and Corollary 1.2] gives positive lower and finite upper injectivity-radius bounds for each fixed homogeneity constant. Except for \(\mathbb H^2\), a uniformly quasiconformally homogeneous surface with finitely generated fundamental group is closed. Infinite-type examples exist, including noncompact regular covers of closed surfaces. Thus a closed-surface result alone would not finish the target.
2. [B07, Proposition 3.2] gives the essential escape condition
   \[
   K(S_j)\longrightarrow1\quad\Longrightarrow\quad
   \ell(S_j)\longrightarrow\infty,
   \tag{2}
   \]
   where \(\ell\) is the infimum of lengths of nontrivial loops. The same paper proves a uniform gap for closed surfaces having at least \(c(g+1)\) fixed points of a nontrivial conformal automorphism, for fixed \(c>0\). This includes hyperelliptic surfaces.
3. [KM, Theorem A] proves a uniform gap for all genus-zero hyperbolic surfaces other than the disk, including infinite-type planar surfaces. Its proof uses separating curves and even intersection numbers; it is not a proof for positive genus.
4. [BMRT, Theorem 2.3] identifies the sharp infimum of **strong** homogeneity constants as approximately \(1.36138\), not attained by a surface other than \(\mathbb H^2\). By (1), this is not a lower bound on ordinary \(K(S)\).
5. [V, Theorems 1.2, 1.5 and 1.6] proves uniform gaps for closed surfaces with maps restricted to Torelli or level-at-least-three congruence subgroups, finite subgroups, or pure cyclic subgroups. [V, Theorem 1.3] makes a genus-linear small-displacement mapping-class count a sufficient condition for a gap on all closed surfaces. That counting hypothesis is not supplied by the theorem.
6. [S, Section 5] explicitly separates the known fixed-genus bound from the question of a genus-independent bound and from the all-surface question. The recent paper [FH] studies geometric function theory on homogeneous Euclidean domains; the inspected abstract and introduction do not claim the present gap theorem.

No known input is labeled a new result of this investigation.

## Attempt 1 Compactness and escaping topology

**Proposed route.** Pass to a geometric limit of surfaces with \(K(S_j)\to1\) and contradict their nontrivial topology.

Equation (2) explains exactly why the naive contradiction fails: every fixed-radius pointed ball eventually becomes a disk. The allowed geometric limit is \(\mathbb H^2\), although every surface in the sequence is different from it. Nontrivial topology need not survive pointed convergence.

There is nevertheless a rigorous fixed-genus consequence. On a closed genus-\(g\) surface, every open ball of radius less than \(\ell(S)/2\) embeds. Its area is \(2\pi(\cosh r-1)\), whereas Gauss-Bonnet gives \(\operatorname{area}(S)=4\pi(g-1)\). Letting \(r\uparrow\ell(S)/2\) gives

\[
\ell(S)\leq2\operatorname{arccosh}(2g-1).
\tag{3}
\]

Consequently, a closed counterexample sequence must have \(g_j\to\infty\). More generally, (2) implies a gap on any class with a common finite systole upper bound. Indeed, otherwise choose one surface in that class with constant below \(1+1/j\); this contradicts (2). The gap may depend on that upper bound.

**Outcome.** Fixed genus and bounded systole are excluded. The missing assertion is a uniform obstruction when both genus and systole diverge, or for infinite-type surfaces. The compactness argument alone does not supply one.

## Attempt 2 Regular covers as possible counterexamples

**Proposed route.** Use increasingly large regular covers of one closed surface to make all local geometry nearly identical, and hope this forces \(K\to1\).

Here is an exact test of that idea. Let \(M\to S\) be a finite regular hyperbolic cover and \(D=\operatorname{diam}(S)\). Write \(\ell=2\inf_p\operatorname{inj}_M(p)\) and \(d=2\sup_p\operatorname{inj}_M(p)\). Take a point \(p\) on a systolic geodesic, so \(\operatorname{inj}_M(p)=\ell/2\). For any \(q\), lift a base geodesic of length at most \(D\) from its projection to the projection of \(p\). Its other endpoint is a deck translate \(p'\) of \(p\). The injectivity-radius function is 1-Lipschitz, hence

\[
\ell\leq d\leq\ell+2D.
\tag{4}
\]

Residual finiteness removes the finitely many conjugacy classes of base geodesics of length at most any prescribed \(L\), producing finite normal covers with \(\ell\to\infty\). Thus (4) gives \(d/\ell\to1\). This recovers the obstruction in [B05, Lemma 6.2].

Regularity also permits a common finite homogeneity upper bound: uniformly bounded identity-isotopic maps on the compact base lift to the cover, and deck transformations adjust the target within its fiber. But neither that bound nor (4) tends to 1.

**Outcome.** The proposed covers disprove a hoped-for universal bound \(d/\ell\geq1+\epsilon\), not the requested quasiconformal gap. Uniform local geometry and convergence to the disk do not control the least distortion needed to move arbitrary points globally. No counterexample sequence was produced.

## Attempt 3 Approximation by conformal automorphisms

**Proposed route.** Repeat the higher-dimensional argument by replacing a low-dilatation map with a nearby conformal automorphism.

Let \(D_0(K)\) denote a universal upper bound on hyperbolic displacement of a \(K\)-quasiconformal disk map whose boundary extension is the identity, chosen increasing with \(D_0(K)\to0\) as \(K\downarrow1\). Such a function is a standard input; see [B07, Proposition 6.2]. For a closed surface, if \(f\) is homotopic to a conformal automorphism \(a\), apply that estimate to the canonical lift of \(a^{-1}f\). It yields

\[
d_S(f(x),a(x))\leq D_0(K(f)).
\tag{5}
\]

Under strong \(K\)-homogeneity, the quotient by conformal automorphisms therefore has diameter at most \(D_0(K)\). The positive diameter bound for hyperbolic orbifolds then gives a gap. The full strong theorem is [BMRT].

**Outcome.** The proof needs the homotopy restriction at (5). Small dilatation alone has not been shown to place the map in a conformal automorphism class uniformly over all surfaces. A lower bound on \(K_{\rm aut}\) cannot be transferred through (1) in the reverse direction. No unrestricted rigidity statement was proved.

## Attempt 4 Counting low-dilatation mapping classes

**Proposed route.** Replace the unavailable individual rigidity in Attempt 3 by a count of possible homotopy classes.

We give a deliberately non-sharp elementary covering estimate, avoiding any isodiametric assertion about subsets of a quotient surface. For a closed genus-\(g\) surface \(S\), let \(N_S(K)\) be the number of mapping classes represented by self-maps with dilatation at most \(K\). This is finite: bounded closed Teichmuller balls are compact and the mapping class group acts properly with finite stabilizers. Suppose \(S\) is \(K\)-homogeneous, with \(K>1\).

Choose one representative \(f_i\) of dilatation at most \(K\) for each such class, and fix \(x\in S\). For every \(y\), homogeneity supplies \(f(x)=y\). If \([f]=[f_i]\), the map \(h=f\circ f_i^{-1}\) is homotopic to the identity and satisfies

\[
K(h)\leq K^2,\qquad h(f_i(x))=y.
\]

The canonical boundary-fixing lift and the definition of \(D_0\) give

\[
S=\bigcup_{i=1}^{N_S(K)} B_S(f_i(x),D_0(K^2)).
\]

Metric balls in a hyperbolic quotient have area at most that of the corresponding disk in \(\mathbb H^2\), even if they are not embedded. Therefore

\[
N_S(K)\geq
\frac{2(g-1)}{\cosh D_0(K^2)-1}.
\tag{6}
\]

Every closed counterexample sequence must consequently satisfy

\[
\frac{N_{S_j}(K_j)}{g_j-1}\longrightarrow\infty.
\tag{7}
\]

For example, if the allowed classes lie in a finite subgroup, Hurwitz and Nielsen realization bound their number by \(84(g-1)\). Equation (6) then forces \(D_0(K^2)\geq\operatorname{arccosh}(43/42)>0\), recovering a non-sharp restricted gap. This is consistent with, and weaker than, [V]'s sharper estimate.

A bound \(N_S(K_*)\leq C(g-1)\), for some fixed \(K_*>1\) on all sufficiently large-systole closed surfaces, would contradict (7) and finish the closed case. We have not proved that bound. Finiteness for each \(S\) gives no such uniform growth control. A finite-index congruence subgroup also does not automatically inherit a transitive family with the same distortion budget; composing maps multiplies dilatations, and the index grows with genus.

**Outcome.** Equations (6)-(7) are rigorous necessary conditions, in the spirit of the existing counting approach. The required upper bound remains missing, and even a closed-case success would leave infinite type.

## Attempt 5 Short-curve coverage and the planar proof

**Proposed route.** Use the transitive images of one shortest geodesic to cover the surface by narrow tubes, then force an impossible curve configuration.

For a closed surface choose a systolic geodesic \(\gamma\) of length \(\ell\), and let \(m_S(K,\gamma)\) count the distinct geodesic representatives of \(f(\gamma)\) as \(f\) runs over self-maps with \(K(f)\leq K\). This number is finite because the length spectrum below a fixed bound is finite. Wolpert's estimate gives length at most \(K\ell\); the geodesic-straightening estimate supplies a universal \(C(K)\to0\) as \(K\to1\), with \(f(\gamma)\) inside the \(C(K)\)-neighborhood of its geodesic representative [KM, Lemmas 2.3 and 2.5].

Fix \(x\in\gamma\). Transitivity implies that the union of those tubes covers \(S\). A radius-\(r\) tube about a closed geodesic of length \(L\) has area at most \(2L\sinh r\): integrate the Fermi-coordinate area element \(\cosh t\,ds\,dt\); overlaps can only reduce the area of the image. Hence

\[
4\pi(g-1)\leq 2m_S(K,\gamma)K\ell\sinh C(K),
\]

and, using (3),

\[
m_S(K,\gamma)\geq
\frac{2\pi(g-1)}{K\ell\sinh C(K)}
\geq\frac{\pi(g-1)}{K\operatorname{arccosh}(2g-1)\sinh C(K)}.
\tag{8}
\]

Thus a closed counterexample sequence needs

\[
\frac{m_{S_j}(K_j,\gamma_j)\ell(S_j)}{g_j-1}\longrightarrow\infty.
\tag{9}
\]

The tempting next claim, that only \(O((g-1)/\ell)\) such near-systolic geodesics can occur uniformly, was not established. Counting pants curves does not prove it: the relevant geodesics need not be disjoint or belong to one pants decomposition.

The planar theorem cannot close this gap for positive genus. On a closed genus-two surface take standard simple curves \(a_1,b_1\) around one handle with algebraic intersection 1. Their minimal geometric intersection is also 1. This explicitly violates the even-intersection and separating-curve properties used in [KM, Lemma 2.1]. It is a counterexample to the proposed transfer of that topological step, not to the homogeneity conjecture. For infinite-area surfaces the finite total-area argument in (8) is unavailable as well.

**Outcome.** A second necessary proliferation condition is proved. The geometric/combinatorial upper bound needed to contradict it, and an infinite-type replacement for the area argument, remain open in this work.

## What would resolve the problem

An affirmative answer requires a topology-independent obstruction to transitive families with \(K\) arbitrarily close to 1, covering infinite type as well as unbounded closed genus. A negative answer requires actual surfaces \(S_j\ne\mathbb H^2\) and globally defined transitive families with verified \(K_j\to1\). None of the constructions or estimates above supplies either deliverable.

The computations accompanying this report only check algebraic constants and finite exact instances of the area identities. They do not verify compactness, quasiconformal estimates, residual finiteness, or the universal conclusion. No numerical candidate for \(K_2\) is asserted.

## References

- [OWR] R. D. Canary, contribution *Quasiconformal Homogeneity of Hyperbolic Manifolds*, pp. 2533-2535 in *Low-Dimensional Manifolds*, Oberwolfach Reports 2 (2005), no. 4, 2519-2570. [Publisher and DOI](https://ems.press/journals/owr/articles/1106), [10.4171/OWR/2005/45](https://doi.org/10.4171/OWR/2005/45).
- [B05] P. Bonfert-Taylor, R. D. Canary, G. Martin, E. C. Taylor, *Quasiconformal homogeneity of hyperbolic manifolds*, Mathematische Annalen 331 (2005), 281-295. [Author manuscript](https://websites.umich.edu/~canary/quasi.pdf).
- [B07] P. Bonfert-Taylor, M. Bridgeman, R. D. Canary, E. C. Taylor, *Quasiconformal homogeneity of hyperbolic surfaces with fixed-point full automorphisms*, Mathematical Proceedings of the Cambridge Philosophical Society 143 (2007), 71-84. [Author manuscript](https://websites.umich.edu/~canary/full.pdf), [10.1017/S0305004107000138](https://doi.org/10.1017/S0305004107000138).
- [KM] F. Kwakkel, V. Markovic, *Quasiconformal Homogeneity of Genus Zero Surfaces*, Journal d'Analyse Mathematique 113 (2011), 173-195. [arXiv:0910.1050](https://arxiv.org/abs/0910.1050), [10.1007/s11854-011-0003-1](https://doi.org/10.1007/s11854-011-0003-1).
- [BMRT] P. Bonfert-Taylor, G. Martin, A. W. Reid, E. C. Taylor, *Teichmuller Mappings, Quasiconformal Homogeneity, and Non-amenable Covers of Riemann Surfaces*, Pure and Applied Mathematics Quarterly 7 (2011), 455-468. [Author manuscript](https://web.ma.utexas.edu/users/areid/Kautfinal07.pdf).
- [V] N. G. Vlamis, *Quasiconformal homogeneity and subgroups of the mapping class group*, Michigan Mathematical Journal 64 (2015), 53-75. [arXiv:1309.7026](https://arxiv.org/abs/1309.7026), [10.1307/mmj/1427203285](https://doi.org/10.1307/mmj/1427203285).
- [S] P. Bonfert-Taylor, R. D. Canary, E. C. Taylor, *Quasiconformal homogeneity after Gehring and Palka*. [arXiv:1401.3662](https://arxiv.org/abs/1401.3662), [Author manuscript](https://dept.math.lsa.umich.edu/~canary/GehringFinal.pdf).
- [FH] A. N. Fletcher, A. M. Hahn, *Geometric function theory on uniformly quasiconformally homogeneous domains*, Journal of Mathematical Analysis and Applications 554 (2026), article 129960. [10.1016/j.jmaa.2025.129960](https://doi.org/10.1016/j.jmaa.2025.129960).
