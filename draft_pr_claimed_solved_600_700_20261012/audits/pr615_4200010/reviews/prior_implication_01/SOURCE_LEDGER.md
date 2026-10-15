# Independently authenticated primary-source ledger

Accessed 12 October 2026, America/Los_Angeles. Full third-party downloads and rendered source pages remain solely in `sources.private/`. No author or other individual was contacted.

| Source | Primary location | Exact inspected passage | Evidence used |
|---|---|---|---|
| Hirotada Anzai, *Ergodic skew product transformations on the torus*, Osaka Mathematical Journal **3**(1) (March 1951), 83–99 | [Osaka institutional record](https://ir.library.osaka-u.ac.jp/repo/ouka/all/11966/), [version-of-record PDF](https://ir.library.osaka-u.ac.jp/repo/ouka/all/11966/omj03_01_08.pdf), [DOI](https://doi.org/10.18910/11966) | §6, Theorem 6 and corollary, printed pp91–92; PDF pages10–11 in this download | The map T_m(x,y)=(x+γ,y+mx), with γ irrational and m≠0, is ergodic and its Koopman operator on the orthocomplement of x-only functions has continuous spectrum. Formula (39) gives the exact Fourier-index shift. It is the same map at m=1 used in the PR, rather than a merely analogous skew product. |
| Manuel de León and Martín Saralegi, *Cosymplectic reduction for singular momentum maps*, Journal of Physics A: Mathematical and General **26** (1993), 5033–5043 | [Full article hosted in author's article collection](https://www.mesa-lml.fr/Articulos/Cosymplectic.pdf), [de León publication list](https://www.manueldeleon.es/publications/papers/), [DOI](https://doi.org/10.1088/0305-4470/26/19/032) | Lemma3.2, printed p5036; extension and Eq.(3.3), p5037; §6.1 and Eq.(6.3), p5042. PDF pages5,6,11 in this download | The exact form pr*Ω+pr*η∧ds is symplectic iff the input pair is cosymplectic. The Hamiltonian h(x)+s realizes the evolution field; at h=0 it realizes the Reeb field itself. The p5037 remark supplies an S¹ thickening with its length form. This remark is used only for symplectic geometry; it is not used to pretend a circle coordinate is globally real Hamiltonian. |
| Oliver Knill, *Some intriguing open problems in Hamiltonian dynamics*, talk of 19 October 2000, item10 | [Author's problem-list HTML](https://people.math.harvard.edu/~knill/seminars/intr/), [author's two-page PDF](https://people.math.harvard.edu/~knill/seminars/bozeman/intr-l.pdf) | HTML item10, PDF page2 | Exact unrestricted positive-measure ugly-set question. No compactness, finite ambient volume, Euclidean, analytic, mechanical, or weak-mixing hypothesis is printed as a condition of the existence question. Weak mixing appears in the separately marked guess. |

The formulas and spectral statements were checked against full rendered primary pages, not only search snippets. In Anzai Theorem6 the relevant subspace is H_0^perp, which PDF extraction can misread as H_0. The de León–Saralegi plus sign in Ω+η∧ds and contraction convention were visually checked. The 1993 paper's received and final-form dates on its first printed page are 11 January and 8 June 1993.

## Download fingerprints

- `sources.private/anzai1951.pdf`: 1,557,995 bytes; SHA-256 `738ade609fd24342fad59f0111eb43029a41b4119b92e3a458ed64a5b6169e91`.
- `sources.private/deleon_saralegi1993.pdf`: 957,467 bytes; SHA-256 `25469746eb0ead7d1f5377da273efba8cbd1d9ca1518738a6390863e2f7b84e6`.
- Local direct retrieval of Knill's HTML returned HTTP403; the author's page and PDF were accessible through the web-reading tool. No fabricated local fingerprint is supplied for that HTML.
- Local primary PDFs were fetched directly from the URLs above. The web tool timed out on the de León–Saralegi full PDF, so the complete locally fetched source was extracted and rendered for inspection.

## Bibliographic boundary

These sources predate the target by 49 and 7 years. Their exact mechanisms, together with the explicit deductions in PROOF.md, settle the unrestricted mathematical existence assertion. This ledger contains **no located earlier article explicitly answering Knill's 2000 item10**, and does not attribute that later question's resolution in words to Anzai or to de León–Saralegi. An explicit historical-resolution claim is not interchangeable with a rigorously verified prior-theorem implication.
