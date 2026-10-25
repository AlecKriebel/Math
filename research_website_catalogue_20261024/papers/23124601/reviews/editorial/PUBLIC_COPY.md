# Fixed-generator positive factorizations in Wajnryb's Artin A5 quotient

Alec Kriebel · Independent researcher · [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X)

3 October 2026 · Zenodo version 1.0 · [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

Unrefereed preprint, Zenodo version 1.0. Extensive AI assistance; no external human peer review or formal proof-assistant certification.

Manuscript and declared publication date: 3 October 2026. Zenodo records version 1.0; the manuscript prints no version number.

## Overview

A positive braid word is built from a fixed list of elementary crossings. This paper classifies all such words representing one specified element of Wajnryb’s quotient of the six-strand braid group.

There are two equivalence conventions. Strict Hurwitz moves rearrange adjacent factors while preserving their product. A broader equivalence also permits conjugating every factor by the same group element. The distinction changes the answer: four strict classes become three classes under the broader convention.

## Original abstract

We classify the positive words in the five standard generators of B₆/⟨⟨ch⁻¹⟩⟩ representing c², where c=(a₁a₂a₃a₄)⁵ and h=a₅a₄a₃a₂a₁²a₂a₃a₄a₅. Their lengths are 20, 30, 40, with respectively one, one, and two strict Hurwitz classes. Simultaneous conjugation identifies the two length-40 classes, giving the three representatives proposed in Wajnryb's question. The proof combines classical geometric and braid results with pure-braid linking constraints and an exhaustive, exact 810-word certificate for the length-20 case. The length spectrum and the twice-per-pair crossing theorem used at length 30 have prior sources; a reproducible six-strand certificate for the latter is supplied as additional evidence.

## The classification

Let a₁,…,a₅ be the five standard generators of B₆, and put c=(a₁a₂a₃a₄)⁵, h=a₅a₄a₃a₂a₁²a₂a₃a₄a₅ and z=(a₁a₂a₃a₄a₅)⁶. Work in G=B₆/⟨⟨ch⁻¹⟩⟩. The full-twist identity gives c²=h²=z in G, with z central.

For every literal positive word in these five fixed generators whose product in G is c², its length is 20, 30 or 40. At length 20 there is one strict Hurwitz class, represented by h². At length 30 there is one, represented by z. At length 40 there are exactly two, represented by (a₁a₂a₃a₄)¹⁰ and (a₂a₃a₄a₅)¹⁰.

The length-20 inputs are exactly the ten distinct cyclic rotations of h² as literal words. Simultaneous conjugation identifies the two length-40 classes, leaving exactly one class at each of the three lengths. This gives the three models in Wajnryb’s question under that broader equivalence.

A strict Hurwitz move replaces adjacent factors (x,y) by (xyx⁻¹,x), or applies its inverse. Intermediate tuples may contain conjugates of generators. The classified inputs remain literal positive words in the five fixed standard generators.

## Why the proof works

Classical chain relations map the quotient to the genus-two mapping class group with one boundary component. The positive boundary-twist length theorem bounds the word length by 40. Abelianization and signed pure-braid linking constraints then rule out lengths 0 and 10 and restrict the crossing patterns at the other three lengths. These constraints are necessary conditions, rather than complete braid invariants.

At length 20, the crossing pattern reduces all inputs to a finite walk problem. A quotient-compatible free-group action rejects the other candidates; centrality separately proves that the ten surviving rotations are genuine and strictly equivalent. At length 30, full free-word identities along every relevant edge of a finite crossing graph prove equality with the full twist. Equal crossing counts alone would not prove this.

At length 40, the noncrossing strand must be an endpoint. The classical four-chain embedding and positive braid relations give one class at each endpoint. Their generated subgroups have different permutation images, so strict moves keep them distinct; an explicit simultaneous conjugation merges them.

## Scope and prior work

The theorem concerns these five fixed standard-generator inputs in this specific six-strand quotient. It does not classify arbitrary products of conjugates of generators, arbitrary nonseparating Dehn-twist factorizations, other ranks or other quotients. Allowing conjugates in intermediate Hurwitz moves does not enlarge the input universe.

The quotient geometry, length spectrum, faithful Artin action, positive monoid embedding and chain embedding are classical inputs. Elrifai–Morton report Casson’s general twice-per-labelled-pair assertion; the note supplies an exact certificate in the required six-strand case. Historical priority of the complete fixed-input classification is not certified, and no current worldwide-open-problem claim is made.

The finite proof depends on complete candidate coverage and literal free-word equalities, together with the stated classical theorems. Equal crossing counts alone do not establish braid equality.

## References and credit

[B. Wajnryb, Relations in the mapping class group (2006), Chapter 8](https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf#page=129). The source of the fixed-positive-word quotient question and the stated Perron–Vannier regular-neighborhood chain embedding theorem.

[D. Auroux, Mapping class group factorizations and symplectic 4-manifolds: some open problems (2006), Chapter 9](https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf#page=138). Distinguishes strict Hurwitz moves from simultaneous global conjugation.

[R. I. Baykur, N. Monden and J. Van Horn-Morris, Positive factorizations of mapping classes (2017)](https://doi.org/10.2140/agt.2017.17.1527). Theorem A supplies the classical maximum length 40 for a positive nonseparating factorization of the genus-two, one-boundary twist.

[J. González-Meneses, Basic results on braid groups (2011)](https://www.numdam.org/article/AMBP_2011__18_1_15_0.pdf). The faithful Artin free-group representation and positive braid monoid embedding are established tools used by the proof.

[M. Matsumoto, A presentation of mapping class groups in terms of Artin groups and geometric monodromy of singularities (2000)](https://doi.org/10.1007/s002080050336). Credits the classical genus-two quotient presentation. The original 1997 institutional manuscript is also cited in the paper.

[Y. Sato, 2-Spheres of Square −1 and the Geography of Genus-2 Lefschetz Fibrations (2008)](https://www.ms.u-tokyo.ac.jp/journal/pdf/jms150403.pdf). The earlier geography result already gives the length spectrum 20, 30, 40 in the corresponding square−1-section, no-reducible-fibre setting.

[E. A. Elrifai and H. R. Morton, Algorithms for positive braids (1994)](https://doi.org/10.1093/qmath/45.4.479). Reports Casson’s general crossing assertion on page 496, without a proof or separate Casson reference. The six-strand certificate is additional evidence for that known assertion.

## AI and review status

AI tools were used extensively in research, proof development, code, literature work and writing. This is an unrefereed preprint without external human peer review or formal proof-assistant certification; the named author is responsible for the work.

## Collaboration

Substantive proof checks, counterexamples and precise comparisons with prior work are welcome. Authorship and acknowledgments would reflect actual research contributions and mutual agreement. Citations credit prior work and imply no participation or endorsement.

## Read the paper and source

Read the complete 6-page deposited paper in the on-page PDF reader.

[Open PDF](/research/fixed-generator-artin-a5/fixed_generator_classification.pdf)

[Download PDF](/research/fixed-generator-artin-a5/fixed_generator_classification.pdf)

[Download original PDF from Zenodo](https://zenodo.org/api/records/23124601/files/fixed_generator_classification.pdf/content)

[Download complete ZIP](/research/fixed-generator-artin-a5/wajnryb-artin-a5-verification.zip)

[Download original complete ZIP from Zenodo](https://zenodo.org/api/records/23124601/files/wajnryb-artin-a5-verification.zip/content)

[Download BibTeX](/research/fixed-generator-artin-a5/citation.bib)

## Citation

Alec Kriebel (2026). Fixed-generator positive factorizations in Wajnryb's Artin A5 quotient. Zenodo version 1.0, 3 October 2026. https://doi.org/10.5281/zenodo.23124601.

```bibtex
@misc{Kriebel2026FixedGeneratorArtinA5,
  author = {Kriebel, Alec},
  title = {Fixed-generator positive factorizations in Wajnryb's Artin A5 quotient},
  year = {2026},
  month = {oct},
  day = {3},
  date = {2026-10-03},
  version = {1.0},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.23124601},
  url = {https://zenodo.org/records/23124601},
  note = {Unrefereed preprint; extensive AI assistance; no external human peer review or formal proof-assistant certification},
  orcid = {0009-0001-9320-500X}
}
```
