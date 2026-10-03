# Clarifications accompanying the frozen report

Problem 30000330 / OWR-1106-004. Added 3 October 2026 after independent review.

The original six-file author freeze is preserved. The following precise readings address all four notes in [the independent audit](independent-audit/AUDIT.md) and accompany every use of the frozen report. They preserve its partial conclusions and its **unresolved, 5/5** outcome.

## 1 The upper injectivity bound depends on the surface

In the first established-input item of REPORT.md, only the positive lower injectivity bound is uniform in the homogeneity constant K alone. The upper estimate is

\[
d(S)\leq K\ell(S)+2K\log4,
\]

where \(d(S)=2\sup_p\operatorname{inj}_S(p)\) and \(\ell(S)=2\inf_p\operatorname{inj}_S(p)\). The right side depends also on the surface's systole. Thus the statement supplies a finite upper bound for each surface, not a K-only bound across all surfaces. The regular-cover towers in Attempt 2 have a common finite homogeneity upper bound and unbounded systole, so they expressly rule out the latter reading. No later deduction uses it.

## 2 The mapping-class cover uses closed balls

The displacement estimate in Attempt 4 gives

\[
S=\bigcup_{i=1}^{N_S(K)}\overline B_S(f_i(x),D_0(K^2)).
\]

The bar denotes a closed metric ball. A radius-r closed quotient ball has area at most \(2\pi(\cosh r-1)\). Equivalently, cover with open balls of radius \(r+\epsilon\), apply the area bound, and let \(\epsilon\downarrow0\). Either convention gives the same inequality (6) and subsequent necessary condition.

## 3 The subgroup count is restricted to that subgroup

If a surface is homogeneous using only classes in a subgroup H, define

\[
N_{S,H}(K)=\#\{[f]\in H:\ K(f)\leq K\text{ for some representative }f\}.
\]

Repeat Attempt 4 using this count. The result is

\[
N_{S,H}(K)\geq\frac{2(g-1)}{\cosh D_0(K^2)-1}.
\]

For finite H one has \(N_{S,H}(K)\leq|H|\leq84(g-1)\), hence the stated restricted threshold \(D_0(K^2)\geq\operatorname{arccosh}(43/42)\). One does not bound the unrestricted \(N_S(K)\) by \(|H|\) merely because a chosen transitive family uses H. The unrestricted necessary condition (7) still uses the full count.

## 4 Sequential claims can use actual admissible constants

The cited literature proves attainment of \(K(S)\). It is also possible to avoid relying on attainment throughout the sequential arguments: if \(K(S_j)\to1\), choose actual admissible homogeneity constants \(k_j\) such that

\[
K(S_j)\leq k_j<K(S_j)+1/j.
\]

Such constants exist by the defining infimum, and \(k_j\to1\). Use these actual constants in the displacement, class-count, and tube-count arguments. In particular the two proliferation conclusions concern \(N_{S_j}(k_j)\) and \(m_{S_j}(k_j,\gamma_j)\), with the same limits claimed in the report. No transitive family is assumed at an unattained infimum.

## Status

The review supports these partial estimates and the identification of their missing steps. It does not prove the needed upper counts, a genus-independent ordinary gap, or an infinite-type extension. The value approximately 1.36138 belongs to strong homogeneity only.
