# Sources and version boundaries

This package gives authored mathematical arguments and public bibliographic metadata. It does not redistribute the cited documents or their extracted text. Retrieval and visual-inspection metadata, byte counts, and SHA-256 identities are in [the source manifest](sources/SOURCE_MANIFEST.json). The source-status date is 15 October 2026.

## Original question and classical exact formula

1. P. Erdős and R. L. Graham, *Old and new problems and results in combinatorial number theory: van der Waerden's theorem and related topics*, L’Enseignement Mathématique (2) 25 (1979), 325–344. The finite-interval statement and irrationality question were visually checked on printed p.336, PDF page 12. [Public archive scan](https://users.renyi.hu/~p_erdos/1979-07.pdf).
2. P. Erdős and R. L. Graham, *Old and new problems and results in combinatorial number theory*, Monographies de L’Enseignement Mathématique 28 (1980). The target was visually checked on printed p.20, PDF page 16. The served scan has 124 PDF pages; title and last served page were inspected, but page-by-page completeness is not certified. [Institutional scan](https://www.math.ucsd.edu/~ronspubs/80_11_number_theory.pdf).
3. R. L. Graham, H. S. Witsenhausen, and J. H. Spencer, *On Extremal Density Theorems for Linear Forms*, in H. Zassenhaus (ed.), Number Theory and Algebra, Academic Press (1977), 103–109. This is the printed author order. Section 4, pp.107–108, gives the special-case exact series; Section 5, Theorem 2, p.109, gives a general form. The positive-integer input and maximum-cardinality definition on p.104 were also visually inspected. [Seven-page published reprint](https://www.math.ucsd.edu/~ronspubs/77_05_extremal_density.pdf).

The existence and series are prior results. The present independent derivation verifies the precise conventions used in this checkpoint; it is not a novelty claim.

## Other consulted sources, with limits

4. Fan Chung, Paul Erdős, and Ronald Graham, *On sparse sets hitting linear forms*, Number Theory for the Millennium I, A K Peters (2002), 257–272. The inspected object is a 17-page author copy with internal pagination 1–17. The final typeset chapter was not inspected. Two official author-hosted downloads were byte-identical: [Graham copy](https://www.math.ucsd.edu/~ronspubs/02_04_linear_forms.pdf), [Chung copy](https://cseweb.ucsd.edu/~fan/research/papers/linear.pdf).

   Its f(k) is a minimum hitting size, whereas the f(k) in this package is a maximum avoiding size; the two differ by k. Its numerical bound and conditional decimal are not adopted as established inputs. A statement printed in an inspected source is distinct from a theorem independently verified here. The present d_45 finite example establishes failure of the minimum-single-color identification in the model defined here. No unreviewed numerical-source correction is incorporated into the checkpoint.

5. Nikola Veselinov, *Extremal densities for forbidden configurations in S-smooth numbers*, [arXiv:2604.15515v1](https://arxiv.org/abs/2604.15515v1), submitted 16 April 2026. The canonical inspected object is the [14-page v1 PDF](https://arxiv.org/pdf/2604.15515v1); an [HTML rendering](https://arxiv.org/html/2604.15515v1) is separately identified. On 15 October 2026 the current abstract page listed only v1 and no journal-publication metadata was observed.

   The source distinguishes the extremum within S-smooth numbers from the extremum in a full integer interval. The latter is the original quantity for S={2,3}. Proposition 4.3 and its displayed proof on PDF p.10 were visually inspected. The [authored reciprocal-tail correction](proofs/05_RECIPROCAL_TAIL_CORRECTION.md) proves that its specialized O(1/X) remainder for S={2,3} is false. The correction preserves the exact tail formula, a weaker O(log X/X) bound, and the density-series argument. No claim about other source propositions is inferred from this correction. The classical density series is independently grounded in the 1977 source.

## Access and identity limits

The live [Erdős Problem 168 page](https://www.erdosproblems.com/168) returned HTTP 403 during the recorded check. Its current contents or status are not asserted on that basis. The original public primary documents establish the formulation used here.

[Public dataset identities](sources/DATASET_IDENTITY.json) distinguish a newly rehashed existing snapshot from a fresh remote retrieval. Only public hashes, byte counts, and snapshot metadata are included, never dataset contents. Those identities do not authenticate any earlier authored proof edition. The package contains no historical proof hash presented as a presently verified file.
