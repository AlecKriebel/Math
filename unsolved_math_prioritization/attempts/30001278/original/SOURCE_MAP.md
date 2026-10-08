# Public sources and dependency map

Checked against retained documents and public pages on 2026-10-07. The eight retained PDFs were freshly retrieved from the public URLs in `SOURCE_METADATA.json`; all eight are byte-identical. The PDFs, extracts, screenshots, and dataset records are deliberately absent from this author packet.

## The actual question

Xavier Caruso, “Bounding Galois action on semi-stable representations,” in *Algebraische Zahlentheorie*, Oberwolfach Report 30/2009, pp. 1709–1712. [Publisher record](https://ems.press/journals/owr/articles/3480), [report PDF](https://ems.press/content/serial-article-files/46230?nt=1), [DOI](https://doi.org/10.4171/OWR/2009/30).

- Printed p. 1709 fixes a perfect residue field and the semistable setting.
- Printed p. 1710 defines the weights by the twists appearing in the Hodge–Tate decomposition; the cyclotomic character has weight +1 in this convention.
- Printed p. 1711, Theorem 2 and Conjecture 3, is the different inequality investigated here. Its final paragraph asks a separate question about further crystalline improvements.
- The catalogue's crystalline formulation is a valid restriction, but its literature explanation does not distinguish these questions. The catalogue status is a dated assertion, not evidence of today's global literature status.

The source's target page and the later theorem/proof pages were inspected visually as well as through text extraction, to check the exponents, strictness, and maximum.

## Imported general ramification input

Xavier Caruso and Tong Liu, *Some bounds for ramification of p^n-torsion semi-stable representations*, J. Algebra 325 (2011), 70–96. [Author manuscript](https://xavier.caruso.ovh/papers/publis/boundramif.pdf), [DOI](https://doi.org/10.1016/j.jalgebra.2010.10.005). Locations below use the manuscript's page numbers.

- pp. 1–2: the perfect-residue-field setup, Theorem 1.1, and the two separate parts of Conjecture 1.2.
- p. 6, Lemma 2.4.1: the rounded monomial annihilator used in Approach 3. Lemma 2.4.2 provides the scalar-polynomial upper bound.
- pp. 14–15: the general annihilator N, the strict finite-level condition, and the reduction to a finite free torsion representation.
- pp. 17–19: property (P_m), Proposition 4.2.1, Corollary 4.2.2, the relative-field argument, and different transitivity.

Approach 3 uses this established method with a valid smaller N. It is not a new integral comparison theorem. At the strict-level endpoint it uses Approach 1 instead; no strict source condition is weakened. For n=1, the target is already Theorem 1.1 itself.

Xavier Caruso, *Représentations galoisiennes p-adiques et (φ,τ)-modules*, Duke Math. J. 162 (2013), 2525–2607. [arXiv:1010.4846v3](https://arxiv.org/abs/1010.4846v3), [author manuscript](https://xavier.caruso.ovh/papers/publis/phitau.pdf), [DOI](https://doi.org/10.1215/00127094-2371976).

- The inspected manuscripts are dated September 2012; the arXiv revision is dated 1 October 2012. The [author's bibliography](https://xavier.caruso.ovh/papers/publis/galois.html) and arXiv record confirm the journal publication.
- p. 1 gives the general perfect-residue-field convention. The finite-extension-of-Q_p hypothesis in Theorem 3.5 belongs to the finite-height/potential-semistability result, not to the displayed statement of Theorem 3.28. This packet imports Theorem 3.28 as stated; it does not extend Theorem 3.5.
- pp. 48–49, Theorem 3.28 and its proof, explicitly establish Conjecture 1.2(1), the upper-break part. The proof identifies principal Witt ideals and a Galois-control condition; it also allows the use of Liu's (φ,G-hat)-module theory.
- The displayed theorem does not state Conjecture 1.2(2). Approach 2 records the precise additional relative estimate needed here and does not treat it as proved by quotation alone.
- The author's website cautions that its manuscripts may differ from the published versions. A retained publisher-page response was a bot-block page, not the journal PDF. We do not claim a byte comparison against the Duke journal PDF.

## Low-weight cases and the crystalline restriction

Shin Hattori, *On a ramification bound of torsion semi-stable representations over a local field*, J. Number Theory 129 (2009), 2474–2503. [arXiv:0801.2149v4](https://arxiv.org/abs/0801.2149v4).

The abstract and Theorem 1.1 concern r<p−1 with arbitrary e and n. For 1<r<p−1, its upper-break bound equals B in our notation, so it also proves the desired different bound. Its r=1 semistable upper-break bound has an extra p^(−n) over B; that displayed statement alone does not settle this endpoint. It must not be silently substituted for the desired different inequality.

Shin Hattori, *Integral p-adic Hodge theory and ramification of crystalline representations*, Panoramas et Synthèses 54 (2019), 159–203. [Final author manuscript, 9 May 2019](https://www.comm.tcu.ac.jp/shinh/RennesHodge/RennesHodge.pdf), [author bibliography](https://www.comm.tcu.ac.jp/shinh/).

Manuscript pp. 15–16, Theorem 2.18, states Fontaine's finite-flat bound d<e(n+1/(p−1)), and the preceding paragraph explains its application to crystalline lattices with weights in [0,1]. It is strictly stronger than our r=1 target, by 1−p^(−n)>0. Thus all crystalline r=1 cases are already covered by this classical input, even though the general semistable r=1 case is not obtained from Hattori's displayed upper-break bound alone. This is credited literature coverage, not a sixth authored approach. Theorem 2.19 and §3.6 give additional context for Fontaine–Laffaille and later developments. No unrestricted higher-weight conclusion is imported from this survey.

## Current inspected refinements

Pavel Čoupek, *Crystalline condition for A_inf-cohomology and ramification bounds*, Doc. Math. 31 (2026), 141–195. [Publisher record](https://ems.press/journals/dm/articles/14299210), [DOI](https://doi.org/10.4171/DM/1040). The publisher records online publication on 21 October 2025, with the 2026 journal volume. The abstract and §5 concern mod p cohomology of smooth proper formal schemes. They do not constitute a general mod p^n theorem for every crystalline lattice.

Pavel Čoupek, *Ramification bounds via Wach modules and q-crystalline cohomology*, Bull. London Math. Soc. 58 (2026), e70440. [arXiv:2410.23453v2](https://arxiv.org/abs/2410.23453v2), [DOI](https://doi.org/10.1112/blms.70440). The inspected revision is dated 26 May 2026. Theorem 1.1 covers mod p crystalline representations over absolutely unramified bases, with arbitrarily large weights. Its introduction distinguishes abstract crystalline and geometric representations. These hypotheses are not erased when comparing it with the present question.

This is a focused dependency and scope check. It is not an exhaustive classification of the literature, a proof of global openness, or evidence that every conjectural subcase left by our five arguments is still open.
