# PR 210: independent physical Cartesian geometry audit

Source head: `2180d64b648b81ac660a792f7823d0b715f9cf12`. Original `PROOF.md` SHA-256: `5a78b9d2fb1f7a0a80e556f2e2b759875bdbba055a454c148524eb44879add7e`.

## Recommendation and strongest verified result

**Accept the mathematical theorem in its explicitly stated scope. No central proof gap or true-domain counterexample was found.** The proof establishes constancy of the product of the two **signed** focal-pedal areas of the **outer tangent polygon**, for every strictly nested nondegenerate confocal elliptical caustic with odd primitive period, including coprime star turning numbers. This is an audit recommendation to the coordinator, not a publication action. There is no novelty or priority conclusion.

The universal result rests on the inspected canonical theorem and a valid meromorphic pole/character/divisor argument. Independent exact Cartesian identities and exact triangles verify the geometric bridge; a separate physical reflection program supplies finite, explicitly uncertified numerical stress evidence. No unsupported new invariant is imported to prove the target.

All suspected proof gaps below were resolved within the stated domain. Numerical computation is not substituted for their universal resolution. Hyperbolic or collapsed caustics are outside that domain. The circle is handled separately as a limit/control. Odd repeated traversals extend the primitive result by a direct scaling of the ordered area sum.

## Independence and source identity

The timestamped `INDEPENDENT_CLAIM_MAP_FROZEN.md` was frozen at **2026-10-15T11:56:58Z** after reading only intake and the original `PROOF.md` / `SOURCES.md`. The fresh Cartesian mechanism and program were authored before reading inherited reviews or verification programs. The inherited review and both programs were subsequently read, not imported or executed in this shard. No other current review or root research note was read. A later parent progress message reported an exact triangle pair already independently derived here; that overlap is disclosed in the log and is not presented as separate corroboration from an uninformed reviewer.

The primary PDFs were reused read-only from the supplied private directory, hashed, independently extracted, and the relevant full pages rendered and visually inspected. `SOURCE_CHECKS.json` records links, hashes, page checks and the source-only typo noted below. Private PDFs/text/renders are excluded from the authored manifest and ignored locally. No Git, provider, SQLite, or external communication mutation occurred.

The arXiv v11 Table 7, printed p. 9, labels the primed product **k605,a**. The published Table 7, printed p. 349, labels the same construction **k606**; published k605 is the original-orbit product. Section 2 uses signed cross-product area, and section 3.7 identifies the prime as the outer polygon. The introduction specifies a confocal **ellipse pair**. The source does not explicitly settle primitive/repetition/star terminology; the candidate's precise least-period formulation and proved star coverage should not be represented as a verbatim source definition.

## Cartesian derivation independent of Jacobi feet

Write a boundary point as

\[
 P(t)=(a\cos t,b\sin t),\qquad c^2=a^2-b^2,\quad F_+=(c,0).
\]

Its tangent has normal \(n=(\cos t/a,\sin t/b)\) and equation \(n\cdot X=1\). Orthogonal projection gives

\[
 Q_+(t)=F_++\frac{1-n\cdot F_+}{n\cdot n}n
 =\left(\frac{a(c+a\cos t)}{a+c\cos t},
         \frac{ab\sin t}{a+c\cos t}\right).
\]

The canceled denominator factor cannot vanish for real \(t\), because \(a>c>0\). Set \(u=\tan(t/2)\) and \(d=b/(a+c)\), so \(d^2=(a-c)/(a+c)\). Then

\[
 Q_+(u)=a\left(\frac{1-d^2u^2}{1+d^2u^2},
                  \frac{2du}{1+d^2u^2}\right).
\]

Thus the focal pedal foot is exactly the rational circle parametrization with stereographic parameter \(du\), and \(Q_+\cdot Q_+=a^2\). For the other focus the parameter is \(u/d\), equivalently \(Q_-(P)=-Q_+(-P)\). These are algebraic identities, including the omitted stereographic endpoint by continuity. Substitution \(\cos t=-\mathrm{sn}\,w,\ \sin t=\mathrm{cn}\,w\) recovers the submitted formula with the correct focus and signs.

To check the **actual outer polygon**, let \(\ell_j\) be the tangent at \(P_j\), and construct \(U_j=\ell_j\cap\ell_{j+1}\). The side from \(U_{j-1}\) to \(U_j\) is exactly \(\ell_j\); no billiard chord is substituted. The fresh program first solves these intersections and then projects onto their literal side directions. Its separate tangent-normal projection agrees to the recorded precision. Finite side segments are never used to clamp the projection.

The real canonical parametrization is injective modulo \(4K\). Distinct adjacent vertices have shift \(0<2v<2K\), so they cannot be antipodal; the adjacent tangents cannot be parallel. An outer side cannot collapse either: that would give three distinct real tangents to a nondegenerate ellipse through one point, whereas a tangent pencil contains at most two. Star intersections and self-crossings do not change this ordered-line argument.

## Exact nonnumerical orbit controls

Take squared boundary semiaxes \((a^2,b^2)=(21,16)\) and confocal parameter \(\lambda=336/25\). The caustic squared semiaxes are \((189/25,64/25)\), both positive and strictly smaller, with the same focal square 5.

Two exact ordered triangular billiards are

\[
 (\sqrt{21},0),\quad(-3\sqrt{21}/5,16/5),\quad(-3\sqrt{21}/5,-16/5)
\]

and

\[
 (0,4),\quad(-21/5,-8/5),\quad(21/5,-8/5).
\]

Their exact boundary, caustic tangency, unit-direction reflection, outer-side incidence and auxiliary-circle checks all vanish symbolically. Projection onto actual outer sides gives respectively

\[
 (B_+,B_-)=((49\sqrt{21}+7\sqrt5)/10,
             (49\sqrt{21}-7\sqrt5)/10)
\]

and \((112/5,112/5)\). Both products are exactly **12544/25**, although the individual areas differ between these two distinct family members. This finite exact check validates concrete geometry; it is not claimed to prove all triangle phases or all periods by itself.

## Adversarial audit of every universal dependency

1. **Canonical coverage and convention.** Stachel's Theorem 4.3 and (4.9), printed p. 1614, use the numerical eccentricity of the caustic as the Jacobi **modulus**, and give exactly the displayed boundary parametrization and step. For any strictly nested pair, \(0<\beta/b<1\) determines a unique \(v\in(0,K)\) through \(\mathrm{cn}\,v=\beta/b\); confocality gives the displayed formula for \(a\). Real injectivity implies that least-period closure is \(N(2v)=4K\tau\), with coprimality and \(0<\tau<N/2\) after orienting the orbit. The canonical parameter runs once monotonically round the ellipse, so this integer is the physical winding. The proof does not limit itself to \(\tau=1\).

2. **A source-only typographical error.** The preceding printed p. 1613 of Stachel visually displays an erroneous factor \((-1)^j\) in the shift of \(\mathrm{dn}(u+2jK)\). In fact dn has real period \(2K\). The theorem, its positive real definition, and [DLMF Table 22.4.3](https://dlmf.nist.gov/22.4#T3) give the correct identity. The submitted proof uses the correct classical shifts and does not depend on that erroneous source display. This is not a defect in the candidate.

3. **All complex poles are accounted for.** On the sn torus \((4K,2iK')\), sn has two simple poles and hence degree two. Its equation \(\mathrm{sn}\,w=a/c\) has the two displayed simple roots \(r\pm v\), because the quarter-shift formulas give that value, \(\mathrm{cn}\) is nonzero there, and \(\mathrm{dn}\) changes sign but is nonzero. Common sn/cn poles are removable in the rational foot formula. On the actual common-function torus \((4K,4iK')\), the extra imaginary translates must be retained, as the candidate does. The sn torus alone is not a period torus of the full foot map.

4. **Residues really are collinear, including all lifts.** At \(r-v,r+v\) the numerators agree and lie on the isotropic direction \((1,i)\); the denominator derivatives oppose. The residues are \(R,-R\). Their translates by \(2iK'\) are both acted on by the same reflection \(J\), preserving collinearity. A real step or a cyclic index wrap cannot connect one imaginary lift to the other. If one substituted noncollinear residues, a determinant double pole would generally remain; the program checks this symbolic negative control.

5. **The N=3 pole/neighbor coincidence is harmless, and has been checked explicitly.** With \(N=3,\tau=1\), \(v=2K/3\). At a pole phase, vertices 0 and 1 are singular; the third is at \(r+2K\), where \(\mathrm{sn}=-1/k\), and is regular. It is the same regular neighbor of both singly singular incident edges. Writing

   \[
   Q_0=R/\epsilon+A+O(\epsilon),\quad
   Q_1=-R/\epsilon+B+O(\epsilon),\quad Q_2=C+O(\epsilon)
   \]

   gives a zero double-pole coefficient and simple-pole coefficient
   \[
      \tfrac12\det(R,A+B-2C).
   \]
   The factor 2 on C is essential in this small-period bookkeeping; a derivation assuming distinct regular neighbors would need repair. The submitted argument only bounds the order term by term and remains valid. This exact Laurent identity is in the fresh program. It does not assume that the total simple residue is nonzero.

6. **There cannot be a hidden third singular vertex.** At a fixed pole phase, the two denominator roots differ by one actual step. Coprimality makes all \(N\) real phase classes distinct modulo \(4K\); exactly the two adjacent indices meet those roots. The imaginary copies remain separate modulo the doubled imaginary lattice. Every incident edge has either one singular endpoint or the already checked collinear pair. The index-cut edge closes with the true \(4K\tau\) period. This works for stars and for N=3.

7. **Reduced lattice and characters are correct.** The area has periods \(2v=\tau L\) and \(4K=NL\); Bezout gives \(L=4K/N\). On \((L,4iK')\) there are at most two simple poles, centered at \(p=iK'\) and \(3p\). The imaginary half-shift reflects one coordinate, so it negates the determinant area. Reflection \(w\mapsto2K-w\) also reverses the cyclic vertex order; the two minus signs cancel. The step period shifts the reflection center to \(b=K-v\). No orientation sign is lost.

8. **The zero-divisor argument neither assumes nonvanishing nor divides by an area.** For \(F(z)=T(b+z)\), evenness, real period L and imaginary anti-period 2p force \(F(p+L/2)=0\), and likewise at \(3p+L/2\). Both points are regular: real half-period displacement cannot equal an allowed pole modulo the lattice. They are distinct. If poles disappear, F is holomorphic on a compact torus and hence constant; anti-periodicity makes it zero. Otherwise anti-periodicity forces both poles, each simple; equality of total zero and pole degrees then proves that the two identified zeros exhaust the divisor and are simple. The product \(F(z)F(z+L/2)\) has every possible pole canceled, including poles of either factor. It is constant by compactness. There is no circular appeal to the target invariant.

9. **Odd parity selects precisely the other focus.** Since \(2K=NL/2\), odd N gives the real half-period class \(L/2\); even N gives a full-period class. The independently derived focus relation thus gives the target for odd N and equality of the two individual areas for even primitive N, without claiming even product invariance. Reversing the orbit changes both area signs and preserves their product. Cyclic shifts and switching the focus names also preserve it.

10. **Limits and exclusions.** All denominators and lattice distinctions used above hold strictly within \(a>b>0,\ \beta>0,\ 0<v<K\). At c=0 the Jacobi-pole derivation need not be used; a regular star rotating in a circle gives the constant directly. Collapsed/hyperbolic caustics require a different statement. For an odd r-fold repetition of a primitive odd orbit, each ordered shoelace sum is r times the primitive area, hence the product is r-squared times its constant. This extends the result to that possible reading of odd source N. Even repetitions of odd orbits can have a constant product and must not be treated as counterexamples to the deliberately primitive even controls.

No unresolved proof gap remains after these checks. The classical canonical parametrization and elementary compact-torus divisor facts are explicit inputs, rather than fresh claims certified by finite tests.

## Independent physical stress program and results

`physical_geometry_check.py` uses **no Jacobi functions** and imports no submitted file. With \(A=a^2,B=b^2\), a ray p+td meets the boundary again at

\[
 t=-\frac{2(p_xd_x/A+p_yd_y/B)}{d_x^2/A+d_y^2/B},
\]

and its direction reflects by \(d\mapsto d-2(d\cdot n)n/(n\cdot n)\). The periodic caustic is determined independently by bisection of the physical lifted winding after N impacts, launching at \((0,b)\) along \((-\sqrt{A-\lambda},-\sqrt\lambda)\). At other eccentric angles, tangent contacts are constructed by pulling the caustic back to the unit circle. Every resulting sample is checked for closure, correct winding, distinct vertices, boundary incidence, physical reflection and tangency to the same confocal ellipse before its area product is accepted as evidence.

The full saved run has **22 cases / 194 sampled orbits**: 17 strict odd families, four even controls, and one circle control. It covers convex pentagons, multiple primitive stars, axes and asymmetric phases, aspect ratios from \(1+10^{-12}\) to 1000, a 101-period near-boundary caustic, and a nearly collapsed elliptic caustic with \(\beta^2\approx3.8147\times10^{-66}\). The most nearly coincident distinct vertices have normalized separation about \(7.81\times10^{-33}\), and the smallest normalized adjacent tangent determinant is about \(3.91\times10^{-33}\); both stay nonzero in this finite run.

All checks pass at **170 decimal digits** with the explicit threshold \(10^{-48}\). The worst normalized closure residual is approximately \(7.50\times10^{-74}\), worst reflection residual \(1.16\times10^{-75}\), worst caustic tangency residual \(1.77\times10^{-83}\), and worst strict-odd product spread \(4.69\times10^{-93}\). These are observed residuals, not rigorous numerical error bounds. Normalizations and each phase's raw values are retained in `results.json`.

The four even product spreads are approximately 0.35994, 0.31021, 0.46406 and 0.05839, while their two focus areas agree. Thus the apparatus detects the expected wrong-parity non-invariance. Separate controls recompute projections after rotation/translation and uniform scaling, and verify orientation reversal, cyclic indexing, central-symmetry focus pairing and degree-four scaling of the product. All pass. No claim of numerical universality, interval enclosure, formal proof checking, or exhaustive parameter coverage is made.

## Reproduction and package limits

Run the standalone program using the audit-specified Python environment and `-B`; it writes only an explicitly requested result file. It is independent of working directory and private sources. The full run is deterministic; the output records its own program SHA-256 and installed library versions.

```text
/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr256_5100017/initial_review_20261013/reproduction_environment/bin/python -B physical_geometry_check.py --output fresh_results.json
```

`AUTHORED_MANIFEST.json` binds every **retained** nonprivate authored artifact except itself. The private source copies/extractions/renders are neither distributed nor required by the program. The report does not certify novelty, the rest of the campaign, or any future modification of the frozen source head. Adjudication completion: **100% of this assigned physical-geometry audit**; the coordinator retains the final integration decision.

Historical diagnostic receipt: an earlier `--quick` run passed six cases / 54 sampled orbits and temporarily saved `quick_results.json`, before the N=3 symbolic additions and the final full run. Its exact intermediate timestamp was not captured. That transient receipt was deliberately removed **before** the original seven-file seal; the coordinator's earlier listing caused the subsequent clarification. No raw copy was preserved or recreated. It is excluded from the final packet. The canonical full program and `results.json` remain unchanged.
