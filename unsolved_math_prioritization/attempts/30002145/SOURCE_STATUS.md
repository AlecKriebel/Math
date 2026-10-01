# 30002145: known fixed-line symmetric-gradient classification

**Accepted disposition:** already_solved as a source-status partial in the original whole-space/local blow-up setting. The new complete mathematical/source gate passes with no unresolved actionable findings; no novel resolution, arbitrary-domain globalization, paper or DOI is claimed.

Three independent families, root universal audit and a new complete adversary pass. Original substantive attempts remain0/5. Extensive AI verification is unrefereed and is not formal proof-assistant certification. Mathematical sections1 onward retain exact original/reviewed bytes. See ACCEPTANCE.md and acceptance.json for current evidence and the separately verified remote disposition.

## 1. Target and source provenance

The pinned UnsolvedMath record, ID 30002145 / OWR-12008-005, asks for the structure of sufficiently regular maps whose symmetric gradient lies in the line spanned by a fixed symmetric product. It does not specify a domain, a regularity threshold, or a conjectured conclusion. Its August 2026 assessment calls the classification incomplete while citing the 2020 paper below.

The requested [problem page](https://www.unsolvedmath.com/problems/30002145) was tried first. The web reader could not access it; a direct request returned HTTP 403. The immutable dataset record was then retrieved and its full source corpus verified against the repository manifest (see `provenance.json`). No prior-report entry matching the numeric ID, code, or title was found in the pinned research-results corpus.

The original source is Rindler's contribution, pp. 2247–2249 of [Oberwolfach Report 36/2012](https://publications.mfo.de/bitstream/handle/mfo/3307/OWR_2012_36.pdf?isAllowed=y&sequence=1). On p. 2248 the question occurs inside an explanation of a published lower-semicontinuity proof. The text immediately discusses both the failure of an overly restrictive separated form and the structural information used to obtain good blow-ups. It is not presented there as an unsolved conjecture. The referenced [2011 paper](https://arxiv.org/pdf/1008.2089) already treats the two-dimensional cases in Propositions 4.7 and 4.9 and Example 4.8.

## 2. Exact literature coverage

De Philippis and Rindler, [*Fine properties of functions of bounded deformation—an approach via linear PDEs*](https://www.aimspress.com/article/doi/10.3934/mine.2020018), *Mathematics in Engineering* **2** (2020), 386–422, gives the all-dimensional result in **Theorem 2.10**, [arXiv version, pp. 12–14](https://arxiv.org/pdf/1911.01356). It allows signed measures in the identity

\[
Eu=P\nu,\qquad u\in BD_{\mathrm{loc}}(\mathbb R^d).
\]

In particular, its two symmetric-product cases cover smooth maps with any sign-changing scalar coefficient. They are not restricted to positive tangent measures. A convenient smooth formulation is as follows; all expressions are modulo an infinitesimal rigid motion \(\omega(x)=Rx+c\), \(R^T=-R\).

### Independent vectors

For linearly independent \(a,b\), every smooth solution has

\[
\begin{aligned}
u(x)={}&a\{H_1(x\cdot b)+(x\cdot b)(x\cdot v)\}\\
&+b\{H_2(x\cdot a)+(x\cdot a)(x\cdot v)\}
-v(x\cdot a)(x\cdot b)+\omega(x),
\end{aligned}
\]

where \(v\perp\operatorname{span}\{a,b\}\) is constant and \(H_1,H_2\) are one-variable functions. Its coefficient is

\[
Eu=(a\odot b)\{H_1'(x\cdot b)+H_2'(x\cdot a)+2x\cdot v\}.
\]

### Parallel, nonzero vectors

Their line is spanned by \(e\odot e\) for a unit vector \(e\). With an orthonormal basis \(e,v_2,\ldots,v_d\), put \(s=x\cdot e\), \(t_j=x\cdot v_j\). The corresponding normal form is

\[
u(x)=e\left\{H(s)+\sum_{j=2}^d t_j P_j'(s)\right\}
-\sum_{j=2}^d v_j P_j(s)+\omega(x).
\]

It gives

\[
Eu=(e\odot e)\left\{H'(s)+\sum_{j=2}^d t_j P_j''(s)\right\}.
\]

If either original vector is zero, \(Eu=0\) and \(u\) is rigid on each connected component. In dimension one the nonzero case permits arbitrary one-variable maps.

These formulas are written for smooth maps to match the source question; the cited theorem contains the stronger BD regularity statement. Writing the split as “independent versus parallel” avoids interpreting the printed condition \(a\ne\pm b\) without a normalization convention.

## 3. Direct checks and why the simpler guess fails

Differentiating the displayed formulas makes every mixed quadratic term cancel except \(2(x\cdot v)(a\odot b)\). In the parallel formula the terms \(e\odot v_j\,P_j'(s)\) similarly cancel. Thus the formulas genuinely satisfy the target inclusion; their necessity is the cited theorem, not a conclusion of the checks.

In three dimensions, the polynomial map

\[
u(x_1,x_2,x_3)=(x_2x_3,x_1x_3,-x_1x_2)
\]

has \(Eu=2x_3(e_1\odot e_2)\). It cannot be a sum of functions of \(x_1\) and \(x_2\) plus a rigid motion, because its strain depends on \(x_3\). This explains the transverse quadratic term.

In the parallel case, Rindler's already-published example

\[
u(x_1,x_2)=(4x_1^3x_2,-x_1^4)
\]

has \(Eu=12x_1^2x_2(e_1\odot e_1)\), excluding one-directional dependence modulo a rigid motion.

`verify.py` checks both general smooth templates symbolically in dimensions 2, 3, and 4 and checks both polynomial examples. It uses exact symbolic identities, with no numerical tolerance or search. These are verification tests, not a new proof or counterexample to an open question.

## 4. Scope boundary and disposition

The theorem is explicitly global on \(\mathbb R^d\), the setting of blow-ups in the original discussion. The displayed differential identities also give the familiar local normal forms on sufficiently small adapted boxes. We do not assert that arbitrary nonconvex domains admit a single global pair of one-variable profiles: disconnected slices create a distinct globalization issue, and the imported record specifies no such target.

Accordingly, the defensible result is a **source-status correction**, not a new mathematical discovery. The record's claim that its cited 2020 source lacks a complete classification is contradicted by Theorem 2.10 in the whole-space setting. If a different global-domain problem was intended, it must be stated separately before allocating a proof budget. No further novel-proof search was undertaken.
