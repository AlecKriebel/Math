# Later realization and priority audit of PR124 / problem10400231

Audit date: 2026-10-06 UTC. Scope: Ohtsuki–Turaev Conjecture 12.26, ordinary integral Alexander polynomial and prescribed full first homology. This is a literature/priority audit; mathematical correctness of the submitted counterexample was supplied as PASS by the parent at 2026-10-06T19:54:21. No new central proof, publication, external communication, or tracked-project mutation was undertaken.

## Result

**Priority remains uncertified for the explicit conjecture application. Strong prior augmentation machinery already implies the odd-prime obstruction, subject to the cited rank-one normalization interface. No authenticated later paper explicitly presenting this pair as a refutation of Conjecture 12.26 was located in the bounded search.** These statements are distinct: an earlier theorem can imply a counterexample without anyone having previously published the conjecture refutation.

The potentially new portion is therefore the explicit application to the printed full-group realization conjecture, the simple family, and its direct integral presentation proof. This audit does not establish that those portions are new. It does not support advertising the modular obstruction as a newly discovered general necessary condition. The characteristic 2 translation of the torsion polynomial-part route was deliberately left unverified; the supplied integral-matrix proof covers all primes and the historical parent audit reports an old integral interface making that proof a formal corollary.

## Exact target and independence

For a closed connected oriented M with H1(M;Z)=Z⊕T, the proposed necessary condition is

\[
\operatorname{ord}_{t=1}(\Delta_M\bmod p)\geq\dim_{\mathbf F_p}(T\otimes\mathbf F_p).
\]

The submitted pair is H=Z⊕(Z/p)^3 and Δp=t+(p³−2)+t^-1. It has the printed reciprocity and augmentation, while its reduction is t^-1(t−1)^2. The obstruction excludes it because 2<3. Ordinary Δ retains integral content; its ambiguity is ±t^k. Dividing by |T| or otherwise taking rational primitive content changes the question.

The complete original source_record.json, prior_imported_report.json, and COUNTEREXAMPLE.md were read before the substantive checkpoint at 19:58:22 UTC. That checkpoint, preserved in RESEARCH_LOG.md, independently distinguished Alcaraz's b1 realization from full-group realization and identified its integral presentation/specialization as substantial prior ingredients. The first other current-review information arrived at 20:02:31 UTC. The later Truman lead was then independently authenticated and checked. SOURCE_LEDGER.json records input/retrieval hashes, exact URLs, dates, and inspected locations; SEARCH_LEDGER.json records all 64 queries on this date. No absence or earliest-priority claim follows from these searches.

## Closest later mathematical precedent

Christopher Brian Truman's authenticated UMD dissertation, *Turaev Torsion of 3-Manifolds with Boundary*, has repository date 2006-04-24 and handle1903/3453. Printed35/PDF44 extends mod-r torsion to integral b1=1 using the polynomial part [τ]. Printed45/PDF54, Theorem 2.2, gives the augmentation inclusion τ modr∈I^(b−2), where H1(M;Zr) is free of rank b≥2; the setting is compact connected oriented manifolds with nonempty boundary and χ=0. It attributes that inclusion to Turaev 2002, II.4.4. The dissertation's rank-one paragraph refers to II.3 and III.4.3. Only the inclusion is needed here, not the leading determinant coefficient. [Authenticated dissertation](https://drum.lib.umd.edu/items/eb6edb82-8b0e-4566-bb69-72fca6e6eed2), [full PDF](https://drum.lib.umd.edu/bitstreams/bdff5925-5370-4b7a-914c-34b29a1f6b91/download).

Truman's arXiv math/0611210v1 supplies the same statements on pp.14 and 20–21, with Theorem 3.3. The archive submission is 2006-11-08, while the presently served v1 PDF prints an internal date August 2, 2018. The authenticated dissertation removes dependence on that date discrepancy. No journal version was authenticated and neither document was counted as an explicit Conjecture 12.26 solution. [arXiv record](https://arxiv.org/abs/math/0611210), DOI10.48550/arXiv.math/0611210.

Fan Ye's *Constrained knots in lens spaces*, AGT23(2023)1097–1166, DOI10.2140/agt.2023.23.1097, printed 1131/PDF37 Eq. 4, displays the boundary convention

\[
[\tau](X,e)=\left(\tau(X,e)+\frac{\Sigma_T}{t-1}\right)U_e(t),\qquad
U_e(t)=t^a\ \text{or}\ t^a\frac{t+1}{2},\quad
\Sigma_T=\sum_{h\in T}h.
\]

This occurs in a proof about lens-space knots, but introduces the formula for a 3-manifold with b1=1 and cites Turaev II.4; the preceding paragraph discusses any compact 3-manifold with torus boundary. It is used here as a torsion-definition quotation, not a noncyclic realization theorem. Half coefficients require care at 2. [Journal PDF](https://msp.org/agt/2023/23-3/agt-v23-n3-p03-p.pdf), [arXiv first submission2020-07-08](https://arxiv.org/abs/2007.04237).

### Explicit bridge to the proposed pair

This paragraph is the audit's mathematical inference from earlier displayed statements, not a claim that Truman or Ye explicitly wrote the conjecture refutation. Use the established primitive-exterior interface: a rank-one closed M has an exterior X with H1(X)=H1(M), ΔX=ΔM, and projected boundary torsion

\[
\rho\tau_X=\pm t^k\frac{\Delta_M}{t-1},\qquad
\rho:\mathbf Z[\mathbf Z\oplus T]\longrightarrow\mathbf Z[t^{\pm1}],\quad h\in T\mapsto1.
\]

The integral interface is supplied in the original counterexample and was additionally reported by the historical parent audit from Turaev 1986, printed 133, Theorem 1.6.1. This later audit did not independently download that1986 source. The projection kills each finite-group augmentation generator and sends I to (t−1).

Let p be odd, s=dimFp(T⊗Fp)≥1, and b=dimFpH1(X;Fp)=1+s. Truman's rank-one inclusion gives [τX] modp∈I^(s−1). Since p divides |T|, ρΣT=|T| vanishes modp. In the local ring Fp[t±1]_(t−1), Ye's Ue has value1 at1 and is a unit. Consequently

\[
\operatorname{ord}_1(\rho[\tau_X]\bmod p)
=\operatorname{ord}_1(\Delta_M\bmod p)-1\geq s-1,
\]

which is precisely ord1(ΔM modp)≥s. In particular, p=3, H=Z⊕(Z/3)^3 and Δ=t+25+t^-1 are excluded by this prior augmentation mechanism. No integral content was removed.

The normalization comparison relies on the printed general b1=1 clause and their cited Turaev polynomial part. Truman references II.3, whereas Ye references II.4. The actual monograph pages were inaccessible in this audit, so their precise section-level identification is a residual attribution gap. The formulas explicitly establish local equivalence for oddp; the half-normalized branch does not furnish an unqualified characteristic 2 proof. These limitations should travel with any claim that this is an exact literature reduction.

## Realization literature and distinctions

**Alcaraz 2014.** *The Alexander polynomial of closed 3-manifolds*, arXiv1406.2042v1 (2014-06-09; manuscript dated2014-04-15), characterizes polynomials realizable by some closed b1=1 manifold. It fixes b1 and Δ, not the full finite group. Theorem 2 proof pp9–10 gives A(M′)=A(M)⊕Λ/(λ). At b1=1, specialization gives T(M′)=T(M)⊕Z/|λ(1)|. Starting with S1×S2 therefore produces cyclic torsion. Printed pp15–17 already retain finite torsion in an integral square presentation and identify specialization at1; Lemma 3 gives the order formula. The nullity/divisibility observation is a short algebraic consequence of such prior machinery. Section5.3 pp18–19 uses Shalen–Wagreich mod-p cover-rank estimates for integral b1≥4 and Δ=1; it is not the prescribed rank-one finite-group theorem. No explicit Ohtsuki12.26 reference or candidate was found. [Primary PDF](https://arxiv.org/pdf/1406.2042v1), DOI10.48550/arXiv.1406.2042.

**Turaev's 2002 survey.** Printed301 realizes (H,λτ) from an already realizable refined (H,τ), for symmetric λ∈Z[H] of augmentation1. It is not arbitrary full-group ordinary-polynomial realization: τ retains finite-group variables, and a realizable base pair is required. Projection multiplies ordinary Δ by ρλ with augmentation1. A base with constant Δ=|T| only produces coefficients divisible by |T|, which misses the submitted primitive polynomial. The survey's examples allow symmetric augmentation-one λ for H=Z³, but any symmetric λ for H=Z²; a blanket augmentation-one description of the Z² example would be inaccurate. [Survey](https://arxiv.org/abs/math/0211084), Geom.Topol.Monogr4(2002)295–302; DOI10.48550/arXiv.math/0211084.

**Massuyeau 2010/2011.** The journal definition in §4.2 uses the ordinary maximal-free-cover integral Alexander order. Theorem 5.4, printed 87, gives closed rank-one torsion Δ/(t−1)^2. Printed89 explains the integral closed polynomial part by subtracting ΣT/((t−1)(t^-1−1)) from a symmetric representative. Theorem 6.5, printed 101–102, concerns integral b1≥3 and the cup determinant in augmentation degree b1−3. It cannot justify replacing integral b1 by mod-p rank; the later mod-r theorem is a separate ingredient. The survey points to Turaev for other cases. Its Ohtsuki bibliography entry concerns a 1996 finite-type-invariant paper, not Conjecture 12.26. [Journal](https://ambp.centre-mersenne.org/articles/10.5802/ambp.294/), DOI10.5802/ambp.294; [arXiv1003.2517](https://arxiv.org/abs/1003.2517).

**Suciu 2019/2022.** *Cohomology jump loci of3-manifolds*, §6.2 p18, is a genuine later source citing Alcaraz and describing polynomial/b1 realization; §6.3 discusses Alexander ideals and complex characteristic varieties. Its broad fixed-H sentence for H=Z omits the necessary augmentation±1 hypothesis, so it cannot be accepted literally as an arbitrary prescribed-pair theorem. The immediately following b1-only characterization is the relevant safe interpretation. No explicit candidate or Ohtsuki12.26 citation was found. [arXiv1901.01419](https://arxiv.org/abs/1901.01419), ManuscriptaMath167(2022)89–123, online2020-11-27; DOI10.1007/s00229-020-01264-5.

**Later Iwasawa/module comparisons.** Tateno–Ueki, JLMS111(2025)e70183, §§6–7 pp32–34, relates completed characteristic elements to Δ(1+T); its reduced Alexander formula treats link exteriors and multivariable covers, not arbitrary closed rank-one full-group realization. Kadokami–Mizusawa, KyushuJMath67(2013)215–226, Theorem 2.2 printed 218, gives λ≥r−1 from r link components and reduced-link divisibility. This r is not the finite-torsion p-rank of a closed rank-one manifold. Neither inspected source supplies the explicit conjecture refutation. [Tateno–Ueki arXiv2401.03258](https://arxiv.org/abs/2401.03258), DOI10.1112/jlms.70183; [Kadokami–Mizusawa journal](https://doi.org/10.2206/kyushujm.67.215), arXiv1204.4892.

Cyclic torsion cases are already acknowledged in the original conjecture remark. For cyclic p-primary torsion the proposed rank inequality gives only s=1; reciprocal augmentation-zero modp often already imposes vanishing at1, so cyclic realization supplies no evidence for noncyclic sufficiency.

## Access gaps and bounded status conclusion

Alcaraz's thesis was not obtained. BL EThOS 564280 authenticates title/author and lists2011; later bibliographies call it2012. The aggregate ORA UUID d89d46a3-03f0-4a71-a746-8f024f988f63 actually authenticates Jessica Banks's *The Kakimizu complex of a link* (2012). That file was rejected as an Alcaraz source. ORA search routes returned404/403, and EThOS metadata supplied no authenticated downloadable thesis. [Authenticated EThOS metadata](https://ethos.bl.uk/concern/thesis_or_dissertations/564280).

The official Turaev 2002 book record and chapter endpoints identify DOI10.1007/978-3-0348-7999-6, but requested chapter PDFs returned subscription HTML with no PDF signature. Chapters II/III and the precise rank-one augmentation/polynomial-part paragraphs were not read directly. Truman and Ye give checkable primary statements and references; those are not a substitute for falsely claiming book fulltext access. [Official book record](https://link.springer.com/book/10.1007/978-3-0348-7999-6).

Exact-number searches returned the original Ohtsuki problem-list mirrors and unrelated numbered conjectures. Broad realization, modular divisibility, Alexander-module, and Iwasawa searches produced the sources above, without an authenticated paper explicitly refuting Conjecture 12.26. This result is **application unlocated / priority unresolved**, not “already solved” and not “first counterexample.” A careful contribution claim must disclose that the obstruction has classical and mod-r antecedents, while separating those antecedents from the unlocated explicit application. Audit completion is 100% of this bounded literature assignment; discovery/priority certification is not 100%.
