# PR104 / 600008: classical-mechanism priority audit

Audit date: 2026-10-06 UTC. Candidate: preserved complete `../original_source_authentication_20261006/original_attempt/ANALYTIC_CRITERION.md`, SHA256 `608217a2ffc120a965b165f5b6065edd83f8cf94c5e77f0f95a0326640db2dae`. Mathematical validity was an input, not the subject of another proof search.

**Verdict:** no demonstrably new mathematical contribution is established by this audit. The separated metric and decisive period identity are exact specializations of published classical formulas. The analytic criterion is therefore a classical corollary at the mechanism level. This is **not** evidence that an earlier author actually stated or resolved this exact on-surface null-chain problem: that historical application question remains open, with one especially close unread fulltext. Recommend holding any novelty promotion; retain the result as an explicit analytic derivation, with bounded possible novelty only in the application and correctly normalized counts.

## Exact claim and counts

For (a,b,c>0), the surface is (x^2/a+y^2/b+z^2/c=1), with ambient metric (dx^2+dy^2-dz^2). Put (f^2=a\sin^2t+b\cos^2t), (L=\int_0^{2\pi}\sqrt{f^2/(c+f^2)}\,dt=2\pi M). The candidate claims that GKT's equator-to-north-tropic-to-equator return map has positive **path lift**

\[
\rho=\frac{\pi}{L}-\frac12=\frac{1-M}{2M}.
\]

Consequently, (n) return-map steps with actual winding (r) close iff (M=n/(n+2r)). A literal chain of (n) full tropic-to-tropic arcs additionally requires even (n). If \(\rho=p/q\) in lowest terms, least return period is (q); least arc count is \(\operatorname{lcm}(2,q)\). Reducing a circle rotation modulo one loses actual winding information and cannot establish these counts.

GKT already supplies the invariant density proportional to the integrand defining (L), the return map, and its Poncelet property. Those are not new. The candidate's extra step is identification of the displacement in that density, followed by its simplification. [GKT primary preprint](https://arxiv.org/abs/0705.0188), §§4–5.

## 1. The separated metric is classical after an explicit continuation

Izmestiev–Tabachnikov, *Ivory's theorem revisited*, Example 3.7 (preprint p.29), publishes the Euclidean ellipsoid metric

\[
ds^2=(\lambda-\mu)\left[
\frac{\lambda\,d\lambda^2}{4(a-\lambda)(b-\lambda)(c_E-\lambda)}-
\frac{\mu\,d\mu^2}{4(a-\mu)(b-\mu)(c_E-\mu)}\right].
\]

Use (c_E=-c), Euclidean third coordinate (Z=iz), (\lambda=-u), (\mu=-v). The surface and ambient metric become exactly the target ones, and the formula becomes

\[
g=\frac{v-u}{4}\left[
\frac{u\,du^2}{(a+u)(b+u)(c-u)}-
\frac{v\,dv^2}{(a+v)(b+v)(c-v)}\right],
\]

exactly the candidate's metric. This continues an algebraic coordinate/metric identity, **not** the source's real Euclidean ordering hypotheses or its unit-energy Riemannian geodesic theorem. The relevant real belt has (u\in[-a,-b]), (v\in[0,c]). Setting (g=0) separates the two positive quadratures. Global seam continuation and the switch at a tropic must still be supplied; the candidate supplies them. [Author preprint](https://arxiv.org/abs/1610.01384), Examples 3.5–3.7 and §3.1.

## 2. The decisive period relation is exactly an old third-kind connection formula

Assume (a>b>0) (exchange (a,b) if needed). Define

\[
I_u=\int_{-a}^{-b}\sqrt{\frac{u}{(a+u)(b+u)(c-u)}}\,du=\frac L2,\qquad
I_v=\int_0^c\sqrt{\frac{v}{(a+v)(b+v)(c-v)}}\,dv.
\]

Let (D=a(b+c)), (\delta=(a-b)/(b+c)>0), (\gamma=c/a>0), (k^2=\delta\gamma\in(0,1)), and (P(z)=z(z+a)(z+b)(z-c)). On the negative cut use

\[
z=c-\frac{a+c}{1+\delta s^2},\quad 0\le s\le1;
\]

on the positive cut use

\[
z=-a+\frac{a+c}{1+\gamma s^2},\quad 0\le s\le1
\]

(the second substitution reverses orientation). Both give

\[
\frac{|dz|}{\sqrt{-P(z)}}=
\frac{2\,ds}{\sqrt D\sqrt{(1-s^2)(1-k^2s^2)}}.
\]

Multiplying by \(-z\) on the first cut and (z) on the second gives

\[
I_u=\frac{2}{\sqrt D}\big[(a+c)\Pi(-\delta,k)-cK(k)\big],\qquad
I_v=\frac{2}{\sqrt D}\big[(a+c)\Pi(-\gamma,k)-aK(k)\big].
\]

Here \(\Pi(n,k)\) is the standard complete third-kind integral with denominator \(1-n\sin^2\theta\). In [DLMF 19.7.8](https://dlmf.nist.gov/19.7#E8), set amplitude \(\varphi=\pi/2\), its (c=\csc^2\varphi=1), \(\alpha^2=-\delta\), \(\omega^2=-\gamma\). The required \(\alpha^2\omega^2=k^2\) holds. With [19.20.1](https://dlmf.nist.gov/19.20#E1), (R_C(0,y)=\pi/(2\sqrt y)), this yields

\[
\Pi(-\delta,k)+\Pi(-\gamma,k)-K(k)
=\frac{\pi}{2\sqrt{(1+\delta)(1+\gamma)}}
=\frac{\pi\sqrt D}{2(a+c)},
\]

hence **\(I_u+I_v=\pi\)**. All radicals are positive; both characteristics are negative, so no principal value or pole hypothesis is hidden. The (a=b) case is the continuous elementary limit. `check_equivalence.py` verifies the rational substitutions and normalization by exact integer polynomial arithmetic; it does not search for a new proof.

This is a third-kind parameter connection relation, not the familiar bilinear first-/second-kind (K,E) Legendre relation. DLMF traces its symmetric-integral antecedent through §§19.21(iii),19.25.14 to Zill–Carlson (1970). The original Zill–Carlson article was not accessible and was **not** read. The official authored DLMF formula is directly checked; no earlier article-specific equation is asserted without inspection.

The candidate's belt topology identifies the return displacement as (I_v). Combining (I_v=\pi-L/2) with circumference (L) gives the claimed \(\rho\); solving (n\rho=r) gives (M=n/(n+2r)). Thus the only application bridge beyond the classical formulas is the exact real return-map displacement and count normalization.

## 3. Existing rotation/billiard theorems do not automatically settle that bridge

| Primary source read | What it establishes for this comparison | Exact mismatch or gap |
|---|---|---|
| [Khesin–Tabachnikov (2009)](https://www.math.utoronto.ca/khesin/papers/Lorentz_AIM.pdf), §§4.2–4.4 | Lorentz Clairaut, pseudo-confocals, generic geodesic/billiard integrability | No target displacement formula located in the read scope |
| [Dragović–Radnović (2009)](https://arxiv.org/abs/0902.4233), §4 | Euclidean on-surface rotation is a ratio of separated quadratures | Source has (0<c<b<a), unit energy, caustic parameter in specified finite intervals; (c_E=-c) and a null/infinite-caustic limit are outside those hypotheses |
| [Dragović–Radnović (2012)](https://arxiv.org/abs/1108.4552), §§3.2,5.2 | Ambient pseudo-Euclidean billiard closure/Cayley conditions; Remark 5.5 credits GKT's on-surface null Poncelet theorem | Straight reflected chords and their counts are not surface null arcs; dropping the infinite caustic does not supply the target third-kind displacement or tropic convention |
| [Casas–Ramírez-Ros (2011)](https://web.mat.upc.edu/rafael.ramirez/res/pdf/siads11.pdf), §§4.3–4.4, Appendix 7 | Classical ambient Euclidean rotation/frequency calculus | Different map and segment count; its standard range (0<\rho<1/2) cannot be imported as the target's unbounded path lift |
| [Jovanović–Jovanović (2015)](https://arxiv.org/abs/1407.0555), §§2–3, Theorem 3.2, §5 | Lax/Chasles and Jacobian translation for the ambient billiard map | Does not prove ordinary Jacobian torsion for the target third-kind real displacement |
| [Fujimori et al. (2017)](https://arxiv.org/abs/1701.02134), §2 | Minkowski curvature coordinates/tropics | No closure criterion in the read section |

The inherited Wüstholz 2017 slides' final null-geodesic statement and Fields talk abstract were read as primary announcement evidence. They do not display this normalized formula or a full derivation. The analytic rationality criterion should not be promoted as a solution of the motivating finite algebraic Cayley determinant problem.

## Priority uncertainty and bounded recommendation

The closest exact-system source is Dragović–Radnović, *Topological invariants for elliptical billiards and geodesics on ellipsoids in the Minkowski space*, Russian 2015, English 2017. [MathNet record](https://www.mathnet.ru/eng/fpm1640) and [publisher record/abstract](https://link.springer.com/article/10.1007/s10958-017-3378-4) were read. Public fulltext routes failed or required subscribed access; no bypass was attempted. Its null-flow, rotation and closure formulas remain **uninspected**. This is a concrete potentially decisive gap, not evidence of novelty. Original classical treatises and the original Zill–Carlson fulltext also were not exhaustively inspected.

The independent searches preceded receipt of other priority conclusions. No absence of a keyword match was counted as novelty evidence. The strongest justified conclusion is: **standard metric + standard third-kind identity + candidate-specific global count identification imply the analytic criterion.** Earlier actual publication of that application is neither demonstrated nor excluded. Hold a “novel solution” claim pending legitimate inspection of the exact-system topology paper and its cited predecessors. If retaining this manuscript now, describe it as an explicit classical analytic derivation and disclose this bounded priority uncertainty. No outreach or prepared letters, external edits, Git actions, or publication actions were performed.
