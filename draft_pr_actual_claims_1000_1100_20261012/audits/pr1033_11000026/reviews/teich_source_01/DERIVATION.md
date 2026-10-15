# Independent derivation: exact Teichmüller source interface

Created 2026-10-13 22:10 UTC. Review family `teich_source_01`; immutable submitted head `6322305d37b8131f034a1b4c3c5e861e4b04844f`.

This derivation was established from the submitted `PROOF.md` and freshly retrieved primary-source bodies before reading any submitted acceptance label or historical audit. It treats the target as a hypothesis. The independently reviewed mathematical claim is

\[
\forall g\ge2\ \exists c_g\in[0,\infty)\ \forall o\in\mathcal T(\Sigma_g)\ \forall r\ge0\ \forall x,y\in\overline B_T(o,r):
\quad\exists\gamma:[0,1]\to\overline B_T(o,r)
\]

with \(\gamma\) continuous and rectifiable, \(\gamma(0)=x\), \(\gamma(1)=y\), and

\[
L_T(\gamma)\le d_T(x,y)+4c_g,
\qquad d_T(X,Y)=\tfrac12\inf_h\log K(h).
\tag{D1}
\]

The constant is allowed to depend on the fixed genus. The claim neither assumes nor obtains uniformity in genus, metric convexity of the balls, a common radial retraction, or a transfer from a quasiisometric model.

## Source input, with its quantifiers

Fix a closed oriented surface \(S=\Sigma_g\), \(g\ge2\). This surface has finite topological type and negative Euler characteristic, so it is in the setting of Lenzhen–Rafi (LR), printed p267, and Fortier Bourque–Rafi (FR), arXiv v3, pp1 and 4. In particular, the hyperbolic conformal structures and essential curve classes used in LR are available.

LR Theorem 15, printed p282 / PDF p16, gives a finite multiplicative constant \(K_S\) such that for every measured foliation \(\mu\), every Teichmüller geodesic \(G\), and every triple \(a,z,b\) appearing in that order on \(G\),

\[
\operatorname{Ext}_z(\mu)\le K_S\max\{\operatorname{Ext}_a(\mu),\operatorname{Ext}_b(\mu)\}.
\tag{D2}
\]

The topology-only convention is explicit on LR printed pp268–269; the uniformity is reflected in the proof's finite case analysis on pp282–284. Replace \(K_S\) by \(\max\{K_S,1\}\), if necessary, and put

\[
c_S=\tfrac12\log K_S\ge0.
\tag{D3}
\]

Although D2 is stated for all measured foliations, simple essential closed curves suffice for the metric conclusion below. Consequently no identification between laminations and foliations, no foliation-specific constant, and no attained maximizing foliation is required for this derivation. LR's own extension from curves to all measured foliations uses continuity and density on p282 with the same constant; taking limits does not change that constant.

## Direct distance deduction, avoiding a maximizer

FR v3 Section 2, p6, equation (2.2), supplies the formula, in the half-log metric,

\[
d_T(o,w)=\sup_{\alpha\in\mathcal C_0(S)}\frac12\log\frac{\operatorname{Ext}_w(\alpha)}{\operatorname{Ext}_o(\alpha)}.
\tag{D4}
\]

Here each \(\alpha\) is an essential simple closed curve. Its extremal length at a point of \(\mathcal T(S)\) is finite and positive, so dividing and taking logarithms is valid. Fix an entirely arbitrary center \(o\), entirely arbitrary endpoints \(a,b\), and any \(z\in[a,b]\). For every such curve \(\alpha\), D2 yields

\[
\begin{aligned}
\frac12\log\frac{\operatorname{Ext}_z(\alpha)}{\operatorname{Ext}_o(\alpha)}
&\le c_S+\max\left\{
\frac12\log\frac{\operatorname{Ext}_a(\alpha)}{\operatorname{Ext}_o(\alpha)},
\frac12\log\frac{\operatorname{Ext}_b(\alpha)}{\operatorname{Ext}_o(\alpha)}
\right\}\\
&\le c_S+\max\{d_T(o,a),d_T(o,b)\}.
\end{aligned}
\]

Take the supremum in D4. The resulting inequality is

\[
\boxed{d_T(o,z)\le\max\{d_T(o,a),d_T(o,b)\}+c_S.}
\tag{D5}
\]

The constant has no dependence on \(o,a,b,z\), any radius, any curve or foliation, injectivity radius, or thickness. Endpoint cases \(z=a,b\) follow immediately because \(c_S\ge0\). If the endpoints coincide, take the constant segment. These observations extend the strictly ordered triples in the proof of Theorem 15 to every point of every segment. LR Theorem 17's proof, printed pp284–285 / PDF pp18–19, explicitly gives this same non-strict D5. Theorems C and 17 are therefore corroboration rather than a reliance on the unspecified open/closed convention of their symbol \(B\).

## Geodesics, metric length, and the original closed ball

FR v3 Section 2, p4, defines \(d_T\) by one half of the logarithm of quasiconformal dilatation. On p5 it states that every Teichmüller line is distance minimizing and that any two distinct Teichmüller-space points lie on a unique such line. Thus minimizing segments exist between all endpoints, and their metric lengths equal \(d_T\). Constant segments cover identical endpoints. The flow \(\operatorname{diag}(e^t,e^{-t})\) agrees with this normalization; no multiplicative metric rescaling enters D3 or D5.

D5 is exactly the source-side hypothesis of the submitted retreat lemma. Its application can also be checked directly: for \(r\ge c_S\), move \(x\) and \(y\) inward along minimizing radial segments by respectively \(\alpha=\min\{c_S,d_T(o,x)\}\) and \(\beta=\min\{c_S,d_T(o,y)\}\), obtaining \(a,b\) with center distances at most \(r-c_S\). Then D5 puts the whole minimizing segment \([a,b]\) in \(\overline B_T(o,r)\). The radial segments remain in that same closed ball. The concatenation is continuous and rectifiable and satisfies

\[
L_T(\gamma)=\alpha+d_T(a,b)+\beta
\le d_T(x,y)+2\alpha+2\beta\le d_T(x,y)+4c_S.
\]

For \(r<c_S\), the path through \(o\) has length at most \(2r<2c_S\le d_T(x,y)+4c_S\). The cases \(r=c_S\), \(r=0\), \(c_S=0\), repeated endpoints, endpoints at the center, and boundary endpoints use non-strict membership and constant segments where appropriate. A different fresh family is assigned the general metric lemma; this paragraph verifies only its concrete source-to-target interface.

The metric estimate therefore establishes D1 with \(c_g=c_{\Sigma_g}\), conditional only on the standard stated external results D2, D4, and geodesic existence.

## Exact-question consequence and compatible sources

Farb's original chapter defines \(\Sigma_g\) as closed and oriented on printed p10 / PDF p17. Printed p24 / PDF p31 defines the distance-two sphere condition with a radius-independent bound for an interior-ball path; printed p25 / PDF p32 asks whether \(\mathcal T(\Sigma_g)\) with the Teichmüller metric has that property. For \(d_T(x,y)=2\), D1 gives \(C_g=2+4c_g\). For every fixed \(k>0\), it gives \(N_g(k)=k+4c_g\) at every center and every radius, which also matches the broader metric-space formulation in PZ's published PDF p7. Same-sphere points are included since the theorem already covers all closed-ball pairs. There is no restriction to one chosen basepoint. The original distance-two question requires no constant across different genera.

PZ Theorem I on published PDF p7 concerns the dual wall space \(X_C(S)\), with the bound \(k+6\). Its ensuing discussion distinguishes that result from an answer in the original Teichmüller metric; it supplies no impossibility theorem, lower bound on intrinsic Teichmüller-ball distance, or extra hypothesis to impose on LR. D1 uses neither its model nor its constant. FR's nonconvex-ball result only rules out the direct geodesic staying inside every ball, and hence is also compatible with the concatenated path in D1.

## Exact remaining dependence

This is an independent check of the submitted argument's theorem interface and mathematical deduction, not a new proof of every earlier paper cited inside LR or of Teichmüller's and Kerckhoff's foundational theorems. LR Theorem 15, the half-log Kerckhoff formula, and minimizing geodesic existence are explicit external dependencies. Their bodies and critical pages were inspected; their premises fit the closed genus-at-least-two claim. No unsupported additional premise was found. No historical novelty, priority, or current worldwide open-status conclusion follows from this review.
