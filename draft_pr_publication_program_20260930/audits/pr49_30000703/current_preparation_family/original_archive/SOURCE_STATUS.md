# The unrestricted Schwarz Pick boundary limit is a known reflection criterion

**Status recommendation: already solved for the exact unrestricted limit printed in the source. No new discovery is claimed.** The function extends holomorphically across an open unit-circle arc containing 1 and maps that arc into the unit circle. This follows from the Kraus–Roth–Ruscheweyh reflection theorem already stated immediately before the question, and the exact single-point equivalence is explicitly recorded in later primary literature.

Problem 30000703 / OWR-1460-009. Checked 30 September 2026. Model: gpt-6-astra, xhigh. Separate adversarial review is required before publication of this source correction.

## Exact source and the relevant known theorem

The original is Oliver Roth, *Local boundary behaviour of analytic maps and the hyperbolic metric*, in [Oberwolfach Report 9/2007](https://ems.press/content/serial-article-files/46093), printed pp. 528–530. Problem 1 on p. 529 asks about the boundary behavior at 1 of a holomorphic disk self-map satisfying

\[
 \lim_{\substack{z\to1\\z\in\mathbb D}}
 \Phi_f(z)=1,\qquad
 \Phi_f(z):=\frac{(1-|z|^2)|f'(z)|}{1-|f(z)|^2}.
 \tag{1}
\]

There is no radial or non-tangential restriction in the printed limit. The pinned record agrees with this formulation. The subsequent Problem 2 asks a different question about regularity of boundary sets for conformal metrics; it is not part of this target.

Theorem 1 on pp. 528–529 of the same contribution gives the following equivalence for an open arc \(\Gamma\subset\partial\mathbb D\) and a holomorphic map \(f:\mathbb D\to\mathbb D\):

- for every \(\xi\in\Gamma\), \(\liminf_{z\to\xi}\Phi_f(z)>0\);
- \(f\) has a holomorphic extension across \(\Gamma\) with \(f(\Gamma)\subset\partial\mathbb D\).

The theorem also states that either condition is equivalent to \(\Phi_f(z)\to1\) at every point of the arc. It is credited there to Daniela Kraus, Oliver Roth and Stephan Ruscheweyh, *A boundary version of Ahlfors' lemma, locally complete conformal metrics and conformally invariant reflection principles for analytic maps*, [Journal d'Analyse Mathématique 101 (2007), 219–256](https://doi.org/10.1007/s11854-007-0009-x).

The later paper by Gumenyuk, Kourou, Moucha and Roth, [*Hyperbolic distortion and conformality at the boundary*, arXiv:2410.13965v1](https://arxiv.org/abs/2410.13965v1), explicitly records the single-point equivalence in Section 8.2, p. 31, equation (8.3): the unrestricted limit in (1) is equivalent to analytic continuation by Schwarz reflection across an open arc containing the boundary point. It credits the same 2007 paper. Thus this conclusion is not a conjectural inference based only on the abstract of a recent preprint.

The full OWR contribution and the relevant 2024 definitions, theorem statements and Section 8.2 were read; the key source pages were rendered. The 2007 journal publication and authorship were verified from the publisher and author pages. Its full 38-page journal PDF was not available through the checked open sources, so no claim is made to have independently audited that entire paper. The precise imported theorem is available in the original OWR source itself.

## Why a single unrestricted limit supplies an arc

Here is the short quantifier argument, included to make the application checkable.

By (1), choose \(\delta>0\) so that

\[
 \Phi_f(z)>\frac12
 \quad\text{whenever }z\in\mathbb D,\ |z-1|<\delta.
 \tag{2}
\]

Shrink \(\delta\), if necessary, and take the open arc
\(\Gamma=\{\xi\in\partial\mathbb D:|\xi-1|<\delta/2\}\).
For every fixed \(\xi\in\Gamma\), all points of \(\mathbb D\) sufficiently close to \(\xi\) lie in \(B(1,\delta)\). Consequently

\[
 \liminf_{\substack{z\to\xi\\z\in\mathbb D}}\Phi_f(z)\ge\frac12>0.
\]

The cited arc theorem applies and gives the stated holomorphic continuation across \(\Gamma\). This argument actually needs only a positive unrestricted liminf at 1. Conversely, the extension and circle-mapping property imply (1) by the same arc theorem.

The observation uses the ordinary, unrestricted limit exactly as written. It cannot be repeated from a bound restricted to a Stolz angle or to a radius: such a bound does not control approach regions near the neighboring boundary points.

## Concrete boundary consequences and limitations

There is a point \(\eta=f(1)\in\partial\mathbb D\), and the unrestricted limit \(f(z)\to\eta\) exists. The extension is conformal at 1. In particular,

\[
 \overline\eta f'(1)=\alpha>0,\qquad
 f(z)=\eta+\alpha\eta(z-1)+O(|z-1|^2).
 \tag{3}
\]

To justify nonvanishing without assuming it, take a small neighborhood where the extension is nonzero. The function \(-\log|f|\) is harmonic, positive on the disk side, and zero on the boundary arc. The boundary point lemma gives a strictly positive inward normal derivative, or equivalently a strictly positive outward radial derivative of \(\log|f|\). Differentiating the identity \(|f(e^{it})|=1\) shows that \(\overline\eta f'(1)\) is real; the preceding normal derivative makes it positive. Thus the complex inverse function theorem applies locally. This is local conformality, not global injectivity.

After shrinking the neighborhood, the exterior part of the continuation is the usual reflection

\[
 f_{\rm ext}(z)=\frac{1}{\overline{f(1/\overline z)}}.
\]

Neither a disk automorphism nor a finite Blaschke product is forced. Two elementary controls show the limits of the conclusion.

1. \(f(z)=z^2\) satisfies
   \[
    \Phi_f(z)=\frac{2|z|}{1+|z|^2}\longrightarrow1
   \]
   as \(z\to1\), but it is not a disk automorphism.
2. The singular inner function
   \[
    f(z)=\exp\!\left(-\frac{1-z}{1+z}\right)
   \]
   maps the disk into itself and is holomorphic across the unit circle near 1. Put \(u=\operatorname{Re}((1-z)/(1+z))=(1-|z|^2)/|1+z|^2>0\). Direct differentiation gives
   \[
    \Phi_f(z)=\frac{u}{\sinh u}\longrightarrow1
   \]
   unrestrictedly at 1. It has an essential singularity at \(-1\), so it is not a finite Blaschke product and need not extend across the whole circle.

These controls are not counterexamples to the known local reflection conclusion.

## Why the imported assessment is too weak

The imported August 2026 assessment says that no complete unrestricted description is supplied and discusses angular conclusions. For the literal unrestricted condition, the cited 2024 paper itself states the stronger analytic-reflection equivalence.

The distinction is substantive. Theorem 1 of the 2024 preprint relates the radial or non-tangential hyperbolic-distortion limit to weak conformality, or angle preservation, together with an angular boundary value. Its Theorem 2 imposes an additional integral condition to obtain a finite angular derivative. Section 8.4 explains that the angular distortion limit alone need not give a finite angular derivative. These results address weaker hypotheses than (1). They must not replace the exact unrestricted target.

The mathematical content of (1) is therefore already characterized by a credited, published reflection theorem. This package does not infer a different intended quantifier for the historical question, does not solve the neighboring boundary-regularity question, and does not claim priority for the elementary point-to-arc application.

**Disposition:** recommend already_solved for the exact selected record after separate source/proof review. Zero fresh substantive proof-search attempts were used; this work is source verification and exposition of the existing theorem.
