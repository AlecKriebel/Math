# Audit of Blaschke compactification comparison

## Finding

**UNSOLVED. Scoped auxiliary results accepted with clarifications.** The missing result is a boundary comparison for every fixed normalized nonmonomial base A in every degree n>2. The packet supplies no actual simultaneous geometric-limit obstruction for even one such base. The five approach families are a faithful account of the investigation; their use is not a measure of proof completion. No novelty or conventional human peer-review claim is supported.

The audit preserves the frozen author archive of 21,759 bytes, SHA-256 3652ecfb4a18b4acabb62df193d7f84f556eecf53cc6fb0d03534be704a30d6e. The author manifest SHA-256 is eeff03be701b9e05d1686b815111cdb85916160537f92561b85e25e32be146e5. All fourteen extracted author files match that archive. Corrections are additive and visible in CORRECTIONS.md.

## Problem identity and interpretation

The two entire pinned public corpora were read and hashed, rather than relying on small extracted records. Their sizes and hashes match the repository manifest. The target is unique by numeric ID, with code AMR-052-0014; the statement hash and canonical joined problem/review hash match the selected catalog. These are identity checks, not evidence of mathematical correctness.

The requested unsolvedmath URL was tried again and remained inaccessible through the web tool. The primary Stony Brook collection was available. Printed pages 7, 8, and 9 were independently inspected as rendered pages and extracted text. They specify origin-fixing disk maps, boundary fixed-point marking, and conformal conjugacy. The actual geometric boundary question appears on printed page 8. The subsequent quasiconformal-quotient question is separate. Hence literal phase monomials are not counterexamples, and neither algebraic source-divisor compactifications nor quasiconformal boundary quotients can replace the target. [Primary collection](https://www.math.stonybrook.edu/preprints/ims92-7.pdf)

The note's marked formulation is an appropriate controlled working setting. A future marked obstruction would still need compatibility with the intended quotient; the note correctly does not claim that arbitrary finite marking can be discarded without proof. The requested homeomorphism is an extension of the common-interior identification, not an arbitrary abstract homeomorphism of two boundary spaces.

## Proof review

### Normalized monomial exclusion

The phase factor making A(1)=1 is correct. If all free zeros vanish, A=z^n. Conversely, the attracting fixed point inside the disk is unique, so a disk conformal conjugacy between the normalized maps fixes 0 and is a rotation. Conjugating e^(it)z^n by z -> cz produces the factor e^(it)c^(n-1), which can be made 1. This removes the artificial phase-monomial exception without weakening the intended nonmonomial condition.

### Proposition 1 Quadratic extension

Accepted in its stated coefficient-normalized, basin-labelled topology. The disk conjugacy calculation gives the degree-two normal form with multiplier lambda. Starting from the existing mating, moving its two attracting fixed points to 0 and infinity and then using the explicit rescaling in C3 gives R(z)=z(z+beta)/(1+alpha z). In the inverse coordinate w=1/z, the map is w(w+alpha)/(1+beta w), so the infinity multiplier is alpha.

The homogeneous polynomials Z(Z+beta W) and W(W+alpha Z) share a zero precisely when alpha beta=1. For fixed |alpha|<1 and |beta|<=1, this cannot occur. The family therefore stays inside the space of genuine quadratic rational maps, including the entire parameter circle. Its coefficient map is continuous and injective on a compact disk, so it is a homeomorphism onto its image; the image equals the closure of the open-disk slice. The continuation of the labelled multiplier beta gives the inverse. C3 records the harmless collision of fixed-point markings at beta=1.

No classification by a single multiplier has been established in higher degree. The proposition cannot serve as a higher-degree parametrization.

### Proposition 2 Fourier witness

Accepted. Logarithmic differentiation on the circle yields the positive Poisson-kernel sum, with mean n. Absolute convergence justifies coefficient extraction. If the first n-1 power sums vanish, Newton's identities force all elementary symmetric functions of the free zeros to vanish, so every free zero is 0. Every nonmonomial normalized base therefore has a nonzero Fourier witness by order n-1 and values of the angular derivative both above and below its mean.

This is genuinely an all-base statement. It remains a statement about dynamical circle derivatives. No inference to a failure of homeomorphic extension of parameter boundaries is provided. The cancellation example correctly prevents replacing the finite range of moments with only the first moment.

### Proposition 3 Harmonic measure rigidity

Accepted, including the direction of absolute continuity. Analytic Fourier moments show that normalized arclength is A-invariant. Schwarz's lemma gives a strict contraction on each compact subdisk, and Cauchy estimates force every fixed Taylor coefficient of powers of A's iterates to vanish. This proves the required Fourier correlations and, by uniform and L1 approximation, uniqueness of an absolutely continuous invariant probability measure.

For nu=h_*m, absolute continuity of h^(-1) sends arclength-null sets to null sets, which is exactly what is needed to conclude nu is absolutely continuous. Invariance and uniqueness then give h_*m=m. An orientation-preserving circle homeomorphism preserving the length of every oriented arc is a rotation. The marking h(1)=1 removes that rotation. No assumption that h itself is absolutely continuous was silently substituted for the stated hypothesis.

The proposed shortcut from this dynamical rigidity to parameter-boundary inequivalence fails: the same rigidity statement holds in degree two, while Proposition 1 gives an extension there. This logical rejection is correct and material.

### Proposition 4 Double-hole degeneration

Accepted after the zero-count correction C2. Homogenizing the exact family gives the common factor (Z+W)^2 at the limit, the reduced map z^(n-2), and a source divisor of multiplicity two at -1. Substituting r=1-epsilon and s=1-c epsilon into the angular derivative gives exactly

    epsilon L_B(-1)=2+2/c+(n-4)epsilon.

This is an algebraic coefficient-pair limit with holes, not a degree-n geometric rational limit. Changing c changes the rescaled rate, but the calculations alone do not identify distinct geometric mating limits.

The imported Cao-Wang-Yin theorem is correctly attributed and applicable to the nonsimple divisor. Compactness of the polynomial target closure converts nonextension into a nonsingleton impression. When n=3, the reduced map is the identity, so the singular-divisor proposition includes z+z^3 in the impression. Neither conclusion specifies which radial paths realize distinct points or compares those points with limits in K_A. The external theorem's proof is not independently reproduced. [Inspected arXiv version](https://arxiv.org/abs/2509.07350v1)

### Proposition 5 Simultaneous graph criterion

Accepted under the stated hypotheses. Compactness and density make both projections from the closed simultaneous graph surjective. If both are injective, each is a compact-to-Hausdorff homeomorphism, giving the required extension. Conversely an extension homeomorphism has a closed graph equal to the closure of the dense interior graph. The two noninjectivity directions correctly distinguish failure of continuous extension from failure of injectivity of an extension.

Cluster-set transport also holds: an extension homeomorphism carries limits of the same parameter sequences forward, and its inverse supplies the reverse inclusion. The two twisting-disk examples are valid. They demonstrate that neither abstract boundary topology nor common failure to extend from a third compactification decides the relative comparison.

The criterion isolates the missing work. It does not produce a nontrivial simultaneous fiber, establish compactness for every possible normalized model, or prove descent through unmarked quotients.

## Current literature and prior-attempt checks

The bounded review on 2026-10-05 found no directly applicable resolution. This is not proof that none exists.

- The publisher confirms Cao, Wang, and Yin's paper appeared on 22 May 2026 in Mathematische Annalen 395, article 69. The mathematical statement used was checked in arXiv v1; the journal PDF was not retrieved. Its target is the polynomial-side Milnor parametrization, not comparison with every rational mating base. [Publisher](https://link.springer.com/article/10.1007/s00208-026-03473-x)
- He, Lee, and Park's arXiv v3 is dated 15 September 2026; the primary publisher-indexed article records 25 September 2026. Its simultaneous uniformization establishes the analytic interior framework. No boundary-comparison conclusion was found there. [arXiv](https://arxiv.org/abs/2507.17077), [publisher record](https://academic.oup.com/imrn/article/2026/19/rnag215/8836186?searchresult=1)
- Luo, Mj, and Mukherjee's v2 is dated 4 May 2026. Its natural closure homeomorphism in the four-punctured-sphere case concerns group-polynomial correspondences. It does not supply the asserted universal rational mating comparison. [arXiv](https://arxiv.org/abs/2504.13107)
- Luo's first degeneration paper concerns polynomial boundary classification and self-bumping; the second gives a convergence theorem under quasi-postcritical-finiteness and nonparallel dual laminations. The audited note does not verify these hypotheses on an obstruction sequence or use them to manufacture incompatible paired limits. [Part I](https://ems.press/content/serial-article-files/31415), [Part II](https://arxiv.org/abs/2102.00357)

Fresh read-only repository checks confirmed the target queue row at rank 794, queued, 0/5. The attempt directory returned 404. Numeric-ID and code PR searches across all states returned no matches; numeric-ID branch and commit searches also returned no matches. The author's default-branch code searches are retained only as bounded historical observations because their index missed the known queue row. No exhaustive historical branch traversal was performed. The live queue's unchanged counter does not invalidate five locally completed approach families; no write updating that queue was authorized in this audit. [Queue](https://github.com/AlecKriebel/Math/blob/main/unsolved_math_prioritization/QUEUE.md)

The upstream OPEN-TRIAGE review explicitly lacked verified literature evidence. Its speculative automorphism-paper association was not treated as a resolution or a skip condition. No prior proof artifact was located.

## Reproducibility and distribution

The preserved author regressions reproduce their exact expected output. Independent code differentiates coefficient polynomials rather than reusing the author's Poisson expression: it checks 132 circle-derivative cases, 96 quadratic cases including all three fixed-point multipliers, and 165 double-hole cases. It also checks 15 Newton identities, a case with the first possible witness only at the fourth moment, and all 265 surjective relations on two three-element sets. These are finite controls only.

Positive replays under normal Python, -O, and -OO, relocation, and adversarial integrity tests are recorded in INTEGRITY_RESULTS.json. Source identities were recomputed against complete inputs, and all six held public PDFs match their recorded hashes and sizes. Reproducibility does not turn finite tests into proofs of analytic or topological statements.

The outer manifest binds the complete safe bundle, including the immutable author archive, corrected status, report, code, and results. No scholarly PDF, extracted page, image, corpus, source record, or private coordination file is distributed. No remote state was changed.

## Remaining mathematical task

For each n>2 and each normalized A outside the monomial conjugacy class, establish incompatible simultaneous limits of M_0 and M_A along the same interior parameters, with genuine degree-n geometric limits and compatible marking or quotient conventions, or give another argument that proves the required nonextension. This remains wholly unproved by the available auxiliary lemmas. The appropriate disposition is UNSOLVED with audited scoped partial results.
