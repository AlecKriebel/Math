# Punctured-disc consequence of classical kernel classification

Audit completed 2026-10-13 04:34 UTC. Completion estimate: 100% of the assigned punctured-disc mechanism and bounded priority comparison. This does not certify global historical priority or current worldwide openness.

For the literal Green-domain scope of Hayman–Lingham Problem 7.42, the negative equality-along-a-line answer has an elementary punctured-disc derivation from older primary facts. This is separate from the explicit smooth-annulus theorem in the submitted note.

Johannes Köhn explicitly classifies the minimal positive harmonic functions on D*={0<|z|<1}, up to positive factors, as

\[
 P_\zeta(z)=\frac{1-|z|^2}{|\zeta-z|^2}\quad(|\zeta|=1),
 \qquad P_0(z)=-\log|z|.
\]

The exact locator is §4, printed p.63, following Satz 4.3, in *Die Harnacksche Metrik in der Theorie der harmonischen Funktionen*, Math. Z. 91 (1966), 50–64. The original page was visually verified in the [archived original article](https://gdz.sub.uni-goettingen.de/download/pdf/PPN266833020_0091/LOG_0010.pdf) ([DOI](https://doi.org/10.1007/BF01113851)). Herron's Theorem 3 and §3.2, printed p.17, give the corresponding punctured-domain Harnack metric formula in the [1987 primary article](https://www.jstage.jst.go.jp/article/kodaimath1978/10/1/10_1_9/_pdf/-char/en). Bear–Smith's Proposition 2.6, p.4, uses the positive-harmonic decomposition v(z)+b log(1/|z|), b>=0, in the [author manuscript dated 23 May 2005](https://math.hawaii.edu/~wayne/mathpapers/harnack.pdf). The inspected manuscript is titled *A tale of two conformally invariant metrics*; its corresponding publication is [JMAA 318 (2006), 498–506](https://doi.org/10.1016/j.jmaa.2005.05.065). The exact proposition locator here is to the inspected manuscript.

The decomposition, or Köhn's classification together with normalized-cone extremality, gives the **one-sided** envelope

\[
 H^{D^*}_a(z)=\max\left\{H^{\mathbb D}_a(z),
 \frac{\log(1/|z|)}{\log(1/|a|)}\right\}.
\]

This uses the cone information in the primary proofs; a symmetric distance formula alone must not be silently substituted for the one-sided envelope.

Here is the explicit deduction recorded by this audit. Take a=1/2 and K=3P_{-1}. Take normalized competitors F_+=P_i/P_i(a), F_-=P_{-i}/P_{-i}(a), and L=log(1/|z|)/log 2. Their gradients at a are

\[
 \nabla K=(-8/3,0),\quad
 \nabla F_\pm=(-32/15,\pm8/5),\quad
 \nabla L=(-2/\log2,0).
\]

Since exp(3/4)>1+3/4+(3/4)^2/2>2, log2<3/4. Thus the gradient of K lies strictly inside the competitors' gradient triangle. More explicitly, with delta=2/log2−8/3>0 and d=(u,v), the largest first-order competitor difference is

\[
 \max\{-\delta u,(8/15)u+(8/5)|v|\}>0\quad(d\ne0).
\]

For u<0 the first term is positive; for u>=0 the second is positive. Its minimum on the unit circle is positive. A common quadratic Taylor remainder therefore yields K<H_a^{D*} throughout a punctured neighborhood of a. This excludes every nontrivial equality curve issuing from a, including every Green line with equality on an initial segment. The alternate poles −1/2±i√3/2 in the proposed package-review mechanism also work; their recorded gradients are correct.

The puncture is polar. Exhausting D* by epsilon<|z|<1 shows that its Green function equals the disc Green function: the inner-boundary correction is bounded by M log(1/|z|)/log(1/epsilon), which tends to zero on interior compact sets. Consequently the boundary Green quotient at −1 is K. Any nonnegative harmonic minorant of K is bounded near zero, extends across zero, and is proportional to the disc Poisson kernel. Hence K is an admissible **minimal Martin kernel** on the doubly connected Green domain D*. The puncture is a degenerate/irregular boundary component; the printed [Problem 7.42, pp.173–174](https://arxiv.org/pdf/1809.07200v2) imposes no exclusion of such components. The conclusion assumes the equality-along-the-line interpretation supplied by the disc example. It does not resolve a weaker interpretation that asks only for some isolated contact away from the base point.

The inspected complete older articles do not state the fixed-kernel local-isolation theorem or identify it as a resolution of Problem 7.42. The preceding implication is an elementary deduction from their pre-existing ingredients. Mathematical derivability establishes this implication; it does **not** establish who first recognized or published it, nor a recognized historical resolution. Neither the punctured-disc example nor the displayed symmetric metric equalities give the submitted theorem for the prescribed kernel on 1<|z|<e.

The smooth-annulus note remains suitable for publication as an explicit, directly proved result with two nondegenerate smooth boundary components, subject to its separate mathematical/package checks. The current absence of a first-resolution or current-worldwide-openness claim is appropriate. Its attribution should additionally credit this simpler classical punctured-disc consequence and describe its own result as a smooth-annulus realization. An assertion that it is a newly original resolution of a still-open problem is not supported by this audit. Historical recognition and priority of the exact annular theorem remain unverified.
