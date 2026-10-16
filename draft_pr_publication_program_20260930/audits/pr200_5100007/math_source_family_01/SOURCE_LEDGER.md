# Primary source and dependency ledger

Retrieved/inspected 2026-10-16 UTC. Downloaded papers are private reading copies excluded from the safe manifest. Page images were visually inspected, then only this auditor's three regenerable images were removed to conserve full shared-disk space. Source PDFs/text/receipts remain private.

## Original target and distinct editions

[arXiv:2004.12497v11](https://arxiv.org/abs/2004.12497v11), 29 October 2020, by Reznik, Garcia, Koiller. Metadata title: *Eighty New Invariants of N-Periodics in the Elliptic Billiard*; PDF front title: *Eighty New Invariants in the Elliptic Billiard*. This is a 17-page PDF. Table 2 printed p.5, row k115, and Figure 1's prime convention were inspected before the candidate. The row is the outer-tangent-vertex one-focus distance product for N=0 mod4, value/proof status question marks. The Introduction explicitly fixes a pair of confocal ellipses. The definition/table does not expressly require least period; the necessary primitive refinement is analyzed exactly in DERIVATIONS.md.

The journal version is *Fifty New Invariants of N-Periodics in the Elliptic Billiard*, Arnold Mathematical Journal 7 (2021), 341-355, [DOI 10.1007/s40598-021-00174-y](https://doi.org/10.1007/s40598-021-00174-y). Its complete [journal-hosted version of record](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf) was independently obtained. The PDF records acceptance 4 January 2021 and online publication 18 February 2021. This distinct edition has 15 pages. Table 2 printed p.345 was rendered and visually inspected: k115 retains the identical product, parity and question-mark proof status. Equality was checked directly, not inferred from metadata/DOI similarity.

Nearby labels differ: arXiv k111=A'A'' (even N), k112=A'A''/A^2 (odd N), k113=A'/A'', k121=sum d1,i. Journal k111 is the odd ratio, k112 is A'/A'', k113 is the even focal-distance sum. The journal cluster has 20 rows; v11 has 21. Thus general labels must not be translated by assumption. The dataset background mixes the Eighty title and 2021; reproducible attribution should distinguish v11 (2020) from journal Fifty (2021). Old question marks establish status only in those editions, not present-day novelty.

## Canonical theorem: exact scope and conventions

Hellmuth Stachel, *On the motion of billiards in ellipses*, European Journal of Mathematics 8 (2022), 1602-1622, [DOI 10.1007/s40879-021-00524-2](https://doi.org/10.1007/s40879-021-00524-2). The full [university repository version of record](https://repositum.tuwien.at/bitstream/20.500.12708/136087/1/Stachel-2022-European%20Journal%20of%20Applied%20Mathematics-vor.pdf) was obtained; printed pp.1613-1614 were visually inspected. The filename includes Applied, but the printed journal heading is European Journal of Mathematics.

Published Theorem 4.3/(4.9) and [author preprint arXiv:2105.03624v2](https://arxiv.org/abs/2105.03624v2), Theorem 2/(4.10), were literally checked. They provide an elliptical caustic, arbitrary initial phase, P=(-ae sn u,be cn u), step 2 Delta-u, modulus m=d/ac, and coprime turning number tau with Delta-u=2 tau K/N. The axes are ae=ac dn(Delta-u)/cn(Delta-u), be=bc/cn(Delta-u). They allow every coprime tau, not only tau=1. No hyperbolic extension is supplied. Candidate mapping: alpha=ac, beta=bc, c=d, v=Delta-u, k=Stachel's modulus m. Software parameter is k^2; the candidate's half-count m=N/2 is a separate symbol.

Source error: both preprint p.10 and published p.1613 incorrectly display dn(u+2rK)=(-1)^r dn(u). The correct real shift leaves dn unchanged. The published typo was confirmed in its page image. The candidate uses the correct DLMF identity; a source note should identify BOTH editions as affected.

## Jacobi facts literally checked

[DLMF 22.4](https://dlmf.nist.gov/22.4), version 1.2.8 (2026-09-15): Tables 22.4.1/22.4.2 locate sn poles and dn zeros and unsquared periods. Squaring gives lattice 2K Z+2iK' Z, whereas the real geometric period of P,Q is 4K. Table 22.4.3 gives sn(z+K+iK')=dn(z)/(k cn(z)), sn(z+2K)=-sn(z), cn(z+2K)=-cn(z), dn(z+2K)=dn(z), and dn(z+2iK')=-dn(z). These substantiate the quarter-shift divisor calculation and correct the Stachel typo.

[DLMF 22.8](https://dlmf.nist.gov/22.8), equations 22.8.1-22.8.3, supplies sn/cn/dn addition identities; equal arguments yield the double-angle formulas. [DLMF 22.13 Table 22.13.1](https://dlmf.nist.gov/22.13#T1) supplies dn'=-k^2 sn cn, giving a simple dn zero at K+iK' for 0<k<1. Compact-torus holomorphic constancy and the identity theorem are standard complex-analysis inputs, applied after full divisor cancellation rather than by assuming equal zero/pole counts suffice.

## Method references versus dependencies

Akopyan, Schwartz, Tabachnikov, [*Billiards in ellipses revisited*](https://arxiv.org/abs/2001.02934): complete 12-page primary arXiv PDF inspected via arXiv service, particularly Sections 4-5 and Theorems 5-6. Its complexified Poncelet angle sums/products are shown bounded by singularity cancellation before complex constancy is applied. This supports method credit; it is not assumed as a black-box k115 theorem here. No novelty inference is made. PR149 is a strategy-credit reference only; this auditor did not read its proof/reviews, and this argument requires no theorem from it.

## Custody and independence

Instructed frozen original HEAD: 379a959609958f1e28f68f1ab6e42970ca9d1641. No local Git query was performed. PROOF.md and SOURCES.md were read only after SOURCE_FIRST_FREEZE.md was saved. No independent_review or prior_imported_report file was opened. A later source_record.json read for its target statement unexpectedly exposed its trailing old research_summary; this is logged and not used as math or priority evidence. Other families' authored work/root mathematics were not read. Shared mpmath 1.3.0 / SymPy 1.14.0 runtime packages only were imported from the algebra family's runtime_packages folder at root direction, without importing its authored code/reports. check_quantifiers.py is independently authored.

## Hashes of exact witnesses

- `primary_source_private/reznik_garcia_koiller_2004.12497v11.pdf` SHA256 `c56bb4ea29734ed04ee153206bb8619286df544714fd3f77fe97bdc945dfe1da`.
- `primary_source_private/reznik_garcia_koiller_2004.12497v11.txt` SHA256 `e18769d6597539248eddbe0e4de687aa56270b92a390d3f85addb0ddd3cb2131`.
- `original_submitted_head/PROOF.md` SHA256 `5d31111bf167822783d32aabb1e0bf2766bb372b3a5359739d9c157f8faab030`.
- `original_submitted_head/SOURCES.md` SHA256 `95be0bd49231a33db45f785deb557fca49154df46eeb6c8e08bca26d2a6fc5b7`.
- `original_submitted_head/source_record.json` SHA256 `b77ba89c72b2ba230dcfd9f1bfc5b8c8039af70e79ac1bddb651636e0a6b090a`.
- Private independent download `journal_reznik.pdf`: 1836579 bytes, SHA256 `c2a2e644521fd03a15833a23bd57c2498b5644036f6bc8fe682c40581f640d42`, UTC `2026-10-16T04:14:36.137547+00:00`.
- Private independent download `stachel_preprint_v2.pdf`: 308878 bytes, SHA256 `e221864a4cad786c38d65f9e2e6ffa03ab8ff8985e22a87e9cc3e46e3096cfd2`, UTC `2026-10-16T04:14:36.329868+00:00`.
- Private independent download `stachel_published.pdf`: 726042 bytes, SHA256 `9121028d7295435740cebb25ec60abe1a0dcc4e96686c226b1b6533bd49515d8`, UTC `2026-10-16T04:14:39.533851+00:00`.
