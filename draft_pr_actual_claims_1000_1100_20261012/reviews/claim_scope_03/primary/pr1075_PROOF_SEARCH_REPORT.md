# A canonical connected-sum reduction for the sharp κ estimate

Target: 30002633 / OWR-13106-006, priority rank 1243.

Date: 10 October 2026 UTC. First substantive attempt. Recommended disposition: **partial, 1/5**. The universal estimate is neither proved nor refuted here.

## 1. Exact question and result of this attempt

For a closed smooth oriented spin manifold $M^{4m}$, with $m\geq1$, let

\[
L_g=\Delta_g+\frac{4m-2}{4(4m-1)}\operatorname{Scal}_g,
\qquad \mu_0(g)\leq\mu_1(g)\leq\cdots
\]

be its conformal Laplacian and its spectrum, indexed from zero and counted with multiplicity. The invariant κ is the least nonnegative integer k such that, for every ε>0, some metric satisfies

\[
\mu_k(g)=1,\qquad |\mu_i(g)|<\varepsilon\quad(0\leq i<k).
\]

It is ∞ if no such integer exists. The question is

\[
|\widehat A(M)|\leq 2^m\kappa(M). \tag{Q_m}
\]

No assumption on π₁ is part of the question. The original location is Bär's contribution to Oberwolfach Report 36/2014, printed p.2006, Theorem 4 and the immediately following open question [OWR]. The existing Bär–Dahl bound is $2^{2m-1}\kappa(M)$, not the proposed $2^m\kappa(M)$ [BD, Theorem 2.4]. For m=1 they agree. The κ=∞ case is vacuous, and κ=0 implies A-hat=0 by positive scalar curvature and the Dirac index theorem.

The principal proved reduction here is the following. Write

\[
B_m=(K3)^m,\qquad X_{m,p}=\#^p B_m\quad(p\geq1).
\]

Choose the K3 orientation for which A-hat(K3)=2. For every fixed m≥2, the following statements are equivalent:

1. (Q_m) holds for every closed oriented spin 4m-manifold.
2. (Q_m) holds for every connected simply connected spin 4m-manifold.
3. $\kappa(X_{m,p})=p$ for every p≥1.
4. $\kappa(X_{m,p})=p$ for an unbounded set of positive integers p.
5. $\lim_{p\to\infty}\kappa(X_{m,p})/p=1$.

This is a consequence of the known surgery theorem and same-dimension α-invariance, with an explicit amplification argument. It is **a reduction, not a proof of any of statements 1–5**. In particular, statement 3 is not known here beyond p=1 (and the already known m=1 case). No novelty claim is made for the component ingredients or for this elementary consequence without a broader literature search.

The argument does not use Bott stabilization. It compares manifolds in exactly the same dimension throughout.

## 2. Precise imported facts

The following facts are used with their original scope.

1. **Spectral surgery.** If a closed Riemannian n-manifold $(M,g)$ is changed by surgery on an embedded $S^j$ with trivial normal bundle and codimension n−j≥3, then, for every fixed k and every δ>0, the resulting smooth manifold admits a metric g′ for which
   \[
   |\mu_i(g')-\mu_i(g)|<\delta\quad(0\leq i\leq k).
   \]
   This is [BD, Theorem 3.1], for the conformal coefficient, a special case of the theorem for $\Delta+c\operatorname{Scal}$, c>0. It compares the **entire ordered initial block**, not only the first eigenvalue or the number of nonpositive eigenvalues.
2. **Consequent monotonicity.** The resulting manifold has κ no larger than the starting manifold [BD, Corollary 3.2]. A detailed normalization check is given below.
3. **Disjoint unions and orientation.** κ is additive under finite disjoint union and unchanged by reversing orientation [BD, equation (3) and adjoining text, p.2].
4. **Positive and zero scalar curvature.** κ=0 exactly when a positive-scalar-curvature metric exists. A connected scalar-flat manifold has κ≤1 [BD, Proposition 1.2]. Nonzero A-hat excludes κ=0.
5. **Same-dimensional simply connected invariance.** If M and N are closed simply connected spin manifolds of the same dimension n≥5 with α(M)=α(N), then κ(M)=κ(N) [BD, Remark 4.3, p.18]. This follows from the preceding bordism/surgery argument and Stolz's theorem; it is not a stabilization assertion. In n=8ℓ, α=A-hat; in n=8ℓ+4, α=A-hat/2 [BD, p.4]. Therefore equal A-hat in a fixed dimension divisible by four implies equal α.
6. **Index facts.** A-hat is integral on closed spin manifolds, is additive under disjoint union and connected sum, multiplicative under Cartesian product, and invariant under oriented spin bordism. For our surgery argument, bordism invariance also follows directly from its expression as a rational Pontryagin characteristic number.
7. **K3.** A K3 surface is connected and simply connected, is spin, has a Ricci-flat metric, and has A-hat=2 in its complex orientation. Consequently $B_m$ is simply connected and scalar-flat, A-hat(B_m)=2^m, and κ(B_m)=1. These are the same building blocks used in [BD, Remark 3.3 and §4].

For transparency, statement 5 is cited as the established published result it is. This attempt does not reprove Stolz's theorem. The spin framing and fundamental-group part of the reduction is independently spelled out below.

## 3. Spectral normalization, including signs and multiplicities

Suppose κ(M)=k<∞ and $\widetilde M$ is obtained from M by a finite sequence of the surgeries in fact 1. Fix a requested tolerance ε>0 and set

\[
\eta=\min\{1/4,\varepsilon/4\}.
\]

Choose a starting metric with μ_k=1 and |μ_i|<η for i<k. At each of the finitely many surgeries apply Theorem 3.1 with an error small enough that the sum of all errors is less than η. The triangle inequality for the ordered eigenvalue lists gives a final metric h on $\widetilde M$ such that

\[
|\mu_i(h)|<2\eta\ (i<k),\qquad
1-\eta<\mu_k(h)<1+\eta.
\]

In particular λ:=μ_k(h)>0. Multiplying the metric by λ multiplies the conformal Laplacian's eigenvalues by λ⁻¹, since both the ordinary Laplacian and scalar curvature have that scaling. For $\widetilde h=\lambda h$,

\[
\mu_k(\widetilde h)=1,\qquad
|\mu_i(\widetilde h)|<\frac{2\eta}{1-\eta}
\leq \frac{8\eta}{3}<\varepsilon.
\]

For ε≤1 the last bound is at most 2ε/3; for ε≥1 it is at most 2/3<ε. This proves $\kappa(\widetilde M)\leq k$. The same normalization applies to k=0, with an empty earlier block. No assertion is made that negative eigenvalues become positive. Their absolute values remain small, which is precisely the definition. Repeated eigenvalues and all multiplicities are preserved in the ordered comparison; no eigenspace labels or simplicity assumptions enter this step.

For one surgery this proves Corollary 3.2 directly. For infinitely many surgeries this argument would not apply, but only a finite number is used below.

## 4. Killing π₁ by spin surgeries in the correct direction

**Lemma 4.1.** Let M be a connected closed smooth spin n-manifold with n≥5. There is a connected closed simply connected spin n-manifold N, obtained from M by finitely many spin surgeries on circles, for which

\[
\kappa(N)\leq\kappa(M),\qquad
\alpha(N)=\alpha(M),
\]

and, if n is divisible by four, A-hat(N)=A-hat(M).

**Proof.** A closed smooth manifold has a finite CW model, so π₁(M) is finitely generated. Represent a finite generating family by embedded circles. In dimension at least five, general position permits the chosen circles to be made pairwise disjoint.

The oriented normal bundle to each oriented embedded circle has rank n−1≥4. Every oriented real vector bundle over S¹ is trivial. The homotopy classes of its oriented framings form a torsor over π₁(SO(n−1))=Z/2. Fixing a normal framing restricts the ambient spin structure to a spin structure on the tangent bundle of the circle. Twisting the normal framing by the nontrivial loop in SO(n−1) toggles this induced spin structure: the map π₁(SO(n−1))→π₁(SO(n)) is an isomorphism in these ranks, and its nontrivial loop lifts to a path in Spin(n) with opposite endpoints. Of the two induced spin structures on S¹ exactly one bounds D². Choose the corresponding framing. The spin structure then extends over the index-two handle $D^2\times D^{n-1}$ in the surgery trace. This is an actual spin bordism, not merely an oriented surgery on a spin manifold with an unspecified framing.

The surgery replaces $S^1\times\operatorname{int}D^{n-1}$ by $D^2\times S^{n-2}$. The complement has the same fundamental group as M: loops and their homotopies can be put in general position disjoint from the embedded circle because its codimension is at least three. Van Kampen then identifies the new fundamental group with π₁(M) modulo the normal closure of the chosen loop. Here $S^{n-2}$ is simply connected, as n≥5. Performing this for the selected generators gives π₁(N)=1. The complement stays connected, and the replacement does not disconnect it, so N is connected.

Each surgery has codimension n−1≥4, within the n−j≥3 hypothesis of [BD, Theorem 3.1]. Section 3 gives κ(N)≤κ(M). The finite sequence of spin handle traces supplies a spin bordism from M to N. Thus α is preserved. In dimensions 4m, the A-hat Pontryagin polynomial extends stably over that bordism; its characteristic number on the oriented boundary N−M is zero, proving A-hat(N)=A-hat(M). ∎

Only this direction of the κ inequality is used. Surgery need not preserve κ in general. The inverse of a circle surgery is a surgery on S^(n−2), of codimension two, outside the theorem's scope.

**Corollary 4.2.** In dimension 4m≥8, a counterexample to (Q_m) with finite κ would produce a simply connected counterexample in the same dimension. Indeed, with A=|A-hat(M)|,

\[
A>2^m\kappa(M)\geq2^m\kappa(N).
\]

For a disconnected M, it suffices to handle its finitely many connected components: use additivity of κ and the triangle inequality for A-hat. Thus no hidden connectedness or fundamental-group restriction remains in the reduction.

## 5. Connected sums and the canonical-family equivalence

**Lemma 5.1.** For connected closed spin n-manifolds M₁,M₂ with n≥3,

\[
\kappa(M_1\# M_2)\leq\kappa(M_1)+\kappa(M_2).
\]

**Proof.** The oriented connected sum is obtained from the disjoint union by an S⁰ surgery of codimension n≥3. Take a compatible spin one-handle. Apply spectral surgery monotonicity and disjoint-union additivity. ∎

In particular,

\[
1\leq \kappa(X_{m,p})\leq p,\qquad
\widehat A(X_{m,p})=2^m p. \tag{5.1}
\]

The lower inequality follows because the index is nonzero. The existing lower bound is more precisely

\[
\left\lceil\frac{p}{2^{m-1}}\right\rceil
\leq \kappa(X_{m,p})\leq p. \tag{5.2}
\]

The left side of (5.2) is merely [BD, Theorem 2.4] after substitution, not a new estimate.

**Theorem 5.2.** For fixed m≥2, (Q_m) is equivalent to κ(X_{m,p})=p for every p≥1.

**Proof.** If (Q_m) holds, (5.1) and A-hat(X_{m,p})=2^m p give p≤κ(X_{m,p})≤p.

Conversely, assume the equalities for all p. It suffices to consider a connected M with finite κ(M)=k and A=|A-hat(M)|>0. Reverse orientation if necessary to make A-hat(M)=A. The integer A is positive. Set d=2^m and form

\[
Y=\#^d M.
\]

By Lemma 5.1, κ(Y)≤dk, while A-hat(Y)=dA. Apply Lemma 4.1 to Y, producing a simply connected spin N with

\[
\kappa(N)\leq dk,\qquad \widehat A(N)=dA.
\]

Both N and X_{m,A} are simply connected spin manifolds of dimension 4m≥8. Their A-hat genera agree, hence their α-genera agree in this fixed dimension. [BD, Remark 4.3] therefore gives

\[
A=\kappa(X_{m,A})=\kappa(N)\leq dk=2^m\kappa(M).
\]

This proves (Q_m). The A=0 and κ=∞ cases are immediate; disconnected manifolds were handled above. ∎

The proof also gives a quantified transfer of a hypothetical violation: if A>dk, then

\[
\kappa(X_{m,A})\leq dk\leq A-1.
\]

There is no passage between different dimensions and no use of a Bott factor. The factor d appears as a **number of connected-sum copies**, not as the dimension of a product.

## 6. Stable slope and amplification of a single defect

Put $a_m(p)=\kappa(X_{m,p})$, and $a_m(0)=0$. Associativity of oriented connected sum and Lemma 5.1 imply

\[
a_m(p+q)\leq a_m(p)+a_m(q). \tag{6.1}
\]

Suppose a_m(p₀)=p₀−δ for p₀≥1 and an integer δ≥1. Write p=qp₀+r, with q≥0 and 0≤r<p₀. Then

\[
a_m(p)\leq q a_m(p_0)+a_m(r)
\leq p-q\delta. \tag{6.2}
\]

For every p≥p₀ this is strictly less than p. Thus **one defect rules out equality at every larger p**, and gives a linear asymptotic saving.

For completeness, subadditivity proves existence of the slope without any geometric compactness argument. Let s=inf_{j≥1} a_m(j)/j. Obviously a_m(p)/p≥s. For a fixed j write p=qj+r. Equation (6.1) and a_m(r)≤r≤j−1 give

\[
\limsup_{p\to\infty}\frac{a_m(p)}p\leq\frac{a_m(j)}j.
\]

Taking the infimum over j proves

\[
\lim_{p\to\infty}\frac{a_m(p)}p
=\inf_{p\geq1}\frac{a_m(p)}p
\in[2^{1-m},1]. \tag{6.3}
\]

If the slope equals one, then a_m(p)/p≥1 for every p, and (5.1) gives equality everywhere. Conversely, equality everywhere gives slope one. Equation (6.2) proves the equivalence with equality along any unbounded sequence. Together with Theorem 5.2 and Corollary 4.2, this proves all five equivalences stated in §1.

This does not calculate the slope. It isolates an exact remaining target.

## 7. Why the attempted analytic shortcuts stop

### 7.1 A metric-uniform one-chirality shortcut fails

In the proof of [BD, Theorem 2.4], one first chooses a metric satisfying the required spectral-gap condition. For that chosen metric, a Hilbert-space comparison applied to sufficiently many copies of the positive spinor bundle bounds its positive harmonic-spinor dimension h⁺ by $R\kappa(M)$, where $R=2^{2m-1}$ is the complex half-spinor rank. The index identity A-hat=h⁺−h⁻≤h⁺ then gives the printed coefficient R. This does not assert that $h^+(g)\leq R\kappa(M)$ for every metric g on M.

The blanket sharper replacement $h^+(g)\leq2^m\kappa(M)$ is false, even for an exact scalar-flat metric. Take the flat torus $T^{4m}$ with its trivial spin structure. All constant spinors are parallel, and the Lichnerowicz identity shows every harmonic spinor is parallel. Hence

\[
h^+=h^-=2^{2m-1}.
\]

The conformal Laplacian is the ordinary Laplacian, with a one-dimensional kernel and positive next eigenvalue, so κ≤1. The classical torus obstruction to positive scalar curvature, cited in [BD, p.3], gives κ=1. The ordinary A-hat index alone would not prove this, since it is zero. Scaling the flat metric normalizes its next scalar eigenvalue to one without changing these harmonic-spinor dimensions. It therefore also supplies an exact normalized κ-witness for which the sharper one-chirality estimate fails when m≥2. Meanwhile A-hat=0, so the torus does not violate the conjectured index inequality.

In fact κ≤1 is already enough to contradict the blanket shortcut; the stronger equality κ=1 is not needed for that contradiction. No higher-index theorem is needed for this limited conclusion.

This example prevents a metric-uniform replacement of the bundle-rank coefficient in the existing argument. It does not rule out every proof based on a different, specially selected family of metrics. Such an argument would have to justify its metric selection and the sharper estimate on that family, or obtain additional control of the chiral difference h⁺−h⁻. No such justification or control is established here.

### 7.2 Holonomy bounds apply to exact limits, and the required limit is absent

For a connected simply connected scalar-flat spin 4m-manifold with nonzero A-hat, a nonzero harmonic spinor is parallel. The known holonomy classification gives irreducible factors with absolute genera 2 for SU(2r), r+1 for Sp(r), and 1 for Spin(7) in dimension eight. The inequalities $2\leq2^r$, $r+1\leq2^r$, and $1\leq2^2$, together with multiplicativity, give $|\widehat A|\leq2^m$. This is the established Futaki bound [F, Corollary 2 and its proof], not a new κ theorem.

Here is a useful precise compactness consequence.

**Proposition 7.1.** Let M be connected and simply connected, closed and spin of dimension 4m≥8, with nonzero A-hat. Suppose metrics g_j witness κ(M)=k≥1 with μ_k(g_j)=1 and all earlier eigenvalues tending to zero. If, after pullback by diffeomorphisms, a subsequence converges in C¹ to a **smooth positive-definite** Riemannian metric g∞ on M, then k=1 and $|\widehat A(M)|\leq2^m$.

**Proof.** The C¹ continuity of the conformal-Laplacian eigenvalues is [BD, Lemma 3.4]. Consequently μ_0(g∞)=…=μ_{k−1}(g∞)=0 and μ_k(g∞)=1. For a real scalar Schrödinger operator on a connected closed manifold, the lowest eigenvalue is simple and admits a strictly positive eigenfunction. Thus the multiplicity of zero here is one, forcing k=1. If f>0 is its zero eigenfunction, the conformally changed metric $f^{4/(4m-2)}g_\infty$ has scalar curvature zero by conformal covariance. Futaki's simply connected scalar-flat bound gives the conclusion. ∎

The hypothesis is deliberately explicit: a smooth positive-definite limit on the fixed manifold. The κ definition supplies no curvature, injectivity-radius, volume, diameter, or C¹ compactness bound. It does not provide this limit or an index-conserving decomposition into k scalar-flat pieces. When k>1, the proposition actually proves that every normalized witnessing sequence must fail this particular compactness property, whether or not M is a counterexample.

For a hypothetical counterexample the simply connected reduction is still a counterexample, so its witnesses necessarily have this degeneration. The proposition does not rule degeneration out.

### 7.3 Connected sums cannot be split by reversing the allowed surgery

The upper bound κ(X_{m,p})≤p comes from merging p scalar-flat components by S⁰ surgeries. The inverse neck-cutting surgery is on S^(4m−1), of codimension one. [BD, Theorem 3.1] requires codimension at least three. It supplies no reverse inequality. More generally, surgeries of codimension at least three cannot split a connected manifold into more connected components: removing their sphere and tube in that codimension leaves a connected complement, and attaching the replacement cannot disconnect it. Thus the desired lower bound cannot be obtained by simply reversing the known construction.

### 7.4 Cartesian-product amplification has a coefficient mismatch

Set $c_n=(n-2)/(4(n-1))$. On a product M^n×N^d,

\[
L_{M\times N}=\Delta_M+\Delta_N+c_{n+d}(\operatorname{Scal}_M+\operatorname{Scal}_N),
\]

whereas the separate conformal Laplacians use c_n and c_d. Even if N is Ricci-flat,

\[
L_{M\times N}=L_M+\Delta_N+
\frac{d}{4(n-1)(n+d-1)}\operatorname{Scal}_M.
\]

The extra term is not controlled by the definition of κ. No product inequality for κ was proved. In particular, multiplicativity of A-hat is not a license to treat the conformal-Laplacian small modes as a tensor-product spectrum. Nor does Bott stabilization prove a fixed-dimensional bound.

## 8. An exact barrier to numerical/subadditive inference

The fixed-dimensional constraints proved above for the canonical family are integer values, a_m(0)=0, a_m(1)=1, subadditivity, and the bounds (5.2). These alone cannot yield a_m(p)=p, even after any finite set of positive tests.

For an arbitrary integer N≥2 define

\[
b_N(0)=0,\qquad b_N(p)=p-\lfloor p/N\rfloor\quad(p\geq1).
\]

Then b_N(p)=p for p<N and b_N(N)=N−1. Also

\[
b_N(p+q)\leq b_N(p)+b_N(q)
\]

because the floor function is superadditive under addition. For N≥2,

\[
\left\lceil p/2\right\rceil\leq b_N(p)\leq p.
\]

Hence for every m≥2 it meets the weaker lower bound in (5.2). Its asymptotic slope is 1−1/N<1. For any finite tested range, choose N larger than that range.

This is an abstract numerical countermodel to the listed inference rules, **not a manifold and not a counterexample to (Q_m)**. It demonstrates why a finite search or manipulation of the existing subadditive bounds cannot settle the universal quantifier. A new geometric/analytic lower-bound mechanism is necessary.

## 9. Status, attribution, and exact remaining gap

Proved in this packet, as consequences of explicitly cited existing theorems:

- spin surgery reduction to simply connected manifolds in the same dimension;
- exact equivalence with the connected sums $\#^p((K3)^m)$;
- equivalent stable-slope/unbounded-equality criteria;
- quantitative propagation of any hypothetical connected-sum defect;
- the normalized-witness compactness obstruction;
- explicit failure of the one-chirality, reverse-surgery, coefficient-blind product, and finite-subadditivity shortcuts.

The central unproved statement is

\[
\kappa\bigl(\#^p((K3)^m)\bigr)\geq p
\quad\text{for every }m\geq2,\ p\geq2.
\]

Equivalently one must prove slope one in (6.3), or construct a single actual pair (m,p) with a smaller κ and verify its full small-eigenvalue block. No such lower bound or counterexample is established. The unrestricted question remains unresolved by this first attempt. The appropriate turn outcome is partial, not candidate or solved.

The bounded literature search revisited the original article, original OWR question, Futaki's author preprint, and Gromov–Lawson's original article. No later full resolution was verified. That is a search limit, not a certification that the question remains open in all literature.

## References

[BD] Christian Bär and Mattias Dahl, *Small eigenvalues of the conformal Laplacian*, Geometric and Functional Analysis 13 (2003), 483–508. Author manuscript arXiv:math/0204200v3 (3 December 2002), 23 PDF pages. https://arxiv.org/abs/math/0204200 ; https://doi.org/10.1007/s00039-003-0419-6 . Relevant locations: Definition 1.1; equation (3); Proposition 1.2; Theorems 2.3–2.4 and 3.1; Corollary 3.2; Lemma 3.4; Proposition 4.2; Remark 4.3; Theorem 4.4; §5.1.

[OWR] Christian Bär, joint work with Mattias Dahl, *Small Eigenvalues of the Conformal Laplacian*, in *Analysis, Geometry and Topology of Positive Scalar Curvature Metrics*, Oberwolfach Report 36/2014, printed pp.2004–2007, especially p.2006. https://doi.org/10.4171/owr/2014/36 . Public report PDF: https://ems.press/content/serial-article-files/46526?nt=1 .

[F] Akito Futaki, *Scalar-flat closed manifolds not admitting positive scalar curvature metrics*, Inventiones Mathematicae 112 (1993), 23–29. Author preprint MPI 92-57, Corollary 2 (printed p.2/PDF p.4), proof (printed p.7/PDF p.9). https://archive.mpim-bonn.mpg.de/1159/1/preprint_1992_57.pdf ; https://doi.org/10.1007/BF01232424 . The 1992 preprint contains historical comments about then-unknown Spin(7) examples; those comments are not treated as current facts.

[GL] Mikhael Gromov and H. Blaine Lawson, Jr., *The classification of simply connected manifolds of positive scalar curvature*, Annals of Mathematics 111 (1980), 423–434, especially the proof of Theorem B, pp.431–432. https://annals.math.princeton.edu/1980/111-3/p02 ; author-hosted PDF https://www.ihes.fr/~gromov/wp-content/uploads/2018/08/827.pdf .
