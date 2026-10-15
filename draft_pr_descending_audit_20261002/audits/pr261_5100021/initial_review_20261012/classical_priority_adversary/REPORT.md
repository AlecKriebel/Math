# Independent classical priority audit of PR261 / 5100021

Audit date: 2026-10-12. Prepared before reading the submitted proof or prior priority verdicts. Mathematical validity of the proposed theorem remains conditional on the separate fresh verification. No external individuals were contacted; no remote or PR writes were made.

## Verdict

The even-period original/outer signed-area product is already a published theorem of Chavez-Caliz (online 2020, journal volume 2021). Its hypotheses cover the strict noncircular confocal elliptical pairs in this target, and its area convention accommodates oriented star polygons. It does **not** explicitly prove the focal pedal–antipedal product. The relevant focal area identities are additional mathematical content; treating them as automatic from the area-product theorem would leave a gap.

The exact target is attributed to an April 2020 experimental observation by Reznik, Garcia and Koiller, with no available proof cited in either the October 2020 v11 catalogue or the final February 2021 journal article. This audit found no pre-2026 primary source explicitly proving the target or supplying both focal area identities. That is a bounded negative finding, not a first-proof or novelty certificate.

Searches also surfaced the October 1, 2026 EulerSolve abstract claiming precisely the target and both area reductions. This audit has not read that proof/source and does not decide its validity, authenticity, or priority. That separate contemporary-preprint audit must be resolved before any first-proof claim. Discovery of the invariant itself is already prior art regardless of how that question is resolved.

## Exact comparison with the strongest classical theorem

[Chavez-Caliz, *More About Areas and Centers of Poncelet Polygons*](https://armj.math.stonybrook.edu/pdf-Springer-final/020-0154.pdf), DOI [10.1007/s40598-020-00154-8](https://doi.org/10.1007/s40598-020-00154-8), Arnold Mathematical Journal 7 (2021), 91–106; online 14 August 2020.

Theorem 6, printed p104, concerns a Poncelet polygon P inscribed in one concentric ellipse and circumscribed about the other. Q is the ordered polygon formed by consecutive tangents to the outer ellipse at P's vertices. For even n it proves A(P)A(Q) constant. Formula (5), p93, defines the ordered algebraic shoelace area. Page 94 defines general position by transverse intersection in CP². The proof on p104 removes poles of the meromorphic product by cancellation with degenerate-polygon area zeros. Theorem 3, p93, is the introductory repetition of Theorem 6.

Short exact quote (13 words): “If n is even, then A(P) · A(Q) stays constant within the Poncelet family.”

The relevant pages p94 and p104 were rendered locally and visually inspected. The statement and complete proof were also extracted as text. This audit does not substitute its own proof for the published theorem.

### Independent check of general position

Write the outer and caustic conics as

\[
\Gamma:\;x^2/a^2+y^2/b^2=z^2,\qquad
\gamma:\;x^2/(a^2-\lambda)+y^2/(b^2-\lambda)=z^2,
\]

with a>b>0, c²=a²-b² and 0<λ<b². Solving the simultaneous equations gives four finite complex points:

\[
x^2=\frac{a^2(a^2-\lambda)}{c^2},\qquad
y^2=-\frac{b^2(b^2-\lambda)}{c^2},\qquad z=1.
\]

There is no intersection at infinity: the coefficient determinant at z=0 is nonzero. All four points have xy≠0. In the finite chart the determinant of the two gradients is

\[
\frac{4xy\lambda c^2}{a^2b^2(a^2-\lambda)(b^2-\lambda)}\ne0.
\]

Thus transversality holds for every pair in the proposed strict confocal domain. This check fails or changes at λ=0, λ=b², or a=b, consistently with the proposed exclusions.

### Stars, period, finiteness and zero areas

The polygon and shoelace definitions do not require a simple convex boundary. For an elliptic-caustic billiard with primitive rotation number w/N and even N, gcd(w,N)=1 forces w odd. Central reflection agrees with the half-orbit shift: P(i+N/2)=−P(i). The tangent construction preserves the chosen orbit order. A polygon should not be reordered spatially to remove its self-intersections.

Consecutive boundary tangents cannot be parallel for this real strict-elliptic-caustic orbit. On a centered ellipse, parallel distinct tangents occur at antipodal points. A chord joining antipodal points passes through the center and cannot be tangent to a nondegenerate centered ellipse. Hence the real outer vertices used in the classical product are finite. This does not by itself establish finiteness of the focal antipedal vertices, which the focal bridge must check separately.

The theorem is a product identity without division by either area. Its application does not require positive or nonzero signed areas. It does not assert the focal antipedal area exists or stays finite at a zero; those are separate construction questions.

The paper's elliptic-curve discussion uses a Poncelet transformation of order n. The standard genuine-period interpretation is appropriate here. Do not infer coverage merely from an even padded list that repeats an odd primitive orbit. This audit imposes the assigned primitive-period hypothesis throughout.

## Catalogue priority and source distinctions

[Reznik, Garcia, Koiller, *Fifty New Invariants of N-Periodics in the Elliptic Billiard*](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf), DOI [10.1007/s40598-021-00174-y](https://doi.org/10.1007/s40598-021-00174-y), Arnold Mathematical Journal 7 (2021), 341–355; online 18 February 2021.

The final article declares signed cross-product areas on p343. It defines original-side pedal feet on p344 and original-vertex antipedal intersections in §3.5, p347. Table 5, p348, has k403,b = Am A*m, N≡0 (mod 4), pole f1 or f2, discovery 4/20, value “?”, proof “?”. Table 2, p345, separately credits Chavez-Caliz for k106 = A′A. The proof-column convention on p344 distinguishes an unrecorded proof from an unknown formula. Therefore k403,b's “?” is not merely an absent numerical value. Table 5 p348 was rendered and visually inspected.

[The v11 primary catalogue](https://arxiv.org/html/2004.12497v11), dated 29 October 2020, has the same k403,b status in Table 5, printed p7. Its title is *Eighty New Invariants in the Elliptic Billiard*. The final article is 2021, not 2022. The 2022 date belongs to Stachel's later motion paper.

The assertions are prior experimental observations; they are not proof certificates. Other abbreviated catalogue entries cannot be assumed as lemmas to prove this entry merely because they are also called invariants.

## Why an extra focal bridge is required

Let pF be original-side focal pedal signed area, qF be original-vertex focal antipedal signed area, A original area, and T outer tangent area. A valid reduction can, for example, establish

\[
p_F=K(a,b,\lambda,N,w)T,\qquad
q_F=R(a,b,\lambda,N,w)A,
\]

with K and R independent of phase and with all ordered constructions well-defined. Then pF qF = KR AT follows from the classical theorem. This argument is only as strong as the two identities. It must not divide by qF or assume qF≠0.

### Exact control against the direct-theorem shortcut

The accompanying `check_classical_bridge.py` uses rational arithmetic, checks every outer-ellipse membership, every caustic side tangency and every consecutive intersection determinant, and computes ordered signed areas. Consider outer axes (5,3), inner axes (3,12/5), and outer focus F=(4,0). The inner ellipse is strict and concentric but not confocal. Its axis ratios differ, it shares no point at infinity with the outer ellipse, and its four complex intersection points have nonzero coordinates; it is in general position.

Two members of its primitive four-Poncelet family are

\[
P_0=((5,0),(0,3),(-5,0),(0,-3)),
\]

\[
P_1=((3,12/5),(-3,12/5),(-3,-12/5),(3,-12/5)).
\]

Both have AT=1800. But

\[
p_F(P_0)q_F(P_0)=202500/289,
\qquad
p_F(P_1)q_F(P_1)=-34596/4375.
\]

These are in the scope of the classical concentric-even theorem, but outside the confocal billiard target. They establish that its conclusion alone does not entail the focal area product. They do not falsify the target.

### Independently checked elementary geometry, short of a full bridge

For a confocal caustic of axes A=√(a²−λ), B=√(b²−λ), focus F=(c,0), and tangent contact X=(A cos t,B sin t), the focal pedal foot is

\[
Q=\left(\frac{A(c+A\cos t)}{A+c\cos t},
          \frac{AB\sin t}{A+c\cos t}\right).
\]

Direct substitution gives |Q|²=A². Thus the known focal-pedal circle is an elementary support-function consequence. In Cartesian contact coordinates it is the projective map

\[
Q=\frac{A^2}{A^2+cX_x}(X_x+c,X_y).
\]

Its denominator is positive on the real caustic since A>c. The map is projective, rather than equiaffine, so it does not automatically preserve area products.

The chord between successive caustic contacts through an original vertex P is its caustic polar. Under this map the corresponding focal-pedal side has equation

\[
(P_x+c)Q_x+P_y Q_y=A^2+cP_x.
\]

By comparison the focal antipedal line at P is

\[
(P_x-c)Z_x+P_y Z_y=|P|^2-cP_x.
\]

The support terms differ and depend on P. Circle membership, polar duality, and central symmetry therefore supply useful geometry but do not supply the phase-independent signed-area coefficients. I have not derived both coefficients independently here. The direct-theorem route is **blocked at that exact bridge**, rather than recorded as a complete classical proof.

## Cited and citing primary-source comparison

| Primary source and locator | Strongest relevant verified statement | Relation to target / exact gap |
|---|---|---|
| Chavez-Caliz (2020/2021), Theorem 6 p104 | Even original area × outer tangent area | Applies to the confocal pair and signed order; needs both focal identities. |
| RGK v11 (2020), Table 5 p7; final (2021), Table 5 p348 | Experimental target itself, proof “?” | Prior discovery; does not certify proof or an unrestricted interpretation of N. |
| [Akopyan–Schwartz–Tabachnikov](https://arxiv.org/abs/2001.02934), v2 (25 Jan 2020), Theorem 3 p3 and proof pp10–11 | Odd original/outer area ratio for concentric ellipses; Poncelet-grid and duality mechanisms | Wrong parity and derived polygons; no antipedal-area bridge found. |
| [Bialy–Tabachnikov](https://arxiv.org/abs/2001.08469), v2 (5 May 2020), §4 pp6–11 | Outer-tangent pedal centroid and sum of squared distances; even focal distance products; center distance products for N≡0 mod4 | Metric products and centroids are not ordered signed areas. No focal area bridge found. |
| [Stachel](https://doi.org/10.1007/s40879-021-00524-2), *On the motion of billiards in ellipses* (2022), Theorem 4.3 p1614, Lemma 5.3 p1620 | Canonical Jacobi parametrization, coprime turning number, quarter-period caustic tangent-length pairing | Strong classical input for an area bridge; no pedal/antipedal area theorem in this paper. |
| [Garcia–Reznik](https://arxiv.org/abs/2011.06640), *Invariants of Self-Intersected N-Periodics*, v3 (19 Jan 2021; initial preprint 2020), Table 1 p8 | Selected low-period basic and focal-inversion invariants; original/outer product credit | No k403,b entry or focal pedal–antipedal proof found. Hyperbolic self-crossing cases must not be confused with elliptic-caustic stars. |
| [Roitman–Garcia–Reznik](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0188.pdf), *New Invariants of Poncelet–Jacobi Bicentric Polygons* (2021), Theorem 2 pp625–627, Appendices A–C | Constant limiting-point pedal perimeters; polar/inversion relation to confocal billiards | A perimeter statement. Area videos/observations do not furnish the target theorem. |
| [Garcia–Reznik–Roitman](https://arxiv.org/abs/2112.02545), *New Properties of Harmonic Polygons*, v3 (29 Sep 2022), §4 pp10–11 | Polar correspondence with homothetic ellipses; odd N=3,5 lateral harmonic-area reciprocal sum | Different families, parity and areas. No target bridge found. |
| [Reznik–Garcia–Stachel](https://arxiv.org/abs/2009.02581), v3 (16 Sep 2020); [journal DOI](https://doi.org/10.1007/s13366-021-00588-x) | Areas of continuous pedal-like curves, with moving pole; Steiner polygon background | Integrating an entire curve with moving pole differs from finite orbit-area products at fixed focus. |
| [Connes–Zagier](https://people.mpim-bonn.mpg.de/zagier/files/amm/114/fulltext.pdf), Monthly 114 (2007), 909–914, §4 pp913–914 | Maximal parallelogram perimeter and connection to four-billiards | Classical four-periodic geometry; no focal pedal–antipedal area theorem found. |
| [Mitrea](https://arxiv.org/abs/1008.0110), *On the Area of Pedal and Antipedal Triangles* (2010), abstract only | Triangle pedal/antipedal area formulas | Only triage-level inspection here. Triangle identity does not establish N divisible by four. |

The downloaded PDFs were searched globally for area/pedal/antipedal/polar terms, with complete relevant text sections read. Visual inspection was concentrated on the decisive Chavez-Caliz and RGK final pages; it is not claimed for all pages of all sources.

### Winding caution for the classical Jacobi input

Stachel's full orbit step is 4Kw/N. With N=4n, stepping by n vertices shifts by wK; this is K or 3K modulo 4K for coprime stars. A literal claim that it is always K loses the winding factor. For the tangent norm, however, dn has period 2K, so odd w gives the same reciprocal identity dn(u)dn(u+wK)=B/A. The quarter-pairing mechanism is therefore already classical after this explicit winding check. A novel-proof discussion should not present that identity or canonical parametrization as new.

## Search limits and publication wording

Queries covered the exact identifiers and titles, focal pedal/antipedal area and billiard terms, and the cited/citing literature around the original/outer theorem. Primary sources, author-hosted papers, arXiv versions, and official journal copies formed the evidence base; aggregators were used only to locate primary works. A search engine's failure to return a theorem is not evidence that none exists. Unindexed proofs, books not fully searched, other languages and unpublished private communications remain outside this bounded audit. No outreach is proposed or initiated.

Strongest verified result: the relevant classical area product is applicable to the proposed domain; the source catalogue explicitly recorded the target without a cited proof; the focal bridge is not an automatic consequence of that classical theorem.

Exact remaining gap for a classical priority defeat: locate a pre-2026 proof of k403,b itself, or a source proving sufficient focal signed-area identities under the target's primitive-star and zero-area scope. The bounded search did not close that gap. Exact remaining gap for an overall priority claim: separately authenticate and verify the October 1, 2026 contemporary preprint, as well as validate the submitted mathematics.

Recommended wording, conditional on the other audits: “We prove the scoped focal pedal–antipedal product recorded experimentally by Reznik, Garcia and Koiller. The reduction uses the known even-period original/outer area-product theorem of Chavez-Caliz and classical confocal/Jacobi geometry.” Any claimed new contribution should identify the actually new focal area bridge, with contemporary prior proofs credited if verified. Avoid “new invariant,” “first proof,” or “independent discovery” until priority evidence permits those statements.

Completion: 100% of this assigned bounded classical literature audit; this is **not** a percentage of the discovery goal, a proof certification, or a complete-literature guarantee.
