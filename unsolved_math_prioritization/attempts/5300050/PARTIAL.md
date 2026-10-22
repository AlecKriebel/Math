# Boundary entropy: an exact harmonic-measure diagnostic and the remaining gap

The general question remains unresolved in this package. The result below identifies a failed shortcut in the imported desk assessment and records a standard sufficient condition. It is not a counterexample to Przytycki’s boundary-entropy question. No novelty is claimed; separate adversarial review is pending.

## 1. Exact question and source correction

Przytycki’s contribution to *Problems in Holomorphic Dynamics*, IMS Preprint 1992/7, printed pp. 29–30, begins with a proper holomorphic self-map
\[
 f:U\longrightarrow U,\qquad d=\deg(f|_U)\ge2,
\]
where \(U\) is a simply connected domain in the Riemann sphere and the iterates converge to a constant point \(p\in U\). The discussion uses a Riemann map \(R:\mathbb D\to U\). Problem 1.1 additionally assumes a holomorphic extension to a neighborhood of \(\overline U\). In precisely that setting, Problem 1.3 asks whether
\[
 h_{\rm top}(f|_{\partial U})=\log d. \tag{1}
\]
All closures and boundaries here are spherical. Thus \(\partial U\) is compact; no Euclidean boundedness, Jordan boundary, local connectivity, or globally rational extension is assumed. The map in (1) is the given self-map, rather than a periodic component’s map before taking its return iterate. The relevant entropy is ordinary topological entropy of a continuous map of the compact boundary.

Properness and continuity imply \(f(\partial U)=\partial U\): a sequence approaching the boundary cannot have images in a compact subset of \(U\), and preimages of a sequence in \(U\) approaching a prescribed boundary point have a convergent subsequence in \(\overline U\), whose limit cannot be interior.

The original source explicitly states that the inequality \(h_{\rm top}(f|_{\partial U})\ge\log d\) is already known. The missing direction is the **upper** bound. The imported summary’s suggestion that the issue is whether the boundary carries full entropy is consequently misleading. Its unqualified assertion about topological entropy “on the basin” also suppresses the choice of entropy convention on a noncompact space; that assertion is not used here.

The current desk assessment proposes pushing harmonic measure through the circle model to obtain the lower bound. This particular mechanism does not work in general, as the following admissible example shows.

## 2. Exact diagnostic: harmonic measure need not have entropy \(\log d\)

**Proposition.** For
\[
 B(z)=z\frac{z-3/5}{1-(3/5)z},\qquad U=\mathbb D,
\]
all the hypotheses of (1) hold and
\[
 h_{\rm top}(B|_{\partial\mathbb D})=\log2,
 \qquad h_m(B|_{\partial\mathbb D})=\log(9/5)<\log2, \tag{2}
\]
where \(m\) is normalized arc length, equivalently harmonic measure of \(\mathbb D\) viewed from its attracting fixed point \(0\).

**Proof of admissibility.** More generally let \(0<a<1\) and put
\(B_a(z)=z(z-a)/(1-az)\). This is a finite Blaschke product of degree two. Its pole \(1/a\) lies outside \(\overline{\mathbb D}\), so it is holomorphic on a neighborhood of that closure. Each factor has modulus one on the circle, and the second factor has modulus less than one in the disk. Hence \(|B_a(z)|<|z|\) for \(0<|z|<1\). The iterates tend to zero: on each compact disk \(|z|\le r<1\), the second factor has modulus bounded by some \(c_r<1\), and all subsequent iterates stay in that disk. Also \(B_a'(0)=-a\), so zero is attracting.

The boundary modulus condition and the argument principle show that every point of \(\mathbb D\) has exactly two preimages there, counting multiplicity. The same condition gives properness. Reflection across the circle gives \(B_a(1/\bar z)=1/\overline{B_a(z)}\), so no point outside the closed disk enters the disk. The circle itself is invariant. Thus \(\mathbb D\) is exactly the immediate attracting basin of zero for this rational map.

**Circle entropy.** In angular coordinates the derivative of the circle map is
\[
 D_a(\theta)=1+\frac{1-a^2}{1-2a\cos\theta+a^2}
 =\frac{2-2a\cos\theta}{1-2a\cos\theta+a^2}.
 \tag{3}
\]
In particular
\[
 \frac{2}{1+a}\le D_a(\theta)\le\frac{2}{1-a}.
\]
It is an orientation-preserving, uniformly expanding circle covering of degree two, hence is topologically conjugate to doubling and has entropy \(\log2\).

For completeness, an increasing expanding lift \(F:\mathbb R\to\mathbb R\) satisfies \(F(x+1)=F(x)+2\). The uniform limit \(H(x)=\lim_n2^{-n}F^n(x)\) exists because \(F(x)-2x\) is bounded, and satisfies \(H\circ F=2H\), \(H(x+1)=H(x)+1\). It is nondecreasing. If \(H(x)=H(y)\) with \(x<y\), the uniform error estimate would bound \(F^n(y)-F^n(x)\) independently of \(n\), whereas uniform expansion forces it to grow at least as \(\lambda^n(y-x)\), with \(\lambda>1\). Therefore \(H\) is a homeomorphism. The degree-two linear covering has entropy \(\log2\), for example from its binary interval partitions.

**Invariant measure and its entropy.** Normalized arc length is invariant under \(B_a\). Indeed, if \(u\) is the harmonic extension of a continuous boundary function, \(u\circ B_a\) is harmonic, continuous on the closed disk, and has center value \(u(B_a(0))=u(0)\). The mean-value property proves \(\int\varphi\circ B_a\,dm=\int\varphi\,dm\).

The metric entropy of this smooth expanding circle map with respect to its invariant length measure is
\[
 h_m(B_a)=\frac1{2\pi}\int_0^{2\pi}\log D_a(\theta)\,d\theta. \tag{4}
\]
Here is a direct justification, so no identification of harmonic measure with a maximal-entropy measure is being assumed. Since \(B_a(1)=1\) and \(B_a^{-1}(1)=\{1,-1\}\), the two half-circle intervals form a full-branch partition. Its \(n\)-cylinders map one-to-one onto the circle cut at 1, and shrink uniformly by expansion. The partition is generating. Smoothness of \(\log D_a\) and inverse contraction give a distortion bound for \(\log D(B_a^n)\) on each cylinder independent of \(n\). Consequently
\[
 -\log m(I_n(x))=\log D(B_a^n)(x)+O(1)
\]
with a uniform constant, away from the countable set of partition endpoints. Integrating, using invariance, and dividing by \(n\) proves (4) by the entropy formula for a generating finite partition.

For \(a=3/5\), (3) has the exact factorization, on \(|z|=1\),
\[
 D_{3/5}(z)=\frac95\frac{|1-z/3|^2}{|1-3z/5|^2}. \tag{5}
\]
For \(|c|<1\), the harmonic function \(\log|1-cz|\) has boundary average zero. Taking the logarithm of (5), integrating and applying (4) gives \(h_m(B)=\log(9/5)\). This proves (2). \(\square\)

More generally the same computation gives
\[
 h_m(B_a)=\log\bigl(1+\sqrt{1-a^2}\bigr),\qquad0<a<1.
\]
To check it without integration formulas, put \(b=\sqrt{1-a^2}\) and \(c=a/(1+b)\). Then
\(2-2a\cos\theta=(1+b)|1-ce^{i\theta}|^2\), and both logarithmic boundary means vanish as before. As \(a\uparrow1\), the metric entropy tends to zero while the topological entropy stays \(\log2\) for every \(a<1\). No conclusion is asserted at the degenerate parameter \(a=1\).

This diagnostic only rejects the proposed **choice of measure** for proving the lower bound. It does not reject the circle model, the existence of other invariant measures, or the known lower bound itself. In this example the conjugacy transports the doubling map’s maximal-entropy measure to a measure of entropy \(\log2\).

## 3. Standard sufficient condition and the missing extension step

**Conditional proposition.** In the setting of (1), if the Riemann map extends continuously to \(\overline{\mathbb D}\), then (1) holds.

Normalize \(R(0)=p\) and let \(g=R^{-1}fR\). It is a finite degree-\(d\) Blaschke product fixing zero. On the circle its angular derivative is a sum of Poisson kernels, one of which is identically one because zero is a root. Since \(d\ge2\), its minimum is strictly greater than one. The lift argument in Section 2, with 2 replaced by \(d\), gives \(h_{\rm top}(g|_{S^1})=\log d\).

The continuous extension \(\bar R:S^1\to\partial U\) is onto by compactness and density of \(R(\mathbb D)\) in \(\overline U\). The interior conjugacy extends to
\(f\bar R=\bar Rg\) by continuity. Entropy does not increase under a continuous factor map, so
\(h_{\rm top}(f|_{\partial U})\le\log d\). Combining this with the lower bound explicitly credited in the original source proves the proposition. Local connectivity of the boundary is a familiar sufficient hypothesis for this continuous extension; a Jordan boundary gives a boundary conjugacy directly.

The continuous-factor upper bound can also be checked directly with separated sets. Uniform continuity gives \(\delta>0\) such that circle points within \(\delta\) have images within a prescribed \(\varepsilon>0\). Choosing one lift of each member of an \((n,\varepsilon)\)-separated boundary set produces an \((n,\delta)\)-separated circle set. Take exponential growth rates and then \(\varepsilon\downarrow0\).

The general source does **not** supply a continuous extension. Almost-everywhere radial limits with respect to harmonic measure are insufficient to turn this into a topological factor argument, and Section 2 explains why that single measure cannot replace the missing upper-bound argument either. A sufficient measurable replacement would be that every ergodic positive-entropy invariant probability on \(\partial U\) is a measurable factor of an invariant probability on the degree-\(d\) circle model. Entropy monotonicity and the variational principle would then give the desired upper bound. That replacement is not established here.

## 4. Literature boundaries and the precise unresolved target

Przytycki’s published 1994 accessibility theorem gives a genuine, but conditional, route. In addition to shrinking coding-tree edges, its Corollary 0.1 retains condition (0.3′). In the basin notation the displayed predecessor (0.3) is
\[
 f^{-n}(U)\cap B_{n,0}\subset U,
\]
for the relevant good inverse neighborhoods. It keeps the inverse pieces on the chosen basin side. Holomorphic extension across \(\partial U\) and properness of \(f:U\to U\) alone have not been shown here to imply this condition. Corollary 0.2 assumes a **completely invariant** rational basin; this is stronger than the original target. The published Corollary 0.1 explicitly qualifies the invariant-measure lifting conclusion by the almost-everywhere side condition. Reading only its abstract, or the subsequent shorthand “onto” sentence without its hypotheses, would lose this restriction.

Roesch–Yin’s polynomial theorem gives Jordan boundaries for bounded attracting Fatou components and therefore settles those particular boundaries through Section 3. This is credited prior mathematics, not a new theorem of this package. The scope audit checks their published statement and proof outline, without claiming a new independent audit of the entire long puzzle argument. It does not cover arbitrary rational or locally defined holomorphic maps in the original question.

Hawkins–Taylor (2018) studies the mass assigned to Fatou boundaries by the **global** rational-map maximal-entropy measure. Such mass statements do not determine the entropy of the restriction to a single basin boundary or replace \(\deg(f|_U)\) by the global rational degree. Levin’s July 2026 preprint, Appendix A, gives a lower bound for completely invariant compact sets under local holomorphic hypotheses. Both the direction of that inequality and its complete-invariance assumptions differ from the missing upper bound here. These sources were inspected for scope, not certified as new proofs in this package.

The remaining problem is exactly to prove the upper bound for every original admissible basin, including boundaries without an established continuous Riemann-map extension, or to construct an admissible holomorphic example with boundary entropy greater than \(\log d\). No such construction or general upper bound was obtained. No current universal-resolution claim was located in the primary sources checked; this is a bounded literature search, not proof of continued openness.

## 5. Verification and status

The accompanying standard-library checker verifies the rational identities behind (3)–(5), admissibility controls, critical points, and a rationally parametrized family of entropy-factor identities. It also checks exact binary-cylinder counts for the comparison doubling map. These finite controls do not establish entropy limits or the unresolved upper bound; those distinctions are explicit above.

This package uses one substantive circle-model diagnostic attempt. Recommended status: **unsolved, 1/5**. The complete problem remains unsolved here. The result is an exact obstruction to one proposed shortcut, together with credited sufficient cases and a precise missing hypothesis.

## References

1. B. Bielefeld and M. Lyubich, eds., *Problems in Holomorphic Dynamics*, IMS Preprint 1992/7, Przytycki contribution, printed pp. 29–30: https://www.math.stonybrook.edu/preprints/ims92-7.pdf
2. F. Przytycki, *Accessibility of typical points for invariant measures of positive Lyapunov exponents for iterations of holomorphic maps*, Fundamenta Mathematicae 144 (1994), 259–278, especially pp. 260, 263–266: https://www.impan.pl/~feliksp/access.pdf
3. P. Roesch and Y. Yin, *The boundary of bounded polynomial Fatou components*, C. R. Acad. Sci. Paris, Ser. I 346 (2008), 877–880, Theorem 1: https://doi.org/10.1016/j.crma.2008.06.004. Longer primary version: https://arxiv.org/abs/0909.4598
4. J. Hawkins and M. Taylor, *The maximal entropy measure of Fatou boundaries*, DCDS 38 (2018), 4421–4431: https://doi.org/10.3934/dcds.2018192; primary preprint https://arxiv.org/abs/1708.07141
5. G. Levin, *Polynomial-like dynamics of analytic maps*, arXiv:2508.17308v3 (July 2026), Definition 1.1 and Appendix A: https://arxiv.org/abs/2508.17308v3
