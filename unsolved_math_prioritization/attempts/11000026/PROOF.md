# Uniform intrinsic detours in Teichmüller balls

## Result

For every fixed closed oriented surface \(S=\Sigma_g\), \(g\ge2\), there is a finite constant \(c_g\ge0\), depending only on \(g\), with the following property. In the actual Teichmüller metric
\[
 d_T(X,Y)=\frac12\inf_{h}\log K(h),
\]
for every center \(o\), every radius \(r\ge0\), and every pair
\(x,y\in\overline B_T(o,r)\), there is a continuous rectifiable path
\(\gamma\subseteq\overline B_T(o,r)\) from \(x\) to \(y\) such that
\[
 \operatorname{length}_T(\gamma)\le d_T(x,y)+4c_g.
 \tag{1}
\]
In particular, for every fixed \(k>0\), same-sphere points at distance \(k\) admit such a path of length at most
\[
 N_g(k)=k+4c_g.
\]
This proves the all-center, all-radius, every-fixed-\(k\) almost-convexity formulation and, by taking \(k=2\), the distance-two formulation in Farb's Question 3.5 [F]. No constant uniform in genus is asserted.

The substantive Teichmüller-theoretic input is Lenzhen–Rafi's uniform additive quasiconvexity theorem [LR, Theorem C and Theorem 17]. The deduction below supplies the exact-original-ball path. No historical novelty of this elementary deduction is asserted.

## A geodesic metric lemma

Let \((M,d)\) be a geodesic metric space. Assume there is \(c\ge0\) such that, for every center \(o\) and every \(a,b\in M\), one can choose a geodesic segment \([a,b]\) satisfying
\[
 d(o,z)\le\max\{d(o,a),d(o,b)\}+c
 \quad\text{for every }z\in[a,b].
 \tag{2}
\]
Then any two points \(x,y\in\overline B(o,r)\) can be joined within the same closed ball by a continuous rectifiable path of length at most \(d(x,y)+4c\).

**Proof.** If \(r<c\), concatenate geodesics from \(x\) to \(o\) and from \(o\) to \(y\). Each segment is inside \(\overline B(o,r)\), and its total length is at most \(2r<2c\le d(x,y)+4c\).

Suppose now that \(r\ge c\). Choose a geodesic from \(o\) to \(x\). On it, let \(a\) be the point at distance
\[
 d(o,a)=\max\{d(o,x)-c,0\}
\]
from \(o\). Choose \(b\) analogously on a geodesic from \(o\) to \(y\). Write
\[
 \alpha=d(x,a)=\min\{c,d(o,x)\},\qquad
 \beta=d(y,b)=\min\{c,d(o,y)\}.
\]
In particular, \(0\le\alpha,\beta\le c\), and
\[
 d(o,a),d(o,b)\le r-c.
\]
By (2), the chosen geodesic from \(a\) to \(b\) lies in
\(\overline B(o,(r-c)+c)=\overline B(o,r)\). The radial subsegments from \(x\) to \(a\) and from \(b\) to \(y\) also remain inside that ball. Their concatenation with \([a,b]\) is therefore a continuous rectifiable path in the original closed ball. The triangle inequality gives
\[
 d(a,b)\le d(a,x)+d(x,y)+d(y,b)=\alpha+d(x,y)+\beta.
\]
Consequently the concatenation has length
\[
 \alpha+d(a,b)+\beta
 \le d(x,y)+2\alpha+2\beta
 \le d(x,y)+4c.
\]
If \(a=b\), the middle segment is constant. The cases \(r=c\), \(c=0\), and \(r=0\) are thus included. This proves the lemma. \(\square\)

## Application in the exact Teichmüller metric

Teichmüller space of a closed finite-type surface is geodesic; its minimizing geodesics have length equal to the Teichmüller distance in the stated normalization. For example, [FR, Section 2] recalls the normalization and the geodesic theorem.

For the fixed surface \(S\), Lenzhen–Rafi prove a finite uniform extremal-length quasiconvexity constant \(K_S\). The extremal-length part of their Theorem A, stated as Theorem 15, holds for every measured foliation and every ordered triple on a Teichmüller geodesic. Their comparison constants depend only on the topology of \(S\), as specified in their notation convention on printed pages 268–269. Their Theorem C states the resulting uniform additive quasiconvexity of balls; Theorem 17 and its proof on printed pages 284–285 establish precisely
\[
 d_T(o,z)\le\max\{d_T(o,a),d_T(o,b)\}+c_S
 \quad (z\in[a,b]),
 \tag{3}
\]
where \(c_S\) is independent of \(o,a,b,z\). One may enlarge \(K_S\) to be at least 1 and take \(c_S=\tfrac12\log K_S\): this is the conversion from their extremal-length inequality through Kerckhoff's formula in the stated normalization. In particular, \(c_S\) has no dependence on radius, center, curve, foliation, injectivity radius, or thickness.

The non-strict inequality (3), explicitly established in that proof, directly includes closed-ball and boundary endpoints; no interpretation of an open-ball symbol is needed. Apply the metric lemma with \(M=\operatorname{Teich}(S)\) and \(c=c_S\). This gives (1). With \(S=\Sigma_g\), denote the constant by \(c_g\). \(\square\)

## Scope and interpretation

For same-sphere endpoints with \(r\ge c_g\), the construction is especially simple: move each endpoint inward by exactly \(c_g\), connect those two points by a Teichmüller geodesic, and return along the other radial segment. The middle segment lies in the original radius-\(r\) ball because the quasiconvexity theorem is applied to the smaller radius-\((r-c_g)\) ball. The additive error is compensated, rather than discarded.

The middle segment has length at most \(d_T(x,y)+2c_g\) by the triangle inequality alone. No Lipschitz radial retraction, fellow travelling, thin-part restriction, discrete approximation, change of metric, or quasiisometric transfer is used.

Consequently, if \(d_{\overline B(o,r)}^{\mathrm{int}}\) is the intrinsic length distance of the closed ball, then
\[
 d_T(x,y)\le d_{\overline B(o,r)}^{\mathrm{int}}(x,y)
 \le d_T(x,y)+4c_g
 \quad (x,y\in\overline B_T(o,r)).
\]
This is compatible with the existence of nonconvex Teichmüller balls [FR]: the path furnished here need not be the direct geodesic from \(x\) to \(y\).

Petyt–Zalloum [PZ, published page 7] prove almost convexity of a wall model with constant \(k+6\) and say that their theorem does not directly answer Farb's questions. The proof here does not transfer that theorem or its constant. It instead applies the elementary lemma to the older exact-metric theorem [LR]. The statement about the wall theorem's scope imposes no contrary mathematical hypothesis on this deduction.

## References

[F] Benson Farb, *Some problems on mapping class groups and moduli space*, in *Problems on Mapping Class Groups and Related Topics*, Question 3.5, printed page 25; preceding almost-convexity definition on printed page 24. https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf

[LR] Anna Lenzhen and Kasra Rafi, *Length of a curve is quasi-convex along a Teichmüller geodesic*, Journal of Differential Geometry 88 (2011), 267–295. Theorem C, printed page 268; Theorem 15, printed page 282; Theorem 17 and proof, printed pages 284–285. https://www.math.toronto.edu/rafi/Papers/Convexity.pdf

[FR] Maxime Fortier Bourque and Kasra Rafi, *Non-convex balls in the Teichmüller metric*, Journal of Differential Geometry 110 (2018), 379–412. ArXiv version 3, 29 August 2017, Section 2. https://arxiv.org/abs/1606.05170v3

[PZ] Harry Petyt and Abdul Zalloum, *Constructing metric spaces from systems of walls*, Mathematische Annalen 396, article 38 (2026), Theorem I and following discussion on published PDF page 7. https://doi.org/10.1007/s00208-026-03534-1
