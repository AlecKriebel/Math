# Rational-point undecidability for smooth projective varieties over the rational numbers

Alec Kriebel · 6 October 2026 · Preprint

Can an algorithm always decide whether a geometric object defined by rational equations has a rational point? This note derives a negative answer for the full promised class of smooth projective geometrically integral varieties over ℚ, using Poonen’s established transfer and the newly released OpenAI arithmetic preprints with two explicit technical substitutions. It also derives a noncomputability result for the height of a smallest rational point.

## Original readers

[Main paper](paper.pdf) · [A conditional coefficient-prime repair of the five-point height argument](height-repair.pdf)

## Original files

- [source.zip](source.zip)

- [verification.zip](verification.zip)

- [paper.pdf](paper.pdf)

- [height-repair.pdf](height-repair.pdf)

[Original Zenodo record](https://zenodo.org/records/23205305) · [DOI](https://doi.org/10.5281/zenodo.23205305) · [BibTeX](citation.bib)

## Full printed abstract — main paper

Combining OpenAI’s negative solution of rational Hilbert’s tenth problem with Poonen’s established effective transfer, we obtain undecidability of rational-point existence for arbitrary smooth projective geometrically integral varieties over ℚ. We specify a homogeneous-equation input promise and reconstruct the terminating contradiction algorithm. There is also no computable uniform bound on the height of one rational point in terms of the size of the presented equations. The arithmetic input is used with two explicit corrections documented here and in the accompanying verification supplement. This is a geometric consequence of that input; neither the geometric reduction nor the base undecidability theorem is claimed as a new independent solution.

## Full printed abstract — A conditional coefficient-prime repair of the five-point height argument

We reconstruct the non-CM arithmetic part of the five-point height argument in the pinned source [1], replacing its new unrestricted 2-adic modularity input by Pan’s published theorem at 5. The 2-adic member of the resulting system supplies the conductor at 5. The deduction is conditional on the preceding geometric and height-comparison inputs stated below; it neither certifies the entire upstream manuscript nor establishes undecidability of rational polynomial solvability.

[1] refers to the first reference below.

## What the main result says

The input is a finite homogeneous-equation presentation of a smooth projective geometrically integral variety over ℚ. Ambient dimension, variety dimension, degrees, number of equations and coefficient heights may all vary. The promise concerns the geometric object presented; an algorithm is required to terminate and answer correctly on every valid input. The note derives that no such algorithm decides whether a rational point exists.

The second conclusion concerns one point when points exist. For a rational projective point, choose primitive integer coordinates with the first nonzero coordinate positive; its height is the largest absolute coordinate. With s(e) the bit length of the specified presentation and embedding, no total computable function B(s(e)) uniformly bounds the height of a smallest rational point. Such a bound would turn a finite search through coordinate vectors into a decision algorithm. This is a computability statement, not a numerical height estimate for a particular variety.

## How the consequence is obtained

Poonen’s effective construction transfers rational-point existence from an affine input to a finite collection of smooth projective candidates. Effective component and geometric-integrality tests ensure that only valid promised inputs reach the hypothetical decision procedure. The resulting reduction makes finitely many nonadaptive disjunctive oracle queries. Naive projective closure or resolution alone cannot replace this transfer, because boundary points can be introduced or rational singular points can be lost.

The arithmetic undecidability input is OpenAI’s Hilbert’s tenth problem over the rational numbers, together with the needed non-CM, full-rational-two-torsion branch of A pointwise 2-converse for elliptic curves with rational two-torsion. Both are new OpenAI Math Release preprints dated 24 September 2026, used at source commit adc7f1241b42e322a6451854ab7e4b4c146bf78a. They are substantive arithmetic dependencies. This note makes their use and the following two substitutions explicit.

- In the five-point height argument, published Pan modularity at coefficient prime 5 replaces the new unrestricted 2-adic modularity input. The compatible 2-adic constituent of the same system supplies the conductor at 5. The coefficient pair is (5, 2).

- In the pointwise-converse determinant argument, an integral universal group-ring correction reconciles inverse/direct Frobenius-Euler conventions and the smoothing factors before character evaluation. The correction preserves the central valuations without adding a factor of two for every auxiliary prime.

## The companion’s conditional theorem

The four-page companion isolates the coefficient-prime substitution. Its theorem explicitly assumes three preceding inputs: a fixed proper cover with its principally polarized abelian-surface family, bounded defining field and reduction control; the fixed quaternionic non-CM/CM dichotomy with a uniform CM Faltings-height bound; and the comparison from base height to stable Faltings height. These retained inputs are separate from Pan’s modularity theorem.

The five points are the individually rational branch values of the fixed discriminant-210 quaternionic quotient, labelled by the distinct involutions 30, 42, 70, 105 and 210. For a rational parameter s outside those branch values, M_S(s) is the product of primes outside a fixed exceptional set S at which at least one branch-contact order is odd. Assuming the three inputs, the companion derives h(s) ≤ H M_S(s)^c for fixed constants H, c > 0. It treats this fixed configuration, not arbitrary five rational points.

The companion does not by itself certify the whole upstream manuscript or establish undecidability of rational polynomial solvability. The main note uses the wider corrected arithmetic argument as well as the geometric transfer.

## Scope and credit

The geometric reduction belongs to Bjorn Poonen’s Existence of rational points on smooth projective varieties (2009). Poonen also credits an earlier ℚ-case route to R. Robinson through Smoryński. The new arithmetic input belongs to the cited OpenAI preprints. The connection between least-point height bounds and rational Hilbert’s tenth problem also has prior literature, including Skorobogatov and Sofos.

The consequence supplies neither a new independent solution of rational Hilbert’s tenth problem nor a new geometric reduction or first-priority claim. It establishes no fixed-curve, fixed-surface or fixed-dimension result, and no automatic Fano, general-type or finite-point-promise extension. A single-output many-one reduction, a specified Turing degree and quantitative reduction bounds are not asserted.

## Status, AI use and collaboration

AI tools were used extensively in the research, drafting and adversarial verification. This work and its new arithmetic preprint dependencies should be read with their unrefereed status in view. The deposited preprint has not undergone conventional human peer review or refereeing. Automated reviews and finite checks do not constitute formal verification of the complete theorem.

Substantive mathematical contributions to corrections or extensions are welcome. Collaboration, authorship and credit would reflect actual contributions.

## Original Zenodo description

Separate full deposit description; distinct from the printed abstracts.

Combining OpenAI's negative solution of rational Hilbert's tenth problem, with two explicit proof corrections documented in the verification package, and Poonen's established effective transfer, this note proves undecidability of rational-point existence for arbitrary smooth projective geometrically integral varieties over Q. It specifies homogeneous-equation presentations and valid-input oracle use, and rules out a computable uniform bound on the height of one point in terms of presentation size. Dimension and all size parameters may vary. The arithmetic breakthrough is attributed to OpenAI and the geometric reduction to Poonen; no independent solution of rational Hilbert's tenth problem, new geometric reduction, fixed-dimensional theorem, many-one hardness or first-priority claim is made. AI tools were used extensively in research, drafting and adversarial verification. The preprint has not undergone conventional human peer review or refereeing at publication; no complete formal verification is claimed. The standalone height supplement explicitly states its retained geometric inputs.

## References and source credit

- [OpenAI, Hilbert’s tenth problem over the rational numbers, preprint (24 September 2026), pinned source.](https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Hilberts-tenth-problem-over-the-rational-numbers-September-24-2026)

- [OpenAI, A pointwise 2-converse for elliptic curves with rational two-torsion, preprint (24 September 2026), same pinned source.](https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-pointwise-2-converse-for-elliptic-curves-with-rational-two-torsion-September-24-2026)

- [Bjorn Poonen, Existence of rational points on smooth projective varieties (2009).](https://doi.org/10.4171/JEMS/159)

- [Lue Pan, The Fontaine–Mazur conjecture in the residually reducible case (2022), Theorem 1.0.4.](https://doi.org/10.1090/jams/991)

- [Alexei N. Skorobogatov and Efthymios Sofos, Schinzel Hypothesis on average and rational points (2023), §1.2.](https://doi.org/10.1007/s00222-022-01153-6)

Pinned OpenAI source commit: adc7f1241b42e322a6451854ab7e4b4c146bf78a

## Licensing

Original manuscript, supplement, prose and first-party research documentation are licensed CC BY 4.0. The original verification code is MIT-licensed. These distinct terms are recorded in the deposited LICENSES.md files; the mixed source and verification ZIPs have no blanket single-license assignment. Referenced OpenAI material and other third-party works retain their own rights.
