# Source and version map

The public source status below is the checked snapshot of **14 October 2026 UTC**. The preserved [source and scope report](sources/SOURCE_SCOPE_REPORT.md) supplies bibliographic adjudication, access history, and target matching. Its [provenance manifest](sources/PUBLIC_PROVENANCE_MANIFEST.json) supplies the full retrieval, inspection, byte-count, hash, and public-dataset match record. Neither source-only file claims to certify proofs; the authored reconstructions and geometric audits provide that separate verification.

## Target source

Zuzana Patáková, joint with Martin Tancer and Uli Wagner, “Barycentric cuts through a convex body,” in *Discrete Geometry*, *Oberwolfach Reports* 17 (2020), report 30/2020, printed pp. 1502–1503. The question is Q2 on printed p. 1502, PDF p. 34, with n ≥ 3 inherited from Q1. The report's [official metadata](https://ems.press/journals/owr/articles/1703876) gives publication on 2 July 2021; the report year is 2020. [Official PDF](https://ems.press/content/serial-article-files/46867?nt=1): 1,132,713 bytes; SHA-256 d31cd6e3ea36121d8df90be869501956bc3827eba7b4ae2a646d84d810dc09fb. Pages 34–35 were inspected in text and visually.

## Sufficient published prior result

Sergii Myroshnychenko, Kateryna Tatarko, and Vladyslav Yaskin, [*Answers to questions of Grünbaum and Loewner*](https://doi.org/10.1016/j.aim.2024.110081), *Advances in Mathematics* 461 (2025), 110081.

- Direct proof source: [arXiv:2404.15188v2](https://arxiv.org/abs/2404.15188v2), 7 November 2024, [versioned PDF](https://arxiv.org/pdf/2404.15188v2), 10 pages, 167,961 bytes.
- SHA-256: 970f4af59ffb9cd4d24530b8614c57b4391a269efa966100665dfe9e2fda9b46.
- Theorem 3: p. 4; main construction: pp. 5–8; transform conventions: pp. 2–3. The reconstruction inspected all ten pages in extracted text and visually checked the key mathematical pages 3 and 5–8. The independent audit visually checked pages 3, 5, 6, 7, and 8.
- Publication identity: corroborated by the [publisher record](https://www.sciencedirect.com/science/article/pii/S0001870824005978), [publisher-deposited Crossref metadata](https://api.crossref.org/works/10.1016/j.aim.2024.110081), and institutional author lists.
- Journal proof bytes: **unrecovered and uninspected**. No publisher PDF hash or byte-equivalence claim exists. The two repairs in this reader are explicitly about inspected author v2 only.

The reconstruction makes dimension five fully explicit; this is sufficient even without auditing every higher dimension. The separate geometry audit also checks the n ≥ 5 construction.

## Credited precursor used for comparison

Vladyslav Yaskin, *On strict inclusions in hierarchies of convex bodies*, *Proceedings of the American Mathematical Society* 136 (2008), 3281–3291, [DOI 10.1090/S0002-9939-08-09424-0](https://doi.org/10.1090/S0002-9939-08-09424-0).

The inspected [author-hosted PDF](https://www.math.ualberta.ca/~vladyaskin/papers/inclusions.pdf) has 10 pages, 201,198 bytes, SHA-256 76537d725c0ecdc407f0aa6a2c60a2e9621cd174aa7c301efef11780ec4a4291. Pages 2–4 were inspected for Theorem 2.2 and Lemmas 2.3–2.5; p. 3 supplies a check on radial Fourier constants. The reconstruction independently proves the seed properties it needs. This author-hosted file is not claimed to equal publisher bytes.

## Supplementary submitted preprint

Shouda Wang, Ge Xiong, and Kaiwen Yang, [*A complete solution to the Grünbaum–Loewner centroid problems*](https://arxiv.org/abs/2606.19865v2), arXiv:2606.19865v2, 31 July 2026.

- [Versioned PDF](https://arxiv.org/pdf/2606.19865v2): 18 pages, 407,327 bytes.
- SHA-256: 21e91319797e8d4b5ececf4d4d8c4c4cc1814bd47422edeb9a3e3ffdfff8b53e.
- Main claim: Theorem 1.1, p. 2. All 18 pages were read through extracted text; pages 9 and 14–17 were additionally visually inspected in the reconstruction. The independent geometry audit visually inspected pages 4 and 14–17.
- The three-author v2 attribution is essential. The source report records that its arXiv comments credit independent simultaneous work by Wang and by Xiong–Yang.
- [Wang's public author page](https://wsdustcx.github.io/My-website/) labels the work submitted; the checked arXiv record gives no journal reference. No journal-publication claim is made here.
- The standard harmonic-analysis prerequisites are listed in the reconstruction; Rubin's 1999 original article and all cited references were not inspected in full.

This supplement covers every n ≥ 3, including n = 3 and n = 4. It is logically unnecessary to the sufficient published MTY negative answer.

## Broader scope sources and bounded negative checks

The preserved report also checks Grünbaum's 1961 original question, the Patáková–Tancer–Wagner SoCG 2020 result concerning maximal Tukey depth, the March 2020 author manuscript, the June 2026 Huang–Myroshnychenko–Tatarko–Yaskin manuscript, and Haddad–Jiménez–Villa's 2026 publication. Exact titles, public URLs, sizes, and hashes are in the provenance manifest. Those materials help distinguish targets and dates; they are not substituted for the sufficient construction proof.

No relevant later version, correction, withdrawal, or status change was found in the bounded source refresh. This is not an exhaustive absence guarantee. Older or later-published statements of openness in dimensions three and four do not by themselves refute the July 2026 submitted manuscript. The separate arbitrary-interior-point question is not disposed of by the centroid counterexample.
