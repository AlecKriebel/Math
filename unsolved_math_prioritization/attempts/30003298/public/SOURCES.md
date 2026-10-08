# Source scope, conventions, and duplicate gate

Checked 7–8 October 2026 UTC. This is a bounded literature investigation, not a claim to have established worldwide current open status.

## Exact primary problem

The official [Surface Bundles report, 56/2016](https://publications.mfo.de/handle/mfo/3560), [PDF](https://publications.mfo.de/bitstream/handle/mfo/3560/OWR_2016_56.pdf?sequence=1), [publisher DOI](https://doi.org/10.4171/OWR/2016/56), printed p.3190, Question 11, attributes the question to Grigori Avramidi. The formula has outer COHOMOLOGY in degree 2g-1 and coefficient HOMOLOGY in degree 2g-2. This was checked in the rendered page, not inferred solely from extracted superscripts.

The printed question fixes a torsion-free finite-index subgroup Gamma of Mod_g. It asks about that subgroup, so the natural general interpretation is every such Gamma, not merely existence of a favorable congruence subgroup. The short local question does not print a genus range or explicitly define C_g. The surrounding mapping-class setting and Avramidi's directly related manuscript use the curve complex of a closed orientable surface with g>=2. That standard range is stated explicitly throughout this packet; no genus-zero or genus-one answer is claimed. The source has no rational-coefficient qualifier; the source question is treated integrally. Rational infinite rank suffices for an affirmative answer.

The supplied corpus's corrected statement agrees with the displayed homology subscript. Its older 'universal curve' and cohomology-coefficient transcription must not be used. The report is identified as 2016 by the official repository even though a supplied citation labels it 2017. The report covers the December 2016 workshop. No mathematical conclusion depends on that bibliographic discrepancy.

## Main theorem's published dependencies

1. Neil J. Fullarton and Andrew Putman, [The high-dimensional cohomology of the moduli space of curves with level structures](https://arxiv.org/abs/1610.03768), J. Eur. Math. Soc. 22 (2020), no.4, 1261–1287, [DOI](https://doi.org/10.4171/JEMS/945). The [author PDF](https://academicweb.nd.edu/~andyp/papers/HighLevel.pdf) is dated 29 November 2017. Inspected §2, all of §3, Proposition 3.11 and the relevant §5 dimension calculation; visually checked pp.9 and 11. The equivariance paragraph preceding Proposition 3.10 is essential. The current arXiv landing page confirms v2 and the journal reference. The publisher DOI did not resolve through the web reader, so no final-typeset-PDF inspection is claimed.
2. Thomas Church, Benson Farb, and Andrew Putman, [The rational cohomology of the mapping class group vanishes in its virtual cohomological dimension](https://academicweb.nd.edu/~andyp/papers/TopCohomologyMod.pdf). Inspected the complete four-page author PDF and visually checked p.2, where the general-coefficient duality formula and the thick-Teichmüller compactification appear. This source is used as a primary account of Harer's duality, not to identify untwisted top cohomology with the target.
3. John L. Harer, *The virtual cohomological dimension of the mapping class group of an orientable surface*, Invent. Math. 84 (1986), 157–176, as credited and applied in the two directly inspected papers above. No separate newly retrieved original-paper PDF is claimed.

## Directly relevant later manuscript and other literature

Grigori Avramidi, [Incompressible fillings of manifolds](https://arxiv.org/abs/1701.00309), v1, submitted 2 January 2017. The [current author publication list](https://sites.google.com/site/gavramidi/papers) describes this work as under revision. The arXiv landing page lists only v1. Inspected pp.2–5, §§1–3, and §§6,9–10; visually checked p.19. Its small-model argument motivates the conditional boundary criterion and its Problem 19 asks a broader dualizing-module question. It is not cited as a published resolution of the present problem. The retained top-degree theorem is independent of it.

The [Brendle–Broaddus–Putman continuation](https://arxiv.org/abs/2003.10913) concerns punctures/boundary and ordinary cohomology of congruence subgroups in virtual cohomological dimension. Its landing-page scope was checked; it is not a result about the exact twisted group here. The 2026 [Petersen–Wade handlebody duality paper](https://jep.centre-mersenne.org/articles/10.5802/jep.341/) was a later search hit, but its group and dualizing module are different. Its abstract does not settle the surface mapping-class target. These papers were not downloaded as dependencies.

Targeted searches covered the exact formula, Avramidi/curve-complex obstruction, infinite generation with the Steinberg module, and tensor-square/finite-quotient language. No checked source was found that resolves the degree 2g-1 for all g>=3. Absence from these searches is not a proof that no such source exists. The genus-two corollary proved here could be known or implicit; no priority claim is attached to it.

## Inherited substantive/semantic duplicate check

Read-only searches of AlecKriebel/Math found no exact-ID PR, code hit, or branch for 30003298/OWR-15177-016, and no matching prior work under Avramidi or Infinite Generation. Branch keyword searches covered Steinberg, mapping, mapping-class, and cohomology, including the returned cohomology continuation page. Local artifacts were scanned for the ID/title/code; observed hits were queue copies rather than an existing proof packet.

The closest result was [PR82](https://github.com/AlecKriebel/Math/pull/82), for problem 30001804. Its metadata and substantive patch concern a conditional noncommutative presentation/certificate reduction for Steinberg-module relations. They do not address infinite generation of H^(2g-1)(Gamma;D_Z), invariant finite-rank pairings, or the genus-two deduction. That existing work is not being counted again. [PR379](https://github.com/AlecKriebel/Math/pull/379) concerns a different group-ring-cohomology finiteness problem, with different coefficients and target. Broader searches yielded unrelated surface/group-cohomology PRs rather than an exact semantic duplicate.

The supplied research_results.json has 6,701 records, no OWR-prefixed keys, and no exact matching report for this problem. Its absence is recorded rather than replacing it with another problem's research result. Repository search is bounded by its indexed scope and the inspected branches/artifacts; it is not an assertion that every private or unindexed historical branch was exhaustively inspected. No substantive prior attempt at this exact target was found in the inspected evidence, so investigation proceeded.

## Numerical source-reading caution

The introductory sample bounds in Fullarton–Putman Remark 1.1 are not used as exact dimensions. Direct evaluation of Proposition 3.11 gives dim(V_3)=324 at g=2 and dim(V_2)=7680 at g=3, whereas the displayed introductory cohomology bounds are respectively 216 and 11520. A cohomology lower bound is a different assertion from an exact quotient dimension. The proof uses Proposition 3.11 and its formula, whose partition recurrence was checked in bounded exact arithmetic. No claim that these finite checks prove the source theorem, or refute its cohomology bounds, is made.
