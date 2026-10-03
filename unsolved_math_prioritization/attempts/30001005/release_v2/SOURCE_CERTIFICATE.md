# Classical obstruction to unrestricted short-time smoothing

Revised after independent audit, 3 October 2026 UTC. This certificate concerns unrestricted locally finite integral Brakke flows, with noncompact initial data allowed; the counterexample dimension is n = 7. Attribution: the classical Simons cone; its area-minimizing property is due to Bombieri, De Giorgi and Giusti. The argument below verifies the stationary-flow obstruction directly. It makes no novelty claim.

## 1. Exact target and source distinction

The pinned UnsolvedMath record 30001005 / OWR-2045-001 fixes a hypersurface \(M_0\subset\mathbb R^{n+1}\), with isolated singular points modeled on regular hypercones, and a given mean-curvature flow \((M_t)_{t\geq0}\) with initial data \(M_0\). It asks whether that flow has self-expanding asymptotics near each singular point and short-time positive-time smoothness when \(n\geq7\). Neither compactness nor a particular weak-flow selection appears in the catalogue statement.

The original source is Tom Ilmanen's contribution, *Relative Expander Monotonicity and MCF with Singular Initial Data*, in **Geometrie**, Oberwolfach Reports 5 (2008), report 34, printed p.1937; the report was published in June 2009. [Official report](https://ems.press/content/serial-article-files/46179), [publisher record](https://ems.press/journals/owr/articles/2045), DOI [10.4171/OWR/2008/34](https://doi.org/10.4171/OWR/2008/34).

The source asks two questions, about forward self-similarity and short-time regularity. It then announces: Theorem 1, self-expanding tangent flows for all dimensions; Theorem 2, construction with a compact-replacement minimizing expander for all dimensions; and Theorem 3, smoothness of the flows of Theorem 2 only for \(n\leq6\). Its low-dimensional statement should therefore not be recast as smoothness of every arbitrary weak flow. Nor does its dimension cutoff certify that the unrestricted high-dimensional smoothing assertion is open.

**Precise conclusion certified here:** the universal high-dimensional smoothing assertion, with integral Brakke mean-curvature flows allowed and with no compactness assumption, is false. Consequently the catalogue's conjunctive assertion in that unrestricted reading is false. We do not infer a universal self-similarity theorem from an announcement, and do not present this example as a counterexample to self-similarity.

## 2. The classical cone satisfies the geometric hypotheses

Write \(z=(x,y)\in\mathbb R^4\times\mathbb R^4\), set

\[
q(z)=|x|^2-|y|^2,\qquad C=q^{-1}(0),\qquad \rho=|z|.
\]

For \(z\ne0\), \(\nabla q=2(x,-y)\ne0\). Thus \(C\setminus\{0\}\) is an embedded smooth 7-dimensional hypersurface. Its link is

\[
C\cap\mathbb S^7=\mathbb S^3(1/\sqrt2)\times\mathbb S^3(1/\sqrt2),
\]

a smooth compact embedded hypersurface of \(\mathbb S^7\). The initial datum is itself its exact tangent cone: every positive dilation fixes \(C\).

The vertex is genuinely singular. If a dilation-invariant hypersurface were differentiable at its vertex, every ray in it would lie in its 7-dimensional tangent plane. But \(C\) spans \(\mathbb R^8\): for unit coordinate vectors \(e_i\in\mathbb R^4\) and \(f_j\in\mathbb R^4\), the vectors \((e_i,f_j)\) and \((e_i,-f_j)\) are in \(C\), and their sums and differences span both factors. It cannot lie in a 7-plane. Thus \(\operatorname{sing}C=\{0\}\).

These facts verify the regular-link and isolated-point hypotheses without taking a product with a Euclidean factor, which would introduce a nonisolated singular set.

## 3. Stationarity, including the vertex

Off the origin use the unit field

\[
\nu(z)=(x,-y)/\rho.
\]

On \(C\) it is a unit normal. Direct differentiation gives

\[
\operatorname{div}\nu
=\frac{4-4}{\rho}-\frac{|x|^2-|y|^2}{\rho^3}
=-q/\rho^3.
\]

Because \(\nu\) is unit, its ambient divergence equals its tangential divergence along \(C\). Hence \(H=0\) on its regular part.

There is no first-variation atom at the vertex. For a compactly supported smooth vector field \(X\), apply the first-variation/divergence identity to \(C\setminus B_\varepsilon\). Its inner-boundary term has absolute value at most

\[
\|X\|_\infty\,\mathcal H^6(C\cap\partial B_\varepsilon)
=\|X\|_\infty\,\mathcal H^6(C\cap\mathbb S^7)\varepsilon^6\longrightarrow0.
\]

The omitted integral over \(C\cap B_\varepsilon\) also tends to zero, because its mass is \(O(\varepsilon^7)\). Therefore \(\int_C\operatorname{div}_C X\,d\mathcal H^7=0\). The multiplicity-one integral varifold of \(C\) is stationary, with generalized mean-curvature vector zero.

## 4. Exact Brakke-flow verification

Let \(\mu_t=\mathcal H^7\llcorner C\) for every \(t\geq0\). These are locally finite Radon measures of integral varifolds. For every nonnegative compactly supported space-time test function \(\phi\), and \(t_1<t_2\),

\[
\mu_{t_2}(\phi(\cdot,t_2))-\mu_{t_1}(\phi(\cdot,t_1))
=\int_{t_1}^{t_2}\int_C\partial_t\phi\,d\mathcal H^7\,dt.
\]

Since \(\mathbf H=0\), this is exactly the right side of the integrated Brakke inequality

\[
\int_{t_1}^{t_2}\int(-|\mathbf H|^2\phi+\mathbf H\cdot\nabla\phi+\partial_t\phi)\,d\mu_t\,dt.
\]

Thus the inequality holds with equality. There is no artificial mass drop and no delayed change of initial data. Every time slice is \(C\), and every positive-time slice is singular at the origin. The desired positive interval of smoothness does not exist.

The example remains stationary after every parabolic rescaling. In particular,

\[
M_t=C=\sqrt t\,C,\qquad t^{-1/2}M_t=C.
\]

Its regular part satisfies the expander equation \(\mathbf H-z^\perp/2=0\), because both terms vanish. A singular stationary cone must not be confused with a smooth expander. This is precisely why self-similar scaling does not imply smoothing.

## 5. Literature attribution and limitations

1. The cone and its minimizing property are classical: Bombieri–De Giorgi–Giusti, *Minimal cones and the Bernstein problem*, Invent. Math. 7 (1969), 243–268, [publisher record](https://link.springer.com/article/10.1007/BF01404309). We inspected that record, not a complete copy of the 1969 paper.
2. De Philippis–Paolini give a primary, fully accessible short proof: *A Short Proof of the Minimality of Simons Cone*, Rend. Sem. Mat. Univ. Padova 121 (2009), 233–241, [publisher record](https://ems.press/journals/rsmup/articles/11697). The [author-deposited March 2008 version](https://cvgmt.sns.it/media/doc/paper/1185/dePPao.pdf), §2, Proposition 2.1 and Theorem 2.2, was read. It proves the relevant minimizing assertion in ambient dimension \(2m\geq8\). Area minimization is stronger than the stationarity needed in §§3–4.
3. Ilmanen's [1998 lecture notes](https://math.jhu.edu/~js/Math745/ilmanen.mcflow.pdf), printed pp.41–42 (PDF pp.43–44), describe the stationary cones and explicitly use the constant evolution \(M_t=C\). The stationary-flow principle used here is therefore not a new observation.
4. Ilmanen's [publication summary](https://people.math.ethz.ch/~ilmanen/papers/pub.pdf), item 23, additionally announces that regular area-minimizing cones have a unique evolution equal to the cone. Only the indexed primary-source excerpt was accessible. It lists *Dynamics of Stationary Cones* as “in preparation.” We do not substitute that announcement for a read published proof, and **do not rely on this stronger uniqueness assertion** for the certificate.
5. Chodosh–Daniels-Holgate–Schulze, *Mean curvature flow from conical singularities*, Invent. Math. 238 (2024), 1041–1066, [full publisher text](https://link.springer.com/article/10.1007/s00222-024-01296-8), Theorems 1.2–1.4, proves the regularity and expander-model results for the outermost flows in dimensions \(2\leq n\leq6\). The paragraph following Theorem 1.2 extends its results to higher dimensions when the outermost expanders are smooth. Section 1.2 explains why forward monotonicity is not simply an available proof of the unrestricted assertion. Section 2.5 defines smooth cones by their smooth links; the cone above fits that definition. These results are not contradicted by this example.

The certificate is deliberately limited to the exact unrestricted implication verified in §§2–4. It does not prove compact-data counterexamples, identify every construction intended in the short OWR announcement, classify all forward tangent flows in high dimension, or establish uniqueness of arbitrary Brakke flows. These are distinct claims. Any repaired problem imposing additional restrictions must state them and receive a new source review.


## 6. Revised source-gate disposition

The independent review passed the Brakke obstruction but held an unqualified original-problem resolution. Its quantifier correction is incorporated above. [SCOPE_DISPOSITION.md](SCOPE_DISPOSITION.md) distinguishes the original selected-flow announcement, the solved modern regimes, and nearby historical questions. The recommendation is a source-repair hold for the catalogue entry, not an unqualified already-solved label. The original selected-flow problem is not certified resolved by this packet.
