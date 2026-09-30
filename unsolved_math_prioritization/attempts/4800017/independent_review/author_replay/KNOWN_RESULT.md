# Problem 17: the sharp polynomial recurrence bound is already proved

**4800017 / AMR-047-0017. Credited complete published resolution; recommend already_solved 0/5 after separate source review.**

## Exact original question

Frantzikinakis, *Some open problems on multiple ergodic averages*, arXiv:1103.3808v3 (16 October2016), Problem17, printed/PDF p.27, asks for the lower bound
\[
\mu(A\cap T_1^{p_1(n)}A\cap\cdots\cap T_\ell^{p_\ell(n)}A)
\ge \mu(A)^{\ell+1}-\varepsilon
\]
for some positive integer n, whenever p_i are rationally independent integer polynomials with zero constant terms. Section1.2, p.2, supplies the standing hypotheses: a probability space and invertible, commuting, measure-preserving transformations. Ergodicity, total ergodicity and weak mixing are not assumed. This is a recurrence inequality, not a pointwise-convergence assertion. The source also predicts bounded gaps for the good n.

## Exact published theorem

Nikos Frantzikinakis and Borys Kuca, *Joint ergodicity for commuting transformations and applications to polynomial sequences*, Inventiones mathematicae239 (2025),621–706, DOI [10.1007/s00222-024-01313-w](https://doi.org/10.1007/s00222-024-01313-w), **Corollary2.11**, proves the requested sharp lower bound for every system, every measurable A and every epsilon>0, and proves that the good positive integers have bounded gaps.

The full author manuscript [arXiv:2207.12288v2](https://arxiv.org/abs/2207.12288v2), dated18December2024, was retrieved. Corollary2.11 is on its p.10 and was visually inspected. The paper's introduction, item(iii), explicitly identifies this result as answering the 2016 source's Problem17. The paragraph immediately before the corollary instead points to Problem16, which is the adjacent characteristic-factor question; this cross-reference discrepancy does not change the theorem or its exact match. Theorem2.10 resolves that characteristic-factor problem, and Corollary2.11 supplies the additional sharp recurrence conclusion.

The publisher's primary page confirms publication on2January2025 and the volume/pages above. It is a subscription preview; we used the complete author manuscript for the exact theorem rather than infer a theorem from the abstract. We did not independently reconstruct the long seminorm-smoothing proof or compare the entire final journal PDF line by line.

## Hypothesis and convention audit

1. **Polynomial independence.** With zero constant terms, the original condition that no nontrivial rational linear combination is constant is equivalent to linear independence over Q: such a constant would have to be zero. For integer coefficient vectors, rank over Q equals rank over R (or C), by the nonzero-minor criterion. Thus the terminology in the theorem imposes no stronger polynomial condition. Same-degree independent families are included; distinct degrees are not required.

2. **Zero constants.** This is a standing assumption explicitly stated in Section2.2 and recalled immediately before Corollary2.11. It exactly matches the source. No non-intersective constant-shift extension is claimed.

3. **Transformations.** The paper defines a system using invertible commuting measure-preserving transformations on a probability space. No ergodicity condition is added in the corollary. Remarks elsewhere about total ergodicity concern a different product-of-integrals limit formula and must not be transferred to this recurrence theorem.

4. **Sign convention.** The corollary writes T_i^{-p_i(n)}A, while the original writes T_i^{p_i(n)}A. Apply the corollary to S_i=T_i^{-1}. These transformations remain invertible, commuting and measure preserving, and S_i^{-p_i(n)}A=T_i^{p_i(n)}A for every n. This preserves the exact set of good n and hence its bounded-gap property.

5. **Positive n and degenerate A.** The theorem's N denotes positive integers, so this is not the trivial n=0 intersection. If mu(A)=0 or1 the requested inequality is immediate, consistently with the theorem. All finite ell>=1 are covered.

6. **General probability spaces.** The theorem uses regular/Lebesgue probability spaces, and the source says these may be assumed for its applications. Even if the original quantifier is read as including arbitrary probability spaces, the particular recurrence statement reduces to the regular case as follows. Let G=Z^ell and define
\[
\Phi(x)(g)=1_A(T^g x),\qquad Y=\{0,1\}^G,\qquad\nu=\Phi_*\mu.
\]
The countable product Y is compact metrizable; Phi is measurable, and nu is a Borel probability. Let the ith shift be (sigma_i omega)(g)=omega(g+e_i). Then Phi(T_i x)=sigma_i Phi(x), so the shifts preserve nu and are invertible and commuting. For the cylinder C={omega:omega(0)=1}, Phi^{-1}(C)=A and
\[
\Phi^{-1}(\sigma_i^k C)=T_i^k A\qquad(k\in\mathbb Z).
\]
Consequently all the relevant intersection measures are identical in the original system and this compact symbolic factor. Applying the theorem to that factor proves the original assertion. If transformations are specified modulo null sets, countability allows restriction to a common conull set or the equivalent measure-algebra construction; finite intersection measures are unaffected.

These checks establish applicability of the published result to the full source statement, including its stronger bounded-gap prediction.

## Correction of the imported report

The pinned imported report says that Frantzikinakis–Kuca2025 gives only joint-ergodicity/characteristic-factor progress and does not record the sharp exponent. Corollary2.11 expressly supplies that exponent and bounded gaps. Therefore the imported `PARTIAL-PROGRESS` classification is contradicted by a directly matching primary theorem. Absence of a line on a progress webpage is not evidence against this explicit theorem. A fresh retrieval of the progress page failed in this audit; no assertion about its current contents is needed.

## Verification and limits

The checker records exact polynomial sign/rank checks and finite commuting-system diagnostics, including nonergodic systems. Those checks verify the elementary convention reductions only. They do not prove the general recurrence theorem or its bounded-gap conclusion. The complete resolution is credited to Frantzikinakis and Kuca, and this package is a source/status correction, not a new proof attempt or a discovery. No result about noncommuting transformations, arbitrary dependent polynomial families, effective gap bounds or pointwise convergence is asserted.
