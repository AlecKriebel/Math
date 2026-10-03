# Credited source-resolution certificate: 30001957

**Result:** Published examples meet the original existential request through its negative-entropy-production alternative. This is a literature resolution, not a new theorem or a new construction by the present researcher. Credit belongs to Eugen Mihailescu and Mariusz Urbański. No author proof-attempt turn was used.

## 1. Exact target and scope

Record 30001957 / OWR-11570-002 is titled *Entropy Production on Folded Hyperbolic Fractals*. Its primary source is Eugen Mihailescu's Problem 1, Open Problems, printed p. 125 of Oberwolfach Report 03/2012 (PDF page index 48), DOI [10.4171/OWR/2012/03](https://doi.org/10.4171/OWR/2012/03).

Formal restatement: exhibit further examples of triples (f, Λ, μ), with Λ a folded fractal invariant under a noninvertible map f that is hyperbolic on Λ, and with invariant probability measures μ, organized in families, for which e_f(μ)<0 or e_f(μ)>0. The introductory toral perturbation is already known in the problem statement. “Negative (or positive)” permits the negative alternative. There is no specified cardinality, requirement of distinct measures for a fixed map, demand for both signs on every fractal, or classification requirement. This certificate supplies a parameterized family of triples and adds none of those stronger conditions.

## 2. An entirely published family

Use the family printed in Mihailescu, *Physical Measures for Multivalued Inverse Iterates Near Hyperbolic Repellors*, JSP 139 (2010), 800–819, [DOI 10.1007/s10955-010-9960-5](https://doi.org/10.1007/s10955-010-9960-5), Examples 3–4, pp. 817–818:

\[
A=\begin{pmatrix}2&1\\2&2\end{pmatrix},\qquad
 g_t(x,y)=\bigl(2x+y+t\sin(2\pi(x+y)),\;2x+2y+t\cos^2(4\pi x)\bigr)\pmod1,
\]
\[
f_t([z_0:z_1],(x,y))=
\left([z_0^2+t z_1^2e^{2\pi i(2x+y)}:z_1^2],\;g_t(x,y)\right)
\quad\text{on } M=\mathbb{CP}^1\times\mathbb T^2.
\]

Take sufficiently small positive t. Smallness means the C² perturbation regime of the cited results; no numerical threshold is claimed. Proposition 3, p. 805, preserves the connected hyperbolic repeller and preimage count. For an isolating neighborhood V of S¹×T², write Λ_t=⋂_{n≤0}f_t^n(V). The paper describes the perturbed set's self-intersecting structure on p. 818. It is a compact, connected, transitive basic repeller, disjoint from the critical set, with stable and unstable directions. Hyperbolicity is in the endomorphism/inverse-limit sense. The measure μ_t⁻ is the invariant equilibrium probability for Φ_t^s=log|det(Df_t|E^s)|; Theorems 2–3 and Corollary 1 establish its inverse-SRB interpretation and stable conditional absolute continuity. [Author-hosted primary PDF](https://imar.ro/~mihailes/Physical-JSP.pdf)

## 3. Published strict sign and hypothesis matching

Mihailescu–Urbański, *Entropy Production for a Class of Inverse SRB Measures*, JSP 150 (2013), 881–888, [DOI 10.1007/s10955-012-0672-x](https://doi.org/10.1007/s10955-012-0672-x), Example pp. 886–887, includes this family by setting k=2, ε=t, g=g_t. Its Corollary 3, p. 887, supplies the strict inequality:

\[
e_{f_t}(\mu_t^-)<0.
\]

Definition 1, p. 883, and Proposition 1(a), p. 884, give
\[
F_{f_t}(\mu_t^-)=H_{\mu_t^-}(\mathcal E\mid f_t^{-1}\mathcal E)=\log d,\qquad d=k|\det A|=4,
\]
\[
e_{f_t}(\mu_t^-)=\log4-\int_{\Lambda_t}\log|\det Df_t|\,d\mu_t^-<0.
\]
Here the derivative determinant is ambient; d counts preimages remaining in Λ_t. The cited family is non-Anosov, fractal, and saddle-type. Folding entropy is not entropy production. The measure is inverse SRB, not the forward-SRB measure from the separate toral example. [Author-hosted primary PDF](https://www.imar.ro/~purice/Inst/2013/EMihailescu/JSP-Entprod2013-final.pdf)

Thus the source supplies every requested object: noninvertible dynamics, a folded hyperbolic fractal, a parameterized invariant-measure family, and a strict allowed sign. This matching uses published results and direct parameter substitution, without new mathematical search.

## 4. Chronology and the meaning of “other”

The 2010 paper already printed the quadratic family and constructed its inverse SRB measures. That is prior credit, not a geometric construction discovered after the OWR question. Its text does not discuss entropy production. The 2011 preprint cited by OWR, [arXiv:1104.2342v1](https://arxiv.org/abs/1104.2342v1), proves the toral sign example in Corollary 4(b); the January 2012 OWR problem repeats that result on T² before asking for other folded fractals. General formulas for equilibrium measures in that preprint do not by themselves supply this family's strict sign.

The later 2013 paper (published online December 22, 2012) adds the needed strict-sign theorem for the non-Anosov fractal family. Thus “other” is met by a different domain and dynamics from the toral signed example, together with a subsequently published entropy-production conclusion. Merely repeating the 2010 family without this later sign theorem would not be the answer certified here.

## 5. Source caveats and attribution boundary

The 2013 printed homogeneous formula has numerator degree k but denominator z₁². Restricting to its included k=2 case avoids the mismatch. Its Corollary 2 proof omits “not” in one cohomology sentence and uses determinant where logarithmic determinant is expected. Those statements are not used here. The invoked strict sign is Corollary 3, independently rendered and read.

This certificate checks applicability of cited results; it does not reconstruct every foundational proof or claim new corrections. The whole-manifold toral example in the original problem and the 2011 general folding-entropy formulas alone would not constitute this certificate. No stronger residual problem is asserted.

