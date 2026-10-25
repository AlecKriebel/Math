# Intermediate-area cylinders in the principal quadratic stratum

At every intermediate shrinking area scale, cylinder counts have a geometric Poisson limit, including every fixed joint moment.

[Alec Kriebel](https://orcid.org/0009-0001-9320-500X) · Independent researcher · 15 October 2026 · Version 1.0 · Unrefereed preprint

[Read the paper](https://zenodo.org/api/records/23387774/files/cylinder_areas.pdf/content) · [Complete source and verification archive](https://zenodo.org/api/records/23387774/files/cylinder_areas_verification.zip/content) · [DOI](https://doi.org/10.5281/zenodo.23387774)

## Abstract

Delecroix asked for the area spectrum of cylinders on large-genus square-tiled surfaces, highlighting the normalized-area window $[g^{-1/2},2g^{-1/2}]$. For the principal holomorphic quadratic stratum, with the number of squares tending to infinity before the genus, we derive a Poisson limit at every intermediate scale $s_g\to0$, $gs_g\to\infty$. The rescaled cylinder areas converge to a Poisson point process of intensity $dx/(2x)$; compact-window counts converge with every fixed joint moment. The highlighted count tends to $\operatorname{Poisson}((\log2)/2)$, and its mean and variance have the same limit. The proof extracts a uniform Gamma/Dirichlet approximation from the published formulas of Delecroix–Liu and Delecroix–Goujard–Zograf–Zorich, then applies classical assembly identities and elementary tail estimates. The weighted permutation model and its unmarked Poisson approximation are prior results. We explicitly credit the earlier microscopic announcements and retain their unresolved normalization discrepancy with the short problem report. AI tools were used extensively; no external human peer review is asserted.

## The result

Take a square-tiled half-translation surface in the principal holomorphic quadratic stratum \(\mathcal Q(1^{4g-4})\). Count each maximal horizontal cylinder once and divide its area by the total surface area. All cylinder heights are allowed. For fixed genus \(g\), sample uniformly from isomorphism classes made from at most \(N\) unit squares, and first let \(N\to\infty\). Write \(\nu_g\) for the resulting law of the normalized areas \((X_i)\). The customary automorphism-weighted sampling has the same fixed-genus limit. The genus tends to infinity only after this first limit.

For every deterministic positive sequence \(s_g\) satisfying

\[
s_g\longrightarrow0,\qquad gs_g\longrightarrow\infty,
\]

the actual geometric cylinder-area process satisfies

\[
\sum_i\delta_{X_i/s_g}\ \Longrightarrow\ \operatorname{PPP}\!\left(\frac{dx}{2x}\right)
\]

vaguely on \((0,\infty)\). For a finite family of fixed pairwise disjoint compact intervals \([a_\ell,b_\ell]\subset(0,\infty)\), the counts converge jointly to independent Poisson variables with means

\[
\lambda_\ell=\frac12\log\!\left(\frac{b_\ell}{a_\ell}\right).
\]

Every fixed joint moment converges as well. The statement concerns the geometric cylinder areas, including their Gamma/Dirichlet marking, rather than only an auxiliary unmarked component model.

In Delecroix's highlighted window \([g^{-1/2},2g^{-1/2}]\), the limiting count is Poisson with parameter \((\log2)/2\). Both its mean and variance tend to \((\log2)/2\), and the probability of finding no cylinder in that window tends to \(2^{-1/2}\).

## Why the intermediate scale works

The argument starts from published formulas for the finite-genus geometric area law. A uniform comparison relates that law to the prior weighted-permutation model with weights \(a_j=\zeta(2j)/(2j)\). Conditional on component sizes, normalized independent Gamma variables give the Dirichlet area distribution.

The unmarked component law has a classical Poisson approximation on intermediate windows. The proof controls the expected effect of the Gamma marks across small, intermediate and large component sizes. This estimate works even when \(gs_g\) tends to infinity arbitrarily slowly. Concentration of the total Gamma mass then supplies the normalized-area process.

The count-moment conclusion uses additional bounds on all fixed moments and a uniform comparison on the principal part of the geometric law. Exceptional contributions vanish separately. These steps justify transferring unbounded count moments, as well as the point-process distribution, back to the geometric ensemble.

## Scope and earlier work

The setting is the principal holomorphic quadratic stratum, with the square-count limit taken before the genus limit. The theorem does not supply diagonal sampling \(N=N(g)\), arbitrary-stratum extensions, a joint statement about all directions on one surface, or either the microscopic regime \(gs_g=O(1)\) or the macroscopic regime \(s_g\asymp1\). The vertical marginal has the same law by symmetry. The stated result addresses intermediate areas rather than every possible interpretation of a full area spectrum.

Delecroix's report formulates the intermediate-area question in Problem 2; diagonal sampling is its separate Problem 3. The geometric law and uniform estimates used here come from Delecroix–Liu and Delecroix–Goujard–Zograf–Zorich, with Aggarwal's work underlying the uniform intersection-number coefficients. The exact weighted-permutation law is already in Delecroix–Goujard–Zograf–Zorich. The selected-component identity is due to Arratia–Tavaré, and Arratia–Barbour–Tavaré already provide the unmarked every-intermediate-rate Poisson approximation. The steps developed here are the explicit geometric comparison, Gamma-marking transfer and convergence of all fixed compact-window count moments.

The earlier Delecroix–Liu small-components announcements are prior intellectual contributions. Liu's thesis displays an all-multiplicity microscopic law at scale \((6g-6)^{-1}\); the Durham slides give a primitive microscopic version as a conjecture and display its \(1/(2x)\) tail. Fixed microscopic windows and a limiting-density tail do not by themselves supply the growing-window uniformity used here. The complete contents of the announced project are not determined by this preprint, and possible overlap remains a priority uncertainty. Historical first priority is not asserted.

The microscopic normalization distinction also remains unresolved: the exact Gamma total and thesis use \(6g-6\), while the short problem report prints \(4g-4\). Those factors produce different fixed microscopic laws. This preprint keeps them distinct and makes no new microscopic theorem or correction of the report.

## Research status and substantive contributions

This is an unrefereed preprint. AI tools were used extensively in the derivation, writing, computation and literature work; internal AI checking is not human peer review or formal proof certification. The complete source and verification archive accompanies the paper. Its finite controls support formulas and transcription; the written argument and cited geometric theorems supply the limiting result.

Substantive proof checks, counterexamples and precise source comparisons are welcome. Authorship and acknowledgments follow actual contributions. The cited researchers receive credit for their prior work; citations do not imply participation or endorsement.

## References

1. A. Aggarwal, *Large genus asymptotics for intersection numbers and principal strata volumes of quadratic differentials*, Inventiones Mathematicae **226** (2021), 897–1010. The uniform estimate is used through its explicit form in Delecroix–Liu.
2. R. Arratia and S. Tavaré, [*Independent process approximations for random combinatorial structures*](https://www.columbia.edu/cu/simontavare/STpapers-pdf/AT94.pdf), Advances in Mathematics **104** (1994), 90–154; Lemma 5, equation (126).
3. R. Arratia, A. D. Barbour and S. Tavaré, [*Limits of logarithmic combinatorial structures*](https://doi.org/10.1214/aop/1019160500), Annals of Probability **28** (2000), 1620–1644; Theorem 3.1.
4. V. Delecroix, [*What we do not know (yet) about square-tiled surfaces in large genus?*](https://doi.org/10.4171/owr/2024/41), Oberwolfach Reports **41/2024**, 2384–2387; Problem 2, p.2387. Report published 14 February 2025.
5. V. Delecroix, É. Goujard, P. Zograf and A. Zorich, [*Large genus asymptotic geometry of random square-tiled surfaces and of random multicurves*](https://doi.org/10.1007/s00222-022-01123-y), Inventiones Mathematicae **230** (2022), 123–224.
6. V. Delecroix and M. Liu, [*Length partition of random multicurves on large genus hyperbolic surfaces*](https://doi.org/10.4171/JEMS/1469), Journal of the European Mathematical Society **27** (2025), 5093–5131; online 7 June 2024.
7. M. Liu, [*Random multi-geodesics on hyperbolic surfaces*](https://www.imj-prg.fr/theses/pdf/mingkun_liu.pdf), doctoral thesis, Université Paris Cité, 2022; Remark 1.5.9, p.22.
8. M. Liu, [Durham Spectra and Moduli Seminar slides](https://www.math.univ-paris13.fr/~mingkun.liu/talks/Durham.pdf), February 2025; slides 26 and 195. The public announcements are credited without assuming the contents of unavailable work.
