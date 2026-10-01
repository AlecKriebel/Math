# Unbounded Godbillon–Vey numbers on one hyperbolic mapping torus

**Problem:** 10300044 / AMR-102-0044, Calegari, Question 10.6 (2002).  
**Status:** complete candidate negative answer to the printed question; independent review pending.  
**Attribution:** the nonzero suspension block is a classical consequence of Thurston and Mather, explicitly recorded by Tsuboi in 1981. The hyperbolization input is Thurston's theorem. No claim of priority is made for the assembly below.

## 1. Source scope and conclusion

Question 10.6 on printed p. 25 of [C] asks whether the Godbillon–Vey numbers of taut foliations of a hyperbolic manifold admit a uniform bound depending on the manifold's volume. It does not specify that the bound be linear. It also does not impose minimality, absence of compact leaves, or a transverse projective structure. The source's Definition 1.1 calls a foliation taut when a closed transversal meets every leaf. Its §13.1 uses the ordinary differential-form Godbillon–Vey invariant and notes that C² regularity suffices.

We work in the particularly unambiguous subclass of **closed, connected, oriented hyperbolic 3-manifolds and smooth cooriented codimension-one foliations**. Write

\[
 d\alpha=\alpha\wedge\eta,\qquad
 \operatorname{gv}(\mathcal F)=\int_M\eta\wedge d\eta,
 \qquad \ker\alpha=T\mathcal F.
\]

The class and its integral are independent of the defining forms.

**Theorem.** There are a fixed closed oriented hyperbolic 3-manifold \(M\), a number \(a>0\), and smooth cooriented taut foliations \(\mathcal F_N\) on \(M\), for every integer \(N\geq1\), such that
\[
 \operatorname{gv}(\mathcal F_N)=Na.
\]
The same embedded circle can be chosen as a closed transversal meeting every leaf of every \(\mathcal F_N\).

Consequently no finite bound depending only on volume, even a nonlinear one, can hold for the source's entire class. Fix any one hyperbolic metric on \(M\): its positive finite volume is independent of \(N\). The conclusion does not say that every hyperbolic 3-manifold has this property, and does not answer a separately restricted question about minimal foliations.

## 2. The precise classical input

Let \(G=\operatorname{Diff}^{\infty}_c(\mathbb R)\), regarded as a discrete group. These are orientation-preserving smooth diffeomorphisms with compact support; orientation preservation also follows from being the identity outside a compact interval.

We use the following classical facts in exactly the form recorded in [T81, printed pp. 1–3, 6]:

1. Thurston's Godbillon–Vey homomorphism on \(H_3(B\overline{\Gamma}_1^{\infty};\mathbb Z)\) is onto \(\mathbb R\), with the oriented/trivial-normal convention of that paper.
2. Mather's map
   \[
   H_2(G;\mathbb Z)\longrightarrow H_3(B\overline{\Gamma}_1^{\infty};\mathbb Z)
   \]
   is an isomorphism. Its geometric compatibility with suspension is essential here. Embed \(\mathbb R\) in an open interval of \(S^1\), extend compactly supported diffeomorphisms by the identity, and form the foliated circle bundle. Tsuboi's displayed commutative diagram on p. 3 says that this construction gives that same map to \(H_3(B\overline{\Gamma}_1^{\infty};\mathbb Z)\).
3. An integral group-homology 2-class is represented by a homomorphism from the fundamental group of a closed oriented surface [T81, p. 6]. We use this representability together with the preceding compact-support diagram. We do not need the stronger genus-reduction assertion later on p. 3, or a uniform surface genus across all real values.

The general Mather–Thurston theorem is also stated in [T13, Theorem 2.1, p. 196], including the compactly supported real-line case. Its subsequent discussion of the Godbillon–Vey map on \(H_2(G;\mathbb Z)\) is on p. 197. We need only the explicit 1981 consequence, and do not need a uniform genus for every possible real value.

Choose one positive value \(a\) of the composite Godbillon–Vey map. The preceding facts give one closed connected oriented surface \(\Sigma=\Sigma_g\), \(g\geq2\), and one representation
\[
 \rho:\pi_1(\Sigma)\longrightarrow G
\]
whose compactified suspension has Godbillon–Vey number \(a\). If a surface representative is initially disconnected, select a component with positive value, or join the components by connected sums with trivial connecting holonomy. Extra trivial handles do not change its group-homology class. Hence the connected genus-at-least-two requirement presents no obstruction.

This input is an existence theorem from classical foliation theory. No finite calculation in this package purports to construct its diffeomorphisms or prove the Mather–Thurston theorem.

## 3. A compact suspension block with product collars

Choose finitely many generators of \(\pi_1(\Sigma)\). All their images under \(\rho\), and their inverses, are the identity outside one compact interval. Every word in these generators is also the identity there. After identifying \(\mathbb R\) with \((0,1)\), all these diffeomorphisms extend smoothly to \(I=[0,1]\) and are the identity on two common endpoint collars.

Form the suspension
\[
 E_\rho=(\widetilde\Sigma\times I)/\pi_1(\Sigma),
\]
with the diagonal action given by deck transformations and \(\rho\). The images of the horizontal slices define a smooth cooriented foliation \(\mathcal H\), transverse to every interval fiber. On the endpoint collars it is the product foliation by copies of \(\Sigma\).

The interval bundle is smoothly trivial **relative to these collars**. Here is an elementary way to see the relative assertion, rather than assuming a flat trivialization. Take finitely many bundle charts and a smooth partition of unity on the base. Average their increasing fiber-coordinate functions with those partition weights. The derivative in the oriented fiber direction is positive, so the average is a coordinate on each fiber. It is the common endpoint coordinate on the collars, where every transition function is the identity. The resulting map gives a smooth fiber-preserving trivialization
\[
 E_\rho\cong\Sigma\times I.
\]
The horizontal foliation usually does not become a product foliation in the interior; no such claim is needed.

Choose a defining 1-form \(\alpha\) positive on the vertical vector field \(V=\partial_s\), normalized by \(\alpha(V)=1\). Thus \(\alpha=ds\) on the collars. Put
\[
 \eta=\iota_Vd\alpha.
\]
Frobenius and contraction give
\[
 0=\iota_V(\alpha\wedge d\alpha)
   =d\alpha-\alpha\wedge\iota_Vd\alpha,
\]
so \(d\alpha=\alpha\wedge\eta\). In particular, \(\eta=0\) on both collars.

Extend this foliated interval bundle across the complementary interval of a circle by the product foliation. Since the holonomy is compactly supported, the resulting foliated circle bundle is exactly the compactification in §2, with its natural orientation. Extend \(\alpha\) by the standard circle-coordinate form and \(\eta\) by zero. It follows that
\[
 \int_{\Sigma\times I}\eta\wedge d\eta=a. \tag{1}
\]
Thus (1) is a relative integral with fixed product collars, justified by an actual closed suspension and not by an arbitrary choice of a primitive on a manifold with boundary.

Every leaf of \(\mathcal H\) meets the fiber over any fixed point \(p\in\Sigma\). Indeed, lift a base path from the projection of any point of the leaf to \(p\) through the flat suspension. The lift exists for the entire path: the holonomy consists of diffeomorphisms of the full compact interval (and is fixed near its boundary). Its endpoint lies in the same leaf over \(p\).

## 4. A fixed hyperbolic ambient manifold

Choose an orientation-preserving smooth diffeomorphism \(\phi:\Sigma\to\Sigma\) whose mapping class is pseudo-Anosov and which fixes a small disk pointwise. Such a representative can be obtained from Penner's filling-multicurve construction [P, Theorem 3.1]: choose the twist annuli thin enough that a small disk in a complementary region is disjoint from them, and use a product containing all prescribed positive and negative twists. Alternatively, isotope a smooth representative of a pseudo-Anosov mapping class to fix a disk. The **mapping class** is pseudo-Anosov; the chosen smooth representative itself need not have the singular-foliation normal form of a pseudo-Anosov homeomorphism.

Fix \(p\) in this disk. Let
\[
 M=(\Sigma\times[0,1])/(x,1)\sim(\phi(x),0).
\]
This is closed, connected and oriented. Thurston's hyperbolization theorem for pseudo-Anosov mapping tori [H, Theorem 0.1, Proposition 2.6 and §5] equips it with a complete hyperbolic metric. Because the fiber is closed, \(M\) is compact, so the volume of that metric is finite and positive. Neither \(M\) nor its metric will depend on \(N\).

The fiber foliation away from any chosen product slab is smooth. The vertical vector field \(\partial_t\) descends through the mapping-torus identification. Since \(\phi(p)=p\), the curve
\[
 \gamma=\{p\}\times[0,1]/\sim
\]
is a smooth embedded circle.

## 5. Stacking, tautness and the exact integral

For a given \(N\), select \(N\) disjoint closed subintervals inside \((0,1)\), separated by nonempty gaps. On the corresponding product slabs \(\Sigma\times[a_j,b_j]\), insert positively rescaled copies of the block of §3. On the remaining slabs, use the ordinary fiber foliation. The product collars make the gluings smooth, including all derivatives. Around the mapping-torus seam the foliation remains the fiber foliation. Denote the resulting smooth cooriented foliation by \(\mathcal F_N\).

**Tautness in the source's single-circle sense.** The circle \(\gamma\) is everywhere transverse: its tangent is vertical, and each suspension block is transverse to the interval fibers. A leaf in a suspension block meets the vertical interval over \(p\) by the path-lifting argument of §3. A leaf in a product region is an entire fiber surface and also meets \(\gamma\). The interface leaves are included in these product collars. Hence every leaf meets this one circle. No appeal to a weaker Reebless condition, to an unrelated closed 2-form criterion, or to a tautness-preservation assertion is required.

**Additivity with the defining forms fixed.** Write \(\ell_j=b_j-a_j>0\) and
\[
 h_j(x,t)=\bigl(x,(t-a_j)/\ell_j\bigr).
\]
On the \(j\)-th block set
\[
 \alpha_j=\ell_j h_j^*\alpha,\qquad \eta_j=h_j^*\eta.
\]
The constant factor gives \(\alpha_j=dt\) on its product collars, and
\[
 d\alpha_j=\alpha_j\wedge\eta_j.
\]
On the complement set \(\alpha_N=dt\) and \(\eta_N=0\). These forms glue globally; \(dt\) is also compatible with the mapping-torus seam. Thus
\[
 d\alpha_N=\alpha_N\wedge\eta_N,
 \qquad \ker\alpha_N=T\mathcal F_N.
\]
The form \(\eta_N\wedge d\eta_N\) is supported in the block interiors. Since every \(h_j\) preserves orientation,
\[
\begin{aligned}
 \operatorname{gv}(\mathcal F_N)
 &=\sum_{j=1}^{N}\int_{\Sigma\times[a_j,b_j]}
       h_j^*(\eta\wedge d\eta)\\
 &=\sum_{j=1}^{N} a=Na.
\end{aligned}
\]
This proves the theorem. Increasing derivatives under compression cause no difficulty: every individual \(N\) gives a smooth foliation, and the question imposes no uniform derivative bound.

## 6. Checks, exclusions and interpretation

- **Fixed ambient topology and volume:** stacking changes the foliation inside a product collar, not the gluing diffeomorphism or the manifold. This is not a covering-space argument in which both volume and Godbillon–Vey number scale.
- **The compact leaves are allowed:** they are genus-\(g\) incompressible fibers, not torus leaves or Reeb components. Question 10.6 does not require minimality; the same source explicitly adds minimality to its different Question 13.1.
- **The block is not a foliation of a ball:** its genus-\(g\) base and compactly supported real-line holonomy are essential. One cannot replace the classical suspension input merely by Thurston's non-taut examples on \(S^3\).
- **The statement after Question 10.6 is not used as a theorem:** the source suggests an estimate from a common normalizing triangulation. A normal form alone does not supply a bound on the transverse differential data appearing in the ordinary Godbillon–Vey form. The theorem above addresses the printed question and has to be judged against the explicit suspension construction, not that suggested expectation.
- **Imported lower-bound claim:** the dataset report also asserts a universal lower bound by hyperbolic volume. The ordinary fiber foliation of the same \(M\) has defining closed form \(dt\), hence Godbillon–Vey number zero, while \(\operatorname{Vol}(M)>0\). That imported lower bound is false. This diagnostic alone would not have answered the source's upper-bound question.
- **Current-literature limitation:** the classical inputs were checked in primary sources; no publication explicitly spelling out this identical fixed-hyperbolic-manifold assembly was established by this search. The argument is a consequence of credited classical results, not a claimed new foundational theorem or a certified historical first.

The accompanying exact checks verify exterior-form signs, collar rescaling, finite additive bookkeeping, and disjoint-interval stacking bookkeeping. They do not prove the classical realization, surface-group or hyperbolization inputs; those enter through the cited theorems and the geometric argument above.

## References

[C] Danny Calegari, *Problems in foliations and laminations of 3-manifolds*, arXiv:math/0209081v1 (2002), Definition 1.1, Question 10.6 p. 25, §13.1 p. 29. [Author preprint](https://arxiv.org/abs/math/0209081).

[T81] Takashi Tsuboi, *On 2-cycles of B Diff(S¹) which are represented by foliated S¹-bundles over T²*, Ann. Inst. Fourier **31**(2) (1981), 1–59, especially pp. 1–3 and 6. The surjectivity input, compact-support group and commutative suspension diagram are all explicit there. [Published paper](https://aif.centre-mersenne.org/articles/10.5802/aif.828/).

[T13] Takashi Tsuboi, *Several problems on groups of diffeomorphisms*, Geometry and Foliations 2013 conference text, pp. 195–200, especially Theorem 2.1 and the discussion on pp. 196–197. [Author-hosted full text](https://tsuboiweb.matrix.jp/faculty-html-gf2013/abstract_files/gf2013_195-200.pdf).

[P] Robert C. Penner, *A construction of pseudo-Anosov homeomorphisms*, Trans. Amer. Math. Soc. **310**(1) (1988), 179–197, Theorem 3.1. [DOI](https://doi.org/10.1090/S0002-9947-1988-0930079-9).

[H] William P. Thurston, *Hyperbolic structures on 3-manifolds, II: Surface groups and 3-manifolds which fiber over the circle*, 1986 preprint, 1998 eprint, Theorem 0.1, Proposition 2.6 and §5. [Full author preprint](https://arxiv.org/abs/math/9801045).
