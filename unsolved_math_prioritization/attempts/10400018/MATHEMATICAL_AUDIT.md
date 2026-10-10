# Independent acceptance audit: Kauffman degree bounds, first attempt

Problem 10400018 / AMR-103-0018, rank 1250. Audited 10 October 2026 UTC.

## Verdict and exact accepted scope

**Accept the mathematical report as a correct partial result, first attempt 1/5. Neither universal question is solved. No substantive correction is required.**

Distributed report: [MATHEMATICAL_REPORT.md](MATHEMATICAL_REPORT.md), 14,724 bytes, SHA-256
`6928a81126e7f177e86a610c51cd5a77e1874adad8f190a5e01ea2580a65bb29`.

This proof-only edition preserves the complete accepted mathematical arguments. Computational-results sections and scattered source-data corroborations are omitted. This is an AI-assisted, unrefereed mathematical audit; acceptance does not mean external human peer review, journal acceptance or formal proof-assistant certification.

The accepted mathematical content is:

1. For a connected sum (J=(\#_iP_i)\#(\#_j\overline{Q_j})) of positive knots and mirrors of positive knots,
   \[
   d_F(J)=s(J)-\sum_j\operatorname{span}_a F_{Q_j}.
   \]
   Hence (d_F(J)\le 2g_4(J)\), and separately (d_F(J)\le2g(J)) and (d_F(J)\le2u(J)).
2. The Euler-characteristic inequality is preserved by nonempty finite split unions. This includes split unions of the knots in item 1.
3. For (K_{n,m}=\#^nT(2,3)\#\#^m\overline{T(3,4)}), with (n\ge0) and (m\ge1),
   \[
   d_F=2n-10m,\quad s=2n-6m,\quad
   \overline{\mathrm{tb}}=2n-11m-1.
   \]
   Its Kauffman-bound defect is exactly (m), including examples with positive (d_F).

The identities and examples are consequences of existing theorems and elementary algebra. This audit makes no novelty or historical-firstness claim and does not count as another proof-search turn.

One harmless convention is made explicit here: a connected sum with no summands denotes the unknot. Alternatively, Theorem A may be read with at least one summand; the omitted empty case follows immediately from (F_O=1) and (s(O)=0).

## 1. Exact target and source applicability

The original Problem 1.18 on printed pages 392–393 of Ohtsuki's collection asks about
\[
d_F(L)=\min\deg_a F_L(a^{-1},z),\qquad
d_F(L)\le1-\chi(L),\qquad d_F(K)\le2u(K).
\]
The adjacent remark records a 15-crossing counterexample to the stronger slice-genus assertion. It does not state a counterexample to either requested bound. The audit visually checked both original pages. [Ohtsuki, Problem 1.18](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf).

Tanaka's printed page 185 explicitly defines a Seifert surface as compact and oriented with no closed components. It imposes no connectedness condition. Proposition 5.1 assumes sharpness of the Kauffman bound and then proves the two knot inequalities. Its statement, definition, and proof were visually checked. Thus the report's surface convention and its distinction between prior sharpness results and the present composite examples are correct. [Tanaka, Proposition 5.1](https://doi.org/10.18910/5513).

The audit used the inspected Kálmán manuscript as a distinct, explicitly identified mathematical dependency.

## 2. Polynomial normalization and degree algebra

The report uses the original Kauffman polynomial with plus skein relation, curl factors (a,a^{-1}), and writhe normalization (F_D=a^{-w(D)}\Lambda_D). KnotInfo's retained convention page explicitly gives those choices. No switch to an unannounced Dubrovnik or inverse-framing convention occurs. [KnotInfo conventions](https://knotinfo.org/descriptions/jones_homfly_kauffman_description/polynomial_defn.html).

Let (M(K)=\max\deg_a F_K), (m(K)=\min\deg_a F_K), and (b(K)=M(K)-m(K)). Then (d_F(K)=-M(K)), not (m(K)). Mirroring changes the curl factors and writhe signs, giving (F_{\overline K}(a,z)=F_K(a^{-1},z)). Therefore
\[
d_F(\overline K)=m(K)=-d_F(K)-b(K).
\]
The sign and the additional span term are both necessary.

For connected sums, (F_{K\#J}=F_KF_J). One can perform the usual skein reduction in the first summand with a distinguished arc for attachment; each terminal unlink factor has its original value multiplied by (F_J), and writhe is additive. This gives the normalization claimed in the report, without an additional split factor. Since the coefficient ring (\mathbb Z[z^{\pm1}]) is an integral domain, extremal coefficients in a product cannot cancel. Consequently (d_F) is connected-sum additive and
\[
d_F(K\#\overline K)=-b(K)\le0.
\]
There is no assertion of unknotting-number additivity. Nonvanishing is also harmless: the defining invariant specializes to 1 at (a=z=1), so a link's Kauffman polynomial is not the zero Laurent polynomial.

At a curl, the plus skein relation yields
\[
(a+a^{-1})\Lambda_D=z(\Lambda_{D\sqcup O}+\Lambda_D).
\]
Thus the split factor is exactly
\[
\delta=(a+a^{-1})/z-1.
\]
Its minimum inverse-(a) degree is (-1), with coefficient (z^{-1}\ne0). The skein reduction in one split factor then gives (F_{L_1\sqcup L_2}=\delta F_{L_1}F_{L_2}), so
\[
d_F(L_1\sqcup\cdots\sqcup L_r)=\sum_i d_F(L_i)-(r-1),\qquad r\ge1.
\]
In particular an (r)-component unlink has (d_F=1-r). The report does not omit the split-union correction or accidentally force connected spanning surfaces.

## 3. Positive knots, Rasmussen normalization, and mirroring

Kálmán's Definition 2 and following discussion explicitly state that positive diagrams are +adequate and identify their +state circles with their Seifert circles. Corollary 6 identifies writhe minus state-circle count with minimum (v)-degree minus one. His page 2 explicitly identifies (v=a^{-1}), and notes that the Dubrovnik version has the same degree distribution. These pages were visually checked, including the convention footnote. For a positive knot diagram with (c) crossings and (v_D) Seifert circles, the consequence is exactly (d_F=c-v_D+1). No positive-braid assumption is inserted. [Kálmán, Definition 2 and Corollary 6](https://arxiv.org/abs/math/0610659).

Rasmussen's Theorems 1, 2, and 4 and Section 5.2 give the slice bound, concordance homomorphism, and (s=c-v_D+1=2g=2g_4) for positive knots. Proposition 3.9 gives mirror sign reversal; Proposition 3.11 gives connected-sum additivity. Pages 1, 8, and 14 were visually checked. These statements use (s(T(2,3))=2). Orientation reversal does not change the crossing signs or this invariant; it exchanges the two canonical orientation-labelled Lee generators. Hence there is no confusion between mirror and concordance inverse. [Rasmussen, Khovanov homology and the slice genus](https://arxiv.org/abs/math/0402131).

The retained early Rasmussen manuscript also contains a conjecture equating (s) and (2\tau) for all knots. The accepted report explicitly excludes that conjecture. It never uses a (\tau) value or substitutes (\tau) for (s), so no unverified (s=2\tau) step is present.

Using these stated theorems and the algebra above,
\[
\begin{aligned}
d_F(J)&=\sum_i s(P_i)-\sum_j s(Q_j)-\sum_j b(Q_j)\\
      &=s(J)-\sum_j b(Q_j)\le s(J)\le |s(J)|\le2g_4(J).
\end{aligned}
\]
Every inequality has the correct direction, including when (s(J)<0). Pushing a Seifert surface into the four-ball gives (g_4\le g). The trace of an unknotting sequence gives an immersed disk with at most one transverse double point per crossing change; resolving the double points by orientable handles gives (g_4\le u). These supply the two required bounds for this class. They do not compare (g) and (u), and they do not require either to be additive.

## 4. Split-sphere compression and Euler characteristic

The proof of Lemma B correctly handles the potentially problematic creation and deletion of closed components. Here is the complete local accounting.

Take an oriented embedded spanning surface (F) with no closed components and make it transverse to a splitting sphere (S). The boundary of (F) misses (S), so all intersections are circles. An innermost intersection on (S) bounds a disk whose interior misses (F). Surgery along the disk removes an annular neighborhood of its boundary from (F) and replaces it by two disks, one pushed to each side of (S). The resulting surface is embedded and orientable with the same oriented boundary. Its Euler characteristic before discarding anything is (\chi(F)+2), and the number of intersection circles strictly decreases.

Only the surface component containing the chosen circle is changed. It had nonempty boundary. If the surgery is nonseparating, it remains one component with boundary and creates no closed component. If separating, it produces two components and at least one retains nonempty boundary, so at most one newly created component is closed. If its genus is (h\ge0), deleting it changes the total relative to the original surface by
\[
2-(2-2h)=2h\ge0.
\]
In particular, deleting a newly created sphere loses exactly the two units just gained by surgery, and does not lose any original Euler characteristic. This also covers a circle inessential on (F). The proof does not assume incompressibility or connectedness.

Iteration ends after finitely many intersections. The remaining surface is disjoint from (S), has no closed components, and splits into spanning surfaces (F_1,F_2) for the two link factors. Thus
\[
\chi(F)\le\chi(F_1)+\chi(F_2)\le\chi(L_1)+\chi(L_2).
\]
Conversely, each factor has a maximal-Euler surface: the set of attainable integers is nonempty and bounded above by the number of boundary components. Applying the same surgery to a maximal surface and the ball-boundary sphere puts it entirely in its factor's ball. Any component lying in the opposite, empty ball would be closed and is discarded as above. Euler characteristic cannot decrease; maximality precludes an increase above the maximum. The two resulting surfaces are disjoint and realize the sum. Therefore
\[
\chi(L_1\sqcup L_2)=\chi(L_1)+\chi(L_2).
\]
Induction and the split polynomial formula yield exactly the extension claimed in the report. This verifies the difficult convention-sensitive step without importing a connected-surface genus formula.

## 5. Explicit family and exact Kauffman-bound defect

Ng's printed page 428 distinguishes the negative ((4,-3)) torus knot from the table's other chirality and explicitly gives maximal (\mathrm{tb}=-12) and Kauffman upper bound (-11). The latter means (d_F(\overline{T(3,4)})=-10) after the framing-variable translation. This page was visually checked, and its publisher PDF was also read through the web tool. The argument uses Ng's identified negative torus knot, not an inferred chirality from the label (8_{19}). [Ng, page 428](https://msp.org/agt/2001/1-1/agt-v1-n1-p21-p.pdf).

Positive-diagram formulas give (d_F(T(2,3))=s(T(2,3))=2), (d_F(T(3,4))=s(T(3,4))=6), and (\overline{\mathrm{tb}}(T(2,3))=1). Hence (b(T(3,4))=4).

Torisu's Theorem 1.1 applies to arbitrary topological knots in standard contact three-space and gives (\overline{\mathrm{tb}}(K\#J)=\overline{\mathrm{tb}}(K)+\overline{\mathrm{tb}}(J)+1). It has no primeness, positivity, or polynomial-sharpness hypothesis. Its original printed page 359 was visually checked. [Torisu, Theorem 1.1](https://msp.org/pjm/2003/210-2/pjm-v210-n2-p10-p.pdf).

There are (n+m\ge1) summands, so the total correction is (n+m-1). Directly,
\[
\overline{\mathrm{tb}}(K_{n,m})=n-12m+(n+m-1)=2n-11m-1.
\]
Together with (d_F=2n-10m), the defect (d_F-1-\overline{\mathrm{tb}}) is (m). Choosing (n=6m) gives (d_F=2m>0), (s=6m), and maximal (\mathrm{tb}=m-1). These knots genuinely fail Tanaka Proposition 5.1's sharpness hypothesis while satisfying the target inequalities by Theorem A.

The optional ordinary-genus equality (g(K_{n,m})=n+3m) is also valid. Standard surfaces provide the upper bound, while the Alexander breadths of the torus-knot factors are 2 and 6. These follow, for example, from the usual coprime-torus formula ((t^{pq}-1)(t-1)/((t^p-1)(t^q-1))), of breadth ((p-1)(q-1)). Multiplicativity and the Seifert-matrix breadth bound provide the matching lower bound. No exact unknotting-number claim is made.

## 6. Source inspection and accepted pins

The audit rehashed the retained PDFs and visually inspected these pages:

- Ohtsuki: PDF 20–21, printed 392–393.
- Tanaka 2010: PDF 10, printed 185.
- Kálmán: PDF 2, 3, and 8.
- Rasmussen: PDF 1, 8, and 14.
- Ng: PDF 2, printed 428.
- Torisu: PDF 3, printed 359.

The remaining source proofs were not audited from foundations. The accepted result is explicitly conditional on these established input theorems; the report supplies the algebraic combination and split-surface argument in full.

The independently verified source pins are:

- Ohtsuki PDF: 4,731,008 bytes; `33d9c18c9ab8403a4d88b978b366451383edd12dd24760a77b9e25b666d9a8fd`.
- Tanaka 2010 PDF: 325,042 bytes; `e492dbecc95d2ae766ffc5dc184a34e580be69111067e3a94774718390450292`.
- Kálmán PDF: 267,626 bytes; `bb44765fae70fcee970f74f8a5f58cefc917da63f66ac9885457a351863d0f6f`.
- Rasmussen PDF: 310,975 bytes; `da5f17e5d649f48e39f8e58f1f7131e37fc57f45443a08456980ed4e23e040df`.
- Ng PDF: 128,486 bytes; `9fdde5e088cf66578a77d3e3fabaab2718b572541a1edea4c271c33c8c2f6d67`.
- Torisu PDF: 638,250 bytes; `d568df739fed4e1b1e493281bd2d9e2456941bb660c9336e0584645561567139`.
- KnotInfo ZIP: 16,471,344 bytes; `1aa3337b4767a2d655a7305999d62ef861920dc3d615d6b03f966d2f17f04f8a`.
- KnotInfo XLS: 82,738,176 bytes; `f4de747845b6432636c49e2dfa84b1c8d3bab681ee12b27402898cb3e4883be0`.

These are integrity pins for inspected copies, not independent provenance attestations. This edition distributes authored mathematical proofs and audits together with public verification metadata. Scripts, computational outputs, source PDFs, screenshots, extracted text, the workbook and source rows are excluded. Edition preparation did not newly retrieve, rehash or inspect source documents or datasets.

## Final disposition

Accept the distributed report identified above, with no mathematical patch required and with the empty-sum convention clarified. Preserve **partial, first attempt 1/5**. Arbitrary nonsplit links and arbitrary knots outside the proved class remain unresolved by this work. This acceptance is neither a complete solution nor a historical-novelty claim.
