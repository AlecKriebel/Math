# Independent source and priority disposition — PR810 / problem2307042

Audit date: 12 October 2026 PDT (13 October 2026 UTC). Reviewer role: source scope and historical priority, independent of the mathematical review. Frozen author proof and source-status packet were read first; existing reviewer conclusions were not consulted. The draft note was inspected only after the primary-source interpretation and main literature findings were established.

## Disposition

**The source supports the claimed negative answer to the equality-along-a-Green-line extension. No verified direct prior resolution, and no immediate prior-theorem implication of this fixed-kernel local-isolation result, was established in the inspected primary literature. Historical first priority remains unresolved.** Publication of the explicit theorem as a research note is supportable with the stated limited target and no first-resolution/current-worldwide-openness claim. The absence of an identified earlier result is not affirmative evidence of novelty.

I found no source-target defect requiring withdrawal of the claimed counterexample. I found repairable bibliography and inspection-scope issues, listed below. This report does not replace the separate proof audit.

## Exact target and what the result answers

The full arXiv:1809.07200v2 source was retrieved. Original printed pp.173–174 were read in extracted text and rendered pages. Problem 7.42 defines the normalized positive-harmonic envelope, then describes equality of a fixed disc Poisson kernel with it on the radius to the kernel's pole. It transfers that property to Green lines in simply connected domains and asks about multiply connected domains. The subsequent editorial update records no reported progress as of that edition. The duplicated phrase and inconsistent displayed symbols are real source defects; the prose definition and disc example determine the intended normalized envelope without exploiting those defects. [Hayman–Lingham, 2018, Problem/Update 7.42](https://arxiv.org/pdf/1809.07200v2).

For clarity, the proposed extension used by the candidate has quantifiers

\[
\forall D,a,\xi\quad\exists\text{ nontrivial Green line }\gamma\text{ issuing from }a:
\quad K_\xi(z)=H_a(z)\ \text{along }\gamma.
\]

Even its initial-segment version requires distinct equality points approaching the base. The candidate instead provides one annulus, base, and minimal Martin point with

\[
\exists U\ni a\quad \forall z\in U\setminus\{a\},\quad K_\xi(z)<H_a(z).
\]

This is a direct logical negation of the initial-segment requirement and hence of the full equality-along-line extension. The implication does not depend on identifying which Green line terminates at the kernel's pole. It excludes every continuous nontrivial equality curve that approaches the base.

The phrase about touching along a line is not given a separate technical definition. The disc equality example strongly supports the paper's interpretation; it is appropriate to state that interpretation explicitly. A weaker question asking only for one remote contact somewhere on some Green line is not settled by the local theorem. It should neither be silently substituted for the source's disc-property extension nor be claimed solved by this proof. The frozen proof and current draft note both acknowledge the remote-contact limitation.

The 2019 Springer book and chapter records are subscription previews; the complete later Problem 7.42 text was not inspected. The publisher's supplemental file, headed *List of known updates: January 2021*, was retrieved from its official extras archive and read in full; it contains no entry for 7.42. This is a bounded editorial-update check, not proof of ongoing openness. The exact question claim must therefore remain tied to the 2018 version. [Official extras archive](https://extras.springer.com/?query=978-3-030-25164-2). The external problem-index page was inaccessible; its live contents/status were not inferred. [2019 chapter record](https://link.springer.com/chapter/10.1007/978-3-030-25165-9_7).

## Primary-literature assessment

| Source and inspected scope | Supported result and its bearing on priority |
| --- | --- |
| D.A. Herron, *The Harnack and other conformally invariant metrics*, Kodai Math. J. 10 (1987), 9–19. Full publisher PDF; key formulas visually checked. [PDF](https://www.jstage.jst.go.jp/article/kodaimath1978/10/1/10_1_9/_pdf/-char/en), DOI 10.2996/kmj/1138037356. | Theorem 1 concerns supremal logarithmic gradient norm. Theorem 4 expresses symmetric Harnack distance using extrema of a Poisson-kernel ratio. Theorem 5 computes distance between antipodal points on the annulus's core circle. These provide the right extremal framework, but do not state that the prescribed antipodal boundary kernel has interior gradient or isolated contact. The two kinds of antipodal points must not be conflated. |
| H.S. Bear and W. Smith, *A tale of two conformally invariant metrics*. Full 8-page author manuscript dated 23 May 2005, plus publisher metadata for J. Math. Anal. Appl. 318 (2006), 498–506, DOI 10.1016/j.jmaa.2005.05.065. [Author PDF](https://math.hawaii.edu/~wayne/mathpapers/harnack.pdf), [publisher record](https://www.sciencedirect.com/science/article/pii/S0022247X05005251). | Theorems 1.1/3.3 characterize equality of Harnack and hyperbolic distances; punctured discs are the nonsimply-connected exception. Section 2.4 discusses normalized cone extrema. No fixed-kernel contact locus or Green-line statement was found. A full author manuscript is now available for inspection; the old packet's abstract-only limitation can be replaced with this precise scope. It should not claim full typeset-text equivalence. |
| Bear–Smith, *An Extension of the Schwarz–Pick Lemma*. Full 10-page author manuscript with provisional journal fields. [PDF](https://math.hawaii.edu/~wayne/mathpapers/Harnack2.pdf). | Theorem 4.5 and Corollary 4.6 give the same general equality-rigidity theme. The file is a distinct manuscript/version, not a final publication citation. It does not prove or disprove the normalized fixed-kernel curve property. |
| J. Köhn, *Die Harnacksche Metrik in der Theorie der harmonischen Funktionen*, Math. Z. 91 (1966), 50–64. All 15 original pages retrieved from public GDZ scans and read through OCR; key pages checked visually. [Publisher metadata](https://link.springer.com/article/10.1007/BF01113851), [GDZ article locator](https://gdz.sub.uni-goettingen.de/dms/resolveppn/?PPN=GDZPPN002396882). | Lemma 1.1, pp.52; minimal-cone extreme-value reduction, pp.57–58; and §§4.2–4.3, pp.62–64 establish the metric framework and a punctured-disc example. The statement that extrema are attained by minimal functions is existential for each pair of points, not universal for each prescribed minimal function. No annular fixed-kernel local-isolation result was found. |
| H. Leutwiler, *On a distance invariant under Möbius transformations in R^n*, Ann. Acad. Sci. Fenn. Ser. A I Math. 12 (1987), 3–17. Full publisher PDF and its sections read. [PDF](https://www.acadsci.fi/mathematica/Vol12/vol12pp003-017.pdf), DOI 10.5186/aasfm.1987.1219. | Section 3 defines a one-sided logarithmic envelope; §5 symmetrizes it by a maximum; §6 ends with a directional differential metric and open structural questions. This is particularly relevant to the candidate's local-gradient mechanism. The paper does not establish the chosen kernel's gradient interiorness or a counterexample to the Green-line property. |
| H. Shiga, *Conformal invariants defined by harmonic functions on Riemann surfaces*, J. Math. Soc. Japan 68 (2016), 441–458. Full 18-page publisher PDF read. [PDF](https://www.jstage.jst.go.jp/article/jmath/68/1/68_441/_pdf/-char/en), DOI 10.2969/jmsj/06810441. | Theorems 3.2/3.4 characterize equality with hyperbolic distance/density. Proposition 5.1, p.455, formulates Harnack distance in terms of normalized Martin kernels. The annulus result for bounded-harmonic invariants in §3 concerns a different function class. None gives the candidate's fixed-kernel equality-curve conclusion. This primary source is a material addition to the old audit. |
| D.H. Armitage, *The Poisson kernel as an extremal function*, IMS Bulletin 32 (1994), 19–31. Public scanned PDF; §§1–2 and bibliography inspected, full OCR text screened. [PDF](https://www.maths.tcd.ie/pub/ims/bull32/bull32_19-31.pdf). | The disc/ball extremality and its gradient equality cases are classical. Section 2.3 cites Goldstein–Kuran (1988) for derivative inequalities on the unit ball. This survey does not establish a multiply-connected fixed-kernel curve property. It supports attribution of classical ingredients, not priority for the annular construction. |
| R. Kargar, *On Harnack inequality and harmonic Schwarz lemma*, arXiv:2312.15232v3 (2024). Full 14-page primary manuscript retrieved; definitions, results, metric section, and bibliography inspected. [arXiv](https://arxiv.org/abs/2312.15232v3). | Its Harnack-function class satisfies local inequalities and is different from Problem 7.42's particular envelope. Its metric/distortion and harmonic Schwarz results do not give the annular contact theorem. The primary bibliography leads to Shiga and Herron–Minda, which were followed. |
| M. Svetlik, *A strengthening of the Harnack inequality*, arXiv:2501.09880v1 (2025); publisher record identifies Indagationes Math. 37 (2026), 639–645, DOI 10.1016/j.indag.2025.06.004. Full 6-page primary manuscript read. [arXiv](https://arxiv.org/abs/2501.09880), [publisher record](https://www.sciencedirect.com/science/article/pii/S0019357725000643). | Theorem 1 refines the unit-disc inequality using the base-point gradient. It is recent relevant gradient literature, but it does not treat an annulus or fixed Martin kernel versus the domain's own normalized envelope. It supplies no identified earlier resolution. |

## Sources not inspected in full

Arsove–Johnson's *A conformal mapping technique for infinitely connected regions*, Memoirs AMS 91 (1970), DOI 10.1090/memo/0091, is directly relevant to Green-line conventions. Its 1964 AMS preliminary-report abstract (Notices, printed p.569, abstract 614-1390) describes slit-disc Green mappings, radial limits, harmonic/Green measure, and Poisson counterparts. That abstract does not state the fixed-kernel extremal property or its negation. The full memoir returned 403, so a complete priority exclusion based on it is unavailable. Their 1977 Green-line/H^p preliminary-report listing was also located; full report text was not inspected. [Official 1964 abstract source](https://www.ams.org/journals/notices/196408/196408FullIssue.pdf), [memoir DOI](https://doi.org/10.1090/memo/0091).

Other located gaps: H. Tanaka, *On Harnack's pseudo-distance* (1977), DOI 10.14492/hokmj/1381758535; D. Herron and D. Minda, *Comparing invariant distances and conformal metrics on Riemann surfaces* (2001), DOI 10.1007/BF02809900; H.S. Bear, *Part Metric and Hyperbolic Metric* (1991), DOI 10.1080/00029890.1991.11995712; M. Goldstein and Ü. Kuran's 1988 paper, DOI 10.1080/17476938808814277. Metadata/abstracts or primary citations were checked, and ordinary full-text retrieval attempted. No conclusions about everything in those inaccessible texts are justified. Shiga's fully inspected paper provides explicit alternative proofs of the Herron–Minda equality results, but that is not inspection of the earlier full paper. [Herron–Minda publisher abstract](https://link.springer.com/article/10.1007/BF02809900).

## Why the checked prior theorems do not immediately settle the candidate

Put

\[
A_D(a,z)=\sup_{h>0}\log\frac{h(z)}{h(a)}=\log H_a(z).
\]

The symmetric Harnack metric is

\[
d_H(a,z)=\max\{A_D(a,z),A_D(z,a)\}.
\]

Strict inequality between this metric and the hyperbolic metric does not say which prescribed kernel realizes either one-sided supremum, nor whether it has contact on a Green trajectory. Similarly, a supremal gradient *norm* does not decide whether a particular kernel's gradient is a directional supporting point of the whole gradient set.

The candidate's checkable mechanism is instead to compute the selected annular boundary kernel's gradient and place it strictly inside the convex hull of four explicit admissible competitors. A common Taylor remainder then rules out contact in every local direction. The inspected prior sources provide standard tools or other equality characterizations; none supplies that interiorness conclusion for the selected kernel without the candidate's additional calculation. This is why I have not classified the result as an immediate consequence of a verified earlier theorem.

## Repairs recommended before the package is final

1. Update the dated source-status / audit record with the newly inspected final-title Bear–Smith author manuscript, Shiga, Köhn, and Leutwiler, keeping manuscript versus typeset-publication distinctions exact.
2. Add at least Shiga to the paper bibliography and explain that its Martin-kernel metric formula and metric-equality results are related background. Köhn/Leutwiler may be in the dated audit only to keep the note concise.
3. Keep the explicit equality-along-the-line interpretation and the remote-contact limitation in the abstract/introduction and metadata. The current draft note does this adequately. Do not describe absence of contact everywhere in the annulus.
4. Retain the current explicit statement that the note does not claim first historical resolution or certified current worldwide openness. Do not convert the editorial 2018 update into a 2026 openness claim.
5. Exclude `private_sources/` (downloaded papers, OCR, images, HTML) and `tanaka_crossref_metadata.json` from intended public selections. Only authored summaries / bibliographic locators and chosen retrieval hash metadata should be released.

No external communication was undertaken or prepared. No Git/ref changes or shared-file mutations were made by this audit.
